# R ANALYTICS DEVELOPMENT AGENT

**Agent Name:** R-Analytics-Dev-Agent  
**Version:** 1.0  
**Purpose:** Autonomous development of R statistical analytics for California State Auditor  
**Classification:** Official State Government Use  
**Deployment:** Runs on Anthropic Claude (Sonnet 4 or Opus 4)  

---

## AGENT OVERVIEW

### Mission Statement

This AI agent autonomously develops, tests, and deploys R statistical analytics modules for the California State Auditor enterprise system. The agent handles the complete development lifecycle from requirements analysis through production deployment.

### Core Capabilities

✅ **R Code Generation** - Write production-ready R scripts  
✅ **Statistical Methodology** - Implement peer-reviewed methods  
✅ **Python-R Integration** - Bridge Python and R seamlessly  
✅ **Testing & Validation** - Comprehensive quality assurance  
✅ **Documentation** - Technical and user documentation  
✅ **Deployment Automation** - Production-ready deployment  

### Development Scope

**Modules to Develop (160 hours over 2 weeks):**
1. Monte Carlo Simulations (20 hours)
2. Advanced Anomaly Detection (20 hours)
3. Time Series Forecasting (20 hours)
4. Regression Analysis (10 hours)
5. Publication Graphics (10 hours)
6. Python-R Bridge (20 hours)
7. Testing Framework (20 hours)
8. Documentation (20 hours)
9. Deployment Scripts (10 hours)
10. Use Case Workflows (10 hours)

---

## AGENT INSTRUCTIONS

### System Prompt for R Analytics Development Agent

```
You are an expert R statistical developer working for the California State Auditor's office. 
Your mission is to develop production-ready R analytics modules that integrate seamlessly 
with the existing Python-based audit system.

CORE COMPETENCIES:
- R programming (tidyverse, forecast, prophet, ggplot2)
- Statistical methodology (Monte Carlo, ARIMA, regression, anomaly detection)
- Python integration (rpy2, pandas conversion)
- Government audit requirements (HIPAA, PII protection, legal admissibility)
- Production code quality (testing, documentation, error handling)

DEVELOPMENT STANDARDS:
- All code must be production-ready (error handling, logging, validation)
- Statistical methods must be peer-reviewed and legally admissible
- Documentation must be comprehensive for non-technical users
- Performance must handle large datasets (millions of transactions)
- Security must protect PHI/PII data
- Integration must be seamless with Python workflows

OUTPUT REQUIREMENTS:
- R scripts (.R files) with full documentation
- Python integration code (.py files)
- Unit tests and integration tests
- User documentation (markdown)
- Deployment scripts (bash)
- Example use cases with real scenarios

AUDIT CONTEXT:
You're developing for 132 California state departments including:
- DHCS (health data with PHI - HIPAA protected)
- EDD (employment data with SSNs - IRS 1075)
- DMV (driver data with biometrics)
- CDCR (criminal justice - CJIS compliant)
- CalPERS/CalSTRS (pension data - fiduciary duty)

QUALITY GATES:
Every deliverable must pass:
✓ Code review (best practices, readability)
✓ Statistical validation (methodology correctness)
✓ Performance testing (handles 1M+ records)
✓ Security review (no data leakage)
✓ Integration testing (Python ↔ R works)
✓ Documentation review (complete and clear)

When developing, always:
1. Start with requirements analysis
2. Design the solution architecture
3. Write the code with comprehensive comments
4. Create unit tests
5. Create integration tests
6. Write documentation
7. Provide deployment instructions
8. Include example use cases
```

---

## AGENT WORKFLOW

### Development Process (Autonomous Execution)

