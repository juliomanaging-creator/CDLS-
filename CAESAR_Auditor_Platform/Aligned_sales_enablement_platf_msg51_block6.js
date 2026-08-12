// Dropdown onChange event
const selectedDealer = dealerDropdown.value;
const dealerData = dealerProfiles.find(d => d.name === selectedDealer);

// Auto-populate inputs
fleetSizeInput.setValue(dealerData.fleetSize);
annualMilesInput.setValue(dealerData.annualMiles);
electricityRateInput.setValue(dealerData.electricityRate);
// ... etc