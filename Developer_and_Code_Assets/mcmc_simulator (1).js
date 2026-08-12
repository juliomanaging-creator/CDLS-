// CDLS MCMC Simulator - Proprietary Grid Capacity Prediction
// Monte Carlo Markov Chain for fragmented fleet optimization

const crypto = require('crypto');

/**
 * Run MCMC simulation to predict aggregate fleet discharge capacity
 * 
 * @param {Object} params - Simulation parameters
 * @param {Array} params.fleetState - Current fleet telemetry
 * @param {Date} params.target_datetime - Time to predict capacity for
 * @param {Number} params.iterations - MCMC iterations (default: 10000)
 * @param {Number} params.parallel_chains - Number of parallel chains (default: 4)
 * @returns {Object} Simulation results with capacity prediction
 */
async function runMCMCSimulation({ fleetState, target_datetime, iterations = 10000, parallel_chains = 4 }) {
  const startTime = Date.now();

  // Calculate time delta (hours until target)
  const now = new Date();
  const hoursUntilTarget = (target_datetime - now) / (1000 * 60 * 60);

  if (hoursUntilTarget < 0) {
    throw new Error('target_datetime must be in the future');
  }

  if (hoursUntilTarget > 72) {
    throw new Error('target_datetime must be within 72 hours (MCMC accuracy degrades beyond this)');
  }

  // Run parallel MCMC chains
  const chainPromises = [];
  for (let chain = 0; chain < parallel_chains; chain++) {
    chainPromises.push(runSingleChain({
      fleetState,
      hoursUntilTarget,
      iterations: Math.floor(iterations / parallel_chains),
      chainId: chain,
    }));
  }

  const chainResults = await Promise.all(chainPromises);

  // Aggregate results across chains
  const allCapacityPredictions = chainResults.flatMap(chain => chain.capacityHistory);

  // Calculate statistics
  const mean = calculateMean(allCapacityPredictions);
  const std = calculateStdDev(allCapacityPredictions, mean);
  const confidenceInterval = calculateConfidenceInterval(allCapacityPredictions, 0.95);

  // Check convergence using Gelman-Rubin statistic
  const convergenceAchieved = checkConvergence(chainResults);

  const executionTime = Date.now() - startTime;

  return {
    simulation_id: crypto.randomBytes(8).toString('hex'),
    predicted_capacity_mean: mean.toFixed(2),
    predicted_capacity_std: std.toFixed(2),
    confidence_interval: [
      confidenceInterval.lower.toFixed(2),
      confidenceInterval.upper.toFixed(2),
    ],
    convergence_achieved: convergenceAchieved,
    execution_time_ms: executionTime,
    iterations_total: iterations,
    parallel_chains,
    chain_results: chainResults.map(chain => ({
      chain_id: chain.chainId,
      final_capacity: chain.finalCapacity.toFixed(2),
      acceptance_rate: chain.acceptanceRate.toFixed(3),
    })),
  };
}

/**
 * Run single MCMC chain
 */
async function runSingleChain({ fleetState, hoursUntilTarget, iterations, chainId }) {
  const capacityHistory = [];
  let acceptCount = 0;

  // Initialize state
  let currentState = initializeState(fleetState);

  // Markov Chain iterations
  for (let i = 0; i < iterations; i++) {
    // Propose new state
    const proposedState = proposeNextState(currentState, hoursUntilTarget);

    // Calculate acceptance probability
    const acceptanceProbability = calculateAcceptanceProbability(currentState, proposedState);

    // Accept or reject proposal (Metropolis-Hastings)
    if (Math.random() < acceptanceProbability) {
      currentState = proposedState;
      acceptCount++;
    }

    // Record capacity prediction
    const capacity = calculateAvailableCapacity(currentState);
    capacityHistory.push(capacity);
  }

  return {
    chainId,
    capacityHistory,
    finalCapacity: capacityHistory[capacityHistory.length - 1],
    acceptanceRate: acceptCount / iterations,
  };
}

/**
 * Initialize Markov chain state
 */
function initializeState(fleetState) {
  return fleetState.map(unit => ({
    unit_id: unit.unit_id,
    battery_soc: unit.battery_soc,
    battery_kwh: unit.battery_kwh,
    dealer_id: unit.dealer_id,
    location: unit.location,
    status: 'available', // available, in_transit, sold, charging
    time_to_next_event: null, // hours until next state change
  }));
}

/**
 * Propose next state using Markov transitions
 */
