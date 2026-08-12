// backend/regulatory_monitor.js

const axios = require('axios');
const { Pool } = require('pg');

class RegulatoryMonitor {
  constructor(pool) {
    this.pool = pool;
    this.alerts = [];
  }

  /**
   * CA Competes Tax Credit Monitoring
   * $1.22M over 5 years requires job creation milestones
   */
  async monitorCACompetesCompliance() {
    const client = await this.pool.connect();
    
    try {
      // Query payroll data
      const payrollQuery = `
        SELECT 
          COUNT(DISTINCT employee_id) as total_employees,
          SUM(CASE WHEN hire_date >= '2026-01-01' THEN 1 ELSE 0 END) as new_hires_2026,
          AVG(hourly_rate) as avg_wage
        FROM payroll
        WHERE employment_status = 'active'
      `;
      
      const result = await client.query(payrollQuery);
      const data = result.rows[0];
      
      // CA Competes requires 20 new jobs at $25/hour minimum
      const compliance = {
        requirement: {
          new_jobs: 20,
          min_wage: 25.00,
          measurement_period: '2026-2030'
        },
        actual: {
          new_jobs: data.new_hires_2026,
          avg_wage: parseFloat(data.avg_wage)
        },
        status: 'compliant',
        risk_level: 'low'
      };
      
      // Risk assessment
      if (data.new_hires_2026 < 20) {
        compliance.status = 'at_risk';
        compliance.risk_level = 'high';
        compliance.gap = 20 - data.new_hires_2026;
        
        await this.triggerAlert({
          type: 'ca_competes_risk',
          severity: 'critical',
          message: `Job creation shortfall: ${compliance.gap} jobs needed`,
          action_required: 'Accelerate hiring to meet tax credit requirements'
        });
      }
      
      if (data.avg_wage < 25.00) {
        compliance.status = 'non_compliant';
        compliance.risk_level = 'critical';
        
        await this.triggerAlert({
          type: 'ca_competes_wage_violation',
          severity: 'critical',
          message: `Avg wage $${data.avg_wage} below $25/hour requirement`,
          action_required: 'Increase wages or risk $1.22M credit clawback'
        });
      }
      
      return compliance;
      
    } finally {
      client.release();
    }
  }

  /**
   * HVIP Voucher Eligibility Monitoring
   * $330K per Semi requires CA-only operation
   */
  async monitorHVIPCompliance() {
    const client = await this.pool.connect();
    
    try {
      // Query GPS data for all Tesla Semis
      const gpsQuery = `
        SELECT 
          vehicle_id,
          COUNT(*) as total_hauls,
          SUM(CASE WHEN state != 'CA' THEN 1 ELSE 0 END) as out_of_state_hauls,
          MAX(gps_coordinates->>'state') as last_state
        FROM transactions t
        JOIN transaction_reconciliation tr ON t.id = tr.transaction_id
        WHERE vehicle_type = 'Tesla Semi'
          AND timestamp >= NOW() - INTERVAL '12 months'
        GROUP BY vehicle_id
      `;
      
      const result = await client.query(gpsQuery);
      
      const violations = result.rows.filter(row => 
        row.out_of_state_hauls > 0
      );
      
      if (violations.length > 0) {
        for (const violation of violations) {
          await this.triggerAlert({
            type: 'hvip_violation',
            severity: 'critical',
            vehicle_id: violation.vehicle_id,
            message: `Vehicle operated outside CA: ${violation.out_of_state_hauls} hauls`,
            financial_impact: '$330,000 voucher at risk',
            action_required: 'Immediate review of vehicle routing protocols'
          });
        }
        
        return {
          status: 'non_compliant',
          violations: violations.length,
          financial_risk: violations.length * 330000
        };
      }
      
      return {
        status: 'compliant',
        vehicles_monitored: result.rows.length,
        financial_secured: result.rows.length * 330000
      };
      
    } finally {
      client.release();
    }
  }

