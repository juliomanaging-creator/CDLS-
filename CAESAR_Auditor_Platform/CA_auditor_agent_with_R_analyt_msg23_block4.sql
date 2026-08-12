-- Auditor queries de-identified data
SELECT 
    county,
    age_range,
    diagnosis_category,
    COUNT(*) as claim_count,
    SUM(amount) as total_paid
FROM medi_cal_claims_deidentified
WHERE service_year = 2026
GROUP BY county, age_range, diagnosis_category
HAVING COUNT(*) > 100
ORDER BY total_paid DESC;

-- Result: Identifies $4.9B variance in Sacramento County
-- for "Endocrine/Metabolic" services, age 36-45
-- NO patient identities accessed