# Training Pipeline Reference

## Location
Training code at `C:\Users\<user>\OneDrive\Documents\training\`

## Files
- `train_eq_agent.py` — EQ optimization RL agent
- `train_dynamics_agent.py` — Dynamics processing RL agent  
- `train_spatial_agent.py` — Spatial audio RL agent
- `train_critic.py` — Critic model for RL training
- `train_joint.py` — Joint training (all agents together)
- `audio_env.py` — Audio environment for RL
- `data_loader.py` — Dataset loading
- `download_datasets.py` — Dataset download utilities
- `train_config.yaml` — Training configuration

## Checkpoint
`best.pt` at 100K steps, 8MB, located at:
`C:\dev\mamba3\mamba3\checkpoints_laptop\best.pt`

## Free GPU Options
- **Modal**: $30/mo free credits. Use `setup_gcloud.sh` as reference for cloud setup.
- **Kaggle**: Free GPU (30hrs/week). Notebook-based.
- **Google Colab**: Free T4 GPU. Good for quick experiments.

## Architecture
The training uses RL (Reinforcement Learning) with separate agents for different audio processing tasks (EQ, dynamics, spatial), a shared critic, and joint training mode. The audio environment simulates DAW-like signal chains.
