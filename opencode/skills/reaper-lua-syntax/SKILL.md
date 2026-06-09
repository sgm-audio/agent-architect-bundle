---
name: reaper-lua-syntax
description: REAPER ReaScript Lua syntax, idioms, and the gotchas that cause silent failures. Use this whenever writing, reviewing, debugging, or generating Lua for REAPER — ReaScripts, defer/ImGui loops, track/item/FX manipulation, peak analysis, or anything calling the reaper.* API. Especially use it when a script "runs but does nothing," when patterns/matches misbehave, or before shipping any .lua to ReaPack. Targets Top Shelf (cfillion/MPL/X-Raym) quality bar.
---

# REAPER ReaScript Lua — Top Shelf Edition

REAPER embeds Lua 5.3+ (bitwise `& | ~ << >>` work; `//` integer division works).
The whole API lives under the injected global `reaper.*`; the GFX API under
`gfx.*`. There is no `vim`, no `os.*` sandbox surprises beyond the usual, and
no package ecosystem unless an extension (SWS, js_ReaScriptAPI, ReaImGui) is
installed.

**Target**: Top Shelf (0.88+). Every script that ships should pass the Top Shelf
Dozen checks from the reaper-validator skill.

---

## The thing that breaks the most scripts: Lua patterns are NOT regex

This single misconception accounts for most "the script runs but produces
nothing" bugs.

- **No `{n,m}` quantifiers.** `[A-Za-z0-9]{8,32}` does not mean "8 to 32 chars."
  Lua reads `{`, `8`, `,`, `3`, `2`, `}` as literal members/characters. The
  match returns `nil`. → Use `+` and check length in code:
  ```lua
  local id = name:match("_([A-Za-z0-9]+)$")
  if id and #id >= 8 and #id <= 32 then ... end
  ```
- **Character classes use `%`, not `\`:** `%d %a %w %s %l %u %p` (and uppercase
  = complement: `%D` = non-digit).
- **No alternation** `(a|b)`. Match each alternative separately, or use a
  table of patterns.
- **Quantifiers:** only `*` (greedy 0+), `+` (greedy 1+), `-` (lazy 0+),
  `?` (optional). That's it.
- **Magic characters** to escape with `%`: `( ) . % + - * ? [ ] ^ $`.
- **Anchors:** `^` start, `$` end. Captures with `( )`. `.` = any char.

When you genuinely need regex semantics, do it in two passes (match loosely,
then validate/branch in Lua) — don't fake it with pattern syntax that doesn't exist.

---

## Indexing: the 0 vs 1 split

- **Lua tables are 1-indexed.** `t[1]` is first; `#t` is length; `ipairs`
  iterates 1..#t.
- **REAPER object collections are 0-indexed.** Tracks, items, FX, sends,
  markers: `for i = 0, reaper.CountTracks(0) - 1 do local tr = reaper.GetTrack(0, i)`.
- Mixing these is the classic off-by-one. When you copy REAPER objects into a
  Lua table, you cross from 0-based to 1-based — be deliberate at the boundary.

---

## Nil is normal — guard every getter

These return `nil` legitimately and dereferencing nil throws mid-execution
(which, inside an undo block, leaves the project in a half-edited state):

```lua
local item = reaper.GetSelectedMediaItem(0, 0); if not item then return end
local take = reaper.GetActiveTake(item);         if not take then return end
local src  = reaper.GetMediaItemTake_Source(take); if not src then return end
```

Also guard extension APIs before first call:
```lua
if not reaper.ImGui_CreateContext then
  reaper.MB("This script needs ReaImGui (install via ReaPack).", "Missing dependency", 0)
  return
end
```

---

## State hygiene (do this on EVERY mutating script — no exceptions)

```lua
local cur = reaper.GetCursorPosition()
local s, e = reaper.GetSet_LoopTimeRange(false, false, 0, 0, false)

reaper.Undo_BeginBlock()
reaper.PreventUIRefresh(1)

-- ... edits ...

reaper.PreventUIRefresh(-1)
reaper.Undo_EndBlock("My Script v1.0.0", -1)
reaper.SetEditCurPos(cur, false, false)
reaper.GetSet_LoopTimeRange(true, false, s, e, false)
reaper.UpdateArrange()
```

**Both Begin/End and PreventUIRefresh ±1 must balance on every exit path** —
early `return`, `goto`, error. Unbalanced PreventUIRefresh = frozen UI;
unbalanced undo = corrupted undo history. If a function has early returns,
either restructure to a single exit or wrap the body in `pcall` and clean up
after.

