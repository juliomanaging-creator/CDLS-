import os
import sys
import subprocess
from pathlib import Path
ROOT = Path(r"C:\Projects\AWS AGENT")
def check_step(name, condition, fix_msg):
    if condition:
        print(f"✅ {name}: OK")
        return True
    else:
        print(f"❌ {name}: FAILED")
        print(f"   👉 FIX: {fix_msg}")
        return False

def run_debug():
    print("🔍 --- Starting 2026 Agent Master Debug ---")
    all_clear = True

    # 1. Check Virtual Environment
    is_venv = sys.prefix != sys.base_prefix
    all_clear &= check_step("Virtual Environment", is_venv, "Run '.\venv\Scripts\Activate.ps1' in PowerShell.")

    # 2. Check Required 2026 Libraries
    required_libs = ["langchain_ollama", "langchain_classic", "fpdf", "streamlit", "faiss"]
    missing_libs = []
    for lib in required_libs:
        try:
            __import__(lib.replace("-", "_"))
        except ImportError:
            missing_libs.append(lib)
    
    all_clear &= check_step("Libraries Installed", len(missing_libs) == 0, 
                            f"Missing: {', '.join(missing_libs)}. Run: pip install langchain-ollama langchain-classic fpdf2 streamlit faiss-cpu")

    # 3. Check Directory Structure & Sector Folders
    kb_path = Path("./knowledge_base")
    sectors = ["aws", "finance", "legal", "healthcare"]
    missing_sectors = [s for s in sectors if not (kb_path / s).exists()]
    
    all_clear &= check_step("Sector Folders", len(missing_sectors) == 0, 
                            f"Missing: {', '.join(missing_sectors)}. Run: mkdir -p {', '.join(['knowledge_base/'+s for s in sectors])}")

    # 4. Check for Knowledge Base Content
    md_files = list(kb_path.glob("**/*.md"))
    all_clear &= check_step("Markdown Files", len(md_files) > 0, "Place at least one .md file in a sector folder.")

    # 5. Check Ollama Server & Models
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        models = [m['name'] for m in response.json().get('models', [])]
        needed = ["llama3.2:latest", "nomic-embed-text:latest"]
        missing_models = [m for m in needed if m not in models]
        
        all_clear &= check_step("Ollama Server", response.status_code == 200, "Ensure Ollama is running (ollama serve).")
        all_clear &= check_step("Models Downloaded", len(missing_models) == 0, 
                                f"Missing: {', '.join(missing_models)}. Run: ollama pull [model_name]")
    except Exception:
        all_clear &= check_step("Ollama Server", False, "Ollama is not responding. Run 'ollama serve'.")

    # 6. Final Verdict
    print("---" * 10)
    if all_clear:
        print("🚀 READY TO LAUNCH!")
        print("Run: python -m streamlit run agent_ui.py")
    else:
        print("⚠️ Issues found. Please apply the fixes above and re-run debug.")

if __name__ == "__main__":
    run_debug()