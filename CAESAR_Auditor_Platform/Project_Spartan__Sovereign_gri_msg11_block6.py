def calculate_annual_revenue_per_pod():
    # Operating calendar
    normal_days = 250  # Regular arbitrage days
    elrp_events = 15   # Emergency demand response events
    maintenance_days = 10  # Downtime
    total_operating_days = normal_days + elrp_events
    
    # Revenue calculation
    normal_revenue = normal_days * 34.29
    elrp_revenue = elrp_events * 86.04
    total_gross_revenue = normal_revenue + elrp_revenue
    
    # Operating costs
    annual_maintenance = 150 * 12  # $150/month
    insurance = 600  # Annual coverage
    software_fees = 240  # CESAR platform
    total_opex = annual_maintenance + insurance + software_fees
    
    # Net revenue
    net_annual_revenue = total_gross_revenue - total_opex
    
    return {
        'normal_days_revenue': round(normal_revenue, 2),
        'elrp_events_revenue': round(elrp_revenue, 2),
        'gross_revenue': round(total_gross_revenue, 2),
        'operating_costs': total_opex,
        'net_annual_revenue': round(net_annual_revenue, 2),
        'roi_months': round((pod_capex + trailer_modification + v2g_inverter) / (net_annual_revenue / 12), 1)
    }

annual = calculate_annual_revenue_per_pod()
print(f"""
ANNUAL REVENUE (Per Energy Pod Trailer):
─────────────────────────────────────
Revenue Streams:
- Normal Days (250): ${annual['normal_days_revenue']:,}
- ELRP Events (15): ${annual['elrp_events_revenue']:,}
- Gross Annual Revenue: ${annual['gross_revenue']:,}

Operating Costs:
- Maintenance: $1,800
- Insurance: $600
- Software: $240
- Total OpEx: ${annual['operating_costs']:,}

NET ANNUAL REVENUE: ${annual['net_annual_revenue']:,}
─────────────────────────────────────
ROI: {annual['roi_months']} months
""")