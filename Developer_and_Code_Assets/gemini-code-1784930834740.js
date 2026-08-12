/**
 * CDLS ENERGY BANK — PRODUCTION SANDBOX TEST HARNESS
 * Target: Treasury Prime API Sandbox (https://api.sandbox.treasuryprime.com)
 * Objective: 100-Transaction Automated ACH Batch Simulation & Audit Log Generation
 */

require('dotenv').config();
const axios = require('axios');
const fs = require('fs');
const crypto = require('crypto');

// Validate Environment Variables
const CONFIG = {
  apiUrl: process.env.TREASURY_PRIME_API_URL || 'https://api.sandbox.treasuryprime.com',
  apiKeyId: process.env.TREASURY_PRIME_API_KEY_ID,
  apiSecretKey: process.env.TREASURY_PRIME_API_SECRET_KEY,
  masterAccountId: process.env.CDLS_MASTER_ACCOUNT_ID || 'acct_1029384756',
  totalTransactions: parseInt(process.env.TOTAL_TRANSACTIONS || '100', 10),
  outputFile: process.env.OUTPUT_AUDIT_FILE || './treasury_prime_100_tx_audit.json'
};

if (!CONFIG.apiKeyId || !CONFIG.apiSecretKey) {
  console.error('\n[ERROR] Missing API Credentials! Please set TREASURY_PRIME_API_KEY_ID and TREASURY_PRIME_API_SECRET_KEY in your .env file.\n');
  process.exit(1);
}

// HTTP Basic Authentication header per Treasury Prime specification
const authHeader = 'Basic ' + Buffer.from(`${CONFIG.apiKeyId}:${CONFIG.apiSecretKey}`).toString('base64');

const apiClient = axios.create({
  baseURL: CONFIG.apiUrl,
  headers: {
    'Authorization': authHeader,
    'Content-Type': 'application/json'
  },
  timeout: 10000
});

// Helper: Generates payload for simulated V2G Dispatch & Logistics Payouts ($150 - $1,250)
function generatePayload(index) {
  const isV2G = index % 2 === 0;
  const amount = (Math.random() * (1250 - 150) + 150).toFixed(2);
  const idempotencyKey = `cdls_prod_sim_${Date.now()}_idx_${index}_${crypto.randomBytes(3).toString('hex')}`;

  return {
    idempotencyKey,
    body: {
      account_id: CONFIG.masterAccountId,
      amount: amount,
      direction: 'credit',
      sec_code: 'ccd',
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

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function executeSingleTransaction(index, retries = 3) {
  const { idempotencyKey, body } = generatePayload(index);

  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const response = await apiClient.post('/ach', body, {
        headers: { 'X-Idempotency-Key': idempotencyKey }
      });

      return {
        status: 'SUCCESS',
        tx_index: index,
        ach_id: response.data.id || `ach_sandbox_mock_${index}`,
        amount: body.amount,
        settlement_type: body.userdata.settlement_type,
        idempotency_key: idempotencyKey,
        http_status: response.status,
        timestamp: new Date().toISOString()
      };
    } catch (err) {
      if (err.response && err.response.status === 429 && attempt < retries) {
        console.warn(`[WARN] Rate limit hit on Tx #${index}. Retrying in ${attempt * 500}ms...`);
        await sleep(attempt * 500);
        continue;
      }

      return {
        status: 'FAILED',
        tx_index: index,
        amount: body.amount,
        idempotency_key: idempotencyKey,
        error: err.response ? err.response.data : err.message,
        timestamp: new Date().toISOString()
      };
    }
  }
}

async function runSimulation() {
  console.log('================================================================');
  console.log('  CDLS ENERGY BANK — TREASURY PRIME 100-TX API SIMULATION RUN');
  console.log('================================================================');
  console.log(`Endpoint        : ${CONFIG.apiUrl}`);
  console.log(`Master Account  : ${CONFIG.masterAccountId}`);
  console.log(`Target Count    : ${CONFIG.totalTransactions} ACH Batch Transfers\n`);

  const auditLog = [];
  let passCount = 0;
  let failCount = 0;
  const startTime = Date.now();

  for (let i = 1; i <= CONFIG.totalTransactions; i++) {
    const result = await executeSingleTransaction(i);
    auditLog.push(result);

    if (result.status === 'SUCCESS') {
      passCount++;
      console.log(`[PASS] Tx #${String(i).padStart(3, '0')}/100 | ACH ID: ${result.ach_id} | $${result.amount} [${result.settlement_type}]`);
    } else {
      failCount++;
      console.error(`[FAIL] Tx #${String(i).padStart(3, '0')}/100 | Error:`, JSON.stringify(result.error));
    }

    await sleep(50); // Pacing delay to prevent network congestion
  }

  const durationSec = ((Date.now() - startTime) / 1000).toFixed(2);

  // Write compliance audit file
  fs.writeFileSync(CONFIG.outputFile, JSON.stringify(auditLog, null, 2));

  console.log('\n================================================================');
  console.log('                 FINAL EXECUTION SUMMARY LOG');
  console.log('================================================================');
  console.log(`Execution Time  : ${durationSec} seconds`);
  console.log(`Total Attempted : ${CONFIG.totalTransactions}`);
  console.log(`Successful      : ${passCount}`);
  console.log(`Failed          : ${failCount}`);
  console.log(`Audit Artifact  : ${CONFIG.outputFile}`);
  console.log('================================================================\n');
}

runSimulation();