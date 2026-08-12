-- Engagement Score Algorithm (run hourly via cron job)
WITH document_engagement AS (
  SELECT 
    dealroom_id,
    COUNT(DISTINCT CASE WHEN event_type = 'view' THEN entity_id END) * 10 as views_score,
    SUM(CASE WHEN event_type = 'time_spent' THEN duration_seconds END) / 60 as minutes_spent,
    COUNT(DISTINCT CASE WHEN event_type = 'download' THEN entity_id END) * 15 as downloads_score
  FROM engagement_events
  WHERE timestamp > NOW() - INTERVAL '7 days'
  GROUP BY dealroom_id
),
engagement_calculation AS (
  SELECT 
    dealroom_id,
    LEAST(100, views_score + (minutes_spent * 2) + downloads_score) as score
  FROM document_engagement
)
INSERT INTO engagement_scores (dealroom_id, overall_score, calculated_at)
SELECT dealroom_id, score, NOW()
FROM engagement_calculation
ON CONFLICT (dealroom_id) DO UPDATE
SET overall_score = EXCLUDED.overall_score, calculated_at = EXCLUDED.calculated_at;