---
name: neural-ambisonics-spatial-audio-synthesis
description: >-
  Use this skill when the user is working on or asking about Ambisonics, spatial audio, binaural rendering, neural spatial audio, HOA (Higher Order Ambisonics), or 3D audio synthesis.
version: 1.0.0
---

# SKILL: Neural Ambisonics & Spatial Audio Synthesis

## CAPABILITIES
- Generate immersive 3D audio scenes using neural networks
- Synthesize early reflections and late reverb for Dolby Atmos or Sony 360 Reality Audio
- Create binaural renderings from Ambisonics (B-format) using HRTF interpolation
- Optimize spatial audio rendering for real-time applications
- Integrate with object-based audio formats and metadata

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Audio sources (mono, stereo, or multi-channel) | Spatial audio scene (Ambisonics, binaural, or object-based) |
| Room characteristics (size, materials, geometry) | Reverberation and early reflections |
| Source positions (azimuth, elevation, distance) | Spatialized audio signals |
| HRTF datasets or individual measurements | Binaural rendering filters |
| Real-time constraints (<20ms latency) | Optimized spatialization pipeline |

## IMPLEMENTATION PATTERN

```python
# Neural Ambisonics and Spatial Audio Synthesizer
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import librosa
from typing import Tuple, List, Optional

# Neural network for generating Ambisonics B-format from mono/stereo input
class AmbisonicsSynthesizer(nn.Module):
    def __init__(self, 
                 input_channels: int = 2,  # Stereo input
                 order: int = 1,         # Ambisonics order (0=mono, 1=first order, 2=second order)
                 base_filters: int = 32):
        super().__init__()
        
        self.order = order
        self.n_channels = (order + 1) ** 2  # Number of Ambisonics channels
        
        # Processing network
        self.conv1 = nn.Conv1d(input_channels, base_filters, kernel_size=15, padding=7)
        self.conv2 = nn.Conv1d(base_filters, base_filters * 2, kernel_size=15, padding=7)
        self.conv3 = nn.Conv1d(base_filters * 2, base_filters * 4, kernel_size=15, padding=7)
        
        # Ambisonics output layers
        self.out_convs = nn.ModuleList([
            nn.Conv1d(base_filters * 4, 1, kernel_size=1)  # For each Ambisonics channel
            for _ in range(self.n_channels)
        ])
        
        # Activation
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        # x: (batch, input_channels, time)
        x = self.relu(self.conv1(x))
        x = self.relu(self.conv2(x))
        x = self.relu(self.conv3(x))
        
        # Generate each Ambisonics channel
        ambisonics_channels = []
        for i in range(self.n_channels):
            channel_out = self.out_convs[i](x)
            ambisonics_channels.append(channel_out)
        
        # Concatenate channels: (batch, n_channels, time)
        ambisonics = torch.cat(ambisonics_channels, dim=1)
        return ambisonics

# Early reflection generator using image source model (enhanced with neural network)
class EarlyReflectionGenerator:
    def __init__(self, 
                 sample_rate: int = 48000,
                 room_size: Tuple[float, float, float] = (5.0, 4.0, 3.0),  # L, W, H
                 wall_absorption: float = 0.1):
        self.sample_rate = sample_rate
        self.room_size = room_size
        self.wall_absorption = wall_absorption
        self.speed_of_sound = 343.0  # m/s
    
    def generate_early_reflections(self, 
                                  source_pos: Tuple[float, float, float],
                                  listener_pos: Tuple[float, float, float],
                                  max_order: int = 2,
                                  duration: float = 0.1) -> np.ndarray:
        """Generate early reflections using image source model"""
        # This is a simplified implementation
        # In practice, use efficient image source model or ray tracing
        # For demonstration, we'll generate a few reflections
        
        # Calculate direct sound
        direct_path = np.linalg.norm(np.array(source_pos) - np.array(listener_pos))
        direct_delay = direct_path / self.speed_of_sound
        
        # Generate image sources for first and second order reflections
        reflections = []
        
        # First order reflections (6 walls for rectangular room)
        walls = [
            (['x'], [-self.room_size[0]/2, self.room_size[0]/2]),  # Left and right walls
            (['y'], [-self.room_size[1]/2, self.room_size[1]/2]),  # Front and back walls
            (['z'], [-self.room_size[2]/2, self.room_size[2]/2])   # Floor and ceiling
        ]
        
        for wall_axis, wall_positions in walls:
            for wall_pos in wall_positions:
                # Create image source
                image_source = list(source_pos)
                axis_idx = {'x':0, 'y':1, 'z':2}[wall_axis[0]]
                image_source[axis_idx] = 2 * wall_pos - source_pos[axis_idx]
                
                # Calculate path length
                path_len = np.linalg.norm(np.array(image_source) - np.array(listener_pos))
                # Add path from source to wall and wall to listener? 
                # Actually, image source method: path length = distance from image source to listener
                delay = path_len / self.speed_of_sound
                
                # Attenuation: wall absorption and distance
                attenuation = (1.0 - self.wall_absorption) / (path_len ** 2)  # Simplified
                
                reflections.append((delay, attenuation))
        
        # Second order reflections (more complex, simplified here)
        # In practice, you would iterate over combinations of walls
        
        # Generate impulse response
        ir_length = int(duration * self.sample_rate)
        ir = np.zeros(ir_length)
        
        # Add direct sound
        direct_sample = int(direct_delay * self.sample_rate)
        if direct_sample < ir_length:
            ir[direct_sample] += 1.0  # Direct sound
        
        # Add reflections
        for delay, attenuation in reflections:
            sample = int(delay * self.sample_rate)
            if sample < ir_length:
                ir[sample] += attenuation
        
        # Apply exponential decay to tail (optional)
        # ir *= np.exp(-np.arange(ir_length) / (self.sample_rate * 0.5))  # 0.5s reverb time
        
        return ir

# Neural network for late reverb synthesis
class LateReverbSynthesizer(nn.Module):
    def __init__(self, 
                 input_dim: int = 128,  # Feature dimension from room characteristics
                 hidden_dim: int = 256,
                 output_length: int = 48000):  # 1 second at 48kHz
        super().__init__()
        
        self.output_length = output_length
        
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.fc3 = nn.Linear(hidden_dim, output_length)
        
        self.relu = nn.ReLU(inplace=True)
    
    def forward(self, x):
        # x: (batch, input_dim)
        x = self.relu(self.fc1(x))
        x = self.relu(self.fc2(x))
        x = self.fc3(x)  # (batch, output_length)
        return x

# Binaural renderer using HRTF interpolation
class BinauralRenderer:
    def __init__(self, 
                 hrtf_dataset: Optional[np.ndarray] = None,
                 sample_rate: int = 48000):
        self.sample_rate = sample_rate
        self.hrtf_dataset = hrtf_dataset  # Shape: (num_positions, 2, ir_length)
        self.positions = None  # Azimuth, elevation for each HRTF
        
        if hrtf_dataset is not None:
            # In practice, load HRTF dataset and extract positions
            # For demonstration, we'll assume it's provided
            pass
    
    def render_binaural(self, 
                       ambisonics: np.ndarray,
                       order: int = 1) -> np.ndarray:
        """Convert Ambisonics to binaural using HRTF interpolation"""
        # This is a simplified implementation
        # In practice, use SH (spherical harmonic) domain decoding and HRTF interpolation
        
        # For first order Ambisonics (W, X, Y, Z), we can decode to binaural
        # using a head-related transfer function (HRTF) matrix
        
        # We'll implement a very basic decoder for demonstration
        if order == 1 and ambisonics.shape[0] >= 4:
            W, X, Y, Z = ambisonics[0], ambisonics[1], ambisonics[2], ambisonics[3]
            
            # Simple binaural rendering (not accurate, just for structure)
            # Left = W + X*cos(azi) + Y*sin(azi)*cos(ele) + Z*sin(ele)
            # Right = W - X*cos(azi) - Y*sin(azi)*cos(ele) + Z*sin(ele)
            # But we need to do this for each frequency band or use time-domain convolution
            
            # Instead, we'll use a placeholder: apply a simple HRTF-like filter
            # In practice, use convolution with HRTF filters for left and right
            
            # For now, return a dummy binaural signal
            left = np.zeros_like(W)
            right = np.zeros_like(W)
            return np.array([left, right])
        else:
            # For higher orders or other cases, use more advanced decoding
            # Placeholder: return stereo copy of first two channels
            if ambisonics.shape[0] >= 2:
                return ambisonics[:2]
            else:
                # Mono to binaural
                mono = ambisonics[0] if ambisonics.shape[0] > 0 else np.zeros_like(ambisonics[0])
                return np.array([mono, mono])

# Full spatial audio synthesis system
class SpatialAudioSynthesizer:
    def __init__(self, 
                 ambisonics_model_path: str,
                 reverb_model_path: str,
                 hrtf_dataset_path: Optional[str] = None,
                 sample_rate: int = 48000):
        self.sample_rate = sample_rate
        
        # Initialize Ambisonics synthesizer
        self.ambisonics_net = AmbisonicsSynthesizer(input_channels=2, order=1)
        self.ambisonics_net.load_state_dict(torch.load(ambisonics_model_path, map_location='cpu'))
        self.ambisonics_net.eval()
        
        # Initialize late reverb synthesizer
        self.reverb_net = LateReverbSynthesizer()
        self.reverb_net.load_state_dict(torch.load(reverb_model_path, map_location='cpu'))
        self.reverb_net.eval()
        
        # Initialize binaural renderer
        if hrtf_dataset_path:
            # Load HRTF dataset
            self.binaural_renderer = BinauralRenderer(
                hrtf_dataset=np.load(hrtf_dataset_path),
                sample_rate=sample_rate
            )
        else:
            self.binaural_renderer = BinauralRenderer(sample_rate=sample_rate)
    
    def process_audio(self, 
                     audio: np.ndarray,
                     source_pos: Tuple[float, float, float] = (0, 0, 1),  # Front, 1m away
                     listener_pos: Tuple[float, float, float] = (0, 0, 0),  # Origin
                     room_size: Tuple[float, float, float] = (5.0, 4.0, 3.0)) -> np.ndarray:
        """Process audio to create spatial audio scene"""
        # Step 1: Generate early reflections
        early_reflections = EarlyReflectionGenerator(
            sample_rate=self.sample_rate,
            room_size=room_size
        ).generate_early_reflections(source_pos, listener_pos, max_order=1, duration=0.05)
        
        # Step 2: Convolve audio with early reflections
        if len(early_reflections) > 0:
            audio_with_early = np.convolve(audio, early_reflections, mode='same')
        else:
            audio_with_early = audio.copy()
        
        # Step 3: Convert to Ambisonics (neural network)
        # Prepare input: stereo audio (we'll duplicate mono to stereo if needed)
        if audio_with_early.ndim == 1:
            stereo_audio = np.array([audio_with_early, audio_with_early])
        else:
            stereo_audio = audio_with_early[:2]  # Take first two channels
        
        audio_tensor = torch.from_numpy(stereo_audio).float().unsqueeze(0)
        with torch.no_grad():
            ambisonics = self.ambisonics_net(audio_tensor).squeeze(0).numpy()  # (n_channels, time)
        
        # Step 4: Generate late reverb (neural network)
        # Extract room characteristics (simplified: use room size and absorption)
        room_features = np.array([
            room_size[0], room_size[1], room_size[2],  # L, W, H
            0.1  # Wall absorption (placeholder)
        ])
        room_features_tensor = torch.from_numpy(room_features).float().unsqueeze(0)
        with torch.no_grad():
            reverb_tail = self.reverb_net(room_features_tensor).squeeze(0).numpy()
        
        # Step 5: Combine early reflections, direct sound, and late reverb
        # We already have audio_with_early (which includes early reflections and direct sound)
        # Add late reverb tail
        # Ensure same length
        min_len = min(len(audio_with_early), len(reverb_tail))
        audio_with_reverb = audio_with_early[:min_len] + reverb_tail[:min_len]
        
        # Step 6: Convert to binaural for headphone playback
        binaural = self.binaural_renderer.render_binaural(audio_with_reverb, order=1)
        
        return binaural
```

