$repoPath = "$env:USERPROFILE\OneDrive"
Set-Location -Path $repoPath

Write-Host "`n========================================================" -ForegroundColor Yellow
Write-Host "   STEP 1: GENERATING INTERACTIVE GRAPH & EXTENSION      " -ForegroundColor Yellow
Write-Host "========================================================`n" -ForegroundColor Yellow

$devAssetsPath = Join-Path $repoPath "Developer_and_Code_Assets"
if (-not (Test-Path -LiteralPath $devAssetsPath)) { New-Item -ItemType Directory -Path $devAssetsPath | Out-Null }

# 1. Manifest
$manifestJson = @'
{
  "manifest_version": 3,
  "name": "CAESAR Platform Tab Manager",
  "version": "1.0",
  "description": "Interactive dropdown and accordion menu for managing open Edge tabs.",
  "permissions": ["tabs", "activeTab"],
  "action": { "default_popup": "popup.html" }
}
