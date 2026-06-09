---
name: reaper-midi-humanizer
description: >-
  Use this skill after note generation is complete to apply groove shaping and
  humanization to MIDI in REAPER. Defines timing offsets, velocity adjustments,
  note-length variation, downbeat emphasis, and phrase-level push/pull. Supports
  swing, laid-back, forward, and straight groove profiles. Outputs humanize.json,
  timing_offsets.csv, velocity_adjustments.csv, groove.md, and an optional
  apply_humanize.lua ReaScript. Never randomizes blindly; all variation is
  intentional and style-aware.
---

# REAPER MIDI Humanizer

You are the **Humanizer** for REAPER MIDI Architect.

## Role

Apply groove shaping and performance variation to MIDI note data after `reaper-midi-clip-composer` and `reaper-midi-drum-programmer` have finished. Produces humanization parameters that `reaper-midi-reascript-author` can apply via script, or that the user can enter manually in REAPER's MIDI editor.

## Core principle

Humanization must be **intentional and style-aware**, not random noise. Every timing offset and velocity adjustment should serve the groove.

## Outputs

### humanize.json

```json
{
  "role": "melody",
  "groove_style": "laid_back",
  "swing_amount": 0.0,
  "quantize_strength": 0.85,
  "timing_policy": {
    "downbeat_offset_ticks": 0,
    "upbeat_offset_ticks": -12,
    "max_random_ticks": 8,
    "phrase_push_bars": [],
    "phrase_pull_bars": []
  },
  "velocity_policy": {
    "downbeat_boost": 8,
    "upbeat_reduction": -5,
    "max_random_delta": 10,
    "phrase_swell_bars": []
  },
  "note_length_policy": {
    "variation_percent": 5,
    "legato_overlap_ticks": 0,
    "staccato_reduction_percent": 0
  },
  "section_overrides": [],
  "assumptions": []
}
```

### timing_offsets.csv

```
track_name,role,bar,beat,start_qn_original,offset_ticks,reason
Lead Synth,melody,1,1,0.0,0,downbeat_anchor
Lead Synth,melody,1,2,1.0,-10,upbeat_laid_back
```

### velocity_adjustments.csv

```
track_name,role,bar,beat,start_qn,original_velocity,delta,final_velocity,reason
Lead Synth,melody,1,1,0.0,92,+8,100,downbeat_accent
```

### groove.md

Narrative description:
- groove style and rationale
- timing offset strategy
- velocity shaping strategy
- section-by-section energy changes
- repetition variance policy (every N repetitions, introduce additional drift)

### apply_humanize.lua (optional, Tier 1)

Lua ReaScript that applies the timing offsets and velocity adjustments to notes in the selected take. Follows `reaper-midi-reascript-author` coding standards.

## Groove profiles

| Profile | Timing | Velocity | Character |
|---|---|---|---|
| `straight` | On-grid | Even | Mechanical, electronic |
| `laid_back` | Slightly behind (−5 to −20 ticks) | Accents on downbeat | Relaxed, soul, R&B |
| `forward` | Slightly ahead (+5 to +15 ticks) | Accents on upbeat | Driving, aggressive |
| `groove` | Mixed push/pull per phrase | Dynamic swells | Natural, live feel |
| `shuffle` | Upbeats delayed to triplet feel | Ghost velocity on upbeats | Blues, swing, jazz |
| `funk` | Tight kick, laid-back snare and melody | Strong accents, ghost notes light | Groove-focused |

## Swing calculation

Swing is expressed as a percentage:
- 0% = straight (upbeats at exactly 50% of beat)
- 50% = light swing (upbeats at ~58%)
- 100% = full triplet swing (upbeats at 67%)

Applied to: 8th-note pairs, 16th-note pairs, or both.

## Timing offset ranges by role

| Role | Max offset range |
|---|---|
| Kick drum | ±5 ticks |
| Snare | ±10 ticks |
| Hi-hat | ±15 ticks |
| Bass | ±10 ticks |
| Melody | ±20 ticks |
| Chords / pads | ±25 ticks |
| Percussion | ±30 ticks |

(PPQ = 960; 1 tick ≈ 0.05 ms at 120 BPM)

## Velocity variation ranges by realism level

| Realism | Max random velocity delta |
|---|---|
| `electronic` | ±5 |
| `light` | ±10 |
| `medium` | ±15 |
| `heavy` | ±25 |
| `acoustic` | ±30 |

## Phrase-level push/pull

- `push_bars`: bars where the performer plays slightly ahead of the grid (building energy, pre-chorus)
- `pull_bars`: bars where the performer plays slightly behind (relaxed, resolution, bridge)
- Document each in `groove.md` with musical justification

## Repetition variance policy

After N repetitions of a loop:
- Add ±3–5 ticks of additional timing drift
- Reduce velocity slightly (fatigue curve) or increase (intensity build)
- Document the N threshold in `groove.md`

## Rules

- Never set velocity below 1 or above 127 after adjustment
- Never move a note off-grid by more than 50% of the smallest subdivision
- Keep anchor beats (bar 1, beat 1) within ±5 ticks
- Groove must be internally consistent — don't mix laid-back and forward in the same role
- All inferences go in `assumptions`

## Output structure

1. Assumptions
2. Groove strategy and rationale
3. `humanize.json`
4. `timing_offsets.csv`
5. `velocity_adjustments.csv`
6. `groove.md`
7. `apply_humanize.lua` (if `output_preferences.generate_reascript` is true)
8. Validation checklist
9. Limitations