## EDGE CASES & FALLBACKS
- **Ambisonics Order Mismatch**: Downmix or upsample Ambisonics channels using appropriate transformations
- **HRTF Individual Variation**: Use individualized HRTFs or apply PCA-based adaptation
- **Latency Issues**: Use smaller neural network models, reduce Ambisonics order, or implement predictive processing
- **Spectral Coloration**: Equalize the spatialization process to compensate for frequency response
- **Externalization Issues**: Apply externalization filters or use individualized HRTFs
- **Front-Back Confusion**: Use dynamic cues or head tracking (if available)
- **Low-Frequency Ambisonics**: Use specialized low-frequency treatment (e.g., bass management)
- **Numerical Instability**: Normalize Ambisonics components, use higher precision processing
- **CPU Usage**: Optimize neural networks, use model pruning or quantization

## INTEGRATION POINTS
- Audio Processing: Librosa, Torchaudio, SciPy, SoundFile
- Ambisonics Libraries: ambisonic, PyAmbisonics, SPARTA
- HRTF Databases: CIPIC, LISTEN, SADIE II, IISLA
- Spatial Audio Formats: Dolby Atmos, DTS:X, Auro-3D, MPEG-H 3DA, Sony 360 Reality Audio
- Real-Time Frameworks: JACK, ASIO, CoreAudio, WebAudio API
- Game Engines: Unity (Resonance Audio), Unreal Engine (Oculus Audio, Steam Audio)
- VR/AR Platforms: Oculus SDK, OpenXR, WebXR
- Measurement Tools: Head and torso simulators (HATS), loudness meters
- Deployment: ONNX, TorchScript, TensorRT for neural network components
- Room Acoustics: Image source model, ray tracing, bidirectional path tracing
- Binaural Rendering: VBAP, VBAP with elevation, Max rE, AllrAD

