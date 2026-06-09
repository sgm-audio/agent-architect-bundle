---
name: hermes-performance-tuning
description: "Optimize Hermes Agent performance: provider selection, model tuning, config trimming, credential pooling, local inference."
version: 1.0.0
author: SGM Studios
license: MIT
tags: [hermes, performance, latency, optimization]
---

# Hermes Performance Tuning

## Quick Wins

- **Provider selection**: Use `hermes model` to pick the fastest model for your task. DeepSeek flash models are fast + cheap. Local models via Ollama have zero network latency but may be slower on CPU.
- **Credential pooling**: `hermes auth add PROVIDER` adds multiple API keys. Hermes cycles through them, reducing rate-limit stalls.
- **Tool trimming**: `hermes tools disable NAME` removes unused toolsets — fewer tools = smaller prompts = faster responses.
- **Context compression**: Terminal: `--yolo` bypasses approval prompts. `/compress` manually compresses context when it gets long.
- **`/fast`**: Toggle priority processing for urgent queries.

## Config Tuning

```yaml
# Faster model fallback
model:
  provider: openrouter
  default: deepseek/deepseek-chat

# Reduce max turns (default 90)
agent:
  max_turns: 30

# Minimal terminal timeout
terminal:
  timeout: 60
```

## Local Models (Ollama)

- **Fastest local**: `gemma-3-4b-it-q4` (4-bit quantized, runs on CPU)
- **Balanced**: `qwen2.5-7b` or `deepseek-coder-6.7b`
- Use `ollama run <model>` to test inference speed before setting as default.

### Configuring Ollama as a Hermes Provider

Local Ollama does NOT appear as a first-class option in `hermes model`. The menu has LM Studio (option 4) and Ollama Cloud (option 20) but not local Ollama. Internally `"ollama"` maps to `"custom"` (`hermes_cli/auth.py` line 1513).

**Method: Named custom provider (recommended)**

Add an entry to the `providers:` dict in `config.yaml` — this preserves your remote provider as default and lets you switch with `/model`:

```yaml
providers:
  ollama-local:
    base_url: http://localhost:11434/v1
    name: "Local Ollama"
    default_model: "huihui_ai/gemma-4-abliterated:e4b-q4_K"

# Then switch active model to it:
model:
  default: huihui_ai/gemma-4-abliterated:e4b-q4_K
  provider: ollama-local
  base_url: http://localhost:11434/v1
```

Set via CLI:
```bash
hermes config set providers.ollama-local.base_url "http://localhost:11434/v1"
hermes config set providers.ollama-local.name "Local Ollama"
hermes config set providers.ollama-local.default_model "huihui_ai/gemma-4-abliterated:e4b-q4_K"
hermes config set model.provider ollama-local
hermes config set model.base_url http://localhost:11434/v1
hermes config set model.default "huihui_ai/gemma-4-abliterated:e4b-q4_K"
```

**Switching back to remote provider:**
```bash
hermes config set model.provider deepseek
hermes config set model.default deepseek-v4-flash
hermes config set model.base_url https://api.deepseek.com/v1
```

**Auto-detection:** Hermes detects Ollama by probing `http://<base_url>/api/tags` for `{"models": [...]}` (see `agent/model_metadata.py::detect_local_server_type`). The `_auto_detect_local_model` function in `hermes_cli/runtime_provider.py` queries `/v1/models` but only auto-selects when exactly 1 model is loaded — won't auto-pick with multiple models.

**Reference:** See `references/hermes-ollama-provider.md` for the full source-level provider system tracing.

## Pitfalls

- Switching provider mid-session requires `/reset` or restart
- Too many API keys in a pool doesn't help if your rate limit is per-account, not per-key
- Local models with <7B params may struggle with complex tool calls — test before making permanent
- Local Ollama does not appear in the `hermes model` interactive menu — use the `providers:` config approach above instead
- The `_auto_detect_local_model` function only works when Ollama has exactly 1 model loaded; with multiple models you must specify `model.default` explicitly
