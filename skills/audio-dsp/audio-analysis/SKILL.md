---
name: audio-analysis
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Audio Analysis", "opencode-migrated"]
    related_skills: []
---


# Skill: Audio Analysis Techniques
## 📖 1. Overview
This skill covers audio analysis techniques including feature extraction, audio classification, pattern recognition, and audio visualization. It encompasses spectral analysis, temporal features, cepstral coefficients, and machine learning approaches for understanding audio content.
## ⚙️ 2. Core Functionality
- **Feature Extraction:** Spectral centroid, rolloff, flux, MFCC, chroma, zero-crossing rate
- **Audio Classification:** Genre, instrument, mood, and speech/music discrimination
- **Pattern Recognition:** Beat detection, onset detection, tempo estimation, key detection
- **Audio Visualization:** Waveforms, spectrograms, mel-scale, pitch tracking
## 📥📤 3. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | Audio signals (time-domain), sample rate, frame size, hop length |
| **Outputs** | Feature vectors, classification labels, onset times, tempo/key estimates |
| **Return Types** | NumPy arrays, pandas DataFrames, JSON feature dictionaries |
## 🏗️ 4. Architecture & Implementation Guide
### 4.1 Feature Extraction Pipeline
```python
import librosa
import numpy as np

def extract_audio_features(y, sr):
    # Spectral features
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    spectral_flux = librosa.onset.onset_strength(y=y, sr=sr)
    
    # Temporal features
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    
    # Cepstral features
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    
    # Chroma features
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    
    return {
        'spectral_centroid': spectral_centroid,
        'spectral_rolloff': spectral_rolloff,
        'spectral_flux': spectral_flux,
        'zero_crossing_rate': zero_crossing_rate,
        'mfcc': mfcc,
        'chroma': chroma
    }
```
### 4.2 Onset Detection
```python
def detect_onsets(y, sr):
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    return onset_times
```
## 🔗 5. Dependencies & Toolchain
- Python 3.7+
- Librosa (audio analysis)
- NumPy (numerical computing)
- SciPy (signal processing)
- Matplotlib/Seaborn (visualization)
- Scikit-learn (machine learning)
- Essentia (alternative audio analysis)
## ⚠️ 6. Edge Cases & Error Handling
| Edge Case | Symptom | Mitigation |
|-----------|---------|------------|
| **Silent Audio** | Zero features, division by zero | Add noise floor, check energy threshold |
| **Variable Length** | Inconsistent feature shapes | Pad/truncate to fixed length, use dynamic time warping |
| **Noise Contamination** | False onsets, spectral skew | Apply noise reduction, spectral gating |
| **Aliasng** | Frequency folding above Nyquist | Ensure proper sampling rate, anti-aliasing filter |
## 🛡️ 7. Real-Time Safety & Performance Constraints
- **Latency:** < 20ms for real-time feature extraction
- **Memory:** Streaming processing for long audio files
- **CPU:** Optimized FFT implementations (FFTW, Intel MKL)
- **Batch Processing:** Parallel feature extraction for datasets
## 🤖 8. Usage Examples & AI Integration
- *Prompt:* "Generate a Python function that extracts MFCC, spectral contrast, and tonnetz features from audio and normalizes them for ML input."
- *Prompt:* "Create an onset detection algorithm using complex domain differential flux with adaptive thresholding."
## 🧪 9. Testing & Validation Strategy
1. **Synthetic Signals:** Test with known signals (sine, noise, clicks)
2. **Benchmark Datasets:** GTZAN for genre, Ballroom for tempo
3. **Comparison with Baselines:** Compare against Essentia, Aubio, VAMP plugins
4. **Cross-Validation:** Leave-one-out for classifier validation
## 📝 10. Best Practices & Maintenance
- Use consistent frame/hop parameters across features
- Normalize features per dataset (zero mean, unit variance)
- Visualize features to inspect quality before modeling
- Document parameter choices and preprocessing steps
- Cache expensive computations (e.g., STFT) for reuse
---
*Skill Version: 1.0.0 | Standards: Librosa, Essentia, VAMP | Domain: Audio Analysis*