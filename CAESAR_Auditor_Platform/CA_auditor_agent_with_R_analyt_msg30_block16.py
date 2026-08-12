# Example 1: Monte Carlo
request = {
    'description': '''
        Create Monte Carlo simulation for budget risk.
        Parameters: dept_id, budget, iterations.
        Risk factors: inflation, costs, emergencies.
        Output: probabilities, VaR, CVaR, plots.
    ''',
    'priority': 'high'
}

result = agent.develop(request)
# Agent completes in ~5 minutes
# Output: Complete R module ready for deployment

# Example 2: Anomaly Detection
request = {
    'description': '''
        Build multi-method anomaly detection.
        Methods: IQR, Z-score, Benford's Law, Isolation Forest.
        Cross-validation with confidence scoring.
    ''',
    'priority': 'high'
}

result = agent.develop(request)
# Agent completes in ~4 minutes