from integration.python_r_bridge import RAnalytics

# Initialize R analytics
r = RAnalytics()

# Call R Monte Carlo simulation from Python
mc_results = r.monte_carlo_budget_risk(
    dept_id="DHCS",
    allocated_budget=124_000_000_000,
    iterations=10000
)

print(f"Probability of overrun: {mc_results['prob_over_budget']*100:.1f}%")
print(f"Value at Risk: ${mc_results['var_95']:,.0f}")

# Call R anomaly detection
import pandas as pd
transactions = pd.read_sql("SELECT * FROM department_transactions", conn)
anomalies = r.detect_anomalies(transactions)

print(f"Anomalies detected: {anomalies['is_anomaly'].sum()}")

# Call R time series forecast
forecast = r.forecast_transactions(historical_data, forecast_periods=30)
print(forecast['forecast'].head(7))