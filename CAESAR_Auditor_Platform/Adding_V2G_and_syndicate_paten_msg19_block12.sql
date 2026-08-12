-- Get all Sacramento inventory
SELECT * FROM kinetic_mesh WHERE cluster_name = 'Sacramento';

-- Find vehicles under $30K
SELECT vin, model, price FROM kinetic_mesh 
WHERE CAST(REPLACE(price, '$', '') AS INTEGER) < 30000;

-- Get average prices by cluster
SELECT cluster_name, AVG(CAST(REPLACE(price, '$', '') AS INTEGER)) 
FROM kinetic_mesh GROUP BY cluster_name;

-- Find high-capacity batteries (100+ kWh)
SELECT * FROM kinetic_mesh WHERE battery_kwh >= 100;