-- Your pod_x_villages table needs:
ALTER TABLE pod_x_villages ADD COLUMN
    water_quality_ppm FLOAT,
    hvac_uptime_pct DECIMAL(5,2),
    food_rescue_partner_id UUID,
    emergency_contact VARCHAR(255);

-- Add compliance tracking
CREATE TABLE health_inspections (
    pod_id INT REFERENCES pod_x_villages(id),
    inspection_date DATE,
    county_inspector_name VARCHAR(100),
    pass_fail VARCHAR(10),
    violations_log JSONB
);