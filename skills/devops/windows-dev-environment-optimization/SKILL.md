---
name: windows-dev-environment-optimization
description: "Diagnose and fix Windows dev environment problems: slow PowerShell startup, conda init overhead, dead PATH entries, broken Miniconda installs, and directory junction management. Covers the class of 'Windows tools are slow at startup and something is broken.'"
version: 1.0.0
author: derived from Hermes agent session
license: MIT
metadata:
  hermes:
    tags: [windows, powershell, conda, path, environment, optimization, startup]
    related_skills: [project-shipping-framework, cli-open-source-tools]
---

# Windows Dev Environment Optimization

## Class of Problem

Windows dev environments accumulate:
- Dead PATH entries from uninstalled software
- Multiple PowerShell profiles running slow init hooks
- Conda/miniconda init overhead (1500-2000ms per shell start)
- Leftover activation scripts from uninstalled tools (Pinokio, etc.)
- Broken dependency trees in conda's site-packages

The symptom is always the same: **"PowerShell/terminal takes 3+ seconds to start and there are error messages."**

## Diagnosis Protocol

### Step 1: Check PowerShell Profiles

Both PS5 and PS7 profiles can exist. Check all locations:

- `OneDrive\Documents\PowerShell\profile.ps1` (PS7 CurrentUser)
- `OneDrive\Documents\WindowsPowerShell\profile.ps1` (PS5 CurrentUser)
- `OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` (PS7 CurrentHost)
- `C:\Windows\System32\WindowsPowerShell\v1.0\profile.ps1` (AllUsers)

Measure each profile's overhead with:
```powershell
powershell.exe -NoProfile -Command "$sw=[System.Diagnostics.Stopwatch]::StartNew(); [do profile work]; $sw.Stop(); Write-Host $sw.ElapsedMilliseconds"
```

### Step 2: Find Conda/Miniconda Installation

Conda is often installed by tools like Pinokio in non-standard paths:
- `C:\pinokio\bin\miniconda\` (Pinokio-managed)
- `C:\Users\<user>\miniconda3\` (standard standalone install)
- `C:\ProgramData\miniconda3\` (system-level)

Run `conda --version` from PowerShell to find the active one.

### Step 3: Check System PATH for Dead Entries

```powershell
$paths = $env:Path -split ';'
foreach ($p in $paths) {
    if ($p -ne '' -and -not (Test-Path $p)) {
        Write-Host "DEAD: $p"
    }
}
```

Check both User and Machine PATH:
```powershell
[Environment]::GetEnvironmentVariable('Path', 'User')
[Environment]::GetEnvironmentVariable('Path', 'Machine')
```

## Common Fixes

### Conda Init Slow Startup (1500-2000ms)

**Problem:** The conda init hook in PowerShell profile runs `conda.exe shell.powershell hook` which starts Python, imports conda, generates module code. This costs ~1500ms on every shell start.

**Fix — Lazy-load the conda module:**

Replace the profile's conda init block with:
```powershell
# Lazy-init: first `conda` call loads the real module, then delegates to conda.exe
$Env:CONDA_EXE = "C:\path\to\miniconda3\Scripts\conda.exe"
$Env:_CONDA_ROOT = "C:\path\to\miniconda3"
$Env:_CONDA_EXE = $Env:CONDA_EXE

# Pre-pend conda to PATH so CLI tools work immediately
$condaPaths = 'C:\path\to\miniconda3', 'C:\path\to\miniconda3\Scripts', 'C:\path\to\miniconda3\Library\bin'
$Env:Path = ($condaPaths + ($Env:Path -split ';' | Where-Object { $_ })) -join ';'

# Lazy-init conda on first use
function conda {
    & $Env:CONDA_EXE shell.powershell hook | Out-String | ?{$_} | Invoke-Expression
    Remove-Item Function:conda -Force
    & conda @args
}
```

This drops startup overhead from ~1500ms to ~50ms.

### Disable Auto-Activate Base

Add `auto_activate_base: false` to `.condarc` to prevent conda from activating the base environment on init. Even with the lazy-load, this saves time when the module loads on first use.

### Conda Dependency Warnings

`RequestsDependencyWarning: urllib3 (2.7.0) or chardet/charset_normalizer doesn't match a supported version!`

