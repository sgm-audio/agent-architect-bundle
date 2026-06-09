---
name: source-separation-pipeline-integration
description: >-
  Use this skill when the user is working on or asking about source separation, stem separation, Demucs, Spleeter, vocal isolation, or integrating audio separation models into a pipeline.
version: 1.0.0
---

# Skill: Source Separation Pipeline Integration
## 📖 1. Overview
Integrates open-source stem separation models (Demucs, HTDemucs, Spleeter) into local utilities for vocal/drums/bass/melody splitting.
## ⚙️ 2. Core Functionality
- Model Inference: ONNX/PyTorch → audio → 4-stem output
- Chunk Processing: Overlap-add to handle long files without memory blowup
- Phase Alignment: Ensure separated stems sum to original
- Post-Processing: Residual subtraction, artifact reduction
## 📥📤 3. Input/Output Schema
| Inputs | Mixed WAV, model path, chunk size, output format | Outputs | Stem WAVs, confidence masks, processing stats |
## 🏗️ 4. Architecture
Stream audio in 10s chunks with 2s overlap. Pass through `HTDemucs` ONNX model. Reconstruct via `scipy.signal.oaconvolve`. Export stems.
## 🔗 5. Dependencies
`demucs`, `onnxruntime`, `torchaudio`, `libsndfile`
## ⚠️ 6. Edge Cases
| Chunk Boundary Artifacts | Clicks at seams | Crossfade overlap-add windows |
| Phase Cancellation | Missing instruments | Use `residual = mix - sum(stems)` |
| High RAM Usage | Swap thrashing | Limit chunk size to 4GB RAM, use float32 streaming |
## 🛡️ 7. Constraints
- Latency: < 1x real-time on CPU
- Memory: < 6GB peak
- Output: 24-bit WAV, phase-coherent
## 🤖 8. Usage
- *Prompt:* "Generate a Python pipeline that chunks a 5-minute track, runs Demucs ONNX, and overlaps stems without artifacts."
## 🧪 9. Testing
- SDR/SIR/SAR metrics against ground truth
- Phase sum test (stems → mix diff < -40dB)
- CPU/memory profiling
## 📝 10. Best Practices
- Pre-quantize models for CPU
- Allow stem mixing UI with solo/mute
- Cache results by hash of input file
*Skill Version: 1.0.0 | Standards: Demucs, ONNX, Source Separation | Domain: Audio AI & ML*