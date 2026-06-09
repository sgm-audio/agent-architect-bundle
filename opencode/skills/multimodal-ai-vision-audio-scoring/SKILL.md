---
name: multimodal-ai-vision-audio-scoring
description: >-
  Use this skill when the user is working on or asking about multimodal AI, vision-audio models, automatic video scoring, AI-generated music for video, or aligning audio with visual content.
version: 1.0.0
---

# SKILL: Multimodal AI (Vision-Audio Scoring)

## CAPABILITIES
- Analyze video frames to generate matching musical scores and sound effects
- Synchronize audio generation to on-screen action and emotion
- Implement vision-language models (CLIP, ViT) for video understanding
- Generate adaptive music that responds to visual content in real-time
- Create sound effects that match visual events and physics

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Video frames or video clips | Generated music or sound effects |
| Visual features (objects, actions, emotions) | Audio parameters (melody, rhythm, instrumentation) |
| Temporal synchronization requirements | Time-stamped audio events |
| Emotional or narrative cues | Music that matches mood and pacing |
| Real-time constraints (<100ms latency) | Low-latency audio generation pipeline |

## IMPLEMENTATION PATTERN

```python
# Multimodal Vision-Audio Scoring System
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import cv2
from transformers import CLIPProcessor, CLIPModel
from typing import Tuple, List, Optional, Dict
import librosa

# Video feature extractor using CLIP
class VideoFeatureExtractor:
    def __init__(self, model_name: str = "openai/clip-vit-base-patch32"):
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name)
        self.model.eval()
        
        # Define text prompts for video understanding
        self.action_prompts = [
            "a person walking", "a person running", "a person jumping",
            "a car driving", "an explosion", "a door closing",
            "glass breaking", "water splashing", "fire burning"
        ]
        
        self.mood_prompts = [
            "happy and upbeat", "sad and melancholic", "tense and suspenseful",
            "calm and peaceful", "energetic and exciting", "dark and mysterious"
        ]
        
        self.genre_prompts = [
            "orchestral music", "electronic music", "jazz music",
            "rock music", "classical music", "ambient music"
        ]
    
    def extract_features(self, frames: List[np.ndarray]) -> Dict[str, np.ndarray]:
        """Extract features from video frames"""
        # Convert frames to PIL images for CLIP
        # In practice, you'd do this more efficiently
        pil_frames = [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) for frame in frames]
        
        # Process with CLIP
        inputs = self.processor(
            text=self.action_prompts + self.mood_prompts + self.genre_prompts,
            images=pil_frames,
            return_tensors="pt",
            padding=True
        )
        
        # Get image and text features
        with torch.no_grad():
            outputs = self.model(**inputs)
            image_embeds = outputs.image_embeds  # (batch, embed_dim)
            text_embeds = outputs.text_embeds    # (num_texts, embed_dim)
            
            # Calculate similarities
            action_similarities = (image_embeds @ text_embeds[:len(self.action_prompts)].T).softmax(dim=-1)
            mood_similarities = (image_embeds @ text_embeds[len(self.action_prompts):len(self.action_prompts)+len(self.mood_prompts)].T).softmax(dim=-1)
            genre_similarities = (image_embeds @ text_embeds[len(self.action_prompts)+len(self.mood_prompts):].T).softmax(dim=-1)
        
        return {
            "action": action_similarities.numpy(),
            "mood": mood_similarities.numpy(),
            "genre": genre_similarities.numpy(),
            "image_embeddings": image_embeds.numpy()
        }

# Audio generation network conditioned on video features
class VideoConditionedAudioNet(nn.Module):
    def __init__(self, 
                 video_embed_dim: int = 512,
                 audio_embed_dim: int = 256,
                 output_dim: int = 128):
        super().__init__()
        
        # Video feature processing
        self.video_proj = nn.Linear(video_embed_dim, audio_embed_dim)
        
        # Temporal convolution for audio generation
        self.audio_net = nn.Sequential(
            nn.Conv1d(audio_embed_dim, audio_embed_dim, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(audio_embed_dim, audio_embed_dim, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv1d(audio_embed_dim, output_dim, kernel_size=1)
        )
    
    def forward(self, video_features: torch.Tensor) -> torch.Tensor:
        """
        Args:
            video_features: (batch, seq_len, video_embed_dim) - video features over time
        Returns:
            audio_features: (batch, seq_len, output_dim) - audio features to decode
        """
        # Project video features to audio embedding space
        projected = self.video_proj(video_features)  # (batch, seq_len, audio_embed_dim)
        
        # Transpose for Conv1d: (batch, audio_embed_dim, seq_len)
        projected = projected.transpose(1, 2)
        
        # Process through audio network
        audio_features = self.audio_net(projected)  # (batch, output_dim, seq_len)
        
        # Transpose back: (batch, seq_len, output_dim)
        audio_features = audio_features.transpose(1, 2)
        return audio_features

# Real-time vision-audio scoring system
class VisionAudioScorer:
    def __init__(self, 
                 video_model_path: str,
                 audio_model_path: str,
                 sample_rate: int = 48000,
                 fps: int = 30):
        self.sample_rate = sample_rate
        self.fps = fps
        self.frame_duration = 1.0 / fps
        
        # Initialize feature extractor
        self.feature_extractor = VideoFeatureExtractor()
        
        # Initialize audio generation model
        self.audio_model = VideoConditionedAudioNet()
        self.audio_model.load_state_dict(torch.load(audio_model_path, map_location='cpu'))
        self.audio_model.eval()
        
        # Audio decoder (simplified - in practice use a vocoder or synthesizer)
        self.audio_decoder = nn.Linear(128, 256)  # Placeholder
        
        # Buffer for accumulating video frames
        self.frame_buffer = []
        self.audio_buffer = np.array([])
        
    def process_video_frame(self, frame: np.ndarray) -> np.ndarray:
        """Process a single video frame and return audio chunk"""
        # Add frame to buffer
        self.frame_buffer.append(frame)
        
        # Process when we have enough frames (e.g., 1 second of video)
        if len(self.frame_buffer) >= self.fps:
            # Extract features from buffered frames
            features = self.feature_extractor.extract_features(self.frame_buffer)
            
            # Convert to tensor
            video_features = torch.from_numpy(features["image_embeddings"]).float().unsqueeze(0)
            
            # Generate audio features
            with torch.no_grad():
                audio_features = self.audio_model(video_features)
                audio_features = self.audio_decoder(audio_features)
            
            # Convert audio features to waveform (simplified)
            # In practice, use a vocoder or synthesizer
            audio_chunk = self.features_to_audio(audio_features.squeeze(0).numpy())
            
            # Clear frame buffer (sliding window approach)
            # Keep last few frames for continuity
            keep_frames = int(self.fps * 0.5)  # Keep half second
            self.frame_buffer = self.frame_buffer[-keep_frames:]
            
            return audio_chunk
        
        # Return silence if not enough frames yet
        return np.zeros(int(self.sample_rate * self.frame_duration))
    
    def features_to_audio(self, features: np.ndarray) -> np.ndarray:
        """Convert audio features to waveform (placeholder)"""
        # This is a simplified implementation
        # In practice, you would use:
        # 1. A vocoder (like WaveNet, HiFi-GAN) to convert features to audio
        # 2. A synthesizer that maps features to oscillators, filters, etc.
        # 3. A retrieval-based system that selects from a library of audio clips
        
        # For demonstration, we'll generate a simple tone based on features
        # Features[0] could control frequency, features[1] amplitude, etc.
        duration = len(features) * (1.0 / self.fps)  # Duration in seconds
        t = np.linspace(0, duration, int(self.duration * self.sample_rate), False)
        
        # Simple mapping: first feature -> frequency, second -> amplitude
        freq = 200 + features[:, 0] * 800  # 200-1000 Hz range
        amp = np.clip(features[:, 1], 0, 1)  # 0-1 range
        
        # Generate audio (simplified - real implementation would be more sophisticated)
        audio = np.zeros(int(duration * self.sample_rate))
        for i in range(len(t)):
            # This is inefficient but illustrates the concept
            if i < len(freq):
                audio[i] = amp[i] * np.sin(2 * np.pi * freq[i] * t[i])
        
        return audio

# Alternative: Retrieval-based vision-audio scoring
class RetrievalBasedScorer:
    def __init__(self, 
                 video_audio_pairs: List[Tuple[np.ndarray, np.ndarray]],
                 sample_rate: int = 48000):
        self.sample_rate = sample_rate
        self.pairs = video_audio_pairs
        self.feature_extractor = VideoFeatureExtractor()
        
        # Pre-compute video features for all pairs
        self.video_features = []
        self.audio_clips = []
        
        for video_frames, audio_clip in pairs:
            features = self.feature_extractor.extract_features(video_frames)
            # Use average features for the clip
            avg_features = np.mean(features["image_embeddings"], axis=0)
            self.video_features.append(avg_features)
            self.audio_clips.append(audio_clip)
        
        self.video_features = np.array(self.video_features)  # (num_pairs, embed_dim)
    
    def score_video_frame(self, frame: np.ndarray) -> np.ndarray:
        """Find matching audio clip for video frame"""
        # Extract features from current frame
        features = self.feature_extractor.extract_features([frame])
        frame_features = np.mean(features["image_embeddings"], axis=0)  # (embed_dim,)
        
        # Find closest match in database
        similarities = np.dot(self.video_features, frame_features)  # (num_pairs,)
        best_match_idx = np.argmax(similarities)
        
        # Return corresponding audio clip
        return self.audio_clips[best_match_idx]
    
    def process_video_stream(self, video_frames: List[np.ndarray], 
                           hop_size: int = 1) -> List[np.ndarray]:
        """Process video stream with hop size"""
        audio_stream = []
        
        for i in range(0, len(video_frames), hop_size):
            frame = video_frames[i]
            audio_clip = self.score_video_frame(frame)
            audio_stream.append(audio_clip)
        
        return audio_stream
```

