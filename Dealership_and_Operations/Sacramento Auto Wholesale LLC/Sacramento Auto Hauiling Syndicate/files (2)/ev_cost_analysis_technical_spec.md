# EV Charging Cost Analysis System
## Technical Specification Document

**Project:** California Dealer Logistics Syndicate - Fleet Cost Optimization Software  
**Version:** 1.0  
**Date:** December 2025  
**Owner:** Julio - Wholesale Dealership Operations

---

## EXECUTIVE SUMMARY

### Business Problem
Wholesale automotive dealers and car hauling operations need accurate, real-time cost comparisons between diesel and electric vehicle operations across multiple California markets to make informed fleet transition decisions. Existing solutions fail to address:

1. **Route-specific cost modeling** for multi-stop dealer logistics
2. **Time-of-use rate optimization** for commercial charging
3. **Real-time integration** with both fuel and electricity pricing APIs
4. **Multi-city comparative analysis** for syndicate-wide operations
5. **Total Cost of Ownership (TCO)** including maintenance differentials

### Solution Overview
A proprietary software platform that integrates real-time pricing data for diesel fuel and EV charging across California markets, calculates route-specific operating costs, and provides decision-support analytics for fleet composition optimization.

---

## UNIQUE VALUE PROPOSITIONS

### Problems This Software Solves That Competitors Don't

#### 1. **Multi-Stop Route Cost Modeling**
**Industry Gap:** Existing solutions (ChargePoint, Geotab, Fleet Complete) calculate single-trip costs but don't optimize for wholesale dealer pickup/delivery routes with 5-8 stops per run.

**Our Solution:** 
- Route-aware cost modeling that factors charging opportunities at dealer locations
- Calculates optimal charging strategy (fast charge vs. Level 2 at overnight stops)
- Models "opportunity charging" during vehicle loading/unloading times
- Accounts for backhaul efficiency and deadhead mileage

**Technical Differentiation:** Graph-based routing algorithm with embedded charging station nodes and time-of-use rate awareness.

#### 2. **Dealer Network Charging Infrastructure Mapping**
**Industry Gap:** Generic charging station locators don't identify which locations have existing dealer relationships or private charging access.

**Our Solution:**
- Maintains database of syndicate member locations with charging capabilities
- Maps private charging agreements and volume discount rates
- Identifies "charging desert" routes requiring strategic infrastructure investment
- Calculates ROI for installing charging at high-frequency dealer locations

**Technical Differentiation:** Proprietary dealer network database integrated with public charging APIs, creating hybrid charging availability matrix.

#### 3. **Commercial Time-of-Use Rate Optimization**
**Industry Gap:** Consumer-focused tools use residential electricity rates; commercial rates are complex with demand charges, time-of-use tiers, and utility-specific tariffs.

**Our Solution:**
- Integrates actual commercial rate schedules from PG&E, SCE, SDG&E
- Models demand charge impacts based on charging behavior
- Recommends optimal charging windows to minimize costs
- Calculates cost differences between Level 2 (overnight) vs. DC fast charging

**Technical Differentiation:** Rate engine with tariff database for CA commercial electricity, including demand charge modeling and seasonal rate variations.

#### 4. **Diesel Price Volatility Hedging Analysis**
**Industry Gap:** Simple cost calculators use static fuel prices; wholesale operations need volatility-aware planning.

**Our Solution:**
- Historical diesel price volatility analysis by market
- Monte Carlo simulation for future cost scenarios
- Calculates "cost certainty premium" of electricity vs. diesel
- Models impact of diesel hedging contracts vs. EV conversion

**Technical Differentiation:** Financial modeling layer with stochastic price forecasting and risk-adjusted TCO calculations.

#### 5. **Payload-Adjusted Range Modeling**
**Industry Gap:** Generic EV range calculators don't account for car hauler load variations (empty vs. fully loaded with 7-10 vehicles).

**Our Solution:**
- Vehicle-specific range degradation models based on payload
- Calculates usable range for loaded outbound vs. empty return trips
- Models seasonal range variations (temperature impacts)
- Identifies routes where payload makes EVs non-viable

**Technical Differentiation:** Physics-based range model incorporating vehicle weight, aerodynamics, and terrain data from mapping APIs.

#### 6. **Maintenance Cost Differential Tracking**
**Industry Gap:** Fleet management systems track maintenance but don't model proactive EV vs. diesel cost differences.

