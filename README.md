# Agent Architect Bundle

**300+ AI agent skills, workflows, and agent definitions** for Hermes Agent and OpenCode.

Built by a solo developer across 2 years of real daily use. These aren't theoretical — they're battle-tested across audio DSP, web development, academic research, REAPER scripting, business ops, and more.

## What's Inside

### 🤖 Hermes Agent Skills (92)
Ready-to-load skills for Hermes Agent organized by category:

| Category | Count | Skills |
|---|---|---|
| Audio DSP | 28 | mamba3, JUCE, CLAP, ARA, ONNX, mixing, sound design, source separation, etc. |
| Software Dev | 20 | frontend-build, deployment-ops, CMake, prompt-engineering, design, UI/UX, etc. |
| Business | 6 | Gumroad, Canadian copyright, SR&ED, PLG loops, subscription billing, CMRRA/SOCAN |
| GitHub | 6 | PR workflow, code review, issues, repo management, auth, codebase inspection |
| Reaper ReaScripts | 3 | Lua syntax, licensing, ship pipeline |
| Academic | 3 | Full paper pipeline: research → write → review → publish |
| + more | 26 | Ollama, local LLMs, Notion, YouTube, devops, mlops, creative, etc. |

### 🧠 OpenCode Agent System (146 skills + 62 agents)
A complete multi-agent architecture with specialist roles:

- **4 Primary Squads**: plan, code-squad, analytics-squad, vision-squad
- **62 Specialist Agents**: code-writer, code-reviewer, bug-hunter, oracle, hephaestus, heavy-hitter, and more
- **6 Webdev Agents**: atlas (planner), hephaestus (builder), oracle (reviewer), prometheus (tester), momus (debugger), explore (navigator)
- **Full config**: opencode.jsonc with NVIDIA NIM + Ollama provider setup
- **Build pipeline**: CMake build automation

### 🏗️ SDK & Integrations
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

## License

Individual skills are MIT licensed unless noted otherwise in their SKILL.md.
The OpenCode agent system configuration is MIT licensed.
