---
name: ollama
description: "Use this skill when the user is working on or asking about Ollama, local LLM deployment with Ollama, model management, custom Modelfiles, Ollama API integration, embedding extraction, or running open-source language models locally."
version: 1.1.0
author: OpenCode (migrated to Hermes) + Hermes agent session Jun 2026
license: MIT
metadata:
  hermes:
    tags: ["Ollama", "opencode-migrated"]
    related_skills: []
---


# Skill: Ollama Model Deployment

## 1. Overview
Covers operating Ollama for local LLM deployment — installing, pulling models, creating Modelfiles, tuning inference parameters, accessing the REST API, and embedding generation. Focuses on practical integration into developer workflows and audio plugin pipelines (e.g., semantic audio search, prompt-based sound generation).

## 2. Core Functionality
- **Ollama CLI:** `ollama pull`, `ollama run`, `ollama create`, `ollama list`, `ollama rm`, `ollama ps`, `ollama stop`, `ollama serve`
- **Performance env vars:** `OLLAMA_NUM_PARALLEL=1` (interactive), `OLLAMA_NUM_PARALLEL=4` (batch), `OLLAMA_GPU_OVERHEAD=512`
- **GPU env vars (Windows):** Set via System Properties > Environment Variables, or `setx OLLAMA_NUM_PARALLEL 1` — NOT `export`, which is Unix-only
- **Modelfiles:** Creating custom models with `FROM`, `PARAMETER`, `TEMPLATE`, `SYSTEM`, `LICENSE`, `ADAPTER`, `MESSAGE` directives
- **Ollama REST API:** `/api/generate`, `/api/chat`, `/api/embeddings`, `/api/create`, `/api/pull`, `/api/tags`, `/api/ps`
- **Embedding Extraction:** Using `nomic-embed-text`, `mxbai-embed-large`, `all-minilm` for semantic search / RAG
- **GPU Acceleration:** Ollama with CUDA, ROCm (HIP), Vulkan backends — `OLLAMA_GPU_OVERHEAD`, `HIP_VISIBLE_DEVICES`
- **Multi-Model Serving:** Running multiple models concurrently, VRAM budgeting, swapping to CPU offload
- **Quantization:** Q4_K_M, Q5_K_M, Q8_0, IQ4_XS — tradeoffs between quality, speed, and memory
- **Ollama + LangChain/LlamaIndex:** Integration for agentic RAG pipelines

## 3. Input/Output Schema
| Inputs | Model name, prompt text, parameters (temperature, top_p, top_k, repeat_penalty, num_ctx, num_predict), Modelfile path |
| Outputs | Generated text stream, embedding vector, model manifest, inference statistics (tokens/sec, prompt_eval_count) |
| API Port | `http://localhost:11434` (configurable via `OLLAMA_HOST`) |
| Default num_ctx | Usually 2048 for CLI, but can be **131072** on some builds — check `ollama ps` SIZE column to see actual memory consumption |

## 4. Architecture
Ollama wraps llama.cpp as a REST server with model management layer. Models are downloaded as GGUF blobs to `~/.ollama/models/`. The server maintains a model loading cache — `ollama run` keeps model in memory until evicted by `ollama stop` or another model's load. The `Modelfile` DSL compiles to GGUF metadata overlays (not new base models).

## 5. Dependencies
`ollama` binary, Windows/macOS/Linux, optional: CUDA Toolkit 11.3+ (NVIDIA), ROCm 5.7+ (AMD), Vulkan SDK (cross-vendor). Python: `ollama` pypi package for API scripting.

### The num_ctx Memory Trap

The `ollama run` default context length can be **131072 tokens** on some builds. This balloons KV cache memory: a 2.5 GB model can show as **6.1 GB** in `ollama ps`. Always set a sensible `num_ctx` in your Modelfile or API call (e.g., `num_ctx 4096` or `num_ctx 8192`).

## 6. Windows-Specific Setup

### Setting Environment Variables
On Windows, use `setx` (persistent) or System Properties > Environment Variables:
```cmd
setx OLLAMA_NUM_PARALLEL 1
setx OLLAMA_GPU_OVERHEAD 512
```
Restart Ollama after changing env vars. `export` is Unix-only — does not work.

