# =====================================================================
# CDLS Repository File Compression & GitHub Pages Deployment Automation
# =====================================================================

Write-Host "Starting repository optimization..." -ForegroundColor Cyan

# 1. Zip heavy CAD (.step) files in Sovereign_Initiatives
$cadPath = "C:\Users\MezaJ\OneDrive\Sovereign_Initiatives"
if (Test-Path $cadPath) {
    $stepFiles = Get-ChildItem -Path $cadPath -Filter "*.step" -Recurse
    if ($stepFiles.Count -gt 0) {
        Write-Host "Compressing CAD (.step) files..." -ForegroundColor Yellow
        Compress-Archive -Path "$cadPath\*.step" -DestinationPath "$cadPath\Sovereign_CAD_Assets.zip" -Force
        Remove-Item -Path "$cadPath\*.step" -Force
        Write-Host "CAD files compressed into Sovereign_CAD_Assets.zip." -ForegroundColor Green
    }
}

# 2. Convert Excel .xlsx files over 25MB to .xlsb using COM Automation
$excelFiles = Get-ChildItem -Path "C:\Users\MezaJ\OneDrive" -Filter "*.xlsx" -Recurse
$excelApp = $null

foreach ($file in $excelFiles) {
    if ($file.Length -gt 25MB) {
        Write-Host "Found large Excel file: $($file.Name) ($([math]::Round($file.Length/1MB, 2)) MB)" -ForegroundColor Yellow
        
        if ($null -eq $excelApp) {
            $excelApp = New-Object -ComObject Excel.Application
            $excelApp.Visible = $false
            $excelApp.DisplayAlerts = $false
        }

        $workbook = $excelApp.Workbooks.Open($file.FullName)
        $newPath = [System.IO.Path]::ChangeExtension($file.FullName, ".xlsb")
        
        # 50 = xlExcel12 (Binary Workbook format)
        $workbook.SaveAs($newPath, 50)
        $workbook.Close($false)
        
        # Untrack old .xlsx and remove local file
        git rm --cached "$($file.FullName)" -ErrorAction SilentlyContinue
        Remove-Item -Path $file.FullName -Force
        Write-Host "Converted $($file.Name) -> $([System.IO.Path]::GetFileName($newPath)) and removed original." -ForegroundColor Green
    }
}

if ($null -ne $excelApp) {
    $excelApp.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excelApp) | Out-Null
}

# 3. Configure Git memory settings
Write-Host "Configuring Git memory settings..." -ForegroundColor Cyan
git config --global core.preloadindex false

# 4. Stage optimized assets and updated repository state
Write-Host "Staging files for Git..." -ForegroundColor Cyan
git add CAESAR_Auditor_Platform CDLS_ZEV_Logistics Dealership_and_Operations Developer_and_Code_Assets Grants_Tax_and_Incentives Sovereign_Initiatives *.html *.py *.md *.csv *.zip *.xlsb .gitignore

# 5. Commit changes
Write-Host "Creating deployment commit..." -ForegroundColor Cyan
git commit -m "Automated asset compression and deployment optimization"

# 6. Push to GitHub
Write-Host "Pushing changes to GitHub..." -ForegroundColor Cyan
git push origin main --force

Write-Host "`nOptimization & Push Complete! GitHub Pages build re-triggered." -ForegroundColor Green
