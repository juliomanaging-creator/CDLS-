// Input Variables
const inputs = {
    // Sales Metrics
    monthlyNewSales: 0,
    monthlyUsedSales: 0,
    avgFrontGross: 0,
    avgBackGross: 0,
    currentLeadCloseRate: 0,
    
    // Website Metrics
    monthlyWebsiteVisitors: 0,
    currentLeadRate: 0,
    expectedLeadRateImprovement: 0,
    
    // Service Metrics
    monthlyServiceROs: 0,
    avgServiceRO: 0,
    expectedServiceImprovement: 0,
    
    // Cost Structure
    monthlySubscriptionCost: 0,
    implementationCost: 0,
    trainingCost: 0
}

// ROI Calculator Functions
function calculateDigitalMarketingROI(inputs) {
    const additionalLeads = 
        inputs.monthlyWebsiteVisitors * 
        (inputs.expectedLeadRateImprovement / 100);
        
    const additionalSales = 
        additionalLeads * 
        (inputs.currentLeadCloseRate / 100);
        
    const monthlyRevenue = 
        additionalSales * 
        (inputs.avgFrontGross + inputs.avgBackGross);
        
    const annualRevenue = monthlyRevenue * 12;
    const annualCost = 
        (inputs.monthlySubscriptionCost * 12) + 
        inputs.implementationCost;
        
    const roi = 
        ((annualRevenue - annualCost) / annualCost) * 100;
        
    return {
        additionalLeads,
        additionalSales,
        monthlyRevenue,
        annualRevenue,
        roi
    };
}