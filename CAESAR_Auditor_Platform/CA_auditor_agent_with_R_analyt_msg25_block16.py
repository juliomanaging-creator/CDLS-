from integration.python_r_bridge import RAnalytics

r = RAnalytics()

# Monte Carlo simulation
results = r.monte_carlo_budget_risk(
    dept_id="DHCS",
    allocated_budget=124_000_000_000,
    iterations=10000
)

print(f"Mean Expenditure: ${results['mean_expenditure']:,.0f}")
print(f"Probability Over Budget: {(1-results['prob_under_budget'])*100:.1f}%")