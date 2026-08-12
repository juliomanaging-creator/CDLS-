-- CALIFORNIA STATE AUDITOR - DATABASE SCHEMA
-- Enterprise audit system for all 132 California state departments

-- Database setup
CREATE DATABASE ca_state_audit;
\c ca_state_audit

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- Master department registry (132 California state departments)
CREATE TABLE state_departments (
    dept_id VARCHAR(20) PRIMARY KEY,
    dept_name VARCHAR(255) NOT NULL,
    parent_agency VARCHAR(255),
    dept_type VARCHAR(50) CHECK (dept_type IN ('Executive', 'Legislative', 'Judicial', 'Constitutional', 'Independent', 'Board/Commission')),
    
    -- Budget & staffing
    annual_budget NUMERIC(15,2),
    employee_count INTEGER,
    
    -- Leadership
    director_name VARCHAR(255),
    director_email VARCHAR(255),
    contact_phone VARCHAR(20),
    physical_address TEXT,
    website_url VARCHAR(255),
    
    -- Audit configuration
    risk_level VARCHAR(20) CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    audit_frequency VARCHAR(20) CHECK (audit_frequency IN ('daily', 'weekly', 'bi-weekly', 'monthly', 'quarterly')),
    last_audit_date TIMESTAMP,
    next_scheduled_audit TIMESTAMP,
    
    -- System fields
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    active BOOLEAN DEFAULT TRUE
);

