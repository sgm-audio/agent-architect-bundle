---
name: real-time-neural-timbre-transfer
description: >-
  Use this skill when the user is working on or asking about timbre transfer, neural style transfer for audio, real-time voice/instrument conversion, or neural audio effects.
version: 1.0.0
---

# SKILL: Real-Time Neural Timbre Transfer

## CAPABILITIES
- Transfer timbre characteristics from one audio signal to another in real-time
- Implement lightweight neural networks (U-Net, GAN variants) for audio processing
- Maintain pitch and timing information while altering spectral characteristics
- Achieve <10ms latency for interactive applications
- Work with various audio sources (vocals, instruments, synthesizers)

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Source audio (to transfer timbre from) | Transferred audio with target timbre |
| Target audio (to apply timbre to) | Processed audio preserving original pitch/timing |
| Neural network model weights | Real-time processed audio stream |
| Latency requirements (<10ms, <20ms) | Optimized model architecture and inference pipeline |
| Audio sample rate and bit depth | Processed audio with matching specifications |

## IMPLEMENTATION PATTERN

```python
# Real-Time Neural Timbre Transfer System
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import librosa
from typing import Tuple, Optional

# Lightweight U-Net architecture for timbre transfer
class TimbreTransferNet(nn.Module):
    def __init__(self, 
                 input_channels: int = 1,
                 base_filters: int = 32,
                 depth: int = 4):
        super().__init__()
        
        self.depth = depth
        self.encoders = nn.ModuleList()
        self.decoders = nn.ModuleList()
        self.pools = nn.ModuleList()
        self.upsamples = nn.ModuleList()
        
        # Encoder blocks
        for i in range(depth):
            in_ch = input_channels if i == 0 else base_filters * (2 ** (i-1))
            out_ch = base_filters * (2 ** i)
            self.encoders.append(
                nn.Sequential(
                    nn.Conv1d(in_ch, out_ch, kernel_size=3, padding=1),
                    nn.BatchNorm1d(out_ch),
                    nn.ReLU(inplace=True),
                    nn.Conv1d(out_ch, out_ch, kernel_size=3, padding=1),
                    nn.BatchNorm1d(out_ch),
                    nn.ReLU(inplace=True)
                )
            )
            if i < depth - 1:  # No pooling after last encoder
                self.pools.append(nn.MaxPool1d(kernel_size=2, stride=2))
        
        # Decoder blocks
        for i in range(depth-1):
            in_ch = base_filters * (2 ** (depth - 1 - i))
            out_ch = base_filters * (2 ** (depth - 2 - i))
            self.upsamples.append(
                nn.ConvTranspose1d(in_ch, out_ch, kernel_size=2, stride=2)
            )
            self.decoders.append(
                nn.Sequential(
                    nn.Conv1d(out_ch * 2, out_ch, kernel_size=3, padding=1),
                    nn.BatchNorm1d(out_ch),
                    nn.ReLU(inplace=True),
                    nn.Conv1d(out_ch, out_ch, kernel_size=3, padding=1),
                    nn.BatchNorm1d(out_ch),
                    nn.ReLU(inplace=True)
                )
            )
        
        # Final layer
        self.final_conv = nn.Conv1d(base_filters, input_channels, kernel_size=1)
    
    def forward(self, x):
        # Encoder
        encoder_outputs = []
        for i in range(self.depth):
            x = self.encoders[i](x)
            encoder_outputs.append(x)
            if i < self.depth - 1:
                x = self.pools[i](x)
        
        # Decoder
        for i in range(self.depth-1):
            x = self.upsamples[i](x)
            # Concatenate with corresponding encoder output
            x = torch.cat([x, encoder_outputs[-(i+2)]], dim=1)
            x = self.decoders[i](x)
        
        x = self.final_conv(x)
        return x

# Real-time processing wrapper
class RealTimeTimbreTransfer:
    def __init__(self, 
                 model_path: str,
                 sample_rate: int = 48000,
                 frame_size: int = 512,
                 hop_size: int = 256):
        self.sample_rate = sample_rate
        self.frame_size = frame_size
        self.hop_size = hop_size
        
        # Load model
        self.model = TimbreTransferNet()
        self.model.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.model.eval()
        
        # Initialize buffers for overlap-add
        self.input_buffer = np.zeros(frame_size, dtype=np.float32)
        self.output_buffer = np.zeros(frame_size, dtype=np.float32)
        self.overlap_buffer = np.zeros(hop_size, dtype=np.float32)
        
        # Statistics for normalization (should match training)
        self.mean = 0.0
        self.std = 0.5
        
    def process_frame(self, audio_frame: np.ndarray) -> np.ndarray:
        """Process a single audio frame"""
        # Normalize
        normalized = (audio_frame - self.mean) / self.std
        
        # Convert to tensor
        input_tensor = torch.from_numpy(normalized).float().unsqueeze(0).unsqueeze(0)
        
        # Inference
        with torch.no_grad():
            output_tensor = self.model(input_tensor)
        
        # Convert back to numpy
        output = output_tensor.squeeze().numpy()
        
        # Denormalize
        denormalized = output * self.std + self.mean
        
        return denormalized
    
    def process_audio(self, audio: np.ndarray) -> np.ndarray:
        """Process full audio with overlap-add"""
        output = np.zeros_like(audio)
        window = np.hanning(self.frame_size)
        
        # Process in frames with hop size
        for i in range(0, len(audio) - self.frame_size + 1, self.hop_size):
            frame = audio[i:i+self.frame_size]
            processed_frame = self.process_frame(frame)
            
            # Apply window and overlap-add
            windowed = processed_frame * window
            output[i:i+self.frame_size] += windowed
        
        # Normalize by window overlap (for perfect reconstruction with 50% overlap)
        if self.hop_size == self.frame_size // 2:
            output /= np.sum(window[::2])  # Approximate normalization
            
        return output

# Alternative: Real-time vocoder-based approach
class VocoderTimbreTransfer:
    def __init__(self, 
                 model_path: str,
                 sample_rate: int = 48000,
                 fft_size: int = 2048,
                 hop_size: int = 512):
        self.sample_rate = sample_rate
        self.fft_size = fft_size
        self.hop_size = hop_size
        
        # Load magnitude transformation network
        self.mag_net = TimbreTransferNet(
            input_channels=1,  # Magnitude spectrum
            base_filters=32,
            depth=4
        )
        self.mag_net.load_state_dict(torch.load(model_path, map_location='cpu'))
        self.mag_net.eval()
        
        # Phase vocoder components
        self.window = np.hanning(fft_size)
        
    def process_audio(self, audio: np.ndarray) -> np.ndarray:
        """Process audio using phase vocoder approach"""
        # STFT
        stft = librosa.stft(audio, 
                           n_fft=self.fft_size, 
                           hop_length=self.hop_size,
                           window=self.window)
        
        magnitude = np.abs(stft)
        phase = np.angle(stft)
        
        # Process magnitude (timbre)
        magnitude_tensor = torch.from_numpy(magnitude).float().unsqueeze(0).unsqueeze(0)
        
        with torch.no_grad():
            processed_mag_tensor = self.mag_net(magnitude_tensor)
        
        processed_magnitude = processed_mag_tensor.squeeze().numpy()
        
        # Reconstruct audio
        processed_stft = processed_magnitude * np.exp(1j * phase)
        processed_audio = librosa.istft(processed_stft,
                                       hop_length=self.hop_size,
                                       window=self.window,
                                       length=len(audio))
        
        return processed_audio
```

