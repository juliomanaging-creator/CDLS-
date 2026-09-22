import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    """Establishes a secure PostgreSQL connection with RealDictCursor."""
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "cdls_grants_pilot"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "postgres"),
        cursor_factory=RealDictCursor
    )
    return conn

def run_migrations():
    """Applies institutional schema migrations with foreign key constraints."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tenants (
                tenant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                name VARCHAR(255) NOT NULL,
                agency_type VARCHAR(100) NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grants (
                grant_id VARCHAR(50) PRIMARY KEY,
                tenant_id UUID REFERENCES tenants(tenant_id) ON DELETE CASCADE,
                title VARCHAR(255) NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'Under Review',
                allocated NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
                compliance_score INT CHECK (compliance_score BETWEEN 0 AND 100),
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_audit_logs (
                log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                grant_id VARCHAR(50) REFERENCES grants(grant_id) ON DELETE CASCADE,
                agent_name VARCHAR(100) NOT NULL,
                evaluation_summary TEXT NOT NULL,
                risk_level VARCHAR(20) NOT NULL,
                evaluated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
        """)

        conn.commit()
        print("[SUCCESS] PostgreSQL schema migrations applied successfully.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Migration failed: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_migrations()