## EDGE CASES & FALLBACKS
- **Latency Issues**: Use smaller video buffers, reduce model complexity, or implement predictive caching
- **Misalignment Between Vision and Audio**: Use temporal alignment techniques or attention mechanisms
- **Insufficient Video Context**: Use longer context windows or recurrent networks for temporal modeling
- **Ambiguous Visual Content**: Implement uncertainty-aware generation or multimodal fusion
- **Audio Quality Degradation**: Use high-quality vocoders or post-processing enhancements
- **Domain Mismatch**: Fine-tune vision models on domain-specific video data
- **Real-Time Constraints**: Implement model distillation or quantization for faster inference
- **Memory Limitations**: Use feature caching or process video in chunks
- **Synchronization Errors**: Implement audio-visual alignment algorithms (like dynamic time warping)

## INTEGRATION POINTS
- Video Processing: OpenCV, FFmpeg, GStreamer, PyTorch Video
- Vision Models: CLIP, ALIGN, Florence, BLIP, ViT
- Audio Generation: Vocoders (WaveNet, HiFi-GAN), synthesizers, audio synthesis libraries
- Multimodal Datasets: AudioSet, VGGSound, Kinetics-Sound, AVE, ESC-50 with video
- Synchronization: Dynamic time warping, CTC (Connectionist Temporal Classification)
- Real-Time Frameworks: GStreamer plugins, WebAssembly, WebCodecs
- Deployment: TensorRT, TorchScript, ONNX Runtime for optimized inference
- Professional Video Tools: Adobe Premiere plugins, DaVinci Resolve Fusion, Final Cut Pro
- Game Engines: Unity, Unreal Engine for adaptive game audio
- Cloud Services: AWS Elastic Transcoder, Google Cloud Video Intelligence API

