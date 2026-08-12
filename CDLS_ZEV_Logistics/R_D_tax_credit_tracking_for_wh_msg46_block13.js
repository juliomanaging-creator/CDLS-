// Example: Load real data in your code
const carrierData = require('./data/sample-data/carrier_cost_data.json');

// Get diesel price for Sacramento
const sacDieselPrice = carrierData.diesel_vehicle_operations
  .ford_f550_car_hauler
  .california_specific
  .diesel_price_sacramento; // Returns: 4.12

// Calculate trip cost
const distance = 85.3; // Sacramento to Modesto
const mpg = 6.5;
const fuelCost = (distance / mpg) * sacDieselPrice;
// Result: $54.03 fuel cost