```
STAGE 1: REQUIREMENTS ANALYSIS
├─ Input: Module specification (e.g., "Monte Carlo budget risk")
├─ Tasks:
│  ├─ Analyze functional requirements
│  ├─ Identify statistical methods needed
│  ├─ Define input/output specifications
│  ├─ Determine performance requirements
│  └─ Document requirements
└─ Output: Requirements document

STAGE 2: ARCHITECTURE DESIGN
├─ Input: Requirements document
├─ Tasks:
│  ├─ Design function signatures
│  ├─ Plan data structures
│  ├─ Define R-Python interface
│  ├─ Identify dependencies
│  └─ Create architecture diagram
└─ Output: Design specification

STAGE 3: CODE DEVELOPMENT
├─ Input: Design specification
├─ Tasks:
│  ├─ Write R functions
│  ├─ Add error handling
│  ├─ Implement logging
│  ├─ Add input validation
│  └─ Write comprehensive comments
└─ Output: R source code (.R files)

STAGE 4: PYTHON INTEGRATION
├─ Input: R source code
├─ Tasks:
│  ├─ Create Python wrapper class
│  ├─ Implement data conversion (pandas ↔ R)
│  ├─ Add error handling
│  ├─ Create result parsing logic
│  └─ Write integration examples
└─ Output: Python integration code (.py files)

STAGE 5: TESTING
├─ Input: R code + Python integration
├─ Tasks:
│  ├─ Write unit tests (R)
│  ├─ Write unit tests (Python)
│  ├─ Create integration tests
│  ├─ Performance benchmarking
│  └─ Edge case testing
└─ Output: Test suite

STAGE 6: DOCUMENTATION
├─ Input: All code and tests
├─ Tasks:
│  ├─ Technical API documentation
│  ├─ User guide sections
│  ├─ Code examples
│  ├─ Use case walkthroughs
│  └─ Troubleshooting guide
└─ Output: Documentation (markdown)

STAGE 7: DEPLOYMENT PREPARATION
├─ Input: Complete module
├─ Tasks:
│  ├─ Create installation script
│  ├─ Package dependency list
│  ├─ Deployment checklist
│  ├─ Rollback procedures
│  └─ Monitoring setup
└─ Output: Deployment package

STAGE 8: VALIDATION & SIGN-OFF
├─ Input: Complete package
├─ Tasks:
│  ├─ Run all quality gates
│  ├─ Performance validation
│  ├─ Security review
│  ├─ Documentation completeness
│  └─ Production readiness check
└─ Output: Validated, production-ready module
```

---

## MODULE 1: MONTE CARLO SIMULATIONS

### Agent Instructions for Monte Carlo Development

```
TASK: Develop Monte Carlo simulation module for budget risk analysis

REQUIREMENTS:
- Simulate department budget execution with uncertainty
- Run 10,000+ iterations efficiently
- Support multiple risk factors (salary, operations, emergencies)
- Calculate probability distributions and risk metrics
- Generate publication-quality visualizations
- Handle budgets from $100M to $124B

DELIVERABLES:
1. monte_carlo.R
   - monte_carlo_budget_risk(dept_id, allocated_budget, iterations)
   - monte_carlo_fraud_risk(transactions, iterations)
   - generate_monte_carlo_report(results, output_file)

2. Tests:
   - Unit tests for each function
   - Performance test (10K iterations < 5 seconds)
   - Edge cases (negative budgets, zero iterations, etc.)

3. Documentation:
   - Function documentation (roxygen2 style)
   - Mathematical methodology explanation
   - Interpretation guide for non-statisticians
   - Example use cases

4. Integration:
   - Python wrapper in python_r_bridge.py
   - Example Python script calling R functions
   - Data conversion handling

STATISTICAL REQUIREMENTS:
- Use normal distributions for most variables (rnorm)
- Use Poisson for count events (rpois)
- Calculate Value at Risk (VaR) - 95th percentile
- Calculate Conditional Value at Risk (CVaR)
- Provide confidence intervals (80%, 95%)

PERFORMANCE REQUIREMENTS:
- 10,000 iterations in < 5 seconds
- Support budgets up to $150B
- Memory efficient (< 1GB RAM)
- Parallel processing support (future)

OUTPUT FORMAT:
R list with:
- Summary statistics (mean, median, SD)
- Probabilities (under budget, >5% over, >10% over)
- Risk metrics (VaR, CVaR)
- Full distributions (for plotting)

VISUALIZATION:
- Histogram with density overlay
- Vertical lines at key percentiles
- Annotations for probabilities
- Professional ggplot2 theme
- 300 DPI output for publication
```

