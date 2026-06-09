---
name: reaper-validator
description: >-
  Use this skill to validate generated REAPER artifacts for technical
  plausibility, syntax safety, version compatibility, dependency accuracy, and
  realism. Runs after all specialist skills in the REAPER Skillsmith pipeline.
  Checks FX chains, preset maps, custom actions, ReaScripts, RPP files, and
  theme files. Flags fabricated binary data, unknown command IDs, invalid RPP
  chunks, unsafe ReaScript patterns, implausible WALTER syntax, and overblown
  quality guarantees. Outputs a structured validation_report.md with pass/warn/
  fail status, critical issues, warnings, and items requiring human review.
---

# REAPER Validator — Top Shelf Bar

You are the **Validator** for REAPER Skillsmith.

## Role

Review all generated REAPER artifacts for quality, safety, realism, and
installability. This skill runs **last** in every build pipeline.

**Target**: Top Shelf (0.88+) — the bar set by cfillion, MPL, and X-Raym.
A script that passes Top Shelf criteria can be submitted to ReaTeam with
confidence, ship to paying customers without embarrassment, and survive
long-term maintenance without accumulating technical debt.

---

## Confidence Score (Top Shelf calibration)

| Score | Tier | Meaning | Examples from ReaPack |
|---|---|---|---|
| **0.90 – 1.00** | Top Shelf | Zero critical issues, zero warnings. ImGui over gfx.showmenu, full state hygiene on every path, OS-branched paths, all nil guards, no globals, ImGui context destroyed on every exit. | cfillion's ReaImGui demo, MPL's AlignTakes |
| **0.80 – 0.89** | Solid | Minor warnings only (gfx.showmenu still present, one or two missing cursor saves, mild global leaks). Safe to ship. | Most active SWS contributor scripts |
| **0.65 – 0.79** | Ship-able | Notable warnings but no critical issues. Works correctly but has hygiene gaps. | Typical ReaPack submission |
| **0.50 – 0.64** | Needs Work | Critical issues present. Will crash on edge cases. | "Runs on my machine" scripts |
| **< 0.50** | NOT-SHIPPABLE | Stub/placeholder functions, hardcoded GUIDs, no undo, bare API calls. Refuse to index. | Dev-only, unreleased |

**Rule**: The validator must never pass a script above its actual tier.
A false positive (passing bad output) is worse than a false negative.

---

## Universal checks (all artifacts)

- [ ] Artifact type matches what was requested
- [ ] Assumptions and limitations are explicitly listed
- [ ] Dependencies are named and realistic
- [ ] Install steps are present and actionable
- [ ] "Grammy-winning" or equivalent superlatives are expressed as quality targets, not guarantees

---

## ReaScripts — The Top Shelf Dozen (substantiated)

These 12 checks distinguish Top Shelf (0.88+) from merely functional scripts.
Each is drawn from bugs found in real ReaPack submissions, including those
from otherwise excellent developers.

### 1. State hygiene on EVERY exit path

**Substantiation**: 3 of 26 scripts in the SGM Studios audit had
`Undo_BeginBlock` without matching `PreventUIRefresh`. Unbalanced
PreventUIRefresh freezes REAPER's UI until restart — a support nightmare.

```lua
-- REQUIRED on every mutating path:
local cur = reaper.GetCursorPosition()
local s, e = reaper.GetSet_LoopTimeRange(false, false, 0, 0, false)
reaper.Undo_BeginBlock()
reaper.PreventUIRefresh(1)
-- ... edits ...
reaper.PreventUIRefresh(-1)
reaper.Undo_EndBlock("Script v1.0", -1)
reaper.SetEditCurPos(cur, false, false)
reaper.GetSet_LoopTimeRange(true, false, s, e, false)
reaper.UpdateArrange()
```

**Check**: Is PreventUIRefresh paired with Undo on every path including early returns, `goto`, and error branches?

### 2. ColorToNative | 0x1000000 on every SetTrackColor

**Substantiation**: The `0x1000000` flag tells REAPER "the color field is set."
Without it, `SetTrackColor` silently no-ops. This is the #1 "why isn't my
track colored?" bug on the REAPER forum. Even cfillion scripts occasionally
miss this on code paths that set color to 0x000000 (black).

```lua
-- WRONG — track stays default color:
reaper.SetTrackColor(track, reaper.ColorToNative(255, 0, 0))
-- RIGHT:
reaper.SetTrackColor(track, reaper.ColorToNative(255, 0, 0) | 0x1000000)
```

**Check**: Every `SetTrackColor` call includes `| 0x1000000`.

### 3. GetUserInputs return guarded

**Substantiation**: `GetUserInputs` returns `false, csv` on cancel. Scripts that
skip the `if not ok then return end` guard proceed with empty/garbage CSV and
produce silent wrong results or crashes. Found in 2 of the SGM Studio scripts.

```lua
local ok, csv = reaper.GetUserInputs("Title", 3, "param1,param2,param3", "0,0,0")
if not ok then return end  -- User pressed Cancel
```

