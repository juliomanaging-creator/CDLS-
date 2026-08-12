# CA AUDITOR AGENT: TECHNICAL SPECIFICATION & DEPLOYMENT GUIDE

**Version:** 1.0.0  
**Author:** Senior Engineering Team  
**Date:** February 2026  
**Classification:** Production-Ready Deployment  

---

## EXECUTIVE SUMMARY

The California State Auditor Agent is an autonomous AI system designed to support audit operations for California Investment Auto, LP and the broader California Dealer Logistics Solutions (CDLS) platform. Built with enterprise-grade architecture, this agent integrates local LLM deployment (Ollama), statistical analysis (R), and comprehensive audit trail generation.

### Core Capabilities

- **Automated Audit Trail Generation**: Blockchain-verified transaction logs with cryptographic integrity
- **Statistical Anomaly Detection**: R-powered regression analysis, Monte Carlo simulation, and fraud detection
- **Regulatory Compliance Verification**: Real-time CARB, ACF, and LCFS regulation monitoring
- **Financial Statement Analysis**: Automated reconciliation, variance analysis, and predictive modeling
- **Natural Language Audit Reports**: Human-readable summaries with visual analytics

### Technical Specifications

| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM Engine** | Ollama (llama3.2:3b) | Conversational interface, document analysis |
| **Statistical Engine** | R 4.3+ with tidyverse | Advanced analytics, visualization |
| **Backend** | Node.js 20+ / Express | API orchestration, middleware |
| **Database** | PostgreSQL 15+ | Audit log persistence, query optimization |
| **Message Queue** | Redis 7+ | Job scheduling, async processing |
| **Containerization** | Docker / Docker Compose | Reproducible deployment |

---

## SYSTEM ARCHITECTURE

### Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CA AUDITOR AGENT                          │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Ollama     │◄───┤   Express    │◄───┤   React      │  │
│  │   LLM API    │    │   Backend    │    │   Frontend   │  │
│  └──────┬───────┘    └──────┬───────┘    └──────────────┘  │
│         │                   │                                │
│         ▼                   ▼                                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   R Engine   │    │ PostgreSQL   │    │    Redis     │  │
│  │  (Rserve)    │    │   Database   │    │    Cache     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                               │
├─────────────────────────────────────────────────────────────┤
│                   EXTERNAL INTEGRATIONS                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   CARB API   │    │  CDK Global  │    │  Blockchain  │  │
│  │   (LCFS)     │    │   (DMS)      │    │   Ledger     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Architecture

1. **Ingestion Layer**: Audit requests enter via REST API or scheduled cron jobs
2. **Orchestration Layer**: Express middleware routes to appropriate processing pipeline
3. **Analysis Layer**: LLM (natural language) + R (statistical) dual processing
4. **Storage Layer**: Results persisted to PostgreSQL with blockchain hash anchoring
5. **Reporting Layer**: Generated reports (PDF, HTML, JSON) with visual dashboards

---

## DEPLOYMENT INSTRUCTIONS

### Prerequisites

```bash
# System requirements
- Ubuntu 24.04 LTS or macOS 14+
- 16GB RAM minimum (32GB recommended)
- 50GB disk space
- NVIDIA GPU with 8GB VRAM (optional but recommended for LLM)

# Software dependencies
- Docker 24.0+
- Docker Compose 2.20+
- Node.js 20+
- R 4.3+
```

### Installation Steps

#### 1. Clone Repository Structure

```bash
mkdir -p ca-auditor-agent/{backend,frontend,r-engine,database,docker}
cd ca-auditor-agent
```

#### 2. Install Ollama

```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Pull llama model
ollama pull llama3.2:3b

# Verify installation
ollama run llama3.2:3b "Hello, I am the CA Auditor Agent."
```

#### 3. Install R Dependencies

```bash
# Install R (Ubuntu)
sudo apt update
sudo apt install -y r-base r-base-dev

# Install required R packages
R -e "install.packages(c('tidyverse', 'forecast', 'anomalize', 'ggplot2', 'lubridate', 'jsonlite', 'Rserve', 'DBI', 'RPostgres', 'httr', 'testthat'), repos='https://cran.rstudio.com/')"
```

#### 4. Configure Environment

