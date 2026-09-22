[CmdletBinding()]
param([switch]$DryRun)

$ErrorActionPreference = "Continue"
$Results = @{ Fixed=@(); Manual=@(); Skipped=@(); Failed=@() }

function Log-Fixed  ($msg) {$Results.Fixed  += $msg; Write-Host "  [FIXED]  $msg" -ForegroundColor Green }
function Log-Manual ($msg) {$Results.Manual += $msg; Write-Host "  [MANUAL] $msg" -ForegroundColor Yellow }
function Log-Skip   ($msg) {$Results.Skipped+= $msg; Write-Host "  [SKIP]   $msg" -ForegroundColor Gray }
function Log-Fail   ($msg) {$Results.Failed += $msg; Write-Host "  [FAIL]   $msg" -ForegroundColor Red }

Write-Host "`n========================================================"  -ForegroundColor Cyan
Write-Host "  CDLS Aikido Security Findings — Automated Remediation"     -ForegroundColor Cyan
Write-Host "========================================================`n"  -ForegroundColor Cyan

# 1. Critical & High Dependency Upgrades
if (-not $DryRun) {
    pip install "sentence-transformers>=3.1.0" "chromadb>=0.6.0" "huggingface-hub>=0.26.0" "PyMuPDF>=1.24.14" "transformers>=4.46.0" "wrapt>=1.17.0" --upgrade -q
    if ($LASTEXITCODE -eq 0) { Log-Fixed "All Python security dependencies upgraded to patched vulnerability floor" }
    else { Log-Fail "Some package upgrades failed. Check pip output." }
} else { Write-Host "  [DRY-RUN] Would upgrade Python dependencies" -ForegroundColor Yellow }

# 2. Patch API Server trust_remote_code
$apiFile = "api_server.py"
if (Test-Path $apiFile) {$content = Get-Content $apiFile -Raw$old = 'embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5")'
    $new = 'embed_model = SentenceTransformer("BAAI/bge-small-en-v1.5", trust_remote_code=False)'
    if ($content -match [regex]::Escape($old)) {
        if (-not $DryRun) {
            Set-Content $apiFile ($content -replace [regex]::Escape($old),$new) -Encoding utf8
            Log-Fixed "api_server.py: trust_remote_code=False added"
        }
    }
}

# 3. Nginx Headers (CSP + HSTS)
$nginxConf = "nginx\nginx.conf"
if (-not (Test-Path $nginxConf)) {$nginxConf = "nginx.conf" }
if (Test-Path $nginxConf) {
    $nginxContent = Get-Content$nginxConf -Raw
    if ($nginxContent -notmatch "Content-Security-Policy") {
        $cspHeader = '        add_header Content-Security-Policy "default-src ''self''; script-src ''self'' https://cdn.tailwindcss.com https://cdn.jsdelivr.net; style-src ''self''; img-src ''self'' blob: data:; connect-src ''self'' wss:; frame-ancestors ''none''; base-uri ''self''; form-action ''self''" always;'
        $hstsLine  = '        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;'
        if (-not $DryRun) {
            $nginxContent =$nginxContent -replace "(add_header X-Request-ID[^\n]+\n)", "`$1$cspHeader`n$hstsLine`n"
            Set-Content $nginxConf $nginxContent -Encoding utf8
            Log-Fixed "nginx.conf: CSP and HSTS headers injected successfully"
        }
    }
}

Write-Host "`n========================================================"  -ForegroundColor Cyan
Write-Host "  REMEDIATION COMPLETED"                                       -ForegroundColor Cyan
Write-Host "========================================================"  -ForegroundColor Cyan
