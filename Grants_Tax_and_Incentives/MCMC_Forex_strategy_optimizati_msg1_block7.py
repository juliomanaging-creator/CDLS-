# Run on a new pair
res = run_pipeline("AUD/USD", "AUDUSD=X")

# Change MCMC samples for tighter posteriors
est = MCMCEstimator(rets, model="GBM", n_samples=50000, burnin=10000)

# Add a custom strategy
def my_strategy(price): ...
STRATEGIES["My Strategy"] = my_strategy