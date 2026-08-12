// Auto-refresh every 30 seconds
setInterval(() => {
  recentActivityQuery.trigger();
  topDealsQuery.trigger();
  alertsQuery.trigger();
}, 30000);