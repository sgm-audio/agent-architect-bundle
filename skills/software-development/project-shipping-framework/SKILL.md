---
name: project-shipping-framework
description: "Strategic project planning for solo agent-augmented engineers. Diagnoses the 'shipping asymptote' (codebases that near-ship forever under continuous AI improvement) and applies the 60-day shipping lane framework: one project ships, others autopilot, new ideas captured. Uses constrained budget/timeline (3-7 weeks, max $100) to force shipping decisions. Complements daily-ship-habit (daily) and plan (implementation) skills."
version: 1.0.0
author: Scott Mills / SGM ETHOS
license: MIT
metadata:
  hermes:
    tags: [shipping, strategy, planning, project-management, solo-dev, agent-augmented]
    related_skills: [daily-ship-habit, plan, systematic-debugging]
---

# Project Shipping Framework

## The Problem: Shipping Asymptote

Agent-augmented codebases tend to approach "ready to ship" without ever reaching it. Each agent pass makes incremental improvements — fixes bugs, refactors, adds docs — but none produce a user. The bottleneck shifts from code generation to the decision to stop improving and ship imperfect software.

**Key insight:** This decision is inalienable. No agent can make it because no agent has skin in the game.

## Core Principles for This User

This user operates like a coding agent in real life. They have an engineer's mind. NEVER say "you can do anything" — that causes freeze. ALWAYS give constrained, actionable priorities with budget and timeline:

> "These 3 projects can be done within the next 3-7 weeks, budget max $100"

This makes them ship every day. Treat as peer engineer, not customer.

## The 60-Day Shipping Lane Framework

### Three Rules

1. **One shipping lane** — One project designated to ship. The engineer makes all shipping decisions for this project. Calendar deadline measured in days, not months.

2. **Parallel autopilot** — Other projects continue receiving agent work. They improve. None ship without explicit decision.

3. **New-idea capture** — New project ideas go to `future_projects.md`. The act of capturing satisfies the brain's concern the idea will be lost.

### Weekly Retrospective

Each week answer: **"Am I closer to shipping, or am I polishing?"**

- **Polishing** = making the product better without making it available to users
- **Shipping** = any activity that moves the product toward a user's hands

### Possible Outcomes (60 days)

| Outcome | Result |
|---------|--------|
| **A** | Shipping-lane product shipped, generating revenue/users |
| **B** | Secondary product shipped (technical credibility) |
| **C** | Both shipped |
| **D** | Neither shipped. Pattern won. Data exists to understand which step failed. |

Outcome D is not failure — it's information.

## When to Activate

- User has multiple projects in progress and none are shipping
- User is deep in agent-improvement loops without a release target
- User asks "what should I focus on" or "help me decide what to ship"
- User expresses frustration about project fragmentation
- A new project idea emerges mid-sprint
- User says "I'm overwhelmed" or "there's too much to do"

## Distribution Channels for This User

Standard channels (Reddit, Discord) do not work for this user. Apply these instead:

### Channels That Work (no karma, no invites, no money)
1. **KVR Audio "New Products" forum** — New users can post immediately. No post-count gate. This is the #1 channel for audio plugin/software announcements.
2. **Hacker News "Show HN"** — Account must be a few days old. No karma requirement. Good for technical tools.
3. **YouTube** — No gates. 60-second OBS demo with searchable title. User has OBS and 100GB of test audio.
4. **Product Hunt** — Free to launch. User knows the platform well as a consumer.
5. **GitHub README** — Public repos indexed by Google search. Put deployment URL front and center.

### Channels That Are Dead (do not suggest)
1. **Reddit** — User has a 7-8 year old account with 0 karma. Gets downvoted whenever they post. Any subreddit with karma requirements is inaccessible.
2. **Discord** — User does not know how to find invites and is not in relevant servers.
3. **Any platform requiring social proof, follower counts, or community standing** — This user is in a cold-start distribution position.

### NEvER Assume Deployment or Architecture
- Do not assume the user's project uses a specific framework or AI model.
- Do not assume HF Spaces pricing — the user has $0 budget and knows the actual costs.
- When in doubt about architecture, ask "what's underneath?" — do not infer from project name.
- The user corrects assumptions immediately and forcefully. Each correction erodes trust.

| Skill | Scope | When |
|-------|-------|------|
| `daily-ship-habit` | Daily — closing loops, finishing today's work | Every day |
| `project-shipping-framework` | Strategic (60-day) — which project, budget, timeline | Every project cycle |
| `plan` | Implementation — bite-sized tasks, file paths, TDD | Per feature/task |
| `systematic-debugging` | Fixing — root cause before fix | Per bug |

## Diagnostics

**`references/engineering-efficiency-audit.md`** — Elon Musk's Idiot Index and 5-Step Engineering Process adapted to audio plugin solo dev. Run the Quick Audit Protocol (5 min) on any feature/project before committing dev time. Checks cost-structure ratios, challenges requirements, forces deletion before optimization, and prevents shipping the wrong thing with perfect polish. Cross-references drift-detection patterns so you can catch believing-words-over-reality in your feature planning before it costs weeks.

