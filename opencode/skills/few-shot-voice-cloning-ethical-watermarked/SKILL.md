---
name: few-shot-voice-cloning-ethical-watermarked
description: >-
  Use this skill when the user is working on or asking about voice cloning, few-shot TTS, ethical voice synthesis, audio watermarking, or responsible voice AI.
version: 1.0.0
---

# SKILL: Few-Shot Voice Cloning (Ethical & Watermarked)

## CAPABILITIES
- Clone voices from very short audio samples (few-shot learning)
- Implement ethical safeguards including consent verification and watermarking
- Generate synthetic speech that preserves speaker identity and speaking style
- Support real-time or near-real-time voice generation for interactive applications
- Detect and prevent misuse through speaker verification and audio watermarking

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Short audio samples of target voice (few seconds to minutes) | Cloned voice model or embedding |
| Text to synthesize | Synthetic speech audio in target voice |
| Consent and verification signals | Ethically compliant voice generation |
| Watermarking parameters | Audio with embedded imperceptible watermark |
| Real-time constraints | Low-latency voice synthesis pipeline |

## IMPLEMENTATION PATTERN

```python
# Few-Shot Voice Cloning System with Ethical Safeguards
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import librosa
from typing import Optional, Tuple
import hashlib
import os

# Speaker encoder (extracts voice embedding from short sample)
class SpeakerEncoder(nn.Module):
    def __init__(self, 
                 input_dim: int = 80,  # Mel-spectrogram channels
                 embedding_dim: int = 256,
                 num_layers: int = 3):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, 
                           embedding_dim, 
                           num_layers=num_layers, 
                           batch_first=True,
                           bidirectional=True)
        self.projection = nn.Linear(embedding_dim * 2, embedding_dim)
    
    def forward(self, mel_spectrogram):
        # mel_spectrogram: (batch, time, mel_bins)
        self.lstm.flatten_parameters()
        outputs, (hidden, cell) = self.lstm(mel_spectrogram)
        # Concatenate forward and backward hidden states
        hidden = torch.cat((hidden[-2,:,:], hidden[-1,:,:]), dim=1)
        embedding = self.projection(hidden)
        return embedding  # (batch, embedding_dim)

# Vocoder (generates audio from mel-spectrogram and speaker embedding)
class VoiceConverter(nn.Module):
    def __init__(self, 
                 mel_dim: int = 80,
                 embedding_dim: int = 256,
                 hidden_dim: int = 512):
        super().__init__()
        self.embedding_proj = nn.Linear(embedding_dim, mel_dim)
        self.lstm = nn.LSTM(mel_dim * 2, hidden_dim, num_layers=2, batch_first=True)
        self.postnet = nn.Sequential(
            nn.Conv1d(hidden_dim, hidden_dim, kernel_size=5, padding=2),
            nn.BatchNorm1d(hidden_dim),
            nn.Tanh(),
            nn.Conv1d(hidden_dim, mel_dim, kernel_size=5, padding=2)
        )
    
    def forward(self, mel_spectrogram, speaker_embedding):
        # mel_spectrogram: (batch, time, mel_dim)
        # speaker_embedding: (batch, embedding_dim)
        # Project embedding to mel dimension
        embedded = self.embedding_proj(speaker_embedding)  # (batch, mel_dim)
        # Expand embedding to match time dimension
        embedded = embedded.unsqueeze(1).expand(-1, mel_spectrogram.size(1), -1)
        # Concatenate mel spectrogram and embedded speaker info
        combined = torch.cat([mel_spectrogram, embedded], dim=-1)  # (batch, time, 2*mel_dim)
        # Process through LSTM
        self.lstm.flatten_parameters()
        outputs, _ = self.lstm(combined)
        # Apply postnet
        residual = self.postnet(outputs.transpose(1, 2))  # (batch, hidden_dim, time)
        output = outputs.transpose(1, 2) + residual  # (batch, time, mel_dim)
        return output.transpose(1, 2)  # (batch, mel_dim, time)

# Watermarking module (imperceptible audio watermark)
class AudioWatermarker:
    def __init__(self, 
                 key: str = "default_key",
                 strength: float = 0.01):
        self.key = key
        self.strength = strength
        # Generate pseudo-noise sequence from key
        self.seed = hashlib.sha256(key.encode()).hexdigest()
        self.rng = np.random.RandomState(seed=int(self.seed, 16) % 2**32)
    
    def embed_watermark(self, audio: np.ndarray) -> np.ndarray:
        """Embed imperceptible watermark in audio"""
        # Generate watermark signal (pseudo-noise)
        watermark = self.rng.normal(0, self.strength, len(audio))
        
        # Apply in frequency domain to make it less perceptible
        # Simple approach: add directly (for demonstration)
        # In practice, use spread spectrum or echo hiding
        watermarked = audio + watermark
        
        # Ensure we don't clip
        watermarked = np.clip(watermarked, -1.0, 1.0)
        return watermarked
    
    def extract_watermark(self, audio: np.ndarray) -> bool:
        """Extract and verify watermark presence"""
        # Simple correlation-based detection (for demonstration)
        # In practice, use more robust detection
        watermark = self.rng.normal(0, self.strength, len(audio))
        correlation = np.correlate(audio, watermark, mode='valid')
        # Threshold-based detection
        return np.max(np.abs(correlation)) > len(audio) * self.strength * 0.5

# Ethical voice cloning system
class EthicalVoiceCloner:
    def __init__(self, 
                 encoder_path: str,
                 converter_path: str,
                 consent_required: bool = True):
        self.encoder = SpeakerEncoder()
        self.converter = VoiceConverter()
        self.watermarker = AudioWatermarker()
        self.consent_required = consent_required
        
        # Load pre-trained weights (in practice)
        # self.encoder.load_state_dict(torch.load(encoder_path))
        # self.converter.load_state_dict(torch.load(converter_path))
        self.encoder.eval()
        self.converter.eval()
    
    def verify_consent(self, 
                      consent_proof: str, 
                      target_voice_sample: np.ndarray) -> bool:
        """Verify consent for voice cloning"""
        if not self.consent_required:
            return True
        
        # In practice, this would involve:
        # 1. Checking a signed consent document or recording
        # 2. Verifying that the consent matches the target voice
        # 3. Checking expiration or scope of consent
        
        # For this example, we'll do a simple voice match check
        # between the consent proof and the target voice sample
        # (This is a placeholder - real implementation would be more robust)
        try:
            # Extract features from consent proof and target sample
            consent_features = self.extract_voice_features(consent_proof)
            target_features = self.extract_voice_features(target_voice_sample)
            
            # Compare features (cosine similarity)
            similarity = np.dot(consent_features, target_features) / (
                np.linalg.norm(consent_features) * np.linalg.norm(target_features))
            
            return similarity > 0.8  # Threshold for consent verification
        except:
            return False
    
    def extract_voice_features(self, audio: np.ndarray) -> np.ndarray:
        """Extract voice-consistent features (simplified)"""
        # In practice, use speaker embedding or i-vector
        # For demonstration, use MFCC mean
        mfcc = librosa.feature.mfcc(y=audio, sr=22050, n_mfcc=13)
        return np.mean(mfcc, axis=1)
    
    def clone_voice(self, 
                   target_voice_sample: np.ndarray,
                   text_to_synthesize: str,
                   consent_proof: Optional[str] = None) -> np.ndarray:
        """Clone voice with ethical safeguards"""
        # Step 1: Verify consent
        if not self.verify_consent(consent_proof or "", target_voice_sample):
            raise PermissionError("Consent verification failed for voice cloning")
        
        # Step 2: Extract speaker embedding from short sample
        # Preprocess audio to mel-spectrogram
        mel_spectrogram = self.audio_to_mel(target_voice_sample)
        mel_tensor = torch.from_numpy(mel_spectrogram).float().unsqueeze(0)
        
        # Get speaker embedding
        with torch.no_grad():
            speaker_embedding = self.encoder(mel_tensor)
        
        # Step 3: Convert text to mel-spectrogram (using TTS model)
        # In practice, use a text-to-mel model (like Tacotron 2 or FastSpeech)
        # For demonstration, we'll use a placeholder
        target_mel = self.text_to_mel(text_to_synthesize)
        target_mel_tensor = torch.from_numpy(target_mel).float().unsqueeze(0)
        
        # Step 4: Generate mel-spectrogram in target voice
        with torch.no_grad():
            converted_mel = self.converter(target_mel_tensor, speaker_embedding)
        
        # Step 5: Convert mel-spectrogram to audio (using vocoder)
        # In practice, use a neural vocoder (like WaveNet, WaveGlow, or HiFi-GAN)
        # For demonstration, we'll use Griffin-Lim
        audio = self.mel_to_audio(converted_mel.squeeze().numpy())
        
        # Step 6: Embed ethical watermark
        watermarked_audio = self.watermarker.embed_watermark(audio)
        
        return watermarked_audio
    
    def audio_to_mel(self, audio: np.ndarray) -> np.ndarray:
        """Convert audio to mel-spectrogram"""
        mel_spectrogram = librosa.feature.melspectrogram(
            y=audio, 
            sr=22050, 
            n_fft=2048, 
            hop_length=512,
            n_mels=80
        )
        return librosa.power_to_db(mel_spectrogram, ref=np.max)
    
    def mel_to_audio(self, mel_spectrogram: np.ndarray) -> np.ndarray:
        """Convert mel-spectrogram to audio"""
        # Convert from log mel to power
        mel_power = librosa.db_to_power(mel_spectrogram, ref=np.max)
        # Use Griffin-Lim to reconstruct audio
        audio = librosa.feature.inverse.mel_to_audio(
            mel_power, 
            sr=22050, 
            n_fft=2048, 
            hop_length=512
        )
        return audio
    
    def text_to_mel(self, text: str) -> np.ndarray:
        """Convert text to mel-spectrogram (placeholder)"""
        # In practice, use a TTS model
        # For demonstration, return a random mel-spectrogram of appropriate length
        # This is NOT a real implementation
        estimated_length = len(text) * 50  # Rough estimate
        return np.random.randn(80, estimated_length)

# Usage example with ethical safeguards
def synthesize_speech_ethically(target_voice_sample, text, consent_recording=None):
    """Ethical voice cloning pipeline"""
    # Initialize cloner (in practice, load pre-trained models)
    cloner = EthicalVoiceCloner(
        encoder_path="speaker_encoder.pt",
        converter_path="voice_converter.pt",
        consent_required=True
    )
    
    # Synthesize speech
    try:
        synthesized_audio = cloner.clone_voice(
            target_voice_sample=target_voice_sample,
            text_to_synthesize=text,
            consent_proof=consent_recording
        )
        return synthesized_audio
    except PermissionError as e:
        print(f"Ethical error: {e}")
        return None
    except Exception as e:
        print(f"Error during voice cloning: {e}")
        return None
```