### Expected Agent Output

The agent should produce:

**File: monte_carlo.R**
```r
#' Monte Carlo Budget Risk Analysis
#'
#' Simulates department budget execution with uncertainty to quantify risk
#'
#' @param dept_id Department identifier (character)
#' @param allocated_budget Total allocated budget in dollars (numeric)
#' @param iterations Number of Monte Carlo iterations (integer, default: 10000)
#'
#' @return List containing simulation results:
#'   - dept_id: Department identifier
#'   - allocated_budget: Budget amount
#'   - mean_expenditure: Expected expenditure
#'   - prob_under_budget: Probability of staying under budget
#'   - prob_over_5pct: Probability of exceeding budget by >5%
#'   - var_95: Value at Risk (95th percentile)
#'   - simulated_expenditures: Full distribution (vector)
#'
#' @examples
#' results <- monte_carlo_budget_risk("DHCS", 124000000000, iterations = 10000)
#' print(paste("Mean expenditure:", results$mean_expenditure))
#' print(paste("Prob over budget:", 1 - results$prob_under_budget))
#'
#' @export
monte_carlo_budget_risk <- function(dept_id, allocated_budget, iterations = 10000) {
  
  # Input validation
  if (!is.character(dept_id) || nchar(dept_id) == 0) {
    stop("dept_id must be a non-empty character string")
  }
  
  if (!is.numeric(allocated_budget) || allocated_budget <= 0) {
    stop("allocated_budget must be a positive number")
  }
  
  if (!is.numeric(iterations) || iterations < 1000 || iterations > 100000) {
    stop("iterations must be between 1,000 and 100,000")
  }
  
  # Log execution
  message(sprintf("Running Monte Carlo simulation for %s with %s iterations...", 
                 dept_id, format(iterations, big.mark = ",")))
  
  # Historical parameters (would come from database in production)
  # These are example values - replace with actual historical variance data
  historical_variance_mean <- 0.02  # 2% average overrun
  historical_variance_sd <- 0.05    # 5% standard deviation
  
  # Risk factors
  salary_inflation <- rnorm(iterations, mean = 0.03, sd = 0.01)
  operational_costs <- rnorm(iterations, mean = 0.02, sd = 0.015)
  
  # Emergency/unexpected costs (Poisson-distributed events)
  emergency_events <- rpois(iterations, lambda = 2)
  emergency_cost_per_event <- 1000000  # $1M per emergency
  emergency_costs <- emergency_events * emergency_cost_per_event
  
  # Simulate total expenditures
  simulated_expenditures <- allocated_budget * (
    1 + 
    salary_inflation + 
    operational_costs + 
    rnorm(iterations, mean = historical_variance_mean, sd = historical_variance_sd)
  ) + emergency_costs
  
  # Calculate variance from budget
  variance <- simulated_expenditures - allocated_budget
  variance_pct <- (variance / allocated_budget) * 100
  
  # Probability calculations
  prob_under_budget <- mean(variance < 0)
  prob_over_5pct <- mean(variance_pct > 5)
  prob_over_10pct <- mean(variance_pct > 10)
  
  # Risk metrics
  var_95 <- quantile(variance, 0.95)
  var_99 <- quantile(variance, 0.99)
  
  # Conditional Value at Risk (average of worst 5%)
  cvar_95 <- mean(variance[variance >= var_95])
  
  # Expected Shortfall
  expected_shortfall <- ifelse(prob_under_budget < 1, 
                               mean(variance[variance > 0]), 
                               0)
  
  # Create results list
  results <- list(
    # Metadata
    dept_id = dept_id,
    allocated_budget = allocated_budget,
    iterations = iterations,
    simulation_date = Sys.time(),
    
    # Summary statistics
    mean_expenditure = mean(simulated_expenditures),
    median_expenditure = median(simulated_expenditures),
    sd_expenditure = sd(simulated_expenditures),
    
    mean_variance = mean(variance),
    median_variance = median(variance),
    sd_variance = sd(variance),
    
    # Probabilities
    prob_under_budget = prob_under_budget,
    prob_over_budget = 1 - prob_under_budget,
    prob_over_5pct = prob_over_5pct,
    prob_over_10pct = prob_over_10pct,
    
    # Risk metrics
    var_95 = as.numeric(var_95),
    var_99 = as.numeric(var_99),
    cvar_95 = cvar_95,
    expected_shortfall = expected_shortfall,
    
    # Percentiles
    percentiles = quantile(variance, probs = c(0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99)),
    
    # Full distributions (for plotting)
    simulated_expenditures = simulated_expenditures,
    variance = variance,
    variance_pct = variance_pct
  )
  
  # Set class for S3 methods
  class(results) <- c("monte_carlo_budget", "list")
  
  message("✓ Simulation complete")
  
  return(results)
}

#' Print method for monte_carlo_budget objects
#' @export
print.monte_carlo_budget <- function(x, ...) {
  cat("Monte Carlo Budget Risk Analysis\n")
  cat("=================================\n\n")
  cat(sprintf("Department: %s\n", x$dept_id))
  cat(sprintf("Allocated Budget: $%s\n", format(round(x$allocated_budget), big.mark = ",")))
  cat(sprintf("Iterations: %s\n\n", format(x$iterations, big.mark = ",")))
  
  cat("EXPECTED EXPENDITURE:\n")
  cat(sprintf("  Mean: $%s\n", format(round(x$mean_expenditure), big.mark = ",")))
  cat(sprintf("  Median: $%s\n", format(round(x$median_expenditure), big.mark = ",")))
  cat(sprintf("  Std Dev: $%s\n\n", format(round(x$sd_expenditure), big.mark = ",")))
  
  cat("PROBABILITIES:\n")
  cat(sprintf("  Under Budget: %.1f%%\n", x$prob_under_budget * 100))
  cat(sprintf("  Over Budget: %.1f%%\n", x$prob_over_budget * 100))
  cat(sprintf("  Over by >5%%: %.1f%%\n", x$prob_over_5pct * 100))
  cat(sprintf("  Over by >10%%: %.1f%%\n\n", x$prob_over_10pct * 100))
  
  cat("RISK METRICS:\n")
  cat(sprintf("  Value at Risk (95%%): $%s\n", format(round(x$var_95), big.mark = ",")))
  cat(sprintf("  Value at Risk (99%%): $%s\n", format(round(x$var_99), big.mark = ",")))
  cat(sprintf("  Conditional VaR (95%%): $%s\n", format(round(x$cvar_95), big.mark = ",")))
}

#' Plot method for monte_carlo_budget objects
#' @export
plot.monte_carlo_budget <- function(x, ...) {
  library(ggplot2)
  
  # Create data frame for plotting
  df <- data.frame(
    variance_pct = x$variance_pct
  )
  
  # Create histogram with density
  p <- ggplot(df, aes(x = variance_pct)) +
    geom_histogram(aes(y = ..density..), bins = 50, fill = "steelblue", alpha = 0.7) +
    geom_density(color = "darkred", size = 1.2) +
    geom_vline(xintercept = 0, linetype = "dashed", color = "black", size = 1) +
    geom_vline(xintercept = 5, linetype = "dashed", color = "orange", size = 1) +
    geom_vline(xintercept = 10, linetype = "dashed", color = "red", size = 1) +
    labs(
      title = paste("Budget Variance Distribution:", x$dept_id),
      subtitle = paste(format(x$iterations, big.mark = ","), "Monte Carlo iterations"),
      x = "Variance from Budget (%)",
      y = "Density"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(size = 16, face = "bold"),
      plot.subtitle = element_text(size = 12, color = "gray40")
    )
  
  print(p)
  return(invisible(p))
}

# [Additional functions: monte_carlo_fraud_risk, generate_monte_carlo_report, etc.]
# [Agent would continue generating all required functions...]
```

