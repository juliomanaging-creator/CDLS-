# ==============================================================================
# CDLS Automated Test Suite Organization & Migration Script
# Organizes test modules into tests\ and validates the 87+ SOP threshold
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

# Core test modules required for the 87+ test suite
$requiredModules = @("test_incidents.py", "test_security.py", "test_auth.py", "tests.py", "conftest.py")

Write-Host "`n[1/3] Locating and organizing test modules..." -ForegroundColor Yellow
foreach ($mod in $requiredModules) {
    # Check if already in tests\
    if (Test-Path "$testsDir\$mod") {
        Write-Host "  [OK] $mod is already located in .\$testsDir\" -ForegroundColor Gray
        continue
    }

    # Search project root or subdirectories
    $foundFile = Get-ChildItem -Recurse -Filter $mod -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($foundFile) {
        Copy-Item -LiteralPath $foundFile.FullName -Destination "$testsDir\$mod" -Force
        Write-Host "  [FIXED] Copied $($foundFile.Name) from $($foundFile.DirectoryName) into .\$testsDir\" -ForegroundColor Green
    } else {
        Write-Host "  [WARN] Module '$mod' not found anywhere in workspace. (If newly authored, place it in .\$testsDir\)" -ForegroundColor Yellow
    }
}

# ------------------------------------------------------------------------------
# 2. UPDATE pytest.ini TO ENSURE SEAMLESS RECURSION DISCOVERY
# ------------------------------------------------------------------------------
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
Set-Content -Path "pytest.ini" -Value $pytestIniContent -Encoding utf8
Write-Host "  [OK] pytest.ini configured successfully to target .\tests\" -ForegroundColor Green

# ------------------------------------------------------------------------------
# 3. EXECUTE FULL TEST SUITE & VALIDATE 87+ THRESHOLD
# ------------------------------------------------------------------------------
Write-Host "`n[3/3] Executing Full Test Suite against .\$testsDir..." -ForegroundColor Yellow

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$resultLog = "full_test_results_$timestamp.txt"

# Run pytest targeting the tests directory
python -m pytest tests -v --tb=short | Tee-Object -FilePath $resultLog

# Parse passing test count
if (Test-Path $resultLog) {
    $logContent = Get-Content $resultLog -Raw
    # Matches summary lines like "87 passed" or "92 passed"
    if ($logContent -match '(\d+)\s+passed') {
        $passCount = [int]$Matches[1]
        Write-Host "`n--------------------------------------------------------" -ForegroundColor Cyan
        Write-Host " TEST EXECUTION SUMMARY: $passCount tests passed" -ForegroundColor $(if ($passCount -ge 87) { "Green" } else { "Yellow" })
        Write-Host "--------------------------------------------------------" -ForegroundColor Cyan
        
        if ($passCount -ge 87) {
            Write-Host " [SUCCESS] Threshold met! SOP requirement of 87+ tests satisfied." -ForegroundColor Green
        } else {
            Write-Host " [WARN] $passCount tests passed. SOP requires 87+. Ensure all test functions are uncommented." -ForegroundColor Yellow
        }
    } else {
        Write-Host " [*] Test execution finished. Check $resultLog for detailed breakdown." -ForegroundColor Cyan
    }
}

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Project Test Organization Complete!" -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Green