## EDGE CASES & FALLBACKS
- **Insufficient Voice Sample**: Fall back to average voice or request more samples
- **Consent Verification Failure**: Refuse to clone voice and log the attempt
- **Watermark Detection Failure**: Apply stronger watermark or use alternative method
- **Voice Similarity False Positives**: Use multi-factor verification (voice + document)
- **Real-Time Latency**: Use streaming synthesis or reduce model complexity
- **Audio Quality Degradation**: Implement post-processing filters or use higher quality vocoders
- **Misuse Attempts**: Log attempts and implement rate limiting or account suspension
- **Cross-Language Cloning**: Use language-specific models or phonetic transcription
- **Emotional Style Transfer**: Prosody modeling or emotional embedding spaces

## INTEGRATION POINTS
- Speech Synthesis: Tacotron 2, FastSpeech 2, VITS, Transformers
- Speaker Encoding: GE2E, x-vectors, d-vectors, ECAPA-TDNN
- Vocoders: WaveNet, WaveGlow, HiFi-GAN, MB-MelGAN
- Watermarking: Spread spectrum, echo hiding, phase coding
- Consent Verification: Blockchain-based consent, digital signatures, biometrics
- Audio Processing: Librosa, Torchaudio, SciPy, Kaldi
- Real-Time Frameworks: JACK, ASIO, CoreAudio, WebAudio API
- Deployment: ONNX, TorchScript, TensorRT for low-latency inference
- Ethical Frameworks: IEEE 7010, ISO/IEC 24745, GDPR Article 9
- Monitoring: Usage logging, abuse detection, consent tracking

