# REAPER Asset System 1 — Prompt Architecture for High-End REAPER Assets

Source: `E:\Reaper Prompting Systems\Reaper Asset System 1` — Added to RAG Jun 2026.

## Overview

A practical prompt architecture for reliably generating high-end REAPER assets with an AI model: FX chains, plugin presets, custom actions, ReaScripts, `.RPP` session templates, and themes/style systems.

Not "one magic prompt" but a **system of prompts** producing:
1. Consistent outputs
2. Technically valid REAPER artifacts
3. Mix/mastering decisions that sound commercial
4. Reusable workflows for different genres

## Core Design Principle

Don't prompt for hype — prompt for:
- Reference-quality sonic targets
- Specific engineering intent
- Constraint-aware implementation
- Format-specific output
- Validation and revision loops

**Bad:** "Make me an amazing vocal chain"
**Good:** "Create a Reaper-compatible vocal FX chain for intimate modern pop female lead vocals, inspired by Billie Eilish/Lorde tonal priorities, optimized for low-noise close-mic recordings, preserving breath detail while controlling harshness in the 2.5-5.5 kHz range, using stock ReaPlugs first and optionally premium alternatives. Output as: signal flow, plugin settings, macro notes, gain staging targets, automation plan, and a save-ready chain structure."

## System Components

### T1: The Core Shell (always use)
1. Role injection — "You are a senior mix engineer..."
2. Technology constraints — "Use REAPER convention, stock ReaPlugs first"
3. Output format specification — "Output as signal flow diagram + settings table + automation notes"
4. Validation criteria — "When finished, verify these measurable targets: [X dB, Y Hz, Z ms]"

### T2: Sonic Target Specification
Define precise frequency targets using real-world references:
- **Sub (20-60 Hz):** Feel, not hear — control with HPF at 30-40 Hz
- **Low Mids (60-250 Hz):** Clarity vs warmth — be specific about what to cut/boost
- **Mids (250 Hz-2 kHz):** Presence, body, boxiness
- **Upper Mids (2-6 kHz):** Clarity, harshness, sibilance
- **Highs (6-20 kHz):** Air, sparkle, noise floor

### T3: Plugin Selection Heuristics
1. Start with stock (ReaPlugs) — they're more capable than expected
2. Move to paid only when stock can't do the specific task
3. If paid, specify exact plugin name, version, and setting

### T4: Output Format Requirements
Always request:
- Signal flow diagram (chain order + send/return routing)
- Settings table (plugin, param, value, reason)
- Macro control mapping (MIDI CC or ReaLearn)
- Automation plan (what moves, when, how much)
- Meter targets (peak, RMS, LUFS, phase correlation)

### T5: Validation Protocol
1. **Null test** — Does the chain pass silence? (Unlikely, but test)
2. **Gain match** — Bypass A/B at same perceived loudness
3. **Spectrum match** — Reference track comparison
4. **Phase correlation meter** — 0 to +1 for stereo
5. **Real-world test** — Play on phone speakers, car, headphones
