<#
.SYNOPSIS
    Gathers scattered project files (by file extension) from your Downloads
    folder and your local OneDrive folder into a single destination folder,
    ready to be pushed to GitHub.

.NOTES
    - Copies files by default (originals are left in place). Set $MoveInstead
      to $true if you want them moved instead of copied.
    - Skips common junk/build folders (node_modules, .git, __pycache__, etc).
    - If two files have the same name, the newer one is kept and the older
      one is renamed with a "_conflict" suffix so nothing is silently lost.
    - Writes a log of everything it did to a .txt file next to the destination
      folder so you can review what happened.
#>

# ================== EDIT THESE SETTINGS ==================

# File extensions that belong to your project (edit this list)
$Extensions = @(".py", ".js", ".html", ".css", ".json", ".md")

# Where to look for files
$SourceFolders = @(
    "$env:USERPROFILE\Downloads",
    "$env:USERPROFILE\OneDrive"          # adjust if your OneDrive path differs,
                                          # e.g. "$env:USERPROFILE\OneDrive - CompanyName"
)

# Where to put the gathered project files
$DestFolder = "$env:USERPROFILE\Desktop\MyProject"

# Copy (safe, default) or Move (removes originals) the files
$MoveInstead = $false

# Folders to ignore entirely while scanning (build artifacts, dependencies, etc.)
$ExcludeDirs = @("node_modules", ".git", "__pycache__", "dist", "build", ".venv", "venv")

# ============================================================

# --- Setup ---
if (-not (Test-Path $DestFolder)) {
    New-Item -ItemType Directory -Path $DestFolder | Out-Null
}

$LogPath = Join-Path (Split-Path $DestFolder -Parent) "GatherProjectFiles_Log.txt"
$LogEntries = @()
$CopiedCount = 0
$SkippedCount = 0
$ConflictCount = 0

function Should-ExcludePath($path) {
    foreach ($dir in $ExcludeDirs) {
        if ($path -match "\\$([regex]::Escape($dir))\\") {
            return $true
        }
    }
    return $false
}

Write-Host "Scanning for files with extensions: $($Extensions -join ', ')" -ForegroundColor Cyan

foreach ($source in $SourceFolders) {
    if (-not (Test-Path $source)) {
        Write-Host "Skipping (not found): $source" -ForegroundColor Yellow
        $LogEntries += "SKIPPED SOURCE (not found): $source"
        continue
    }

    Write-Host "Scanning: $source" -ForegroundColor Cyan

    $files = Get-ChildItem -Path $source -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object {
            ($Extensions -contains $_.Extension.ToLower()) -and
            (-not (Should-ExcludePath $_.FullName))
        }

    foreach ($file in $files) {
        $destPath = Join-Path $DestFolder $file.Name

        if (Test-Path $destPath) {
            $existing = Get-Item $destPath
            if ($existing.LastWriteTime -ge $file.LastWriteTime) {
                # Existing copy is same age or newer — skip this one but log it
                $SkippedCount++
                $LogEntries += "SKIPPED (older duplicate): $($file.FullName)"
                continue
            } else {
                # Incoming file is newer — keep the OLD one under a conflict name first
                $conflictName = [System.IO.Path]::GetFileNameWithoutExtension($existing.Name) + "_conflict" + $existing.Extension
                $conflictPath = Join-Path $DestFolder $conflictName
                Move-Item -Path $destPath -Destination $conflictPath -Force
                $ConflictCount++
                $LogEntries += "CONFLICT: kept older file as $conflictName, replacing with newer version from $($file.FullName)"
            }
        }

        if ($MoveInstead) {
            Move-Item -Path $file.FullName -Destination $destPath -Force
        } else {
            Copy-Item -Path $file.FullName -Destination $destPath -Force
        }

        $CopiedCount++
        $LogEntries += "COPIED: $($file.FullName) -> $destPath"
    }
}

# --- Write log ---
$Summary = @(
    "Gather-ProjectFiles run: $(Get-Date)"
    "Destination: $DestFolder"
    "Files copied/moved: $CopiedCount"
    "Duplicates skipped: $SkippedCount"
    "Conflicts (older file renamed): $ConflictCount"
    ""
    "---- Details ----"
) + $LogEntries

$Summary | Out-File -FilePath $LogPath -Encoding UTF8

Write-Host ""
Write-Host "Done." -ForegroundColor Green
Write-Host "  Files gathered : $CopiedCount"
Write-Host "  Skipped (dupes): $SkippedCount"
Write-Host "  Conflicts      : $ConflictCount"
Write-Host "  Destination    : $DestFolder"
Write-Host "  Full log       : $LogPath"
