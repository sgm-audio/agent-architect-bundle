---
name: reaper-reascript-authoring
description: "Use when writing, reviewing, debugging, or shipping Lua ReaScripts for Cockos REAPER — covers safe scripting conventions, MIDI manipulation, session architecture, FX chains, and ReaPack/Reapack licensing. Ported from the user's OpenCode Reaper skill suite (22 skills consolidated into one)."
version: 1.0.0
author: Hermes Agent (ported from OpenCode reaper-* skill suite)
license: MIT
metadata:
  hermes:
    tags: [reaper, reascript, lua, daw, midi, audio-plugin]
    related_skills: [opencode, mamba3-dsp-methodology, reaper-lua-syntax, reascript-licensing]
---

# REAPER ReaScript Authoring

## Overview

This skill consolidates the user's ReaScript workflow — 22 custom OpenCode skills built over months of development — into a single class-level Hermes skill. Covers the full lifecycle: writing production-safe Lua scripts, MIDI manipulation, session architecture, FX chains, theme building, validation (Top Shelf quality), and ReaPack licensing for release.

The user's workflow was built in OpenCode and is tested against real REAPER usage. When in doubt about a Reaper-specific interaction, delegate to OpenCode via `opencode run '...'` since OpenCode has the full depth of the 22 source skills.

## When to Use

- Writing or reviewing Lua ReaScripts for REAPER
- Building MIDI manipulation scripts (arrangement, composition, drum programming, humanization, expression, harmony)
- Designing session architectures or FX chains
- Creating REAPER themes
- Validating scripts against Top Shelf quality standards
- Preparing scripts for ReaPack release with licensing metadata
- Debugging scripts that "run but do nothing" (most common Lua pattern errors)

Don't use for: general Lua programming (not REAPER-specific), Python scripting for REAPER (use the python-debugpy or general Python skills), non-REAPER audio DSP (use mamba3-dsp-methodology).

## Core Concepts

### Language: Lua 5.3+

REAPER embeds Lua 5.3+. Key facts:
- Bitwise operators work: `& | ~ << >>`
- Integer division: `//`
- No regex — Lua patterns are NOT regex. This is the #1 bug source.
- The entire API lives under the injected global `reaper.*`
- The GFX API under `gfx.*`
- No package ecosystem unless an extension (SWS, js_ReaScriptAPI, ReaImGui) is installed

### The Lua Pattern Gotcha That Breaks Everything

```lua
-- WRONG: This does NOT mean "8 to 32 alphanumeric chars"
local id = name:match("_([A-Za-z0-9]{8,32})$")
-- Lua reads { } as literal brace characters, match returns nil

-- RIGHT: Match open-ended, check length in code
local id = name:match("_([A-Za-z0-9]+)$")
if id and #id >= 8 and #id <= 32 then ... end
```

Also remember: no `\d`, no `\w`, no `{n,m}`, no `(?:)` non-capturing groups.

## Required Outputs for Every Script

| File | Contents |
|------|----------|
| `script_name.lua` | Main script with full comments |
| `README.md` | What it does, supported versions, key behaviors |
| `install.md` | Where to save, how to add to Action List, shortcut setup |
| `test_cases.md` | Step-by-step test scenarios with expected outcomes |

## Mandatory Coding Standards

Every script MUST include at the top:

```lua
-- USER SETTINGS (edit here) ---------------------------------------------------
local SETTING_NAME = "default_value"  -- description
-- END USER SETTINGS -----------------------------------------------------------
```

### Mandatory wrappers

```lua
reaper.Undo_BeginBlock()
reaper.PreventUIRefresh(1)

-- Script logic here

reaper.PreventUIRefresh(-1)
reaper.Undo_EndBlock("Script Description", -1)
```

### Validation patterns — always check selections

```lua
-- Check track selection
local track = reaper.GetSelectedTrack(0, 0)
if not track then
    reaper.ShowMessageBox("Please select a track first.", "Error", 0)
    return
end

-- Check item selection
local item = reaper.GetSelectedMediaItem(0, 0)
if not item then
    reaper.ShowMessageBox("Please select a media item first.", "Error", 0)
    return
end

-- Check take
local take = reaper.GetActiveTake(item)
if not take or not reaper.TakeIsMIDI(take) then
    reaper.ShowMessageBox("Please select a MIDI item.", "Error", 0)
    return
end
```

### Chunk editing — use sparingly

Prefer the REAPER API over fragile chunk editing. When chunk editing is necessary (e.g. setting track colors, routing), document why the API didn't suffice in a comment.

## Script Categories

### MIDI Scripts

The user has scripts covering these MIDI domains in OpenCode:

