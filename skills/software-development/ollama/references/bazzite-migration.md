# Bazzite OS Migration for Audio/ML Development

**Bazzite** = Fedora Atomic (Silverblue variant). Immutable rootfs. Uses `rpm-ostree` for system packages and `distrobox` (podman containers) for development environments.

## Why Bazzite for MAAPS Suite

| Need | Windows | Bazzite |
|------|---------|---------|
| Ollama GPU | CPU-only (no AMD ROCm on Windows) | **ROCm native** — Radeon 860M (gfx1152) supported |
| REAPER | Native Windows build | Native Linux build (same license) |
| CLAP plugins | CLAP SDK works | CLAP SDK works, PipeWire audio |
| C++ dev | VS 2022 + clang-cl | GCC/Clang via distrobox |

## Migration Path

### What Transfers Directly

| Data | Windows Path → | Linux Path |
|------|----------------|------------|
| Source code | `C:\dev\*` → | `~/dev/` |
| Hermes config | `C:\Users\<user>\AppData\Local\hermes\` → | `~/.config/hermes/` |
| Ollama models | `~/.ollama/models/` → | `~/.ollama/models/` (copy blobs/) |
| Hermes skills | Same — skills dir inside hermes home | Same layout |
| RAG corpus | Under Hermes home | Copy recursively |
| Session DB | `state.db` | Same file, copy directly |
| Git repos | Any | Same — `git remote -v` works |

### What Changes

| Tool | Windows | Bazzite |
|------|---------|---------|
| Package manager | winget, chocolatey | `rpm-ostree install` (system) or `distrobox enter` (dev) |
| Shell | git-bash/MSYS | Native bash (no path translation needed) |
| IDE | VS 2022 | VS Code (flatpak) or Codium |
| Docker | Docker Desktop | podman (built-in) |
| GPU compute | No AMD GPU in Ollama | ROCm 6.x — `sudo dnf install rocm-hip` |
| Hermes install | Download.exe installer | `curl -fsSL https://hermes-agent.nousresearch.com/install.sh \| bash` |
| Hermes home | `C:\Users\<user>\AppData\Local\hermes\` | `~/.config/hermes/` |
| Audio stack | ASIO/WASAPI | PipeWire + JACK (low-latency) |

## Important: Immutable OS Implications

Bazzite root is read-only. You **cannot** `sudo dnf install` directly (well, `rpm-ostree install` layers packages, but it's not the intended workflow for dev tools).

**Pattern for dev:**
```bash
# Create a dev container
distrobox create --name mamba3-dev --image fedora:41
distrobox enter mamba3-dev

# Inside the container — full dnf access
sudo dnf install cmake gcc clang clang-tools-extra juce-devel \
  python3-pip python3-devel

# Build audio plugins inside the container
# Copy the binary out to test on the host
```

**REAPER runs on the host** (flatpak or direct download). Built plugins are copied from the container to `~/.vst/` or `~/.clap/` on the host for testing.

## Getting ROCm Working on Bazzite

```bash
# Layer the ROCm packages
rpm-ostree install rocm-hip rocm-clinfo rocminfo
systemctl reboot  # required for rpm-ostree changes

# Verify
rocminfo
clinfo | grep "Device Name"

# Ollama should auto-detect the iGPU after reboot
ollama run gemma-3-4b-it-q4 "test"
ollama ps  # Check PROCESSOR column
```

## Migration Script

A complete migration script is at `C:\dev\ollama-setup\migrate-to-bazzite.sh`. Run it from Windows before wiping the drive. It backs up:
- All projects, Hermes config+skills+memory+RAG, Ollama blobs, backlog archive, bashrc/gitconfig/ssh