**Our Solution:**
- Predictive maintenance cost modeling (brake replacement, oil changes eliminated)
- Tracks actual maintenance events across mixed fleet
- Calculates realized savings vs. projected
- Models warranty coverage differences and battery degradation

**Technical Differentiation:** Maintenance cost database specific to car hauler operations with predictive analytics.

#### 7. **Incentive and Rebate Maximization**
**Industry Gap:** Manual tracking of complex, time-limited incentive programs leads to missed opportunities.

**Our Solution:**
- Real-time database of federal, state, and utility EV incentives
- Automatic eligibility calculations based on fleet composition
- Alert system for expiring programs and application deadlines
- Models optimal timing for fleet conversion to maximize incentives

**Technical Differentiation:** Incentive intelligence layer with automated eligibility matching and application deadline tracking.

#### 8. **Syndicate-Wide Cost Aggregation**
**Industry Gap:** Each dealer operates independently; no visibility into collective bargaining power.

**Our Solution:**
- Aggregates energy consumption across syndicate members
- Models volume discount opportunities for electricity supply
- Identifies shared infrastructure investment opportunities
- Calculates economies of scale for maintenance and parts

**Technical Differentiation:** Multi-tenant architecture with privacy-preserved aggregation for collective analytics.

---

## SYSTEM ARCHITECTURE

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Web App    │  │ Mobile App   │  │  Admin Portal   │   │
│  │  (Dealers)   │  │ (Drivers)    │  │  (Management)   │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Cost Comparison Engine                    │   │
│  │  • Route cost calculator                             │   │
│  │  • Time-of-use optimizer                            │   │
│  │  • TCO modeling                                      │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Analytics & Reporting                     │   │
│  │  • Dashboard generation                              │   │
│  │  • Scenario modeling                                 │   │
│  │  • Trend analysis                                    │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  PostgreSQL  │  │    Redis     │  │   TimescaleDB   │   │
│  │  (Core DB)   │  │   (Cache)    │  │  (Time Series)  │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  EXTERNAL INTEGRATIONS                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │   Fuel APIs  │  │ Charging APIs│  │  Utility APIs   │   │
│  │  (GasBuddy)  │  │(ChargePoint) │  │  (PG&E, SCE)    │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  Mapping API │  │ Weather API  │  │  Incentive DB   │   │
│  │  (Google)    │  │(OpenWeather) │  │   (Custom)      │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Frontend:**
- React 18+ with TypeScript
- Material-UI component library
- Recharts for data visualization
- Mapbox GL JS for mapping interface

**Backend:**
- Node.js with Express.js
- Python 3.11+ for analytics engine
- FastAPI for ML model serving

**Database:**
- PostgreSQL 15+ (primary data store)
- Redis (caching and session management)
- TimescaleDB (time-series pricing data)

**Infrastructure:**
- Docker containerization
- AWS deployment (EC2, RDS, ElastiCache)
- CloudFlare CDN
- GitHub Actions CI/CD

---

## DATA STRUCTURES

### Core Database Schema

#### 1. Cities Table
```sql
CREATE TABLE cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state_code CHAR(2) NOT NULL DEFAULT 'CA',
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    utility_provider VARCHAR(100),
    utility_territory_id VARCHAR(50),
    average_commercial_rate DECIMAL(8, 4), -- $/kWh
    demand_charge_applicable BOOLEAN DEFAULT TRUE,
    timezone VARCHAR(50) DEFAULT 'America/Los_Angeles',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cities_location ON cities USING GIST(
    ll_to_earth(latitude, longitude)
);
```

#### 2. Fuel Prices Table (Time Series)
```sql
CREATE TABLE fuel_prices (
    price_id BIGSERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(city_id),
    fuel_type VARCHAR(20) NOT NULL, -- 'diesel', 'unleaded', 'premium'
    price_per_gallon DECIMAL(6, 3) NOT NULL,
    station_count INTEGER, -- number of stations in average
    price_date TIMESTAMP NOT NULL,
    data_source VARCHAR(50), -- 'gasbuddy_api', 'eia_gov', 'manual'
    confidence_score DECIMAL(3, 2) -- 0.00 to 1.00
);

CREATE INDEX idx_fuel_prices_lookup ON fuel_prices(city_id, fuel_type, price_date DESC);

-- Hypertable for time-series optimization
SELECT create_hypertable('fuel_prices', 'price_date');
```

