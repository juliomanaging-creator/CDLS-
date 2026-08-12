// Calculate critical path and risk assessment
class ActionPlanAnalyzer {
  constructor(actionPlan, actionItems) {
    this.plan = actionPlan;
    this.items = actionItems;
  }
  
  calculateCriticalPath() {
    // Build dependency graph
    const graph = this.buildDependencyGraph();
    
    // Find longest path (critical path)
    const criticalPath = this.longestPath(graph);
    
    // Calculate earliest start dates
    const schedule = this.forwardPass(graph);
    
    return {
      criticalItems: criticalPath,
      estimatedCompletionDate: schedule.projectEndDate,
      slack: this.calculateSlack(schedule),
      riskLevel: this.assessRisk(schedule)
    };
  }
  
  assessRisk(schedule) {
    const today = new Date();
    const daysUntilTarget = (this.plan.target_close_date - today) / (1000 * 60 * 60 * 24);
    const daysNeeded = (schedule.projectEndDate - today) / (1000 * 60 * 60 * 24);
    
    const blockedItems = this.items.filter(i => i.status === 'blocked').length;
    const overdueItems = this.items.filter(i => 
      i.due_date < today && i.status !== 'completed'
    ).length;
    
    if (daysNeeded > daysUntilTarget || blockedItems > 2 || overdueItems > 3) {
      return 'high';
    } else if (daysNeeded > daysUntilTarget * 0.9 || blockedItems > 0) {
      return 'medium';
    }
    return 'low';
  }
}