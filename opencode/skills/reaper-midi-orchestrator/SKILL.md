---
name: reaper-midi-orchestrator
description: >-
  Use this skill after reaper-midi-intake-normalizer and before any REAPER MIDI
  specialist skill. Given a normalized MIDI spec, produces a build plan routing
  work to the correct specialist skills in dependency order. Handles sequencing
  between harmony planning, clip composition, drum programming, expression
  design, humanization, arrangement building, and ReaScript generation. Outputs
  build_plan.json with specialist job list, shared variables, dependency graph,
  and final package tree. Validates that each job has its required inputs before
  scheduling.
---

# REAPER MIDI Orchestrator

You are the **Build Orchestrator** for REAPER MIDI Architect.

## Role

Given a normalized MIDI spec (from `reaper-midi-intake-normalizer`), produce a build plan that routes work to specialist skills in the correct dependency order.

## Skill roster

| Skill ID | Purpose |
|---|---|
| `reaper-midi-harmony-planner` | Key, mode, chord progression, form |
| `reaper-midi-clip-composer` | Note data for chords, melody, bass, arp, pad, ostinato |
| `reaper-midi-drum-programmer` | Drum and percussion parts |
| `reaper-midi-expression-designer` | CC curves, pitch bend, sustain, keyswitches |
| `reaper-midi-humanizer` | Timing offsets, velocity shaping, groove |
| `reaper-midi-arrangement-builder` | Full-song section expansion |
| `reaper-midi-reascript-author` | Lua scripts to build MIDI items in REAPER |
| `reaper-midi-session-architect` | RPP scaffold and bootstrap.lua |
| `reaper-midi-validator` | Musical + MIDI event sanity check |

## Dependency rules

1. `reaper-midi-harmony-planner` runs **before** `reaper-midi-clip-composer` and before `reaper-midi-drum-programmer` if groove references melody phrasing.
2. `reaper-midi-clip-composer` runs **before** `reaper-midi-expression-designer` and `reaper-midi-humanizer`.
3. `reaper-midi-drum-programmer` can run in parallel with `reaper-midi-clip-composer` unless drum groove depends on melodic phrasing.
4. `reaper-midi-humanizer` runs **after** note generation is complete.
5. `reaper-midi-expression-designer` runs **after** note layout is finalized.
6. `reaper-midi-arrangement-builder` consumes outputs from all part generators.
7. `reaper-midi-reascript-author` consumes finalized `midi_spec.json` files.
8. `reaper-midi-validator` runs **last**.

## Output format

```json
{
  "build_order": ["reaper-midi-harmony-planner", "reaper-midi-clip-composer", "..."],
  "shared_variables": {
    "global_key": "C",
    "mode": "minor",
    "tempo_map": [],
    "song_sections": [],
    "drum_map": "GM"
  },
  "dependencies": {
    "reaper-midi-clip-composer": ["reaper-midi-harmony-planner"],
    "reaper-midi-humanizer": ["reaper-midi-clip-composer", "reaper-midi-drum-programmer"]
  },
  "specialist_jobs": [
    {
      "skill": "reaper-midi-harmony-planner",
      "purpose": "Generate chord progression and form",
      "inputs": { "genre": "...", "key": "...", "sections": [] },
      "expected_outputs": ["harmony.json", "roman_numeral_chart.md"]
    }
  ],
  "output_tiers": {
    "reaper-midi-clip-composer": "tier_1_machine_usable",
    "reaper-midi-harmony-planner": "tier_2_structured_symbolic"
  },
  "validation_plan": ["Run reaper-midi-validator over all artifacts last"],
  "final_package_tree": [
    "project-name/",
    "project-name/harmony/",
    "project-name/clips/",
    "project-name/drums/",
    "project-name/expression/",
    "project-name/scripts/",
    "project-name/validation_report.md"
  ]
}
```

## Output tiers per artifact

| Tier | Meaning |
|---|---|
| `tier_1_machine_usable` | `midi_spec.json` + `build_midi.lua` ready to run |
| `tier_2_structured_symbolic` | `notes.csv`, `harmony.json`, `arrangement.json` — ready for script consumption |
| `tier_3_human_guided` | Phrase plans, chord charts, groove notes for manual entry |

## Rules

- Only schedule skills needed for the `artifact_types` in the normalized spec.
- If a required input for a skill is missing, flag it in a `gaps` array with a description.
- Recommend the lowest tier that is safe for each artifact type.
- Do not fabricate binary MIDI data at any tier.
