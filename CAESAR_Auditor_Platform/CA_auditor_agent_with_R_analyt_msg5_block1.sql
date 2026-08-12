-- Enhanced reconciliation table with three-way validation
CREATE TABLE transaction_reconciliation (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id UUID REFERENCES transactions(id),
    
    -- Operational Layer
    gps_coordinates JSONB NOT NULL,  -- Start, waypoints, end coordinates
    gps_total_distance NUMERIC(10,2), -- Miles
    load_manifest_hash VARCHAR(66),   -- SHA-256 of vehicle VINs
    driver_signature_hash VARCHAR(66),
    driver_timestamp TIMESTAMP WITH TIME ZONE,
    
    -- Financial Layer
    haul_token_amount NUMERIC(18,8),
    haul_token_tx_hash VARCHAR(66),   -- Blockchain transaction
    usd_payment_amount NUMERIC(10,2),
    usd_settlement_timestamp TIMESTAMP WITH TIME ZONE,
    carbon_tokens_minted INTEGER,
    carbon_mint_tx_hash VARCHAR(66),
    
    -- Environmental Layer
    energy_discharged_kwh NUMERIC(10,4),
    cesar_controller_id VARCHAR(100),
    grid_settlement_id VARCHAR(100),
    battery_soc_start NUMERIC(5,2),   -- State of charge %
    battery_soc_end NUMERIC(5,2),
    caiso_settlement_amount NUMERIC(10,2),
    
    -- Reconciliation Metrics
    integrity_score NUMERIC(5,4) CHECK (integrity_score >= 0 AND integrity_score <= 1),
    gps_variance_pct NUMERIC(5,2),    -- Expected vs actual distance
    energy_variance_pct NUMERIC(5,2), -- Expected vs actual discharge
    financial_variance_pct NUMERIC(5,2),
    reconciliation_status VARCHAR(50) DEFAULT 'pending',
    
    -- Audit Trail
    reconciled_at TIMESTAMP WITH TIME ZONE,
    reconciled_by VARCHAR(255),
    exception_notes TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_txn_reconciliation_status ON transaction_reconciliation(reconciliation_status);
CREATE INDEX idx_txn_reconciliation_integrity ON transaction_reconciliation(integrity_score);
CREATE INDEX idx_txn_reconciliation_created ON transaction_reconciliation(created_at DESC);

-- View for institutional auditors (pre-filtered exceptions)
CREATE VIEW institutional_audit_view AS
SELECT 
    tr.transaction_id,
    t.timestamp as haul_timestamp,
    tr.integrity_score,
    tr.reconciliation_status,
    tr.gps_variance_pct,
    tr.energy_variance_pct,
    tr.financial_variance_pct,
    tr.haul_token_tx_hash,
    tr.carbon_mint_tx_hash,
    tr.cesar_controller_id,
    tr.exception_notes
FROM transaction_reconciliation tr
JOIN transactions t ON tr.transaction_id = t.id
WHERE 
    tr.integrity_score < 0.95  -- Flag < 95% integrity
    OR tr.gps_variance_pct > 5.0
    OR tr.energy_variance_pct > 5.0
    OR tr.financial_variance_pct > 5.0
ORDER BY tr.integrity_score ASC, tr.created_at DESC;