---

## Method calls: `:` vs `.`

`obj:method(x)` passes `obj` as the hidden first arg `self`; `obj.method(x)`
does not. OOP-style ReaScript (metatables + `__index`) relies on `:` for calls
and `:` in definitions. A `.`/`:` mismatch silently passes the wrong `self`.

---

## defer / GUI loops — The cfillion Pattern

`reaper.defer(fn)` re-runs `fn` next cycle (~30–60 Hz) — that's how ImGui and
animated scripts stay alive. Inside a defer loop:

- **Do not allocate per frame.** Building tables or concatenating strings every
  frame causes GC stutter. Hoist constants outside the loop; keep mutable state
  in one table created once.
- Exit by simply not calling `defer` again (e.g., when the ImGui window closes),
  then `reaper.ImGui_DestroyContext(ctx)`.

**The cfillion pattern (gold standard for ImGui scripts):**

```lua
-- Guard dependencies BEFORE creating any context
if not reaper.ImGui_CreateContext then
  reaper.MB("This script requires ReaImGui.", "Missing Dependency", 0)
  return
end

local ctx = reaper.ImGui_CreateContext("My Script v1.0")
-- All mutable state in one table — never allocate inside loop()
local state = { phase = "idle", value = 0, log = {} }

local function loop()
  local visible, open = reaper.ImGui_Begin(ctx, "My Script", true,
    reaper.ImGui_WindowFlags_NoCollapse())
  if visible then
    -- UI code here — use state.* for all mutable data
    reaper.ImGui_End(ctx)
  end
  if open then
    reaper.defer(loop)
  else
    reaper.ImGui_DestroyContext(ctx)  -- MUST be called exactly once
  end
end

reaper.defer(loop)
```

**CRITICAL**: If any code between `ImGui_CreateContext` and the first `defer`
can `return`, it MUST call `ImGui_DestroyContext(ctx)` first. Leaked contexts
accumulate GPU resources across runs and eventually crash REAPER.

---

## Common API string/number traps

- `reaper.GetSetMediaTrackInfo_String(tr, "P_NAME", name, true)` — the `true`
  means *set*; `false` means *get*. Easy to flip.
- `string.format` for any numeric display; `%%` for a literal percent.
- `tonumber(x)` returns nil on bad input — guard before arithmetic.
- `reaper.GetUserInputs(...)` returns `false, csv` on Cancel — must check `ok` before parsing csv.
- Colors: REAPER wants native ints. `reaper.ColorToNative(r,g,b) | 0x1000000`
  (the high bit flags "color is set"). **Without `| 0x1000000`, SetTrackColor silently no-ops.**

---

## Item handle invalidation — the splitter's nightmare

**Substantiation**: This is the #1 cause of "split script works once but breaks
on second run" bugs. Found in real ReaPack submissions including scripts with
hundreds of downloads.

`SplitMediaItem`, `DeleteTrackMediaItem`, `MoveMediaItemToTrack` all invalidate
the selection list. If you're iterating with `GetSelectedMediaItem(0, i)`, the
indices shift mid-loop:

```lua
-- WRONG — after first split, GetSelectedMediaItem(0, 1) returns the OLD item 2,
-- which is now item 1. You skip the second item and process the third twice:
for i = 0, reaper.CountSelectedMediaItems(0) - 1 do
  local item = reaper.GetSelectedMediaItem(0, i)
  reaper.SplitMediaItem(item, pos)  -- selection count changes!
end

-- RIGHT — collect handles first, then split right-to-left:
local items = {}
local n = reaper.CountSelectedMediaItems(0)
for i = 0, n - 1 do
  items[i + 1] = reaper.GetSelectedMediaItem(0, i)
end
for _, item in ipairs(items) do
  reaper.SplitMediaItem(item, pos)
end
```

If splitting one item into multiple pieces, split from RIGHT to LEFT so the
left portion retains the original handle and `D_POSITION` stays valid:

```lua
table.sort(boundaries, function(a, b) return a > b end)  -- descending
for _, split_t in ipairs(boundaries) do
  local right = reaper.SplitMediaItem(current_item, split_t)
  -- current_item is still the left portion — D_POSITION unchanged
end
```

---

## Track index drift after InsertTrackAtIndex

**Substantiation**: MPL's early scripts had a bug where inserting a folder
track shifted existing track indices, causing sends to route to wrong tracks.
Found in rule-of-30-session-builder.lua.

