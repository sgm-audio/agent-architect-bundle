---
name: faust-functional-audio-stream-integration
description: >-
  Use this skill when the user is working on or asking about Faust DSP language, Faust to C++/JUCE/WASM, functional audio stream processing, or integrating Faust-generated DSP.
version: 1.0.0
---

# Skill: Faust (Functional Audio Stream) Integration
## 📖 1. Overview
Writes DSP in high-level Faust language, compiles to optimized C++ for rapid plugin prototyping and architecture exploration.
## ⚙️ 2. Core Functionality
- Functional Syntax: Signal processing as pure functions
- Architecture Files: JUCE/CLAP/WebAudio wrappers
- DSP Optimization: Vectorization, fixed-point, memory pooling
- Parameter Binding: `nentry`, `slider`, `button` to APVTS
## 📥📤 3. Input/Output Schema
| Inputs | `.dsp` source, architecture files, target format | Outputs | C++ classes, compiled binaries, parameter metadata |
## 🏗️ 4. Architecture
`faust -o plugin.cpp -a juce.cpp synth.dsp`. Integrate `plugin.cpp` into JUCE `AudioProcessor`. Use `faust2api` for DAW wrappers.
## 🔗 5. Dependencies
`faust` compiler, `llvm` backend, JUCE
## ⚠️ 6. Edge Cases
| Memory Leak | State not saved | Implement `instanceInit`/`instanceClear` |
| Real-Time Violation | `printf`/malloc in RT | Strip debug, use fixed arrays |
| Parameter Drift | UI/audio mismatch | Map to `APVTS` via wrapper |
## 🛡️ 7. Constraints
- Latency: Zero overhead vs hand-written C++
- Size: < 50KB generated code
- Safety: RT-safe by design
## 🤖 8. Usage
- *Prompt:* "Generate a Faust DSP chain for a waveshaper with soft-knee compression and APVTS parameter binding."
## 🧪 9. Testing
- Output parity with C++ reference
- Parameter automation stress
- Cross-architecture validation
## 📝 10. Best Practices
- Keep `.dsp` pure, side-effect free
- Version compiler alongside project
- Use `declare` for metadata
*Skill Version: 1.0.0 | Standards: Faust 2.x, DSP | Domain: Opencode Architecture*