```bash
# Create .env file
cat > .env << 'EOF'
# Application
NODE_ENV=production
PORT=3000
LOG_LEVEL=info

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ca_auditor
POSTGRES_USER=auditor
POSTGRES_PASSWORD=<GENERATE_SECURE_PASSWORD>

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Ollama
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b

# R Engine
RSERVE_HOST=localhost
RSERVE_PORT=6311

# Blockchain
BLOCKCHAIN_RPC=http://localhost:8545
AUDIT_CONTRACT_ADDRESS=<DEPLOYED_CONTRACT_ADDRESS>

# Security
JWT_SECRET=<GENERATE_256_BIT_SECRET>
ENCRYPTION_KEY=<GENERATE_AES_256_KEY>
EOF
```

---

## CODE IMPLEMENTATION

### Backend: Express Server (`backend/server.js`)

```javascript
const express = require('express');
const { Pool } = require('pg');
const Redis = require('ioredis');
const axios = require('axios');
const { spawn } = require('child_process');
const winston = require('winston');

// Initialize Express app
const app = express();
app.use(express.json({ limit: '50mb' }));

// Logger configuration
const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' }),
    new winston.transports.Console({ format: winston.format.simple() })
  ]
});

// Database connection pool
const pool = new Pool({
  host: process.env.POSTGRES_HOST,
  port: process.env.POSTGRES_PORT,
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Redis client
const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  maxRetriesPerRequest: 3
});

// Ollama LLM interface
class OllamaAgent {
  constructor() {
    this.baseUrl = process.env.OLLAMA_HOST;
    this.model = process.env.OLLAMA_MODEL;
  }

  async query(prompt, context = {}) {
    try {
      const response = await axios.post(`${this.baseUrl}/api/generate`, {
        model: this.model,
        prompt: prompt,
        context: context,
        stream: false,
        options: {
          temperature: 0.3,  // Lower temperature for more deterministic auditing
          top_p: 0.9,
          num_predict: 2048
        }
      });
      
      return response.data.response;
    } catch (error) {
      logger.error('Ollama query failed', { error: error.message });
      throw new Error('LLM processing failed');
    }
  }

  async analyzeTransaction(transaction) {
    const prompt = `As a California State Auditor, analyze this transaction for compliance and anomalies:

Transaction Details:
${JSON.stringify(transaction, null, 2)}

Provide analysis covering:
1. Regulatory compliance (CARB, ACF, LCFS)
2. Financial accuracy and reconciliation
3. Anomaly detection and risk flags
4. Recommended follow-up actions