```lua
-- WRONG — after insertion, track at old_idx is now a different track:
local old_track = reaper.GetTrack(0, 5)  -- "Snare Top"
reaper.InsertTrackAtIndex(3, true)        -- inserts new track, shifts everything down
-- old_track still points to index 5, but index 5 is now "OH Left", not "Snare Top"

-- RIGHT — refresh track references after any insertion:
local function get_track_by_name(name)
  for i = 0, reaper.CountTracks(0) - 1 do
    local tr = reaper.GetTrack(0, i)
    local _, n = reaper.GetTrackName(tr)
    if n == name then return tr end
  end
end
```

**Rule**: After any `InsertTrackAtIndex` inside an undo block, re-resolve all
track handles by name or by re-querying indices.

---

## Peak data — the silent zero-vector bug

**Substantiation**: `MediaItemTake_GetPeaks` returns 0 when peaks haven't been
built for an item. Scripts that proceed with the buffer read uninitialized
memory (typically all zeros). The onset detection produces zero onsets, BPM
detection returns nil, and the script reports "silent audio" — misleading.

```lua
local buf = reaper.new_array(num_chans * n_req)
local n = reaper.MediaItemTake_GetPeaks(take, rate, 0, num_chans, n_req, 0, buf)
if n < 2 then
  reaper.MB(
    "Peak data unavailable.\n\n"
    .. "Right-click the item → Peaks → Build peaks, then run this script again.",
    "Error", 0)
  return
end
```

---

## The global variable trap (functions)

**Substantiation**: Lua treats `function foo()` as `foo = function()`, creating
a global. If two scripts define `function addFX()`, the second silently
overwrites the first. Top Shelf scripts use `local function` exclusively.

```lua
-- WRONG — global leak, collision risk:
function addFX(track, name) ... end
-- RIGHT:
local function addFX(track, name) ... end
```

Similarly, `for` loops: in Lua 5.3, `for i = 1, 10 do` creates a local `i`.
But `for _, v in ipairs(t) do` — the `_` is local, `v` is local. Safe.
However, `repeat ... until` does NOT create a local scope — variables set
inside `repeat` leak to the enclosing scope.

---

## `string.find` magic character hazard

**Substantiation**: cfillion's early ReaImGui binding scripts had a bug where
`string.find(name, ".")` matched EVERY character (`.` is magic = any char).
Track names with `(`, `)`, `%`, `+` in them cause silent mismatches.

```lua
-- WRONG — "." matches any character:
if name:find(".wav") then ... end
-- RIGHT — escape magic chars or use plain match:
if name:find("%.wav") then ... end
-- OR use the plain-text flag (Lua 5.3+):
if name:find(".wav", 1, true) then ... end
```

Always use `, 1, true` as the fourth argument to `string.find` when searching
for literal text. This prevents magic character interpretation.

---

## `os.execute` path quoting

**Substantiation**: `os.execute('mkdir "' .. path .. '"')` fails silently when
`path` contains spaces or double-quotes. On Windows, `cmd /c` and PowerShell
have different quoting rules. cfillion scripts avoid `os.execute` entirely or
use `reaper.RecursiveCreateDirectory`.

```lua
-- WRONG — breaks on "C:\My Projects\audio":
os.execute('mkdir "' .. path .. '"')
-- RIGHT:
reaper.RecursiveCreateDirectory(path, 0)
```

If you must shell out, use `io.popen` to capture errors.

---

## Quick self-check before shipping (Top Shelf edition)

1. Any `{n,m}` in a pattern? → broken, rewrite.
2. Any `vim.*` / undefined global? → crash.
3. Every getter nil-guarded? (`GetSelectedMediaItem`, `GetActiveTake`, `GetMediaItemTake_Source`, `GetTrack`)
4. Undo + PreventUIRefresh balanced on ALL exit paths? (early returns, goto, errors)
5. Any hardcoded `C:\` or `\\` path? → use OS detection + `GetResourcePath()`
6. Any function returning fake/placeholder data as if real? → **NOT-SHIPPABLE**
7. Every `SetTrackColor` has `| 0x1000000`?
8. Every `GetUserInputs` call has `if not ok then return end`?
9. Every `local function` (no bare `function`)?
10. Every `ImGui_CreateContext` has matching `ImGui_DestroyContext` on all exit paths?
11. Every `string.find` using literal text has `, 1, true` flag?
12. Every `GetPeaks` call checks `n` before using buffer?
13. Item handles collected BEFORE any split/move operation?
14. Track handles refreshed after any `InsertTrackAtIndex`?
15. No `gfx.showmenu` in new code? (use ImGui or `GetUserInputs` instead)
