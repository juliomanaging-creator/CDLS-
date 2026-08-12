// React portal calls agent system

const result = await agentService.discoverWorkflow(
    'Onboard Sacramento Auto Group',
    { dealer_name: 'Sacramento Auto Group', annual_volume: 500 }
);

// Agents discover 6-step workflow automatically
// Portal displays real-time progress
result.steps.forEach(step => {
    console.log(`${step.agent}: ${step.action} - ${step.status}`);
});