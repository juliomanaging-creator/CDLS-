import os
import sys
import hashlib
import uuid
import pandas as pd
from core.deal_jackets import DealJacketManager

def run_diagnostics():
    print("=== S.A.L.S.A. PRE-FLIGHT DIAGNOSTIC v2.0 ===")
    print("---------------------------------------------")
    
    # 1. Verify Folder Structure
    required_folders = ['core', 'deal_jackets', 'data_input', 'audit_output', 'logs']
    missing_folders = [f for f in required_folders if not os.path.exists(f)]
    
    if not missing_folders:
        print("[PASS] Directory Architecture: OK")
    else:
        print(f"[FAIL] Missing Folders: {missing_folders}")

    # 2. Hardware ID Generation
    try:
        hw_id = hashlib.md5(hex(uuid.getnode()).encode()).hexdigest()
        print(f"[INFO] Local Hardware ID: {hw_id}")
        
        license_key = os.getenv("SALSA_LICENSE_KEY")
        dev_mode = os.getenv("SALSA_DEV_MODE")
        
        if dev_mode == "1":
            print("[PASS] License Status: BYPASS (DEV_MODE ACTIVE)")
        elif license_key == hw_id:
            print("[PASS] License Status: VALIDATED")
        else:
            print("[WARN] License Status: LOCKED (Key missing or invalid)")
    except Exception as e:
        print(f"[FAIL] License Logic Error: {e}")

    # 3. Deal Jacket & Export Logic
    try:
        manager = DealJacketManager()
        test_file = manager.export_to_accounting_csv("diagnostic_test.csv")
        
        if os.path.exists(test_file):
            print("[PASS] CSV Export Engine: OPERATIONAL")
            os.remove(test_file)
        else:
            print("[FAIL] CSV Export Engine: FILE NOT CREATED")
    except Exception as e:
        print(f"[FAIL] Deal Jacket Logic Error: {e}")

    # 4. Dashboard Connectivity
    if os.path.exists("dashboard.html"):
        print("[PASS] Emerald Dashboard: DETECTED")
    else:
        print("[FAIL] Emerald Dashboard: FILE NOT FOUND")

    print("---------------------------------------------")
    print("Diagnostic Complete.")

if __name__ == "__main__":
    run_diagnostics()