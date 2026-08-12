// Step 1: Calculate carbon avoided
const dieselEmissions = miles * 22.4 / 2000; // lbs to tons
const evEmissions = miles * 0.0 / 2000; // assuming renewable electricity
const carbonAvoided = dieselEmissions - evEmissions; // metric tons CO2e

// Step 2: Convert to LCFS credits
const lcfsCredits = carbonAvoided * 0.89; // credit intensity factor

// Step 3: Calculate revenue
const creditValue = lcfsCredits * currentCreditPrice; // $/year

// Step 4: Add to ROI
const totalAnnualSavings = fuelSavings + maintenanceSavings + creditValue;
const enhancedPayback = upfrontCost / totalAnnualSavings;