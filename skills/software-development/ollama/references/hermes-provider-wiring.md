# Wiring Ollama as a Hermes Provider

## Provider Config in config.yaml

```yaml
model:
  default: <model-name>
  provider: ollama-launch

providers:
  ollama-launch:
    api: http://127.0.0.1:11434/v1
    default_model: <model-name>
    models:
      - model-1
      - model-2
      # etc.
    name: Ollama
```

## Switching Mid-Session

```bash
hermes config set model.provider ollama-launch
hermes config set model.default gemma-3-4b-it-q4:latest
```

Needs a fresh session (`/reset` or new `hermes` invocation) to pick up.

## Verifying the API is Running

```bash
curl -s http://127.0.0.1:11434/api/tags
```

Returns JSON list of available models. If connection refused, start Ollama first.

## Common Pitfall

The model name in Hermes config must **exactly** match what `curl /api/tags` returns under `"name"`. Watch for:
- HuggingFace-style names: `hf.co/Tekimax/granite-ml-coder-GGUF:Q4_K_M`
- Namespaced: `huihui_ai/gemma-4-abliterated:e4b-q4_K`
- Tag suffixes: `gemma-3-4b-it-q4:latest`

## RAM Budget for Multiple Models

Hermes loads one model at a time via Ollama — no need to budget for concurrent loads. But if you set `OLLAMA_NUM_PARALLEL > 1`, each concurrent request loads its own model copy.
