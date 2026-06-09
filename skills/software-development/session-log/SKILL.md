---
name: session-log
description: "End-of-session log + cross-session recovery via references/session-recovery.md."
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Session Log", "opencode-migrated"]
    related_skills: []
---


# Session Log

**Always invoke at session end.** Writes or appends a comprehensive session log to `SESSION_LOG.md` in the project root directory.

## Instructions

Execute these steps in order:

### 1. Gather session data

Synthesize the entire conversation to extract:

- **Session date** — today's date
- **Started with** — the user's opening request/objective for this session
- **Summary** — 3-5 bullet points of what was accomplished (focus on concrete outcomes, not process)
- **New files created** — absolute paths of any files written this session
- **Files modified** — absolute paths of any files edited this session
- **Bugs fixed** — bugs found and how they were fixed (root cause + fix)
- **Bugs discovered but NOT fixed** — bugs identified but left for later
- **Architecture decisions** — any design decisions made, with rationale
- **Commands to remember** — important CLI commands run, especially those that would need to be re-run (training launches, builds, tests)
- **Environment state** — any important state (GPU available, dataset paths, checkpoint locations)
- **Blockers** — anything blocking progress for next session
- **Next steps** — the most important 3-5 things to do next session, in priority order
- **Key numbers** — any important quantitative results (test pass counts, parameter counts, loss values, timing)

### 2. Check if SESSION_LOG.md exists

Look for `SESSION_LOG.md` in the project root directory. The project root is the workspace root passed to the agent.

If it does **not** exist, write a fresh file with this header:
```markdown
# Session Log

Automatic session-to-session reference. Each section is one session.
Last entry is most recent.

---
```

Then append the new entry.

If it **does** exist, simply append a new entry at the end.

### 3. Write the session entry

Use this EXACT format (Markdown). Append it to the file:

```markdown
## Session YYYY-MM-DD

**Duration:** ~X hours (or "ongoing")
**Objective:** <user's opening request>

### ✅ Accomplished
- <bullet>
- <bullet>

### 📁 Files Created
- `path/to/file`

### 📝 Files Modified
- `path/to/file`

### 🐛 Bugs Fixed
- **<bug description>** — root cause: <cause>, fix: <fix description>

### ⚠️ Known Issues Left Open
- <issue description> — <why not fixed>

### 🏗️ Architecture Decisions
- **Decision:** <what> — **Rationale:** <why>

### 💾 Commands to Remember
```bash
<command>
```

### 🔧 Environment
- GPU: <model>, <memory> (e.g. "Radeon 860M, 12GB")
- Dataset: <path>
- Checkpoints: <path>
- Key state: <anything else>

### 🧱 Blockers
- <blocker>
- (or "None" if no blockers)

### 👣 Next Steps
1. **<top priority>** — <details>
2. ...
3. ...

### 🔢 Key Numbers
- <metric>: <value>
```
**AGENTS.md update:** After writing the log, update the `AGENTS.md` file in the project root (if it exists) to include this as the last section under a "Session Log" heading:
```
## Session Persistence

A `SESSION_LOG.md` file is maintained in the project root. It is an append-only log
of every OpenCode session. Use it to reconstruct context when starting a new session:
- Read the last entry for "Next Steps" and "Blockers"
- Scroll back further for architecture decisions and key commands
- Look at "Environment" for current state of datasets, checkpoints, etc.

This file is maintained by the `session-log` skill at session close.
```

### 4. Also save to agentmemory

After writing the file, save the session summary to agentmemory for cross-session context retrieval:

```python
save to agentmemory:
  type: "session"
  content: <session summary (same as the markdown entry)>
  concepts: "session-log,<project-name>,<key-topic-1>,<key-topic-2>"
  files: <list of files modified/created>
```

## Output file location

The file is written to `SESSION_LOG.md` in the **project root directory** (the workspace root folder passed to the agent at session start). NOT to temp directories, NOT to hidden folders.

## Important rules

- This is **append-only**. Never rewrite existing session entries.
- Date each session with `YYYY-MM-DD`.
- Be concise but complete — the user should be able to start a new session by reading ONLY this file.
- If the project root has an `AGENTS.md` or similar project-level instructions file, update it with a brief note about the session log (as shown above).
- If session was very short (<5 exchanges with no real work), write a minimal entry: date, objective, and "No significant work this session."
- Always save to agentmemory as well so prior context is retrievable even without the file.
