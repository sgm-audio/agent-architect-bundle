---
name: ai-powered-mastering-chain-optimization
description: >-
  Use this skill when the user is working on or asking about AI mastering, intelligent mastering chain, automated EQ and compression, or ML-based audio mastering tools.
version: 1.0.0
---

# SKILL: AI-Powered Mastering Chain Optimization

## CAPABILITIES
- Use reinforcement learning to automatically sequence and parameterize mastering chains
- Optimize EQ, compression, limiting, and other mastering processors based on genre-specific loudness standards
- Adapt mastering processing to input audio characteristics in real-time
- Generate mastering presets that comply with broadcast and streaming loudness norms (LUFS)
- Integrate AI optimization into mastering plugins and DAWs

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Input audio characteristics (spectrum, dynamics, loudness) | Optimized mastering chain parameters |
| Target loudness standards (LUFS, true peak) | Processor settings (EQ bands, compressor thresholds, etc.) |
| Genre or style descriptors | Processing chain topology (order of processors) |
| Audio material references | Similar mastering settings |
| Real-time constraints (<10ms latency) | Optimized processing pipeline |

## IMPLEMENTATION PATTERN

```python
# AI-Powered Mastering Chain Optimizer using Reinforcement Learning
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from typing import List, Tuple, Dict, Optional
import random

# Define the mastering environment
class MasteringEnvironment:
    def __init__(self, 
                 sample_rate: int = 48000,
                 target_lufs: float = -14.0,
                 max_episode_steps: int = 1000):
        self.sample_rate = sample_rate
        self.target_lufs = target_lufs
        self.max_episode_steps = max_episode_steps
        self.current_step = 0
        
        # Define the action space: parameters for each processor
        # We'll have a fixed chain: EQ -> Compressor -> Limiter
        # Each processor has a set of parameters
        self.action_space = {
            'eq_low_gain': (-12.0, 12.0),      # dB
            'eq_mid_gain': (-12.0, 12.0),
            'eq_high_gain': (-12.0, 12.0),
            'comp_threshold': (-60.0, 0.0),    # dBFS
            'comp_ratio': (1.0, 20.0),         # ratio
            'comp_attack': (1.0, 100.0),       # ms
            'comp_release': (10.0, 1000.0),    # ms
            'limiter_ceiling': (-6.0, 0.0),    # dBTP
            'limiter_release': (10.0, 500.0)   # ms
        }
        self.action_names = list(self.action_space.keys())
        self.action_bounds = np.array([self.action_space[name] for name in self.action_names])
        
        # Observation space: audio features
        self.observation_space = {
            'lufs': (-70.0, 0.0),
            'true_peak': (-70.0, 0.0),
            'dynamic_range': (0.0, 30.0),
            'spectral_centroid': (0.0, sample_rate/2),
            'spectral_spread': (0.0, sample_rate/2),
            'zero_crossing_rate': (0.0, 1.0)
        }
        self.obs_names = list(self.observation_space.keys())
        self.obs_bounds = np.array([self.observation_space[name] for name in self.obs_names])
        
        # Initialize audio processor (simplified)
        self.audio_processor = AudioProcessor()
        self.reset()
    
    def reset(self):
        self.current_step = 0
        # Reset audio processor to neutral state
        self.audio_processor.reset()
        # Get initial observation from a segment of audio
        self.current_audio = self.get_audio_segment()
        obs = self._get_observation()
        return obs
    
    def step(self, action: np.ndarray) -> Tuple[np.ndarray, float, bool, dict]:
        # Apply action to audio processor
        self._apply_action(action)
        
        # Process audio segment
        processed_audio = self.audio_processor.process(self.current_audio)
        
        # Calculate reward based on how close we are to target
        reward = self._calculate_reward(processed_audio)
        
        # Move to next audio segment (or loop)
        self.current_step += 1
        self.current_audio = self.get_audio_segment()
        
        # Get new observation
        obs = self._get_observation()
        
        # Check if episode is done
        done = self.current_step >= self.max_episode_steps
        
        # Additional info
        info = {
            'lufs': self._measure_lufs(processed_audio),
            'true_peak': self._measure_true_peak(processed_audio),
            'dynamic_range': self._measure_dynamic_range(processed_audio)
        }
        
        return obs, reward, done, info
    
    def _apply_action(self, action: np.ndarray):
        # Map action to processor parameters
        action_dict = {}
        for i, name in enumerate(self.action_names):
            low, high = self.action_bounds[i]
            # Normalize action from [0,1] to [low, high]
            value = low + action[i] * (high - low)
            action_dict[name] = value
        
        # Apply to audio processor
        self.audio_processor.set_parameters(action_dict)
    
    def _get_observation(self) -> np.ndarray:
        # Measure features from current audio segment
        lufs = self._measure_lufs(self.current_audio)
        true_peak = self._measure_true_peak(self.current_audio)
        dynamic_range = self._measure_dynamic_range(self.current_audio)
        spectral_centroid = self._measure_spectral_centroid(self.current_audio)
        spectral_spread = self._measure_spectral_spread(self.current_audio)
        zcr = self._measure_zero_crossing_rate(self.current_audio)
        
        obs = np.array([lufs, true_peak, dynamic_range, spectral_centroid, spectral_spread, zcr])
        # Normalize observation to [0,1] for neural network
        obs_norm = (obs - self.obs_bounds[:,0]) / (self.obs_bounds[:,1] - self.obs_bounds[:,0])
        obs_norm = np.clip(obs_norm, 0.0, 1.0)
        return obs_norm
    
    def _calculate_reward(self, processed_audio: np.ndarray) -> float:
        # Reward based on proximity to target LUFS and true peak
        lufs = self._measure_lufs(processed_audio)
        true_peak = self._measure_true_peak(processed_audio)
        
        # We want LUFS close to target, true peak below -1 dBTP (for example)
        lufs_error = abs(lufs - self.target_lufs)
        tp_error = max(0, true_peak - (-1.0))  # Penalty if above -1 dBTP
        
        # Combine errors (lower is better)
        error = lufs_error + 2.0 * tp_error  # Weight true peak more
        
        # Reward is negative error (we want to maximize reward -> minimize error)
        reward = -error
        
        # Add bonus for good dynamic range (not over-compressed)
        dr = self._measure_dynamic_range(processed_audio)
        if dr > 8.0:  # Good dynamic range
            reward += 1.0
        elif dr < 4.0:  # Over-compressed
            reward -= 2.0
        
        return reward
    
    # Helper measurement functions (simplified)
    def _measure_lufs(self, audio: np.ndarray) -> float:
        # In practice, use pyloudnorm or similar
        # Placeholder: return RMS-based approximation
        rms = np.sqrt(np.mean(audio**2))
        # Rough conversion: LUFS ≈ 20*log10(RMS) - 10 (very approximate)
        return 20.0 * np.log10(max(rms, 1e-10)) - 10.0
    
    def _measure_true_peak(self, audio: np.ndarray) -> float:
        # In practice, use oversampling and peak measurement
        # Placeholder: return peak sample
        return 20.0 * np.log10(max(np.abs(audio), 1e-10))
    
    def _measure_dynamic_range(self, audio: np.ndarray) -> float:
        # In practice, use EBU R128 dynamic range
        # Placeholder: crest factor (peak to RMS ratio)
        rms = np.sqrt(np.mean(audio**2))
        peak = np.max(np.abs(audio))
        if rms > 0:
            return 20.0 * np.log10(peak / rms)
        else:
            return 0.0
    
    def _measure_spectral_centroid(self, audio: np.ndarray) -> float:
        # Simplified spectral centroid
        freqs = np.fft.rfftfreq(len(audio), 1.0/self.sample_rate)
        mag = np.abs(np.fft.rfft(audio))
        return np.sum(freqs * mag) / np.sum(mag) if np.sum(mag) > 0 else 0.0
    
    def _measure_spectral_spread(self, audio: np.ndarray) -> float:
        # Simplified spectral spread
        centroid = self._measure_spectral_centroid(audio)
        freqs = np.fft.rfftfreq(len(audio), 1.0/self.sample_rate)
        mag = np.abs(np.fft.rfft(audio))
        spread = np.sqrt(np.sum(((freqs - centroid)**2) * mag) / np.sum(mag)) if np.sum(mag) > 0 else 0.0
        return spread
    
    def _measure_zero_crossing_rate(self, audio: np.ndarray) -> float:
        # Zero crossing rate
        signs = np.sign(audio)
        zero_crossings = ((signs[1:] != signs[:-1]) & (signs[1:] != 0)).sum()
        return zero_crossings / len(audio)
    
    def get_audio_segment(self) -> np.ndarray:
        # In practice, this would return a segment of the audio being mastered
        # For demonstration, return a random audio segment
        # In a real implementation, this would be fixed audio or streaming
        duration = 10.0  # seconds
        t = np.linspace(0, duration, int(duration * self.sample_rate), False)
        # Generate a mix of sine waves and noise
        audio = np.sin(2*np.pi*100*t) * 0.3
        audio += np.sin(2*np.pi*300*t) * 0.2
        audio += np.sin(2*np.pi*1000*t) * 0.1
        audio += np.random.normal(0, 0.1, len(t))
        # Normalize
        audio = audio / np.max(np.abs(audio)) * 0.8
        return audio.astype(np.float32)

# Simplified audio processor (placeholder)
class AudioProcessor:
    def __init__(self):
        self.parameters = {
            'eq_low_gain': 0.0,
            'eq_mid_gain': 0.0,
            'eq_high_gain': 0.0,
            'comp_threshold': -20.0,
            'comp_ratio': 4.0,
            'comp_attack': 10.0,
            'comp_release': 100.0,
            'limiter_ceiling': -1.0,
            'limiter_release': 100.0
        }
    
    def reset(self):
        self.parameters = {
            'eq_low_gain': 0.0,
            'eq_mid_gain': 0.0,
            'eq_high_gain': 0.0,
            'comp_threshold': -20.0,
            'comp_ratio': 4.0,
            'comp_attack': 10.0,
            'comp_release': 100.0,
            'limiter_ceiling': -1.0,
            'limiter_release': 100.0
        }
    
    def set_parameters(self, params: Dict[str, float]):
        self.parameters.update(params)
    
    def process(self, audio: np.ndarray) -> np.ndarray:
        # Apply EQ (simplified as gain per band)
        # In practice, use actual filters
        low_mask = np.abs(np.fft.rfftfreq(len(audio), 1.0/self.sample_rate)) < 250
        mid_mask = (np.abs(np.fft.rfftfreq(len(audio), 1.0/self.sample_rate)) >= 250) & \
                   (np.abs(np.fft.rfftfreq(len(audio), 1.0/self.sample_rate)) < 4000)
        high_mask = np.abs(np.fft.rfftfreq(len(audio), 1.0/self.sample_rate)) >= 4000
        
        spectrum = np.fft.rfft(audio)
        spectrum[low_mask] *= 10**(self.parameters['eq_low_gain']/20)
        spectrum[mid_mask] *= 10**(self.parameters['eq_mid_gain']/20)
        spectrum[high_mask] *= 10**(self.parameters['eq_high_gain']/20)
        audio = np.fft.irfft(spectrum, len(audio))
        
        # Apply compressor (simplified)
        threshold = 10**(self.parameters['comp_threshold']/20)
        ratio = self.parameters['comp_ratio']
        # Simple compressor: reduce gain above threshold
        abs_audio = np.abs(audio)
        gain = np.ones_like(abs_audio)
        mask = abs_audio > threshold
        gain[mask] = (threshold + (abs_audio[mask] - threshold) / ratio) / abs_audio[mask]
        gain[np.abs(audio) < 1e-10] = 0  # Avoid division by zero
        audio = audio * gain
        
        # Apply limiter (simplified as soft clipping)
        ceiling = 10**(self.parameters['limiter_ceiling']/20)
        # Soft limiter using tanh
        audio = ceiling * np.tanh(audio / ceiling)
        
        return audio

# Agent (simplified policy network)
class MasteringAgent(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int):
        super(MasteringAgent, self).__init__()
        self.fc1 = nn.Linear(obs_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_dim)
        
    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = torch.tanh(self.fc3(x))  # Output in [-1, 1]
        return x

# Training loop (simplified)
def train_mastering_agent():
    env = MasteringEnvironment()
    obs_dim = len(env.obs_names)
    action_dim = len(env.action_names)
    agent = MasteringAgent(obs_dim, action_dim)
    optimizer = optim.Adam(agent.parameters(), lr=0.001)
    memory = []
    
    for episode in range(1000):
        obs = env.reset()
        done = False
        total_reward = 0
        
        while not done:
            obs_tensor = torch.from_numpy(obs).float().unsqueeze(0)
            action_tensor = agent(obs_tensor)
            action = action_tensor.detach().numpy()[0]
            # Action is in [-1, 1], convert to [0,1] for environment
            action_env = (action + 1) / 2
            
            next_obs, reward, done, info = env.step(action_env)
            
            memory.append((obs, action_env, reward, next_obs, done))
            obs = next_obs
            total_reward += reward
            
            # Train on batch
            if len(memory) >= 32:
                batch = random.sample(memory, 32)
                obs_batch, action_batch, reward_batch, next_obs_batch, done_batch = zip(*batch)
                
                obs_batch = torch.from_numpy(np.array(obs_batch)).float()
                action_batch = torch.from_numpy(np.array(action_batch)).float()
                reward_batch = torch.from_numpy(np.array(reward_batch)).float().unsqueeze(1)
                next_obs_batch = torch.from_numpy(np.array(next_obs_batch)).float()
                done_batch = torch.from_numpy(np.array(done_batch)).float().unsqueeze(1)
                
                # Compute current Q values
                current_q = agent(obs_batch)
                # For simplicity, we're using a Q-learning like update (not exactly correct for policy gradient)
                # In practice, use PPO, A2C, or similar
                next_q = agent(next_obs_batch)
                target_q = reward_batch + 0.99 * next_q * (1 - done_batch)
                
                loss = F.mse_loss(current_q, target_q.detach())
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                
                # Clear memory after training (for simplicity)
                memory = []
        
        print(f"Episode {episode}, Total Reward: {total_reward:.2f}")

# Usage example
if __name__ == "__main__":
    # Train the agent (this would take many episodes in practice)
    # train_mastering_agent()
    
    # For inference, use the trained agent
    env = MasteringEnvironment()
    agent = MasteringAgent(len(env.obs_names), len(env.action_names))
    # agent.load_state_dict(torch.load("mastering_agent.pt"))
    agent.eval()
    
    obs = env.reset()
    done = False
    while not done:
        obs_tensor = torch.from_numpy(obs).float().unsqueeze(0)
        with torch.no_grad():
            action_tensor = agent(obs_tensor)
        action = action_tensor.detach().numpy()[0]
        action_env = (action + 1) / 2  # Convert to [0,1]
        obs, reward, done, info = env.step(action_env)
        print(f"Step: {env.current_step}, Reward: {reward:.2f}, LUFS: {info['lufs']:.2f}")
```

