CREATE TABLE kinetic_mesh (
    vin VARCHAR(17) UNIQUE,
    cluster_name VARCHAR(100),
    battery_kwh INTEGER,
    price VARCHAR(50),
    scan_timestamp TIMESTAMP,
    ip_strategy VARCHAR(50)
);