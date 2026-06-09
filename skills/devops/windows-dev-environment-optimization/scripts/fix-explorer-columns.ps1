# Windows Explorer Column Defaults Fix
# Run: powershell -ExecutionPolicy Bypass -File fix-explorer-columns.ps1
# Clears folder view cache and sets Details view with Name (wide) + Type columns.
# Run once per user. No admin needed.
# If this doesn't stick after running, use the manual fallback:
#   View -> Options -> View -> Apply to Folders

$ErrorActionPreference = "Stop"
Write-Host "Resetting Windows Explorer folder views..."

# Kill explorer briefly to release locks
Stop-Process -Name explorer -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Clear all saved folder view settings (bag cache)
$bagsPath = "HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags"
$bagsMRU = "HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU"

Remove-Item -Path "$bagsPath\AllFolders" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "$bagsMRU" -Recurse -Force -ErrorAction SilentlyContinue

# Set AllFolders default to Details view (Mode=4, LogicalViewMode=1)
$basePath = "HKCU:\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags\AllFolders\Shell"
New-Item -Path $basePath -Force | Out-Null
Set-ItemProperty -Path $basePath -Name "FolderType" -Value "NotSpecified" -Type String -Force
Set-ItemProperty -Path $basePath -Name "Mode" -Value 4 -Type DWord -Force
Set-ItemProperty -Path $basePath -Name "LogicalViewMode" -Value 1 -Type DWord -Force

# Define column layout: Name(400px) | DateModified(150px) | Type(150px) | Size(100px)
# ColInfo binary format: 4-byte sort index | column definitions
# Each column: 4-byte prop ID | 4-byte width | 4-byte char-width | 1-byte flags
$cols = [byte[]]@(
    # Sort indicator (4 bytes)
    0x00, 0x00, 0x00, 0x00,

    # Column 0: Name (prop 0, width 400, flags 1=visible)
    0x00, 0x00, 0x00, 0x00,
    0x90, 0x01, 0x00, 0x00,
    0x90, 0x01, 0x00, 0x00,
    0x01,

    # Column 1: Date Modified (prop 3, width 150)
    0x03, 0x00, 0x00, 0x00,
    0x96, 0x00, 0x00, 0x00,
    0x96, 0x00, 0x00, 0x00,
    0x01,

    # Column 2: Type (prop 4, width 150) — THIS IS THE KEY DEFAULT THE USER WANTS
    0x04, 0x00, 0x00, 0x00,
    0x96, 0x00, 0x00, 0x00,
    0x96, 0x00, 0x00, 0x00,
    0x01,

    # Column 3: Size (prop 1, width 100)
    0x01, 0x00, 0x00, 0x00,
    0x64, 0x00, 0x00, 0x00,
    0x64, 0x00, 0x00, 0x00,
    0x01
)

# Write the binary ColInfo value
Set-ItemProperty -Path $basePath -Name "ColInfo" -Value $cols -Type Binary -Force

# Restart explorer
Write-Host "Done. Restarting Explorer..."
Start-Process explorer

Write-Host ""
Write-Host "New defaults applied. If they don't stick:"
Write-Host "  1. Open any folder"
Write-Host "  2. Set it to Details view with Name (wide) + Type columns"
Write-Host "  3. View -> Options -> View -> Apply to Folders"
