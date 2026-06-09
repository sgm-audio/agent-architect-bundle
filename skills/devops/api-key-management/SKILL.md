---
name: api-key-management
description: "Use when the user dumps multiple API keys at once, or when you need to set up credentials in .env across providers. Covers secure parsing, writing, verification, and deduplication of bulk credential pastes."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [credentials, api-keys, env, security, setup]
    related_skills: [hermes-agent]
---

# API Key Management

## Overview

Users often paste a batch of API keys in a single message — sometimes 10-15 keys at once. This skill provides a repeatable protocol for handling those dumps securely, writing them to `.env`, verifying they were written correctly, and configuring the corresponding providers in `config.yaml`.

## When to Use

- User pastes a block of API keys in natural language ("my X key is sk-... my Y key is...")
- User asks you to set up credentials for a new provider
- You need to add API keys to `.env` for tools that require them (web search, STT, TTS, GitHub, etc.)
- After adding credentials, you need to verify they're usable

Not for: handling secrets through `hermes auth` (OAuth flow), editing pre-existing auth files, or credential rotation on already-configured systems.

## Key Format Recognition by Prefix

| Prefix | Provider | Env Var |
|--------|----------|---------|
| `sk-or-v1-` | OpenRouter | `OPENROUTER_API_KEY` |
| `sk-` (35-40 chars) | DeepSeek / OpenAI | `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` |
| `sk-` (60-70 chars) | OpenCode / misc OpenAI-compat / OpenRouter | `OPENCODE_ZEN_API_KEY`, `OPENCODE_GO_API_KEY` |
| `sk-or-v1-` (70+ chars) | OpenRouter | `OPENROUTER_API_KEY` |
| `github_pat_` | GitHub PAT | `GITHUB_TOKEN` |
| `gsk_` | Groq | `GROQ_API_KEY` |
| `fc-` | Firecrawl | `FIRECRAWL_API_KEY` |
| `tvly-` | Tavily | `TAVILY_API_KEY` |
| `ntn_` | Notion | `NOTION_API_KEY` |
| `re_` | Resend | `RESEND_API_KEY` |
| `e2b_` | E2B | `E2B_API_KEY` |
| `lsv2_` | LangChain | `LANGCHAIN_API_KEY` |
| `AIza` | Google/Gemini | `GOOGLE_API_KEY` |
| `c0203d6a` | Serper | `SERPER_API_KEY` |
| format: `id.secret` | Ollama / Open WebUI | `OLLAMA_API_KEY` |

## Procedure

### 1. Parse the paste (natural language "my X key is Y" format)

The most common format is one key per line in natural language. Each line matches:

```
my <provider_name> api key is <key_value>
my <provider_name> key is <key_value>
```

Extract with simple line-by-line scanning. For each line that contains "key is" or "key:", take the text before "key" as the provider hint and the text after "is"/":" as the key value. Match provider hints against known names:

| User says | Possible env var | Notes |
|-----------|-----------------|-------|
| "opencode" | `OPENCODE_ZEN_API_KEY` or `OPENCODE_GO_API_KEY` | Usually an OpenAI-format key, NOT a DeepSeek key |
| "openrouter" | `OPENROUTER_API_KEY` | Starts with `sk-or-v1-` |
| "deepseek" | `DEEPSEEK_API_KEY` | Starts with `sk-`, 35-40 chars |
| "groq" | `GROQ_API_KEY` | Starts with `gsk_` |
| "firecrawl" | `FIRECRAWL_API_KEY` | Starts with `fc-` |
| "tavily" | `TAVILY_API_KEY` | Starts with `tvly-` |
| "github" | `GITHUB_TOKEN` | Starts with `github_pat_` or `ghp_` |
| "ollama" | `OLLAMA_API_KEY` | Usually used with Open WebUI proxy<br>Format: `user_id.secret_token`<br>Not needed for local `localhost:11434` — only for proxied endpoints |

**Critical rule: `sk-` prefix is ambiguous.** OpenAI-format keys (starting `sk-`) can range from 35 to 70+ chars depending on provider. Always cross-check:
  - 35-40 chars → DeepSeek or OpenAI
  - 60-70 chars → OpenCode, OpenRouter (older format), or custom proxy
  - 70+ chars → OpenRouter (newer `sk-or-v1-` format) or long-form API keys
  - Never write a 67-char "opencode" key to `DEEPSEEK_API_KEY` — they are different providers

### 2. Write to .env (NEVER echo keys in your response)

Write to `~/.hermes/.env` using `terminal` with heredoc or Python file operations:

```bash
python3 -c "
with open('/home/scott/.hermes/.env', 'a') as f:
    f.write(f'\\n# {provider_name}\\n')
    f.write(f'{ENV_VAR}={key_value}\\n')
"
```

