# OpenCode Agent System

## Squad-First Architecture

Always route work through a **Squad Leader** (primary agent, Tab-switchable).
Squad leaders dispatch to specialist sub-agents.

### Primary Squads (Tab to cycle — 4 squads)

| Squad | Model | Purpose |
|---|---|---|
| `plan` | deepseek-v4-flash | **Read-only.** Architecture exploration, code review, requirements analysis, implementation planning |
| `code-squad` | deepseek-v4-pro | Code generation, review, debugging, architecture, testing |
| `analytics-squad` | deepseek-v4-pro | Data analysis, planning, critique, structured decisions |
| `vision-squad` | kimi-k2.6 | Image analysis, document processing, multimodal synthesis |

### Specialist Sub-agents (invoke via @name; hidden ones auto-invoke by context)

**Heavy Hitter:** `@heavy-hitter` (nemotron-3-ultra) — Nvidia NIM frontier squad for the hardest problems
**Code & Engineering:** `@code-writer` (deepseek-v4-flash), `@code-reviewer` (nemotron-3-ultra), `@bug-hunter` (nemotron-3-ultra), `@system-architect` (deepseek-v4-pro), `@test-engineer` (deepseek-v4-flash)
**Research:** `@web-researcher` (deepseek-v4-flash), `@doc-reader` (kimi-k2.6), `@knowledge-synthesizer` (deepseek-v4-pro), `@fact-verifier` (deepseek-v4-pro), `@knowledge-base` (deepseek-v4-flash), `@semantic-searcher` (deepseek-v4-flash)
**Content:** `@writer` (minimax-m2.7), `@summarizer` (deepseek-v4-flash), `@translator` (kimi-k2.6), `@editor` (minimax-m2.7), `@content-strategist` (minimax-m2.7), `@outreach-writer` (minimax-m2.7)
**Analysis:** `@data-analyst` (deepseek-v4-pro), `@logic-engine` (glm-5.1), `@planner` (deepseek-v4-pro), `@critic` (nemotron-3-ultra), `@decision-engine` (glm-5.1), `@methodology-advisor` (glm-5.1)
**Multimodal:** `@vision-analyst` (kimi-k2.6), `@embedding-engine` (deepseek-v4-flash), `@multimodal-synthesizer` (kimi-k2.6), `@media-coordinator` (deepseek-v4-flash)
**Outreach/SEO:** `@lead-scout` (deepseek-v4-flash), `@email-finder` (deepseek-v4-flash), `@web-design-concept` (minimax-m2.7), `@on-page-seo` (deepseek-v4-flash), `@technical-seo` (deepseek-v4-flash), `@content-seo` (deepseek-v4-flash), `@backlink-agent` (deepseek-v4-flash)
**ReaPack Pipeline:** `@lua-auditor` (deepseek-v4-pro), `@header-doctor` (deepseek-v4-flash), `@rt-optimizer` (deepseek-v4-flash), `@index-builder` (deepseek-v4-flash)
**Skill Eval:** `@skill-grader` (deepseek-v4-flash), `@skill-comparator` (deepseek-v4-flash), `@skill-analyzer` (deepseek-v4-flash)
**Agent Builder:** `@skillful-orchestrator` (deepseek-v4-pro), `@sam-analyst` (deepseek-v4-flash), `@jenny-engineer` (deepseek-v4-pro), `@will-reviewer` (deepseek-v4-pro), `@tom-builder` (deepseek-v4-flash)
**Hidden — auto-invoke by context:** `@heavy-hitter` (nemotron-3-ultra), `@outreach-squad` (deepseek-v4-flash), `@seo-squad` (deepseek-v4-flash), `@content-squad` (minimax-m2.7), `@reapack-prep` (deepseek-v4-pro), `@orchestrator` (deepseek-v4-flash), `@memory-manager` (deepseek-v4-flash), `@context-tracker` (deepseek-v4-flash), `@tool-dispatcher` (deepseek-v4-flash), `@state-machine` (deepseek-v4-flash)

### Webdev Specialist Agents (with full prompt definitions)

