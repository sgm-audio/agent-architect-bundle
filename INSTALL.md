# Installation Guide

## Hermes Agent Skills

### Via Tap (Recommended)
```bash
hermes skills tap add scottmills306/agent-architect-bundle
hermes skills list          # See all available skills
hermes skills search audio  # Search for audio-related skills
```

### Manual
Copy individual skill directories to your Hermes skills folder:
```bash
cp -r skills/audio-dsp ~/.hermes/skills/
```

## OpenCode Agent System

### Full Install
```bash
# Backup your current config first
cp -r ~/.config/opencode ~/.config/opencode.backup

# Copy the entire system
cp -r opencode/* ~/.config/opencode/
```

### Selective Install
```bash
# Install specific agents
cp opencode/agents/code-reviewer.md ~/.config/opencode/agents/
cp opencode/agents/bug-hunter.md ~/.config/opencode/agents/

# Install specific skills
cp -r opencode/skills/frontend-build ~/.config/opencode/skills/
```

### Configuration
Edit `~/.config/opencode/opencode.jsonc` to set your API keys:
- NVIDIA NIM: Set `NVIDIA_API_KEY` environment variable
- Ollama: Ensure Ollama is running on localhost:11434

## Verifying Installation

### Hermes
```bash
hermes skills list           # Should show installed skills
hermes skills inspect audio-dsp/mamba3-dsp-methodology  # Preview a skill
```

### OpenCode
OpenCode will load agents from `~/.config/opencode/agents/` and skills from `~/.config/opencode/skills/` automatically.

Check `~/.config/opencode/opencode.jsonc` includes:
```json
"instructions": [
    "~/.config/opencode/AGENTS.md",
    "~/.config/opencode/meta-orchestrator.md"
]
```
