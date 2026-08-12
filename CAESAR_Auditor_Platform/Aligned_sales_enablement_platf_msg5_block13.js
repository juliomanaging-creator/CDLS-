// Backend generates hierarchical structure
function generateOrgChart(dealroomId) {
  // Query stakeholders and relationships
  const stakeholders = await Stakeholder.findByDealroom(dealroomId);
  const relationships = await StakeholderRelationship.findByStakeholders(
    stakeholders.map(s => s.id)
  );
  
  // Build tree structure
  const tree = {
    nodes: stakeholders.map(s => ({
      id: s.id,
      name: s.name,
      title: s.title,
      roleType: s.role_type,
      influenceLevel: s.influence_level,
      engagementLevel: s.engagement_level,
      lastInteraction: s.last_interaction_date
    })),
    edges: relationships.map(r => ({
      from: r.stakeholder_from_id,
      to: r.stakeholder_to_id,
      type: r.relationship_type,
      strength: r.strength
    }))
  };
  
  return tree;
}