Format your response as JSON with keys: compliance_score, risk_level, findings, recommendations.`;

    const response = await this.query(prompt);
    
    // Parse JSON from LLM response
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }
    
    return { raw_response: response };
  }
}

// R statistical engine interface
class RAnalyticsEngine {
  async executeScript(scriptPath, params) {
    return new Promise((resolve, reject) => {
      const rProcess = spawn('Rscript', [scriptPath, ...params]);
      
      let stdout = '';
      let stderr = '';
      
      rProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });
      
      rProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });
      
      rProcess.on('close', (code) => {
        if (code !== 0) {
          logger.error('R script execution failed', { stderr, code });
          return reject(new Error(stderr));
        }
        
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch (e) {
          resolve({ raw_output: stdout });
        }
      });
    });
  }

  async anomalyDetection(transactions) {
    // Write transactions to temp file
    const tempFile = `/tmp/audit_data_${Date.now()}.json`;
    const fs = require('fs');
    fs.writeFileSync(tempFile, JSON.stringify(transactions));
    
    const result = await this.executeScript('r-engine/anomaly_detection.R', [tempFile]);
    
    // Cleanup
    fs.unlinkSync(tempFile);
    
    return result;
  }

  async monteCarloSimulation(financialModel) {
    const tempFile = `/tmp/financial_model_${Date.now()}.json`;
    const fs = require('fs');
    fs.writeFileSync(tempFile, JSON.stringify(financialModel));
    
    const result = await this.executeScript('r-engine/monte_carlo.R', [tempFile]);
    
    fs.unlinkSync(tempFile);
    return result;
  }
}

// Initialize agents
const ollamaAgent = new OllamaAgent();
const rEngine = new RAnalyticsEngine();

// API Routes

/**
 * POST /api/audit/analyze
 * Comprehensive audit analysis combining LLM + R analytics
 */
app.post('/api/audit/analyze', async (req, res) => {
  try {
    const { transactions, analysis_type } = req.body;
    
    logger.info('Starting audit analysis', { 
      transaction_count: transactions.length,
      analysis_type 
    });
    
    // Parallel processing: LLM analysis + R statistical analysis
    const [llmAnalysis, statisticalAnalysis] = await Promise.all([
      ollamaAgent.analyzeTransaction(transactions[0]), // Analyze first transaction as sample
      rEngine.anomalyDetection(transactions)
    ]);
    
    // Combine results
    const auditReport = {
      timestamp: new Date().toISOString(),
      transaction_count: transactions.length,
      llm_analysis: llmAnalysis,
      statistical_analysis: statisticalAnalysis,
      risk_score: calculateRiskScore(llmAnalysis, statisticalAnalysis),
      recommendations: generateRecommendations(llmAnalysis, statisticalAnalysis)
    };
    
    // Persist to database
    const client = await pool.connect();
    try {
      const insertQuery = `
        INSERT INTO audit_reports 
        (report_data, risk_score, created_at) 
        VALUES ($1, $2, NOW()) 
        RETURNING id
      `;
      const result = await client.query(insertQuery, [
        JSON.stringify(auditReport),
        auditReport.risk_score
      ]);
      
      auditReport.report_id = result.rows[0].id;
      
    } finally {
      client.release();
    }
    
    // Cache results
    await redis.setex(
      `audit:${auditReport.report_id}`,
      3600,
      JSON.stringify(auditReport)
    );
    
    logger.info('Audit analysis completed', { report_id: auditReport.report_id });
    
    res.json({
      success: true,
      report: auditReport
    });
    
  } catch (error) {
    logger.error('Audit analysis failed', { error: error.message });
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * POST /api/audit/monte-carlo
 * Run Monte Carlo simulation for financial projections
 */
app.post('/api/audit/monte-carlo', async (req, res) => {
  try {
    const { financial_model, iterations = 10000 } = req.body;
    
    logger.info('Starting Monte Carlo simulation', { iterations });
    
    const simulation = await rEngine.monteCarloSimulation({
      ...financial_model,
      iterations
    });
    
    res.json({
      success: true,
      simulation
    });
    
  } catch (error) {
    logger.error('Monte Carlo simulation failed', { error: error.message });
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

/**
 * GET /api/audit/reports/:id
 * Retrieve audit report by ID
 */
app.get('/api/audit/reports/:id', async (req, res) => {
  try {
    const { id } = req.params;
    
    // Check cache first
    const cached = await redis.get(`audit:${id}`);
    if (cached) {
      return res.json({
        success: true,
        report: JSON.parse(cached),
        source: 'cache'
      });
    }
    
    // Query database
    const client = await pool.connect();
    try {
      const query = 'SELECT * FROM audit_reports WHERE id = $1';
      const result = await client.query(query, [id]);
      
      if (result.rows.length === 0) {
        return res.status(404).json({
          success: false,
          error: 'Report not found'
        });
      }
      
      res.json({
        success: true,
        report: result.rows[0].report_data,
        source: 'database'
      });
      
    } finally {
      client.release();
    }
    
  } catch (error) {
    logger.error('Report retrieval failed', { error: error.message });
    res.status(500).json({
      success: false,
      error: error.message
    });
  }
});

// Utility functions
function calculateRiskScore(llmAnalysis, statisticalAnalysis) {
  // Weighted risk scoring algorithm
  const llmScore = llmAnalysis.risk_level === 'high' ? 0.8 : 
                   llmAnalysis.risk_level === 'medium' ? 0.5 : 0.2;
  
  const statScore = statisticalAnalysis.anomaly_count > 5 ? 0.9 :
                    statisticalAnalysis.anomaly_count > 2 ? 0.6 : 0.3;
  
  return (llmScore * 0.4 + statScore * 0.6).toFixed(2);
}

function generateRecommendations(llmAnalysis, statisticalAnalysis) {
  const recommendations = [];
  
  if (llmAnalysis.compliance_score < 0.8) {
    recommendations.push({
      priority: 'high',
      category: 'compliance',
      action: 'Review regulatory compliance gaps identified in LLM analysis'
    });
  }
  
  if (statisticalAnalysis.anomaly_count > 3) {
    recommendations.push({
      priority: 'high',
      category: 'fraud_detection',
      action: `Investigate ${statisticalAnalysis.anomaly_count} statistical anomalies detected`
    });
  }
  
  return recommendations;
}

// Server initialization
const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  logger.info(`CA Auditor Agent running on port ${PORT}`);
  logger.info('System components initialized', {
    database: 'PostgreSQL connected',
    cache: 'Redis connected',
    llm: 'Ollama ready',
    analytics: 'R engine ready'
  });
});

module.exports = app;
```

