---
name: automated-audio-regression-and-unit-testing
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Automated Audio Regression And Unit Testing", "opencode-migrated"]
    related_skills: []
---


# Skill: Automated Audio Regression & Unit Testing
## 📖 1. Overview
Headless test suites that render audio to disk, run phase-cancellation, spectral analysis, and CPU profiling against golden references to guarantee DSP correctness across commits.
## ⚙️ 2. Core Functionality
- Headless Rendering: CLI plugin host with `AudioProcessor::processBlock()` loop
- Phase Cancellation: `render_new - render_ref` → RMS < -140dB target
- Spectral Diff: FFT magnitude comparison with tolerance thresholds
- CI Integration: GitHub Actions runner, artifact upload, failure gating
## 📥📤 3. Input/Output Schema
| Inputs | Plugin binaries, test MIDIs/WAVs, reference WAVs, tolerance configs | Outputs | Pass/fail reports, delta audio files, CPU/latency CSVs, CI badges |
## 🏗️ 4. Architecture
`pytest` + `subprocess` to run headless host. Compare outputs via `scipy.signal` or C++ `libaiff`. Store golden files in Git LFS. Trigger on PR merge.
## 🔗 5. Dependencies
`libaiff`, `libsndfile`, `Catch2`/`doctest`, `FFmpeg` (optional)
## ⚠️ 6. Edge Cases
| Float Rounding | Diff at -130dB | Allow `1e-5` tolerance |
| Sample Rate Drift | Length mismatch | Resample reference to exact test SR |
| Dither/Quantization | Noise floor shift | Disable host dither for deterministic tests |
## 🛡️ 7. Constraints
- Deterministic: Same binary → bit-identical output
- Runtime: < 30s per test suite in CI
- Storage: LFS for >100MB reference WAVs
## 🤖 8. Usage
- *Prompt:* "Generate a Python script that renders a VST3 to WAV, loads a reference, and computes phase cancellation RMS."
## 🧪 9. Testing
- Run on macOS/Windows/Linux CI runners
- Inject known bugs → verify detection
- Test with different block sizes (16, 64, 256, 1024)
## 📝 10. Best Practices
- Version reference WAVs with plugin version
- Use lossless formats only (WAV/FLAC)
- Automate delta audio listening on failure
*Skill Version: 1.0.0 | Standards: CI/CD, Headless Audio, FFT Diff | Domain: Real-Time Audio*