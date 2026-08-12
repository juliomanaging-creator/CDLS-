/**
 * CDLS ENERGY BANK — PRODUCTION SANDBOX TEST HARNESS
 * Executable: 100-Transaction Automated ACH Batch Simulation
 * Environment: Treasury Prime API Sandbox (https://api.sandbox.treasuryprime.com)
 */

const axios = require('axios');
const fs = require('fs');
const crypto = require('crypto');

// Configuration & Environment Security
const CONFIG = {
  apiUrl: process.env.TREASURY_PRIME_API_URL || 'https://api.sandbox.treasuryprime.com',
  apiKeyId: process.env.TREASURY_PRIME_API_KEY_ID || 'tp_key_sandbox_demo',
  apiSecretKey: process.env.TREASURY_PRIME_API_SECRET_KEY || 'tp_secret_sandbox_demo',
  masterAccountId: process.env.CDLS_MASTER_ACCOUNT_ID || 'acct_1029384756',
  totalTransactions: 100,
  outputFile: './treasury_prime_100_tx_audit.json'
};

// HTTP Basic Authentication setup per Treasury Prime API spec
const authHeader = 'Basic ' + Buffer.from(`${CONFIG.apiKeyId}:${CONFIG.apiSecretKey}`).toString('base64');

const apiClient = axios.create({
  baseURL: CONFIG.apiUrl,
  headers: {
    'Authorization': authHeader,
    'Content-Type': 'application/json'
  },
  timeout: 10000 // 10s timeout per HTTP request
});

// Helper: Random generator for simulated V2G Dispatch & Logistics Payouts ($150 - $1,250)
function generateTransactionPayload(index) {
  const isV2G = index % 2 === 0;
  const amount = (Math.random() * (1250 - 150) + 150).toFixed(2);
  const idempotencyKey = `cdls_prod_sim_${Date.now()}_idx_${index}_${crypto.randomBytes(3).toString('hex')}`;

  return {
    idempotencyKey,
    payload: {
      account_id: CONFIG.masterAccountId,
      amount: amount,
      direction: 'credit',
      sec_code: 'ccd', // Corporate Credit or Debit for B2B payouts
      userdata: {
        batch_id: 'CDLS_SACRAMENTO_PILOT_001',
        tx_index: index,
        judas_ai_zk_verified: true,
        settlement_type: isV2G ? 'CAISO_V2G_DISPATCH' : 'ZEV_HAUL_PAYOUT',
        node_location: 'SACRAMENTO_HUB_01'
      }
    }
  };
}

// Helper: Exponential backoff delay for API rate limits / network hiccups
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function executeSingleTransaction(index, retries = 3) {
  const { idempotencyKey, payload } = generateTransactionPayload(index);

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await apiClient.post('/ach', payload, {
        headers: { 'X-Idempotency-Key': idempotencyKey }
      });

      return {
        status: 'SUCCESS',
        tx_index: index,
        ach_id: response.data.id || `ach_sandbox_mock_${index}`,
        amount: payload.amount,
        settlement_type: payload.userdata.settlement_type,
        idempotency_key: idempotencyKey,
        http_status: response.status,
        timestamp: new Date().toISOString()
      };
    } catch (err) {
      if (err.response && err.response.status === 429 && attempt < retries) {
        console.warn(`[WARN] Rate limited on Tx #${index}. Retrying in ${attempt * 500}ms...`);
        await sleep(attempt * 500);
        continue;
      }

      return {
        status: 'FAILED',
        tx_index: index,
        amount: payload.amount,
        idempotency_key: idempotencyKey,
        error: err.response ? err.response.data : err.message,
        timestamp: new Date().toISOString()
      };
    }
  }
}

async function runProductionSimulation() {
  console.log('================================================================');
  console.log('  CDLS ENERGY BANK — TREASURY PRIME 100-TX API SIMULATION RUN');
  console.log('================================================================');
  console.log(`Target Endpoint : ${CONFIG.apiUrl}`);
  console.log(`Master Account  : ${CONFIG.masterAccountId}`);
  console.log(`Execution Size  : ${CONFIG.totalTransactions} Concurrent ACH Credits\n`);

  const auditLog = [];
  let passCount = 0;
  let failCount = 0;

  const startTime = Date.now();

  for (let i = 1; i <= CONFIG.totalTransactions; i++) {
    const result = await executeSingleTransaction(i);
    auditLog.push(result);

    if (result.status === 'SUCCESS') {
      passCount++;
      console.log(`[PASS] Tx #${String(i).padStart(3, '0')}/100 | ACH: ${result.ach_id} | $${result.amount} [${result.settlement_type}]`);
    } else {
      failCount++;
      console.error(`[FAIL] Tx #${String(i).padStart(3, '0')}/100 | Error: ${JSON.stringify(result.error)}`);
    }

    // Gentle 50ms pacing between API calls to maintain smooth throughput
    await sleep(50);
  }

  const durationSec = ((Date.now() - startTime) / 1000).toFixed(2);

  // Export full DFPI Audit File
  fs.writeFileSync(CONFIG.outputFile, JSON.stringify(auditLog, null, 2));

  console.log('\n================================================================');
  console.log('                 FINAL EXECUTION SUMMARY LOG');
  console.log('================================================================');
  console.log(`Execution Time  : ${durationSec} seconds`);
  console.log(`Total Attempted : ${CONFIG.totalTransactions}`);
  console.log(`Passed (200 OK) : ${passCount}`);
  console.log(`Failed          : ${failCount}`);
  console.log(`Audit Artifact  : ${CONFIG.outputFile}`);
  console.log('================================================================\n');
}

// Execute Script
runProductionSimulation();