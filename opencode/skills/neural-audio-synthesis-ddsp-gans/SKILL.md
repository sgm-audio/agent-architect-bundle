---
name: neural-audio-synthesis-ddsp-gans
description: >-
  Use this skill when the user is working on or asking about DDSP, differentiable DSP, GANs for audio, neural audio synthesis, audio generation models, or differentiable audio processing.
version: 1.0.0
---

# Skill: Neural Audio Synthesis (DDSP & GANs)
## 📖 1. Overview
Hybrid audio synthesis combining Differentiable DSP (DDSP) oscillators/filters with neural timbre modeling (GANs/VAEs) for expressive, physically-plausible sound generation.
## ⚙️ 2. Core Functionality
- Differentiable Oscillators: Wavetable generation with `sinc` interpolation
- Harmonic/Noise Split: Per-frame spectral envelope estimation
- Neural Timbre: GAN/VAE decoder mapping latent vectors to filter parameters
- Real-Time Control: MIDI → latent interpolation → DSP parameter mapping
## 📥📤 3. Input/Output Schema
| Inputs | MIDI note/velocity, latent vectors, DSP coeffs | Outputs | PCM audio, spectral masks, latency-compensated triggers |
## 🏗️ 4. Architecture
`DDSPSynth` class: `oscillator.harmonic_sum(harmonics, phase)` + `filtered_noise(noise_envelope)`. Train with `torch` + `torchaudio`, export to ONNX.
## 🔗 5. Dependencies
`DDSP` (Google), `PyTorch`, `ONNX`, `RTNeural`
## ⚠️ 6. Edge Cases
| Phase Discontinuity | Clicks/pops | Phase accumulator, crossfade windows |
| Latent Collapse | Boring/timbre lock | Regularization, diversity loss during training |
| GPU Fallback | Latency > 20ms | CPU-optimized `RTNeural` path, reduce model depth |
## 🛡️ 7. Constraints
- Latency: < 10ms RT
- Memory: < 50MB model weights
- CPU/GPU: Hybrid fallback
## 🤖 8. Usage
- *Prompt:* "Generate a DDSP oscillator with harmonic series and differentiable amplitude envelope in PyTorch."
## 🧪 9. Testing
- MOS listening tests
- Spectral similarity vs acoustic reference
- Real-time CPU profiling
## 📝 10. Best Practices
- Quantize weights to INT8 for deployment
- Pre-compute harmonic tables
- Document latent space dimensions in UI
*Skill Version: 1.0.0 | Standards: DDSP, GAN/VAE, ONNX | Domain: Audio AI & ML*