### Updating Ollama
Check for updates: `ollama --version`

**Via winget (recommended on Windows):**
```powershell
winget upgrade --id Ollama.Ollama --accept-source-agreements --accept-package-agreements
```
Auto-downloads the latest version. File is ~1.3 GB — can timeout on slow connections. Re-run to resume.

**Manual:** Download installer from https://ollama.com/download/windows.
Or check the app UI — it logs "New update available" in server output with the exact download URL.

### Diagnosing GPU Acceleration on Windows
1. Run a model: `ollama run <model> "test"`
2. In another terminal: `ollama ps`
3. Check PROCESSOR column:
   - "100% CPU" = no GPU acceleration active
   - "9%/91% CPU/GPU" = partial GPU offload
   - "100% GPU" = fully GPU accelerated
4. On AMD Radeon iGPUs (860M, 780M, etc.), Windows Ollama <0.5 ships no Vulkan support. Update to 0.30+ and the Vulkan backend may detect the iGPU. Verify with `ollama ps` after update.

### Hardware Info on Windows from WSL/git-bash
- CPU: `cat /proc/cpuinfo` (shows model, cores, AVX512 flags, hypervisor detection)
- RAM: `cat /proc/meminfo` (MemTotal, MemFree)
- GPU: `powershell.exe -Command "Get-CimInstance Win32_VideoController | Select-Object Name,AdapterRAM | Format-List"` or `clinfo` (from git-bash/WSL) for GPU name, architecture gfx#, VRAM
- ROCm check: `ls /dev/kfd 2>/dev/null || echo "no /dev/kfd (ROCm)"`
- Vulkan check: `ls /dev/dri 2>/dev/null || echo "no /dev/dri"`
- CPU/cores: `powershell.exe -Command "Get-CimInstance Win32_Processor | Select-Object Name,NumberOfCores,NumberOfLogicalProcessors | Format-List"`

## Cross-Platform Model Migration (Windows <-> Linux)

When moving Ollama to a new OS (e.g., Windows -> Bazzite/Fedora):