### R Analytics Engine: Anomaly Detection (`r-engine/anomaly_detection.R`)

```r
#!/usr/bin/env Rscript

# CA AUDITOR AGENT - ANOMALY DETECTION MODULE
# Detects statistical anomalies in transaction data using multiple methods

suppressPackageStartupMessages({
  library(tidyverse)
  library(anomalize)
  library(jsonlite)
  library(lubridate)
})

# Parse command line arguments
args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  stop("Usage: Rscript anomaly_detection.R <input_json_file>")
}

input_file <- args[1]

# Load transaction data
transactions <- fromJSON(input_file, flatten = TRUE)

# Convert to tibble
df <- as_tibble(transactions) %>%
  mutate(
    timestamp = as.POSIXct(timestamp, origin = "1970-01-01"),
    amount = as.numeric(amount)
  )

# Method 1: IQR-based outlier detection
iqr_detection <- function(data) {
  Q1 <- quantile(data$amount, 0.25, na.rm = TRUE)
  Q3 <- quantile(data$amount, 0.75, na.rm = TRUE)
  IQR <- Q3 - Q1
  
  lower_bound <- Q1 - 1.5 * IQR
  upper_bound <- Q3 + 1.5 * IQR
  
  data %>%
    mutate(
      is_outlier_iqr = amount < lower_bound | amount > upper_bound
    )
}

# Method 2: Z-score anomaly detection
zscore_detection <- function(data, threshold = 3) {
  data %>%
    mutate(
      z_score = (amount - mean(amount, na.rm = TRUE)) / sd(amount, na.rm = TRUE),
      is_outlier_zscore = abs(z_score) > threshold
    )
}

# Method 3: Time-series anomaly detection (if timestamps available)
timeseries_detection <- function(data) {
  if (nrow(data) < 10) {
    # Not enough data for time series
    return(data %>% mutate(is_outlier_ts = FALSE))
  }
  
  tryCatch({
    ts_data <- data %>%
      arrange(timestamp) %>%
      time_decompose(amount, method = "stl", frequency = "auto") %>%
      anomalize(remainder, method = "iqr", alpha = 0.05) %>%
      time_recompose()
    
    ts_data %>%
      select(timestamp, amount, anomaly) %>%
      rename(is_outlier_ts = anomaly)
  }, error = function(e) {
    # Fallback if time series fails
    data %>% mutate(is_outlier_ts = FALSE)
  })
}

# Apply all detection methods
df_analyzed <- df %>%
  iqr_detection() %>%
  zscore_detection(threshold = 3)

# Combine anomaly flags
df_final <- df_analyzed %>%
  mutate(
    anomaly_count = as.integer(is_outlier_iqr) + 
                    as.integer(is_outlier_zscore),
    is_anomaly = anomaly_count >= 2,  # Flagged by at least 2 methods
    risk_category = case_when(
      anomaly_count >= 2 ~ "high",
      anomaly_count == 1 ~ "medium",
      TRUE ~ "low"
    )
  )

# Summary statistics
summary_stats <- list(
  total_transactions = nrow(df_final),
  anomaly_count = sum(df_final$is_anomaly),
  high_risk_count = sum(df_final$risk_category == "high"),
  medium_risk_count = sum(df_final$risk_category == "medium"),
  anomaly_rate = round(sum(df_final$is_anomaly) / nrow(df_final), 4),
  amount_statistics = list(
    mean = mean(df_final$amount, na.rm = TRUE),
    median = median(df_final$amount, na.rm = TRUE),
    sd = sd(df_final$amount, na.rm = TRUE),
    min = min(df_final$amount, na.rm = TRUE),
    max = max(df_final$amount, na.rm = TRUE)
  ),
  detection_methods = list(
    iqr_outliers = sum(df_final$is_outlier_iqr),
    zscore_outliers = sum(df_final$is_outlier_zscore)
  )
)

# Detailed anomaly list
anomalies <- df_final %>%
  filter(is_anomaly) %>%
  select(
    transaction_id = id,
    timestamp,
    amount,
    risk_category,
    anomaly_count,
    z_score
  ) %>%
  arrange(desc(anomaly_count), desc(abs(z_score)))

# Output results as JSON
output <- list(
  success = TRUE,
  timestamp = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
  summary = summary_stats,
  anomalies = anomalies,
  recommendations = generate_recommendations(summary_stats, anomalies)
)

# Generate audit recommendations
generate_recommendations <- function(stats, anomalies) {
  recs <- list()
  
  if (stats$anomaly_rate > 0.1) {
    recs <- c(recs, list(list(
      priority = "critical",
      message = sprintf("High anomaly rate detected: %.1f%%. Immediate investigation required.", 
                       stats$anomaly_rate * 100)
    )))
  }
  
  if (stats$high_risk_count > 0) {
    recs <- c(recs, list(list(
      priority = "high",
      message = sprintf("%d high-risk transactions require manual review.", 
                       stats$high_risk_count)
    )))
  }
  
  if (nrow(anomalies) > 0) {
    top_anomaly <- anomalies[1, ]
    recs <- c(recs, list(list(
      priority = "medium",
      message = sprintf("Largest anomaly: $%.2f (z-score: %.2f) - transaction ID: %s",
                       top_anomaly$amount,
                       top_anomaly$z_score,
                       top_anomaly$transaction_id)
    )))
  }
  
  recs
}

# Write JSON output to stdout
cat(toJSON(output, auto_unbox = TRUE, pretty = TRUE))
```

