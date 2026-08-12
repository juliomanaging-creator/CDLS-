// Recalculate stakeholder engagement scores nightly
async function updateStakeholderEngagement(stakeholderId) {
  const recentInteractions = await StakeholderInteraction.find({
    stakeholder_id: stakeholderId,
    occurred_at: { $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }
  });
  
  const documentViews = await EngagementEvent.count({
    user_email: stakeholder.email,
    event_type: 'view',
    timestamp: { $gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000) }
  });
  
  // Weighted scoring
  const score = Math.min(10, 
    (recentInteractions.length * 1.5) +
    (documentViews * 0.5) +
    (recentInteractions.filter(i => i.sentiment === 'positive').length * 2)
  );
  
  await Stakeholder.update(stakeholderId, { engagement_level: Math.round(score) });
}