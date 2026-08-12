-- Which vehicles are most efficient?
SELECT 
  v.vin,
  v.make,
  v.model,
  COUNT(h.id) as total_hauls,
  AVG(h.distance_miles) as avg_haul_distance,
  SUM(cs.kwh_consumed) / SUM(h.distance_miles) as kwh_per_mile,
  AVG(h.gross_margin_usd) as avg_margin
FROM vehicles v
JOIN hauls h ON v.id = h.vehicle_id
JOIN charging_sessions cs ON v.id = cs.vehicle_id
WHERE h.haul_date > NOW() - INTERVAL '90 days'
GROUP BY v.id, v.vin, v.make, v.model
ORDER BY kwh_per_mile ASC; -- most efficient first