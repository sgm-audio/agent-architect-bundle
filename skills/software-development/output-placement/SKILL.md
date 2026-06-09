---
name: output-placement
description: ""IRON RULE skill. All user-facing documents, papers, reports, builds, deliverables, and generated files MUST be written to the project root directory or a user-specified path. NEVER use temp directories (%TEMP%, /tmp, etc.) for user-facing output.""
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Output Placement", "opencode-migrated"]
    related_skills: []
---


# Output Placement (IRON RULE)

## The Rule

**Any file generated for the user — documents, papers, builds, exports, reports, scripts — MUST be placed in one of:**

1. **The project root** (the directory the user is working in)
2. **A user-specified path** (the user tells you exactly where)
3. **A documented subdirectory of the project root** (e.g., `docs/`, `dist/`, `output/`)

## Banned Locations

The following are **never acceptable** for user-facing output:

- `%TEMP%`, `/tmp`, `/var/tmp`, or any temp directory
- `C:\Windows\System32` or any system directory
- The opencode temp workspace directory
- Any path the user would not naturally find

## Determining the Correct Path

1. If the user is in a project directory with a `AGENTS.md`, `README.md`, or version control — use that directory as root.

2. If the user is NOT in a project directory (e.g., working directory is `C:\Windows\System32` or similar), ASK them where they want the output before writing anything.

3. If the user specifies a path, use it exactly. Do not second-guess.

4. If unsure, ask. Never guess.

## Enforcement

When generating any file:

```
1. CHECK: Is there an active project directory? (AGENTS.md, .git, README.md present?)
   YES → write output there (or to {project_root}/output/)
   NO  → ask user where to put it

2. VERIFY: The path is NOT in any temp/system directory
   VIOLATION → stop, move file to correct location, apologize
   PASS → proceed
```