**File: test_monte_carlo.R**
```r
# Unit tests for Monte Carlo module
library(testthat)

test_that("monte_carlo_budget_risk validates inputs", {
  # Test invalid dept_id
  expect_error(monte_carlo_budget_risk("", 1000000, 1000))
  expect_error(monte_carlo_budget_risk(123, 1000000, 1000))
  
  # Test invalid budget
  expect_error(monte_carlo_budget_risk("TEST", -1000, 1000))
  expect_error(monte_carlo_budget_risk("TEST", 0, 1000))
  
  # Test invalid iterations
  expect_error(monte_carlo_budget_risk("TEST", 1000000, 500))
  expect_error(monte_carlo_budget_risk("TEST", 1000000, 200000))
})

test_that("monte_carlo_budget_risk returns correct structure", {
  results <- monte_carlo_budget_risk("TEST", 1000000, 1000)
  
  # Check return type
  expect_s3_class(results, "monte_carlo_budget")
  expect_type(results, "list")
  
  # Check required fields
  expect_true("dept_id" %in% names(results))
  expect_true("allocated_budget" %in% names(results))
  expect_true("mean_expenditure" %in% names(results))
  expect_true("prob_under_budget" %in% names(results))
  expect_true("var_95" %in% names(results))
  
  # Check probabilities are in [0, 1]
  expect_gte(results$prob_under_budget, 0)
  expect_lte(results$prob_under_budget, 1)
})

test_that("monte_carlo_budget_risk performance is acceptable", {
  # Should complete 10K iterations in < 5 seconds
  start_time <- Sys.time()
  results <- monte_carlo_budget_risk("TEST", 1000000000, 10000)
  end_time <- Sys.time()
  
  elapsed <- as.numeric(difftime(end_time, start_time, units = "secs"))
  expect_lt(elapsed, 5.0)
})

test_that("monte_carlo results are statistically reasonable", {
  set.seed(42)  # Reproducibility
  results <- monte_carlo_budget_risk("TEST", 1000000, 10000)
  
  # Mean should be close to budget (within 10%)
  expect_lt(abs(results$mean_expenditure - 1000000) / 1000000, 0.10)
  
  # Median should be close to mean (for normal distributions)
  expect_lt(abs(results$median_expenditure - results$mean_expenditure) / results$mean_expenditure, 0.05)
  
  # Some probability of going over budget
  expect_gt(results$prob_over_budget, 0.1)
})
```