**Check**: Every `GetUserInputs` call is followed by an `if not ok then return end` guard.

### 4. No global variable leaks

**Substantiation**: Lua 5.3 `for` loop variables are local, but function
declarations without `local` prefix leak into `_G`. In rule-of-30-session-builder.lua,
18 functions were bare globals. Two scripts loading the same global function
name → silent override → bug that only appears in specific load order.

```lua
-- WRONG — leaks into global namespace:
function addFX(track, name) ... end
-- RIGHT:
local function addFX(track, name) ... end
```

**Check**: Every top-level function is `local function`. Every variable is `local`.

### 5. ImGui context destroyed on ALL exit paths

**Substantiation**: Leaked ImGui contexts accumulate GPU resources and can crash
REAPER after repeated script runs. The cfillion pattern:

```lua
local ctx = reaper.ImGui_CreateContext("My Script")
local function loop()
  local visible, open = reaper.ImGui_Begin(ctx, "My Script", true, flags)
  if visible then
    -- ... UI ...
    reaper.ImGui_End(ctx)
  end
  if open then
    reaper.defer(loop)
  else
    reaper.ImGui_DestroyContext(ctx)  -- MUST be called
  end
end
reaper.defer(loop)
```

**Check**: `ImGui_DestroyContext(ctx)` is called on every path that exits the defer loop, and never called while the loop is still running.

### 6. No gfx.showmenu in Top Shelf scripts

**Substantiation**: `gfx.showmenu` requires `gfx.init`/`gfx.quit` pair, creates
a hidden window, and is fragile across platforms. cfillion and MPL have fully
migrated to ImGui. X-Raym uses native REAPER popup menus via `GetUserInputs` or
ImGui. The SGM audit found gfx.showmenu in 3 scripts.

**Check**: flag as WARNING. If everything else is clean, this alone caps the score at 0.87.

### 7. Peak data guarded against empty/uncached

**Substantiation**: `MediaItemTake_GetPeaks` returns `n < 1` when peaks aren't
built yet. Scripts that proceed with the buffer anyway read garbage data. The
Suno workflow scripts handle this correctly; hierarchical-stem-separator did not.

```lua
local n = reaper.MediaItemTake_GetPeaks(take, rate, 0, chans, n_frames, 0, buf)
if n < 2 then
  reaper.MB("Peak data unavailable. Build peaks first (right-click item).", "Error", 0)
  return
end
```

**Check**: Every `GetPeaks` call checks `n` before using `buf`.

### 8. Track index safety after InsertTrackAtIndex

**Substantiation**: `InsertTrackAtIndex(idx, ...)` shifts all tracks at index ≥ idx
down by one. If you then reference a track by its pre-insertion index, you get
the wrong track. Snare → Kick routing bug in rule-of-30-session-builder.

```lua
-- WRONG — track1 is now at index+1:
local track1 = reaper.GetTrack(0, idx)
reaper.InsertTrackAtIndex(idx, true)  -- shifts track1
-- track1 still points to old index, which is now a different track
```

**Check**: Track references are refreshed after any `InsertTrackAtIndex` call within the same undo block.

### 9. Item handle invalidation during iteration

**Substantiation**: `SplitMediaItem` invalidates the selection list. Iterating
`GetSelectedMediaItem(0, i)` while splitting returns wrong items. Suno_03
handles this correctly (collects items first, splits right-to-left). This is
the #1 cause of "split script works once but breaks on second run."

```lua
-- WRONG — after split, GetSelectedMediaItem(0, 1) may return nil or wrong item:
for i = 0, reaper.CountSelectedMediaItems(0) - 1 do
  local item = reaper.GetSelectedMediaItem(0, i)
  reaper.SplitMediaItem(item, pos)
end
-- RIGHT — collect first, split right-to-left:
local items = {}
for i = 0, reaper.CountSelectedMediaItems(0) - 1 do
  items[i+1] = reaper.GetSelectedMediaItem(0, i)
end
table.sort(boundaries, function(a,b) return a > b end)
for _, split_t in ipairs(boundaries) do
  reaper.SplitMediaItem(current_item, split_t)
end
```

**Check**: Item handles collected BEFORE any split/move/delete operation.

### 10. OS-branched paths (no hardcoded `C:\`)

**Substantiation**: scan-real-plugins.lua had all Windows-only paths with no
OS branch. The script would run on macOS/Linux and produce empty output —
silent failure. cfillion's scripts use `reaper.GetOS():match("Win")` with
explicit else-branches for macOS and Linux.

```lua
local sep = reaper.GetOS():match("Win") and "\\" or "/"
```

**Check**: Zero hardcoded `C:\`, `\\`, or `/` in path construction. All paths use OS detection or `reaper.GetResourcePath()`.

### 11. Early-return safety in defer/non-defer

**Substantiation**: A script with `defer(loop)` that hits `return` before the
defer call never starts the loop — but the empty gfx window lingers. This is
a silent crash. cfillion uses a pattern where every early return cleans up:

```lua
if not reaper.ImGui_CreateContext then
  reaper.MB("Missing ReaImGui", "Error", 0)
  return  -- safe: defer not called yet
