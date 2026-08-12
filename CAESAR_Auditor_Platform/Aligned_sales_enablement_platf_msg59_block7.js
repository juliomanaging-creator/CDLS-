// Your fleet data
const numberOfVehicles = 20;
const milesPerVehicle = 50000;
const totalAnnualMiles = numberOfVehicles * milesPerVehicle; // 1,000,000

// Carbon calculation
const dieselEmissionsPerMile = 22.4 / 2000; // lbs to tons
const totalCO2Avoided = totalAnnualMiles * dieselEmissionsPerMile; // 11,200 tons
const lcfsCredits = totalCO2Avoided * 0.89; // 9,968 credits/year

// Market prices
const currentPrice = 100; // $/credit
const projectedPrices = {
  sixMonths: 110,
  oneYear: 120,
  twoYears: 140,
  threeYears: 160
};

// Your cost of capital
const alternativeInvestmentReturn = 0.08; // 8% annual (what else could you do with the money?)
const discountRate = 0.10; // 10% discount rate for risk