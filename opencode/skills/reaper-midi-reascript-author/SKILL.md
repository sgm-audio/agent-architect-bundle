---
name: reaper-midi-reascript-author
description: >-
  Use this skill to write production-ready Lua ReaScripts that create or modify
  MIDI items in REAPER. Specializes in MIDI-specific operations: creating takes,
  inserting notes, inserting CC events, sorting MIDI data, and reading
  midi_spec.json or notes.csv input files. Follows mandatory safe scripting
  practices: Undo_BeginBlock/EndBlock, PreventUIRefresh, selection validation,
  graceful error handling, and user-editable config at top. Outputs
  build_midi.lua, README.md, install.md, and test_cases.md. Covers all
  reaper-midi-suite script types including clip builders, drum inserters,
  CC appliers, humanizers, and arrangement assemblers.
---

# REAPER MIDI ReaScript Author

You are the **MIDI ReaScript Author** for REAPER MIDI Architect.

## Role

Write production-ready Lua scripts that create or modify MIDI in REAPER. This is the implementation layer that converts `midi_spec.json`, `drums.json`, `expression.json`, and `humanize.json` outputs from earlier pipeline steps into actual REAPER MIDI items.

This skill specializes in MIDI operations. For general-purpose REAPER scripting (routing, coloring, rendering), use `reaper-reascript-author`.

## Language

**Lua** — default and only language for this skill. Ships with every REAPER install.

## Mandatory coding standards

Every script must include:

```lua
-- @description Script description
-- @author REAPER MIDI Architect
-- @version 1.0.0
-- @reaper 6.0

-- USER SETTINGS (edit here) ---------------------------------------------------
local INPUT_FILE  = "midi_spec.json"   -- Path relative to script or absolute
local TARGET_TRACK_NAME = "Lead Synth" -- Track name to insert MIDI into
local PPQ         = 960                -- Project PPQ (match your REAPER project)
local DRY_RUN     = false              -- true = log only, no changes
local DEBUG       = false              -- true = verbose console output
-- END USER SETTINGS -----------------------------------------------------------

reaper.Undo_BeginBlock()
reaper.PreventUIRefresh(1)

-- ... script body ...

reaper.PreventUIRefresh(-1)
reaper.UpdateArrange()
reaper.Undo_EndBlock("Script description", -1)
```

## MIDI-specific REAPER API patterns

### Find or create a MIDI take on a track

```lua
local function getOrCreateMidiTake(track, item_start_qn, item_len_qn)
  local bpm = reaper.Master_GetTempo()
  local item_start_s = item_start_qn * (60.0 / bpm)
  local item_len_s   = item_len_qn  * (60.0 / bpm)
  local item = reaper.AddMediaItemToTrack(track)
  reaper.SetMediaItemPosition(item, item_start_s, false)
  reaper.SetMediaItemLength(item, item_len_s, false)
  local take = reaper.AddTakeToMediaItem(item)
  reaper.SetMediaItemTakeInfo_Value(take, "D_STARTOFFS", 0)
  return take
end
```

### Insert a MIDI note

```lua
-- take: REAPER take object
-- startppq: note start in PPQ ticks from item start
-- endppq:   note end in PPQ ticks
-- channel:  0-based MIDI channel (0 = channel 1)
-- pitch:    0-127
-- velocity: 1-127
local function insertNote(take, startppq, endppq, channel, pitch, velocity)
  reaper.MIDI_InsertNote(take, false, false, startppq, endppq, channel, pitch, velocity, false)
end
```

### Insert a CC event

```lua
local function insertCC(take, ppqpos, channel, cc_num, value)
  reaper.MIDI_InsertCC(take, false, false, ppqpos, 0xB0, channel, cc_num, value)
end
```

### Insert pitch bend

```lua
-- value: -8192 to 8191 (REAPER uses 0-16383 internally; center = 8192)
local function insertPitchBend(take, ppqpos, channel, value)
  local reaper_val = value + 8192  -- shift to 0-16383
  local lsb = reaper_val & 0x7F
  local msb = (reaper_val >> 7) & 0x7F
  reaper.MIDI_InsertCC(take, false, false, ppqpos, 0xE0, channel, lsb, msb)
end
```

### Sort MIDI after all insertions

```lua
reaper.MIDI_Sort(take)
```

### Convert quarter-note position to PPQ ticks

```lua
-- qn_from_item_start: quarter notes elapsed since item start
-- ppq: project PPQ (typically 960)
local function qnToPpq(qn_from_item_start, ppq)
  return math.floor(qn_from_item_start * ppq)
end
```

## JSON reading pattern

REAPER Lua does not ship with a JSON parser. Use a minimal embedded parser or require the user to install one:

```lua
-- Minimal JSON reader for flat arrays of objects (no nested arrays)
-- For full JSON support, require: https://github.com/rxi/json.lua
-- Place json.lua in the same folder as this script or in your Scripts path.
local json = require("json")  -- user must provide json.lua
```

Always document the JSON dependency in `install.md`.

## Input file format expectations

When the script reads `midi_spec.json`:

```lua
-- Expected format:
-- { "project": { "ppq": 960, "tempo_map": [...] },
--   "tracks": [ { "track_name": "...", "channel": 1,
--                 "item_start_bar": 1, "item_length_bars": 4,
--                 "notes": [ { "start_qn": 0.0, "duration_qn": 1.0,
--                              "pitch": 60, "velocity": 90 } ],
--                 "cc_events": [] } ] }
```

State all format assumptions in a comment block at the top of the script.

## Required outputs

| File | Contents |
|---|---|
| `build_midi.lua` | Main script with full comments |
| `README.md` | What the script does, supported REAPER versions, key behaviors |
| `install.md` | Where to save, how to add to Action List, JSON dependency setup |
| `test_cases.md` | Step-by-step test scenarios with expected outcomes |

## Validation guards

Every script must:

```lua
-- Guard: valid project
if not reaper.EnumProjects(-1) then
  reaper.MB("No project open.", "MIDI Builder", 0)
  return
end

-- Guard: target track exists
local function findTrackByName(name)
  for i = 0, reaper.CountTracks(0) - 1 do
    local track = reaper.GetTrack(0, i)
    local _, n = reaper.GetTrackName(track)
    if n == name then return track end
  end
  return nil
end
```

## Dry-run mode

```lua
if DRY_RUN then
  reaper.ShowConsoleMsg(string.format(
    "[DRY RUN] Would insert note: pitch=%d vel=%d start=%.3f dur=%.3f\n",
    pitch, velocity, start_qn, dur_qn))
else
  insertNote(take, startppq, endppq, channel - 1, pitch, velocity)
end
```

## Rules

- Wrap all edits in `Undo_BeginBlock` / `Undo_EndBlock`
- Always call `MIDI_Sort(take)` after all note/CC insertions
- Validate track existence before inserting
- Convert channels from 1-based (human-readable) to 0-based (REAPER API) internally
- Document JSON dependency explicitly in `install.md`
- Never hardcode GUIDs unless the user supplies them
- `DRY_RUN = false` must be the shipping default (dry run is opt-in)

## Output structure

1. Assumptions (including PPQ, JSON library, REAPER version)
2. `build_midi.lua` (fully commented)
3. `README.md`
4. `install.md` (including json.lua setup instructions)
5. `test_cases.md`
6. Known limitations
