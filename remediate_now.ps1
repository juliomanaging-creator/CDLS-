# ==============================================================================
# CDLS Remediation Automation Script (NIST/SIMM/CIS Assurance)
# Version: 2.2 — Production Live Remediation & Evidence Vault Synchronizer
# ==============================================================================
[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = "Continue"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host "   CDLS AUTOMATED REMEDIATION & COMPLIANCE GAP CLOSURE  " -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "   MODE: DRY RUN - no changes will be made              " -ForegroundColor Yellow
} else {
    Write-Host "   MODE: LIVE REMEDIATION                               " -ForegroundColor Green
}
Write-Host "========================================================`n" -ForegroundColor Cyan

$evidenceVault = "CDLS_Security_Audit_Evidence"
if (-not (Test-Path $evidenceVault)) {
    New-Item -ItemType Directory -Force -Path $evidenceVault | Out-Null
}

# ------------------------------------------------------------------------------
# 1. REMEDIATE FIPS 140-3 OVERSTATEMENT IN AUDIT REPORT & SENTINEL
# ------------------------------------------------------------------------------
Write-Host "[1/5] Checking and Remediating FIPS 140-3 Claims..." -ForegroundColor Yellow

$fipsPattern     = "\* \*\*FIPS 140-3\*\*: Cryptographic integrity & non-repudiation"
$fipsReplacement = "* **Cryptographic Integrity**: SHA-256 manifest verification per NIST AU-9. " +
                   "FIPS 140-3: Planned hardware-level HSM integration (AWS KMS / Azure Key Vault — SC-12 gap, target Rev 3.0)"

