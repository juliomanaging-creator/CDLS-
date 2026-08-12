-- Which routes are most profitable for EV vs. diesel?
SELECT 
  origin,
  destination,
  AVG(distance_miles) as avg_distance,
  AVG(gross_margin_usd / distance_miles) as margin_per_mile,
  COUNT(*) as haul_count,
  SUM(revenue_usd) as total_revenue
FROM hauls
WHERE haul_date > NOW() - INTERVAL '90 days'
GROUP BY origin, destination
HAVING COUNT(*) > 5 -- routes with meaningful sample size
ORDER BY margin_per_mile DESC;