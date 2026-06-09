---
name: reinforcement-learning-for-synth-patching
description: >-
  Use this skill when the user is working on or asking about RL for synthesizer patching, reinforcement learning to find synth presets, automated sound design with AI, or patch optimization.
version: 1.0.0
---

# Skill: Reinforcement Learning for Synth Patching
## 📖 1. Overview
Trains RL agents to auto-dial synthesizer parameters to match user-provided target reference audio.
## ⚙️ 2. Core Functionality
- Environment: Synth plugin simulator (parameter space → audio → reward)
- Agent: PPO/SAC policy mapping target features → knob positions
- Reward Function: Spectral similarity, envelope match, harmonic alignment
- Fine-Tuning: User feedback loop, preference optimization
## 📥📤 3. Input/Output Schema
| Inputs | Target audio, synth parameter ranges, RL model | Outputs | Parameter vector, reward history, similarity score |
## 🏗️ 4. Architecture
`gym` env: `step(action) → synth.render() → compute_melspec() → reward`. Train with `stable-baselines3`. Deploy as ONNX policy.
## 🔗 5. Dependencies
`gymnasium`, `stable-baselines3`, `pytorch`, `librosa`
## ⚠️ 6. Edge Cases
| Local Minima | Poor match | Multi-start training, entropy regularization |
| Unplayable Patches | Unstable oscillators | Penalize NaN/clip, constrain action space |
| Slow Convergence | >10k steps | Pre-train on dataset, use expert demonstrations |
## 🛡️ 7. Constraints
- Inference: < 50ms parameter generation
- Reward: Spectral distance < 0.15
- Safety: Clamp all params to valid ranges
## 🤖 8. Usage
- *Prompt:* "Define a Gymnasium environment for a subtractive synth with reward based on Mel-spectrogram distance to a target."
## 🧪 9. Testing
- A/B listening tests
- Parameter boundary validation
- Reward curve stability analysis
## 📝 10. Best Practices
- Use normalized parameter space
- Save best checkpoints via early stopping
- Provide "randomize" fallback in UI
*Skill Version: 1.0.0 | Standards: PPO, Gymnasium, ONNX Policy | Domain: Audio AI & ML*