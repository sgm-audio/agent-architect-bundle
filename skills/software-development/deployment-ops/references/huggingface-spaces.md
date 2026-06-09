# HuggingFace Spaces Deployment Reference

## SDK Selection

| SDK | Use Case | Notes |
|-----|----------|-------|
| `sdk: gradio` | Simple apps, no exotic deps | HF manages Python version (latest) |
| `sdk: streamlit` | Data viz apps | Same as gradio |
| `sdk: docker` | Need specific Python version, system deps, or custom environment | Full control, slower builds |

## Critical Config (README frontmatter)

```yaml
---
title: App Name
emoji: 🎸
colorFrom: blue
colorTo: purple
sdk: docker          # or gradio / streamlit
app_file: Dockerfile # for docker SDK; app.py for gradio SDK
license: mit
---
```

## Docker Space Best Practices

### Python Version Pinning
- TF < 2.16 requires Python ≤ 3.11
- TF 2.16+ works on Python 3.12
- Python 3.13 has limited TF support (only 2.20+)
- **For Basic Pitch (TF-based):** Use Python 3.11 + TF 2.15
```dockerfile
FROM python:3.11-slim
```

### Critical: Bind to 0.0.0.0
HF proxy can't reach `127.0.0.1`. Always launch on all interfaces:
```python
demo.launch(server_name="0.0.0.0")  # NOT demo.launch()
```

### Filesystem
- Working dir is `/app`
- Port is `7860`
- No persistent storage between restarts (ephemeral)
- Use HF Buckets (`hf buckets`) for persistent data

## Common Build Errors & Fixes

### "No module named 'X'"
Add to `requirements.txt`, push, rebuild.

### TensorFlow version not found
TF releases are Python-version-specific. Check [pypi.org/project/tensorflow](https://pypi.org/project/tensorflow/#history) for compatible versions.

### "Could not find a version that satisfies the requirement"
Often caused by Python version mismatch. Switch to Docker SDK and pin the base image to a compatible Python version.

### Gradio version conflicts
If `sdk: gradio`, HF installs Gradio automatically via `sdk_version`. Don't pin gradio in requirements.txt — let HF manage it. If Docker, add gradio to requirements.

### Space stuck at APP_STARTING
Check runtime logs: `hf spaces logs <namespace>/<space-name>`. Common causes:
- TF import taking 5+ minutes on CPU (normal)
- App crashed silently — check logs for traceback
- Bound to 127.0.0.1 instead of 0.0.0.0

## HF CLI Commands

```bash
# Login
hf auth login --token <token>

# Create space (if not existing)
hf repos create <name> --type space --space-sdk gradio

# Check status
hf spaces info <namespace>/<name>

# View logs
hf spaces logs <namespace>/<name>         # runtime logs
hf spaces logs <namespace>/<name> --build  # build logs

# Set hardware
hf spaces settings <namespace>/<name> --hardware cpu-basic
hf spaces settings <namespace>/<name> --hardware zero-a10g  # requires PRO

# Push code (git)
git remote add hf https://<user>:<token>@huggingface.co/spaces/<namespace>/<name>
git push hf main
```

## Hardware Tiers

| Name | CPU | RAM | GPU | Cost |
|------|-----|-----|-----|------|
| cpu-basic | 2 vCPU | 16 GB | — | Free |
| cpu-upgrade | 8 vCPU | 32 GB | — | $0.03/hr |
| zero-a10g | Dynamic | — | A10G (shared) | Free (PRO req.) |
| t4-small | 4 vCPU | 15 GB | T4 16GB | $0.40/hr |
| a10g-small | 4 vCPU | 15 GB | A10G 24GB | $1.00/hr |

## Deps That Often Break

- **tensorflow**: Python version locked. Check compatibility before deploying.
- **basic-pitch**: Pulls TF. Can use ONNX backend instead (`pip install basic-pitch[onnx]`) for CPU-only.
- **demucs**: Needs PyTorch + torchaudio (huge). Skip on free tier.
- **torch**: 192MB+ download. Use `--index-url https://download.pytorch.org/whl/cpu` for CPU-only.
- **onnxruntime**: Lightweight CPU version is `onnxruntime` (not `onnxruntime-gpu`).