#### 3. EV Charging Rates Table
```sql
CREATE TABLE ev_charging_rates (
    rate_id BIGSERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(city_id),
    charging_network VARCHAR(50), -- 'ChargePoint', 'EVgo', 'Electrify America', 'Private'
    charging_speed VARCHAR(20), -- 'Level2', 'DC_Fast_50kW', 'DC_Fast_150kW', 'DC_Fast_350kW'
    rate_structure VARCHAR(20), -- 'per_kwh', 'per_minute', 'hybrid'
    base_rate DECIMAL(6, 3), -- $/kWh or $/minute
    session_fee DECIMAL(5, 2), -- flat fee per session
    idle_fee DECIMAL(5, 2), -- $/minute after charging complete
    time_of_use_applicable BOOLEAN DEFAULT FALSE,
    effective_date TIMESTAMP NOT NULL,
    expiration_date TIMESTAMP,
    data_source VARCHAR(50),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ev_rates_lookup ON ev_charging_rates(city_id, charging_network, effective_date DESC);
```

#### 4. Time-of-Use Rate Schedules
```sql
CREATE TABLE tou_rate_schedules (
    schedule_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(city_id),
    utility_provider VARCHAR(100) NOT NULL,
    rate_plan_name VARCHAR(100), -- 'B20', 'EV2-A', etc.
    customer_type VARCHAR(20), -- 'commercial', 'industrial'
    season VARCHAR(20), -- 'summer', 'winter'
    period_type VARCHAR(20), -- 'peak', 'partial_peak', 'off_peak'
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    days_of_week INTEGER[], -- Array: 0=Sunday, 6=Saturday
    energy_rate DECIMAL(6, 4), -- $/kWh
    demand_charge DECIMAL(6, 2), -- $/kW
    effective_date DATE NOT NULL,
    expiration_date DATE
);

CREATE INDEX idx_tou_schedules ON tou_rate_schedules(city_id, utility_provider, season);
```

#### 5. Charging Stations Table
```sql
CREATE TABLE charging_stations (
    station_id SERIAL PRIMARY KEY,
    city_id INTEGER REFERENCES cities(city_id),
    station_name VARCHAR(200),
    network VARCHAR(50),
    address TEXT,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    access_type VARCHAR(20), -- 'public', 'private', 'dealer_network'
    dealer_id INTEGER REFERENCES dealers(dealer_id), -- if private
    num_ports INTEGER,
    charging_speeds TEXT[], -- Array of available speeds
    amenities TEXT[], -- ['restroom', 'wifi', 'food']
    operational_hours JSONB, -- {"monday": "00:00-24:00", ...}
    reliability_score DECIMAL(3, 2), -- 0.00 to 1.00
    last_verified TIMESTAMP
);

CREATE INDEX idx_stations_location ON charging_stations USING GIST(
    ll_to_earth(latitude, longitude)
);
```

#### 6. Dealers Table (Syndicate Members)
```sql
CREATE TABLE dealers (
    dealer_id SERIAL PRIMARY KEY,
    dealer_name VARCHAR(200) NOT NULL,
    city_id INTEGER REFERENCES cities(city_id),
    address TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    syndicate_member BOOLEAN DEFAULT FALSE,
    has_charging BOOLEAN DEFAULT FALSE,
    charging_capacity_kw INTEGER, -- total installed capacity
    charging_available_to_network BOOLEAN DEFAULT FALSE,
    preferred_charging_window TIME[], -- [start_time, end_time]
    volume_discount_rate DECIMAL(6, 4), -- negotiated $/kWh if applicable
    contact_name VARCHAR(100),
    contact_phone VARCHAR(20),
    contact_email VARCHAR(100),
    joined_date DATE,
    active BOOLEAN DEFAULT TRUE
);
```

#### 7. Routes Table
```sql
CREATE TABLE routes (
    route_id SERIAL PRIMARY KEY,
    route_name VARCHAR(100),
    origin_dealer_id INTEGER REFERENCES dealers(dealer_id),
    destination_dealer_id INTEGER REFERENCES dealers(dealer_id),
    waypoints JSONB, -- Array of {dealer_id, sequence, estimated_minutes}
    total_distance_miles DECIMAL(6, 2),
    estimated_duration_minutes INTEGER,
    typical_payload_vehicles INTEGER, -- number of cars hauled
    frequency VARCHAR(20), -- 'daily', 'weekly', 'on_demand'
    last_run_date TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);
```

