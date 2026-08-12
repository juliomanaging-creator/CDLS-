# Energy Pod Trailer Specifications
pod_capacity_kwh = 90  # EcoFlow DELTA Pro Ultra (stackable to 90kWh)
usable_capacity_kwh = 63  # 70% depth of discharge (DOD) for longevity
charge_rate_kw = 7.2  # Level 2 charging (240V, 30A)
discharge_rate_kw = 19.2  # Fermata V2G inverter max
fleet_size = 100  # Initial Sacramento pilot

# Dealer Site Configuration
dealers_participating = 6  # Initial LOI sites
pods_per_dealer = 17  # ~17 trailers per dealer (100 ÷ 6)
parking_duration_hours = 20  # Trailers idle 20 hrs/day (4 hrs hauling)

# Grid Revenue Streams
elrp_rate_per_kwh = 2.00  # Emergency Load Reduction Program
day_ahead_rate_per_kwh = 0.35  # CAISO day-ahead market
real_time_rate_per_kwh = 0.85  # Peak demand (4-9 PM)
lcfs_credit_per_kwh = 0.08  # Low Carbon Fuel Standard

# Operational Costs
pod_capex = 18000  # EcoFlow system + HED dampening
trailer_modification = 5000  # Custom bay integration
v2g_inverter = 12000  # Fermata Energy charger
installation_per_site = 45000  # Bonding, electrical, permits
monthly_maintenance = 150  # Per pod per month