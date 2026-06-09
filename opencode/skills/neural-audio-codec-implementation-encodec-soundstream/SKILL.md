---
name: neural-audio-codec-implementation-encodec-soundstream
description: >-
  Use this skill when the user is working on or asking about EnCodec, SoundStream, neural audio codecs, audio compression with neural networks, or implementing audio codecs with deep learning.
version: 1.0.0
---

# SKILL: Neural Audio Codec Implementation (EnCodec/SoundStream)

## CAPABILITIES
- Implement neural audio codecs like EnCodec or SoundStream for high-compression audio
- Achieve low-bitrate audio transmission (3-64 kbps) with high perceptual quality
- Handle variable bitrate and constant bitrate modes
- Support streaming and offline encoding/decoding
- Integrate with existing audio pipelines and DAWs

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Audio waveforms (PCM, float) | Compressed bitstream |
| Bitstream | Reconstructed audio waveforms |
| Target bitrate and quality settings | Encoded audio packets |
| Latency requirements | Optimized encoding/decoding pipeline |
| Audio sample rate and bit depth | Compressed representation specifications |

## IMPLEMENTATION PATTERN

```python
# Neural Audio Codec Implementation (EnCodec-style)
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional

# Simplified EnCodec-style encoder
class Encoder(nn.Module):
    def __init__(self, 
                 channels: int = 1,
                 dimension: int = 128,
                 n_filters: int = 32,
                 n_residual_layers: int = 1,
                 ratios: Tuple[int, ...] = (8, 5, 4, 2)):  # For 24kHz -> 6kbps
        super().__init__()
        
        # Initial convolution
        self.conv_block = nn.Sequential(
            nn.Conv1d(channels, n_filters, kernel_size=7, padding=3),
            nn.ELU()
        )
        
        # Downsampling layers
        self.downsample_layers = nn.ModuleList()
        for i, ratio in enumerate(ratios):
            layer = nn.Sequential(
                nn.Conv1d(n_filters * (2 ** i), 
                         n_filters * (2 ** (i + 1)),
                         kernel_size=ratio * 2,
                         stride=ratio,
                         padding=ratio // 2),
                nn.ELU()
            )
            self.downsample_layers.append(layer)
        
        # Residual layers
        self.residual_layers = nn.ModuleList()
        for _ in range(n_residual_layers):
            self.residual_layers.append(
                nn.Sequential(
                    nn.Conv1d(n_filters * (2 ** len(ratios)), 
                             n_filters * (2 ** len(ratios)),
                             kernel_size=3, padding=1),
                    nn.ELU(),
                    nn.Conv1d(n_filters * (2 ** len(ratios)), 
                             n_filters * (2 ** len(ratios)),
                             kernel_size=3, padding=1),
                    nn.ELU()
                )
            )
        
        # Final projection
        self.final_conv = nn.Conv1d(n_filters * (2 ** len(ratios)), 
                                   dimension, 
                                   kernel_size=3, padding=1)
    
    def forward(self, x):
        # x: (B, C, T)
        x = self.conv_block(x)
        
        for layer in self.downsample_layers:
            x = layer(x)
        
        for layer in self.residual_layers:
            residual = x
            x = layer(x)
            x = x + residual  # Residual connection
        
        x = self.final_conv(x)
        return x  # (B, dimension, T')

# Simplified EnCodec-style decoder
class Decoder(nn.Module):
    def __init__(self, 
                 channels: int = 1,
                 dimension: int = 128,
                 n_filters: int = 32,
                 n_residual_layers: int = 1,
                 ratios: Tuple[int, ...] = (8, 5, 4, 2)):  # Must match encoder
        super().__init__()
        
        # Initial projection
        self.initial_conv = nn.Conv1d(dimension, 
                                     n_filters * (2 ** len(ratios)),
                                     kernel_size=3, padding=1)
        
        # Residual layers
        self.residual_layers = nn.ModuleList()
        for _ in range(n_residual_layers):
            self.residual_layers.append(
                nn.Sequential(
                    nn.Conv1d(n_filters * (2 ** len(ratios)), 
                             n_filters * (2 ** len(ratios)),
                             kernel_size=3, padding=1),
                    nn.ELU(),
                    nn.Conv1d(n_filters * (2 ** len(ratios)), 
                             n_filters * (2 ** len(ratios)),
                             kernel_size=3, padding=1),
                    nn.ELU()
                )
            )
        
        # Upsampling layers (reverse of encoder ratios)
        self.upsample_layers = nn.ModuleList()
        for i, ratio in enumerate(reversed(ratios)):
            layer = nn.Sequential(
                nn.ConvTranspose1d(n_filters * (2 ** (len(ratios) - i - 1)),
                                  n_filters * (2 ** (len(ratios) - i - 2)),
                                  kernel_size=ratio * 2,
                                  stride=ratio,
                                  padding=ratio // 2),
                nn.ELU()
            )
            self.upsample_layers.append(layer)
        
        # Final convolution
        self.final_conv = nn.Conv1d(n_filters, channels, kernel_size=7, padding=3)
    
    def forward(self, x):
        # x: (B, dimension, T')
        x = self.initial_conv(x)
        
        for layer in self.residual_layers:
            residual = x
            x = layer(x)
            x = x + residual  # Residual connection
        
        for layer in self.upsample_layers:
            x = layer(x)
        
        x = self.final_conv(x)
        return x  # (B, C, T)

# Quantizer (Simplified RVQ - Residual Vector Quantization)
class ResidualVectorQuantizer(nn.Module):
    def __init__(self, 
                 dimension: int = 128,
                 n_codebooks: int = 4,
                 codebook_size: int = 1024,
                 commitment_cost: float = 0.25):
        super().__init__()
        
        self.n_codebooks = n_codebooks
        self.codebook_size = codebook_size
        self.commitment_cost = commitment_cost
        
        # Codebooks
        self.codebooks = nn.ModuleList([
            nn.Embedding(codebook_size, dimension) 
            for _ in range(n_codebooks)
        ])
    
    def forward(self, z):
        # z: (B, dimension, T)
        # Transpose for easier handling: (B, T, dimension)
        z = z.permute(0, 2, 1)
        B, T, D = z.shape
        
        # Initialize
        quantized = torch.zeros_like(z)
        residual = z
        all_losses = []
        all_indices = []
        
        # Process each codebook
        for i in range(self.n_codebooks):
            # Flatten for quantization
            flat_residual = residual.reshape(-1, D)  # (B*T, D)
            
            # Find nearest neighbors
            distances = torch.cdist(flat_residual, self.codebooks[i].weight)  # (B*T, codebook_size)
            encoding_indices = torch.argmin(distances, dim=-1)  # (B*T)
            
            # Quantize
            quantized_residual = self.codebooks[i](encoding_indices)  # (B*T, D)
            quantized_residual = quantized_residual.view(B, T, D)
            
            # Update residual
            residual = residual - quantized_residual.detach()
            quantized = quantized + quantized_residual
            
            # Calculate commitment loss
            e_latent_loss = F.mse_loss(quantized_residual.detach(), residual)
            q_latent_loss = F.mse_loss(quantized_residual, residual.detach())
            loss = q_latent_loss + self.commitment_cost * e_latent_loss
            all_losses.append(loss)
            
            # Store indices
            all_indices.append(encoding_indices.view(B, T))
        
        # Calculate total loss
        loss = torch.stack(all_losses).sum()
        
        # Straight-through estimator
        quantized = z + (quantized - z).detach()
        
        # Transpose back: (B, dimension, T)
        quantized = quantized.permute(0, 2, 1)
        
        # Convert indices to bytes for storage/transmission
        indices = torch.stack(all_indices, dim=-1)  # (B, T, n_codebooks)
        
        return quantized, loss, indices

# Full EnCodec-style model
class NeuralAudioCodec(nn.Module):
    def __init__(self, 
                 sample_rate: int = 24000,
                 target_bandwidth: float = 6.0,  # kbps
                 channels: int = 1):
        super().__init__()
        
        self.sample_rate = sample_rate
        self.target_bandwidth = target_bandwidth
        self.channels = channels
        
        # Calculate frames per second and bits per frame
        # For 24kHz audio with 2.5ms frame size (60 samples)
        self.frame_length = int(sample_rate * 0.0025)  # 60 samples
        self.frames_per_second = sample_rate // self.frame_length  # 400 fps
        
        # Target bits per frame
        self.target_bits_per_frame = int((target_bandwidth * 1000) // self.frames_per_second)
        
        # Build encoder, decoder, quantizer
        self.encoder = Encoder(channels=channels)
        self.decoder = Decoder(channels=channels)
        
        # Calculate quantization parameters based on target bitrate
        # Simplified: assume we want to use all bits for quantization
        self.quantizer = ResidualVectorQuantizer(
            dimension=128,
            n_codebooks=min(8, max(2, self.target_bits_per_frame // 8)),  # Rough estimate
            codebook_size=256  # 8 bits per codebook entry
        )
    
    def compress(self, audio: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Compress audio to bitstream
        Args:
            audio: (B, C, T) tensor in [-1, 1] range
        Returns:
            codes: (B, n_codebooks, T') quantized indices
            commitment_loss: scalar loss
            scale: scaling factor used
        """
        # Encode
        z = self.encoder(audio)  # (B, dimension, T')
        
        # Quantize
        quantized, commitment_loss, codes = self.quantizer(z)
        
        return codes, commitment_loss, z  # Return z for potential use in decoder
    
    def decompress(self, codes: torch.Tensor, 
                  encoder_output: Optional[torch.Tensor] = None) -> torch.Tensor:
        """
        Decompress codes to audio
        Args:
            codes: (B, n_codebooks, T') quantized indices
            encoder_output: Optional encoder output for consistency loss
        Returns:
            audio: (B, C, T) reconstructed audio
        """
        # If we have encoder output, use it for quantization (training)
        # Otherwise, we need to re-quantize the codes (inference)
        if encoder_output is not None:
            # Training mode: use encoder output to get quantized representation
            quantized, _, _ = self.quantizer(encoder_output)
        else:
            # Inference mode: reconstruct from codes
            # This is simplified - actual implementation would use the codebooks
            # to look up vectors based on codes
            B, n_codebooks, T_prime = codes.shape
            dimension = 128  # Should match encoder dimension
            
            # Initialize quantized tensor
            quantized = torch.zeros((B, dimension, T_prime), device=codes.device)
            
            # For each codebook, look up vectors and accumulate
            for i in range(n_codebooks):
                codebook_vectors = self.quantizer.codebooks[i].weight  # (codebook_size, dimension)
                # Gather vectors based on codes
                selected_vectors = F.embedding(codes[:, :, i], codebook_vectors)  # (B, T', dimension)
                quantized = quantized + selected_vectors
        
        # Decode
        audio = self.decoder(quantized)
        return audio
    
    def forward(self, audio: torch.Tensor):
        """Forward pass for training"""
        codes, commitment_loss, encoder_output = self.compress(audio)
        reconstructed = self.decompress(codes, encoder_output)
        reconstruction_loss = F.l1_loss(audio, reconstructed)
        total_loss = reconstruction_loss + commitment_loss
        return reconstructed, total_loss

# Usage example
def encode_decode_audio(audio waveform, target_bandwidth=6.0):
    """Encode and decode audio using neural codec"""
    # Initialize codec
    codec = NeuralAudioCodec(sample_rate=24000, target_bandwidth=target_bandwidth)
    
    # Prepare audio tensor (normalize to [-1, 1])
    audio_tensor = torch.from_numpy(audio waveform).float().unsqueeze(0).unsqueeze(0)  # (1, 1, T)
    audio_tensor = audio_tensor / 32768.0  # Assuming 16-bit input
    
    # Compress
    codes, commitment_loss, _ = codec.compress(audio_tensor)
    
    # Decompress
    reconstructed_tensor = codec.decompress(codes)
    
    # Convert back to numpy
    reconstructed = reconstructed_tensor.squeeze().numpy() * 32768.0
    reconstructed = reconstructed.astype(audio waveform.dtype)
    
    return reconstructed
```