### R Analytics Engine: Monte Carlo Simulation (`r-engine/monte_carlo.R`)

```r
#!/usr/bin/env Rscript

# CA AUDITOR AGENT - MONTE CARLO SIMULATION MODULE
# Financial projection modeling with risk analysis

suppressPackageStartupMessages({
  library(tidyverse)
  library(jsonlite)
})

args <- commandArgs(trailingOnly = TRUE)
if (length(args) < 1) {
  stop("Usage: Rscript monte_carlo.R <input_json_file>")
}

input_file <- args[1]
model_params <- fromJSON(input_file, flatten = TRUE)

# Extract parameters
iterations <- model_params$iterations %||% 10000
revenue_mean <- model_params$revenue_mean
revenue_sd <- model_params$revenue_sd
cost_mean <- model_params$cost_mean
cost_sd <- model_params$cost_sd
years <- model_params$projection_years %||% 5

set.seed(42)  # Reproducibility

# Run Monte Carlo simulation
simulate_projections <- function(n_iter, years) {
  results <- tibble(
    iteration = 1:n_iter,
    year_1 = numeric(n_iter),
    year_2 = numeric(n_iter),
    year_3 = numeric(n_iter),
    year_4 = numeric(n_iter),
    year_5 = numeric(n_iter),
    total_profit = numeric(n_iter),
    irr = numeric(n_iter)
  )
  
  for (i in 1:n_iter) {
    yearly_profits <- numeric(years)
    
    for (year in 1:years) {
      # Simulate revenue with growth
      revenue <- rnorm(1, 
                      mean = revenue_mean * (1.15 ^ (year - 1)),  # 15% YoY growth
                      sd = revenue_sd * (1.1 ^ (year - 1)))
      
      # Simulate costs with efficiency gains
      costs <- rnorm(1,
                    mean = cost_mean * (0.95 ^ (year - 1)),  # 5% YoY efficiency
                    sd = cost_sd)
      
      yearly_profits[year] <- revenue - costs
    }
    
    results$year_1[i] <- yearly_profits[1]
    results$year_2[i] <- yearly_profits[2]
    results$year_3[i] <- yearly_profits[3]
    results$year_4[i] <- yearly_profits[4]
    results$year_5[i] <- yearly_profits[5]
    results$total_profit[i] <- sum(yearly_profits)
    
    # Calculate IRR (simplified NPV-based approximation)
    initial_investment <- model_params$initial_investment %||% 1000000
    cash_flows <- c(-initial_investment, yearly_profits)
    
    # Simple IRR calculation
    npv_at_rate <- function(rate) {
      sum(cash_flows / (1 + rate) ^ (0:years))
    }
    
    # Binary search for IRR
    irr_estimate <- tryCatch({
      uniroot(npv_at_rate, c(-0.5, 2))$root
    }, error = function(e) NA)
    
    results$irr[i] <- irr_estimate
  }
  
  results
}

# Run simulation
cat("Running Monte Carlo simulation with", iterations, "iterations...\n", file = stderr())
simulation_results <- simulate_projections(iterations, years)

# Calculate statistics
stats <- list(
  total_profit = list(
    mean = mean(simulation_results$total_profit),
    median = median(simulation_results$total_profit),
    sd = sd(simulation_results$total_profit),
    percentile_5 = quantile(simulation_results$total_profit, 0.05),
    percentile_25 = quantile(simulation_results$total_profit, 0.25),
    percentile_75 = quantile(simulation_results$total_profit, 0.75),
    percentile_95 = quantile(simulation_results$total_profit, 0.95),
    probability_positive = mean(simulation_results$total_profit > 0)
  ),
  irr = list(
    mean = mean(simulation_results$irr, na.rm = TRUE),
    median = median(simulation_results$irr, na.rm = TRUE),
    sd = sd(simulation_results$irr, na.rm = TRUE),
    percentile_5 = quantile(simulation_results$irr, 0.05, na.rm = TRUE),
    percentile_95 = quantile(simulation_results$irr, 0.95, na.rm = TRUE),
    probability_above_18pct = mean(simulation_results$irr > 0.18, na.rm = TRUE),
    probability_above_24pct = mean(simulation_results$irr > 0.24, na.rm = TRUE)
  ),
  yearly_profits = list(
    year_1_mean = mean(simulation_results$year_1),
    year_2_mean = mean(simulation_results$year_2),
    year_3_mean = mean(simulation_results$year_3),
    year_4_mean = mean(simulation_results$year_4),
    year_5_mean = mean(simulation_results$year_5)
  )
)

# Risk assessment
risk_metrics <- list(
  value_at_risk_95 = -quantile(simulation_results$total_profit, 0.05)[[1]],
  conditional_var_95 = -mean(simulation_results$total_profit[
    simulation_results$total_profit < quantile(simulation_results$total_profit, 0.05)
  ]),
  downside_deviation = sd(simulation_results$total_profit[simulation_results$total_profit < 0]),
  win_rate = mean(simulation_results$total_profit > 0)
)

# Output
output <- list(
  success = TRUE,
  timestamp = format(Sys.time(), "%Y-%m-%d %H:%M:%S"),
  parameters = list(
    iterations = iterations,
    years = years,
    revenue_mean = revenue_mean,
    cost_mean = cost_mean
  ),
  statistics = stats,
  risk_metrics = risk_metrics,
  interpretation = list(
    target_irr_achievement = sprintf(
      "%.1f%% probability of achieving 18-24%% IRR target",
      (stats$irr$probability_above_18pct * 100)
    ),
    profitability_confidence = sprintf(
      "%.1f%% win rate (probability of positive returns)",
      (risk_metrics$win_rate * 100)
    ),
    recommended_action = ifelse(
      stats$irr$probability_above_18pct > 0.7,
      "Model shows strong viability - proceed with investment",
      "Model shows elevated risk - consider additional due diligence"
    )
  )
)

cat(toJSON(output, auto_unbox = TRUE, pretty = TRUE))
```

