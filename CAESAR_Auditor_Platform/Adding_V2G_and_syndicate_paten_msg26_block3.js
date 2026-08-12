// 1. Faster data refresh (1-minute updates)
cron.schedule('*/1 * * * *', refreshTelemetry);

// 2. Time-aware probabilities
const { P_SALE, P_HAUL, P_CHARGE } = getDynamicProbabilities(hour, dayOfWeek);

// 3. Holiday calendar
if (isHoliday(targetDate)) {
  P_SALE *= 0.1;  // Minimal sales on Christmas
}

// 4. Weather integration
const weather = await fetch(`https://api.weather.gov/points/${lat},${lon}`);
const efficiencyFactor = getBatteryEfficiency(weather.temperature);