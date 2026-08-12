// Current (broken):
Annual Savings = (currentCost - cdlsCost) × hauls

// Fixed:
if (currentCost < cdlsCost) {
  Annual Value = carbonCredits + capitalAvoidance + complianceValue - costIncrease
  Label = "TOTAL ANNUAL VALUE" (instead of "SAVINGS")
} else {
  Annual Savings = (currentCost - cdlsCost) × hauls + carbonCredits
  Label = "ANNUAL HAULING COST SAVINGS"
}