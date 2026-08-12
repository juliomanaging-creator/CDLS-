// Frontend tracking service
class AnalyticsTracker {
  trackDocumentView(documentId, dealroomId) {
    this.sendEvent({
      type: 'view',
      entityType: 'document',
      entityId: documentId,
      dealroomId: dealroomId,
      timestamp: new Date().toISOString()
    });
  }
  
  trackTimeSpent(entityId, entityType, durationSeconds) {
    this.sendEvent({
      type: 'time_spent',
      entityType: entityType,
      entityId: entityId,
      duration: durationSeconds
    });
  }
  
  trackScrollDepth(documentId, pageNumber, scrollPercentage) {
    // Throttled to avoid excessive events
    this.sendEvent({
      type: 'scroll_depth',
      entityType: 'document',
      entityId: documentId,
      metadata: { pageNumber, scrollPercentage }
    });
  }
}