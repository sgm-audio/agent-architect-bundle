# Master TODO.md Protocol

## Why

Scott has 45+ unshipped projects, ADHD, and context-switches constantly. He loses session state on API failures, network drops, and daily resets. A single `TODO.md` file in a known path is his anchor — the one thing that survives every disconnection and tells him where he left off.

## The File

**Location:** `C:\Dev\hivyr\.ETHOS\NexusPerformanceNode\TODO.md` (or project root if working in a specific repo)

**Rules:**
- One file. Not per-project. Not in `.hermes/`. One master list.
- Every session starts and ends with a scan of this file.
- Every new project/task gets added here before any code is written.
- Completed items are marked, not deleted (for retrospective tracking).

## Required Sections

### 1. Header
```
Scott's Master Project Inventory — Generated YYYY-MM-DD
First thing every session: scan this file.
Second thing: check if anything changed since last session.
```

### 2. Active Project Table

| Column | Content |
|--------|---------|
| **Project** | Name + link to repo if public |
| **Description** | One-line what it does |
| **Status** | Shipped / In Progress / Pending / Archived |
| **Repo** | GitHub URL |
| **Next Action** | Single concrete step |
| **Blocker** | What's preventing next action (or "none") |

### 3. Stats Section
- Total repos tracked
- Shipped count
- In progress count
- Archived count
- Deleted count
- Next deadlines (CERN app, etc.)

### 4. Reminder Boxes
Big visible boxes for critical deadlines:
```
⚠️ CERN APPLICATION — Deadline TOMORROW
⚠️ MAMBA3 PUSH FAILED — Retry with git config http.postBuffer
```

### 5. Footer
```
Last updated: YYYY-MM-DD
Next session: scan this file first.
```

## Session Protocol

**Start of every session:**
1. Read TODO.md
2. Check if any background processes completed (CLARA push, OpenCode builds)
3. Ask: "What are we working on today?"

**End of every session:**
1. Update TODO.md with new statuses
2. Save critical facts to memory (if space permits)
3. If the user is about to disconnect, confirm: "Everything is saved"

## Training Metrics & Code Stats

When the user asks "how do I get training metrics?" or "how many lines of code?":

### Lines of Code
```bash
# Count by extension
find /c/Dev -name "*.py" -o -name "*.rs" -o -name "*.cpp" -o -name "*.hpp" | xargs wc -l | tail -1

# Or use pygount (preferred — handles binary files)
pip install pygount
pygount /c/Dev/mamba3 --format=summary
```

### Training Metrics (ML models)
```bash
# Check TensorBoard logs
tensorboard --logdir /c/Dev/mamba3/runs --port 6006

# Read training status files
cat /c/Dev/mamba3/training_status.md  # if it exists
cat /c/Dev/mamba3/training_commands.md

# Check checkpoint directory
ls -la /c/Dev/mamba3/checkpoints/

# Parse latest training log
grep -E "(loss|accuracy|epoch|step)" /c/Dev/mamba3/logs/train_*.log | tail -20
```

### Git Stats
```bash
# Total commits in a repo
git rev-list --count HEAD

# Uncommitted changes
git status --short | wc -l

# Size of repo (including history)
git count-objects -vH | grep "size-pack"
```

## OpenCode Session Integration

When delegating to OpenCode, the prompt should include:
```
After completing the task:
1. Run any tests and report results
2. List files changed and a summary of changes
3. Save a brief changelog entry to the project root
```

This ensures OpenCode sessions produce a durable artifact even if the Hermes session resets.

## When to Update

- Project status changes
- New project discovered
- Blocker resolved
- Deadline approaches
- End of session (always)
- User explicitly asks "what's my status?"

## Scott's Specific Requirements

- The TODO.md must be in his face every session. He WILL forget it exists.
- He needs reminders. The CERN app reminder triggered every single response until he shipped it.
- Training metrics are not automatic — they require a manual check or a cron job.
- "make sure every session in opencode you use runs /endsession" — OpenCode does not have `/endsession`. The equivalent is: capture the changelog, then exit with Ctrl+C. Document the session outcome before closing.