## EXECUTION EXAMPLES

**Input:** "Create a spatial audio effect that places a sound source 30 degrees to the left and elevates it 15 degrees"
**Output:**
```python
# Initialize spatial audio synthesizer
spatial_synth = SpatialAudioSynthesizer(
    ambisonics_model_path="ambisonics_net.pt",
    reverb_model_path="reverb_net.pt",
    hrtf_dataset_path="hrtf_dataset.npz",
    sample_rate=48000
)

# Process a mono audio signal (e.g., a voice recording)
voice, sr = librosa.load("voice_recording.wav", sr=None)
spatial_audio = spatial_synth.process_audio(
    voice,
    source_pos=(np.cos(np.radians(30+90)), np.sin(np.radians(30+90)), np.sin(np.radians(15))),  # Convert to Cartesian
    listener_pos=(0, 0, 0),
    room_size=(4.0, 3.0, 2.5)
)

# Save as binaural for headphone listening
sf.write("spatial_voice.wav", spatial_audio.T, sr)  # Transpose to (time, channels)
```

**Input:** "Generate a Dolby Atmos-compatible bed from a stereo music mix"
**Output:**
```python
# For Dolby Atmos, we would typically generate Ambisonics or object-based audio
# This example creates a first-order Ambisonics bed from stereo

# Load stereo music mix
mix, sr = librosa.load("stereo_mix.wav", sr=None)

# Initialize Ambisonics synthesizer (for bed generation)
ambisonics_net = AmbisonicsSynthesizer(input_channels=2, order=1)
ambisonics_net.load_state_dict(torch.load("ambisonics_bed_net.pt", map_location='cpu'))
ambisonics_net.eval()

# Prepare input
if mix.ndim == 1:
    stereo_mix = np.array([mix, mix])
else:
    stereo_mix = mix[:2]  # Ensure stereo

mix_tensor = torch.from_numpy(stereo_mix).float().unsqueeze(0)
with torch.no_grad():
    ambisonics_bed = ambisonics_net(mix_tensor).squeeze(0).numpy()  # (4, time) for order=1

# Save Ambisonics B-format (W, X, Y, Z)
# In practice, use Ambisonics library to write proper format
# For demonstration, save as multi-channel WAV
sf.write("atmos_bed.wav", ambisonics_bed.T, sr)

# This Ambisonics bed can then be used as input to a Dolby Atmos encoder
# or converted to object-based audio using appropriate tools
```