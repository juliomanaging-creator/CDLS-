# BEFORE: 5 minutes per module
result = llm.generate("Create Monte Carlo simulation...")

# AFTER: 0.5 seconds per module  
result = template.fill(MONTE_CARLO_TEMPLATE, params)