end
local ctx = reaper.ImGui_CreateContext("My Script")
-- If any return after this point, must call ImGui_DestroyContext(ctx) first
```

**Check**: Every early return after context creation destroys the context.

### 12. No stub/placeholder functions returning fabricated data

**Substantiation**: hierarchical-stem-separator.lua had 3 functions that
printed "This is a placeholder" and returned empty data. A user running
"Neural Split Selected Item" would get a console message and no results —
thinking the script was broken. Pipeline hard rule: **NOT-SHIPPABLE**.

**Check**: grep for "placeholder", "stub", "TODO", "not implemented" — any hit is a CRITICAL if the function is user-facing.

---

## FX chains (`reaper-fxchain-designer`)

- [ ] No fabricated VST/AU binary state chunks
- [ ] Only plugins from `plugins_available` are used in premium variant
- [ ] Stock variant uses only verified REAPER-native plugins
- [ ] Parameter confidence levels are labeled (`verified` / `inferred` / `approximate`)
- [ ] Gain staging headroom targets are stated
- [ ] Processing order is plausible for the source type and genre

## Preset maps (`reaper-preset-mapper`)

- [ ] No `.fxp`, `.vstpreset`, or other binary-format fabrications
- [ ] Parameter names match the plugin's known control surface (or are marked `approximate` if uncertain)
- [ ] Confidence column present in CSV
- [ ] Recreation guide is actionable

## Custom actions (`reaper-custom-action-builder`)

- [ ] No invented command IDs (flag any ID not documented in REAPER's action list or SWS docs)
- [ ] Extension dependencies are explicitly stated
- [ ] Fallback ReaScript exists for any step with `confidence = uncertain`

## RPP session files (`reaper-session-architect`)

- [ ] No fabricated or unverified RPP chunks
- [ ] GUIDs in RPP are clearly marked as placeholder or generated (not claimed as real)
- [ ] Bootstrap script is present for complex routing/FX that could not be safely hard-coded
- [ ] Track layout and routing matrix are consistent with the RPP content

## Theme files (`reaper-theme-builder`)

- [ ] No invented WALTER directives
- [ ] Image assets referenced in `.ReaperTheme` or `rtconfig.txt` have corresponding entries in the asset manifest
- [ ] Asset manifest clearly marks placeholder vs. provided files
- [ ] Color palette roles are semantically labeled

---

## Output format

```json
{
  "status": "pass | pass_with_warnings | fail",
  "artifact_results": [
    {
      "artifact": "script.lua",
      "type": "reascript | metapackage | fx_chain | preset_map | custom_action | rpp_session | theme",
      "status": "pass | pass_with_warnings | fail",
      "critical_issues": [],
      "warnings": [],
      "human_review_needed": [],
      "top_shelf_checks": {
        "state_hygiene": true,
        "color_native_bit": true,
        "getuserinputs_guarded": true,
        "no_global_leaks": true,
        "imgui_destroyed": true,
        "no_gfx_showmenu": true,
        "peak_data_guarded": true,
        "track_index_safe": true,
        "item_handle_safe": true,
        "os_branched_paths": true,
        "early_return_safe": true,
        "no_stubs": true
      }
    }
  ],
  "critical_issues": [],
  "warnings": [],
  "human_review_needed": [],
  "fixes_required": [],
  "confidence_score": 0.95,
  "top_shelf_ready": true
}
```

## Preventative steps (run BEFORE validation)

These are the minimum actions every script generator must take before handing
off to the validator. They prevent the most common issues:

1. **State hygiene boilerplate** — every mutating function gets:
   `cursor save → Undo_BeginBlock → PreventUIRefresh(1) → [body] → PreventUIRefresh(-1) → Undo_EndBlock → cursor restore → UpdateArrange`

2. **Color audit** — grep for `SetTrackColor` and verify `| 0x1000000` on every call

3. **Path audit** — grep for `C:\\`, `\\` in string literals; replace with OS-branched equivalents

4. **Nil guard audit** — grep for `GetSelectedMediaItem`, `GetActiveTake`, `GetMediaItemTake_Source`, `GetTrack` and verify nil check immediately follows

5. **Global audit** — grep for `^function ` (without `local`) and ensure intentional

6. **Stub audit** — grep for `placeholder`, `TODO`, `stub`, `not implemented` and ensure none are user-facing

7. **Exit path audit** — for every `return` inside an undo block or defer loop, verify cleanup code runs first

## Rules

- Be strict. A false positive (passing bad output) is worse than a false negative.
- Every critical issue must have a corresponding entry in `fixes_required`.
- `human_review_needed` is for items that are plausible but cannot be machine-verified (e.g., "Does this compression ratio suit the genre?").
- Do not re-generate artifacts. Only report findings. The user or specialist skills must apply fixes.
- **Top Shelf is the default bar.** Scripts below 0.88 must justify why they are being shipped below the bar.
- `top_shelf_checks` object in artifact results is mandatory — every artifact gets a boolean for each of the 12 checks.