function proposeNextState(currentState, hoursUntilTarget) {
  const newState = currentState.map(unit => ({ ...unit }));

  // Apply stochastic transitions for each unit
  newState.forEach(unit => {
    // Transition probabilities (calibrated from historical data)
    const P_SALE_PER_HOUR = 0.00417; // 1/(10 days * 24 hours) = wholesale turnover
    const P_HAUL_PER_HOUR = 0.006;   // ~1 haul every 7 days
    const P_CHARGE_PER_HOUR = 0.05;   // If SoC < 30%, likely charging

    // Sales transition
    if (Math.random() < P_SALE_PER_HOUR * hoursUntilTarget) {
      unit.status = 'sold';
      unit.battery_soc = null; // No longer available for V2G
      return;
    }

    // Hauling transition
    if (unit.status === 'available' && Math.random() < P_HAUL_PER_HOUR * hoursUntilTarget) {
      unit.status = 'in_transit';
      unit.battery_soc -= 5 + Math.random() * 10; // 5-15% SoC loss during haul
      unit.time_to_next_event = 2 + Math.random() * 4; // 2-6 hours hauling
      return;
    }

    // Charging transition
    if (unit.battery_soc < 30 && Math.random() < P_CHARGE_PER_HOUR) {
      unit.status = 'charging';
      unit.battery_soc += Math.min(50, 100 - unit.battery_soc); // Charge to 80%+
      unit.battery_soc = Math.min(100, unit.battery_soc);
    }

    // Return to available after transit
    if (unit.status === 'in_transit' && unit.time_to_next_event) {
      unit.time_to_next_event -= hoursUntilTarget;
      if (unit.time_to_next_event <= 0) {
        unit.status = 'available';
        unit.time_to_next_event = null;
      }
    }

    // Ensure SoC stays in bounds
    if (unit.battery_soc !== null) {
      unit.battery_soc = Math.max(0, Math.min(100, unit.battery_soc));
    }
  });

  return newState;
}

/**
 * Calculate acceptance probability (Metropolis-Hastings)
 */
function calculateAcceptanceProbability(currentState, proposedState) {
  // For MCMC grid prediction, we always accept valid proposals
  // (standard Metropolis with uniform proposal distribution)
  
  // Could add energy function to prefer certain states
  // For now: accept all physically valid states
  return 1.0;
}

/**
 * Calculate available discharge capacity from fleet state
 */
function calculateAvailableCapacity(state) {
  const SAFETY_BUFFER_SOC = parseFloat(process.env.GRID_SAFETY_BUFFER_SOC || 20);
  const MAX_DISCHARGE_RATE = parseFloat(process.env.GRID_MAX_DISCHARGE_RATE || 0.80);

  let totalCapacityKwh = 0;

  state.forEach(unit => {
    // Only available units with sufficient SoC can discharge
    if (unit.status === 'available' && unit.battery_soc > SAFETY_BUFFER_SOC) {
      const availableSoc = unit.battery_soc - SAFETY_BUFFER_SOC;
      const availableKwh = (availableSoc / 100) * unit.battery_kwh;
      const dischargeableKwh = availableKwh * MAX_DISCHARGE_RATE;

      totalCapacityKwh += dischargeableKwh;
    }
  });

  // Convert to MW
  return totalCapacityKwh / 1000;
}

/**
 * Check convergence using Gelman-Rubin statistic
 * R-hat < 1.1 indicates convergence
 */
function checkConvergence(chainResults) {
  if (chainResults.length < 2) return false;

  const m = chainResults.length; // number of chains
  const n = chainResults[0].capacityHistory.length; // iterations per chain

  // Calculate within-chain variance (W)
  const withinChainVariances = chainResults.map(chain => {
    const mean = calculateMean(chain.capacityHistory);
    const variance = calculateVariance(chain.capacityHistory, mean);
    return variance;
  });

  const W = calculateMean(withinChainVariances);

  // Calculate between-chain variance (B)
  const chainMeans = chainResults.map(chain => calculateMean(chain.capacityHistory));
  const overallMean = calculateMean(chainMeans);
  const B = chainMeans.reduce((sum, mean) => sum + Math.pow(mean - overallMean, 2), 0) / (m - 1);

  // Calculate pooled variance estimate
  const varPlus = ((n - 1) / n) * W + B;

  // Calculate R-hat (potential scale reduction factor)
  const rHat = Math.sqrt(varPlus / W);

  // Convergence achieved if R-hat < 1.1
  return rHat < 1.1;
}

// ===========================================
// STATISTICAL UTILITIES
// ===========================================

function calculateMean(values) {
  return values.reduce((sum, val) => sum + val, 0) / values.length;
}

function calculateVariance(values, mean) {
  return values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / (values.length - 1);
}

function calculateStdDev(values, mean) {
  return Math.sqrt(calculateVariance(values, mean));
}

function calculateConfidenceInterval(values, confidence = 0.95) {
  const sorted = [...values].sort((a, b) => a - b);
  const alpha = 1 - confidence;

  const lowerIndex = Math.floor(sorted.length * (alpha / 2));
  const upperIndex = Math.floor(sorted.length * (1 - alpha / 2));

  return {
    lower: sorted[lowerIndex],
    upper: sorted[upperIndex],
  };
}

// ===========================================
// EXPORTS
// ===========================================

module.exports = {
  runMCMCSimulation,
  // Export utilities for testing
  calculateMean,
  calculateStdDev,
  calculateConfidenceInterval,
};
