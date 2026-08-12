-- Active dealers count
SELECT COUNT(*) FROM dealers WHERE status IN ('pilot', 'committed', 'active');

-- Hot leads (last 7 days)
SELECT d.*, ls.engagement_score
FROM dealers d
JOIN lead_scores ls ON d.id = ls.dealer_id
WHERE ls.engagement_score > 70
AND ls.last_activity > NOW() - INTERVAL '7 days'
ORDER BY ls.engagement_score DESC;

-- Recent activity
SELECT 
  d.name,
  'ran calculation' as action,
  c.annual_savings,
  c.created_at
FROM calculations c
JOIN dealers d ON c.dealer_id = d.id
WHERE c.created_at > NOW() - INTERVAL '24 hours'
ORDER BY c.created_at DESC
LIMIT 20;