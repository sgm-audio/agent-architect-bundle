---
name: ollama
description: Use this skill when the user is working on or asking about Ollama, local LLM deployment with Ollama, model management, custom Modelfiles, Ollama API integration, embedding extraction, or running open-source language models locally.
version: 1.0.0
---

# Skill: Ollama Model Deployment

## 1. Overview
Covers operating Ollama for local LLM deployment — installing, pulling models, creating Modelfiles, tuning inference parameters, accessing the REST API, and embedding generation. Focuses on practical integration into developer workflows and audio plugin pipelines (e.g., semantic audio search, prompt-based sound generation).

## 2. Core Functionality
- **Ollama CLI:** `ollama pull`, `ollama run`, `ollama create`, `ollama list`, `ollama rm`, `ollama ps`, `ollama stop`
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

## 4. Architecture
Ollama wraps llama.cpp as a REST server with model management layer. Models are downloaded as GGUF blobs to `~/.ollama/models/`. The server maintains a model loading cache — `ollama run` keeps model in memory until evicted by `ollama stop` or another model's load. The `Modelfile` DSL compiles to GGUF metadata overlays (not new base models).

## 5. Dependencies
`ollama` binary, Windows/macOS/Linux, optional: CUDA Toolkit 11.3+ (NVIDIA), ROCm 5.7+ (AMD), Vulkan SDK (cross-vendor). Python: `ollama` pypi package for API scripting.

## 6. Edge Cases
| Out of Memory | Model too large for GPU VRAM | Set `num_ctx` lower (default 2048), use K-quant (Q4_K_M), enable `OLLAMA_GPU_OVERHEAD=512` |
| Model Not Found | Typo in model name | `ollama pull` first; check `ollama list` for available models |
| Slow Generation | CPU-only fallback | Verify `ollama ps` shows GPU layers; set `HIP_VISIBLE_DEVICES=0` or `CUDA_VISIBLE_DEVICES=0` |
| Connection Refused | Server not running | `ollama serve` in daemon mode; check `OLLAMA_HOST` env var |
| /api/embeddings returns empty | Model doesn't support embeddings | Use `nomic-embed-text` or `mxbai-embed-large` instead of chat models |

## 7. Constraints
- Ollama on Windows runs under WSL2 or natively via the Windows preview build
- Each model consumes VRAM ≈ model size in GB + KV cache (≈ 2 × `num_ctx` × layers × 2 bytes)
- `num_ctx` max practical: 8192 for most laptop GPUs, 32768 for desktop GPUs
- Embedding dimension varies by model: 768 (all-minilm), 1024 (nomic-embed-text), 1024 (mxbai-embed-large)

## 8. Usage
- *Prompt:* "Pull and run Llama 3.2 8B with Ollama, with Q4_K_M quantization and 4096 context."
- *Prompt:* "Create a custom Modelfile for a code-assistant with system prompt set to 'You are a C++ audio plugin expert'."
- *Prompt:* "Generate embeddings for a dataset of audio descriptions using nomic-embed-text via the Ollama API."
- *Prompt:* "Switch Ollama to run on my AMD iGPU instead of CPU."

## 9. Testing
- `ollama run llama3.2 "hello"` — smoke-test model loading and generation
- `curl http://localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"hello","stream":false}'`
- `ollama ps` — confirm model loaded and GPU layer count > 0
- Benchmark: `ollama run llama3.2` then measure tokens/sec from `/api/generate` response metrics

## 10. Best Practices
- Store Modelfiles in version control alongside the project (e.g., `models/code-assistant.modelfile`)
- Set `OLLAMA_NUM_PARALLEL=1` for interactive use, `OLLAMA_NUM_PARALLEL=4` for batch inference
- Use streaming API (`"stream": true`) for real-time chat, non-streaming for embedding
- Pin model versions with `ollama pull <model>:<tag>` (not `:latest`) for reproducibility
- Monitor VRAM: `ollama ps` shows per-model memory in "Size" column
- For audio plugin integration, use the REST API in a separate process — never embed Ollama in the audio thread
*Skill Version: 1.0.0 | Standards: Ollama 0.3+, GGUF, llama.cpp | Domain: Local LLM Deployment*
