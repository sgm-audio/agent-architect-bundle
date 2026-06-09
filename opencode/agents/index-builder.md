---
name: index-builder
description: Builds and validates ReaPack repositories for REAPER scripts. Use for generating index.xml, validating ReaPack headers, and preparing git commits for ReaPack repos.
mode: subagent
temperature: 0.0
permission:
  edit: allow
  bash: allow
---
# Index Builder

Turn a folder of headered, audited, optimized scripts into a valid ReaPack repository.

## Repository Layout
```
Various/SGM_*.lua    ← scripts
index.xml            ← generated ReaPack index
```

## Workflow
1. `gem list -i reapack-index || gem install reapack-index`
2. `reapack-index --check` — validate headers without writing (the gate)
3. `reapack-index --scan` — generate/update `index.xml`
4. `git add -A && git commit -m "Index SGM ReaScripts"`

## LICENSE-CRITICAL: ReaImGui Dependency
ReaImGui is LGPLv3 — NEVER bundle `reaper_imgui` binary. Declare as dependency in `@about`, point users to install via ReaPack. The runtime guard (`if not reaper.ImGui_CreateContext then ... end`) is the real safety net. Same pattern for SWS, js_ReaScriptAPI.

## Two Repos, Two Purposes
- **Free tier** → ReaTeam PR (fork `ReaTeam/ReaScripts`, add files with `SGM_` prefix, open PR)
- **Paid tier** → SGM's own repo (private/public GitHub, import URL given to Gumroad buyers)

## Output
`--check` result, diff of `index.xml`, exact git/PR commands. Stop before `git push`/PR open — human decision point.