  /**
   * Real-time mileage tracking for HVIP
   */
  async trackHVIPMileageRequirements() {
    // HVIP requires 25,000 CA miles per year minimum
    const client = await this.pool.connect();
    
    try {
      const mileageQuery = `
        SELECT 
          vehicle_id,
          SUM(gps_total_distance) as total_miles,
          MIN(driver_timestamp) as first_haul,
          MAX(driver_timestamp) as last_haul
        FROM transaction_reconciliation
        WHERE 
          cesar_controller_id LIKE 'SEMI-%'
          AND driver_timestamp >= DATE_TRUNC('year', CURRENT_DATE)
        GROUP BY vehicle_id
      `;
      
      const result = await client.query(mileageQuery);
      
      const compliance = result.rows.map(row => {
        const daysElapsed = Math.floor(
          (new Date() - new Date(row.first_haul)) / (1000 * 60 * 60 * 24)
        );
        const expectedMiles = (25000 / 365) * daysElapsed;
        const complianceRate = row.total_miles / expectedMiles;
        
        return {
          vehicle_id: row.vehicle_id,
          actual_miles: parseFloat(row.total_miles),
          expected_miles: expectedMiles,
          compliance_rate: complianceRate,
          status: complianceRate >= 0.9 ? 'on_track' : 'at_risk'
        };
      });
      
      // Alert on vehicles falling behind
      const atRisk = compliance.filter(v => v.status === 'at_risk');
      if (atRisk.length > 0) {
        await this.triggerAlert({
          type: 'hvip_mileage_shortfall',
          severity: 'medium',
          vehicles: atRisk.length,
          message: `${atRisk.length} vehicles below mileage trajectory`,
          action_required: 'Increase utilization to meet 25K annual requirement'
        });
      }
      
      return compliance;
      
    } finally {
      client.release();
    }
  }

  /**
   * Alert aggregation and distribution
   */
  async triggerAlert(alert) {
    this.alerts.push({
      ...alert,
      timestamp: new Date().toISOString()
    });
    
    // Persist to database
    await this.pool.query(
      `INSERT INTO regulatory_alerts 
       (alert_type, severity, message, metadata, created_at)
       VALUES ($1, $2, $3, $4, NOW())`,
      [alert.type, alert.severity, alert.message, JSON.stringify(alert)]
    );
    
    // Real-time notification to auditor dashboard
    if (alert.severity === 'critical') {
      await axios.post(
        `${process.env.AUDITOR_DASHBOARD_URL}/alerts/critical`,
        alert
      );
    }
  }

  /**
   * Daily compliance report
   */
  async generateComplianceReport() {
    const [caCompetes, hvipEligibility, hvipMileage] = await Promise.all([
      this.monitorCACompetesCompliance(),
      this.monitorHVIPCompliance(),
      this.trackHVIPMileageRequirements()
    ]);
    
    return {
      timestamp: new Date().toISOString(),
      ca_competes: caCompetes,
      hvip_eligibility: hvipEligibility,
      hvip_mileage: hvipMileage,
      overall_status: this.computeOverallStatus([
        caCompetes.status,
        hvipEligibility.status
      ]),
      financial_at_risk: this.computeFinancialRisk([
        caCompetes,
        hvipEligibility
      ])
    };
  }

  computeOverallStatus(statuses) {
    if (statuses.includes('non_compliant')) return 'non_compliant';
    if (statuses.includes('at_risk')) return 'at_risk';
    return 'compliant';
  }

  computeFinancialRisk(results) {
    let risk = 0;
    
    // CA Competes risk
    if (results[0].status !== 'compliant') {
      risk += 1220000; // Full $1.22M at risk
    }
    
    // HVIP risk
    if (results[1].status === 'non_compliant') {
      risk += results[1].financial_risk || 0;
    }
    
    return risk;
  }
}

module.exports = RegulatoryMonitor;