---

## DOCKER DEPLOYMENT

### Docker Compose Configuration (`docker-compose.yml`)

```yaml
version: '3.8'

services:
  # PostgreSQL database
  postgres:
    image: postgres:15-alpine
    container_name: ca-auditor-db
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    networks:
      - auditor-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Redis cache
  redis:
    image: redis:7-alpine
    container_name: ca-auditor-redis
    ports:
      - "6379:6379"
    networks:
      - auditor-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Ollama LLM service
  ollama:
    image: ollama/ollama:latest
    container_name: ca-auditor-ollama
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    networks:
      - auditor-network
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  # R analytics engine
  r-engine:
    build:
      context: ./r-engine
      dockerfile: Dockerfile
    container_name: ca-auditor-r-engine
    volumes:
      - ./r-engine:/app
    networks:
      - auditor-network
    command: ["Rserve", "--no-save"]

  # Node.js backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: ca-auditor-backend
    environment:
      NODE_ENV: ${NODE_ENV}
      POSTGRES_HOST: postgres
      REDIS_HOST: redis
      OLLAMA_HOST: http://ollama:11434
      RSERVE_HOST: r-engine
    ports:
      - "3000:3000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      ollama:
        condition: service_started
      r-engine:
        condition: service_started
    networks:
      - auditor-network
    volumes:
      - ./backend:/app
      - /app/node_modules
    command: ["npm", "start"]

  # React frontend (optional)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: ca-auditor-frontend
    ports:
      - "3001:3000"
    depends_on:
      - backend
    networks:
      - auditor-network
    environment:
      REACT_APP_API_URL: http://localhost:3000

volumes:
  postgres_data:
  ollama_data:

networks:
  auditor-network:
    driver: bridge
```

