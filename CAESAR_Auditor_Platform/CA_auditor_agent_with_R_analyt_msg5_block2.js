// backend/reconciliation_engine.js

const { Pool } = require('pg');
const axios = require('axios');
const crypto = require('crypto');

class ReconciliationEngine {
  constructor(pool) {
    this.pool = pool;
    this.VARIANCE_THRESHOLD = 0.05; // 5% tolerance
  }

  /**
   * Master reconciliation function
   * Runs after every haul completion
   */
  async reconcileTransaction(transactionId) {
    const client = await this.pool.connect();
    
    try {
      await client.query('BEGIN');
      
      // Step 1: Gather data from all three layers
      const operationalData = await this.fetchOperationalData(transactionId);
      const financialData = await this.fetchFinancialData(transactionId);
      const environmentalData = await this.fetchEnvironmentalData(transactionId);
      
      // Step 2: Calculate variances
      const variances = this.calculateVariances(
        operationalData,
        financialData,
        environmentalData
      );
      
      // Step 3: Compute integrity score
      const integrityScore = this.computeIntegrityScore(variances);
      
      // Step 4: Determine reconciliation status
      const status = this.determineStatus(integrityScore, variances);
      
      // Step 5: Persist reconciliation record
      const insertQuery = `
        INSERT INTO transaction_reconciliation (
          transaction_id,
          gps_coordinates, gps_total_distance, load_manifest_hash,
          driver_signature_hash, driver_timestamp,
          haul_token_amount, haul_token_tx_hash, usd_payment_amount,
          usd_settlement_timestamp, carbon_tokens_minted, carbon_mint_tx_hash,
          energy_discharged_kwh, cesar_controller_id, grid_settlement_id,
          battery_soc_start, battery_soc_end, caiso_settlement_amount,
          integrity_score, gps_variance_pct, energy_variance_pct,
          financial_variance_pct, reconciliation_status,
          reconciled_at, reconciled_by
        ) VALUES (
          $1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15,
          $16, $17, $18, $19, $20, $21, $22, $23, NOW(), 'system'
        ) RETURNING id
      `;
      
      await client.query(insertQuery, [
        transactionId,
        operationalData.gps_coordinates,
        operationalData.gps_total_distance,
        operationalData.load_manifest_hash,
        operationalData.driver_signature_hash,
        operationalData.driver_timestamp,
        financialData.haul_token_amount,
        financialData.haul_token_tx_hash,
        financialData.usd_payment_amount,
        financialData.usd_settlement_timestamp,
        financialData.carbon_tokens_minted,
        financialData.carbon_mint_tx_hash,
        environmentalData.energy_discharged_kwh,
        environmentalData.cesar_controller_id,
        environmentalData.grid_settlement_id,
        environmentalData.battery_soc_start,
        environmentalData.battery_soc_end,
        environmentalData.caiso_settlement_amount,
        integrityScore,
        variances.gps_variance_pct,
        variances.energy_variance_pct,
        variances.financial_variance_pct,
        status
      ]);
      
      await client.query('COMMIT');
      
      // Step 6: Alert if critical variance
      if (integrityScore < 0.85 || status === 'exception') {
        await this.triggerAuditorAlert(transactionId, integrityScore, variances);
      }
      
      return {
        success: true,
        integrity_score: integrityScore,
        status: status,
        variances: variances
      };
      
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  /**
   * Fetch operational layer data
   */
  async fetchOperationalData(transactionId) {
    // Query GPS data from Route Optimization Agent
    const gpsResponse = await axios.get(
      `${process.env.ROUTE_AGENT_URL}/gps/${transactionId}`
    );
    
    // Query load manifest
    const manifestResponse = await axios.get(
      `${process.env.ROUTE_AGENT_URL}/manifest/${transactionId}`
    );
    
    // Calculate manifest hash for immutability
    const manifestHash = crypto
      .createHash('sha256')
      .update(JSON.stringify(manifestResponse.data.vehicle_vins.sort()))
      .digest('hex');
    
    return {
      gps_coordinates: gpsResponse.data.waypoints,
      gps_total_distance: gpsResponse.data.total_miles,
      load_manifest_hash: manifestHash,
      driver_signature_hash: manifestResponse.data.driver_signature,
      driver_timestamp: manifestResponse.data.signature_timestamp
    };
  }

  /**
   * Fetch financial layer data
   */
  async fetchFinancialData(transactionId) {
    // Query blockchain for $HAUL token settlement
    const tokenTx = await this.queryBlockchain(transactionId, 'HAUL');
    
    // Query USD payment system
    const usdPayment = await axios.get(
      `${process.env.PAYMENT_API_URL}/settlements/${transactionId}`
    );
    
    // Query $CARBON token minting event
    const carbonTx = await this.queryBlockchain(transactionId, 'CARBON');
    
    return {
      haul_token_amount: tokenTx.amount,
      haul_token_tx_hash: tokenTx.hash,
      usd_payment_amount: usdPayment.data.amount,
      usd_settlement_timestamp: usdPayment.data.settled_at,
      carbon_tokens_minted: carbonTx.amount,
      carbon_mint_tx_hash: carbonTx.hash
    };
  }

  /**
   * Fetch environmental layer data
   */
  async fetchEnvironmentalData(transactionId) {
    // Query CESAR controller
    const cesarResponse = await axios.get(
      `${process.env.CESAR_API_URL}/discharge/${transactionId}`
    );
    
    // Query CAISO settlement
    const caisoResponse = await axios.get(
      `${process.env.CAISO_API_URL}/settlements/${cesarResponse.data.settlement_id}`
    );
    
    return {
      energy_discharged_kwh: cesarResponse.data.kwh_discharged,
      cesar_controller_id: cesarResponse.data.controller_id,
      grid_settlement_id: cesarResponse.data.settlement_id,
      battery_soc_start: cesarResponse.data.soc_start,
      battery_soc_end: cesarResponse.data.soc_end,
      caiso_settlement_amount: caisoResponse.data.payment_amount
    };
  }

  /**
   * Calculate variances between expected and actual
   */
  calculateVariances(operational, financial, environmental) {
    // Expected distance based on route optimization
    const expectedDistance = 350; // miles (avg CA haul)
    const gpsVariance = Math.abs(
      (operational.gps_total_distance - expectedDistance) / expectedDistance
    ) * 100;
    
    // Expected energy discharge: 1.7 kWh per mile
    const expectedEnergy = operational.gps_total_distance * 1.7;
    const energyVariance = Math.abs(
      (environmental.energy_discharged_kwh - expectedEnergy) / expectedEnergy
    ) * 100;
    
    // Expected revenue: $400 per haul + carbon credits
    const expectedRevenue = 400 + 24.68; // base + carbon
    const actualRevenue = financial.usd_payment_amount;
    const financialVariance = Math.abs(
      (actualRevenue - expectedRevenue) / expectedRevenue
    ) * 100;
    
    return {
      gps_variance_pct: gpsVariance,
      energy_variance_pct: energyVariance,
      financial_variance_pct: financialVariance
    };
  }

  /**
   * Compute integrity score (weighted average)
   */
  computeIntegrityScore(variances) {
    // Weights: GPS 30%, Energy 40%, Financial 30%
    const gpsScore = Math.max(0, 1 - (variances.gps_variance_pct / 100));
    const energyScore = Math.max(0, 1 - (variances.energy_variance_pct / 100));
    const financialScore = Math.max(0, 1 - (variances.financial_variance_pct / 100));
    
    return (gpsScore * 0.3 + energyScore * 0.4 + financialScore * 0.3);
  }

  /**
   * Determine reconciliation status
   */
  determineStatus(integrityScore, variances) {
    if (integrityScore >= 0.95 && 
        variances.gps_variance_pct < 5 &&
        variances.energy_variance_pct < 5 &&
        variances.financial_variance_pct < 5) {
      return 'verified';
    } else if (integrityScore >= 0.85) {
      return 'review';
    } else {
      return 'exception';
    }
  }

  /**
   * Query blockchain for transaction
   */
  async queryBlockchain(transactionId, tokenType) {
    // Implementation depends on blockchain (Ethereum, Polygon, etc.)
    // This is a placeholder for actual Web3 integration
    const response = await axios.get(
      `${process.env.BLOCKCHAIN_RPC}/query`,
      {
        params: {
          transaction_id: transactionId,
          token_type: tokenType
        }
      }
    );
    
    return response.data;
  }

  /**
   * Trigger alert to auditor
   */
  async triggerAuditorAlert(transactionId, integrityScore, variances) {
    // Send to Rebecca McNeil's dashboard
    await axios.post(
      `${process.env.AUDITOR_DASHBOARD_URL}/alerts`,
      {
        transaction_id: transactionId,
        integrity_score: integrityScore,
        variances: variances,
        priority: integrityScore < 0.75 ? 'critical' : 'high',
        timestamp: new Date().toISOString()
      }
    );
  }
}

module.exports = ReconciliationEngine;