#### 8. Cost Calculations Table (Cache/History)
```sql
CREATE TABLE cost_calculations (
    calc_id BIGSERIAL PRIMARY KEY,
    route_id INTEGER REFERENCES routes(route_id),
    calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    vehicle_type VARCHAR(50), -- 'diesel_hauler', 'ev_hauler_model_x'
    fuel_type VARCHAR(20), -- 'diesel', 'electric'
    
    -- Diesel costs
    diesel_price_per_gallon DECIMAL(6, 3),
    fuel_efficiency_mpg DECIMAL(5, 2),
    diesel_total_cost DECIMAL(8, 2),
    
    -- EV costs
    ev_kwh_per_mile DECIMAL(4, 2),
    charging_cost_per_kwh DECIMAL(6, 4),
    charging_session_fees DECIMAL(6, 2),
    ev_total_cost DECIMAL(8, 2),
    
    -- Comparison metrics
    cost_difference DECIMAL(8, 2),
    cost_difference_pct DECIMAL(5, 2),
    
    -- Metadata
    calculation_parameters JSONB, -- store all input assumptions
    user_id INTEGER,
    
    PRIMARY KEY (calc_id)
);

CREATE INDEX idx_cost_calcs_route ON cost_calculations(route_id, calculation_date DESC);
```

#### 9. Vehicle Specifications Table
```sql
CREATE TABLE vehicle_specs (
    vehicle_id SERIAL PRIMARY KEY,
    manufacturer VARCHAR(50),
    model VARCHAR(100),
    year INTEGER,
    vehicle_type VARCHAR(50), -- 'diesel_car_hauler', 'ev_car_hauler', 'diesel_pickup'
    fuel_type VARCHAR(20),
    
    -- Diesel specs
    tank_capacity_gallons DECIMAL(5, 2),
    city_mpg DECIMAL(5, 2),
    highway_mpg DECIMAL(5, 2),
    
    -- EV specs
    battery_capacity_kwh DECIMAL(6, 2),
    epa_range_miles INTEGER,
    kwh_per_mile_unloaded DECIMAL(4, 2),
    kwh_per_mile_loaded DECIMAL(4, 2),
    max_charging_speed_kw INTEGER,
    
    -- Common specs
    payload_capacity_lbs INTEGER,
    vehicle_weight_lbs INTEGER,
    msrp DECIMAL(10, 2),
    
    -- Maintenance
    avg_maintenance_per_mile DECIMAL(5, 3),
    warranty_details JSONB
);
```

#### 10. Incentives Table
```sql
CREATE TABLE incentives (
    incentive_id SERIAL PRIMARY KEY,
    incentive_name VARCHAR(200) NOT NULL,
    incentive_type VARCHAR(50), -- 'federal_tax_credit', 'state_rebate', 'utility_rebate', 'grant'
    jurisdiction VARCHAR(100), -- 'federal', 'california', 'pge_territory'
    eligible_vehicle_types TEXT[],
    amount DECIMAL(10, 2),
    amount_type VARCHAR(20), -- 'fixed', 'per_vehicle', 'percentage'
    max_amount DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    application_deadline DATE,
    eligibility_criteria JSONB,
    application_url TEXT,
    active BOOLEAN DEFAULT TRUE,
    notes TEXT
);
```

---

## WORKFLOW SPECIFICATIONS

### Workflow 1: Real-Time Cost Comparison Query

**User Story:** Dealer wants to compare diesel vs. EV costs for today's route from Sacramento to Modesto with 3 dealer stops.

**Workflow Steps:**

1. **Input Collection**
   - User selects route (or enters origin/destination)
   - System auto-populates waypoints from dealer database
   - User confirms payload (number of vehicles hauling)
   - User selects comparison vehicles (e.g., "Ford F-550 Diesel" vs. "BrightDrop Zevo 600")

2. **Data Retrieval**
   ```
   Parallel API calls:
   ├── Fetch latest diesel prices for cities on route
   ├── Fetch EV charging rates for stations near route
   ├── Fetch time-of-use schedules for charging windows
   ├── Retrieve vehicle specifications
   └── Query weather data (temperature affects EV range)
   ```

3. **Route Analysis**
   ```
   For each vehicle type:
   ├── Calculate total distance (Google Maps API)
   ├── Identify elevation changes (impacts efficiency)
   ├── Determine optimal fuel/charging stops
   └── Calculate payload-adjusted consumption
   ```

4. **Cost Calculation - Diesel**
   ```
   diesel_cost = (total_miles / mpg_with_payload) * avg_diesel_price
   + def_fluid_cost (if applicable)
   + estimated_maintenance_per_mile * total_miles
   ```

