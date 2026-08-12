// Enhanced Settlement for Multi-Pickup Routes
app.post('/api/v1/settle-batch-haul', async (req, res) => {
    const { dealerId, offers } = req.body;
    
    try {
        let totalValue = 0;
        let totalUnits = 0;
        let totalMiles = 0;
        let inoperableCount = 0;

        // Aggregate batch data WITH operational status tracking
        offers.forEach(o => {
            const numericValue = parseFloat(o.amount.replace(/[^0-9.-]+/g, ""));
            totalValue += numericValue;
            totalUnits += o.units;
            totalMiles += o.distance || 0;
            if (!o.operable) inoperableCount++;
        });

        // Calculate efficiency metrics for institutional reporting
        const avgRatePerMile = totalValue / totalMiles;
        const complexityBonus = inoperableCount > 0 ? 1.15 : 1.0; // 15% for non-runners

        // Dealer Tier Share with complexity adjustment
        const tierShare = 0.20; 
        const haulMintAmount = totalValue * tierShare * complexityBonus;

        // CRITICAL: Log route efficiency data for CalPERS reporting
        await db.query(`
            INSERT INTO haul_settlements 
            (dealer_id, total_units, total_miles, haul_revenue, avg_rate_per_mile, inoperable_count, settlement_date) 
            VALUES ($1, $2, $3, $4, $5, $6, NOW())
        `, [dealerId, totalUnits, totalMiles, totalValue, avgRatePerMile, inoperableCount]);

        // Record individual order details for audit trail
        for (const offer of offers) {
            await db.query(`
                INSERT INTO order_ledger 
                (order_id, vin, pickup_city, delivery_city, distance, rate, operable) 
                VALUES ($1, $2, $3, $4, $5, $6, $7)
            `, [
                offer.orderId, 
                offer.vin, 
                offer.pickupCity, 
                offer.deliveryCity, 
                offer.distance, 
                offer.amount,
                offer.operable
            ]);
        }

        res.status(200).json({
            success: true,
            totalHaulMinted: haulMintAmount.toFixed(2),
            avgRatePerMile: avgRatePerMile.toFixed(2),
            efficiencyScore: (avgRatePerMile / 2.50 * 100).toFixed(1), // % of target rate
            message: `Batch of ${offers.length} hauls settled. ${inoperableCount} inoperable units processed.`
        });
    } catch (error) {
        console.error("Settlement failure:", error);
        res.status(500).json({ error: "Settlement Engine Failure" });
    }
});