## EDGE CASES & FALLBACKS
- **Latency Spikes**: Use smaller frame sizes, optimize model inference, or implement predictive buffering
- **Quality Degradation**: Fall back to parametric EQ or vocoder-based timbre transfer
- **Pitch Tracking Failure**: Use robust pitch estimation algorithms (YIN, SWIPE) or work in frame-based domain
- **Memory Constraints**: Quantize model weights, use model pruning, or implement recursive processing
- **Audio Dropouts**: Implement buffer underflow protection with silence generation or repetition
- **Model Incompatibility**: Validate model architecture matches expected input/output dimensions
- **Numerical Instability**: Add gradient clipping during training, use stable normalization techniques
- **Frequency Aliasing**: Ensure proper sampling rates and apply anti-aliasing filters when needed
- **Timbre Drift**: Implement adaptive normalization or running statistics for long audio sequences

## INTEGRATION POINTS
- Audio Libraries: Librosa, Torchaudio, SciPy, NumPy
- Deep Learning: PyTorch, TensorFlow, ONNX Runtime
- Audio Effects: VST3, AU, AAX, CLAP plugins
- Real-Time Frameworks: JACK, ASIO, CoreAudio, WASAPI
- Speech Processing: WORLD vocoder, STRAIGHT, SNR-based enhancements
- Musical Instrument Processing: Modalysis, physical modeling synthesizers
- Pitch Detection: YIN, pYIN, SWIPE, PEFAC algorithms
- Vocoders: WORLD, STRAIGHT, LPCNet, WaveNet
- Feature Extraction: MFCC, spectral contrast, chroma, zero-crossing rate
- Deployment: TensorRT, TorchScript, CoreML for optimized inference
- Hardware Acceleration: GPU (CUDA), DSPs, NPUs for embedded deployment

## EXECUTION EXAMPLES

**Input:** "Transfer the timbre of a violin to a human voice in real-time"
**Output:**
```python
# Initialize timbre transfer system
timbre_transfer = RealTimeTimbreTransfer(
    model_path="violin_to_voice_timbre_net.pt",
    sample_rate=48000,
    frame_size=512,
    hop_size=256
)

# Process audio stream in real-time (callback-based)
def audio_callback(indata, outdata, frames, time, status):
    # indata: input audio buffer (numpy array)
    # outdata: output audio buffer (to fill)
    
    # Process the frame
    processed = timbre_transfer.process_frame(indata[:, 0])  # Mono input
    
    # Output to both channels (or process stereo appropriately)
    outdata[:, 0] = processed  # Left channel
    outdata[:, 1] = processed  # Right channel (for stereo output)

# For file-based processing
def process_audio_file(input_path, output_path):
    # Load audio
    audio, sr = librosa.load(input_path, sr=48000, mono=True)
    
    # Process
    processed_audio = timbre_transfer.process_audio(audio)
    
    # Save
    sf.write(output_path, processed_audio, sr)
```

**Input:** "Create a real-time guitar-to-saxophone timbre transformer"
**Output:**
```python
# Guitar to saxophone timbre transfer
guitar_to_sax = RealTimeTimbreTransfer(
    model_path="guitar_to_saxophone_timbre_net.pt",
    sample_rate=44100,
    frame_size=1024,  # Larger frame for better frequency resolution
    hop_size=512
)

# For live processing with JACK or similar
def process_jack_frames(input_buffer, output_buffer):
    # Convert to numpy arrays
    input_audio = np.frombuffer(input_buffer, dtype=np.float32)
    
    # Process
    output_audio = guitar_to_sax.process_audio(input_audio)
    
    # Convert back to bytes
    output_buffer[:] = output_audio.tobytes()
```