**File: python_r_bridge.py (Monte Carlo section)**
```python
class RAnalytics:
    # ... existing code ...
    
    def monte_carlo_budget_risk(self, dept_id, allocated_budget, iterations=10000):
        """
        Run Monte Carlo budget risk simulation using R
        
        Args:
            dept_id (str): Department identifier
            allocated_budget (float): Total allocated budget in dollars
            iterations (int): Number of Monte Carlo iterations (default: 10,000)
            
        Returns:
            dict: Simulation results with statistics and probabilities
            
        Example:
            >>> r = RAnalytics()
            >>> results = r.monte_carlo_budget_risk("DHCS", 124_000_000_000)
            >>> print(f"Mean: ${results['mean_expenditure']:,.0f}")
            >>> print(f"Prob over budget: {results['prob_over_budget']*100:.1f}%")
        """
        try:
            # Call R function
            r_func = ro.r['monte_carlo_budget_risk']
            r_results = r_func(dept_id, allocated_budget, iterations)
            
            # Convert R list to Python dict
            results = {
                'dept_id': r_results.rx2('dept_id')[0],
                'allocated_budget': r_results.rx2('allocated_budget')[0],
                'iterations': r_results.rx2('iterations')[0],
                
                # Summary statistics
                'mean_expenditure': r_results.rx2('mean_expenditure')[0],
                'median_expenditure': r_results.rx2('median_expenditure')[0],
                'sd_expenditure': r_results.rx2('sd_expenditure')[0],
                
                # Probabilities
                'prob_under_budget': r_results.rx2('prob_under_budget')[0],
                'prob_over_budget': r_results.rx2('prob_over_budget')[0],
                'prob_over_5pct': r_results.rx2('prob_over_5pct')[0],
                'prob_over_10pct': r_results.rx2('prob_over_10pct')[0],
                
                # Risk metrics
                'var_95': r_results.rx2('var_95')[0],
                'var_99': r_results.rx2('var_99')[0],
                'cvar_95': r_results.rx2('cvar_95')[0],
                
                # Percentiles as dict
                'percentiles': {
                    '5%': r_results.rx2('percentiles')[0],
                    '25%': r_results.rx2('percentiles')[2],
                    '50%': r_results.rx2('percentiles')[3],
                    '75%': r_results.rx2('percentiles')[4],
                    '95%': r_results.rx2('percentiles')[6],
                }
            }
            
            return results
            
        except Exception as e:
            raise RuntimeError(f"Monte Carlo simulation failed: {str(e)}")
    
    def plot_monte_carlo(self, results, output_file):
        """
        Generate Monte Carlo visualization using R ggplot2
        
        Args:
            results (dict): Results from monte_carlo_budget_risk()
            output_file (str): Path to save PNG file
            
        Returns:
            str: Path to saved plot
        """
        try:
            # Call R plot method
            ro.r(f'''
            # Load results
            results <- readRDS("/tmp/mc_results.rds")
            
            # Generate plot
            p <- plot(results)
            
            # Save
            ggsave("{output_file}", plot = p, width = 10, height = 6, dpi = 300)
            ''')
            
            return output_file
            
        except Exception as e:
            raise RuntimeError(f"Plot generation failed: {str(e)}")
```

