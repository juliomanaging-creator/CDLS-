-- Predict which vehicles need service soon
SELECT 
  v.vin,
  MAX(t.odometer_miles) as current_miles,
  MAX(m.odometer_miles) as last_service_miles,
  MAX(t.odometer_miles) - MAX(m.odometer_miles) as miles_since_service,
  CASE 
    WHEN (MAX(t.odometer_miles) - MAX(m.odometer_miles)) > 5000 
    THEN 'Service Due'
    WHEN (MAX(t.odometer_miles) - MAX(m.odometer_miles)) > 4000 
    THEN 'Service Soon'
    ELSE 'OK'
  END as status
FROM vehicles v
LEFT JOIN telematics_data t ON v.id = t.vehicle_id
LEFT JOIN maintenance_records m ON v.id = m.vehicle_id
GROUP BY v.id, v.vin
HAVING (MAX(t.odometer_miles) - MAX(m.odometer_miles)) > 4000
ORDER BY miles_since_service DESC;