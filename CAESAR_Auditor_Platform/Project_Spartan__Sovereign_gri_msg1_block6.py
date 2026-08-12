class GridReliabilityMonitor:
    def __init__(self):
        self.soc_threshold = 0.20  # Never discharge below 20%
        self.backup_reserves = 500  # kWh buffer per region
    
    async def validate_dispatch_order(self, request):
        available_capacity = await self.get_fleet_soc()
        if available_capacity < request.mwh + self.backup_reserves:
            return {"status": "REJECT", "reason": "Insufficient reserves"}