5. **Cost Calculation - EV**
   ```
   For each charging segment:
   ├── Determine charging type needed (Level 2 vs DC Fast)
   ├── Calculate kWh needed
   ├── Apply time-of-use rate (if charging at dealer overnight)
   ├── Add session fees
   └── Add demand charges (if applicable)
   
   ev_cost = sum(segment_costs) 
           + estimated_maintenance_per_mile * total_miles
   ```

6. **Comparative Analysis**
   ```
   Calculate:
   ├── Absolute cost difference
   ├── Cost per mile
   ├── Cost per vehicle hauled
   ├── Annual projected savings (if daily route)
   └── Payback period calculation
   ```

7. **Results Presentation**
   - Side-by-side cost breakdown
   - Interactive map showing fuel/charge stops
   - Sensitivity analysis (what if diesel prices change by ±20%?)
   - Recommendation based on route characteristics

**API Endpoints:**

```javascript
POST /api/v1/cost-comparison/calculate
Request body:
{
  "route_id": 123,
  "origin": {"lat": 38.5816, "lng": -121.4944}, // Sacramento
  "destination": {"lat": 37.6391, "lng": -120.9969}, // Modesto
  "waypoints": [
    {"dealer_id": 45, "lat": 38.4404, "lng": -121.3708}, // Elk Grove dealer
    {"dealer_id": 78, "lat": 38.0022, "lng": -121.2958}  // Stockton dealer
  ],
  "payload_vehicles": 7,
  "diesel_vehicle_id": 5,
  "ev_vehicle_id": 12,
  "departure_time": "2025-01-15T08:00:00-08:00",
  "return_same_day": true
}

Response:
{
  "calculation_id": "abc123",
  "route_summary": {
    "total_distance_miles": 127.4,
    "estimated_duration_minutes": 165,
    "number_of_stops": 3
  },
  "diesel_analysis": {
    "vehicle": "Ford F-550 Super Duty",
    "fuel_needed_gallons": 15.8,
    "avg_fuel_price": 4.89,
    "fuel_cost": 77.26,
    "maintenance_cost": 6.37,
    "total_cost": 83.63,
    "cost_per_mile": 0.656,
    "cost_per_vehicle_hauled": 11.95
  },
  "ev_analysis": {
    "vehicle": "BrightDrop Zevo 600",
    "energy_needed_kwh": 198.5,
    "charging_sessions": [
      {
        "location": "Elk Grove Dealer - Private Level 2",
        "kwh": 45.0,
        "cost": 6.75,
        "duration_minutes": 90,
        "rate_type": "dealer_volume_rate"
      },
      {
        "location": "Electrify America - Stockton",
        "kwh": 85.0,
        "cost": 42.50,
        "duration_minutes": 28,
        "rate_type": "dc_fast_public"
      }
    ],
    "total_charging_cost": 49.25,
    "session_fees": 2.00,
    "maintenance_cost": 2.55,
    "total_cost": 53.80,
    "cost_per_mile": 0.422,
    "cost_per_vehicle_hauled": 7.69
  },
  "comparison": {
    "ev_savings": 29.83,
    "ev_savings_pct": 35.7,
    "annual_savings_projection": 7,748.00, // if daily route
    "break_even_analysis": {
      "vehicle_price_premium": 95000,
      "annual_fuel_savings": 7748,
      "annual_maintenance_savings": 989,
      "payback_years": 10.9,
      "incentives_available": 45000,
      "payback_years_after_incentives": 5.7
    }
  },
  "recommendations": [
    "EV is economically viable for this route",
    "Private charging at Elk Grove dealer significantly reduces costs",
    "Consider installing DC fast charging at Stockton location to eliminate public charging stops",
    "Route is within EV range even when fully loaded"
  ],
  "risk_factors": [
    "Limited charging infrastructure between Stockton and Modesto",
    "Winter temperature could reduce range by 15-20%",
    "Public DC fast charging costs are 3x higher than dealer private charging"
  ]
}
```

### Workflow 2: Syndicate-Wide Cost Aggregation

**User Story:** Management wants to see total energy costs across all syndicate members for the past quarter.

**Workflow Steps:**

1. **Authentication & Authorization**
   - Verify user has admin/management role
   - Load dealer permissions (which dealers can user see)

2. **Time Period Selection**
   - User selects date range (Q4 2024)
   - System queries all routes operated during period

