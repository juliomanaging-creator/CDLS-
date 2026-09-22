<#
.SYNOPSIS
Universal Multi-Agent RAG: Auto-Repair, Sync, and Run Script
#>

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  UNIVERSAL RESEARCH AGENT: REPAIR & SYNC PIPELINE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Enforce UTF-8 to eliminate cp1252 character mapping errors
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
Write-Host "[1/4] Console stream encoding set to UTF-8." -ForegroundColor Green

# 2. Ensure package directories exist
$directories = @("agents", "database", "utils", "config")
foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir | Out-Null
        Write-Host "      Created missing directory: $dir" -ForegroundColor Yellow
    }
}

# 3. Ensure each submodule contains an __init__.py package marker
foreach ($dir in $directories) {
    $initFile = Join-Path $dir "__init__.py"
    if (-not (Test-Path $initFile)) {
        New-Item -ItemType File -Path $initFile | Out-Null
        Write-Host "      Created package marker: $initFile" -ForegroundColor Yellow
    }
}
Write-Host "[2/4] Package directories and stubs verified." -ForegroundColor Green

# 4. Mirror root scripts into designated subpackages
$syncMap = @{
    "categorization_agent.py" = "agents\categorization_agent.py"
    "ingestion_agent.py"      = "agents\ingestion_agent.py"
    "query_agent.py"          = "agents\query_agent.py"
    "rd_insights_agent.py"    = "agents\rd_insights_agent.py"
    "db_manager.py"           = "database\db_manager.py"
    "logger.py"               = "utils\logger.py"
    "settings.py"             = "config\settings.py"
}

foreach ($source in $syncMap.Keys) {
    if (Test-Path $source) {
        $destination = $syncMap[$source]
        Copy-Item -Path $source -Destination $destination -Force
        Write-Host "      Synced: $source -> $destination" -ForegroundColor Gray
    }
}
Write-Host "[3/4] Submodule synchronization complete." -ForegroundColor Green

# 5. Launch the orchestrator
Write-Host "[4/4] Executing orchestrator.py..." -ForegroundColor Green
Write-Host "------------------------------------------------------------" -ForegroundColor DarkGray

try {
    python orchestrator.py
} catch {
    Write-Host "`nPipeline halted: $_" -ForegroundColor Red
}