## EDGE CASES & FALLBACKS
- **Bitrate Mismatch**: Dynamically adjust quantization precision or frame size
- **Error Propagation**: Use error concealment techniques (packet loss hiding)
- **Latency Issues**: Reduce look-ahead in encoder or use causal convolutions
- **Quality Degradation**: Implement perceptual loss functions or adversarial training
- **Memory Constraints**: Use model pruning, quantization, or knowledge distillation
- **Clip Artifacts**: Add soft clipping or use tanh activation in final layer
- **Silence Handling**: Implement voice activity detection (VAD) for efficient encoding
- **Sample Rate Conversion**: Resample audio to match codec's expected rate
- **Channel Mismatch**: Convert between mono/stereo as needed or use multi-channel codec

## INTEGRATION POINTS
- Audio Frameworks: PyTorch Audio, TensorFlow Audio, JUCE, VST SDK
- Communication Protocols: WebRTC, Opus, UDP/RTP, QUIC
- Storage Formats: OGG, MP4, custom binary formats
- Streaming Services: IceCast, SHOUTcast, RTMP
- Hardware Acceleration: GPU (CUDA), DSPs, NPUs
- DAW Integration: VST3, AU, AAX, CLAP plugins as codec bridges
- Containerization: Docker, Kubernetes for scalable deployment
- Monitoring: Prometheus, Grafana for bitrate and quality metrics
- Testing: PESQ, STOI, MOSNet, AWS Polly benchmark suites

