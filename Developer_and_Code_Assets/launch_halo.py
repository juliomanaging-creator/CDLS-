import os
import time
import psycopg2

# 'r' prefix prevents the SyntaxWarning for C:\Projects
STATUS_FILE = r"C:\Projects\mesh_active.txt"
DB_URL = os.getenv("DATABASE_URL", "postgresql://architect:your_password@halo_db:5432/iron_halo_vault")

def log_to_db(event):
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("INSERT INTO system_logs (event, timestamp) VALUES (%s, NOW())", (event,))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database Log Error: {e}")

def main():
    print(r"--- INITIATING IRON HALO MESH [C:\Projects] ---")
    with open(STATUS_FILE, "w") as f:
        f.write("ACTIVE")
    
    log_to_db("MESH_STARTUP: Iron Halo Engine Online")
    
    try:
        while True:
            # Main monitoring loop
            time.sleep(5)
    except KeyboardInterrupt:
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)

if __name__ == "__main__":
    main()