| Agent | Role | Model |
|---|---|---|
| `@atlas` | Project planner & task decomposer | deepseek-v4-pro |
| `@hephaestus` | Code generation & implementation | deepseek-v4-pro |
| `@oracle` | Code review & quality analysis | nemotron-3-ultra |
| `@prometheus` | Test generation & validation | deepseek-v4-flash |
| `@momus` | Debugging & error analysis | nemotron-3-ultra |
| `@explore` | Fast file exploration & navigation | deepseek-v4-flash |

### Model Strategy

| Model | Use For |
|---|---|
| `deepseek-v4-pro` (Nvidia NIM) | Heavy reasoning: architecture, planning, data analysis, engineering, agent building |
| `deepseek-v4-flash` (Nvidia NIM) | **Default model.** Speed: code writing, research, outreach, SEO, testing, exploration, orchestration |
| `nemotron-3-ultra` (Nvidia NIM) | Frontier reasoning: code review, bug hunting, quality analysis, critique, heavy-hitter squad |
| `kimi-k2.6` (Nvidia NIM) | Vision/multimodal, documents, translation, image analysis |
| `minimax-m2.7` (Nvidia NIM) | Creative: writing, editing, content strategy, outreach copy, design concepts |
| `glm-5.1` (Nvidia NIM) | Specialized: logic, methodology, formal reasoning |
| `opencode/big-pickle` | Free tier — lightweight exploration |
| `opencode/gpt-5-nano` | Free tier — quick research |
| `ollama/gemma-3-4b-it-q4` | Lightweight local: knowledge base, tool dispatch, state management |

## Web Development Skills

4 skills loaded from `~/.config/opencode/skills/`:

| Skill | Purpose |
|---|---|
| `website-design` | Design systems, UI/UX, color palettes, typography, responsive layouts |
| `frontend-build` | Next.js, React, TypeScript, Tailwind, shadcn/ui, component patterns |
| `deployment-ops` | Vercel/Netlify deployment, CI/CD, domains, DNS, monitoring |
| `client-handoff` | Documentation, training, maintenance plans, deliverables |

Invoke by asking for the skill by name or describing a matching task.

## Webdev Workflow

```
Phase 1: @atlas plan [project brief]     -> task breakdown, tech stack
Phase 2: @hephaestus build [components]  -> implementation
Phase 3: @oracle review [changes]        -> code review
Phase 4: @prometheus test [features]     -> test suite
Phase 5: @momus debug [issue]            -> root cause fix
```

Always: @oracle review before merge. @prometheus test before deploy.

## Commands

- `/recall` -- Search agentmemory for session history and lessons
- `/remember` -- Save information to agentmemory for future recall
- `/briefing` -- Create/update global session briefing
- `/changelog` -- Show full session changelog
- `/endsession` -- Finalize session, compile summary, update briefing
- `/build` -- LangGraph DAG: cmake configure -> compile -> validate -> test -> sign -> package
- `/reapack-prep` -- Run ReaPack shipping pipeline

## Tool Integrations

- **context7**: External library docs
- **playwright**: E2E browser tests
- **puppeteer**: Browser automation, screenshots, visual testing
- **github**: PRs, issues, code search
- **agentmemory**: Session memory persistence
- **superpowers**: 14 engineering workflow skills (MCP stdio server)

## Parallel Work

- Use `task` tool to dispatch multiple sub-agents in parallel
- Squads handle sequential dependencies internally
- For independent analysis tasks, dispatch to specialists in parallel

---

# mamba3 -- CLAP / VST3 / ARA Development

## Build System

```bash
cmake -B build -G "Visual Studio 17 2022" -DCMAKE_C_COMPILER=clang-cl -DCMAKE_CXX_COMPILER=clang-cl
cmake --build build --config Release
```

## Code Quality

Format with clang-format:
```bash
cmake --build build --target clang-format
```

Lint with clang-tidy:
```bash
cmake --build build --target clang-tidy
```

Or run directly on all sources:
```bash
run-clang-tidy -p build -header-filter="src/*" src/
```

## Type Checking

Static analysis with clang:
```bash
clang-cl /analyze src/*.cpp /I include /std:c++20
```

## Testing

```bash
cmake --build build --target check
ctest --test-dir build --output-on-failure
```

## Audio-Specific Checks

Check for real-time unsafe calls:
```bash
rg "malloc|free|new|delete|mutex\.lock|sleep|printf" src/ --include "*.cpp" --include "*.h"
```