3. **Data Aggregation**
   ```sql
   SELECT 
     d.dealer_name,
     COUNT(DISTINCT cc.route_id) as routes_operated,
     SUM(CASE WHEN cc.fuel_type = 'diesel' THEN cc.diesel_total_cost ELSE 0 END) as diesel_costs,
     SUM(CASE WHEN cc.fuel_type = 'electric' THEN cc.ev_total_cost ELSE 0 END) as ev_costs,
     SUM(cc.diesel_total_cost + cc.ev_total_cost) as total_energy_costs
   FROM cost_calculations cc
   JOIN routes r ON cc.route_id = r.route_id
   JOIN dealers d ON r.origin_dealer_id = d.dealer_id
   WHERE d.syndicate_member = TRUE
     AND cc.calculation_date BETWEEN '2024-10-01' AND '2024-12-31'
   GROUP BY d.dealer_id, d.dealer_name
   ORDER BY total_energy_costs DESC;
   ```

4. **Visualization Generation**
   - Create dashboard with:
     - Total syndicate energy spend
     - Diesel vs. EV cost breakdown
     - Cost per mile trends over quarter
     - Top 10 most expensive routes
     - Dealer-level comparison (respecting privacy settings)

5. **Opportunity Analysis**
   - Identify routes where EV would save >30%
   - Calculate collective volume discount opportunities
   - Recommend shared charging infrastructure investments

### Workflow 3: Incentive Eligibility Check

**User Story:** Dealer purchasing 3 EV haulers wants to know all available incentives.

**Workflow Steps:**

1. **Vehicle & Business Info Collection**
   - Vehicle specifications (manufacturer, model, GVWR)
   - Purchase timing
   - Business structure (LLC, S-Corp)
   - Current fleet composition

2. **Eligibility Matching**
   ```sql
   SELECT *
   FROM incentives
   WHERE active = TRUE
     AND current_date BETWEEN start_date AND COALESCE(end_date, '2099-12-31')
     AND 'commercial_hauler' = ANY(eligible_vehicle_types)
     AND (jurisdiction = 'federal' OR jurisdiction = 'california')
   ORDER BY amount DESC;
   ```

3. **Stacking Analysis**
   - Determine which incentives can be combined
   - Calculate maximum total incentive value
   - Identify application deadlines

4. **Application Guidance**
   - Generate checklist of required documents
   - Provide application URLs and instructions
   - Set reminder alerts for deadlines

---

## USER INTERFACE SPECIFICATIONS

### UI Component 1: Cost Comparison Dashboard

