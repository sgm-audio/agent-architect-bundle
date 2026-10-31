# Session 2026-06-07 — Specific Fixes Applied

## Environment

- OS: Windows 10
- Shell: PowerShell 7 + Windows PowerShell 5
- Miniconda: installed by Pinokio at `C:\pinokio\bin\miniconda\`
- Pinokio: uninstalled by user, but conda/scripts remained

## Errors Found

### Error 1: PowerShell startup 3500ms+
**Root cause:** Both PS5 and PS7 profiles ran `conda.exe shell.powershell hook` which starts Python, imports conda, generates module code. Each call: ~1800ms.

**Fix applied:** Replaced conda init hook with lazy-load function. New profile overhead: ~54ms.
- Set env vars immediately (CONDA_EXE, _CONDA_ROOT, _CONDA_EXE)
- Pre-pend conda paths to PATH
- Define `function conda` that calls the real hook on first use, then removes itself and delegates to conda.exe

### Error 2: SSL_CERT_DIR error every shell start
**Root cause:** `openssl_deactivate-win.ps1` line 6: `Remove-Item -Path Env:\SSL_CERT_DIR` without `-ErrorAction SilentlyContinue`. Fired when `__CONDA_OPENSSL_CERT_DIR_SET` was "1" but `SSL_CERT_DIR` env var was already removed.

**Fix:** Added `-ErrorAction SilentlyContinue` to the `Remove-Item` call.

### Error 3: RequestsDependencyWarning (urllib3/charset mismatch)
**Root cause:** urllib3 2.7.0 installed, but requests 2.32.3 was packaged expecting a different version range.

**Fix:** `pip install --upgrade requests urllib3 charset-normalizer` — upgraded requests to 2.34.2, warning disappeared.

### Error 4: 8 dead Pinokio paths in System PATH
**Dead entries removed from Machine PATH:**
- `C:\pinokio\bin\miniconda`
- `C:\pinokio\bin\miniconda\Scripts`
- `C:\pinokio\bin\miniconda\condabin`

**Dead entries found in PATH (via junction):**
- `C:\pinokio\bin\ffmpeg-env\Library\bin`
- `C:\pinokio\bin\miniconda\Library\mingw64\bin`
- `C:\pinokio\bin\miniconda\Library\mingw-w64\bin`
- `C:\pinokio\bin\miniconda\Library\usr\bin`
- `C:\pinokio\bin\miniconda\Library\bin`
- `C:\pinokio\bin\miniconda\bin`

### Error 5: Pinokio activation scripts
**Scripts deleted from `<conda_root>\etc\conda\activate.d\`:**
- `zz_pinokio_ffmpeg.ps1` — Set ffmpeg paths to nonexistent `C:\pinokio\bin\ffmpeg-env`
- `zz_pinokio_ffmpeg.bat`
- `zz_pinokio_ffmpeg.sh`
- `zz_pinokio_unset_ssl_cert_dir-win.ps1`
- `zz_pinokio_unset_ssl_cert_dir-win.bat`
- `zz_pinokio_unset_ssl_cert_dir-win.sh`

**Scripts deleted from `<conda_root>\etc\conda\deactivate.d\`:**
- `zz_pinokio_ffmpeg.ps1`
- `zz_pinokio_ffmpeg.bat`
- `zz_pinokio_ffmpeg.sh`

### Error 6: PowerShell profile PATH escaping
**Root cause:** Using double-quoted strings for PATH with `\U` in path (e.g., `\Users`) triggered PowerShell escape sequence parsing.

**Fix:** Switched to single-quoted arrays: `$condaPaths = 'C:\path\one', 'C:\path\two'`

## Relocation Details

Used Windows directory junction (reparse point) to avoid copying 2.4GB:
```powershell
New-Item -Path 'C:\Users\<user>\miniconda3_NEW' -ItemType Junction -Target 'C:\pinokio\bin\miniconda'
```

Failed approaches:
- `mv` in git-bash: Permission denied
- `shutil.copytree` via Python: timed out at 120s
- `Copy-Item` via PowerShell: killed at 162s (2.4GB on laptop spinner)
- `robocopy`: hung silently
- `rmdir /S /Q` on partial copy: hit long-path torch files, "system cannot find the file specified"

## Timing Measurements

| Operation | Before | After |
|---|---|---|
| Conda init hook | 1464-1816ms | 54ms (lazy-load) |
| SSL_CERT_DIR error | Every shell start | Gone |
| Total profile overhead | ~3500ms (both profiles) | ~54ms |
| RequestsDependencyWarning | Every conda call | Gone |

## Files Modified

- `C:\Users\<user>\OneDrive\Documents\PowerShell\profile.ps1` (PS7)
- `C:\Users\<user>\OneDrive\Documents\WindowsPowerShell\profile.ps1` (PS5)
- `C:\pinokio\bin\miniconda\.condarc` (added `auto_activate_base: false`, updated paths)
- `C:\\pinokio\\bin\\miniconda\\etc\\conda\\deactivate.d\\openssl_deactivate-win.ps1` (added ErrorAction)
- System PATH (Machine) — removed 3 dead entries

## File Explorer Column Fix (Post-Conda Cleanup)

The user reported constant frustration with:
- Name column too narrow (must resize every folder)
- Type column never visible by default (must manually add)
- Music folders auto-grouped by Artist/Album

Script solution: `scripts/fix-explorer-columns.ps1` — clears the folder view cache (BagMRU + Bags registry keys) and sets a default column layout with Name (400px), Type (150px), Date Modified (150px), Size (100px). The key insight: `ColInfo` is a binary registry value defining column layout, and clearing BagMRU forces Windows to rebuild from the AllFolders template.

Manual fallback if the registry approach doesn't stick: View → Options → View → Apply to Folders from any Details-mode folder.