1. **Backup model blobs:**
   - Source: `~/.ollama/models/` (Windows: `C:\Users\<user>\.ollama\models\`)
   - Contains: `blobs/` (large ~12GB), `manifests/` (small metadata)
   - Copy both directories. On Windows, onedrive may back up `.ollama/`
   
2. **On the new OS:**
   ```bash
   # Install Ollama first
   # Copy blobs to ~/.ollama/models/blobs/
   # Copy manifests to ~/.ollama/models/manifests/
   # ollama list  # should show all models
   ```
   
3. **Alternative: just re-pull** — if internet is fast enough:
   ```bash
   ollama pull gemma-3-4b-it-q4
   ollama pull qwen2.5:7b
   # etc.
   ```
   Models are cached per-machine. re-pulling on new OS downloads fresh.
   Migration is simpler than you think — Ollama stores GGUF blobs keyed by SHA256 digest. Same model = same digests across all OS.

4. **Hermes config on new OS:**
   - Windows: `C:\Users\<user>\AppData\Local\hermes\config.yaml`
   - Linux: `~/.config/hermes/config.yaml`
   - Copy the file directly. Update any Windows-specific paths inside.

### RAM Budgeting for Model Selection

On a system with **32 GB total RAM** and ~16 GB free:

| Model Size | Max Context | Est. Total Memory | Risk |
|------------|-------------|-------------------|------|
| 1.2 GB (1B) | 16K | ~2 GB | Safe |
| 821 MB (1.3B MoE) | 8K | ~1.5 GB | Safe |
| 2.5 GB (4B) | 8K | ~4 GB | Safe |
| 4.7 GB (7B) | 8K | ~7 GB | Safe |
| 5.5 GB (8B vision) | 4K | ~7 GB | Safe |
| 9.6 GB (12B) | 4K | ~11 GB | Tight — may swap |
| 9.6 GB (12B) | 2K | ~10 GB | Manageable |

**KV cache formula:** ~2 MB per 1K tokens of context per 1B parameters.
So a 12B model at 4K context = 12 × 4 × 2 = ~96 MB KV cache overhead.

**Rule of thumb:** model_size + 10% overhead + KV cache. Leave 2-4 GB for the OS.

## 7. Edge Cases

| Edge Case | Symptom | Fix |
|---|---|---|
| Out of Memory | Model too large for GPU VRAM | Set `num_ctx` lower (default 2048), use K-quant (Q4_K_M), enable `OLLAMA_GPU_OVERHEAD=512` |
| Model Not Found | Typo in model name | `ollama pull` first; check `ollama list` for available models |
| Slow Generation | CPU-only fallback | Verify `ollama ps` shows GPU layers; set `HIP_VISIBLE_DEVICES=0` or `CUDA_VISIBLE_DEVICES=0` |
| GPU Not Used on Windows (AMD) | Radeon iGPU not detected | Check `ollama ps` PROCESSOR column - "100% CPU" means no GPU. Radeon integrated GPUs need Vulkan backend (Ollama 0.5+). ROCm is Linux-only for AMD GPUs. |
| Connection Refused | Server not running | `ollama serve` in daemon mode; check `OLLAMA_HOST` env var |
| /api/embeddings returns empty | Model doesn't support embeddings | Use `nomic-embed-text` or `mxbai-embed-large` instead of chat models |

## 8. Constraints
- Ollama on Windows runs under WSL2 or natively via the Windows preview build
- Each model consumes VRAM ≈ model size in GB + KV cache (≈ 2 × `num_ctx` × layers × 2 bytes)
- `num_ctx` max practical: 8192 for most laptop GPUs, 32768 for desktop GPUs
- Embedding dimension varies by model: 768 (all-minilm), 1024 (nomic-embed-text), 1024 (mxbai-embed-large)

## 9. Usage
- *Prompt:* "Pull and run Llama 3.2 8B with Ollama, with Q4_K_M quantization and 4096 context."
- *Prompt:* "Create a custom Modelfile for a code-assistant with system prompt set to 'You are a C++ audio plugin expert'."
- *Prompt:* "Generate embeddings for a dataset of audio descriptions using nomic-embed-text via the Ollama API."
- *Prompt:* "Switch Ollama to run on my AMD iGPU instead of CPU."

## 10. Testing
- `ollama run llama3.2 "hello"` — smoke-test model loading and generation
- `curl http://localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"hello","stream":false}'`
- `ollama ps` — confirm model loaded and GPU layer count > 0
- Benchmark: `ollama run llama3.2` then measure tokens/sec from `/api/generate` response metrics

## 11. Best Practices
- Store Modelfiles in version control alongside the project (e.g., `models/code-assistant.modelfile`)
- Set `OLLAMA_NUM_PARALLEL=1` for interactive use, `OLLAMA_NUM_PARALLEL=4` for batch inference
- Use streaming API (`"stream": true`) for real-time chat, non-streaming for embedding
- Pin model versions with `ollama pull <model>:<tag>` (not `:latest`) for reproducibility
- Monitor VRAM: `ollama ps` shows per-model memory in "Size" column
- For audio plugin integration, use the REST API in a separate process — never embed Ollama in the audio thread

## 12. Windows GPU Diagnostics (Quick Reference)

When a user says "Ollama isn't using my AMD iGPU":

1. `ollama ps` — check PROCESSOR column. "100% CPU" = no GPU.
2. `ollama --version` — if < 0.30, GPU (especially AMD iGPU) support is limited.
3. `clinfo` from git-bash/WSL — shows GPU name and gfx# (e.g., gfx1152 = Radeon 860M RDNA 3.5).
4. Update Ollama to latest → re-test `ollama ps`.
5. AMD iGPUs on Windows need Vulkan backend (Ollama 0.5+ on Windows). ROCm is Linux-only for AMD GPUs.

## 13. Reference Files

This skill ships with supporting reference files:

| File | Contents |
|------|----------|
| `references/hermes-provider-wiring.md` | Configuring Ollama as a Hermes provider — yaml syntax, model name gotchas, RAM considerations |
| `references/bazzite-migration.md` | Migrating from Windows to Bazzite (Fedora Atomic) — immutable OS implications, ROCm setup, distrobox workflow for C++ audio plugin dev |

Check these when the task involves Hermes integration or cross-OS migration.

*Skill Version: 1.2.0 | Standards: Ollama 0.3+, GGUF, llama.cpp | Domain: Local LLM Deployment*