**Layout:**
```
┌─────────────────────────────────────────────────────────────────┐
│  California Dealer Logistics - Fleet Cost Analyzer        [≡]   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Route: Sacramento → Elk Grove → Stockton → Modesto            │
│  Distance: 127.4 mi  |  Payload: 7 vehicles  |  Today's Date   │
│                                                                  │
│  ┌────────────────────────┐  ┌────────────────────────┐        │
│  │   DIESEL HAULER        │  │   ELECTRIC HAULER      │        │
│  │   Ford F-550           │  │   BrightDrop Zevo 600  │        │
│  │                        │  │                        │        │
│  │   $83.63               │  │   $53.80               │        │
│  │   Total Route Cost     │  │   Total Route Cost     │        │
│  │                        │  │                        │        │
│  │   $0.66 per mile       │  │   $0.42 per mile       │        │
│  │   $11.95 per vehicle   │  │   $7.69 per vehicle    │        │
│  │                        │  │                        │        │
│  │  ⛽ Fuel: $77.26       │  │  ⚡ Charging: $49.25   │        │
│  │  🔧 Maint: $6.37       │  │  🔧 Maint: $2.55       │        │
│  │                        │  │  💳 Fees: $2.00        │        │
│  └────────────────────────┘  └────────────────────────┘        │
│                                                                  │
│  💰 EV SAVES: $29.83 (35.7%) on this route                      │
│  📊 Annual projection: $7,748 savings (if daily route)          │
│                                                                  │
│  [View Detailed Breakdown]  [Adjust Parameters]  [Save Report]  │
│                                                                  │
│  ───────────────────────────────────────────────────────────    │
│                                                                  │
│  📍 Route Map with Fuel/Charging Stops:                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                                                           │  │
│  │         [Interactive map showing route with markers]     │  │
│  │         - Diesel stations in orange                      │  │
│  │         - EV charging stations in green                  │  │
│  │         - Dealer locations in blue                       │  │
│  │                                                           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ⚠️ Considerations:                                              │
│  • Limited DC fast charging between Stockton and Modesto        │
│  • Winter temps may reduce EV range 15-20%                      │
│  • Private charging at Elk Grove saves $18 vs. public           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Interactive Elements:**

- **Route Modification:** Click map to add/remove waypoints
- **Vehicle Selection:** Dropdown to compare different hauler models
- **Payload Slider:** Adjust number of vehicles hauled (0-10)
- **Date/Time Picker:** See how time-of-use rates affect costs
- **Sensitivity Controls:** "What if diesel prices increase 20%?"

### UI Component 2: City Price Comparison Table

**Spreadsheet-Style View:**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ California City Energy Price Comparison - December 2025                      │
├──────────┬─────────┬──────────────┬──────────────┬─────────────┬─────────────┤
│ City     │ County  │ Diesel Price │ Level 2 EV   │ DC Fast EV  │ Advantage   │
│          │         │ ($/gallon)   │ ($/kWh)      │ ($/kWh)     │             │
├──────────┼─────────┼──────────────┼──────────────┼─────────────┼─────────────┤
│Sacramento│Sacramento│   $4.89      │   $0.15      │   $0.52     │ EV 48% ✓    │
│Stockton  │San Joaquin│  $4.76      │   $0.16      │   $0.49     │ EV 45% ✓    │
│Modesto   │Stanislaus│  $4.68      │   $0.17      │   $0.51     │ EV 43% ✓    │
│Fresno    │Fresno    │   $4.72      │   $0.18      │   $0.48     │ EV 44% ✓    │
│Bakersfield│Kern     │   $4.81      │   $0.16      │   $0.47     │ EV 46% ✓    │
│Los Angeles│Los Angeles│ $5.23      │   $0.20      │   $0.56     │ EV 42% ✓    │
│San Diego │San Diego │   $5.35      │   $0.22      │   $0.58     │ EV 40% ✓    │
│San Jose  │Santa Clara│  $5.41      │   $0.19      │   $0.54     │ EV 43% ✓    │
│Oakland   │Alameda   │   $5.29      │   $0.21      │   $0.57     │ EV 41% ✓    │
│Riverside │Riverside │   $4.94      │   $0.17      │   $0.50     │ EV 46% ✓    │
└──────────┴─────────┴──────────────┴──────────────┴─────────────┴─────────────┘

📊 Statewide Averages:
   Diesel: $5.01/gal  |  Level 2 EV: $0.18/kWh  |  DC Fast: $0.52/kWh
   
🔄 Last Updated: 2 hours ago
📥 [Export to Excel]  [Share Report]  [Set Price Alerts]
```

**Features:**
- Sortable columns (click header to sort)
- Color coding (green = lowest prices, red = highest)
- Export to Excel/CSV
- Historical price charts (click city name)
- Email alerts when prices change significantly

### UI Component 3: Route Builder Interface

**Drag-and-Drop Route Planning:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Build Your Route                                          [Save]│
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Origin:  [Sacramento Wholesale Auto ▼]                         │
│           123 Auto Row, Sacramento CA                           │
│           📍 38.5816, -121.4944                                 │
│                                                                  │
│  ────── Add Stop ──────                                          │
│  🚛 Pickup: [Select Dealer Location ▼]                          │
│     Estimated load time: [30] minutes                           │
│     Vehicles to load: [3]                                       │
│                                                                  │
│  ────── Add Stop ──────                                          │
│  🚛 Pickup: Stockton Auto Exchange                              │
│     Estimated load time: 45 minutes                             │
│     Vehicles to load: 4                                         │
│     [Remove Stop]                                               │
│                                                                  │
│  ────── Add Stop ──────                                          │
│                                                                  │
│  Destination: [Modesto Car Auction ▼]                           │
│                1000 Auction Blvd, Modesto CA                    │
│                                                                  │
│  ═════════════════════════════════════════════════════════      │
│                                                                  │
│  Route Summary:                                                 │
│  • Total Distance: 127.4 miles                                  │
│  • Estimated Duration: 2h 45m (includes loading)                │
│  • Total Vehicles Hauled: 7                                     │
│  • Payload Weight: ~21,000 lbs                                  │
│                                                                  │
│  Charging Opportunities on Route:                               │
│  ⚡ Elk Grove Dealer (Private L2) - During 30min load           │
│  ⚡ Electrify America Stockton (DC Fast) - 15min detour         │
│  ⚡ ChargePoint Modesto (DC Fast) - At destination              │
│                                                                  │
│  [Calculate Costs]  [Optimize Route]  [Save as Template]        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### UI Component 4: Syndicate Dashboard (Admin View)

