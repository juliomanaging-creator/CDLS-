// Current model
current_annual_cost = trips_per_year × cost_per_trip
// Example: 25 × $850 = $21,250

// CDLS model
cdls_annual_cost = trips_per_year × cdls_price_per_trip
// Example: 25 × $850 = $21,250 (SAME COST)

// But CDLS moves MORE cars per trip
current_capacity = trips_per_year × 8
cdls_capacity = trips_per_year × 9
extra_capacity_value = (cdls_capacity - current_capacity) × value_per_car

// Example: (225 - 200) × $106 = $2,650 extra value