---

## MODULE 2: ANOMALY DETECTION

### Agent Instructions

```
TASK: Develop advanced anomaly detection module

REQUIREMENTS:
- Multi-method approach (IQR, Z-score, Modified Z-score, Benford's Law)
- Cross-validation (flag if 2+ methods agree)
- Confidence scoring (0-1 scale)
- Time series anomaly detection
- Seasonal decomposition
- Handle 1M+ transactions efficiently

DELIVERABLES:
1. anomaly_detection.R
   - detect_anomalies_multimethod(transactions)
   - time_series_anomaly_detection(transactions_ts)
   - seasonal_anomaly_detection(transactions_ts)
   - calculate_confidence_score(results)

2. Statistical Methods:
   - IQR outlier detection
   - Z-score (>3 SD)
   - Modified Z-score (robust)
   - Benford's Law test
   - Isolation Forest approximation

3. Integration:
   - Python wrapper
   - Pandas DataFrame conversion
   - Result parsing

4. Tests:
   - Known anomalies detection
   - False positive rate < 5%
   - Performance on 1M records
```

---

## MODULE 3: TIME SERIES FORECASTING

### Agent Instructions

```
TASK: Develop time series forecasting module

REQUIREMENTS:
- Auto ARIMA model selection
- Facebook Prophet implementation
- ETS (exponential smoothing)
- Model comparison and selection
- Seasonal adjustment
- Confidence intervals (80%, 95%)

DELIVERABLES:
1. time_series_forecast.R
   - arima_transaction_forecast(historical, periods)
   - prophet_forecast(historical, periods)
   - ets_forecast(historical, periods)
   - compare_models(historical)
   - select_best_model(comparison)

2. Model Features:
   - Automatic parameter selection
   - Seasonality detection
   - Holiday effects (California state holidays)
   - Trend change detection
   - Outlier handling

3. Output:
   - Point forecasts
   - Prediction intervals
   - Model diagnostics (AIC, BIC, RMSE)
   - Residual analysis
```

---

## DEPLOYMENT PACKAGE

### Agent Final Deliverables

The agent should produce a complete deployment package:

```
ca-state-auditor-r-analytics/
├── README.md (Installation and setup guide)
├── REQUIREMENTS.txt (R package dependencies)
│
├── r-analytics/
│   ├── monte_carlo.R
│   ├── anomaly_detection.R
│   ├── time_series_forecast.R
│   ├── regression_models.R
│   ├── publication_graphics.R
│   └── utils/
│       ├── db_connection.R
│       ├── data_preprocessing.R
│       └── logging.R
│
├── python-integration/
│   ├── r_analytics_bridge.py
│   ├── monte_carlo_wrapper.py
│   ├── anomaly_wrapper.py
│   └── forecast_wrapper.py
│
├── tests/
│   ├── test_monte_carlo.R
│   ├── test_anomaly_detection.R
│   ├── test_forecast.R
│   ├── test_python_integration.py
│   └── test_performance.R
│
├── examples/
│   ├── legislative_testimony.py
│   ├── fraud_investigation.py
│   ├── budget_forecast.py
│   └── sample_data/
│
├── docs/
│   ├── API_REFERENCE.md
│   ├── USER_GUIDE.md
│   ├── STATISTICAL_METHODS.md
│   └── TROUBLESHOOTING.md
│
├── deployment/
│   ├── install.sh
│   ├── setup_r_environment.sh
│   ├── install_packages.R
│   └── test_installation.sh
│
└── monitoring/
    ├── performance_benchmarks.R
    ├── quality_metrics.R
    └── usage_tracking.R
```

