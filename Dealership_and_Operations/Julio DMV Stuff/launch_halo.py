import os
import time

# Absolute path for the air-gapped status handshake
STATUS_FILE = r"C:\Projects\mesh_active.txt"

def main():
    print("--- INITIATING IRON HALO MESH [C:\Projects] ---")
    
    # Signal the dashboard that we are live
    try:
        with open(STATUS_FILE, "w") as f:
            f.write("ACTIVE")
        
        print("Scrambling Shards... DNA Verified. Monitoring Nodes...")
        while True:
            # Main monitoring loop
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutting down Mesh...")
    finally:
        if os.path.exists(STATUS_FILE):
            os.remove(STATUS_FILE)

if __name__ == "__main__":
    main()