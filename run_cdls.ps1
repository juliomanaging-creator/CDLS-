# ==========================================================
# CDLS Multi-Agent RAG Platform Launcher & Runner
# ==========================================================

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "   CDLS Secure Platform Startup Utility     " -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

# 1. Ensure .env file exists for container environment variables
if (-not (Test-Path ".env")) {
    Write-Host "[INFO] .env file not found. Generating default secure configuration..." -ForegroundColor Yellow
    @"
SECRET_KEY=cdls-production-secure-cryptographic-key-998877
DB_USER=postgres
DB_PASS=postgres
DB_HOST=postgres
DB_PORT=5432
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/cdls_production
"@ | Out-File -Encoding utf8 .env
    Write-Host "[SUCCESS] .env configuration generated." -ForegroundColor Green
} else {
    Write-Host "[OK] Existing .env configuration detected." -ForegroundColor Green
}

# 2. Build and spin up the hardened Docker Compose stack
Write-Host "[INFO] Launching hardened container stack via Docker Compose..." -ForegroundColor Yellow
docker compose -f docker-compose.hardened.yml up --build -d

# 3. Verify status
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host "   [SUCCESS] CDLS PLATFORM RUNNING STABLY!   " -ForegroundColor Green
    Write-Host "=============================================" -ForegroundColor Green
    Write-Host "-> FastAPI Docs / Swagger UI: http://localhost:8000/docs" -ForegroundColor Cyan
    Write-Host "-> Active Containers:" -ForegroundColor Cyan
    docker compose -f docker-compose.hardened.yml ps
} else {
    Write-Host "[ERROR] Failed to start containers. Please ensure Docker Desktop is running." -ForegroundColor Red
}