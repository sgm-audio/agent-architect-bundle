# Hermes + Ollama: Provider System Deep Dive

## The Core Problem

`hermes model` has no "Local Ollama" option. Menu shows LM Studio (option 4, first-class at `127.0.0.1:1234/v1`) and Ollama Cloud (option 20, `ollama.com/v1`), but not local Ollama. This doc traces why and how to work around it.

## Provider Alias Mapping

File: `hermes_cli/auth.py` line 1513

```python
"ollama": "custom",        # local Ollama → routes through "custom" provider
"ollama_cloud": "ollama-cloud",
"vllm": "custom",
"llamacpp": "custom",
```

So `"ollama"` is never a first-class provider — it maps to the generic `"custom"` type. Contrast with `"lmstudio"` which has its own `HermesOverlay` with a hardcoded `base_url_override="http://127.0.0.1:1234/v1"` (line 84-90 in `providers.py`).

## The Model Menu

File: `hermes_cli/main.py` — the `select_provider_and_model` function generates the numbered menu. There's no entry for local Ollama because no `HermesOverlay` exists for it. Options 29-30 ("custom" / "Custom endpoint") are the intended path for local Ollama.

## Auto-Detection of Local Server Type

File: `agent/model_metadata.py` lines 476-534 — `detect_local_server_type()`

```python
# Probing sequence:
# 1. /api/v1/models → "lm-studio" (most specific)
# 2. /api/tags with {"models": [...]} in response → "ollama"
# 3. /v1/props or /props with default_generation_settings in text → "llamacpp"
# 4. /version with {"version": ...} → "vllm"
```

Ollama detection works by hitting `http://<base_url>/api/tags` (strips `/v1` suffix first) and checking the response JSON for a `"models"` key. If present, it returns `"ollama"`.

## Auto-Select of Model Name

File: `hermes_cli/runtime_provider.py` lines 160-180 — `_auto_detect_local_model()`

```python
def _auto_detect_local_model(base_url: str) -> str:
    url = base_url.rstrip("/")
    if not url.endswith("/v1"):
        url += "/v1"
    resp = requests.get(url + "/models", timeout=5)
    if resp.ok:
        models = resp.json().get("data", [])
        if len(models) == 1:
            return models[0].get("id", "")
```

This only auto-selects when exactly ONE model is loaded in the local server. With multiple models (typical), it returns `""` and Hermes falls through to the configured default or the built-in default.

## The `providers` Dict vs `model` Section

Config supports two formats for custom/local providers:

### Legacy: `custom_providers` (list format)
```yaml
custom_providers:
  - name: "ollama-local"
    base_url: "http://localhost:11434/v1"
```

### New: `providers` (dict format, recommended)
```yaml
providers:
  ollama-local:
    base_url: http://localhost:11434/v1
    name: "Local Ollama"
    default_model: "huihui_ai/gemma-4-abliterated:e4b-q4_K"
```

Both are merged at runtime in `config.py::get_compatible_custom_providers()` (line 3862). The dict format is preferred because it gives a named key that Hermes can reference in `model.provider`.

## Runtime Resolution Chain

File: `hermes_cli/model_switch.py`

When you call `hermes chat` or do `/model`, the resolution chain is:

1. **Direct aliases** (`model_aliases` in config or built-in `DIRECT_ALIASES`) — checked first
2. **Provider aliases** (`_PROVIDER_ALIASES` dict in auth.py) — resolves `ollama` → `custom`
3. **Runtime provider** (`resolve_runtime_provider()` in `runtime_provider.py`) — looks up credentials, base_url
4. **Custom provider entries** — if the provider name matches a key in `providers` dict or `custom_providers` list, the configured `base_url` is used
5. **Fallback** — if resolution falls through to "custom" with no known base_url, it keeps the existing credentials

### Key code paths:

- `hermes_cli/model_switch.py` line 962: comment about `"ollama-launch"` as a named custom provider that `resolve_runtime_provider` doesn't know about
- `hermes_cli/auth.py` line 1500-1516: the `_PROVIDER_ALIASES` dict
- `hermes_cli/config.py` line 3848-3909: `providers_dict_to_custom_providers()` and `get_compatible_custom_providers()`
- `hermes_cli/config.py` line 3680-3740: `_normalize_custom_provider_entry()` — accepts `base_url`, `url`, `api` as URL keys; `apiKey`/`baseUrl` as camelCase aliases

## Verification Commands

```bash
# Check Ollama is running
curl -s http://localhost:11434/api/tags | python -c "import json,sys; d=json.load(sys.stdin); [print(m['name']) for m in d['models']]"

# Check Hermes sees the OpenAI-compatible model list
curl -s http://localhost:11434/v1/models

# Quick inference test
curl -s -X POST http://localhost:11434/api/generate \
  -d '{"model":"<model-name>","prompt":"hello in one word","stream":false}' \
  | python -c "import json,sys; print(json.load(sys.stdin).get('response','ERROR'))"
```

## Related Source Files

| File | Key Function | Purpose |
|------|-------------|---------|
| `hermes_cli/auth.py` | `_PROVIDER_ALIASES` dict (L1500) | Maps `"ollama"` → `"custom"` |
| `hermes_cli/providers.py` | `HERMES_OVERLAYS` dict | Per-provider transport/auth/URL config |
| `hermes_cli/runtime_provider.py` | `_auto_detect_local_model()` (L160) | Auto-pick model when 1 loaded |
| `hermes_cli/model_switch.py` | `parse_model_flags()`, `perform_model_switch()` | `/model` command resolution |
| `agent/model_metadata.py` | `detect_local_server_type()` (L476) | Probes known endpoints to identify server |
| `hermes_cli/config.py` | `get_compatible_custom_providers()` (L3862) | Merges providers/custom_providers for runtime |