## EDGE CASES & FALLBACKS
- **Reward Function Issues**: Shape reward to avoid local optima, use curriculum learning
- **Training Instability**: Use experience replay, target networks, or trust region methods
- **Over-Optimization to Training Audio**: Regularize with diverse audio material or use validation set
- **Latency Concerns**: Use smaller networks, fewer processors, or approximate inference
- **Parameter Interactions**: Model processor interactions explicitly or use hierarchical actions
- **Audio Quality Degradation**: Implement quality constraints in reward function
- **Genre Mismatch**: Condition policy on genre descriptors or use multi-task learning
- **Reference Drift**: Use loudness normalization in observation space
- **Exploration vs Exploitation**: Use entropy regularization or epsilon-greedy during training

## INTEGRATION POINTS
- Audio Processing: Librosa, Torchaudio, SciPy, pyloudnorm, Essentia
- Reinforcement Learning: Stable Baselines3, RLlib, TensorFlow Agents
- Mastering Plugins: VST3, AU, AAX, CLAP
- DAW Integration: AudioUnit, VST, AAX interfaces
- Reference Materials: LUFS meters, spectrum analyzers, vectorscopes
- Broadcasting Standards: EBU R128, ATSC A/85, Apple Music Sound Check
- Streaming Standards: Spotify Loudness Normalization, YouTube Loudness, Tidal
- Measurement Tools: TT Dynamic Range Meter, Youlean Loudness Meter, Waves WLM
- Deployment: ONNX, TorchScript, TensorRT for low-latency inference
- Cloud Training: AWS SageMaker, Google Vertex AI, Azure Machine Learning
- Hardware Acceleration: GPU (CUDA), TPUs for faster training