## EXECUTION EXAMPLES

**Input:** "Clone a voice from a 5-second consent recording to synthesize audiobook narration"
**Output:**
```python
# Load the 5-second consent recording and target voice sample (same person)
consent_audio, sr = librosa.load("consent_recording.wav", sr=None)
target_audio, sr = librosa.load("target_voice_sample.wav", sr=None)  # Should match consent

# Text to synthesize
text = "Once upon a time, in a faraway kingdom..."

# Synthesize with ethical safeguards
synthesized = synthesize_speech_ethically(
    target_voice_sample=target_audio,
    text=text,
    consent_recording=consent_audio
)

if synthesized is not None:
    sf.write("audiobook_narration.wav", synthesized, sr)
else:
    print("Voice cloning failed due to ethical concerns")
```

**Input:** "Create a real-time voice cloning system for live customer service avatars"
**Output:**
```python
# Real-time voice cloning for avatars
class RealTimeVoiceAvatar:
    def __init__(self):
        # Initialize models (pre-loaded for low latency)
        self.encoder = SpeakerEncoder().eval()
        self.converter = VoiceConverter().eval()
        self.watermarker = AudioWatermarker(key="avatar_service_2024")
        # ... (rest of initialization)
    
    def process_avatar_speech(self, text_input, avatar_voice_sample):
        # Verify consent for this avatar session (pre-verified)
        # Extract speaker embedding once per session
        # Synthesize text to speech in real-time chunks
        # Apply watermark to output stream
        pass
```