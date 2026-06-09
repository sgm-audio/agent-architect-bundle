---
name: local-large-language-model-llm-orchestration
description: >-
  Use this skill when the user is working on or asking about local LLM inference, Ollama, llama.cpp, running language models locally, or orchestrating local AI models for audio.
version: 1.0.0
---

# Skill: Local Large Language Model (LLM) Orchestration
## 📖 1. Overview
Runs quantized local LLMs (Llama-3/Mistral via `llama.cpp`) offline inside DAW/app for conversational AI assistants without cloud latency or privacy risks.
## ⚙️ 2. Core Functionality
- GGUF Model Loading: `llama.cpp` context, KV cache allocation
- Prompt Engineering: System prompts for music production, context window management
- Streaming Output: Token-by-token generation for real-time UI feedback
- Resource Throttling: CPU/RAM limits, background thread priority
## 📥📤 3. Input/Output Schema
| Inputs | User query, conversation history, system prompt, model config | Outputs | Generated tokens, completion status, context usage metrics |
## 🏗️ 4. Architecture
`llama_context` initialized at plugin load. `llama_decode()` in background thread. Output streamed via `std::atomic<std::string>`. Cap tokens at 256 for speed.
## 🔗 5. Dependencies
`llama.cpp`, `GGUF` models, `json` config
## ⚠️ 6. Edge Cases
| Context Overflow | Truncation, loss of history | Sliding window, summarize old turns |
| RAM Exhaustion | DAW crash | Quantize to Q4_K_M, cap KV cache to 2048 |
| Hallucination | Incorrect plugin advice | Ground responses in manual via RAG fallback |
## 🛡️ 7. Constraints
- Latency: < 3s for 100 tokens
- Memory: < 4GB RAM
- CPU: < 40% single-core, priority `IDLE`
## 🤖 8. Usage
- *Prompt:* "Generate a `llama.cpp` C++ wrapper that streams tokens to a DAW editor with context window management."
## 🧪 9. Testing
- Throughput (tokens/sec) benchmark
- Context retention stress
- Offline capability validation
## 📝 10. Best Practices
- Pre-load model on startup; defer init if RAM < 8GB
- Use `GGML` backend for CPU acceleration
- Provide "Stop Generation" UI button
*Skill Version: 1.0.0 | Standards: llama.cpp, GGUF, Local LLM | Domain: Audio AI & ML*