-- Transaction monitoring (all financial transactions across departments)
CREATE TABLE department_transactions (
    transaction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dept_id VARCHAR(20) REFERENCES state_departments(dept_id),
    
    -- Transaction details
    transaction_date TIMESTAMP NOT NULL,
    transaction_type VARCHAR(100) CHECK (transaction_type IN ('Expenditure', 'Revenue', 'Payroll', 'Grant', 'Contract', 'Transfer', 'Adjustment')),
    amount NUMERIC(15,2) NOT NULL,
    fiscal_year INTEGER,
    quarter INTEGER CHECK (quarter BETWEEN 1 AND 4),
    
    -- Parties involved
    vendor_id VARCHAR(50),
    vendor_name VARCHAR(255),
    employee_id VARCHAR(50),
    employee_name VARCHAR(255),
    
    -- Description & categorization
    description TEXT,
    account_code VARCHAR(50),
    object_code VARCHAR(50),
    fund_source VARCHAR(100),
    program_code VARCHAR(50),
    
    -- Approval workflow
    approval_authority VARCHAR(255),
    approval_date TIMESTAMP,
    authorization_number VARCHAR(100),
    
    -- Procurement details (if applicable)
    procurement_method VARCHAR(100),
    competitive_bid BOOLEAN,
    bid_count INTEGER,
    contract_number VARCHAR(100),
    
    -- Validation & integrity
    integrity_score NUMERIC(5,4) CHECK (integrity_score BETWEEN 0 AND 1),
    fiscal_system_verified BOOLEAN DEFAULT FALSE,
    bank_reconciled BOOLEAN DEFAULT FALSE,
    general_ledger_verified BOOLEAN DEFAULT FALSE,
    
    -- Anomaly detection
    anomaly_flags JSONB,
    fraud_risk_score NUMERIC(5,4),
    
    -- Audit status
    audit_status VARCHAR(50) CHECK (audit_status IN ('pending', 'verified', 'review', 'exception', 'resolved')) DEFAULT 'pending',
    auditor_notes TEXT,
    audited_by VARCHAR(255),
    audited_at TIMESTAMP,
    
    -- Blockchain anchor
    blockchain_hash VARCHAR(66),
    blockchain_timestamp TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Three-way reconciliation tracking
CREATE TABLE reconciliation_events (
    reconciliation_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dept_id VARCHAR(20) REFERENCES state_departments(dept_id),
    
    -- Period
    reconciliation_date DATE NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    reconciliation_type VARCHAR(50) CHECK (reconciliation_type IN ('Daily', 'Weekly', 'Monthly', 'Quarterly', 'Annual')),
    
    -- Transaction counts
    total_transactions INTEGER,
    verified_count INTEGER,
    flagged_count INTEGER,
    exception_count INTEGER,
    
    -- Financial totals
    total_expenditures NUMERIC(15,2),
    total_revenue NUMERIC(15,2),
    net_position NUMERIC(15,2),
    
    -- Budget analysis
    budget_allocated NUMERIC(15,2),
    budget_spent NUMERIC(15,2),
    budget_variance NUMERIC(15,2),
    budget_variance_pct NUMERIC(5,2),
    
    -- Three-way reconciliation sources
    fiscal_system_total NUMERIC(15,2),
    bank_statement_total NUMERIC(15,2),
    general_ledger_total NUMERIC(15,2),
    
    -- Variance analysis
    reconciliation_variance NUMERIC(15,2),
    variance_threshold_exceeded BOOLEAN,
    variance_explained BOOLEAN,
    variance_explanation TEXT,
    
    -- Data quality metrics
    data_completeness_pct NUMERIC(5,2),
    data_accuracy_pct NUMERIC(5,2),
    timeliness_score NUMERIC(5,4),
    
    -- Compliance scoring
    financial_integrity_score NUMERIC(5,4),
    operational_compliance_score NUMERIC(5,4),
    data_quality_score NUMERIC(5,4),
    composite_risk_score NUMERIC(5,4),
    risk_level VARCHAR(20),
    
    -- Audit trail
    reconciled_by VARCHAR(255),
    reviewed_by VARCHAR(255),
    approved_by VARCHAR(255),
    approval_date TIMESTAMP,
    
    -- Supporting documentation
    documentation_path TEXT,
    evidence_hash VARCHAR(66),
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Compliance monitoring (regulatory, policy, legal requirements)
CREATE TABLE compliance_events (
    compliance_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dept_id VARCHAR(20) REFERENCES state_departments(dept_id),
    
    -- Compliance event details
    compliance_date TIMESTAMP NOT NULL,
    compliance_type VARCHAR(100) CHECK (compliance_type IN ('Policy', 'Regulation', 'Legal', 'Ethical', 'Contractual', 'Federal', 'State')),
    requirement_code VARCHAR(100),
    requirement_description TEXT,
    
    -- Status
    compliance_status VARCHAR(50) CHECK (compliance_status IN ('Compliant', 'Non-Compliant', 'Partial', 'Under Review', 'N/A')),
    
    -- Violation details (if applicable)
    violation_severity VARCHAR(50) CHECK (violation_severity IN ('Minor', 'Moderate', 'Major', 'Critical')),
    violation_description TEXT,
    violation_date TIMESTAMP,
    
    -- Financial impact
    financial_impact NUMERIC(15,2),
    potential_penalty NUMERIC(15,2),
    
    -- Corrective action
    corrective_action_required BOOLEAN,
    corrective_action_plan TEXT,
    responsible_official VARCHAR(255),
    remediation_deadline DATE,
    remediation_status VARCHAR(50),
    remediation_completed_date DATE,
    
    -- Evidence & documentation
    documentation_path TEXT,
    evidence_hash VARCHAR(66),
    supporting_documents JSONB,
    
    -- Responsible parties
    department_contact VARCHAR(255),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    
    -- External oversight
    oversight_agency VARCHAR(255),
    reported_to_oversight BOOLEAN,
    oversight_case_number VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Fraud detection and investigation
CREATE TABLE fraud_alerts (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dept_id VARCHAR(20) REFERENCES state_departments(dept_id),
    
    -- Alert metadata
    alert_date TIMESTAMP NOT NULL,
    alert_type VARCHAR(100) CHECK (alert_type IN ('Statistical Anomaly', 'Pattern Recognition', 'Duplicate Payment', 'Ghost Employee', 'Vendor Collusion', 'Benford Violation', 'Whistleblower', 'External Tip')),
    
    -- Severity & priority
    severity VARCHAR(50) CHECK (severity IN ('Low', 'Medium', 'High', 'Critical')),
    priority INTEGER CHECK (priority BETWEEN 1 AND 5),
    
    -- Alert details
    description TEXT,
    flagged_transactions JSONB,  -- Array of transaction IDs
    flagged_individuals JSONB,   -- Employee or vendor IDs
    
    -- Detection methodology
    detection_method VARCHAR(100) CHECK (detection_method IN ('Statistical', 'Machine Learning', 'Pattern Recognition', 'Manual Review', 'Whistleblower', 'External Audit')),
    anomaly_score NUMERIC(5,4),
    confidence_level NUMERIC(5,4),
    false_positive_probability NUMERIC(5,4),
    
    -- Financial impact
    estimated_loss NUMERIC(15,2),
    confirmed_loss NUMERIC(15,2),
    recovery_amount NUMERIC(15,2),
    
    -- Investigation
    investigation_status VARCHAR(50) CHECK (investigation_status IN ('Open', 'In Progress', 'Closed - Confirmed Fraud', 'Closed - False Positive', 'Closed - Inconclusive', 'Referred to Law Enforcement')),
    investigator_assigned VARCHAR(255),
    investigation_start_date TIMESTAMP,
    investigation_notes TEXT,
    resolution_date TIMESTAMP,
    outcome VARCHAR(50),
    outcome_details TEXT,
    
    -- Legal & law enforcement
    law_enforcement_agency VARCHAR(255),
    law_enforcement_notified BOOLEAN,
    law_enforcement_case_number VARCHAR(100),
    legal_action_taken BOOLEAN,
    prosecution_status VARCHAR(100),
    
    -- Whistleblower protection (if applicable)
    whistleblower_case BOOLEAN,
    whistleblower_protected BOOLEAN,
    
    -- Corrective measures
    control_weaknesses_identified TEXT,
    corrective_actions_implemented TEXT,
    
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Audit reports (department-level and statewide)
CREATE TABLE audit_reports (
    report_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Report classification
    report_type VARCHAR(50) CHECK (report_type IN ('Department', 'Cross-Department', 'Statewide', 'Special Investigation', 'Performance Audit', 'Financial Audit', 'Compliance Audit')),
    dept_id VARCHAR(20) REFERENCES state_departments(dept_id),  -- NULL for statewide
    
    -- Reporting period
    report_date DATE NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    fiscal_year INTEGER,
    
    -- Report content
    report_title VARCHAR(500),
    executive_summary TEXT,
    findings JSONB,  -- Structured findings
    recommendations JSONB,  -- Structured recommendations
    
    -- Scoring
    financial_integrity_score NUMERIC(5,4),
    operational_compliance_score NUMERIC(5,4),
    data_quality_score NUMERIC(5,4),
    performance_score NUMERIC(5,4),
    composite_risk_score NUMERIC(5,4),
    overall_risk_level VARCHAR(50),
    
    -- Statistics
    total_transactions_reviewed INTEGER,
    flagged_transactions INTEGER,
    critical_exceptions INTEGER,
    fraud_alerts_count INTEGER,
    compliance_violations INTEGER,
    
    -- Distribution & access
    distributed_to JSONB,  -- Array of recipients
    public_release BOOLEAN DEFAULT FALSE,
    public_release_date DATE,
    legislative_notification BOOLEAN DEFAULT FALSE,
    confidential BOOLEAN DEFAULT FALSE,
    security_classification VARCHAR(50),
    
    -- File storage
    pdf_path TEXT,
    pdf_hash VARCHAR(66),  -- SHA-256 of PDF file
    blockchain_anchor VARCHAR(66),
    ipfs_hash VARCHAR(100),  -- Optional IPFS storage
    
    -- Metadata
    generated_by VARCHAR(255),
    reviewed_by VARCHAR(255),
    approved_by VARCHAR(255),  -- State Auditor approval
    approval_date TIMESTAMP,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Performance metrics (program effectiveness, service delivery)
CREATE TABLE performance_metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dept_id VARCHAR(20) REFERENCES state_departments(dept_id),
    
    -- Metric details
    metric_date DATE NOT NULL,
    metric_category VARCHAR(100) CHECK (metric_category IN ('Financial', 'Operational', 'Service Delivery', 'Outcome', 'Output', 'Efficiency', 'Quality')),
    metric_name VARCHAR(255) NOT NULL,
    metric_description TEXT,
    
    -- Values
    metric_value NUMERIC(15,4),
    metric_unit VARCHAR(50),
    
    -- Benchmarking
    target_value NUMERIC(15,4),
    baseline_value NUMERIC(15,4),
    prior_year_value NUMERIC(15,4),
    
    -- Analysis
    variance_from_target NUMERIC(15,4),
    variance_pct NUMERIC(5,2),
    trend VARCHAR(50) CHECK (trend IN ('Improving', 'Stable', 'Declining', 'Insufficient Data')),
    performance_rating VARCHAR(50) CHECK (performance_rating IN ('Exceeds', 'Meets', 'Below', 'Critical')),
    
    -- Context
    notes TEXT,
    data_source VARCHAR(255),
    calculation_method TEXT,
    
    -- Comparisons
    statewide_average NUMERIC(15,4),
    national_average NUMERIC(15,4),
    peer_group_average NUMERIC(15,4),
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Reporting submissions (timeliness and quality tracking)
CREATE TABLE reporting_submissions (
    submission_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dept_id VARCHAR(20) REFERENCES state_departments(dept_id),
    
    -- Report details
    report_name VARCHAR(255),
    report_type VARCHAR(100),
    report_period DATE,
    
    -- Deadlines
    report_due_date DATE NOT NULL,
    report_submitted_date DATE,
    days_late INTEGER GENERATED ALWAYS AS (
        CASE 
            WHEN report_submitted_date > report_due_date 
            THEN report_submitted_date - report_due_date
            ELSE 0
        END
    ) STORED,
    
    -- Quality assessment
    data_completeness_pct NUMERIC(5,2),
    data_accuracy_pct NUMERIC(5,2),
    format_compliance BOOLEAN,
    quality_score NUMERIC(5,4),
    
    -- Issues
    errors_found INTEGER,
    corrections_required INTEGER,
    resubmission_required BOOLEAN,
    resubmitted_date DATE,
    
    -- Assessment
    assessed_by VARCHAR(255),
    assessment_notes TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Transactions
CREATE INDEX idx_dept_txn_date ON department_transactions(dept_id, transaction_date DESC);
CREATE INDEX idx_dept_txn_amount ON department_transactions(amount DESC);
CREATE INDEX idx_dept_txn_type ON department_transactions(transaction_type);
CREATE INDEX idx_dept_txn_vendor ON department_transactions(vendor_id);
CREATE INDEX idx_dept_txn_status ON department_transactions(audit_status);
CREATE INDEX idx_dept_txn_integrity ON department_transactions(integrity_score);

-- Reconciliation
CREATE INDEX idx_recon_dept_date ON reconciliation_events(dept_id, reconciliation_date DESC);
CREATE INDEX idx_recon_risk ON reconciliation_events(risk_level);

-- Compliance
CREATE INDEX idx_compliance_dept_date ON compliance_events(dept_id, compliance_date DESC);
CREATE INDEX idx_compliance_status ON compliance_events(compliance_status);
CREATE INDEX idx_compliance_severity ON compliance_events(violation_severity);

-- Fraud
CREATE INDEX idx_fraud_dept_date ON fraud_alerts(dept_id, alert_date DESC);
CREATE INDEX idx_fraud_severity ON fraud_alerts(severity);
CREATE INDEX idx_fraud_status ON fraud_alerts(investigation_status);

-- Audit reports
CREATE INDEX idx_reports_date ON audit_reports(report_date DESC);
CREATE INDEX idx_reports_dept ON audit_reports(dept_id);
CREATE INDEX idx_reports_type ON audit_reports(report_type);
CREATE INDEX idx_reports_risk ON audit_reports(overall_risk_level);

-- Performance metrics
CREATE INDEX idx_metrics_dept_date ON performance_metrics(dept_id, metric_date DESC);
CREATE INDEX idx_metrics_category ON performance_metrics(metric_category);
CREATE INDEX idx_metrics_rating ON performance_metrics(performance_rating);

-- Full-text search
CREATE INDEX idx_txn_description_fts ON department_transactions USING gin(to_tsvector('english', description));
CREATE INDEX idx_compliance_fts ON compliance_events USING gin(to_tsvector('english', requirement_description));
CREATE INDEX idx_fraud_description_fts ON fraud_alerts USING gin(to_tsvector('english', description));

-- ============================================================================
-- VIEWS FOR REPORTING
-- ============================================================================

-- Statewide dashboard view
CREATE VIEW statewide_dashboard AS
SELECT 
    d.dept_id,
    d.dept_name,
    d.dept_type,
    d.risk_level,
    d.annual_budget,
    r.financial_integrity_score,
    r.operational_compliance_score,
    r.data_quality_score,
    r.composite_risk_score,
    r.total_transactions,
    r.exception_count,
    (SELECT COUNT(*) FROM fraud_alerts WHERE dept_id = d.dept_id AND investigation_status = 'Open') as open_fraud_cases,
    (SELECT COUNT(*) FROM compliance_events WHERE dept_id = d.dept_id AND compliance_status = 'Non-Compliant') as compliance_violations
FROM state_departments d
LEFT JOIN LATERAL (
    SELECT * FROM reconciliation_events 
    WHERE dept_id = d.dept_id 
    ORDER BY reconciliation_date DESC 
    LIMIT 1
) r ON TRUE
WHERE d.active = TRUE;

-- High risk transactions view
CREATE VIEW high_risk_transactions AS
SELECT 
    t.*,
    d.dept_name,
    CASE 
        WHEN t.integrity_score < 0.85 THEN 'CRITICAL'
        WHEN t.integrity_score < 0.95 THEN 'HIGH'
        ELSE 'MEDIUM'
    END as risk_category
FROM department_transactions t
JOIN state_departments d ON t.dept_id = d.dept_id
WHERE t.integrity_score < 0.95
    OR t.audit_status = 'exception'
    OR t.fraud_risk_score > 0.5
ORDER BY t.integrity_score ASC, t.amount DESC;

-- Department performance summary
CREATE VIEW department_performance_summary AS
SELECT 
    d.dept_id,
    d.dept_name,
    COUNT(DISTINCT pm.metric_id) as total_metrics,
    AVG(pm.metric_value) as avg_metric_value,
    SUM(CASE WHEN pm.performance_rating = 'Exceeds' THEN 1 ELSE 0 END) as exceeds_count,
    SUM(CASE WHEN pm.performance_rating = 'Meets' THEN 1 ELSE 0 END) as meets_count,
    SUM(CASE WHEN pm.performance_rating = 'Below' THEN 1 ELSE 0 END) as below_count,
    SUM(CASE WHEN pm.performance_rating = 'Critical' THEN 1 ELSE 0 END) as critical_count
FROM state_departments d
LEFT JOIN performance_metrics pm ON d.dept_id = pm.dept_id
    AND pm.metric_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY d.dept_id, d.dept_name;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

-- Auto-update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_state_departments_updated_at
    BEFORE UPDATE ON state_departments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_fraud_alerts_updated_at
    BEFORE UPDATE ON fraud_alerts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- INITIAL DATA - SAMPLE DEPARTMENTS
-- ============================================================================

INSERT INTO state_departments (dept_id, dept_name, parent_agency, dept_type, annual_budget, employee_count, risk_level, audit_frequency) VALUES
('CALTRANS', 'Department of Transportation', 'Transportation Agency', 'Executive', 15700000000, 20000, 'HIGH', 'weekly'),
('CDCR', 'Department of Corrections and Rehabilitation', 'Executive', 'Executive', 15500000000, 65000, 'HIGH', 'weekly'),
('DOF', 'Department of Finance', 'Executive', 'Executive', 500000000, 350, 'CRITICAL', 'daily'),
('EDD', 'Employment Development Department', 'Labor and Workforce Development', 'Executive', 17000000000, 10000, 'HIGH', 'weekly'),
('DHCS', 'Department of Health Care Services', 'Health and Human Services', 'Executive', 124000000000, 5000, 'CRITICAL', 'daily'),
('DSS', 'Department of Social Services', 'Health and Human Services', 'Executive', 32000000000, 3800, 'HIGH', 'weekly'),
('DMV', 'Department of Motor Vehicles', 'Government Operations', 'Executive', 1200000000, 9000, 'MEDIUM', 'bi-weekly'),
('CALFIRE', 'Department of Forestry and Fire Protection', 'Natural Resources', 'Executive', 3600000000, 8500, 'HIGH', 'weekly'),
('CONTROLLER', 'State Controller', 'Constitutional Office', 'Constitutional', 250000000, 1200, 'CRITICAL', 'daily'),
('TREASURER', 'State Treasurer', 'Constitutional Office', 'Constitutional', 150000000, 500, 'CRITICAL', 'daily'),
('SOS', 'Secretary of State', 'Constitutional Office', 'Constitutional', 100000000, 550, 'MEDIUM', 'monthly'),
('CPUC', 'Public Utilities Commission', 'Independent', 'Independent', 350000000, 1000, 'HIGH', 'weekly'),
('CEC', 'Energy Commission', 'Independent', 'Independent', 800000000, 600, 'HIGH', 'weekly'),
('CALPERS', 'Public Employees Retirement System', 'Independent', 'Independent', 500000000, 3000, 'CRITICAL', 'daily'),
('CALSTRS', 'State Teachers Retirement System', 'Independent', 'Independent', 400000000, 1300, 'CRITICAL', 'daily'),
('UC', 'University of California', 'Higher Education', 'Independent', 44000000000, 227000, 'HIGH', 'weekly'),
('CSU', 'California State University', 'Higher Education', 'Independent', 12000000000, 56000, 'HIGH', 'weekly');

-- Grant appropriate permissions
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO ca_auditor_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ca_auditor_app;

-- Complete
\echo 'California State Auditor Database Schema Created Successfully'
\echo 'Total Tables: 9'
\echo 'Total Views: 3'
\echo 'Sample Departments Loaded: 17 of 132'
