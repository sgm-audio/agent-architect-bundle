# Agent Architect Bundle

The agent skills and agent definitions I use day to day with Hermes Agent and OpenCode: 92 Hermes skills, 199 `SKILL.md` files under `opencode/` (146 top-level skill folders) and 62 OpenCode agent definitions. That's 291 `SKILL.md` files in total. Some of them are third-party; see [Third-party content](#third-party-content).

I built most of these over two years of my own work in audio DSP, web dev, research, REAPER scripting and running a small business. They're tuned to how I work, so expect to edit them.

## What's inside

### Hermes Agent skills (92)

Counted by `SKILL.md` files under `skills/`:

| Category | Count | Examples |
|---|---|---|
| Audio DSP | 28 | mamba3, JUCE, CLAP, ARA, ONNX, mixing, sound design, source separation |
| Software development | 27 | frontend-build, deployment-ops, CMake, prompt engineering, UI/UX |
| MLOps | 8 | evaluation, Hugging Face Hub, inference, models |
| Business | 7 | Gumroad, Canadian copyright, SR&ED, subscription billing, CMRRA/SOCAN |
| GitHub | 6 | PR workflow, code review, issues, repo management |
| REAPER ReaScripts | 3 | Lua syntax, licensing, ship pipeline |
| Academic (in `hardware/`) | 3 | academic paper, paper reviewer, paper pipeline |
| Other | 10 | devops, Hermes, research, media, creative, productivity |

### OpenCode agent system (146 skill folders, 62 agents)

A multi-agent setup with specialist roles:

- **4 Primary Squads**: plan, code-squad, analytics-squad, vision-squad
- **62 Specialist Agents**: code-writer, code-reviewer, bug-hunter, oracle, hephaestus, heavy-hitter, and more
- **6 Webdev Agents**: atlas (planner), hephaestus (builder), oracle (reviewer), prometheus (tester), momus (debugger), explore (navigator)
- **Config**: opencode.jsonc with NVIDIA NIM + Ollama provider setup
- **Build pipeline**: CMake build automation

### Integrations
- LangGraph/AutoGen multi-agent orchestration
- NVIDIA NIM, Ollama, and local model support
- GitHub MCP, Playwright, Puppeteer, context7
- AgentMemory persistence

## Quick Start

### Hermes Agent
```bash
# Add as a tap repository
hermes skills tap add scottmills306/agent-architect-bundle

# Browse available skills
hermes skills browse

# Install specific skills
hermes skills install audio-dsp/mamba3-dsp-methodology
```

### OpenCode
Copy the `opencode/` directory to `~/.config/opencode/`:
```bash
cp -r opencode/* ~/.config/opencode/
```

Or cherry-pick individual agents:
```bash
cp opencode/agents/code-reviewer.md ~/.config/opencode/agents/
cp opencode/agents/plan.md ~/.config/opencode/agents/
```

## Requirements

- **Hermes Agent**: v0.x+ ([install](https://hermes-agent.nousresearch.com))
- **OpenCode**: Latest version ([install](https://opencode.ai))
- **Optional**: Ollama for local inference, NVIDIA NIM API key for cloud models

## Licence

My own work here is MIT. See [LICENSE](LICENSE).

## Third-party content

Some folders are other people's work, and their own licence applies:

- `opencode/skills/opencode-skillful/`: MIT, zenobi.us
- `opencode/skills/skillful-agent-system-builder/`: MIT, houarnu166. Its `context/skills_ref/` folder is a copy of Anthropic's example skills. Most of those are Apache-2.0, but `docx`, `pdf`, `pptx` and `xlsx` are © Anthropic, all rights reserved (see each `LICENSE.txt`).
- `opencode/agents/skillful/skillful/` (`mcp-builder`, `skill-creator`): Anthropic, see each `LICENSE.txt`
- `opencode/skills/ui-ux-pro-max-skill/`: MIT, Next Level Builder
- `skills/creative/humanizer/`: MIT, Siqi Chen
- Skills marked `author: Orchestra Research`, `Hugging Face` or "adapted from obra/superpowers" come from those projects.
