// backend/audit_on_chain.js

const { ethers } = require('ethers');
const crypto = require('crypto');

class AuditOnChainEngine {
  constructor(provider, contractAddress, privateKey) {
    this.provider = new ethers.JsonRpcProvider(provider);
    this.wallet = new ethers.Wallet(privateKey, this.provider);
    this.contract = new ethers.Contract(
      contractAddress,
      AUDIT_CONTRACT_ABI,
      this.wallet
    );
  }

  /**
   * Record complete audit trail on blockchain
   */
  async recordAuditTrail(auditData) {
    const trail = {
      transaction_id: auditData.transaction_id,
      reconciliation_id: auditData.reconciliation_id,
      
      // Process hashes
      operational_data_hash: this.hashData(auditData.operational),
      financial_data_hash: this.hashData(auditData.financial),
      environmental_data_hash: this.hashData(auditData.environmental),
      
      // Decision hashes
      r_script_version: auditData.r_script_version,
      r_script_hash: this.hashFile(auditData.r_script_path),
      llm_model_version: auditData.llm_model,
      llm_prompt_hash: this.hashData(auditData.llm_prompt),
      
      // Result hashes
      integrity_score: auditData.integrity_score,
      reconciliation_status: auditData.status,
      final_report_hash: this.hashData(auditData.report),
      
      // Metadata
      auditor_signature: auditData.auditor_signature || 'system',
      timestamp: Date.now()
    };
    
    // Merkle root of all hashes
    const merkleRoot = this.computeMerkleRoot([
      trail.operational_data_hash,
      trail.financial_data_hash,
      trail.environmental_data_hash,
      trail.r_script_hash,
      trail.llm_prompt_hash,
      trail.final_report_hash
    ]);
    
    // Submit to blockchain
    const tx = await this.contract.recordAuditTrail(
      trail.transaction_id,
      merkleRoot,
      JSON.stringify(trail),
      { gasLimit: 500000 }
    );
    
    await tx.wait();
    
    return {
      blockchain_tx_hash: tx.hash,
      merkle_root: merkleRoot,
      audit_trail: trail
    };
  }

  /**
   * Verify audit trail integrity
   */
  async verifyAuditTrail(transactionId) {
    const onChainData = await this.contract.getAuditTrail(transactionId);
    const offChainData = await this.fetchOffChainData(transactionId);
    
    // Recompute merkle root from off-chain data
    const recomputedRoot = this.computeMerkleRoot([
      this.hashData(offChainData.operational),
      this.hashData(offChainData.financial),
      this.hashData(offChainData.environmental),
      this.hashFile(offChainData.r_script_path),
      this.hashData(offChainData.llm_prompt),
      this.hashData(offChainData.report)
    ]);
    
    return {
      is_valid: recomputedRoot === onChainData.merkleRoot,
      on_chain_root: onChainData.merkleRoot,
      recomputed_root: recomputedRoot,
      timestamp: onChainData.timestamp
    };
  }

  hashData(data) {
    return crypto.createHash('sha256')
      .update(JSON.stringify(data))
      .digest('hex');
  }

  hashFile(filePath) {
    const fs = require('fs');
    const content = fs.readFileSync(filePath);
    return crypto.createHash('sha256')
      .update(content)
      .digest('hex');
  }

  computeMerkleRoot(hashes) {
    if (hashes.length === 1) return hashes[0];
    
    const nextLevel = [];
    for (let i = 0; i < hashes.length; i += 2) {
      const left = hashes[i];
      const right = hashes[i + 1] || left;
      const combined = crypto.createHash('sha256')
        .update(left + right)
        .digest('hex');
      nextLevel.push(combined);
    }
    
    return this.computeMerkleRoot(nextLevel);
  }
}

// Smart Contract ABI
const AUDIT_CONTRACT_ABI = [
  {
    "inputs": [
      { "name": "transactionId", "type": "bytes32" },
      { "name": "merkleRoot", "type": "bytes32" },
      { "name": "metadata", "type": "string" }
    ],
    "name": "recordAuditTrail",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "inputs": [{ "name": "transactionId", "type": "bytes32" }],
    "name": "getAuditTrail",
    "outputs": [
      { "name": "merkleRoot", "type": "bytes32" },
      { "name": "metadata", "type": "string" },
      { "name": "timestamp", "type": "uint256" }
    ],
    "stateMutability": "view",
    "type": "function"
  }
];

module.exports = AuditOnChainEngine;