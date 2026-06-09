# Windows File Explorer Column Defaults Fix

## Problem

Windows Explorer defaults to grouped views for Music/Pictures/Videos folders. The Type column is never visible by default, Name is too narrow, and folders auto-group by Artist/Album on Music folders.

## Manual Fix (Quickest)

1. Open any folder (e.g., `C:\Users\<user>`)
2. Right-click column header → check **Type**
3. Drag **Name** column wider (400px+)
4. View → Options → Change folder and search options → View → **Apply to Folders**

This applies the current view settings to ALL folders of that type. Do once per folder type (Generic, Music, Pictures).

## Scripted Fix

See `scripts/fix-explorer-columns.ps1` — clears bag cache and sets Details view with Name (400px), Type (150px), Date Modified, Size. Run once per user:

```powershell
powershell -ExecutionPolicy Bypass -File fix-explorer-columns.ps1
```

## Registry Details

- Bag cache: `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\Bags`
- BagMRU: `HKCU\Software\Classes\Local Settings\Software\Microsoft\Windows\Shell\BagMRU`
- `ColInfo` binary value defines column layout per folder type
- Deleting AllFolders + BagMRU forces Windows to rebuild from default template

## Column Property IDs

| ID | Column |
|----|--------|
| 0  | Name |
| 1  | Size |
| 3  | Date Modified |
| 4  | Type |
| 14 | Date Created |
