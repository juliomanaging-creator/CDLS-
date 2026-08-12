-- All agents read/write to central PostgreSQL database

-- Agent 12 (Carbon Calculation) writes
INSERT INTO carbon_credits (haul_id, mt_co2, created_at)
VALUES (12345, 0.29, NOW());

-- Agent 13 (Carbon Banking) reads
SELECT SUM(mt_co2) FROM carbon_credits WHERE status = 'pending';

-- Agent 6 (Carbon Legal) updates
UPDATE carbon_credits SET status = 'verra_submitted' WHERE id = 123;

-- Agent 14 (Carbon Trading) sells
UPDATE carbon_credits SET status = 'sold', buyer = 'Microsoft' WHERE id = 123;