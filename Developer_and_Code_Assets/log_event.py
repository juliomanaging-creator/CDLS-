import datetime
import sys

LOG_FILE = r"C:\Projects\mesh_audit_log.txt"

def log_event(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        log_event(sys.argv[1])