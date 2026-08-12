class JudasBiddingSystem:
    def __init__(self, fleet_soc, grid_price_signal):
        self.soc = fleet_soc  # State of Charge (%)
        self.price = grid_price_signal # CAISO Real-Time Price ($/kWh)
        self.threshold = 1.20 # Minimum bid price ($)

    def evaluate_bid(self):
        # 1. Check Grid Stress (Price spikes)
        if self.price >= self.threshold:
            # 2. Check Fleet Health
            available_units = [u for u in self.soc if u > 20] # Never drain below 20%
            
            if len(available_units) > 100:
                return "EXECUTE_DISCHARGE" # Signal sent to ISO 15118 chargers
        
        return "HOLD_ENERGY" # Wait for higher peak

# Judas AI constantly scans the CAISO OASIS API every 5 minutes.