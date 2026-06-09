---
name: reascript-ship-pipeline
description: "End-to-end pipeline to take a natural-language ReaScript idea to a shipped ReaPack package. Catches the 12 AI-generated bugs that models always miss: luac syntax check, Top Shelf validation, @provides filename fix, TrackFX_AddByName 4th param, non-existent reaper.* calls, and ReaPack packaging."
version: 1.0.0
author: Scott Mills / SGM Studios
license: MIT
metadata:
  hermes:
    tags: ["reascript", "reapack", "ship", "validation"]
    related_skills: ["reaper-lua-syntax", "reaper-validator", "gumroad-digital-product"]
---

# ReaScript Ship Pipeline

Run when the user says "ship this script", "validate [script]", "fix [script]", or wants to publish a ReaScript to ReaPack.

## Step 0: Register once, run forever (workflow fix)

The user's pain point: manually clicking Actions → New action → Browse every time.

**Fix:** Register each script ONCE via Actions → New action → Load ReaScript. After that, every edit just needs:

1. Edit the `.lua` file
2. Press `?` in REAPER, search script name, click **Run**
3. REAPER reads the file fresh every time — no re-registration needed

## Step 1: Syntax check with luac

Always run this first — it catches 95% of AI-generated syntax errors instantly:

```bash
luac -p path/to/script.lua
```

Silent output = clean. Error output = fix before even opening REAPER.

Common AI syntax errors to look for:
- `{8,32}` in a string pattern — Lua patterns don't support `{n,m}`. Replace with `%w+` and validate with `#var >= 8 and #var <= 32`
- Missing `end` — always check block closure
- Bare `function name()` instead of `local function name()` — every top-level function must be local
- `-- @provides [main] .` — the `.` must be the actual filename

## Step 2: Check @provides header

The most common shipping blocker. The `@provides` line MUST name the actual file, not `.`

```
-- @provides [main] SGM_auto_master.lua     ✓
-- @provides [main] .                        ✗ (ReaPack can't register this)
```

## Step 3: Check for non-existent reaper.* API calls

These are the top offenders that models invent:

| Fake API | Real API |
|----------|----------|
| `reaper.ClearConsole()` | `reaper.ShowConsoleMsg("")` — clearing requires printing blank lines |
| `reaper.file_exists()` | `io.open(path, "r")` and check result |
| `reaper.GetNumTracks()` | `reaper.CountTracks(0)` |
| `reaper.GetProjectPath("")` | `reaper.GetProjectPath("")` — this IS real but returns "" on unsaved projects |
| `reaper.TrackFX_AddByName(track, name, skipUI)` | MUST pass 4th param: `reaper.TrackFX_AddByName(track, name, skipUI, -1)` where -1 = create new |
| `reaper.ColorToNative(r,g,b)` | MUST `| 0x1000000` or SetTrackColor silently no-ops |

Search for these with:
```bash
rg "ClearConsole|file_exists|GetNumTracks|TrackFX_AddByName\([^,]+,[^,]+,[^,]+\)" path/to/script.lua
```

## Step 4: Run the Top Shelf 12 validator

Load the `reaper-validator` skill for the full checklist. For programmatic checking, run the validator script directly (it lives under the reaper-validator skill):

```bash
python "C:\Users\scott\AppData\Local\hermes\skills\reaper-reascripts\reaper-validator\scripts\validate-top-shelf.py" path/to/script.lua
```

This runs all 12 checks in one shot and returns JSON with pass/fail per check and a confidence score.

Manual walkthrough of all 12 checks:

1. State hygiene (Undo_BeginBlock + PreventUIFresh pair + cursor save)
2. ColorToNative | 0x1000000 on every SetTrackColor
3. Every GetUserInputs guarded with `if not ok then return end`
4. No global function leaks (`function` → `local function`)
5. ImGui context destroyed on ALL exit paths (paired Create/Destroy)
6. No gfx.showmenu (blocks score at 0.87 max)
7. Peak data guarded against empty/uncached
8. Track index refreshed after InsertTrackAtIndex
9. Item handles collected before SplitMediaItem/MoveMediaItem
10. OS-branched paths (no hardcoded C:\)
11. Early-return safety in defer loops
12. No stub/placeholder functions

## Step 5: Generate ReaPack index.xml

For scripts going into a repo, generate an index.xml entry. **CRITICAL: Use `<source>` tags with full URLs, NOT `<files><file>` relative paths.** The relative format silently fails when served from raw.githubusercontent.com — the index loads but no packages appear in Browse.

Correct format (verified working against ReaTeam, X-Raym, MPL repos):

```xml
<category name="Track">
  <reapack name="ScriptName" type="script" desc="Brief description">
    <version name="1.0.0" author="Scott Mills" time="2026-06-06T12:00:00Z">
      <changelog><![CDATA[+ Initial release]]></changelog>
      <source main="main">https://raw.githubusercontent.com/SGM-Studios/REPO_NAME/main/ScriptName.lua</source>
    </version>
  </reapack>
</category>
```

Key differences from the broken `<files><file>` format:
- `<source main="main">` replaces `<files><file name="...">`
- Full absolute URL (including branch) instead of relative filename
- Include `author="..."` attribute on `<version>` tag
- Use `<changelog><![CDATA[...]]></changelog>` instead of `<commit>`
- Use ISO 8601 datetime format for `time` attribute (`YYYY-MM-DDThh:mm:ssZ`)

## Step 6: Git commit and push

```bash
cd /path/to/repo
git add -A
git commit -m "Add ScriptName v1.0.0"
git push origin main
```

The raw.githubusercontent.com CDN caches for ~5 minutes. Test after that window.

## Quick reference: most common AI bugs

| Bug | Fix |
|-----|-----|
| `@provides [main] .` | Replace `.` with actual filename |
| `function name()` | Add `local` before `function` |
| `TrackFX_AddByName(t, n, false)` | Add `, -1` as 4th param |
| `string.match("{8,32}")` | Replace with `%w+` + length check |
| `reaper.ClearConsole()` | Remove or replace with console msg |
| `reaper.file_exists()` | Use `io.open` instead |
| Missing `local` on variables | Add `local` everywhere |
| `SetTrackColor` without `\| 0x1000000` | Add bit flag |
| Missing `UpdateArrange()` | Add after mutations |
| Plugin param values not normalized | TrackFX_SetParam takes 0-1 floats |
