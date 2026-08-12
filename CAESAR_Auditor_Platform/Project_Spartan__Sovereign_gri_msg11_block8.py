def calculate_dealer_site_revenue(pods_per_dealer=17):
    pod_net_revenue = 7223.10
    dealer_total_revenue = pods_per_dealer * pod_net_revenue
    
    # Dealer receives hosting fee (10% of gross revenue)
    hosting_fee = (pods_per_dealer * 9863.10) * 0.10
    
    # CDLS platform fee (20% of net revenue)
    cdls_platform_fee = dealer_total_revenue * 0.20
    
    # Driver pool split (70% of remaining revenue)
    remaining_after_platform = dealer_total_revenue - cdls_platform_fee
    driver_pool = remaining_after_platform * 0.70
    cdls_net = remaining_after_platform * 0.30
    
    return {
        'dealer_total_revenue': round(dealer_total_revenue, 2),
        'dealer_hosting_fee': round(hosting_fee, 2),
        'cdls_platform_fee': round(cdls_platform_fee, 2),
        'driver_pool_70': round(driver_pool, 2),
        'cdls_net_30': round(cdls_net, 2)
    }

dealer = calculate_dealer_site_revenue()
print(f"""
DEALER SITE REVENUE (17 Energy Pods):
─────────────────────────────────────
Total Site Revenue: ${dealer['dealer_total_revenue']:,}

Revenue Distribution:
- Dealer Hosting Fee (10%): ${dealer['dealer_hosting_fee']:,}
- CDLS Platform Fee (20%): ${dealer['cdls_platform_fee']:,}
- Driver Pool (70%): ${dealer['driver_pool_70']:,}
- CDLS Net (30%): ${dealer['cdls_net_30']:,}

Per Driver (assume 17 drivers):
- Annual Income: ${round(dealer['driver_pool_70'] / 17, 2):,}
- Monthly Income: ${round(dealer['driver_pool_70'] / 17 / 12, 2):,}
""")