#!/usr/bin/env python3
"""
Quick Setup Script
Run this first to install dependencies and verify your environment.
Usage: python setup.py
"""

import subprocess
import sys
import os
from typing import Optional

import os as _os
from pathlib import Path as _Path

def _safe_path(user_path: str, base_dir: Optional[str] = None) -> str:
    if base_dir is None:
        base_dir = str(_Path(__file__).resolve().parent)
    real = _os.path.realpath(_os.path.abspath(user_path))
    allowed = _os.path.realpath(_os.path.abspath(base_dir))
    if not real.startswith(allowed + _os.sep) and real != allowed:
        raise ValueError(f"Path traversal attempt detected: {user_path!r}")
    return real


def check_python_version():
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]}")


def install_requirements():
    print("\nInstalling dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("✓ Dependencies installed")


def check_api_key():
    key = os.getenv("ANTHROPIC_API_KEY", "")
    if not key:
        print("\n⚠️  ANTHROPIC_API_KEY not set")
        print("   Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        print("   Or add it to a .env file")
        return False
    print(f"✓ ANTHROPIC_API_KEY found (sk-...{key[-6:]})")
    return True


def create_env_file():
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write("# Anthropic Knowledge Base Configuration\n")
            f.write("ANTHROPIC_API_KEY=your-api-key-here\n\n")
            f.write("# Optional: Use PostgreSQL instead of SQLite\n")
            f.write("# USE_POSTGRES=false\n")
            f.write("# POSTGRES_DSN=postgresql://user:pass@localhost:5432/anthropic_kb\n\n")
            f.write("# Models (defaults shown)\n")
            f.write("# CATEGORIZATION_MODEL=claude-haiku-4-5-20251001\n")
            f.write("# QUERY_MODEL=claude-sonnet-4-20250514\n\n")
            f.write("# Paths\n")
            f.write("# SQLITE_PATH=./anthropic_kb.db\n")
            f.write("# CHROMA_DIR=./chroma_db\n")
        print("✓ Created .env file — add your ANTHROPIC_API_KEY to it")


def create_init_files():
    for path in ["agents/__init__.py", "database/__init__.py", "utils/__init__.py", "config/__init__.py"]:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if not os.path.exists(path):
            open(path, "w").close()
    print("✓ Package __init__.py files created")


def run_quick_test():
    print("\nRunning quick system test...")
    try:
        import anthropic
        import httpx
        from bs4 import BeautifulSoup
        print("✓ Core imports successful")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

    try:
        import sqlite3
        conn = sqlite3.connect(":memory:")
        conn.close()
        print("✓ SQLite available")
    except Exception as e:
        print(f"❌ SQLite error: {e}")

    try:
        import chromadb
        print("✓ ChromaDB available")
    except ImportError:
        print("⚠️  ChromaDB not available (will use in-memory fallback)")

    return True


if __name__ == "__main__":
    print("=" * 50)
    print("ANTHROPIC KNOWLEDGE BASE - Setup")
    print("=" * 50)

    check_python_version()
    create_init_files()
    create_env_file()
    install_requirements()
    check_api_key()
    run_quick_test()

    print("\n" + "=" * 50)
    print("Setup complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("  1. Add your ANTHROPIC_API_KEY to .env")
    print("  2. Run: python orchestrator.py   (full pipeline)")
    print("  3. Or:  python -c \"")
    print("       import asyncio")
    print("       from orchestrator import OrchestratorAgent")
    print("       from config.settings import load_config")
    print("       o = OrchestratorAgent(load_config())")
    print("       asyncio.run(o.query('What are Claude\\'s capabilities?'))\"")
    print("\nFor continuous updates: python scheduler.py")
