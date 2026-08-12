const state_variables = {
  // Existing variables (from previous models)
  X1: fleet_size,              // Number of CDLS trucks
  X2: grid_capacity_mw,        // Available V2G capacity
  X3: dealer_partnerships,     // Number of participating dealers
  
  // NEW variables for Universal Dignity Program
  X4: dignity_modules_deployed,     // Number of housing units
  X5: maintenance_cost_per_module,  // Annual cost
  X6: social_stability_index,       // Housing stability metric (0-1)
  X7: ca_tax_debt_remaining,        // California's budget deficit
  X8: lcfs_credit_price,            // Carbon credit market price
};