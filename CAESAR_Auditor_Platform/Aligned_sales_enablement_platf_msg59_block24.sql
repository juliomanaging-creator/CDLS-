-- Core tables

CREATE TABLE vehicles (
  id SERIAL PRIMARY KEY,
  vin VARCHAR(17) UNIQUE NOT NULL,
  dealer_id INTEGER REFERENCES dealers(id),
  make VARCHAR(50),
  model VARCHAR(50),
  year INTEGER,
  battery_kwh DECIMAL(10,2),
  purchase_date DATE,
  purchase_price DECIMAL(12,2),
  status VARCHAR(50) -- active, maintenance, retired
);

CREATE TABLE telematics_data (
  id BIGSERIAL PRIMARY KEY,
  vehicle_id INTEGER REFERENCES vehicles(id),
  timestamp TIMESTAMP NOT NULL,
  location POINT, -- PostgreSQL geographic type
  odometer_miles DECIMAL(10,2),
  battery_soc DECIMAL(5,2),
  speed_mph DECIMAL(5,2),
  charging_status VARCHAR(20)
);
CREATE INDEX idx_telematics_vehicle_time ON telematics_data(vehicle_id, timestamp DESC);

CREATE TABLE charging_sessions (
  id SERIAL PRIMARY KEY,
  vehicle_id INTEGER REFERENCES vehicles(id),
  charger_id VARCHAR(50),
  start_time TIMESTAMP,
  end_time TIMESTAMP,
  kwh_consumed DECIMAL(10,2),
  cost_usd DECIMAL(10,2),
  utility_rate DECIMAL(10,4)
);

CREATE TABLE hauls (
  id SERIAL PRIMARY KEY,
  vehicle_id INTEGER REFERENCES vehicles(id),
  dealer_id INTEGER REFERENCES dealers(id),
  haul_date DATE,
  origin VARCHAR(200),
  destination VARCHAR(200),
  distance_miles DECIMAL(10,2),
  vehicles_hauled INTEGER,
  revenue_usd DECIMAL(10,2),
  electricity_cost_usd DECIMAL(10,2),
  gross_margin_usd DECIMAL(10,2)
);

CREATE TABLE maintenance_records (
  id SERIAL PRIMARY KEY,
  vehicle_id INTEGER REFERENCES vehicles(id),
  service_date DATE,
  odometer_miles DECIMAL(10,2),
  service_type VARCHAR(100),
  total_cost_usd DECIMAL(10,2),
  downtime_hours DECIMAL(5,2)
);

CREATE TABLE carbon_credits (
  id SERIAL PRIMARY KEY,
  quarter VARCHAR(10), -- e.g., "2026-Q1"
  dealer_id INTEGER REFERENCES dealers(id),
  credits_generated DECIMAL(10,2),
  credits_sold DECIMAL(10,2),
  credits_banked DECIMAL(10,2),
  average_sale_price DECIMAL(10,2),
  revenue_usd DECIMAL(12,2)
);