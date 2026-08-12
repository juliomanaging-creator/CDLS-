# SCENARIO 1: NORMAL DAY (No Grid Events)
# Trailer operates on CAISO day-ahead + real-time arbitrage

def calculate_normal_day_revenue():
    # Morning charge (cheap grid power)
    morning_charge = 63  # kWh (fully charge from 30% to 100%)
    morning_cost = morning_charge * 0.12  # Off-peak rate
    
    # Evening discharge (peak demand 4-9 PM)
    evening_discharge = 45  # kWh (discharge to 30% SOC minimum)
    evening_revenue = evening_discharge * 0.85  # Real-time peak rate
    
    # Net daily revenue
    net_revenue = evening_revenue - morning_cost
    
    return {
        'morning_cost': round(morning_cost, 2),
        'evening_revenue': round(evening_revenue, 2),
        'net_daily_revenue': round(net_revenue, 2),
        'lcfs_bonus': round(evening_discharge * 0.08, 2)  # Carbon credits
    }

normal_day = calculate_normal_day_revenue()
print(f"""
NORMAL DAY REVENUE (Per Pod):
- Morning Charge Cost: ${normal_day['morning_cost']}
- Evening Discharge Revenue: ${normal_day['evening_revenue']}
- Net Daily Revenue: ${normal_day['net_daily_revenue']}
- LCFS Carbon Credits: +${normal_day['lcfs_bonus']}
─────────────────────────────────────
TOTAL DAILY NET: ${normal_day['net_daily_revenue'] + normal_day['lcfs_bonus']}
""")