**Executive Overview:**

```
┌─────────────────────────────────────────────────────────────────┐
│  California Dealer Logistics Syndicate - Q4 2024 Performance    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  💰 Total Energy Costs:  $487,392                               │
│      Diesel: $421,244 (86.4%)  |  Electric: $66,148 (13.6%)    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Cost Trend (Oct - Dec 2024)                            │   │
│  │                                                          │   │
│  │  $180k ┤     ████                                        │   │
│  │        │     ████    ████                                │   │
│  │  $150k ┤ ████████████████    ████                        │   │
│  │        │ ████████████████████████                        │   │
│  │  $120k ┤ ████████████████████████████                    │   │
│  │        └──────────────────────────────                   │   │
│  │         Oct      Nov      Dec                            │   │
│  │         ■ Diesel   ■ Electric                            │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  📊 Fleet Composition:  34 Diesel  |  6 Electric                │
│  🔄 Routes Operated:    2,341 routes  |  298,467 miles          │
│  ⚡ Charging Sessions:  1,847 sessions  |  126,834 kWh          │
│                                                                  │
│  Top Opportunities for Cost Reduction:                          │
│  1. Sacramento-Modesto route: $89k annual savings if EV         │
│  2. Install DC fast charging at Stockton hub: saves $34k/yr     │
│  3. Negotiate volume electricity rate: potential $28k/yr        │
│                                                                  │
│  🎯 2025 Transition Goals:                                       │
│     ████████░░░░░░░░░░ 40% (Target: 25 EV haulers by Q4)        │
│                                                                  │
│  [Member Performance]  [Route Analysis]  [Export Report]        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## DEVELOPMENT ROADMAP

### Phase 1: MVP (Months 1-3)
- [ ] Database schema implementation
- [ ] Core cost calculation engine
- [ ] Integration with GasBuddy API (diesel prices)
- [ ] Integration with PlugShare API (EV charging locations/prices)
- [ ] Basic route cost comparison UI
- [ ] Excel export functionality
- [ ] 10 major CA cities coverage

### Phase 2: Enhanced Features (Months 4-6)
- [ ] Time-of-use rate optimization
- [ ] Dealer network management
- [ ] Private charging station tracking
- [ ] Mobile app (driver view)
- [ ] Automated data refresh (hourly)
- [ ] Historical price trending
- [ ] Expand to 50+ CA cities

### Phase 3: Advanced Analytics (Months 7-9)
- [ ] Machine learning price prediction
- [ ] Syndicate aggregation dashboard
- [ ] Incentive eligibility matching
- [ ] TCO calculator with financing options
- [ ] Weather-adjusted range modeling
- [ ] Maintenance cost tracking integration

### Phase 4: Enterprise Features (Months 10-12)
- [ ] API for third-party integrations
- [ ] White-label capability for partners
- [ ] Blockchain-based energy credit trading
- [ ] Integration with fleet management systems
- [ ] Automated reporting for investors
- [ ] Multi-state expansion (beyond CA)

---

## R&D TAX CREDIT JUSTIFICATION

**Technical Uncertainties Being Resolved:**

1. **Optimal charging strategy algorithms** - No existing solution optimally sequences fast vs. slow charging based on route constraints and time-of-use rates

2. **Payload-adjusted range prediction** - Physics-based modeling of EV range degradation under variable load conditions specific to car hauling

3. **Multi-tenant cost aggregation with privacy preservation** - Novel approach to calculating collective insights without exposing dealer-specific data

4. **Real-time tariff optimization** - Complex rate structures require custom parsing engines for each utility's tariff schedules

5. **Stochastic fuel price modeling** - Combining historical volatility with current market signals to project future cost scenarios

**Process of Experimentation:**

- Testing multiple routing algorithms (Dijkstra vs. A* vs. genetic algorithms)
- Evaluating different ML models for price prediction (ARIMA vs. LSTM vs. Prophet)
- Prototyping various UI/UX approaches for dealer usability
- Load testing database designs for time-series efficiency
- API integration testing with multiple data providers

This software development qualifies for R&D tax credits under IRC Section 41.

---

**Document Version:** 1.0  
**Last Updated:** December 2025  
**Next Review:** January 2026
