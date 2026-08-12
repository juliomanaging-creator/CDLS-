# --- ARCHITECT COMMAND: IRON HALO IGNITION ---
$ErrorActionPreference = "SilentlyContinue"
Write-Host "`n[1/4] DETECTING CORE INFRASTRUCTURE..." -ForegroundColor Cyan

# Force current directory to Projects root
Set-Location "C:\Projects"

# --- PATH REPAIR PROTOCOL ---
# If 'docker' isn't found, we manually inject the likely install paths
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Docker not in PATH. Reconstructing environment links..." -ForegroundColor Yellow
    $DockerPaths = @(
        "C:\Program Files\Docker\Docker\resources\bin",
        "C:\Program Files\Docker\Docker\resources",
        "C:\Program Data\DockerDesktop\version-bin"
    )
    foreach ($path in $DockerPaths) {
        if (Test-Path $path) {
            $env:Path += ";$path"
            Write-Host "[+] Linked: $path" -ForegroundColor Gray
        }
    }
}

# --- DOCKER ENGINE VERIFICATION ---
if (!(Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "`n[ERROR] Docker Desktop is not installed or not running." -ForegroundColor Red
    Write-Host "Please ensure the Docker Whale icon is Green in your system tray.`n" -ForegroundColor White
    Pause
    exit
}

Write-Host "[2/4] REPAIRING PYTHON ENVIRONMENT..." -ForegroundColor Cyan
# This fixes the psycopg2 error for your local machine if you run outside Docker
python -m pip install psycopg2-binary fpdf --quiet

Write-Host "[3/4] ASSEMBLING DOCKER CONTAINERS..." -ForegroundColor Cyan
# The '--build' ensures any changes to your code are baked into the new image
docker compose up -d --build

Write-Host "`n[4/4] SYSTEM STABILIZED." -ForegroundColor Green
Write-Host "--------------------------------------------------"
Write-Host "PORTAL LIVE  : http://127.0.0.1:9000" -ForegroundColor White
Write-Host "MOBILE MIRROR: http://192.168.1.125:9000" -ForegroundColor White
Write-Host "--------------------------------------------------`n"

# Open the portal automatically
Start-Process "http://127.0.0.1:9000"
Pause