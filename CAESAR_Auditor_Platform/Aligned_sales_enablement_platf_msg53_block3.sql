-- Create read-only user for Retool queries
CREATE USER retool_readonly WITH PASSWORD 'secure_password_here';
GRANT CONNECT ON DATABASE cdls_calculator TO retool_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO retool_readonly;

-- Create read-write user for Retool mutations
CREATE USER retool_readwrite WITH PASSWORD 'another_secure_password';
GRANT CONNECT ON DATABASE cdls_calculator TO retool_readwrite;
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO retool_readwrite;

-- Don't grant DELETE except on specific tables
GRANT DELETE ON calculations, analytics_events TO retool_readwrite;