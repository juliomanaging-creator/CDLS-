# 12 CPU cores, 12 agents
with ProcessPoolExecutor(max_workers=12) as executor:
    # All agents start at same time
    futures = [executor.submit(agent.execute) for agent in all_agents]
    
    # Collect results as they finish
    results = [f.result() for f in futures]

# Total time = slowest agent (not sum of all agents)