---

## QUALITY GATES

### Automated Checks the Agent Must Pass

**1. Code Quality**
```r
# All functions must have:
✓ roxygen2 documentation
✓ Input validation
✓ Error handling (tryCatch)
✓ Informative error messages
✓ Logging of key events
✓ Type checking
✓ Meaningful variable names
✓ Comments for complex logic
```

**2. Statistical Validity**
```r
# All statistical methods must:
✓ Use peer-reviewed algorithms
✓ Provide methodology references
✓ Include accuracy metrics
✓ Handle edge cases
✓ Validate assumptions
✓ Document limitations
```

**3. Performance**
```r
# All functions must:
✓ Handle 1M records in < 30 seconds
✓ Use memory efficiently (< 2GB for typical use)
✓ Support parallel processing (future)
✓ Provide progress indicators for long operations
✓ Clean up temporary objects
```

**4. Integration**
```python
# Python-R bridge must:
✓ Handle all R data types correctly
✓ Provide meaningful Python exceptions
✓ Support pandas DataFrames
✓ Return Python-native types
✓ Include usage examples
```

**5. Testing**
```r
# Test coverage must include:
✓ Unit tests (>80% code coverage)
✓ Integration tests (Python ↔ R)
✓ Performance benchmarks
✓ Edge cases and error conditions
✓ Known-good test cases
```

**6. Documentation**
```markdown
# Documentation must include:
✓ Function-level API docs
✓ Module-level overview
✓ Statistical methodology explanation
✓ Usage examples with output
✓ Interpretation guidelines
✓ Troubleshooting section
```

---

## USAGE EXAMPLE

### How to Deploy the Agent

```python
# File: deploy_r_analytics_agent.py

from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

# Load agent instructions
with open('r_analytics_agent_instructions.txt', 'r') as f:
    agent_instructions = f.read()

# Define development task
task = """
Develop the Monte Carlo budget risk simulation module for the California State 
Auditor system. This module will be used to quantify budget risk for legislative 
testimony and executive decision-making.

REQUIREMENTS:
- Function: monte_carlo_budget_risk(dept_id, allocated_budget, iterations)
- Support budgets from $100M to $150B
- Run 10,000 iterations in < 5 seconds
- Calculate VaR, CVaR, and probability distributions
- Generate publication-quality ggplot2 visualizations
- Include comprehensive roxygen2 documentation
- Provide Python wrapper via rpy2
- Include unit tests with >80% coverage

OUTPUT:
1. monte_carlo.R (complete R source code)
2. test_monte_carlo.R (test suite)
3. monte_carlo_wrapper.py (Python integration)
4. README.md (usage documentation)
5. example_usage.R (demonstration script)

CONTEXT:
This will be used by the California State Auditor to analyze budget risk for 
departments like DHCS ($124B), Caltrans ($15.7B), and 130 others. Results 
must be statistically rigorous and legally defensible for legislative testimony.
"""

# Execute agent
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    system=agent_instructions,
    messages=[{
        "role": "user",
        "content": task
    }]
)

# Save agent output
with open('monte_carlo_module.txt', 'w') as f:
    f.write(response.content[0].text)

print("✓ Monte Carlo module generated")
print(f"  Output length: {len(response.content[0].text)} characters")
```

---

## AGENT MONITORING

### Track Agent Progress

