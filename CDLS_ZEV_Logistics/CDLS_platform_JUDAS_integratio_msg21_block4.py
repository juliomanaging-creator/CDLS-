# RER Validation Analysis
dealers_surveyed = 20
total_monthly_hauls = sum(dealer_data['monthly_hauls'])
avg_hauls_per_dealer = total_monthly_hauls / dealers_surveyed
total_monthly_revenue = total_monthly_hauls * 1200

# Validation Metrics
committed_dealers = count(commitment_level == "Yes")
investment_commitments = count(investment_interest == "Yes")
total_equity_committed = investment_commitments * 500000

# Carbon Impact
total_co2_saved = total_monthly_hauls * 0.29  # MT
carbon_credit_revenue = total_co2_saved * 85

# RER Validation
projected_rer = avg_hauls_per_dealer * 1200 * dealers_surveyed
actual_rer = total_monthly_revenue
validation_accuracy = (actual_rer / projected_rer) * 100