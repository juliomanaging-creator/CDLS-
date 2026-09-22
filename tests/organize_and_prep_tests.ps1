# ==============================================================================
# CDLS Automated Test Suite Organization & Migration Script
# Version: 2.1 — BOM-free initialization and 87+ SOP threshold verification
# ==============================================================================
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "   CDLS TEST SUITE ORGANIZATION & 87+ SOP VALIDATOR     " -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

$testsDir = "tests"
if (-not (Test-Path $testsDir)) {
    New-Item -ItemType Directory -Force -Path $testsDir | Out-Null
    Write-Host "[+] Created directory: .\$testsDir" -ForegroundColor Green
} else {
    Write-Host "[*] Directory .\$testsDir already exists." -ForegroundColor Cyan
}

$requiredModules = @("test_incidents.py", "test_security.py", "test_auth.py", "tests.py", "conftest.py")

Write-Host "`n[1/3] Locating and organizing test modules..." -ForegroundColor Yellow
foreach ($mod in$requiredModules) {
    if (Test-Path "$testsDir\$mod") {
        Write-Host "  [OK] $mod is already located in .\$testsDir\" -ForegroundColor Gray
        continue
    }

    $foundFile = Get-ChildItem -Recurse -Filter$mod -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($foundFile) {
        Copy-Item -LiteralPath $foundFile.FullName -Destination "$testsDir\$mod" -Force
        Write-Host "  [FIXED] Copied $($foundFile.Name) from $($foundFile.DirectoryName) into .\$testsDir\" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] Module '$mod' not found in workspace." -ForegroundColor Yellow
    }
}

# Write pytest.ini without BOM (ASCII encoding) to prevent parsing errors
Write-Host "`n[2/3] Validating pytest.ini configuration..." -ForegroundColor Yellow
$pytestIniContent = @"
[pytest]
testpaths = tests
python_files = test_*.py *_test.py tests.py
norecursedirs = compliance_evidence_* .git .venv temp_audio chroma_db chroma_audio_store node_modules secure_vault patent_drawings
filterwarnings =
    ignore::DeprecationWarning
asyncio_mode = auto
"@
[System.IO.File]::WriteAllText("$PWD\pytest.ini", $pytestIniContent, [System.Text.Encoding]::ASCII)
Write-Host "  [OK] pytest.ini configured successfully without BOM." -ForegroundColor Green

Write-Host "`n[3/3] Executing Full Test Suite against .\$testsDir..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$resultLog = "full_test_results_$timestamp.txt"

python -m pytest tests -v --tb=short | Tee-Object -FilePath $resultLog

if (Test-Path $resultLog) {
    $logContent = Get-Content -LiteralPath$resultLog -Raw
    if ($logContent -match '(\d+)\s+passed') {
        $passCount = [int]$Matches[1]
        Write-Host "`n--------------------------------------------------------" -ForegroundColor Cyan
        Write-Host " TEST EXECUTION SUMMARY: $passCount tests passed" -ForegroundColor $(if ($passCount -ge 87) { "Green" } else { "Yellow" })
        Write-Host "--------------------------------------------------------" -ForegroundColor Cyan
        
        if ($passCount -ge 87) {
            Write-Host " [SUCCESS] Threshold met! SOP requirement of 87+ tests satisfied." -ForegroundColor Green
        } else {
            Write-Host " [WARN] $passCount tests passed. SOP requires 87+." -ForegroundColor Yellow
        }
    }
}

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Project Test Organization Complete!" -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Green