## EXECUTION EXAMPLES

**Input:** "Encode audio at 8 kbps for real-time transmission over Bluetooth"
**Output:**
```python
# Initialize codec for Bluetooth transmission
codec = NeuralAudioCodec(
    sample_rate=16000,  # Bluetooth-friendly sample rate
    target_bandwidth=8.0,  # 8 kbps
    channels=1  # Mono for Bluetooth headset
)

# Process audio in real-time chunks
def process_audio_chunk(audio_chunk):
    # audio_chunk: numpy array of int16 samples
    audio_tensor = torch.from_numpy(audio_chunk).float().unsqueeze(0).unsqueeze(0) / 32768.0
    
    # Encode
    codes, _, _ = codec.compress(audio_tensor)
    
    # Transmit codes (would be packetized for actual transmission)
    transmit_data(codes.numpy().tobytes())
    
    # For playback on receiving end:
    # received_bytes = receive_data()
    # received_codes = torch.from_numpy(np.frombuffer(received_bytes, dtype=np.int64))
    # received_codes = received_codes.view(1, -1, codec.encoder.frame_length // 160)  # Adjust dimensions
    # decoded_audio = codec.decompress(received_codes)
    # return (decoded_audio.squeeze().numpy() * 32768).astype(np.int16)
```

**Input:** "Implement a neural audio codec for music at 32 kbps stereo"
**Output:**
```python
# High-quality music codec
music_codec = NeuralAudioCodec(
    sample_rate=44100,  # CD quality
    target_bandwidth=32.0,  # 32 kbps stereo
    channels=2  # Stereo
)

# For music, we might want to adjust the architecture:
# - Larger latent dimension for better quality
# - More codebooks or larger codebooks
# - Possibly use hierarchical quantization
# - Add perceptual loss components during training
```