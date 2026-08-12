function calculate_arbitrage_window(grid_price, soc_level) {
    if (soc_level > 20 && grid_price > MARKET_THRESHOLD) {
        return "INITIATE_V2G_DISCHARGE";
    }
    return "STAY_IN_RESERVE";
}