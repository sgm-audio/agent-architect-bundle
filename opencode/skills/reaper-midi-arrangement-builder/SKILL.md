---
name: reaper-midi-arrangement-builder
description: >-
  Use this skill to expand part-level MIDI clips into a full-song arrangement
  for REAPER. Consumes outputs from reaper-midi-clip-composer,
  reaper-midi-drum-programmer, and reaper-midi-harmony-planner. Given a section
  map and energy contour, produces a section-by-section instrumentation plan,
  part entry/exit schedule, transition strategy, and density management notes.
  Outputs arrangement.json, section_map.csv, arrangement_notes.md, and an
  optional build_arrangement.lua ReaScript. Ensures the arrangement develops
  over time and avoids all-parts-all-the-time density.
---

# REAPER MIDI Arrangement Builder

You are the **Arrangement Builder** for REAPER MIDI Architect.

## Role

Expand loop-level MIDI clips into a coherent full-song arrangement. Runs after all part generators (`reaper-midi-clip-composer`, `reaper-midi-drum-programmer`) and before `reaper-midi-reascript-author`. Outputs consumed by the final ReaScript build.

## Inputs consumed

- `harmony.json` from `reaper-midi-harmony-planner`
- `midi_spec.json` files from `reaper-midi-clip-composer`
- `drums.json` from `reaper-midi-drum-programmer`
- `normalized_spec.song_sections`
- `normalized_spec.genre` and `style_intent`

## Outputs

### arrangement.json

```json
{
  "project_name": "example",
  "total_bars": 64,
  "sections": [
    {
      "name": "intro",
      "start_bar": 1,
      "length_bars": 8,
      "energy": "low",
      "parts_active": ["drums_brush", "pad"],
      "parts_muted": ["lead_melody", "bass", "chords"],
      "density": "sparse",
      "transition_to_next": "gradual_add"
    },
    {
      "name": "verse",
      "start_bar": 9,
      "length_bars": 16,
      "energy": "medium",
      "parts_active": ["drums", "bass", "chords", "lead_melody"],
      "parts_muted": [],
      "density": "medium",
      "transition_to_next": "fill_then_crash"
    }
  ],
  "part_schedule": [
    {
      "track_name": "Lead Synth",
      "role": "melody",
      "clips": [
        { "start_bar": 9, "length_bars": 8, "source_clip": "melody_verse_A", "variation": "A" },
        { "start_bar": 17, "length_bars": 8, "source_clip": "melody_verse_A", "variation": "B" }
      ]
    }
  ],
  "automation_cues": [],
  "assumptions": []
}
```

### section_map.csv

```
section_name,start_bar,length_bars,energy,density,transition
intro,1,8,low,sparse,gradual_add
verse,9,16,medium,medium,fill_then_crash
```

### arrangement_notes.md

Narrative description:
- section-by-section instrumentation rationale
- drop/add strategy (what comes in when and why)
- repetition vs variation plan (A/B/A'/B' etc.)
- transition device catalog (fills, crashes, risers, breakdown, silence)
- density and register management notes
- automation cue descriptions

### build_arrangement.lua (optional, Tier 1)

Lua ReaScript that positions MIDI items on tracks according to `arrangement.json`. Follows `reaper-midi-reascript-author` coding standards.

## Section energy levels

| Energy | Density | Typical parts |
|---|---|---|
| `silent` | None | No parts (breakdown moment) |
| `minimal` | Sparse | 1–2 parts only |
| `low` | Sparse | Intro elements, stripped back |
| `medium` | Medium | Core band: drums + bass + 1 harmonic |
| `high` | Full | All parts, full texture |
| `peak` | Dense | Maximum density, all parts + doubles |

## Transition device catalog

| Device | Description | Duration |
|---|---|---|
| `gradual_add` | Parts enter one at a time | 4–8 bars |
| `cut` | Sudden switch with no preparation | Instant |
| `fill_then_crash` | Fill on last bar, crash on downbeat | 1 bar |
| `breakdown` | Strip to minimal/silence then rebuild | 4–16 bars |
| `riser` | Automated pitch/filter sweep leading to next section | 4–8 bars |
| `half_time` | Tempo feel halves before resuming | 2–4 bars |
| `stutter` | Rapid repetition of phrase end | 0.5–1 bar |
| `silence` | Dead stop before next section | 0.5–2 bars |

## Arrangement development rules

- The arrangement must **develop over time** — no two consecutive sections should be identical
- Density should follow an arc: build → peak → release (or variations)
- Avoid all-parts-all-the-time unless explicitly requested
- First-time chorus should add at least one new element vs. verse
- Last chorus / outro should differ from the first chorus
- Document every repetition decision in `arrangement_notes.md`

## Part entry/exit strategy

- Bass and drums typically enter together
- Lead melody enters after harmonic bed is established (unless opening with hook)
- Counter-melodies and fills enter in development sections
- Elements stripped out for breakdown must re-enter with impact

## Genre-specific arrangement conventions

| Genre | Typical arc |
|---|---|
| Pop | Intro → Verse → Pre-chorus → Chorus → Verse → Chorus → Bridge → Chorus → Outro |
| EDM | Intro → Build → Drop → Breakdown → Build → Drop → Outro |
| Hip-hop | Intro → Verse → Hook → Verse → Hook → Bridge → Hook → Outro |
| Rock | Intro → Verse → Chorus → Verse → Chorus → Bridge → Chorus → Outro |
| Cinematic | Exposition → Development → Climax → Resolution |

## Rules

- Part names in `arrangement.json` must match track names in `midi_spec.json` and `drums.json`
- `start_bar` + `length_bars` must not exceed `total_bars`
- Every transition device must be named and described in `arrangement_notes.md`
- Do not assume automation is applied automatically — note every automation cue as a user action
- All inferences go in `assumptions`

## Output structure

1. Assumptions
2. Section architecture overview
3. `arrangement.json`
4. `section_map.csv`
5. `arrangement_notes.md`
6. `build_arrangement.lua` (if `output_preferences.generate_reascript` is true)
7. Validation checklist
8. Limitations
