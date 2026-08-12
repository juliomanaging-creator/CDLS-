import os
import shutil

def deploy_emerald_suite():
    print("=== S.A.L.S.A. EMERALD AUTO-DEPLOYMENT ===")
    
    # 1. Define the production tree
    structure = {
        'core': ['__init__.py', 'engine.py', 'deal_jackets.py'],
        'data_input': [],
        'deal_jackets': [],
        'audit_output': [],
        'audit_reports_pdf': [],
        'logs': [],
        'examples': []
    }

    # 2. Create Folders
    for folder in structure.keys():
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"[OK] Created folder: {folder}")

    # 3. Create __init__.py to fix Import Errors
    init_file = os.path.join('core', '__init__.py')
    with open(init_file, 'w') as f:
        f.write("# S.A.L.S.A. Core Package\n")
    print("[FIX] Initialized core package to resolve import errors.")

    # 4. Relocate Orphaned Files
    # Note: This moves files from root to core if they exist in root
    files_to_move = ['engine.py', 'deal_jackets.py']
    for f in files_to_move:
        if os.path.exists(f):
            shutil.move(f, os.path.join('core', f))
            print(f"[MOVE] Relocated {f} to core/")

    print("\n[SUCCESS] Environment organized for Emerald Production.")
    print("Run Deploy_SALSA.bat to launch.")

if __name__ == "__main__":
    deploy_emerald_suite()