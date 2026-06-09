---
name: retro
version: 2.0.0
description: >
  Use this skill for weekly engineering retrospective. Analyzes commit history, work patterns, and code quality metrics with persistent history and trend tracking. Team-aware: breaks down per-person contributions with praise and growth areas. Designed for a senior IC/CTO-level builder.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Question
---

# Retro — Weekly Engineering Retrospective

Generates a comprehensive engineering retrospective analyzing commit history, work patterns, and code quality metrics. Team-aware: identifies the user running the command, then analyzes every contributor with per-person praise and growth opportunities.

## Arguments

- `/retro` — default: last 7 days
- `/retro 24h` — last 24 hours
- `/retro 14d` — last 14 days
- `/retro 30d` — last 30 days
- `/retro compare` — compare current window vs prior same-length window
- `/retro compare 14d` — compare with explicit window

## Instructions

Parse the argument to determine the time window. Default to 7 days if no argument given. Use `--since="N days ago"` for git log queries.

**Argument validation:** If the argument doesn't match a valid pattern, show usage and stop.

### Step 1: Gather Raw Data

First, fetch origin and identify the current user:
```bash
git fetch origin main --quiet
git config user.name
git config user.email
```

The name returned by `git config user.name` is **"you"** — the person reading this retro. All other authors are teammates.

Run ALL of these git commands:

```bash
# 1. All commits in window with timestamps, subject, hash, author, files changed
git log origin/main --since="<window>" --format="%H|%aN|%ae|%ai|%s" --shortstat

# 2. Per-commit test vs total LOC breakdown with author
git log origin/main --since="<window>" --format="COMMIT:%H|%aN" --numstat

# 3. Commit timestamps for session detection and hourly distribution
TZ=America/Los_Angeles git log origin/main --since="<window>" --format="%at|%aN|%ai|%s" | sort -n

# 4. Files most frequently changed (hotspot analysis)
git log origin/main --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn

# 5. PR numbers from commit messages (extract #NNN patterns)
git log origin/main --since="<window>" --format="%s" | grep -oE '#[0-9]+' || echo "No PR numbers found"

# 6. Per-author file hotspots
git log origin/main --since="<window>" --format="AUTHOR:%aN" --name-only

# 7. Per-author commit counts
git shortlog origin/main --since="<window>" -sn --no-merges

# 8. TODOS.md backlog (if available)
cat TODOS.md 2>/dev/null || echo "No TODOS.md found"
```

### Step 2: Compute Metrics

Calculate and present these metrics in a summary table:

| Metric | Value |
|--------|-------|
| Commits to main | N |
| Contributors | N |
| PRs merged | N |
| Total insertions | N |
| Total deletions | N |
| Net LOC added | N |
| Test LOC (insertions) | N |
| Test LOC ratio | N% |
| Version range | vX.Y.Z → vX.Y.Z |
| Active days | N |
| Detected sessions | N |

Then show a **per-author leaderboard** immediately below:

```
Contributor         Commits   +/-          Top area
You (name)              32   +2400/-300   src/
alice                    12   +800/-150    services/
bob                       3   +120/-40     tests/
```

Sort by commits descending. The current user always appears first, labeled "You (name)".

**Backlog Health (if TODOS.md exists):**
- Total open TODOs (exclude `## Completed`)
- P0/P1 count (critical items)
- P2 count (important items)
- Items completed this period
- Items added this period

### Step 3: Commit Time Distribution

Show hourly histogram using bar chart:

```
Hour  Commits
 00:    4      ████
 07:    5      █████
 ...
```

Call out peak hours, dead zones, bimodal vs continuous patterns, late-night coding.

### Step 4: Work Session Detection

Detect sessions using **45-minute gap** threshold between consecutive commits.

Classify sessions:
- **Deep sessions** (50+ min)
- **Medium sessions** (20-50 min)
- **Micro sessions** (<20 min)

Calculate total active coding time, average session length, LOC per hour.

### Step 5: Commit Type Breakdown

Categorize by conventional commit prefix (feat/fix/refactor/test/chore/docs). Show as percentage bar.

Flag if fix ratio exceeds 50% — signals "ship fast, fix fast" pattern.

### Step 6: Hotspot Analysis

Show top 10 most-changed files. Flag files changed 5+ times (churn hotspots).

### Step 7: PR Size Distribution

