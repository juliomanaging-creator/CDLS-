# --- 2026 Directory-as-Context Starter ---

# 1. Start Ollama silently
if (-not (Get-Process "ollama" -ErrorAction SilentlyContinue)) {
    Write-Host "🚀 Starting local LLM engine..." -ForegroundColor Cyan
    Start-Process "ollama" -ArgumentList "serve" -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

# 2. Verify Directory Context
$kbPath = ".\knowledge_base"
$sectors = Get-ChildItem -Path $kbPath -Directory
Write-Host "📂 Found $($sectors.Count) Sectors: $($sectors.Name -join ', ')" -ForegroundColor Yellow

# 3. Auto-Index Check
# If the index doesn't exist, run the indexer first
if (-not (Test-Path ".\unified_knowledge_index")) {
    Write-Host "🧠 Building initial knowledge index..." -ForegroundColor Magenta
    & ".\venv\Scripts\python.exe" update_index.py
}

# 4. Launch Streamlit UI
Write-Host "✨ Launching Agent..." -ForegroundColor Green
& ".\venv\Scripts\python.exe" -m streamlit run agent_ui.py