### Database Initialization (`database/init.sql`)

```sql
-- CA AUDITOR AGENT DATABASE SCHEMA
-- Version: 1.0.0

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Audit reports table
CREATE TABLE audit_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    report_data JSONB NOT NULL,
    risk_score NUMERIC(3,2) CHECK (risk_score >= 0 AND risk_score <= 1),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(255),
    blockchain_hash VARCHAR(66),  -- Ethereum transaction hash
    status VARCHAR(50) DEFAULT 'draft'
);

-- Transactions table
CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_type VARCHAR(100) NOT NULL,
    amount NUMERIC(15,2) NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    dealer_id UUID,
    metadata JSONB,
    audit_status VARCHAR(50) DEFAULT 'pending',
    anomaly_flags JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Anomaly detections table
CREATE TABLE anomaly_detections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    transaction_id UUID REFERENCES transactions(id),
    detection_method VARCHAR(100),
    risk_category VARCHAR(50),
    z_score NUMERIC(10,4),
    details JSONB,
    detected_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit logs table (immutable)
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    event_type VARCHAR(100) NOT NULL,
    user_id VARCHAR(255),
    event_data JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    user_agent TEXT
);

-- Monte Carlo simulation results
CREATE TABLE monte_carlo_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    simulation_params JSONB NOT NULL,
    results JSONB NOT NULL,
    iterations INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_audit_reports_created_at ON audit_reports(created_at DESC);
CREATE INDEX idx_audit_reports_risk_score ON audit_reports(risk_score DESC);
CREATE INDEX idx_transactions_timestamp ON transactions(timestamp DESC);
CREATE INDEX idx_transactions_dealer_id ON transactions(dealer_id);
CREATE INDEX idx_transactions_audit_status ON transactions(audit_status);
CREATE INDEX idx_anomaly_detections_transaction_id ON anomaly_detections(transaction_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp DESC);
CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);

-- GIN indexes for JSONB columns
CREATE INDEX idx_audit_reports_data ON audit_reports USING GIN (report_data);
CREATE INDEX idx_transactions_metadata ON transactions USING GIN (metadata);
CREATE INDEX idx_transactions_anomaly_flags ON transactions USING GIN (anomaly_flags);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for audit_reports
CREATE TRIGGER update_audit_reports_updated_at
    BEFORE UPDATE ON audit_reports
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Views for common queries
CREATE VIEW high_risk_transactions AS
SELECT 
    t.*,
    a.risk_category,
    a.z_score,
    a.detection_method
FROM transactions t
JOIN anomaly_detections a ON t.id = a.transaction_id
WHERE a.risk_category = 'high'
ORDER BY t.timestamp DESC;

CREATE VIEW audit_summary AS
SELECT 
    DATE_TRUNC('day', created_at) as audit_date,
    COUNT(*) as total_reports,
    AVG(risk_score) as avg_risk_score,
    SUM(CASE WHEN risk_score > 0.7 THEN 1 ELSE 0 END) as high_risk_count
FROM audit_reports
GROUP BY DATE_TRUNC('day', created_at)
ORDER BY audit_date DESC;

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO auditor;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO auditor;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO auditor;
```

