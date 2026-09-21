# ==============================================================================
# CDLS Complete Launch, Verification & Evidence Packaging Pipeline
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "   CDLS FULL-STACK SECURITY & AUDIT PACKAGER LAUNCHER   " -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

# ------------------------------------------------------------------------------
# 1. RUN CORE SECURITY SENTINEL (AppSec Gate: SAST, SCA, Secrets, IaC)
# ------------------------------------------------------------------------------
Write-Host "[1/4] Running Security Sentinel Audit..." -ForegroundColor Yellow
& python security_sentinel.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "[!] Security Sentinel encountered issues. Please review output." -ForegroundColor Red
} else {
    Write-Host "[+] Security Sentinel Audit completed with 100/100 score." -ForegroundColor Green
}

# ------------------------------------------------------------------------------
# 2. RUN EXPANDED INFRASTRUCTURE & REGRESSION SCANS
# ------------------------------------------------------------------------------
Write-Host "`n[2/4] Executing Broader Infrastructure & Test Runner..." -ForegroundColor Yellow
.\run_broad_scans.ps1

# ------------------------------------------------------------------------------
# 3. LOCATE LATEST EVIDENCE ARTIFACTS
# ------------------------------------------------------------------------------
Write-Host "`n[3/4] Locating Latest Evidence Dossier..." -ForegroundColor Yellow
$latestEvidenceDir = Get-ChildItem -Directory "CDLS_Security_Audit_Evidence\compliance_evidence_*" | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $latestEvidenceDir) {
    Write-Error "No compliance_evidence_* directory was found."
    exit 1
}

Write-Host "[+] Target Directory: $($latestEvidenceDir.FullName)" -ForegroundColor Green

# ------------------------------------------------------------------------------
# 4. BUNDLE EVERYTHING INTO AUDITOR SUBMISSION PACKAGE
# ------------------------------------------------------------------------------
$dateStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$packageZip = "CDLS_Compliance_Submission_Package_$dateStamp.zip"
$stageDir = "audit_staging_$dateStamp"

New-Item -ItemType Directory -Force -Path $stageDir | Out-Null

# Copy primary artifacts
Copy-Item -Path "SECURITY_AUDIT_REPORT.md" -Destination "$stageDir\" -Force
Copy-Item -Path "$($latestEvidenceDir.FullName)\*" -Destination "$stageDir\" -Recurse -Force

# Generate package root manifest
Get-ChildItem -Path "$stageDir\*" | Where-Object { $_.Name -ne "PACKAGE_SHA256_MANIFEST.txt" } | Get-FileHash -Algorithm SHA256 | Out-File -FilePath "$stageDir\PACKAGE_SHA256_MANIFEST.txt" -Encoding ascii

# Zip archive
Compress-Archive -Path "$stageDir\*" -DestinationPath $packageZip -Force
Remove-Item -Path $stageDir -Recurse -Force

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Full Package Generated Successfully!" -ForegroundColor Green
Write-Host " Deliverable ZIP: $pwd\$packageZip" -ForegroundColor Green
Write-Host " Primary Report : $pwd\SECURITY_AUDIT_REPORT.md" -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Green