## EXECUTION EXAMPLES

**Input:** "Generate suspenseful music for a video scene showing a person walking slowly down a dark hallway"
**Output:**
```python
# Initialize scorer
scorer = VisionAudioScorer(
    video_model_path="video_encoder.pt",
    audio_model_path="audio_decoder.pt",
    sample_rate=48000,
    fps=30
)

# Process video frames
audio_track = []
for frame in video_frames:
    audio_chunk = scorer.process_video_frame(frame)
    audio_track.append(audio_chunk)

# Concatenate audio chunks
final_audio = np.concatenate(audio_track)
sf.write("suspenseful_score.wav", final_audio, 48000)
```

**Input:** "Create a real-time system that generates sound effects for video game actions"
**Output:**
```python
# Real-time game audio scorer
class GameAudioScorer:
    def __init__(self):
        self.feature_extractor = VideoFeatureExtractor()
        # Pre-load sound effect mappings
        self.action_to_sfx = {
            "explosion": load_sfx("explosion.wav"),
            "gunshot": load_sfx("gunshot.wav"),
            "footstep": load_sfx("footstep.wav"),
            "jump": load_sfx("jump.wav"),
            "door_open": load_sfx("door_open.wav")
        }
        self.last_action = None
        self.action_cooldown = 0
    
    def process_frame(self, frame):
        # Extract features
        features = self.feature_extractor.extract_features([frame])
        action_probs = features["action"][0]  # First frame
        
        # Find most likely action
        action_idx = np.argmax(action_probs)
        action_name = self.feature_extractor.action_prompts[action_idx]
        confidence = action_probs[action_idx]
        
        # Trigger sound effect if confident enough and not on cooldown
        if confidence > 0.7 and self.action_cooldown <= 0:
            if action_name in self.action_to_sfx:
                play_sound_effect(self.action_to_sfx[action_name])
                self.action_cooldown = 30  # 30 frames cooldown (~0.5s at 60fps)
        
        # Decrease cooldown
        if self.action_cooldown > 0:
            self.action_cooldown -= 1
```
