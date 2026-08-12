// Current broker model
current_annual_cost = vehicles_per_year × cost_per_vehicle
// Example: 200 × $400 = $80,000

// CDLS model  
trips_needed = Math.ceil(vehicles_per_year / 9)
cdls_annual_cost = trips_needed × cdls_price_per_trip
// Example: 23 trips × $850 = $19,550

// MASSIVE SAVINGS
annual_savings = current_annual_cost - cdls_annual_cost
// Example: $80,000 - $19,550 = $60,450 (75.6% savings!)