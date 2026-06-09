---
name: audio-to-midi
description: >-
  Use this skill when the user is working on or asking about audio to MIDI conversion, pitch detection, polyphonic pitch tracking, melody extraction, or transcribing audio to MIDI.
version: 1.0.0
---

# Skill: Audio-to-MIDI Conversion Techniques
## 📖 1. Overview
This skill covers audio-to-MIDI conversion techniques including automatic transcription, polyphonic transcription, rhythm detection, and MIDI generation from audio. It encompasses converting audio recordings to MIDI, transcribing music, and extracting musical data from audio for further processing and arrangement.
## ⚙️ 2. Core Functionality
- **Monophonic Transcription:** Pitch detection, note onset/offset, velocity estimation
- **Polyphonic Transcription:** Multiple fundamental frequency estimation (MPE), chord recognition
- **Rhythm Detection:** Beat tracking, tempo estimation, quantization, groove extraction
- **MIDI Generation:** Note events, control changes, pitch bend, program changes
## 📥📤 3. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | Audio signals (polyphonic/monophonic), sample rate, tempo prior, instrument model |
| **Outputs** | MIDI note events, controller data, tempo map, time signature, key signature |
| **Return Types** | Standard MIDI files (.mid), MIDI event arrays, JSON transcription results |
## 🏗️ 4. Architecture & Implementation Guide
### 4.1 Monophonic Transcription Pipeline
```python
import librosa
import numpy as np
import pretty_midi

def audio_to_midi_monophonic(audio, sr, onset_threshold=0.5):
    # 1. Onset detection
    onset_env = librosa.onset.onset_strength(y=audio, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=onset_env, 
                                              sr=sr, threshold=onset_threshold)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    
    # 2. Pitch estimation (using YIN or similar)
    pitches, magnitudes = librosa.piptrack(y=audio, sr=sr, fmin=librosa.note_to_hz('C2'),
                                           fmax=librosa.note_to_hz('C7'))
    
    # 3. Track pitch over time
    pitch_track = []
    for t in range(len(onset_frames)):
        index = onset_frames[t]
        pitch_index = np.argmax(magnitudes[:, index])
        pitch = pitches[pitch_index, index]
        pitch_track.append(pitch)
    
    # 4. Create MIDI
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
    
    for i, (onset_time, pitch) in enumerate(zip(onset_times, pitch_track)):
        if i < len(onset_times) - 1:
            offset_time = onset_times[i + 1]
        else:
            offset_time = onset_time + 0.5  # Default note duration
        
        note_number = int(librosa.hz_to_note(pitch)) if pitch > 0 else 60
        note = pretty_midi.Note(
            velocity=100,
            pitch=note_number,
            start=onset_time,
            end=offset_time
        )
        instrument.notes.append(note)
    
    midi.instruments.append(instrument)
    return midi
```
### 4.2 Polyphonic Transcription (using NNLS or Deep Learning)
```python
# Placeholder for polyphonic approach
def audio_to_midi_polyphonic(audio, sr):
    # Would use:
    # 1. Constant-Q Transform or STFT
    # 2. Non-negative matrix factorization (NMF)
    # 3. Deep learning models (CNN/RNN)
    # 4. Multiple F0 estimation (YIN, SWIPE, PEFAC)
    # 5. Note tracking and voice separation
    pass
```
## 🔗 5. Dependencies & Toolchain
- Python: Librosa, NumPy, SciPy, pretty_midi, mir_eval
- Standalone: Melodyne, AudioScore, WIDI Recognition System, Sibelius AudioScore
- VST/AU Plugins: Melodyne Essential, Waves Torque, Celemony Melodyne
- Deep Learning: Onsets and Frames, Transcription models (TensorFlow/PyTorch)
- DSP: Aubio, YIN pitch tracking, FFTW
## ⚠️ 6. Edge Cases & Error Handling
| Edge Case | Symptom | Mitigation |
|-----------|---------|------------|
| **Polyphonic Ambiguity** | Wrong notes, missing voices | Use velocity weighting, harmonic consistency |
| **Pitch Drift** | Inaccurate tuning detection | Reference pitch tracking, tuning estimation |
| **Onset Detection Errors** | Missed notes, false triggers | Adaptive thresholding, spectral flux |
| **Rhythm Quantization** | Stiff, unnatural timing | Groove preservation, swing quantification |
## 🛡️ 7. Real-Time Safety & Performance Constraints
- **Latency:** Not critical for offline transcription
- **Accuracy:** Note onset timing < 20ms error, pitch accuracy > 90%
- **Memory:** Buffer size trade-off between latency and frequency resolution
- **Batch Processing:** Process in chunks for long recordings
## 🤖 8. Usage Examples & AI Integration
- *Prompt:* "Generate a polyphonic transcription system using a CNN architecture that predicts pitch activations per time-frequency bin."
- *Prompt:* "Create a real-time audio-to-MIDI converter for live instrument control with < 50ms latency."
## 🧪 9. Testing & Validation Strategy
1. **Synthetic MIDI:** Generate MIDI, synthesize audio, transcribe back to MIDI
2. **Human Performance:** Record instrument performances, compare transcription
3. **Benchmark Datasets:** MAPS, MedleyDB, Guitar Set for instrument-specific testing
4. **Objective Metrics:** Note precision, recall, F-measure, onset timing error
## 📝 10. Best Practices & Maintenance
- Preprocess audio: noise reduction, normalization, EQ for target instrument
- Consider instrument-specific models (piano, guitar, vocals)
- Post-process MIDI: quantize velocities, remove spurious notes, adjust timing
- Validate with multiple audio formats and sample rates
- Document limitations and expected accuracy for different materials
---
*Skill Version: 1.0.0 | Standards: MIDI 1.0, SP-MIDI, VST Audio Extension | Domain: Audio-to-MIDI Conversion*