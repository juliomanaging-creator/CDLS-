def calculate_elrp_event_revenue():
    # ELRP activation (typically 10-20 events per summer)
    # Duration: 1-4 hours of discharge at $2/kWh
    
    elrp_discharge = 45  # kWh full discharge
    elrp_revenue = elrp_discharge * 2.00  # $2/kWh emergency rate
    
    # No arbitrage on ELRP days (grid priority)
    morning_charge_cost = 63 * 0.12
    
    net_revenue = elrp_revenue - morning_charge_cost
    
    return {
        'elrp_revenue': round(elrp_revenue, 2),
        'morning_cost': round(morning_charge_cost, 2),
        'net_elrp_revenue': round(net_revenue, 2),
        'lcfs_bonus': round(elrp_discharge * 0.08, 2)
    }

elrp_day = calculate_elrp_event_revenue()
print(f"""
ELRP EVENT DAY REVENUE (Per Pod):
- ELRP Discharge Revenue: ${elrp_day['elrp_revenue']}
- Morning Charge Cost: ${elrp_day['morning_cost']}
- Net ELRP Revenue: ${elrp_day['net_elrp_revenue']}
- LCFS Carbon Credits: +${elrp_day['lcfs_bonus']}
─────────────────────────────────────
TOTAL ELRP EVENT: ${elrp_day['net_elrp_revenue'] + elrp_day['lcfs_bonus']}
""")