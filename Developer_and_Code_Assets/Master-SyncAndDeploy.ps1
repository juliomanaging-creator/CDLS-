# ==============================================================================
# MASTER PIPELINE: DOWNLOADS ORGANIZER -> REPO SYNC -> INDEX GEN -> GITHUB PUSH
# ==============================================================================

$downloadsPath = "$env:USERPROFILE\Downloads"
$repoPath      = "$env:USERPROFILE\OneDrive"
$organizerScript = Join-Path $downloadsPath "Organize-Downloads.ps1"

Write-Host "`n========================================================" -ForegroundColor Gold
Write-Host "   STEP 1: EXECUTING LOCAL DOWNLOADS ORGANIZER          " -ForegroundColor Gold
Write-Host "========================================================`n" -ForegroundColor Gold

if (Test-Path -LiteralPath $organizerScript) {
    & $organizerScript
    Write-Host "[OK] Downloads organized into subfolders." -ForegroundColor Green
} else {
    Write-Host "[SKIP] Organize-Downloads.ps1 not found in $downloadsPath" -ForegroundColor DarkGray
}

Write-Host "`n========================================================" -ForegroundColor Gold
Write-Host "   STEP 2: SYNCING DOWNLOADS TO GITHUB REPO SUBFOLDERS  " -ForegroundColor Gold
Write-Host "========================================================`n" -ForegroundColor Gold

$folderRouting = @{
    "Documents_PDFs"    = "Sovereign_Initiatives"
    "Spreadsheets_Data" = "Grants_Tax_and_Incentives"
    "Installers_Apps"   = "Developer_and_Code_Assets"
    "Images_Media"      = "Developer_and_Code_Assets"
    "Archives_Code"     = "Developer_and_Code_Assets"
}

$repoFiles = Get-ChildItem -LiteralPath $repoPath -Recurse -File -ErrorAction SilentlyContinue | 
    Where-Object { 
        $_.FullName -notmatch '\\\.git\\' -and 
        $_.Name -notlike "*.env*" -and 
        $_.Name -ne "desktop.ini" 
    }

$repoHashes = @{}
foreach ($file in $repoFiles) {
    $hashObj = Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256 -ErrorAction SilentlyContinue
    if ($hashObj) {
        $repoHashes[$file.Name] = @{
            Path = $file.FullName
            Hash = $hashObj.Hash
        }
    }
}

$downloadFiles = Get-ChildItem -LiteralPath $downloadsPath -Recurse -File -ErrorAction SilentlyContinue | 
    Where-Object { 
        $_.Name -notlike "*.crdownload" -and 
        $_.Name -ne "Organize-Downloads.ps1" -and 
        $_.Name -notlike "*.env*" -and 
        $_.Name -ne "desktop.ini" 
    }

foreach ($file in $downloadFiles) {
    $dlHashObj = Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256 -ErrorAction SilentlyContinue
    if (-not $dlHashObj) { continue }
    
    $dlHash = $dlHashObj.Hash
    $categoryFolder = $file.Directory.Name
    $targetSubfolder = if ($folderRouting.ContainsKey($categoryFolder)) { $folderRouting[$categoryFolder] } else { "Developer_and_Code_Assets" }
    $targetPath = Join-Path -Path $repoPath -ChildPath $targetSubfolder

    if (-not (Test-Path -LiteralPath $targetPath)) {
        New-Item -ItemType Directory -Path $targetPath | Out-Null
    }

    if ($repoHashes.ContainsKey($file.Name)) {
        $match = $repoHashes[$file.Name]
        if ($match.Hash -eq $dlHash) {
            Write-Host "[UNCHANGED] $($file.Name) - Already in repo." -ForegroundColor DarkGray
        } else {
            Write-Host "[UPDATED] $($file.Name) -> Updating in $targetSubfolder" -ForegroundColor Yellow
            Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $targetPath $file.Name) -Force -ErrorAction SilentlyContinue
        }
    } else {
        Write-Host "[NEW FILE] $($file.Name) -> Copying to $targetSubfolder" -ForegroundColor Cyan
        Copy-Item -LiteralPath $file.FullName -Destination (Join-Path $targetPath $file.Name) -Force -ErrorAction SilentlyContinue
    }
}

Write-Host "`n========================================================" -ForegroundColor Gold
Write-Host "   STEP 3: GENERATING SUBDIRECTORY INDEX.HTML PAGES     " -ForegroundColor Gold
Write-Host "========================================================`n" -ForegroundColor Gold

$subdirs = @(
    "CAESAR_Auditor_Platform",
    "CDLS_ZEV_Logistics",
    "Dealership_and_Operations",
    "Developer_and_Code_Assets",
    "Grants_Tax_and_Incentives",
    "Sovereign_Initiatives"
)

foreach ($dir in $subdirs) {
    $dirPath = Join-Path $repoPath $dir
    if (Test-Path -LiteralPath $dirPath) {
        $files = Get-ChildItem -LiteralPath $dirPath -File -ErrorAction SilentlyContinue | 
            Where-Object { $_.Name -ne "index.html" -and $_.Name -ne "desktop.ini" }
        
        $fileItemsHtml = ""
        foreach ($f in $files) {
            $fileItemsHtml += @"
            <li style="margin-bottom: 0.8rem;">
                <a href="$($f.Name)" style="color: #d4af37; text-decoration: none; font-weight: 600;">$($f.Name)</a>
                <span style="color: #8b949e; font-size: 0.85rem; margin-left: 0.5rem;">($([math]::Round($f.Length / 1KB, 2)) KB)</span>
            </li>
"@
        }

        $htmlContent = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>$dir Directory Index</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0d1117; color: #c9d1d9; padding: 2rem; }
        .container { max-width: 800px; margin: 0 auto; background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 2rem; }
        h1 { color: #f0f6fc; font-size: 1.5rem; border-bottom: 1px solid #30363d; padding-bottom: 0.75rem; }
        a.back-link { color: #58a6ff; text-decoration: none; font-size: 0.9rem; display: inline-block; margin-bottom: 1rem; }
        ul { list-style: none; padding: 0; margin-top: 1.5rem; }
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="back-link">&larr; Back to Main Directory</a>
        <h1>$dir</h1>
        <ul>
            $fileItemsHtml
        </ul>
    </div>
</body>
</html>
"@
        Set-Content -Path (Join-Path $dirPath "index.html") -Value $htmlContent
    }
}
Write-Host "[OK] Directory index pages successfully generated." -ForegroundColor Green

Write-Host "`n========================================================" -ForegroundColor Gold
Write-Host "   STEP 4: STAGING, COMMITTING, AND PUSHING TO GITHUB   " -ForegroundColor Gold
Write-Host "========================================================`n" -ForegroundColor Gold

Set-Location -Path $repoPath

if (Test-Path -LiteralPath "Developer_and_Code_Assets\conversations.json") {
    git rm --cached Developer_and_Code_Assets/conversations.json 2>$null
}

git add .
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Automated sync and index update: $timestamp"

$env:GIT_OPTIONAL_LOCKS = "0"
git push origin main

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host "   PIPELINE COMPLETE: ALL CHANGES LIVE ON GITHUB PAGES  " -ForegroundColor Green
Write-Host "========================================================`n" -ForegroundColor Green
