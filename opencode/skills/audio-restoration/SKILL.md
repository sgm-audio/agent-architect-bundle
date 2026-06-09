---
name: audio-restoration
description: >-
  Use this skill when the user is working on or asking about audio restoration, noise reduction, click removal, hum elimination, de-noising, or cleaning up degraded audio recordings.
version: 1.0.0
---

# Skill: Professional Audio Restoration Techniques
## 📖 1. Overview
This skill covers professional audio restoration techniques including noise reduction, click and pop removal, hum elimination, audio repair, and archival restoration. It encompasses cleaning up old recordings, removing unwanted noise, repairing damaged audio, and restoring archival material for preservation and remastering.
## ⚙️ 2. Core Functionality
- **Noise Reduction:** Adaptive filtering, spectral subtraction, Wiener filtering
- **Click & Pop Removal:** Interpolation, wavelet detection, median filtering
- **Hum Elimination:** Notch filtering, harmonic cancellation, adaptive notch
- **Clickless Declicking:** Spectral interpolation, morphological operations
- **Broadcast Restoration:** Tape hiss reduction, vinyl crackle removal, shellac noise
## 📥📤 3. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | Degraded audio signals, noise profiles, damage markers, restoration parameters |
| **Outputs** | Cleaned audio signals, noise reduction maps, artifact reports, quality metrics |
| **Return Types** | Restored audio files, before/after comparisons, processing logs |
## 🏗️ 4. Architecture & Implementation Guide
### 4.1 Noise Reduction Pipeline
```python
import numpy as np
import librosa
from scipy import signal
import noisereduce as nr

def restore_audio(audio, sr, noise_clip=None):
    # 1. Noise profiling
    if noise_clip is None:
        # Estimate noise from beginning/end
        noise_clip = audio[:int(0.5*sr)]  # First 0.5 seconds
    
    # 2. Spectral gating
    reduced_noise = nr.reduce_noise(y=audio, sr=sr, y_noise=noise_clip, 
                                   stationary=False, prop_decrease=0.75)
    
    # 3. Click/pop detection and removal
    clicks = detect_clicks(reduced_noise, sr)
    audio_declicked = interpolate_clicks(reduced_noise, clicks, sr)
    
    # 4. Hum removal (50/60 Hz and harmonics)
    audio_dehummed = remove_hum(audio_declicked, sr, [50, 60])
    
    # 5. Final EQ balancing
    audio_restored = spectral_balance(audio_dehummed, sr)
    
    return audio_restored
```
### 4.2 Click Detection & Interpolation
```python
def detect_clicks(audio, sr, threshold=0.1):
    # Energy-based click detection
    energy = np.abs(audio)
    diff = np.diff(energy, prepend=0)
    clicks = np.where(diff > threshold * np.max(diff))[0]
    return clicks

def interpolate_clicks(audio, click_indices, sr):
    audio_copy = audio.copy()
    for idx in click_indices:
        # Interpolate using neighboring samples
        start = max(0, idx - 10)
        end = min(len(audio), idx + 11)
        if start < idx and end > idx + 1:
            audio_copy[idx] = np.mean(audio[start:idx]) * 0.5 + np.mean(audio[idx+1:end]) * 0.5
    return audio_copy
```
## 🔗 5. Dependencies & Toolchain
- Python: NumPy, SciPy, Librosa, noisereduce, scikit-learn
- Standalone: iZotope RX, Cedar Cambridge, Waves X-Noise, SoundSoap Pro
- Plugins: RX Spectral Declick, Waves X-Click, Sonnox DeBuzzer
- FFmpeg: For format conversion and filtering
- SoX: For noise profiling and basic filtering
## ⚠️ 6. Edge Cases & Error Handling
| Edge Case | Symptom | Mitigation |
|-----------|---------|------------|
| **Over-Processing** | "Underwater" sound, artifacts | Conservative processing, A/B comparison |
| **Signal Cancellation** | Loss of wanted signal | Side-chain processing, selective gating |
| **Residual Noise** | Pumpy noise floor | Multi-stage processing, spectral shaping |
| **Tonal Artifacts** | Musical noise, warbling | Phase vocoder, spectral interpolation |
## 🛡️ 7. Real-Time Safety & Performance Constraints
- **Latency:** Not critical for offline restoration
- **Accuracy:** Transparent processing with minimal artifacts
- **Monitoring:** High-resolution metering and spectral display
- **Reference:** Comparison with clean reference when available
## 🤖 8. Usage Examples & AI Integration
- *Prompt:* "Generate an adaptive noise reduction algorithm that learns noise profile from silent sections."
- *Prompt:* "Create a click removal system using morphological operations on the audio envelope."
## 🧪 9. Testing & Validation Strategy
1. **Known Distortion:** Add controlled noise/distortion, measure removal efficiency
2. **Transparency Testing:** Process clean audio, verify no degradation
3. **Subjective Testing:** Blind listening tests with expert listeners
4. **Objective Metrics:** SNR improvement, PESQ, STOI scores
## 📝 10. Best Practices & Maintenance
- Always process on copies, preserve originals
- Work in high resolution (24-bit/96kHz or higher)
- Use multiple passes for severe damage rather than aggressive single pass
- Document all processing steps for reproducibility
- Calibrate monitoring system for accurate assessment
- Archive both original and restored versions with documentation
---
*Skill Version: 1.0.0 | Standards: AES69-2008, EBU Tech 3276, ARSC Guidelines | Domain: Audio Restoration*