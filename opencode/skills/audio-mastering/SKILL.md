---
name: audio-mastering
description: >-
  Use this skill when the user is working on or asking about audio mastering, loudness normalization, LUFS targets, mastering chain, limiting, or preparing audio for distribution.
version: 1.0.0
---

# Skill: Professional Audio Mastering
## 📖 1. Overview
This skill covers professional audio mastering techniques including loudness optimization, EQ, compression, limiting, and final polish for music tracks. It encompasses preparing tracks for distribution, achieving competitive loudness, and adding professional finishing touches to audio productions.
## ⚙️ 2. Core Functionality
- **Loudness Optimization:** LUFS measurement, true peak limiting, dynamic range control
- **Spectral Balancing:** Mastering EQ, harmonic enhancement, mid/side processing
- **Dynamic Control:** Multiband compression, glue compression, transient shaping
- **Limiting & Clipping:** Transparent limiting, overshoot control, dithering
- **Format Preparation:** Sample rate conversion, bit depth reduction, metadata embedding
## 📥📤 3. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | Mixed audio stems, reference tracks, target loudness specs, delivery format requirements |
| **Outputs** | Mastered audio files, loudness reports, waveform visuals, metadata tags |
| **Return Types** | WAV/AIFF/FLAC masters, PDF loudness reports, DDP images for replication |
## 🏗️ 4. Architecture & Implementation Guide
### 4.1 Mastering Chain Template
```python
import numpy as np
import pyloudnorm as pyln
from scipy import signal

def mastering_chain(audio, sr, target_lufs=-14.0):
    # 1. Gain staging
    audio = normalize_peak(audio, -1.0)  # Leave headroom
    
    # 2. Spectral balancing (mastering EQ)
    audio = mastering_eq(audio, sr)
    
    # 3. Dynamic control (multiband compression)
    audio = multiband_compressor(audio, sr)
    
    # 4. Stereo enhancement (optional)
    audio = stereo_enhancer(audio, sr)
    
    # 5. Loudness normalization
    meter = pyln.Meter(sr)  # Create EBU R128 meter
    loudness = meter.integrated_loudness(audio)
    gain = target_lufs - loudness
    audio = pyln.normalize.loudness(audio, loudness, target_lufs)
    
    # 6. True peak limiting
    audio = true_peak_limiter(audio, sr, -1.0)  # -1 dBTP ceiling
    
    # 7. Dithering (if bit depth reduction)
    audio = dither_audio(audio, target_bit_depth=16)
    
    return audio
```
### 4.2 Reference-Based Matching
```python
def match_to_reference(master, reference, sr):
    # Match spectral balance
    master_eq = match_eq_spectrum(master, reference, sr)
    
    # Match loudness characteristics
    master_loudness = match_loudness_range(master, reference, sr)
    
    # Match stereo width
    master_stereo = match_stereo_width(master, reference, sr)
    
    return master_stereo
```
## 🔗 5. Dependencies & Toolchain
- DAWs: Pro Tools, Logic Pro, Ableton Live, Reaper
- Plugins: iZotope Ozone, Waves SSL, FabFilter Pro-L 2, Sonnox Oxford
- Metering: Youlean Loudness Meter, Insight, Waves WLM
- Analysis: RX Spectral Declare, MeldaProduction MAnalyzer
- Python: pyloudnorm, librosa, scipy, numpy
## ⚠️ 6. Edge Cases & Error Handling
| Edge Case | Symptom | Mitigation |
|-----------|---------|------------|
| **Over-Compression** | Pumping, breathing, loss of dynamics | Use gentle ratios, longer attack/release |
| **Frequency Masking** | Muffled highs, boomy lows | Surgical EQ, mid/side separation |
| **True Peak Overshoots** | Distortion after conversion | True peak limiting, adequate headroom |
| **Format Conversion Artifacts** | Aliasing, quantization noise | Proper SRC, dithering, noise shaping |
## 🛡️ 7. Real-Time Safety & Performance Constraints
- **Latency:** Not critical for offline mastering
- **Accuracy:** Precise loudness measurement (EBU R128)
- **Monitoring:** Calibrated monitoring environment
- **Reference:** A/B comparison with reference tracks
## 🤖 8. Usage Examples & AI Integration
- *Prompt:* "Generate a mastering chain that achieves -14 LUFS integrated loudness with <1 dBTP true peak."
- *Prompt:* "Create a reference matching algorithm that adjusts EQ and dynamics to match a target master."
## 🧪 9. Testing & Validation Strategy
1. **Loudness Compliance:** Verify LUFS and true peak against broadcast standards
2. **Spectral Analysis:** Compare frequency spectrum with reference masters
3. **Dynamic Range:** Measure DR (Dynamic Range) and crest factor
4. **Blind Listening:** A/B testing with experienced mastering engineers
## 📝 10. Best Practices & Maintenance
- Monitor in acoustically treated room with calibrated speakers
- Take frequent ear breaks to avoid fatigue
- Use multiple reference systems (headphones, car, phone)
- Document processing chain for recall and revisions
- Stay updated on loudness standards (EBU R128, ATSC A/85, Apple Music)
---
*Skill Version: 1.0.0 | Standards: EBU R128, ITU-R BS.1770, AES Recommendations | Domain: Audio Mastering*