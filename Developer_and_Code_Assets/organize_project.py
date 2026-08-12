import os
import shutil

def setup_salsa_environment():
    # Define the professional directory structure
    folders = [
        'core',                 # Engine and Deal Jacket logic
        'data_input',           # CSVs from DMS or Auctions
        'deal_jackets',         # Digital JSON folders for vehicles
        'audit_output',         # Compliance text reports
        'audit_reports_pdf',     # Compliance PDF reports
        'logs',                 # System logs
        'reports',              # PDF generator components
        'examples'              # Templates for dealers
    ]

    print("=== S.A.L.S.A. Project Architect ===")
    
    # Create Folders
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created folder: {folder}")
        else:
            print(f"Verified folder: {folder}")

    # Ensure __init__.py exists for proper Python importing
    init_path = os.path.join('core', '__init__.py')
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write("# S.A.L.S.A. Core Package\n")
        print("Initialized core package.")

    print("\nEnvironment Organized. Ready for Launch.")

if __name__ == "__main__":
    setup_salsa_environment()