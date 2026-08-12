#!/usr/bin/env python3
"""
CDLS Data Lake - Simple Launcher
Runs the GUI application with automatic setup
"""

import sys
import subprocess
import os
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import pandas
        import pyarrow
        import duckdb
        import openpyxl
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True
    except:
        return False

def main():
    # Check if we're in the right directory
    if not Path("cdls_data_lake_app.py").exists():
        print("Error: Please run this script from the data-lake-setup directory")
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("Dependencies not found. Installing...")
        if not install_dependencies():
            print("Failed to install dependencies.")
            print("Please run: pip install -r requirements.txt")
            sys.exit(1)
    
    # Launch the application
    print("Launching CDLS Data Lake...")
    try:
        from cdls_data_lake_app import main as app_main
        app_main()
    except Exception as e:
        print(f"Error launching application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
