---
name: engineering-efficiency-triage
description: "Elon Musk 5-question engineering framework (Idiot Index + delete-first) adapted for solo audio/DSP plugin development. Use when the user mentions multiple projects, scope uncertainty, hesitation about what to work on, or any sense of being pulled in directions they didn't choose."
version: 1.0.0
author: assistant
license: MIT
---

# Engineering Efficiency Triage

Periodically apply Musk's 5-step engineering framework to the user's project portfolio. The goal is cutting waste and focusing on what actually ships.

## The Two Core Concepts

### 1. The Idiot Index

```
Idiot Index = Total cost of a part / Raw material cost
```

For a solo dev: **total time invested / minimum viable time to deliver value.**

If the ratio is > 10, question whether the project should exist. If it's > 50, it should probably be killed or rebuilt from scratch.

### 2. The 5 Questions (in order, never skip steps)

1. **Make the requirements less dumb.** Every requirement came from someone, not from physics. Question it. "Why does it need 5 stems?" "Why does it need ARA?" "Why does it need to run on macOS?"

2. **Delete the part/step/process.** If you don't add back at least 10% of what you deleted, you didn't delete enough. **This is the most important step.**

3. **Simplify and optimize.** Only AFTER step 2. Optimizing deleted work is waste.

4. **Accelerate cycle time.** Speed up what remains.

5. **Automate.** Do this LAST. Don't automate something you should have deleted.

## When to Activate

Load this skill and ask Idiot Index questions when any of these fire:

- User mentions feeling overwhelmed by project scope
- User talks about "should build" vs "want to build"
- User mentions a project that's been in progress for months without shipping
- User lists 3+ active projects
- User expresses frustration about not shipping
- User archives/sidelined projects and I want to reinforce the decision
- The "Building What AI Tells You To Build" drift pattern fires (see drift-detection skill)

## Framework Adapted for Audio Plugin Dev

### Question Requirements for Plugins
- "Does this plugin really need ARA, or is CLAP enough?"
- "Does it need 5 stems or would 3 cover 90%?"
- "Does it need a GUI or can it ship headless with params?"
- "Does the model need 50M params or would 10M work?"

### Delete First for Projects
- Which feature in the backlog has no user asking for it? Delete.
- Which plugin variant exists because "it should exist" not because anyone wants it?
- Which export format (VST3, AU, AAX) can you drop until someone asks for it?

### The Distribution Bottleneck
The user can build and ship code reliably but has no community standing (no Discord invites, no subreddit karma). See `references/distribution-channels.md` for no-account-required distribution paths.

## Pitfalls

- **Don't optimize performance of code that shouldn't exist.** SIMD-optimizing the wrong algorithm is worse than slow on the right one.
- **Don't ask all 5 questions at once.** Start with Step 1 (question requirements). Only move to Step 2 after the requirement is actually in doubt.
- **"Testing it yourself is not shipping"** — the user has called this out. Testing is validation. Shipping means another human uses it.
- **"I shipped that already"** — the user may have shipped something without public evidence (private repo, old account, etc.). Accept the claim; don't demand public proof.
- **The "stems baggage"** — the user built Tab Agent and Stem Surgeon because AI tools/environment shouted "stems" at them, not because they wanted to. Check whether a project started from internal desire or external noise. For deeper root cause analysis of this pattern (the 17-year wound with Adam's band), see `drift-detection` skill's "Building What AI Tells You To Build" section.

## Backlog Triage — The SHIP/ARCHIVE/TRASH Protocol

When confronted with a directory full of unknown projects and files, use this systematic 4-phase protocol. It's a concrete implementation of Step 2 (Delete First).

### Phase 1: Inventory
- Get recursive listing with human-readable sizes (`find ... -exec ls -lh {} \; | sort -k 5 -rh`)
- Count files by extension to understand what you're dealing with (`find ... -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn`)
- Identify subdirectories that are caches/venvs/node_modules/__pycache__ — mentally exclude these

### Phase 2: Classify
- **Large root-level files** (>20KB): sample first 10-20 lines to determine content type (AI session log, architecture doc, code file, system prompt, binary)
- **Subdirectories**: for each, list key files (excluding caches), read README if exists, check for status markers (PRD, ADR, test files, CI config)
- Identify: language, completeness (prototype/alpha/beta/production), what it actually does

### Phase 3: Grade
Use 3 buckets:

| Grade | Criteria | Action |
|-------|----------|--------|
| **SHIP** | Actively useful code, papers, tools aligned with current goals. Has evidence of working (test output, shipped artifacts, real data). | Move to C:\dev\ organized by project |
| **ARCHIVE** | Valuable reference but not actively needed. Includes raw AI session logs (big tool-call dumps), architecture docs for superseded approaches, system prompts that were already consumed. | Compress to tar.gz, cold storage |
| **TRASH** | No unique value. Duplicates (same content different agent session), stale leads/output (older than 60 days), binaries (.pyc .exe .pyd), cache dirs (venv node_modules __pycache__), generic checklists, PNGs with no context. | DELETE |

### Phase 4: Execute
1. **TRASH first** — delete all trash files and projects, clear caches
2. **SHIP** — move to C:\dev\ in organized structure
3. **ARCHIVE** — tar.gz each project, store in C:\archive\ or external drive
4. **Done** — the original directory becomes clean or is itself archived

### Pitfalls
- **Don't delete tools the user actively uses**. Check memory and user profile first. The user called out: Notion, HuggingFace, GitHub, specific CLI tools. When in doubt, ASK before trashing a tool/project skill.
- **AI session logs are almost always TRASH** — they document work that's already done. The artifact (refactored code, built tool) is on disk. The tool-call record is noise.
- **Massive system prompts (>100KB) are usually duplicative** — the same XML persona format gets generated by different sessions. Keep one representative reference, trash the rest.
- **Timestamps matter** — files dated within a 12-minute window (e.g. "Jun 8 09:12-09:24") are batch-generated and likely low-value.
- **Misleading filenames** are common — "Nextjs App Router UI Components" might start with Python REAPER code. Always sample the first lines before classifying.

## Related Skills

- `drift-detection` — pattern markers for when the user is drifting into unproductive work
- `daily-ship-habit` — complementary daily habit framework
- `project-shipping-framework` — 60-day shipping lane framework for solo devs

## Supporting Files

- `references/distribution-channels.md` — no-account-required distribution paths
- `references/cron-morning-kickoff.md` — template for scheduling a 4-task shipping day via cron