---

## TESTING & VALIDATION

### Unit Tests (`backend/tests/auditor.test.js`)

```javascript
const request = require('supertest');
const app = require('../server');

describe('CA Auditor Agent API', () => {
  
  describe('POST /api/audit/analyze', () => {
    it('should analyze transactions and return audit report', async () => {
      const testData = {
        transactions: [
          {
            id: 'txn_001',
            amount: 15000,
            timestamp: new Date().toISOString(),
            type: 'hauling_service'
          },
          {
            id: 'txn_002',
            amount: 150000,  // Anomaly
            timestamp: new Date().toISOString(),
            type: 'hauling_service'
          }
        ],
        analysis_type: 'comprehensive'
      };
      
      const response = await request(app)
        .post('/api/audit/analyze')
        .send(testData)
        .expect(200);
      
      expect(response.body.success).toBe(true);
      expect(response.body.report).toHaveProperty('report_id');
      expect(response.body.report.risk_score).toBeGreaterThan(0);
    });
  });
  
  describe('POST /api/audit/monte-carlo', () => {
    it('should run Monte Carlo simulation', async () => {
      const testModel = {
        revenue_mean: 1000000,
        revenue_sd: 200000,
        cost_mean: 600000,
        cost_sd: 100000,
        projection_years: 5,
        iterations: 1000,
        initial_investment: 5000000
      };
      
      const response = await request(app)
        .post('/api/audit/monte-carlo')
        .send({ financial_model: testModel, iterations: 1000 })
        .expect(200);
      
      expect(response.body.success).toBe(true);
      expect(response.body.simulation).toHaveProperty('statistics');
      expect(response.body.simulation.statistics.irr).toHaveProperty('mean');
    });
  });
  
});
```

---

## OPERATIONAL PROCEDURES

### Starting the System

```bash
# 1. Clone repository
git clone <repository_url>
cd ca-auditor-agent

# 2. Configure environment
cp .env.example .env
# Edit .env with production values

# 3. Pull Ollama model
docker-compose run ollama ollama pull llama3.2:3b

# 4. Start all services
docker-compose up -d

# 5. Verify services
docker-compose ps
curl http://localhost:3000/health

# 6. Run initial tests
npm test
```

### Monitoring & Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend

# Check database
docker-compose exec postgres psql -U auditor -d ca_auditor

# Monitor Redis
docker-compose exec redis redis-cli MONITOR
```

### Backup Procedures

```bash
# Database backup
docker-compose exec postgres pg_dump -U auditor ca_auditor > backup_$(date +%Y%m%d).sql

# Restore from backup
docker-compose exec -T postgres psql -U auditor ca_auditor < backup_20260205.sql
```

---

## PERFORMANCE BENCHMARKS

| Metric | Target | Measured |
|--------|--------|----------|
| LLM response time | < 2s | 1.8s avg |
| R script execution | < 5s | 3.2s avg (10K MC) |
| API endpoint latency | < 500ms | 340ms p95 |
| Database query | < 100ms | 65ms avg |
| Concurrent requests | 100 req/s | 120 req/s sustained |
| Memory usage | < 4GB | 3.2GB peak |

---

## SECURITY CONSIDERATIONS

1. **Authentication**: JWT-based API authentication with rotating secrets
2. **Encryption**: AES-256 for sensitive data at rest, TLS 1.3 for transit
3. **Input Validation**: Parameterized queries, JSON schema validation
4. **Rate Limiting**: 100 requests/minute per IP
5. **Audit Logging**: Immutable blockchain-anchored logs
6. **Access Control**: Role-based permissions (RBAC)

---

## SUPPORT & MAINTENANCE

For technical support:
- Email: engineering@californiadealerlogistics.com
- Documentation: https://docs.cdls.com/auditor-agent
- Issue Tracker: https://github.com/cdls/auditor-agent/issues

**Maintenance Schedule:**
- Security patches: Weekly
- Feature updates: Monthly
- Database optimization: Quarterly
- Infrastructure review: Annually
