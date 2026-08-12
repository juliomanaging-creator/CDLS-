// CDLS Platform - Backend API Server
// Production-ready Express.js application

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const rateLimit = require('express-rate-limit');
const { Pool } = require('pg');
const Redis = require('ioredis');
const WebSocket = require('ws');
const http = require('http');

// Import business logic modules
const { calculateDischargeCapacity } = require('./logic/v2g_engine');
const { validateTelemetry } = require('./logic/ledger_kernel');
const { runMCMCSimulation } = require('./logic/mcmc_simulator');

// ===========================================
// CONFIGURATION
// ===========================================

const app = express();
const PORT = process.env.PORT || 3001;
const server = http.createServer(app);

// Database connection pool
const db = new Pool({
  host: process.env.DB_HOST || 'localhost',
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME || 'cdls_platform',
  user: process.env.DB_USER || 'cdls_admin',
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

// Redis connection for caching MCMC results
const redis = new Redis({
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  retryStrategy: (times) => Math.min(times * 50, 2000),
});

// WebSocket server for real-time grid updates
const wss = new WebSocket.Server({ server });

// ===========================================
// MIDDLEWARE
// ===========================================

// Security headers
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
}));

// CORS configuration
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true,
}));

// Request parsing
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true }));

// HTTP request logging
app.use(morgan('combined', {
  skip: (req) => req.path === '/health',
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: parseInt(process.env.RATE_LIMIT_WINDOW_MS || '900000'), // 15 min
  max: parseInt(process.env.RATE_LIMIT_MAX_REQUESTS || '100'),
  message: 'Too many requests from this IP, please try again later.',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// ===========================================
// DATABASE INITIALIZATION
// ===========================================

async function initializeDatabase() {
  try {
    // Create fleet_telemetry table
    await db.query(`
      CREATE TABLE IF NOT EXISTS fleet_telemetry (
        id SERIAL PRIMARY KEY,
        unit_id VARCHAR(50) UNIQUE NOT NULL,
        battery_soc DECIMAL(5,2) NOT NULL CHECK (battery_soc >= 0 AND battery_soc <= 100),
        location_lat DECIMAL(10,8) NOT NULL,
        location_lon DECIMAL(11,8) NOT NULL,
        battery_kwh INTEGER NOT NULL,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        dealer_id VARCHAR(50),
        status VARCHAR(20) DEFAULT 'available',
        INDEX idx_unit_id (unit_id),
        INDEX idx_last_updated (last_updated)
      )
    `);

    // Create grid_events table
    await db.query(`
      CREATE TABLE IF NOT EXISTS grid_events (
        id SERIAL PRIMARY KEY,
        event_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        event_type VARCHAR(50) NOT NULL,
        price_multiplier DECIMAL(5,4) NOT NULL,
        predicted_capacity_mw DECIMAL(10,2),
        actual_capacity_mw DECIMAL(10,2),
        revenue_usd DECIMAL(12,2),
        mcmc_simulation_id VARCHAR(50),
        caiso_lmp DECIMAL(8,2),
        INDEX idx_timestamp (event_timestamp),
        INDEX idx_type (event_type)
      )
    `);

    // Create mcmc_simulations table
    await db.query(`
      CREATE TABLE IF NOT EXISTS mcmc_simulations (
        id SERIAL PRIMARY KEY,
        simulation_id VARCHAR(50) UNIQUE NOT NULL,
        run_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        iterations INTEGER NOT NULL,
        convergence_achieved BOOLEAN DEFAULT false,
        predicted_capacity_mean DECIMAL(10,2),
        predicted_capacity_std DECIMAL(10,2),
        confidence_interval_95_low DECIMAL(10,2),
        confidence_interval_95_high DECIMAL(10,2),
        execution_time_ms INTEGER,
        fleet_size INTEGER,
        parameters JSONB,
        results JSONB,
        INDEX idx_simulation_id (simulation_id),
        INDEX idx_timestamp (run_timestamp)
      )
    `);

    console.log('✅ Database tables initialized successfully');
  } catch (error) {
    console.error('❌ Database initialization error:', error);
    throw error;
  }
}

// ===========================================
// HEALTH CHECK ENDPOINT
// ===========================================

app.get('/health', async (req, res) => {
  try {
    // Check database connection
    await db.query('SELECT 1');
    
    // Check Redis connection
    await redis.ping();

    res.json({
      status: 'healthy',
      timestamp: new Date().toISOString(),
      services: {
        database: 'up',
        redis: 'up',
        api: 'up',
      },
      version: process.env.DEPLOY_VERSION || '1.0.0',
    });
  } catch (error) {
    res.status(503).json({
      status: 'unhealthy',
      error: error.message,
    });
  }
});

// ===========================================
// API ROUTES - V2G GRID OPTIMIZATION
// ===========================================

// POST /api/v2g/calculate-discharge
// Calculate optimal discharge strategy for current fleet
app.post('/api/v2g/calculate-discharge', async (req, res) => {
  try {
    const { gridStressSignal } = req.body;

    if (!gridStressSignal || gridStressSignal < 0 || gridStressSignal > 1) {
      return res.status(400).json({
        error: 'Invalid gridStressSignal (must be between 0.0 and 1.0)',
      });
    }

    // Fetch current fleet telemetry from database
    const result = await db.query(`
      SELECT unit_id, battery_soc, location_lat, location_lon, battery_kwh, dealer_id
      FROM fleet_telemetry
      WHERE status = 'available'
        AND battery_soc > $1
        AND last_updated > NOW() - INTERVAL '10 minutes'
    `, [parseFloat(process.env.GRID_SAFETY_BUFFER_SOC || 20)]);

    const fleetTelemetry = result.rows.map(row => ({
      unit_id: row.unit_id,
      battery_soc: parseFloat(row.battery_soc),
      location_lat_long: [parseFloat(row.location_lat), parseFloat(row.location_lon)],
      battery_kwh: parseInt(row.battery_kwh),
      dealer_id: row.dealer_id,
    }));

    if (fleetTelemetry.length === 0) {
      return res.status(404).json({
        error: 'No available fleet units with sufficient battery charge',
      });
    }

    // Calculate discharge capacity using proprietary V2G algorithm
    const dischargeStrategy = calculateDischargeCapacity(fleetTelemetry, gridStressSignal);

    // Calculate aggregate metrics
    const totalKwhToGrid = dischargeStrategy.reduce((sum, unit) => sum + parseFloat(unit.kwh_to_grid), 0);
    const totalRevenue = dischargeStrategy.reduce((sum, unit) => sum + parseFloat(unit.revenue_est), 0);

    // Log grid event to database
    await db.query(`
      INSERT INTO grid_events (event_type, price_multiplier, predicted_capacity_mw, revenue_usd)
      VALUES ($1, $2, $3, $4)
    `, ['discharge_calculation', gridStressSignal, totalKwhToGrid / 1000, totalRevenue]);

    res.json({
      success: true,
      timestamp: new Date().toISOString(),
      fleet_size: fleetTelemetry.length,
      grid_stress_signal: gridStressSignal,
      discharge_strategy: dischargeStrategy,
      aggregates: {
        total_kwh_to_grid: totalKwhToGrid.toFixed(2),
        total_capacity_mw: (totalKwhToGrid / 1000).toFixed(2),
        estimated_revenue_usd: totalRevenue.toFixed(2),
        avg_discharge_per_unit: (totalKwhToGrid / fleetTelemetry.length).toFixed(2),
      },
    });

    // Broadcast update to WebSocket clients
    broadcastGridUpdate({
      type: 'discharge_calculated',
      capacity_mw: (totalKwhToGrid / 1000).toFixed(2),
      revenue: totalRevenue.toFixed(2),
    });

  } catch (error) {
    console.error('Discharge calculation error:', error);
    res.status(500).json({
      error: 'Internal server error during discharge calculation',
      message: error.message,
    });
  }
});

// ===========================================
// API ROUTES - MCMC SIMULATION
// ===========================================

// POST /api/mcmc/simulate
// Run MCMC simulation for grid capacity prediction
app.post('/api/mcmc/simulate', async (req, res) => {
  try {
    const {
      target_datetime,
      iterations = parseInt(process.env.MCMC_ITERATIONS || 10000),
      parallel_chains = parseInt(process.env.MCMC_PARALLEL_CHAINS || 4),
    } = req.body;

    if (!target_datetime) {
      return res.status(400).json({
        error: 'target_datetime is required (ISO 8601 format)',
      });
    }

    // Check cache for recent simulation
    const cacheKey = `mcmc:${target_datetime}:${iterations}`;
    const cached = await redis.get(cacheKey);
    
    if (cached) {
      console.log('Returning cached MCMC result');
      return res.json({
        ...JSON.parse(cached),
        cached: true,
      });
    }

    // Fetch current fleet state
    const fleetResult = await db.query(`
      SELECT unit_id, battery_soc, location_lat, location_lon, battery_kwh, dealer_id
      FROM fleet_telemetry
      WHERE status != 'decommissioned'
        AND last_updated > NOW() - INTERVAL '1 hour'
    `);

    const fleetState = fleetResult.rows.map(row => ({
      unit_id: row.unit_id,
      battery_soc: parseFloat(row.battery_soc),
      location: [parseFloat(row.location_lat), parseFloat(row.location_lon)],
      battery_kwh: parseInt(row.battery_kwh),
      dealer_id: row.dealer_id,
    }));

    // Run MCMC simulation
    const startTime = Date.now();
    const simulationResult = await runMCMCSimulation({
      fleetState,
      target_datetime: new Date(target_datetime),
      iterations,
      parallel_chains,
    });
    const executionTime = Date.now() - startTime;

    // Store simulation results in database
    const simulation_id = `mcmc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    await db.query(`
      INSERT INTO mcmc_simulations (
        simulation_id, iterations, convergence_achieved,
        predicted_capacity_mean, predicted_capacity_std,
        confidence_interval_95_low, confidence_interval_95_high,
        execution_time_ms, fleet_size, parameters, results
      ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
    `, [
      simulation_id,
      iterations,
      simulationResult.convergence_achieved,
      simulationResult.predicted_capacity_mean,
      simulationResult.predicted_capacity_std,
      simulationResult.confidence_interval[0],
      simulationResult.confidence_interval[1],
      executionTime,
      fleetState.length,
      JSON.stringify({ target_datetime, parallel_chains }),
      JSON.stringify(simulationResult.chain_results),
    ]);

    const response = {
      success: true,
      simulation_id,
      timestamp: new Date().toISOString(),
      execution_time_ms: executionTime,
      fleet_size: fleetState.length,
      ...simulationResult,
      cached: false,
    };

    // Cache result for 5 minutes
    await redis.setex(
      cacheKey,
      parseInt(process.env.MCMC_CACHE_TTL || 300),
      JSON.stringify(response)
    );

    res.json(response);

  } catch (error) {
    console.error('MCMC simulation error:', error);
    res.status(500).json({
      error: 'MCMC simulation failed',
      message: error.message,
    });
  }
});

// ===========================================
// API ROUTES - FLEET TELEMETRY
// ===========================================

// POST /api/telemetry/update
// Update fleet telemetry data (called by vehicles/dealers)
app.post('/api/telemetry/update', async (req, res) => {
  try {
    const telemetryUpdates = Array.isArray(req.body) ? req.body : [req.body];

    // Validate telemetry data
    for (const update of telemetryUpdates) {
      const validationError = validateTelemetry(update);
      if (validationError) {
        return res.status(400).json({
          error: 'Telemetry validation failed',
          details: validationError,
        });
      }
    }

    // Upsert telemetry data
    const upsertPromises = telemetryUpdates.map(update =>
      db.query(`
        INSERT INTO fleet_telemetry (
          unit_id, battery_soc, location_lat, location_lon,
          battery_kwh, dealer_id, status, last_updated
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
        ON CONFLICT (unit_id) DO UPDATE SET
          battery_soc = EXCLUDED.battery_soc,
          location_lat = EXCLUDED.location_lat,
          location_lon = EXCLUDED.location_lon,
          battery_kwh = EXCLUDED.battery_kwh,
          dealer_id = EXCLUDED.dealer_id,
          status = EXCLUDED.status,
          last_updated = NOW()
      `, [
        update.unit_id,
        update.battery_soc,
        update.location_lat,
        update.location_lon,
        update.battery_kwh,
        update.dealer_id,
        update.status || 'available',
      ])
    );

    await Promise.all(upsertPromises);

    res.json({
      success: true,
      updated_count: telemetryUpdates.length,
      timestamp: new Date().toISOString(),
    });

  } catch (error) {
    console.error('Telemetry update error:', error);
    res.status(500).json({
      error: 'Failed to update telemetry',
      message: error.message,
    });
  }
});

// GET /api/telemetry/fleet
// Get current fleet status
app.get('/api/telemetry/fleet', async (req, res) => {
  try {
    const { dealer_id, min_soc } = req.query;

    let query = `
      SELECT unit_id, battery_soc, location_lat, location_lon,
             battery_kwh, dealer_id, status, last_updated
      FROM fleet_telemetry
      WHERE last_updated > NOW() - INTERVAL '1 hour'
    `;

    const params = [];
    
    if (dealer_id) {
      params.push(dealer_id);
      query += ` AND dealer_id = $${params.length}`;
    }

    if (min_soc) {
      params.push(parseFloat(min_soc));
      query += ` AND battery_soc >= $${params.length}`;
    }

    query += ' ORDER BY last_updated DESC';

    const result = await db.query(query, params);

    res.json({
      success: true,
      fleet_size: result.rows.length,
      timestamp: new Date().toISOString(),
      fleet: result.rows,
    });

  } catch (error) {
    console.error('Fleet query error:', error);
    res.status(500).json({
      error: 'Failed to query fleet',
      message: error.message,
    });
  }
});

// ===========================================
// API ROUTES - ANALYTICS & REPORTING
// ===========================================

// GET /api/analytics/revenue
// Get revenue analytics for grid services
app.get('/api/analytics/revenue', async (req, res) => {
  try {
    const { start_date, end_date } = req.query;

    const result = await db.query(`
      SELECT
        DATE(event_timestamp) as date,
        COUNT(*) as event_count,
        SUM(actual_capacity_mw) as total_capacity_mw,
        SUM(revenue_usd) as total_revenue_usd,
        AVG(price_multiplier) as avg_price_multiplier
      FROM grid_events
      WHERE event_timestamp >= $1 AND event_timestamp <= $2
      GROUP BY DATE(event_timestamp)
      ORDER BY date DESC
    `, [start_date || '2026-01-01', end_date || '2026-12-31']);

    const totalRevenue = result.rows.reduce((sum, row) => sum + parseFloat(row.total_revenue_usd || 0), 0);

    res.json({
      success: true,
      period: { start_date, end_date },
      total_revenue_usd: totalRevenue.toFixed(2),
      daily_breakdown: result.rows,
    });

  } catch (error) {
    console.error('Analytics query error:', error);
    res.status(500).json({
      error: 'Analytics query failed',
      message: error.message,
    });
  }
});

// ===========================================
// WEBSOCKET REAL-TIME UPDATES
// ===========================================

wss.on('connection', (ws) => {
  console.log('New WebSocket connection established');

  ws.on('message', (message) => {
    try {
      const data = JSON.parse(message);
      console.log('Received WS message:', data);

      // Handle subscription requests, etc.
      if (data.type === 'subscribe') {
        ws.subscribed = data.channel;
      }

    } catch (error) {
      console.error('WebSocket message error:', error);
    }
  });

  ws.on('close', () => {
    console.log('WebSocket connection closed');
  });
});

function broadcastGridUpdate(data) {
  wss.clients.forEach((client) => {
    if (client.readyState === WebSocket.OPEN) {
      client.send(JSON.stringify({
        type: 'grid_update',
        timestamp: new Date().toISOString(),
        data,
      }));
    }
  });
}

// ===========================================
// ERROR HANDLING
// ===========================================

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Route not found',
    path: req.path,
  });
});

// Global error handler
app.use((err, req, res, next) => {
  console.error('Global error:', err);
  res.status(err.status || 500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'production' ? 'An error occurred' : err.message,
  });
});

// ===========================================
// SERVER STARTUP
// ===========================================

async function startServer() {
  try {
    // Initialize database
    await initializeDatabase();

    // Test Redis connection
    await redis.ping();
    console.log('✅ Redis connection established');

    // Start HTTP server
    server.listen(PORT, () => {
      console.log('='.repeat(60));
      console.log('🚀 CDLS Platform API Server');
      console.log('='.repeat(60));
      console.log(`Port: ${PORT}`);
      console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
      console.log(`Database: ${process.env.DB_NAME || 'cdls_platform'}`);
      console.log(`Redis: ${process.env.REDIS_HOST || 'localhost'}:${process.env.REDIS_PORT || 6379}`);
      console.log(`Health Check: http://localhost:${PORT}/health`);
      console.log('='.repeat(60));
    });

  } catch (error) {
    console.error('❌ Server startup failed:', error);
    process.exit(1);
  }
}

// Graceful shutdown
process.on('SIGTERM', async () => {
  console.log('SIGTERM received, shutting down gracefully...');
  
  server.close(() => {
    console.log('HTTP server closed');
  });

  await db.end();
  await redis.quit();
  
  process.exit(0);
});

// Start the server
startServer();

module.exports = { app, db, redis, wss };