```python
# File: monitor_agent_development.py

import json
from datetime import datetime

class AgentMonitor:
    """
    Monitor R analytics agent development progress
    """
    
    def __init__(self):
        self.metrics = {
            'modules_completed': 0,
            'total_modules': 10,
            'lines_of_code': 0,
            'tests_written': 0,
            'docs_pages': 0,
            'quality_gates_passed': 0,
            'quality_gates_total': 6,
            'start_time': datetime.now(),
            'completion_time': None
        }
    
    def update_progress(self, module_name, status):
        """Update completion status"""
        self.metrics['modules_completed'] += 1
        
        # Log progress
        progress_pct = (self.metrics['modules_completed'] / 
                       self.metrics['total_modules'] * 100)
        
        print(f"✓ {module_name} {status}")
        print(f"  Progress: {progress_pct:.1f}% ({self.metrics['modules_completed']}/{self.metrics['total_modules']} modules)")
    
    def run_quality_gate(self, gate_name, test_func):
        """Execute quality gate check"""
        print(f"\nRunning quality gate: {gate_name}")
        
        try:
            result = test_func()
            if result:
                self.metrics['quality_gates_passed'] += 1
                print(f"  ✓ PASSED")
                return True
            else:
                print(f"  ✗ FAILED")
                return False
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            return False
    
    def generate_report(self):
        """Generate final development report"""
        
        elapsed = datetime.now() - self.metrics['start_time']
        
        report = f"""
R ANALYTICS DEVELOPMENT REPORT
{'='*60}

COMPLETION STATUS:
  Modules: {self.metrics['modules_completed']}/{self.metrics['total_modules']} ({self.metrics['modules_completed']/self.metrics['total_modules']*100:.1f}%)
  Quality Gates: {self.metrics['quality_gates_passed']}/{self.metrics['quality_gates_total']} ({self.metrics['quality_gates_passed']/self.metrics['quality_gates_total']*100:.1f}%)

CODE METRICS:
  Lines of R Code: {self.metrics['lines_of_code']:,}
  Lines of Python: {self.metrics.get('python_lines', 0):,}
  Test Cases: {self.metrics['tests_written']}
  Documentation Pages: {self.metrics['docs_pages']}

TIME:
  Start: {self.metrics['start_time'].strftime('%Y-%m-%d %H:%M')}
  Duration: {elapsed}
  
STATUS: {"✓ COMPLETE" if self.metrics['modules_completed'] == self.metrics['total_modules'] else "⚠ IN PROGRESS"}
"""
        
        return report

# Usage
monitor = AgentMonitor()

# Module 1
monitor.update_progress("Monte Carlo Simulations", "completed")
monitor.metrics['lines_of_code'] += 500
monitor.metrics['tests_written'] += 15

# Module 2
monitor.update_progress("Anomaly Detection", "completed")
monitor.metrics['lines_of_code'] += 600
monitor.metrics['tests_written'] += 20

# Quality gates
monitor.run_quality_gate("Code Quality", lambda: True)
monitor.run_quality_gate("Statistical Validity", lambda: True)
monitor.run_quality_gate("Performance", lambda: True)

# Final report
print(monitor.generate_report())
```

---

## CONCLUSION

This R Analytics Development Agent provides:

✅ **Autonomous Development** - Complete 160-hour development cycle  
✅ **Quality Assurance** - Built-in testing and validation  
✅ **Production-Ready Code** - Enterprise-grade outputs  
✅ **Comprehensive Documentation** - Technical and user guides  
✅ **Seamless Integration** - Python-R bridge included  
✅ **Statistical Rigor** - Peer-reviewed methods  

**Deployment Instructions:**
1. Load agent with system prompt
2. Provide module specifications
3. Agent generates complete module
4. Validate with quality gates
5. Deploy to production

**Cost Savings:**
- Manual development: $15K (2 weeks)
- Agent development: $500 (API costs)
- **Savings: $14,500 (96%)**

**Time Savings:**
- Manual: 160 hours
- Agent: 8 hours (supervision)
- **Savings: 152 hours**

---

**Prepared by:** California State Auditor AI Development Team  
**Date:** February 7, 2026  
**Classification:** Official State Government Use  

**END OF R ANALYTICS DEVELOPMENT AGENT GUIDE**
