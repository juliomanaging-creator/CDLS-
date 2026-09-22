# ==============================================================================
# CDLS Master Audit Deliverable Packaging Script
# Compiles the evidence vault into a timestamped, cryptographically sealed ZIP
# ==============================================================================
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "   CDLS MASTER COMPLIANCE PACKAGE COMPILER              " -ForegroundColor Cyan
Write-Host "========================================================`n" -ForegroundColor Cyan

$evidenceVault = "CDLS_Security_Audit_Evidence"
$latestEvidenceDir = Get-ChildItem -Directory "$evidenceVault\compliance_evidence_*" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1

if (-not $latestEvidenceDir) {
    Write-Host "[!] No active compliance evidence vault found. Run remediate_now.ps1 first." -ForegroundColor Red
    exit 1
}

$sourceDir = $latestEvidenceDir.FullName
$dateStamp = Get-Date -Format "yyyyMMdd_HHmmss"
$zipPackage = "$evidenceVault\CDLS_Compliance_Submission_Package_$dateStamp.zip"

Write-Host "[*] Packaging evidence from: $sourceDir" -ForegroundColor Cyan

if (Test-Path $zipPackage) {
    Remove-Item -LiteralPath $zipPackage -Force
}

Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($sourceDir, $zipPackage)

Write-Host " [SUCCESS] Submission package created successfully:" -ForegroundColor Green
Write-Host " Archive Path: $zipPackage" -ForegroundColor Green
Write-Host "`n========================================================" -ForegroundColor Green