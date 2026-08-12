-- ============================================
-- CDLS ROI CALCULATOR DATABASE SCHEMA
-- ============================================

-- Table 1: Users (your team and dealer contacts)
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  role VARCHAR(50) CHECK (role IN ('admin', 'sales', 'dealer', 'investor')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login TIMESTAMP,
  is_active BOOLEAN DEFAULT true
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Table 2: Dealers
CREATE TABLE dealers (
  id SERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  contact_email VARCHAR(255),
  contact_phone VARCHAR(50),
  location VARCHAR(200),
  fleet_size INTEGER,
  annual_miles INTEGER,
  current_fuel_cost DECIMAL(10,3),
  electricity_rate DECIMAL(10,4),
  operating_days INTEGER DEFAULT 260,
  current_equipment TEXT,
  equity_commitment DECIMAL(12,2),
  status VARCHAR(50) CHECK (status IN ('prospect', 'pilot', 'committed', 'active', 'inactive')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by INTEGER REFERENCES users(id)
);

CREATE INDEX idx_dealers_status ON dealers(status);
CREATE INDEX idx_dealers_location ON dealers(location);

-- Table 3: Calculations (every time someone runs the calculator)
CREATE TABLE calculations (
  id SERIAL PRIMARY KEY,
  dealer_id INTEGER REFERENCES dealers(id),
  user_id INTEGER REFERENCES users(id),
  session_id VARCHAR(100),
  
  -- Input values
  fleet_size INTEGER NOT NULL,
  annual_miles INTEGER NOT NULL,
  diesel_price DECIMAL(10,3),
  electricity_rate DECIMAL(10,4),
  operating_days INTEGER,
  
  -- Calculated results
  diesel_annual_cost DECIMAL(12,2),
  ev_annual_cost DECIMAL(12,2),
  annual_savings DECIMAL(12,2),
  payback_period DECIMAL(10,2),
  five_year_savings DECIMAL(12,2),
  carbon_reduction DECIMAL(10,2),
  
  -- Carbon credits
  lcfs_credits DECIMAL(10,2),
  credit_revenue DECIMAL(12,2),
  
  -- Metadata
  calculation_type VARCHAR(50) CHECK (calculation_type IN ('dealer_fleet', 'investor_roi', 'route_economics')),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address INET,
  user_agent TEXT
);

CREATE INDEX idx_calculations_dealer ON calculations(dealer_id);
CREATE INDEX idx_calculations_created ON calculations(created_at DESC);
CREATE INDEX idx_calculations_session ON calculations(session_id);

-- Table 4: Saved Scenarios (dealers can save multiple "what-if" scenarios)
CREATE TABLE scenarios (
  id SERIAL PRIMARY KEY,
  calculation_id INTEGER REFERENCES calculations(id),
  dealer_id INTEGER REFERENCES dealers(id),
  scenario_name VARCHAR(200),
  scenario_notes TEXT,
  is_favorite BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_scenarios_dealer ON scenarios(dealer_id);

-- Table 5: Carbon Credits (LCFS credit tracking)
CREATE TABLE carbon_credits (
  id SERIAL PRIMARY KEY,
  dealer_id INTEGER REFERENCES dealers(id),
  reporting_period VARCHAR(20), -- e.g., "2025-Q1"
  credits_generated DECIMAL(10,2),
  credits_sold DECIMAL(10,2),
  credits_banked DECIMAL(10,2),
  sale_price_per_credit DECIMAL(10,2),
  total_revenue DECIMAL(12,2),
  carb_submitted BOOLEAN DEFAULT false,
  submitted_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_carbon_dealer_period ON carbon_credits(dealer_id, reporting_period);

-- Table 6: Email Logs (track all automated emails)
CREATE TABLE email_logs (
  id SERIAL PRIMARY KEY,
  dealer_id INTEGER REFERENCES dealers(id),
  calculation_id INTEGER REFERENCES calculations(id),
  recipient_email VARCHAR(255),
  email_type VARCHAR(50) CHECK (email_type IN ('results', 'follow_up', 'reminder', 'report')),
  subject VARCHAR(500),
  sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  opened_at TIMESTAMP,
  clicked_at TIMESTAMP,
  status VARCHAR(50) CHECK (status IN ('sent', 'delivered', 'opened', 'clicked', 'bounced', 'failed'))
);

CREATE INDEX idx_email_dealer ON email_logs(dealer_id);
CREATE INDEX idx_email_status ON email_logs(status);

-- Table 7: Analytics Events (track user behavior)
CREATE TABLE analytics_events (
  id SERIAL PRIMARY KEY,
  dealer_id INTEGER REFERENCES dealers(id),
  user_id INTEGER REFERENCES users(id),
  session_id VARCHAR(100),
  event_type VARCHAR(100), -- e.g., 'calculator_view', 'calculation_run', 'email_clicked'
  event_data JSONB, -- flexible JSON storage for event-specific data
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ip_address INET,
  user_agent TEXT
);

CREATE INDEX idx_analytics_dealer ON analytics_events(dealer_id);
CREATE INDEX idx_analytics_type ON analytics_events(event_type);
CREATE INDEX idx_analytics_created ON analytics_events(created_at DESC);

-- Table 8: Lead Scores (calculated engagement scores)
CREATE TABLE lead_scores (
  id SERIAL PRIMARY KEY,
  dealer_id INTEGER REFERENCES dealers(id) UNIQUE,
  total_calculations INTEGER DEFAULT 0,
  total_scenarios_saved INTEGER DEFAULT 0,
  emails_opened INTEGER DEFAULT 0,
  links_clicked INTEGER DEFAULT 0,
  last_activity TIMESTAMP,
  engagement_score INTEGER, -- 0-100
  lead_grade VARCHAR(10) CHECK (lead_grade IN ('A+', 'A', 'B', 'C', 'D')),
  calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT
);

CREATE INDEX idx_lead_scores_grade ON lead_scores(lead_grade);
CREATE INDEX idx_lead_scores_engagement ON lead_scores(engagement_score DESC);

-- Table 9: Fuel Prices (historical tracking)
CREATE TABLE fuel_prices (
  id SERIAL PRIMARY KEY,
  date DATE NOT NULL,
  location VARCHAR(100),
  diesel_price DECIMAL(10,3),
  electricity_rate DECIMAL(10,4),
  source VARCHAR(100), -- e.g., 'EIA', 'PG&E', 'manual'
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_fuel_date ON fuel_prices(date DESC);
CREATE INDEX idx_fuel_location ON fuel_prices(location);

-- Table 10: CARB Compliance (regulatory tracking)
CREATE TABLE carb_compliance (
  id SERIAL PRIMARY KEY,
  dealer_id INTEGER REFERENCES dealers(id),
  compliance_year INTEGER,
  reporting_quarter VARCHAR(10),
  vehicles_reported INTEGER,
  total_miles DECIMAL(12,2),
  emissions_avoided DECIMAL(10,2),
  compliance_status VARCHAR(50) CHECK (compliance_status IN ('pending', 'submitted', 'approved', 'rejected')),
  submission_date DATE,
  approval_date DATE,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_carb_dealer_year ON carb_compliance(dealer_id, compliance_year);

-- ============================================
-- VIEWS (Pre-calculated queries for performance)
-- ============================================

-- View 1: Dealer Activity Summary
CREATE VIEW dealer_activity_summary AS
SELECT 
  d.id,
  d.name,
  d.status,
  COUNT(DISTINCT c.id) as total_calculations,
  COUNT(DISTINCT s.id) as saved_scenarios,
  MAX(c.created_at) as last_calculation,
  AVG(c.annual_savings) as avg_savings,
  ls.engagement_score,
  ls.lead_grade
FROM dealers d
LEFT JOIN calculations c ON d.id = c.dealer_id
LEFT JOIN scenarios s ON d.id = s.dealer_id
LEFT JOIN lead_scores ls ON d.id = ls.dealer_id
GROUP BY d.id, d.name, d.status, ls.engagement_score, ls.lead_grade;

-- View 2: Monthly Calculation Trends
CREATE VIEW monthly_calculation_trends AS
SELECT 
  DATE_TRUNC('month', created_at) as month,
  COUNT(*) as total_calculations,
  COUNT(DISTINCT dealer_id) as unique_dealers,
  AVG(annual_savings) as avg_savings,
  SUM(carbon_reduction) as total_carbon_avoided
FROM calculations
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month DESC;

-- View 3: Top Performing Dealers (by savings)
CREATE VIEW top_dealers_by_savings AS
SELECT 
  d.id,
  d.name,
  d.location,
  d.status,
  AVG(c.annual_savings) as avg_annual_savings,
  AVG(c.payback_period) as avg_payback,
  COUNT(c.id) as calculation_count
FROM dealers d
JOIN calculations c ON d.id = c.dealer_id
GROUP BY d.id, d.name, d.location, d.status
ORDER BY avg_annual_savings DESC
LIMIT 20;

-- ============================================
-- FUNCTIONS (Automated calculations)
-- ============================================

-- Function 1: Update Lead Score (run nightly)
CREATE OR REPLACE FUNCTION update_lead_scores()
RETURNS void AS $$
BEGIN
  INSERT INTO lead_scores (dealer_id, total_calculations, emails_opened, engagement_score, lead_grade, calculated_at)
  SELECT 
    d.id,
    COUNT(DISTINCT c.id),
    COUNT(DISTINCT e.id) FILTER (WHERE e.opened_at IS NOT NULL),
    LEAST(100, 
      (COUNT(DISTINCT c.id) * 10) + 
      (COUNT(DISTINCT e.id) FILTER (WHERE e.opened_at IS NOT NULL) * 5) +
      (COUNT(DISTINCT s.id) * 15)
    ) as score,
    CASE 
      WHEN score >= 80 THEN 'A+'
      WHEN score >= 60 THEN 'A'
      WHEN score >= 40 THEN 'B'
      WHEN score >= 20 THEN 'C'
      ELSE 'D'
    END as grade,
    NOW()
  FROM dealers d
  LEFT JOIN calculations c ON d.id = c.dealer_id
  LEFT JOIN email_logs e ON d.id = e.dealer_id
  LEFT JOIN scenarios s ON d.id = s.dealer_id
  GROUP BY d.id
  ON CONFLICT (dealer_id) DO UPDATE
  SET 
    total_calculations = EXCLUDED.total_calculations,
    emails_opened = EXCLUDED.emails_opened,
    engagement_score = EXCLUDED.engagement_score,
    lead_grade = EXCLUDED.lead_grade,
    calculated_at = EXCLUDED.calculated_at;
END;
$$ LANGUAGE plpgsql;

-- Function 2: Calculate Carbon Credits (quarterly)
CREATE OR REPLACE FUNCTION calculate_quarterly_credits(p_dealer_id INTEGER, p_quarter VARCHAR)
RETURNS DECIMAL AS $$
DECLARE
  total_credits DECIMAL;
BEGIN
  SELECT SUM(carbon_reduction * 0.89) INTO total_credits
  FROM calculations
  WHERE dealer_id = p_dealer_id
    AND TO_CHAR(created_at, 'YYYY-"Q"Q') = p_quarter;
  
  RETURN COALESCE(total_credits, 0);
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- SAMPLE DATA (for testing)
-- ============================================

-- Insert sample dealers
INSERT INTO dealers (name, contact_email, location, fleet_size, annual_miles, electricity_rate, equity_commitment, status) VALUES
('San Diego Auto Transport', 'contact@sdautotransport.com', 'San Diego', 8, 22000, 0.19, 50000, 'committed'),
('NorCal Logistics', 'info@norcallogistics.com', 'Sacramento', 12, 28000, 0.17, 75000, 'pilot'),
('Central Valley Hauling', 'admin@cvhauling.com', 'Fresno', 6, 18000, 0.15, 40000, 'committed'),
('Bay Area Transport', 'operations@bayareatransport.com', 'Oakland', 15, 32000, 0.21, 100000, 'active'),
('SoCal Express', 'manager@socalexpress.com', 'Los Angeles', 10, 25000, 0.20, 65000, 'pilot');

-- Insert sample fuel prices
INSERT INTO fuel_prices (date, location, diesel_price, electricity_rate, source) VALUES
('2025-12-26', 'California', 4.862, 0.18, 'EIA'),
('2025-12-25', 'California', 4.855, 0.18, 'EIA'),
('2025-12-24', 'California', 4.870, 0.18, 'EIA');

-- ============================================
-- MAINTENANCE TASKS
-- ============================================

-- Daily: Update lead scores
-- Schedule this to run at 2 AM daily
-- SELECT update_lead_scores();

-- Weekly: Archive old calculations (older than 2 years)
-- CREATE TABLE calculations_archive (LIKE calculations INCLUDING ALL);
-- INSERT INTO calculations_archive SELECT * FROM calculations WHERE created_at < NOW() - INTERVAL '2 years';
-- DELETE FROM calculations WHERE created_at < NOW() - INTERVAL '2 years';

-- Monthly: Generate carbon credit reports
-- (Run on 1st of each month)

-- ============================================
-- BACKUP STRATEGY
-- ============================================

-- Full backup daily at 1 AM:
-- pg_dump -U postgres -d cdls_calculator > backup_$(date +%Y%m%d).sql

-- Point-in-time recovery enabled:
-- wal_level = replica
-- archive_mode = on
-- archive_command = 'test ! -f /var/lib/postgresql/archive/%f && cp %p /var/lib/postgresql/archive/%f'