# Get LMP from CAISO
lmp = requests.get("http://caiso_connector:80/api/latest-lmp").json()

# Make V2G decision based on price
if lmp['price'] > 0.15:  # High price = discharge
    requests.post(
        "http://tesla_connector:8001/vehicles/VIN/discharge",
        json={"target_soc": 30, "max_power_kw": 650}
    )
elif lmp['price'] < 0.05:  # Low price = charge
    requests.post(
        "http://tesla_connector:8001/vehicles/VIN/charge",
        json={"target_soc": 85, "max_rate_kw": 250}
    )