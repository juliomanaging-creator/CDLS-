# Your payout model needs:
async def process_driver_split(revenue: float, driver_id: str):
    # Add safety checks
    if revenue < 0:
        raise ValueError("Negative revenue detected")
    
    # Implement tiered structure
    base_split = 0.70
    performance_bonus = calculate_grid_reliability_bonus(driver_id)
    
    total_share = revenue * (base_split + performance_bonus)
    
    # Tax withholding (1099 contractors)
    irs_withholding = total_share * 0.30  # Estimated tax
    net_payment = total_share - irs_withholding
    
    await transfer_funds(
        to=driver_id,
        amount=net_payment,
        memo=f"Grid Services: {datetime.now()}"
    )