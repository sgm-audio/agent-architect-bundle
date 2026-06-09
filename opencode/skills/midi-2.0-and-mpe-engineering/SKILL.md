---
name: midi-2.0-and-mpe-engineering
description: >-
  Use this skill when the user is working on or asking about MIDI 2.0, MPE (MIDI Polyphonic Expression), per-note pitch bend, MIDI CI, or UMP (Universal MIDI Packet).
version: 1.0.0
---

# Skill: MIDI 2.0 & MPE (MIDI Polyphonic Expression) Engineering
## 📖 1. Overview
Implements high-resolution, per-note controller streams (MIDI 2.0 UMP, MPE Zone 1/2) for expressive controllers like Roli Seaboard, Osmose, and modern DAWs.
## ⚙️ 2. Core Functionality
- UMP Parsing: 32-bit Universal MIDI Packet decoding (Group, Status, 16/32-bit data)
- MPE Mapping: Per-note bend, pressure, timbre, slide via channel-per-note allocation
- Polyphonic Voice Management: 128+ voice allocation with per-note state tracking
- Resolution Scaling: 7-bit → 16-bit parameter normalization
## 📥📤 3. Input/Output Schema
| Inputs | UMP packets, MIDI 1.0 fallback, controller matrices | Outputs | Per-note voice state, high-res automation curves, MIDI 1.0 compatibility messages |
## 🏗️ 4. Architecture
`struct NoteState { float bend, pressure, timbre; bool active; };` Use atomic map or flat array indexed by MIDI channel/note. Parse UMP `UMP_TYPE_MIDI_NOTE_ON` with 32-bit velocity/pitch.
## 🔗 5. Dependencies
`juce::MidiMessage`, `UMP` parser libs, MPE spec v1.1
## ⚠️ 6. Edge Cases
| Note Stealing | Dropped chords | Implement LRU/voice priority, per-note release trails |
| UMP/1.0 Mix | Host confusion | Explicit MPE zone negotiation, fallback to channel-per-note |
| High-Res Noise | Parameter jitter | Apply per-note exponential smoothing (`alpha = 0.02`) |
## 🛡️ 7. Constraints
- Latency: < 1ms note-to-audio
- Memory: 128 notes × 16 bytes = ~2KB fixed
- Thread: MPE state updated on MIDI thread, sampled atomically by audio
## 🤖 8. Usage
- *Prompt:* "Generate an MPE voice allocator that maps channel 1-16 to individual notes with per-note timbre control."
## 🧪 9. Testing
- Roli/Osmose hardware loopback
- UMP validation with `MIDI 2.0 Tester`
- Stress: 64 simultaneous per-note modulations
## 📝 10. Best Practices
- Always expose MPE enable toggle
- Document channel-per-note mapping in UI
- Clamp high-res values to [0.0, 1.0] before DSP
*Skill Version: 1.0.0 | Standards: MIDI 2.0 UMP, MPE 1.1 | Domain: Real-Time Audio*