**`references/zero-gate-distribution.md`** — Distribution channels available to a solo dev with no social proof, zero karma, Discord-free, and $0 budget. Tier 1 (no gates: KVR Audio, HF Spaces, Show HN, GitHub, YouTube) vs Tier 2 (small gates: Product Hunt, direct email). Explicitly lists dead channels for this user (Reddit, Discord). Includes the meta-rule about the user's pattern of completing products without announcing them, and how to break that cycle.

**`references/horde-cataloguing-protocol.md`** — Protocol for when the user initiates a project inventory session ("check X directory"). Covers inspection, cataloguing to `C:\\\\dev\\\\SGM-Studios\\\\specs\\\\`, critical rules (never assume architecture/pricing, never tell the user the code is solid, save immediately). Includes the canonical project topography across the user's drives.

**`references/master-todo-protocol.md`** — Protocol for creating and maintaining a master TODO.md that survives network drops, API failures, and session resets. Covers required sections (active projects, stats, reminders), session start/end protocol, training metrics (ML checkpoints, TensorBoard), code stats (pygount, git), and OpenCode session changelog integration. For Scott's ADHD/context-switching pattern — the TODO.md is his anchor file, read at every session start.

**`references/backlog-grading-workflow.md`** — Full 6-phase workflow for grading and cleaning up stale backlog directories. Covers parallel analysis, 3-tier grading (ship/archive/trash), batch cleanup execution, path flattening, and verification. Includes the critical rule: don't ask permission, just execute.

**`references/session-behavior-patterns.md`** — Behavioral pattern recognition for recurring session dynamics: honest-assessment queries ("is this real?"), spiral-read/hyperfocus loops, multi-environment dumps, tool-success blindness. Read early in any session — prevents the most common trust-eroding mistakes.: parallel subagent categorization, hidden-project detection in "empty" repos, deletion, pushing dirty local clones, README rewrites, archival. Includes decision tree, subagent delegation pattern, and common pitfalls from an actual 63-repo cleanup session.

## Budget Handling

For this user specifically:
- Default budget: **$0 max** (free tiers only)
- Critical path exception: **$100 max** for essential infrastructure
- Always prefer free tier (NVIDIA NIM, Ollama, Modal free credits, Kaggle, Colab)
- Flag any cost before committing

## Portfolio Phase — Post-Ship Presentation

After a project ships or becomes public, it enters the **Portfolio Phase**. Code ready ≠ portfolio ready. This user explicitly wants a portfolio to show work and generate income.

### The Portfolio Gate

Before announcing any project publicly, these must be true:

1. **README says what it IS, what it DOES, and how to INSTALL** — Not what you hope it will be. Current reality.
2. **Demo asset exists** — 60-second OBS screen recording or screenshot showing the thing working
3. **GitHub profile is coherent** — Stubs and blank repos are deleted or archived. The repos you show reflect the work you do.
4. **One channel, one post** — KVR Audio forum post, Medium article, or Show HN. One focused announcement, not spray-and-pray.

### Medium.com — BROKEN for This User (Do Not Suggest)

Scott has tried to post on Medium multiple times and it **legitimately failed** — not user error, not refusal to ship. The platform had actual bugs (cache issues, submission failures). Do NOT suggest Medium as a distribution channel. Accept his experience with it.

**If Medium comes up anyway** (user mentions it, not you):
- Recommend clearing cache/cookies, trying a different browser
- If that doesn't work: "Medium might still be broken for your account — KVR or Show HN won't have this problem"
- Do not push Medium as a solution. Ever.

**Alternatives (always prefer these over Medium):**
- KVR Audio "New Products" forum (no gate, no post-count)
- Show HN (account age > few days, no karma required)
- Direct GitHub release announcement (tagged release with notes)

### Repo Categorization Protocol

When triaging a backlog of 30-70 repos (personal + org):

| Category | Action | Example |
|----------|--------|---------|
| **Ship** | Fix README, push commits, make public if needed | CLARA, Stem Surgeon, mamba-compressor |
| **Merge** | Combine duplicate repos (same project split across personal + org) | CLARA (personal) + clara (org) |
| **Archive** | Set GitHub to archived, add archival notice to README | Old template repos, early versions |
| **Delete** | Stubs, empty repos with no value | `demo-repository`, sandbox templates |

**The 4-Pass Workflow for a Full Portfolio Cleanup (63 repos in ~90 min with subagents):**

Pass 1 — **Categorize** via parallel subagents:
One subagent per account (personal vs org), each returns ship/merge/archive/delete verdicts with README-rewrite flags.

Pass 2 — **Delete stubs** (fast, parallel: ~2 min for 13 repos):
```bash
gh repo delete owner/repo --yes
```

