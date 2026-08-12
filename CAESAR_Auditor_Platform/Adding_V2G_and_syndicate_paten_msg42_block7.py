import numpy as np
import pandas as pd
from scipy import stats

def run_mcmc_simulation(scenario, iterations=10000):
    """
    Monte Carlo Markov Chain simulation for CDLS 10-year forecast
    Enhanced with dignity module variables
    """
    
    # Initialize state
    state = {
        'year': 2026,
        'fleet_size': 50,
        'dignity_modules': 0,
        'ca_tax_debt': 68e9,  # $68B
        'cumulative_royalties': 0,
        'lcfs_credit_price': 98,
        'grid_capacity_mw': 7.5  # 50 trucks × 150 kWh × 80%
    }
    
    results = []
    
    for iteration in range(iterations):
        yearly_trajectory = []
        
        for year in range(2026, 2036):
            # Transition probabilities (Markov chain)
            
            # Fleet growth (stochastic)
            if scenario == 'conservative':
                growth_rate = np.random.normal(0.35, 0.08)  # 35% ± 8%
            elif scenario == 'aggressive':
                growth_rate = np.random.normal(0.55, 0.12)  # 55% ± 12%
            else:  # recession
                growth_rate = np.random.normal(0.18, 0.15)  # 18% ± 15%
            
            state['fleet_size'] = int(state['fleet_size'] * (1 + growth_rate))
            
            # Grid capacity (deterministic based on fleet)
            state['grid_capacity_mw'] = state['fleet_size'] * 0.15  # 150 kWh per truck
            
            # Grid revenue (stochastic with temperature/price factors)
            base_revenue_per_mw = 34592  # From historical analysis
            temp_multiplier = np.random.normal(1.0, 0.15)  # Weather variance
            price_multiplier = np.random.normal(1.0, 0.22)  # Market variance
            
            grid_revenue = (state['grid_capacity_mw'] * base_revenue_per_mw * 
                          temp_multiplier * price_multiplier)
            
            # Hauling revenue (more stable)
            hauls_per_truck_per_year = np.random.normal(650, 50)
            price_per_haul = np.random.normal(700, 35)
            hauling_revenue = state['fleet_size'] * hauls_per_truck_per_year * price_per_haul
            
            # LCFS credits
            state['lcfs_credit_price'] = state['lcfs_credit_price'] * np.random.normal(1.02, 0.08)
            mt_co2_saved = state['fleet_size'] * 91  # MT per truck per year
            lcfs_revenue = mt_co2_saved * state['lcfs_credit_price']
            
            # Total revenue
            total_revenue = grid_revenue + hauling_revenue + lcfs_revenue
            
            # 99% royalty to California
            royalty_payment = total_revenue * 0.99
            state['cumulative_royalties'] += royalty_payment
            
            # California tax debt reduction
            natural_reduction = state['ca_tax_debt'] * 0.033  # 3.3% GDP growth
            state['ca_tax_debt'] = max(0, state['ca_tax_debt'] - natural_reduction - royalty_payment)
            
            # Dignity modules (funded by V2G surplus)
            v2g_surplus_per_module = 500  # $1,200 revenue - $700 maintenance
            modules_affordable = int(grid_revenue * 0.10 / 20100)  # 10% of grid revenue for new modules
            state['dignity_modules'] = min(
                state['dignity_modules'] + modules_affordable,
                10000  # Cap at 10,000 modules
            )
            
            # Record year
            yearly_trajectory.append({
                'iteration': iteration,
                'year': year,
                'fleet_size': state['fleet_size'],
                'grid_capacity_mw': state['grid_capacity_mw'],
                'total_revenue': total_revenue,
                'royalty_to_ca': royalty_payment,
                'ca_tax_debt': state['ca_tax_debt'],
                'dignity_modules': state['dignity_modules'],
                'lcfs_price': state['lcfs_credit_price']
            })
        
        results.extend(yearly_trajectory)
    
    return pd.DataFrame(results)

# Run all scenarios
results_conservative = run_mcmc_simulation('conservative', 10000)
results_aggressive = run_mcmc_simulation('aggressive', 10000)
results_recession = run_mcmc_simulation('recession', 10000)