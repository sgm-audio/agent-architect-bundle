---
name: music-information-retrieval-mir-techniques
description: >-
  Use this skill when the user is working on or asking about MIR, music information retrieval, beat tracking, onset detection, key/tempo estimation, chroma features, or music analysis algorithms.
version: 1.0.0
---

# Skill: Music Information Retrieval (MIR) Techniques
## 📖 1. Overview
Implements onset detection, pitch tracking (YIN/PYIN), key/tempo estimation to enable context-aware audio plugins and AI agents.
## ⚙️ 2. Core Functionality
- Onset Detection: Spectral flux, complex domain, adaptive thresholding
- Pitch Tracking: YIN autocorrelation, PYIN probabilistic refinement
- Key/Tempo: Chromagram → Krumhansl-Schmuckler, beat tracking via DP/DTW
- Real-Time Buffering: Circular FFT windows, overlap processing
## 📥📤 3. Input/Output Schema
| Inputs | Audio stream, FFT buffers, tempo/pitch priors | Outputs | BPM estimate, MIDI note, key signature, confidence scores |
## 🏗️ 4. Architecture
`yin()` function with `threshold=0.1`, parabolic interpolation. `tempo_estimate` via autocorrelation of energy envelope. Async analysis thread posts to UI via lock-free queue.
## 🔗 5. Dependencies
`librosa` (Python training), `aubio`/custom C++ YIN, `KISSFFT`
## ⚠️ 6. Edge Cases
| Harmonic Confusion | Octave errors | PYIN octave range constraints |
| Silence/Gaps | BPM drift | Decay threshold, reset on >200ms silence |
| Polyphonic Input | Pitch smearing | Multi-peak detection, confidence masking |
## 🛡️ 7. Constraints
- Latency: < 50ms for analysis window
- CPU: < 10% background thread
- Memory: Fixed FFT ring buffer
## 🤖 8. Usage
- *Prompt:* "Implement a real-time YIN pitch tracker with parabolic interpolation and harmonic rejection."
## 🧪 9. Testing
- Ground truth MIDI files vs extracted pitch
- Synthetic polyphonic test cases
- Latency profiling on 2048-sample windows
## 📝 10. Best Practices
- Run analysis on background thread
- Smooth estimates with EMA (`alpha=0.1`)
- Document confidence thresholds in UI
*Skill Version: 1.0.0 | Standards: YIN, Chromagram, MIR spec | Domain: Audio AI & ML*