Fix: Upgrade requests and charset-normalizer in the conda base environment:
```powershell
pip install --upgrade requests urllib3 charset-normalizer
```

### SSL_CERT_DIR Error on Conda Activation

`Remove-Item : Cannot find path 'Env:\SSL_CERT_DIR'`

Fix: Add `-ErrorAction SilentlyContinue` to the deactivate script at:
`<conda_root>\etc\conda\deactivate.d\openssl_deactivate-win.ps1`

Change line 6 from:
```powershell
Remove-Item -Path Env:\SSL_CERT_DIR
```
to:
```powershell
Remove-Item -Path Env:\SSL_CERT_DIR -ErrorAction SilentlyContinue
```

### Dead Activation Scripts from Uninstalled Software

Tools like Pinokio leave scripts in conda's activate.d/deactivate.d:
- `zz_pinokio_ffmpeg.ps1` — Sets FFMPEG env vars pointing to nonexistent paths
- `zz_pinokio_unset_ssl_cert_dir-win.ps1` — Unnecessary cleanup
- `zz_pinokio_*` variants (.bat, .sh, .ps1)

Delete these from `<conda_root>\etc\conda\activate.d\` and `<conda_root>\etc\conda\deactivate.d\`.

### Remove Dead PATH Entries

Dead entries in PATH cause Windows to probe nonexistent directories on every startup. Common culprits:
- `C:\pinokio\bin\miniconda\*` (uninstalled Pinokio)
- `C:\Program Files\Git\usr\local\bin` (doesn't exist in all Git installs)

Fix (requires admin for Machine PATH):
```powershell
$oldPath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
$dead = @('C:\dead\path\one', 'C:\dead\path\two')
$newParts = ($oldPath -split ';') | Where-Object {
    $keep = $true
    foreach ($d in $dead) { if ($_ -like $d) { $keep = $false } }
    $keep
}
[Environment]::SetEnvironmentVariable('Path', ($newParts -join ';'), 'Machine')
```

### Relocating Miniconda Without Copying 2GB

When you need to move a conda install but don't want to wait for a 2.4GB copy:

**Option A: Windows Directory Junction (instant)**
```powershell
# Remove incomplete partial copy first
rmdir /S /Q C:\Users\<user>\miniconda3

# Create junction (reparse point, not a copy)
New-Item -Path 'C:\Users\<user>\miniconda3' -ItemType Junction -Target 'C:\old\path\miniconda'
```

A junction is a reparse point — it looks like the real directory to all programs but the data stays at the original path. No data is moved. Update profiles and condarc to point at the junction path.

**Option B: robocopy (for actual relocation)**
```cmd
robocopy C:\old\path\miniconda C:\new\path\miniconda3 /E /R:2 /W:3
```
Then update profiles and delete the original. Slow on spinner drives.

### Conda PATH Escaping in PowerShell Profiles

When setting PATH in a PowerShell profile, use single-quoted arrays. Double-quoted strings interpret `\U` as an escape sequence:

```powershell
# WRONG — \U in path triggers escape parsing
$Env:Path = "C:\Users\scott\..." -split '...'

# RIGHT — single quotes avoid escape issues
$condaPaths = 'C:\path\one', 'C:\path\two'
$Env:Path = ($condaPaths + ($Env:Path -split ';' | Where-Object { $_ })) -join ';'
```

## Verification

After changes, measure startup time:
```powershell
powershell.exe -NoProfile -Command "Measure-Command { powershell.exe -Command 'exit' }"
```

Compare before and after. Target: under 200ms total startup overhead from profile scripts.

## References

- Conda init hook: `<conda_root>\\shell\\condabin\\Conda.psm1`
- Conda activate.d/deactivate.d: `<conda_root>\\etc\\conda\\activate.d\\`, `<conda_root>\\etc\\conda\\deactivate.d\\`
- Conda config file: `<conda_root>\\.condarc` or `%USERPROFILE%\\.condarc`
- PowerShell profile locations: `$PROFILE | Get-Member`
- `references/session-2026-06-07-fixes.md` — Full fix log from a real Pinokio+conda cleanup session
- `references/explorer-column-defaults-fix.md` — File Explorer column layout fix (Name wide, Type visible, no grouping)
- `scripts/fix-explorer-columns.ps1` — PowerShell script to reset folder views and set column defaults
