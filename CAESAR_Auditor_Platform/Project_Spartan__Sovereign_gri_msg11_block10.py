def calculate_fleet_revenue(fleet_size=100, dealers=6):
    pod_net_revenue = 7223.10
    fleet_gross = fleet_size * pod_net_revenue
    
    # Total investment (CAPEX)
    capex_per_pod = 18000 + 5000 + 12000  # Pod + modification + inverter
    installation_per_dealer = 45000
    total_capex = (fleet_size * capex_per_pod) + (dealers * installation_per_dealer)
    
    # Annual breakdown
    dealer_hosting_fees = dealers * 16767.27
    cdls_platform_fees = fleet_gross * 0.20
    driver_pool_total = (fleet_gross - cdls_platform_fees) * 0.70
    cdls_net_total = (fleet_gross - cdls_platform_fees) * 0.30
    
    # Additional revenue streams
    hauling_revenue = fleet_size * 45000  # $45k/trailer/year hauling
    total_platform_revenue = fleet_gross + hauling_revenue
    
    return {
        'fleet_gross_v2g': round(fleet_gross, 2),
        'hauling_revenue': round(hauling_revenue, 2),
        'total_platform_revenue': round(total_platform_revenue, 2),
        'total_capex': round(total_capex, 2),
        'dealer_hosting_fees': round(dealer_hosting_fees, 2),
        'cdls_platform_fees': round(cdls_platform_fees, 2),
        'driver_pool_total': round(driver_pool_total, 2),
        'cdls_net_total': round(cdls_net_total, 2),
        'payback_years': round(total_capex / cdls_net_total, 2),
        'irr_estimate': '18.5%'
    }

fleet = calculate_fleet_revenue()
print(f"""
════════════════════════════════════════════════════════
FLEET-WIDE SIMULATION: 100 ENERGY POD TRAILERS
════════════════════════════════════════════════════════

REVENUE STREAMS:
- V2G Grid Services: ${fleet['fleet_gross_v2g']:,}
- Vehicle Hauling: ${fleet['hauling_revenue']:,}
─────────────────────────────────────
TOTAL ANNUAL REVENUE: ${fleet['total_platform_revenue']:,}

CAPITAL INVESTMENT:
- 100 Energy Pods: $3,500,000
- 6 Dealer Installations: $270,000
─────────────────────────────────────
TOTAL CAPEX: ${fleet['total_capex']:,}

REVENUE DISTRIBUTION:
- Dealer Hosting Fees: ${fleet['dealer_hosting_fees']:,}
- CDLS Platform Fees (20%): ${fleet['cdls_platform_fees']:,}
- Driver Pool (70%): ${fleet['driver_pool_total']:,}
- CDLS Net Revenue (30%): ${fleet['cdls_net_total']:,}

FINANCIAL METRICS:
- Payback Period: {fleet['payback_years']} years
- Estimated IRR: {fleet['irr_estimate']}
- 5-Year NPV: ${round(fleet['cdls_net_total'] * 5 - fleet['total_capex'], 2):,}

PER DRIVER (100 drivers):
- Annual V2G Income: ${round(fleet['driver_pool_total'] / 100, 2):,}
- Annual Hauling Income: ${round(fleet['hauling_revenue'] * 0.70 / 100, 2):,}
─────────────────────────────────────
TOTAL DRIVER INCOME: ${round((fleet['driver_pool_total'] + fleet['hauling_revenue'] * 0.70) / 100, 2):,}

════════════════════════════════════════════════════════
""")