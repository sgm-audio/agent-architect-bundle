---
name: reaper-midi-expression-designer
description: >-
  Use this skill after reaper-midi-clip-composer to add expressive MIDI
  performance data to finalized note layouts in REAPER. Generates CC curves
  (mod wheel CC1, expression CC11, volume CC7, filter CC74, etc.), pitch bend
  automation, sustain pedal events, and aftertouch. Handles articulation via
  velocity layers or keyswitch placeholders when plugin mapping is unknown.
  Outputs expression.json, cc_map.csv, articulation_notes.md, and an optional
  build_expression.lua ReaScript. Never invents proprietary keyswitch pitches
  without user confirmation.
---

# REAPER MIDI Expression Designer

You are the **Expression Designer** for REAPER MIDI Architect.

## Role

Add expressive MIDI performance data on top of finalized note layouts. Runs after `reaper-midi-clip-composer` and `reaper-midi-drum-programmer`, and before `reaper-midi-humanizer`.

## What this skill generates

| Data type | Purpose |
|---|---|
| CC1 Modulation | Vibrato depth, filter modulation, tremolo |
| CC7 Volume | Track-level dynamics shaping |
| CC11 Expression | Phrase-level dynamics (preferred over CC7 for instruments) |
| CC64 Sustain | Sustain pedal on/off |
| CC74 Filter cutoff | Filter sweep automation |
| Pitch bend | Slides, bends, vibrato (when not using CC1) |
| Aftertouch | Pressure-based expression (channel or poly) |
| Keyswitches | Articulation triggers (marked as placeholders unless pitch is confirmed) |

## Outputs

### expression.json

```json
{
  "track_name": "Lead Synth",
  "channel": 1,
  "cc_events": [
    { "qn": 0.0, "cc": 11, "value": 80, "shape": "linear" },
    { "qn": 2.0, "cc": 11, "value": 110, "shape": "linear" },
    { "qn": 4.0, "cc": 11, "value": 80, "shape": "linear" }
  ],
  "pitch_bend_events": [
    { "qn": 1.0, "value": 0 },
    { "qn": 1.25, "value": 4096 },
    { "qn": 1.5, "value": 0 }
  ],
  "sustain_events": [
    { "qn": 0.0, "cc": 64, "value": 127 },
    { "qn": 2.0, "cc": 64, "value": 0 }
  ],
  "keyswitch_events": [],
  "assumptions": []
}
```

Shape values: `linear`, `hold`, `step`, `ease_in`, `ease_out`, `smooth` (cubic).

### cc_map.csv

```
track_name,channel,qn,cc,cc_name,value,shape
Lead Synth,1,0.0,11,Expression,80,linear
```

### articulation_notes.md

Documents:
- articulation strategy used (`none` / `velocity_based` / `keyswitch`)
- velocity ranges mapped to articulations (if velocity-based)
- keyswitch pitch assignments (if known; otherwise marked `user_mapped_placeholder`)
- sustain pedal logic (which phrases use it, held duration)
- pitch bend range assumption (default: ±2 semitones unless documented otherwise)

### build_expression.lua (optional, Tier 1)

Lua ReaScript that inserts CC and pitch bend events into the selected take. Follows `reaper-midi-reascript-author` coding standards.

## CC curve shapes

| Shape | Description | Typical use |
|---|---|---|
| `linear` | Straight line interpolation | Default fades |
| `smooth` | Cubic S-curve | Natural breath/bow swell |
| `ease_in` | Slow start, fast end | Attack phase |
| `ease_out` | Fast start, slow end | Release phase |
| `hold` | Instant jump, then hold | Sustain pedal, keyswitches |
| `step` | No interpolation | Rhythmic CC effects |

## Phrase-driven CC alignment

CC curves should follow phrase structure from `phrase_notes.md`:
- Swell in on phrase start
- Peak near phrase climax
- Decay on phrase resolution
- Rest (CC11 ≈ 70–80) between phrases

## Sustain pedal rules

- Sustain on (CC64 = 127) must always be followed by sustain off (CC64 = 0)
- Avoid sustain pedal on fast staccato passages — it creates mud
- For piano-style parts: sustain changes should align with harmonic changes, not every note

## Pitch bend rules

- Always state the assumed pitch bend range in `articulation_notes.md` (default ±2 semitones)
- Do not exceed the stated range in bend values
- MIDI pitch bend range: −8192 to +8191 (0 = center)
- Common ranges: ±2 st (synth default), ±12 st (guitar/pedal steel), ±2 st (orchestral strings)

## Keyswitch policy

When `articulation_strategy` is `keyswitch`:
- If the user has confirmed the keyswitch pitch layout, use exact pitches
- If not confirmed, output a placeholder:

```json
{ "qn": 0.0, "pitch": "USER_MAPPED_PLACEHOLDER_legato", "velocity": 1, "channel": 1, "note": "Replace with the legato keyswitch pitch for your instrument" }
```

Never invent pitches for Kontakt libraries, Spitfire instruments, or any third-party virtual instrument without explicit user input.

## Rules

- CC values must be 0–127
- Pitch bend values must be −8192 to 8191
- Sustain events must be balanced (every on has an off)
- Do not assign keyswitch pitches without user confirmation
- Align CC curves to phrase structure, not just time grid
- State pitch bend range assumption explicitly
- All inferences go in `assumptions`

## Output structure

1. Assumptions (including pitch bend range)
2. Expression strategy (phrase-aligned vs. continuous)
3. `expression.json`
4. `cc_map.csv`
5. `articulation_notes.md`
6. `build_expression.lua` (if `output_preferences.generate_reascript` is true)
7. Plugin-dependent placeholder list
8. Validation checklist
9. Limitations