## EXECUTION EXAMPLES

**Input:** "Optimize a mastering chain for hip-hop music targeting -14 LUFS integrated loudness"
**Output:**
```python
# After training, use the agent to process hip-hop audio
env = MasteringEnvironment(target_lufs=-14.0)
# Assume we have a hip-hop audio segment
hip_hop_audio = load_hip_hop_sample()
env.current_audio = hip_hop_audio

obs = env.reset()
total_reward = 0
while not env.done:
    obs_tensor = torch.from_numpy(obs).float().unsqueeze(0)
    with torch.no_grad():
        action_tensor = agent(obs_tensor)
    action = action_tensor.detach().numpy()[0]
    action_env = (action + 1) / 2
    obs, reward, done, info = env.step(action_env)
    total_reward += reward
    if env.current_step % 100 == 0:
        print(f"Step {env.current_step}: LUFS={info['lufs']:.2f}, True Peak={info['true_peak']:.2f} dBTP")

# Get final parameters
final_params = env.audio_processor.parameters
print("Optimized Mastering Chain:")
print(f"  EQ Low: {final_params['eq_low_gain']:.1f} dB")
print(f"  EQ Mid: {final_params['eq_mid_gain']:.1f} dB")
print(f"  EQ High: {final_params['eq_high_gain']:.1f} dB")
print(f"  Compressor: Threshold={final_params['comp_threshold']:.1f} dB, Ratio={final_params['comp_ratio']:.1f}:1")
print(f"  Limiter: Ceiling={final_params['limiter_ceiling']:.1f} dBTP")
```