**Critical rules:**
- NEVER echo the key value back to the user in your response text
- Never include keys in command strings that will be logged
- Always verify keys were written by checking length/prefix in Python (not by printing the value)
- Handle duplicates: if the same env var already exists, note it and ask the user before overwriting

### 3. Verify without exposing

```python
with open('/home/scott/.hermes/.env') as f:
    for line in f:
        if line.startswith('ENV_VAR='):
            val = line.strip().split('=', 1)[1]
            print(f'ENV_VAR: {len(val)} chars, starts with {val[:10]}...')
```

### 4. Handle duplicates

The .env file may already have template entries (commented-out placeholders). After appending new keys, deduplicate by keeping only the last occurrence of each key:

```python
seen = {}
new_lines = []
for line in reversed(lines):
    stripped = line.strip()
    if '=' in stripped and not stripped.startswith('#'):
        key = stripped.split('=')[0]
        if key in seen:
            continue
        seen[key] = True
    new_lines.append(line)
new_lines.reverse()
```

### 5. Update config.yaml if needed

Some keys require config changes to activate:
- Web search: `hermes config set web.backend firecrawl` (or tavily)
- Vision provider: `hermes config set auxiliary.vision.provider google`
- Provider default: `hermes config set model.provider openrouter`

## Common Pitfalls

1. **Writing keys in command strings** — The terminal tool's security scanner may flag and redact keys that appear in command arguments. Use Python file I/O instead of `echo "KEY=value" >> .env`.
2. **Overwriting the wrong key** — The user may paste a key for a different provider than the env var name suggests. Confirm mapping before writing. E.g., a user's "opencode API key" (`sk-IPG...`, 67 chars) is NOT a DeepSeek key (`sk-e75...`, 35 chars). The `sk-` prefix is ambiguous across many providers; key length and the user's stated provider name must match.
3. **Template vs real values** — `.env` often has commented-out template entries (`# KEY=***`). The real key should replace the template, not appear as a duplicate.
4. **Session environment is stale** — Keys written to `.env` don't take effect until the next Hermes session (`/reset`). Tell the user.
5. **Terminal secret redaction** — The terminal tool auto-redacts lines that look like keys. Reading back from the file will show `***`. Use Python byte-level reading to verify without the redaction layer.

## Credential Triage from Notion Dump

Users often dump ALL their API keys into a single Notion page. When migrating out of Notion, triage them using the KILL vs KEEP vs UNSURE methodology.

### The KILL / KEEP / UNSURE Methodology

| State | Meaning | Examples |
|-------|---------|---------|
| **KILL** | Service is dead, abandoned, or incompatible | n8n (Docker RAM conflict with training), abandoned bot tokens |
| **KEEP** | Actively used or likely needed | NVIDIA (primary), OpenRouter (backup), Groq (fallback), Firecrawl (web search) |
| **UNSURE** | Store safely, flag for review | OpenAI keys pointing at proxies, old OAuth client IDs |

### Cluster by Function

```
PRIMARY PROVIDER:    NVIDIA keys (1 main + N backups)
BACKUP PROVIDERS:    OpenRouter, Groq, DeepSeek
WEB SEARCH STACK:    Firecrawl + Serper + Tavily
EMAIL:               Resend (x2, one per domain)
CODE ACCESS:         GitHub tokens (PATs)
AUXILIARY MODELS:    Gemini, OpenAI (via proxy)
INFRASTRUCTURE:      E2B, Twingate, Neo4j, LangChain
DEAD:                n8n (Docker conflict), Clawdbot bot (migrated), WSL bridge tokens
```

### Dead Service Detection Signals

- **Resource conflict**: "n8n needs Docker but training already takes 30GB RAM" -> KILL
- **Platform migration**: "Clawdbot Telegram bot token" -> KILL (user moved to different agent)
- **Deprecated architecture**: WSL bridge tokens, ancient Docker MCP profiles -> KILL
- **Service name not recognized**: ask once, if no response mark UNSURE and store safely

### Workflow

1. Extract all keys from the Notion page (search "API's" or page list)
2. Group by provider function
3. Apply KILL / KEEP / UNSURE triage
4. Write KEEP keys to `~/.hermes/.env`
5. Write UNSURE keys as commented-out entries for review
6. Save a triage inventory file locally (never echo keys in conversation)
7. Never mention KILLed services or their people/projects unless the user brings them up

## Verification Checklist

- [ ] Each key was written to the correct env var
- [ ] No key values were echoed in conversation
- [ ] Duplicate env vars were cleaned up (last-wins dedup)
- [ ] The corresponding provider is configured in config.yaml if needed
- [ ] User was told to `/reset` for changes to take effect