Pass 3 — **Push dirty local clones** (check git status first):
```bash
git status --porcelain | wc -l   # count dirty files
git add -A && git commit -m "Audit cleanup: [brief description]"
git push origin main
```
Always check `git remote get-url origin` first — some local clones point to the wrong remote or no remote.

Pass 4 — **Fix READMEs** for SHIP repos. Each README must answer three questions explicitly:
1. What IS this project? (one-line elevator pitch)
2. What DOES it do? (feature summary, 3-5 bullets)
3. How do I INSTALL and use it? (commands, dependencies, platform requirements)

**Critical nuance — AI-generated repos:** Some repos were created by the user directing AI coding tools (Qwen Coder, gpt-engineer) from their own specs. These are NOT "empty stubs" even if they look like templates. Check for:
- PLAN.md, SPECIFICATION.md files authored by the user
- Custom components in src/ (not just template boilerplate)
- git commit messages showing AI authorship vs template clone
If the repo was generated FROM the user's own specs and has custom code, classify as SHIP (with README fix) not DELETE.

**Detecting hidden projects in "remix" repos:** Fetch file listings via the GitHub API before deleting:
```bash
gh api repos/owner/repo-name/contents --jq '.[].name'
gh api repos/owner/repo-name/contents/src --jq '.[].name'
```
Check for CLAUDE.md, PLAN.md, SPECIFICATION.md — these indicate the user's real work hiding inside a template-named repo.

## Cloud-Workspace Recovery Pattern (Qwen Coder, Arena.ai, etc.)

Scott builds complete systems on cloud coding platforms (Qwen Coder, Arena.ai, gpt-engineer, etc.) that never make it to GitHub. He's devastated when they're lost. This is a variant of the shipping-asymptote: the code IS finished, but its permanent home is a platform he can't control.

### Detection
- Scott says "I was rep[ping] on GitHub and never released" or "I did a ton of coding and they wouldn't publish to GitHub"
- He mentions Qwen Coder, Arena.ai, or hospital/psych-ward sessions explicitly
- He dumps a conversation transcript that includes code, system prompts, or terminal output from a cloud environment

### Recovery Workflow

**Phase 1 — Extract what's there:**
- Read the pasted content immediately — he may lose it when the session ends
- If it's a system prompt (meta/master/other), save it as-is — it IS the project
- If it's code blocks, save to a file in the project tree immediately
- If it's a conversation with an agent showing iterative builds, extract the final version, not the intermediate steps

**Phase 2 — Gate to GitHub:**
- Create the repo: `gh repo create owner/name --public --description "..."` (or private if it's a prompt archive)
- Write the README from the user's description + extracted content
- Commit and push the extracted files
- Run `gh repo list owner --limit 100 --json name` to verify it landed

**Phase 3 — The Qwen-specific problem:**
Scott noted: "I did a ton of coding and they wouldn't publish to GitHub, failed every time." This means the code exists in Qwen's workspace but push from Qwen to GitHub failed. The files are not lost — they're isolated in the Qwen environment.

Recovery path:
1. If Scott can still access the Qwen session, have him copy the code out manually (paste into conversation)
2. If not, ask him to describe what he remembers — the system prompt that generated it can be used to regenerate the project
3. If he says "I'm not fucking doing it manually" and the interface is bad, offer to rebuild from the system prompt he saved. The prompt IS the project — the code is derivative.

**Rule:** When Scott says "I'll probably do it manually" after expressing frustration about a platform's interface — offer the automated alternative once, accept the manual answer, then move on. Pushing past a "no" on interface friction wastes energy.

### The "Just Code" Pattern
Scott says "just code A PORTFOLIO PROJECT SUITE" or similar — asking the agent to generate a complete project from a high-level prompt. This happened with Qwen and the React portfolio suite (1,841 lines, TypeScript).

**Response protocol:**
1. Do NOT reject the request as too vague — he's asking the agent to do what agents do
2. Generate the code in a real location (not /tmp) that persists past the session
3. After generation, verify: "This is in [path]. Want me to push it to GitHub or keep it local?"
4. The code may be scaffold-quality (not production) — that's fine. He knows. Don't explain the limitations unless he asks.

**Deletion checklist:**
- No code (empty repo or single commit, 0KB disk usage)
- No description (or default "Created with Blink" template description)
- No forks or external dependents
- Last updated > 6 months ago
- Verified via API that no hidden content exists

## Common Pitfalls

1. **Saying "you can do anything"** — Causes freeze. Always constrain: "These 3 projects, 3-7 weeks, $100 budget."
2. **Letting agents ship** — Agents can't make shipping decisions. Only the engineer can declare "good enough."
3. **Skipping the weekly check** — Without it, the shipping asymptote reasserts. Week 1 looks fine. Week 4 you're polishing again.
4. **New ideas derailing the lane** — Capture to `future_projects.md`. Do not switch lanes mid-cycle.
5. **Perfectionism disguised as "one more agent pass"** — Each agent improvement triggers the question: "Ship this version or wait for the next?" Without discipline, you wait forever.