**Input:** "Create a real-time mastering assistant that suggests EQ settings based on input spectrum"
**Output:**
```python
# Real-time mastering suggestion system
class MasteringSuggester:
    def __init__(self):
        # Load pre-trained model for EQ suggestion
        self.eq_model = torch.jit.load("eq_suggester.pt")
        self.eq_model.eval()
    
    def suggest_eq(self, spectrum: np.ndarray) -> Dict[str, float]:
        # spectrum: magnitude spectrum (frequency bins)
        # Normalize and convert to tensor
        spectrum_tensor = torch.from_numpy(spectrum).float().unsqueeze(0).unsqueeze(0)
        with torch.no_grad():
            eq_params = self.eq_model(spectrum_tensor)
        # eq_params: [low_gain, mid_gain, high_gain] in dB
        return {
            'low': eq_params[0, 0].item(),
            'mid': eq_params[0, 1].item(),
            'high': eq_params[0, 2].item()
        }
    
    def process_audio(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        # Analyze audio
        spectrum = np.abs(np.fft.rfft(audio))
        freqs = np.fft.rfftfreq(len(audio), 1.0/sample_rate)
        
        # Suggest EQ
        eq_settings = self.suggest_eq(spectrum)
        
        # Apply EQ (simplified)
        low_mask = freqs < 250
        mid_mask = (freqs >= 250) & (freqs < 4000)
        high_mask = freqs >= 4000
        
        spectrum = np.fft.rfft(audio)
        spectrum[low_mask] *= 10**(eq_settings['low']/20)
        spectrum[mid_mask] *= 10**(eq_settings['mid']/20)
        spectrum[high_mask] *= 10**(eq_settings['high']/20)
        audio = np.fft.irfft(spectrum, len(audio))
        
        return audio
```