| Category | What it does |
|----------|-------------|
| Arrangement Builder | Structure MIDI clips into song sections |
| Clip Composer | Generate/transform MIDI patterns |
| Drum Programmer | Map drum hits to GM/articulation maps |
| Expression Designer | CC curves, velocity gradients, modulation |
| Harmony Planner | Chord progression generation, voice leading |
| Humanizer | Timing/velocity randomization with musical constraints |
| Intake Normalizer | Quantize, deduplicate, consolidate incoming MIDI |
| MIDI ReaScript Author | General-purpose MIDI script creation |
| MIDI Orchestrator | Multi-track MIDI orchestration scripts |
| MIDI Session Architect | Full MIDI session bill of materials |
| MIDI Validator | Check for overlapping notes, stuck notes, corrupt events |

### Session Architecture

- **Session Architect**: Full REAPER session generation (tracks, routing, FX, markers, regions, tempo map)
- **Intake Normalizer**: Audio intake normalization (gain staging, peak normalization, LUFS)
- **FX Chain Designer**: Build FX chains with parameter mapping and automation

### Validation (Top Shelf)

Run scripts through this checklist before shipping:

1. Script runs without errors on empty project
2. Script runs without errors on multi-track project
3. All selection checks fire correctly with no selection
4. Undo block wraps all state changes
5. No hardcoded GUIDs unless user-supplied
6. No Lua pattern errors (no regex syntax used)
7. Chunk editing (if used) has comment explaining why API didn't work
8. README, install.md, test_cases.md all present

## ReaPack Licensing for Release

When preparing scripts for public release via ReaPack:

1. Add ReaPack metadata to script header:
```lua
-- @description Script Name
-- @version 1.0
-- @author Your Name
-- @changelog Initial release
-- @donation https://...
-- @links
--   Website https://...
-- @provides
--   [main] script_name.lua
```

2. Convert to ReaPack package format if distributing multiple scripts
3. Release via GitHub + ReaPack/index.xml

## Common Pitfalls

1. **Lua patterns != regex** — No `{n,m}`, no `\d`, no `\w`. This is the #1 cause of "runs but produces nothing" bugs.
2. **Missing undo blocks** — Every state change must be wrapped in `Undo_BeginBlock`/`Undo_EndBlock`
3. **No selection validation** — Script crashes if no track/item/take is selected. Always check and show error message.
4. **Hardcoded GUIDs** — Will break if the user moves tracks/items. Use API lookups instead.
5. **Chunk editing when API suffices** — Chunks are fragile across REAPER versions. Prefer `reaper.SetMediaTrackInfo_Value` / `reaper.SetTrackStateChunk` only when the API doesn't expose the property.
6. **Forgetting `PreventUIRefresh(1)`** — Causes flickering during batch operations on large sessions.
7. **Defer scripts without exit conditions** — Infinite defer loops drain CPU. Always provide a way to exit (timeout, user action, action toggle).
8. **Modifying project state in ImGui draw callbacks** — Draw callbacks fire on every frame. Queue state changes for the defer callback.
9. **Python scripts requiring `reapy`** — Python ReaScripts need explicit dependency documentation. Stick to Lua which ships built-in.
10. **Shipping without test_cases.md** — The user's standard requires test cases for every script. Include steps and expected outcomes.

## REAPER Asset Prompting Systems

Three reference files for AI-driven REAPER asset generation were sourced from `E:\Reaper Prompting Systems\` and `E:\bazzite-vst-modernized\`:

| Reference | Contents |
|-----------|----------|
| `references/reaper-asset-system-1.md` | Prompt architecture for generating high-end REAPER assets — FX chains, signal flow, sonic target specification, validation protocol |
| `references/reaper-asset-system-2.md` | Advanced constraint injection, iterative refinement pipeline, mix bus vs individual track philosophy |
| `references/beat-making-systems.md` | Beat production prompting (trap, hip-hop, lo-fi, house, DnB), Hip EDM hybrid template system |

Load these when the user asks to generate REAPER content with an AI model — they encode your own testing-proven prompt structures.

## Verification Checklist

- [ ] Script has USER SETTINGS section at top
- [ ] All selection state is validated before access
- [ ] `Undo_BeginBlock` / `Undo_EndBlock` wraps state changes
- [ ] `PreventUIRefresh(1)` / `(-1)` matches batch operations
- [ ] No regex syntax in Lua pattern calls
- [ ] No hardcoded GUIDs
- [ ] Chunk editing (if used) has justification comment
- [ ] README.md, install.md, test_cases.md generated
- [ ] Script tested on empty project + multi-track project
- [ ] ReaPack metadata header present (if releasing)

## Delegation to OpenCode

The user's original 22 Reaper skills lived in OpenCode at `~/.config/opencode/skills/` and were consolidated into this skill. The individual Hermes-level copies were deleted in June 2026 as redundant. For complex or novel ReaScript tasks, delegate directly — OpenCode may still have the original depth:

```
terminal(command="opencode run 'Write a ReaScript that batch-normalizes all selected MIDI items to velocity range 64-128 with humanization'", workdir="/mnt/c/dev")
```

Note: the individual reaper-* skills (reaper-validator, reaper-midi-*, etc.) no longer exist as Hermes skills. This consolidated skill + reaper-lua-syntax + reascript-licensing + reascript-ship-pipeline are the only REAPER skills in the Hermes library.
