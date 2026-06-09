---
name: review
version: 1.0.0
description: >
  Use this skill for pre-landing PR review. Analyzes diff against main for SQL safety, LLM trust boundary violations, conditional side effects, and other structural issues. Integrates with Greptile AI review comments when available.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - Question
---

# Pre-Landing PR Review

You are running the review workflow. Analyze the current branch's diff against main for structural issues that tests don't catch.

---

## Step 1: Check branch

1. Run `git branch --show-current` to get the current branch.
2. If on `main`, output: **"Nothing to review — you're on main or have no changes against main."** and stop.
3. Run `git fetch origin main --quiet && git diff origin/main --stat` to check if there's a diff. If no diff, output the same message and stop.

---

## Step 2: Read the checklist

Look for a review checklist in the project. Search for files matching `*checklist*` in the project root and `.claude/` or `.opencode/` directories.

**If no checklist file can be found:** Use the default review checklist below. Do not proceed without a checklist.

### Default Review Checklist

**CRITICAL — SQL & Data Safety:**
- SQL injection vectors (string interpolation in queries)
- Mass assignment vulnerabilities
- Data exposure in API responses (PII, tokens, internal IDs)
- Missing authorization checks on data access
- Race conditions in database operations

**CRITICAL — LLM Output Trust Boundary:**
- Unsanitized LLM output rendered as HTML (XSS vector)
- LLM output used in SQL queries without validation
- LLM output used in system commands
- LLM output written to database without content review
- Missing output sanitization/validation layers

**INFORMATIONAL — Conditional Side Effects:**
- Feature flags that leave data in inconsistent states when toggled
- Code paths with hidden side effects (log writes, API calls, state mutations)
- Callbacks/observers that fire in unexpected order

**INFORMATIONAL — Magic Numbers & String Coupling:**
- Hard-coded URLs, API keys, timeouts, limits
- String literals duplicated across files

**INFORMATIONAL — Dead Code & Consistency:**
- Commented-out code
- Unused imports, variables, functions
- Inconsistent patterns (same pattern implemented differently in nearby code)

**INFORMATIONAL — LLM Prompt Issues:**
- Prompt injection vulnerabilities (unvalidated user input in prompts)
- Prompt leakage (system prompts exposed to users)
- Missing prompt versioning or evaluation

**INFORMATIONAL — Test Gaps:**
- Untested error paths
- Missing edge cases (empty states, boundary values, auth failures)
- Tests that don't actually assert the behavior they describe

**INFORMATIONAL — View/Frontend:**
- Missing loading/empty/error states
- Accessibility issues (missing aria labels, focus management)
- Hard-coded text that should be internationalized

---

## Step 2.5: Check for Greptile review comments (if available)

If the project uses GitHub and has a PR open, try to fetch Greptile or GitHub review comments.

```bash
# Check if gh is available and there's a PR
gh pr view --json number,title 2>/dev/null && echo "PR_EXISTS"
```

**If a PR exists:** Try to fetch review comments:
```bash
gh pr view --json comments,reviews 2>/dev/null
```

Classify any comments found:
- **VALID & ACTIONABLE** — real issues that need fixing
- **VALID BUT ALREADY FIXED** — issues addressed in newer commits
- **FALSE POSITIVE** — incorrect analysis
- **SUPPRESSED** — known false positives from prior triage

**If no PR exists, `gh` fails, or no comments found:** Skip this step silently.

---

## Step 3: Get the diff

```bash
git fetch origin main --quiet
git diff origin/main
```

---

## Step 4: Two-pass review

Apply the checklist against the diff in two passes:

1. **Pass 1 (CRITICAL):** SQL & Data Safety, LLM Output Trust Boundary
2. **Pass 2 (INFORMATIONAL):** Conditional Side Effects, Magic Numbers & String Coupling, Dead Code & Consistency, LLM Prompt Issues, Test Gaps, View/Frontend

---

## Step 5: Output findings

**Always output ALL findings** — both critical and informational. The user must see every issue.

- If CRITICAL issues found: output all findings, then for EACH critical issue use a separate Question with the problem, your recommended fix, and options (A: Fix it now, B: Acknowledge, C: False positive — skip).
  After all critical questions are answered, output a summary of what the user chose for each issue. If the user chose A (fix) on any issue, apply the recommended fixes. If only B/C were chosen, no action needed.
- If only non-critical issues found: output findings. No further action needed.
- If no issues found: output **Pre-Landing Review: No issues found.**

### Greptile comment resolution (if applicable)

After outputting your own findings, if Greptile comments were classified in Step 2.5:

**Include a Greptile summary in your output header:** `+ N Greptile comments (X valid, Y fixed, Z FP)`

1. **VALID & ACTIONABLE comments:** These follow the same Question flow as critical issues (A: Fix it now, B: Acknowledge, C: False positive).
2. **FALSE POSITIVE comments:** Present each via Question — explain why it's wrong, offer A) Reply explaining false positive, B) Fix it anyway, C) Ignore.
3. **VALID BUT ALREADY FIXED comments:** Note in output — no Question needed.
4. **SUPPRESSED comments:** Skip silently.

---

## Step 5.5: TODOS cross-reference

Read `TODOS.md` in the repository root (if it exists). Cross-reference the PR against open TODOs:

- **Does this PR close any open TODOs?** If yes, note which items.
- **Does this PR create work that should become a TODO?** If yes, flag it.
- **Are there related TODOs that provide context?** If yes, reference them.

If TODOS.md doesn't exist, skip this step silently.

---

## Important Rules

- **Read the FULL diff before commenting.** Do not flag issues already addressed in the diff.
- **Read-only by default.** Only modify files if the user explicitly chooses "Fix it now" on a critical issue. Never commit, push, or create PRs.
- **Be terse.** One line problem, one line fix. No preamble.
- **Only flag real problems.** Skip anything that's fine.
