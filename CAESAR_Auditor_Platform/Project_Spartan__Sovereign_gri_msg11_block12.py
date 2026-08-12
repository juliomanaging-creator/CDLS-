def optimized_dual_revenue_model():
    # Energy pod is SECONDARY revenue stream
    # Hauling is PRIMARY business
    
    hauling_annual = 45000  # Per trailer
    v2g_annual = 7223  # Per energy pod
    total_revenue = hauling_annual + v2g_annual
    
    # Driver split (70%)
    driver_total = total_revenue * 0.70
    driver_monthly = driver_total / 12
    
    # CDLS margin (30%)
    cdls_margin = total_revenue * 0.30
    
    # ROI calculation
    capex_per_unit = 35000  # Pod system only (trailer already owned)
    roi_years = capex_per_unit / cdls_margin
    
    return {
        'total_revenue': round(total_revenue, 2),
        'driver_annual': round(driver_total, 2),
        'driver_monthly': round(driver_monthly, 2),
        'cdls_margin': round(cdls_margin, 2),
        'roi_years': round(roi_years, 2),
        'margin_percent': round((cdls_margin / total_revenue) * 100, 1)
    }

optimized = optimized_dual_revenue_model()
print(f"""
OPTIMIZED DUAL-REVENUE MODEL:
═════════════════════════════════════════

Per Trailer Annual Revenue:
- Hauling Services: $45,000 (primary)
- V2G Grid Services: $7,223 (secondary)
─────────────────────────────────────
TOTAL REVENUE: ${optimized['total_revenue']:,}

Revenue Split:
- Driver (70%): ${optimized['driver_annual']:,}/year (${optimized['driver_monthly']:,}/month)
- CDLS (30%): ${optimized['cdls_margin']:,}/year

Investment:
- Energy Pod System: $35,000
- ROI Period: {optimized['roi_years']} years
- Margin: {optimized['margin_percent']}%

═════════════════════════════════════════
CONCLUSION: V2G is 13.8% revenue boost
Hauling remains core business (86.2%)
═════════════════════════════════════════
""")