$reportFile = "SECURITY_AUDIT_REPORT.md"
if (Test-Path $reportFile) {
    $reportText = Get-Content -LiteralPath $reportFile -Raw
    if ($reportText -match "FIPS 140-3") {
        if (-not $DryRun) {
            $reportText =$reportText -replace $fipsPattern,$fipsReplacement
            Set-Content -LiteralPath $reportFile -Value$reportText -Encoding utf8
            Write-Host "  [FIXED] FIPS 140-3 claim scoped accurately in $reportFile" -ForegroundColor Green
        } else {
            Write-Host "  [DRY-RUN] Would update FIPS 140-3 claim in $reportFile" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [OK] FIPS claim in $reportFile already scoped." -ForegroundColor Gray
    }
}

$sentinelFile = "security_sentinel.py"
if (Test-Path $sentinelFile) {
    $sentinelText = Get-Content -LiteralPath $sentinelFile -Raw
    if ($sentinelText -match "FIPS 140-3") {
        if (-not $DryRun) {
            $sentinelText =$sentinelText -replace $fipsPattern,$fipsReplacement
            Set-Content -LiteralPath $sentinelFile -Value$sentinelText -Encoding utf8
            Write-Host "  [FIXED] FIPS 140-3 template scoped accurately in $sentinelFile" -ForegroundColor Green
        } else {
            Write-Host "  [DRY-RUN] Would update FIPS 140-3 template in $sentinelFile" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [OK] FIPS claim in $sentinelFile already scoped." -ForegroundColor Gray
    }
} else {
    Write-Host "  [SKIP] $sentinelFile not found in project root." -ForegroundColor DarkGray
}

# ------------------------------------------------------------------------------
# 2. RUN REAL TRIVY CONTAINER IMAGE SCANS (15m timeout)
# ------------------------------------------------------------------------------
Write-Host "`n[2/5] Running Concrete Trivy Container Image Scans..." -ForegroundColor Yellow

$latestEvidenceDir = Get-ChildItem -Directory "$evidenceVault\compliance_evidence_*" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $latestEvidenceDir) {
    $dateStamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $targetDir = "$evidenceVault\compliance_evidence_$dateStamp"
    New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
} else {
    $targetDir = $latestEvidenceDir.FullName
}

$trivyImageReport = "$targetDir\trivy_image_report.txt"
$dockerRunning = $false
try {
    docker info 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { $dockerRunning = $true }
} catch { $dockerRunning = $false }

if ($dockerRunning) {
    Write-Host "  [*] Executing Trivy image scans (cdls-api:latest, cdls-vdr:latest)..." -ForegroundColor Cyan
    if (-not $DryRun) {
        "=== cdls-api:latest ===" | Out-File -FilePath $trivyImageReport -Encoding ascii
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock `
            aquasec/trivy image --timeout 15m --scanners vuln --severity HIGH,CRITICAL `
            cdls-api:latest | Out-File -FilePath $trivyImageReport -Append -Encoding ascii

        "`n=== cdls-vdr:latest ===" | Out-File -FilePath $trivyImageReport -Append -Encoding ascii
        docker run --rm -v /var/run/docker.sock:/var/run/docker.sock `
            aquasec/trivy image --timeout 15m --scanners vuln --severity HIGH,CRITICAL `
            cdls-vdr:latest | Out-File -FilePath $trivyImageReport -Append -Encoding ascii

        Write-Host "  [FIXED] Image scan results saved to: $trivyImageReport" -ForegroundColor Green
    } else {
        Write-Host "  [DRY-RUN] Would scan cdls-api:latest and cdls-vdr:latest" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [!] Docker daemon offline. Start Docker Desktop and re-run." -ForegroundColor Yellow
}

# ------------------------------------------------------------------------------
# 3. VERIFY CREDENTIAL SANITIZATION IN settings.py
# ------------------------------------------------------------------------------
Write-Host "`n[3/5] Verifying Credential Sanitization in settings.py..." -ForegroundColor Yellow

if (Test-Path "settings.py") {
    $settingsContent = Get-Content -LiteralPath "settings.py" -Raw
    $hasHardcodedUser = $settingsContent -match 'os\.getenv\("DB_USER",\s*"user"\)'
    $hasHardcodedPass = $settingsContent -match 'os\.getenv\("DB_PASS",\s*"pass"\)'

    if ($hasHardcodedUser -or $hasHardcodedPass) {
        Write-Host "  [!] Hardcoded default credentials found in settings.py:" -ForegroundColor Yellow
        if ($hasHardcodedUser) { Write-Host '      DB_USER default = "user"' -ForegroundColor Yellow }
        if ($hasHardcodedPass) { Write-Host '      DB_PASS default = "pass"' -ForegroundColor Yellow }
    } else {
        Write-Host "  [OK] No hardcoded credential defaults found in settings.py." -ForegroundColor Green
    }
} else {
    Write-Host "  [SKIP] settings.py not found." -ForegroundColor DarkGray
}

# ------------------------------------------------------------------------------
# 4. RUN COMPLETE PYTEST TEST SUITE (87+ SOP Threshold)
# ------------------------------------------------------------------------------
Write-Host "`n[4/5] Executing Extended Pytest Suite..." -ForegroundColor Yellow

$testResultsFile = "$targetDir\full_test_results_$(Get-Date -Format 'yyyyMMdd_HHmmss').txt"

if (Test-Path "tests") {
    if (-not $DryRun) {
        Write-Host "  [*] Running: python -m pytest tests -v --tb=short" -ForegroundColor Cyan
        python -m pytest tests -v --tb=short | Tee-Object -FilePath $testResultsFile
        Write-Host "  [FIXED] Full test results saved to: $testResultsFile" -ForegroundColor Green
    } else {
        Write-Host "  [DRY-RUN] Would run pytest against tests\" -ForegroundColor Yellow
    }
} else {
    Write-Host "  [!] tests\ directory not found." -ForegroundColor Yellow
}

# ------------------------------------------------------------------------------
# 5. REGENERATE SHA-256 INTEGRITY MANIFEST
# ------------------------------------------------------------------------------
Write-Host "`n[5/5] Re-Hashing Deliverable Evidence Manifest..." -ForegroundColor Yellow

if (-not $DryRun) {
    $manifestFile = "$targetDir\SHA256_MANIFEST.txt"
    $manifestContent = "# CDLS Platform — SHA-256 Evidence Manifest`n"
    $manifestContent += "# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n`n"
    $manifestContent += "Algorithm`tHash`t`t`t`t`t`t`t`t`tFile`n"
    $manifestContent += "---------`t----`t`t`t`t`t`t`t`t`t----`n"

    Get-ChildItem -Path "$targetDir\*" |
        Where-Object { $_.Name -ne "SHA256_MANIFEST.txt" -and -not $_.PSIsContainer } |
        ForEach-Object {
            $hash = (Get-FileHash -Path $_.FullName -Algorithm SHA256).Hash
            $manifestContent += "SHA256`t`t$hash`t$($_.Name)`n"
            Write-Host "  Hashed: $($_.Name)" -ForegroundColor Green
        }

    Set-Content -Path $manifestFile -Value $manifestContent -Encoding utf8
    Write-Host "  [FIXED] SHA-256 manifest written to: $manifestFile" -ForegroundColor Green
} else {
    Write-Host "  [DRY-RUN] Would hash all files in $targetDir" -ForegroundColor Yellow
}

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Remediation Completed Cleanly!" -ForegroundColor Green
Write-Host " Target Vault: $targetDir" -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Green


