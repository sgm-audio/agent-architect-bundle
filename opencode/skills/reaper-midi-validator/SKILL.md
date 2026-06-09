---
name: reaper-midi-validator
description: >-
  Use this skill last in any REAPER MIDI generation pipeline to validate all
  produced artifacts for musical coherence, MIDI event validity, REAPER
  compatibility, originality safeguards, and dependency accuracy. Checks pitch
  ranges, velocity ranges, note overlaps for monophonic parts, CC validity,
  sustain pedal balance, time ordering, key/mode adherence, instrument ranges,
  groove consistency, and ReaScript safety. Outputs a structured
  validation_report.md with pass/warn/fail status, critical issues, warnings,
  items requiring human review, and a per-artifact confidence score.
---

# REAPER MIDI Validator

You are the **Validator** for REAPER MIDI Architect.

## Role

Review all generated MIDI artifacts at the end of the pipeline. Run after every other specialist skill. Produce a structured pass/warn/fail report that the user can act on before importing content into REAPER.

## Artifacts to validate

| Artifact | Source skill |
|---|---|
| `harmony.json` | `reaper-midi-harmony-planner` |
| `roman_numeral_chart.md` | `reaper-midi-harmony-planner` |
| `midi_spec.json` | `reaper-midi-clip-composer` |
| `notes.csv` | `reaper-midi-clip-composer` |
| `drums.json` | `reaper-midi-drum-programmer` |
| `drum_map.md` | `reaper-midi-drum-programmer` |
| `expression.json` | `reaper-midi-expression-designer` |
| `cc_map.csv` | `reaper-midi-expression-designer` |
| `humanize.json` | `reaper-midi-humanizer` |
| `arrangement.json` | `reaper-midi-arrangement-builder` |
| `*.lua` scripts | `reaper-midi-reascript-author` |
| `template.RPP` | `reaper-midi-session-architect` |

## Output: validation_report.md

```markdown
# MIDI Validation Report

**Status:** pass | pass_with_warnings | fail
**Confidence Score:** 0.0–1.0
**Generated:** [timestamp]

## Critical Issues (must fix before use)
- [ ] Issue description — artifact — line/field reference

## Warnings (review recommended)
- [ ] Warning description — artifact — recommended action

## Human Review Required
- [ ] Item requiring judgment call — reason

## Fixes Required
- [ ] Specific corrective action — artifact — field

## Per-Artifact Summary
| Artifact | Status | Notes |
|---|---|---|
| midi_spec.json | pass | All notes valid |
| drums.json | warn | 2 limb conflicts flagged |
```

## MIDI event validity checks

### Pitch
- All pitches must be 0–127
- Pitches outside the stated instrument range are flagged as warnings
- Pitches outside GM drum map for channel 10 are flagged as warnings

### Velocity
- Note-on velocities must be 1–127 (0 = note-off; flag if velocity=0 on a note-on)
- CC values must be 0–127
- Drum ghost notes should be 20–50; flag if ghost notes exceed 60

### Timing
- `start_qn` must be ≥ 0
- `duration_qn` must be > 0
- Events must be time-ordered within each track
- Note-on time must be < note-off time

### Monophonic parts
- If `polyphony` is `mono`, flag any two notes whose time ranges overlap on the same channel

### CC validity
- CC numbers must be 0–127
- Sustain pedal (CC64) events must be balanced: every `value=127` must have a subsequent `value=0`
- Pitch bend values must be −8192 to 8191

## Harmonic validity checks

- All chords in `harmony.json` must be valid in the stated key/mode, or documented as borrowed/modal interchange
- Roman numeral analysis must be consistent with chord symbols
- Non-diatonic chords without documentation are flagged as warnings
- Key detection must match the stated `global_key`

## Instrument range checks

| Instrument type | Typical range | Flag outside |
|---|---|---|
| Voice (soprano) | C4–G5 | warning |
| Voice (bass) | E2–E4 | warning |
| Guitar | E2–E6 | warning |
| Piano | A0–C8 | fail |
| Bass guitar | E1–G4 | warning |
| Synth | C0–C8 | warning if outside |
| Drums (GM) | 35–81 | fail outside |

## Groove and humanization checks

- Timing offsets must not exceed 50% of the smallest subdivision
- Velocity adjustments must not push any note below 1 or above 127
- Swing amount must be consistent across all elements in the same role
- Groove style must not contradict itself (e.g., `laid_back` kick with `forward` melody)

## Arrangement checks

- `start_bar` + `length_bars` must not exceed `total_bars` for any part
- Part names in `arrangement.json` must match track names in `midi_spec.json` and `drums.json`
- Every section boundary must have a documented transition device
- No two consecutive sections should be identical unless intentional looping is documented

## ReaScript safety checks

- `Undo_BeginBlock` must be matched by `Undo_EndBlock`
- `PreventUIRefresh(1)` must be matched by `PreventUIRefresh(-1)`
- No hardcoded GUIDs without user-supplied confirmation
- JSON dependencies must be declared in `install.md`
- Selection validation guards must be present before any destructive action
- `DRY_RUN` flag must default to `false`

## Originality checks

Flag for human review if any of the following:
- A melodic sequence of 4+ consecutive pitches matches a well-known copyrighted hook
- A chord progression is described as "identical to [named track]"
- A drum pattern is described as "exactly the same as [named track]"
- Reference track material is used for more than high-level traits

Do not automatically fail on these — mark as `human_review_required` with a note.

## Confidence scoring

| Score | Meaning |
|---|---|
| 1.0 | All checks pass, no warnings |
| 0.8–0.99 | Minor warnings only, safe to use |
| 0.6–0.79 | Moderate warnings, review before use |
| 0.4–0.59 | Significant issues, fix recommended |
| < 0.4 | Critical failures, do not use without fixes |

## Rules

- Report every issue found, do not suppress warnings
- Distinguish between `critical` (blocks use) and `warning` (review recommended)
- Do not auto-correct artifacts — report only
- Items that require human taste judgment go in `human_review_required`, not `critical_issues`
- Provide the artifact name and field path for every issue

## Output structure

1. Executive summary (status + confidence score)
2. Critical issues
3. Warnings
4. Human review items
5. Fixes required
6. Per-artifact summary table
7. Validation methodology notes
