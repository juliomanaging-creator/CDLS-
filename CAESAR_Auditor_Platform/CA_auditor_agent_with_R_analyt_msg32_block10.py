# Instead of generating from scratch (5 minutes):
"Create Monte Carlo simulation with salary inflation, 
operational costs, emergency expenses, probabilities..."

# We use pre-written template (0.5 seconds):
MONTE_CARLO_TEMPLATE = """
library(MASS)
library(ggplot2)

monte_carlo_budget_risk <- function(
    dept_id,
    allocated_budget,
    iterations = {ITERATIONS},
    # ... 300 lines of pre-written, validated code
) {
    # All the complex logic is already here
    # Just fill in the parameters
}
"""

# Agent fills: {ITERATIONS} = 10000
# Done in 0.5 seconds