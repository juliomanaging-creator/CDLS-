# ==============================================================================
# CDLS Repository Isolation & Sanitization Pipeline (Dynamic Path)
# ==============================================================================
$ErrorActionPreference = "Stop"

Write-Host "`n[*] Starting Git repository sanitization and isolation..." -ForegroundColor Cyan

# 1. Use the script's actual parent directory automatically
$projectDir = if ($PSScriptRoot) {$PSScriptRoot } else { (Get-Location).Path }
Set-Location -LiteralPath $projectDir
Write-Host "[+] Working Directory: $pwd" -ForegroundColor Green

# 2. Write strict .gitignore to prevent personal and sensitive data leakage
$gitignoreContent = @"
# Environment & Secrets
.env
.env*
*.env
*.txt.txt

# Personal Documents & Binaries
*.pdf
*.bin
*.zip
*.lnk
*.jpg
*.png

# External and Operating Folders
/Dealership_and_Operations/
/Sovereign_Initiatives/
/Developer_and_Code_Assets/
/CAESAR_Auditor_Platform/
/CDLS_ZEV_Logistics/
/Personal_and_Financial/
/Job Applications/
/data-lake-setup/
/Funds/
/Security/
/Camera Roll/
/Documents/
/Pictures/
/Screenshots/

# Python Runtime & Caches
__pycache__/
*.py[cod]
.venv/
env/
venv/
.pytest_cache/
temp_audio/
chroma_db/
chroma_audio_store/

# Local OS & Editor artifacts
.vscode/
desktop.ini
Thumbs.db
"@

Set-Content -LiteralPath "$projectDir\.gitignore" -Value $gitignoreContent -Encoding utf8
Write-Host "[+] Strict .gitignore created." -ForegroundColor Green

# 3. Disconnect from parent git tree if running inside a nested repo
if (Test-Path -LiteralPath "$projectDir\.git") {
    Remove-Item -LiteralPath "$projectDir\.git" -Recurse -Force
    Write-Host "[+] Reset local repository state." -ForegroundColor Green
}

# 4. Initialize fresh local repository bounded exclusively to this folder
git init -b main
Write-Host "[+] Isolated Git repository initialized on branch main." -ForegroundColor Green

# 5. Stage only project files permitted by .gitignore
git add .
Write-Host "[+] Permitted code and documentation files staged." -ForegroundColor Green

# 6. Create clean initial commit
git commit -m "chore(core): initialize clean, isolated CDLS IP studio platform"

# 7. Wire to GitHub remote repository
$remoteUrl = "https://github.com/juliomanaging-creator/CDLS-.git"
git remote add origin $remoteUrl
Write-Host "[+] Remote origin set to $remoteUrl." -ForegroundColor Green

# 8. Force-push the isolated, sanitized commit history to replace remote tree
Write-Host "[*] Pushing sanitized repository to GitHub..." -ForegroundColor Cyan
git push --force -u origin main

Write-Host "`n[SUCCESS] Repository successfully sanitized, isolated, and pushed to GitHub!`n" -ForegroundColor Green