From commit diffs, estimate PR sizes:
- **Small** (<100 LOC)
- **Medium** (100-500 LOC)
- **Large** (500-1500 LOC)
- **XL** (1500+ LOC) — flag these

### Step 8: Focus Score + Ship of the Period

**Focus score:** Percentage of commits touching the single most-changed top-level directory. Higher score = deeper focused work.

**Ship of the period:** Auto-identify the single highest-LOC change in the window. Highlight PR number, title, LOC changed, why it matters.

### Step 9: Team Member Analysis

For each contributor (including the current user), compute:
1. Commits and LOC
2. Areas of focus (top 3 directories)
3. Commit type mix
4. Session patterns and peak hours
5. Test discipline (personal test LOC ratio)
6. Biggest ship

**For the current user ("You"):** Deepest treatment — session analysis, time patterns, focus score. Frame in first person.

**For each teammate:** Write 2-3 sentences on their work and patterns. Then:
- **Praise** (1-2 specific things anchored in actual commits)
- **Opportunity for growth** (1 specific, constructive suggestion)

**If only one contributor (solo repo):** Skip the team breakdown.

**If there are Co-Authored-By trailers:** Parse and credit co-authors. Note AI co-authors separately as "AI-assisted commits."

### Step 10: Week-over-Week Trends (if window >= 14d)

If the time window is 14 days or more, split into weekly buckets and show trends.

### Step 11: Streak Tracking

Count consecutive days with at least 1 commit to origin/main:
- Team streak
- Personal streak

### Step 12: Load History & Compare

Check for prior retro history:

```bash
ls -t .context/retros/*.json 2>/dev/null || echo "No prior retros"
```

**If prior retros exist:** Calculate deltas and include a **Trends vs Last Retro** section.

**If no prior retros:** Skip comparison, append "First retro recorded — run again next week to see trends."

### Step 13: Save Retro History

Save a JSON snapshot:

```bash
mkdir -p .context/retros
```

Use this schema:
```json
{
  "date": "YYYY-MM-DD",
  "window": "7d",
  "metrics": {
    "commits": 47,
    "contributors": 3,
    "insertions": 3200,
    "deletions": 800,
    "net_loc": 2400,
    "test_loc": 1300,
    "test_ratio": 0.41,
    "active_days": 6,
    "sessions": 14,
    "deep_sessions": 5,
    "avg_session_minutes": 42,
    "loc_per_session_hour": 350,
    "feat_pct": 0.40,
    "fix_pct": 0.30,
    "peak_hour": 22,
    "ai_assisted_commits": 32
  },
  "authors": {
    "Name": { "commits": 32, "insertions": 2400, "deletions": 300, "test_ratio": 0.41, "top_area": "src/" }
  },
  "version_range": ["1.16.0", "1.16.1"],
  "streak_days": 47
}
```

### Step 14: Write the Narrative

Structure the output as:

**Tweetable summary** (first line):
```
Week of Mar 1: 47 commits (3 contributors), 3.2k LOC, 38% tests, peak: 10pm | Streak: 47d
```

## Engineering Retro: [date range]

### Summary Table
### Trends vs Last Retro (if applicable)
### Time & Session Patterns
### Shipping Velocity
### Code Quality Signals
### Focus & Highlights
### Your Week (personal deep-dive)
### Team Breakdown (skip if solo)
### Top 3 Team Wins
### 3 Things to Improve
### 3 Habits for Next Week
### Week-over-Week Trends (if applicable)

---

## Compare Mode

When the user runs `/retro compare` (or `/retro compare 14d`):

1. Compute metrics for the current window
2. Compute metrics for the immediately prior same-length window
3. Show a side-by-side comparison table with deltas
4. Write narrative highlighting biggest improvements and regressions
5. Save only the current-window snapshot

## Tone

- Encouraging but candid, no coddling
- Specific and concrete — always anchor in actual commits/code
- Skip generic praise — say exactly what was good and why
- Frame improvements as leveling up, not criticism
- Never compare teammates against each other negatively
- Use markdown tables and code blocks for data, prose for narrative
- Output directly to the conversation — only write `.context/retros/` JSON to filesystem

## Important Rules

- ALL narrative output goes directly to the user. The ONLY file written is the JSON snapshot.
- Use `origin/main` for all git queries (not local main which may be stale)
- Convert all timestamps to Pacific time for display
- If the window has zero commits, say so and suggest a different window
- On first run (no prior retros), skip comparison sections gracefully
