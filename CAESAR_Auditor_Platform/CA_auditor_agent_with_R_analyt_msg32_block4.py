# BEFORE: 30 minutes (sequential)
for agent in agents:
    result = agent.execute()  # 5 min each

# AFTER: 5 minutes (parallel)
results = parallel_execute(agents)  # All 6 simultaneously