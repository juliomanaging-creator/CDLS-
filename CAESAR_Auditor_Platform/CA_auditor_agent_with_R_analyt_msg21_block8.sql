-- Every PHI access logged immutably
INSERT INTO phi_access_log VALUES (
    user_id: 'auditor_jane_smith',
    transaction_id: 'txn_12345',
    access_timestamp: '2026-02-07 14:32:15',
    access_type: 'view',
    business_justification: 'Investigating duplicate DHCS payments',
    supervisor_approved: true,
    supervisor_id: 'manager_bob_jones',
    data_accessed: '{"fields": ["patient_age_range", "diagnosis_category"]}',
    ip_address: '10.20.30.40'
);

-- Cannot be modified or deleted (immutable trigger prevents)