---
name: ship
version: 1.0.0
description: >
  Use this skill for the fully automated ship workflow: merge main, run tests, review diff, bump version, update CHANGELOG, commit, push, create PR. Optimized for minimal confirmation — only stops for critical issues.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Question
---

# Ship: Fully Automated Ship Workflow

You are running the ship workflow. This is a **non-interactive, fully automated** workflow. Do NOT ask for confirmation at every step. Run straight through and output the PR URL at the end.

**Only stop for:**
- On `main` branch (abort)
- Merge conflicts that can't be auto-resolved
- Test failures
- Critical issues in pre-landing review that user chooses to fix
- Minor or major version bump needed (ask)
- TODOS.md missing and user wants to create one

**Never stop for:**
- Uncommitted changes (always include them)
- Version bump choice (auto-pick MICRO or PATCH)
- CHANGELOG content (auto-generate from diff)
- Commit message approval (auto-commit)

---

## Step 1: Pre-flight

1. Check the current branch. If on `main`, **abort**: "You're on main. Ship from a feature branch."

2. Run `git status`. Uncommitted changes are always included.

3. Run `git diff main...HEAD --stat` and `git log main..HEAD --oneline` to understand what's being shipped.

---

## Step 2: Merge origin/main (BEFORE tests)

```bash
git fetch origin main && git merge origin/main --no-edit
```

**If there are merge conflicts:** Try to auto-resolve if they are simple (VERSION, CHANGELOG). If complex, **STOP** and show them.

---

## Step 3: Run tests (on merged code)

Detect available test frameworks:

```bash
# Check for common test runners
if [ -f "package.json" ]; then
  echo "NODE_PROJECT"
fi
if [ -f "Cargo.toml" ]; then
  echo "RUST_PROJECT"
fi
if [ -f "Makefile" ] && grep -q "^test" Makefile; then
  echo "MAKEFILE_TEST"
fi
```

Run the appropriate test command. If multiple test runners exist, run them in parallel.

**If any test fails:** Show the failures and **STOP**. Do not proceed.

**If all pass:** Continue silently.

---

## Step 3.5: Pre-Landing Review

Review the diff for structural issues that tests don't catch.

1. Use the review checklist (search for `*checklist*` or use the default from the review skill)
2. Run `git diff origin/main` to get the full diff
3. Apply the review checklist in two passes:
   - **Pass 1 (CRITICAL):** SQL & Data Safety, LLM Output Trust Boundary
   - **Pass 2 (INFORMATIONAL):** All remaining categories
4. **Always output ALL findings**
5. Output a summary header: `Pre-Landing Review: N issues (X critical, Y informational)`
6. **If CRITICAL issues found:** For EACH critical issue, use a separate Question with:
   - The problem
   - Your recommended fix
   - Options: A) Fix it now (recommended), B) Acknowledge and ship anyway, C) False positive
   After resolving: if the user chose A on any issue, apply fixes, commit (`git add <fixed-files> && git commit -m "fix: apply pre-landing review fixes"`), then **STOP** and tell the user to run ship again.
7. **If only non-critical issues found:** Output them and continue.
8. **If no issues found:** Output "Pre-Landing Review: No issues found." and continue.

Save the review output — it goes into the PR body.

---

## Step 4: Version bump (auto-decide)

1. Read the current `VERSION` file (detect format: semver, 4-digit, etc.)
2. **Auto-decide the bump level based on the diff:**
   - Count lines changed (`git diff origin/main...HEAD --stat | tail -1`)
   - **MICRO/PATCH** (least significant): < 50 lines changed, trivial tweaks
   - **MINOR** (middle): 50+ lines changed, bug fixes, features
   - **MAJOR** (most significant): **ASK the user** — breaking changes only
3. Compute the new version and write it to the VERSION file.

---

## Step 5: CHANGELOG (auto-generate)

1. Read `CHANGELOG.md` header to know the format. If no CHANGELOG exists, create one.
2. Auto-generate the entry from ALL commits on the branch:
   - Use `git log main..HEAD --oneline` for commit list
   - Use `git diff main...HEAD` for full diff context
   - Categorize changes: `### Added`, `### Changed`, `### Fixed`, `### Removed`
   - Insert after the file header, dated today
   - Format: `## [X.Y.Z] - YYYY-MM-DD`

**Do NOT ask the user to describe changes.** Infer from the diff and commit history.

---

## Step 5.5: TODOS.md (auto-update)

Cross-reference TODOS.md against the changes being shipped.

**1. Check if TODOS.md exists.** If not, ask if the user wants to create one.

**2. Detect completed TODOs:**
- Match commit messages against TODO titles
- Check if files referenced in TODOs appear in the diff
- Be conservative — only mark clearly completed items

**3. Move completed items** to a `## Completed` section with version and date.

**4. Output summary:** `TODOS.md: N items marked complete.`

---

## Step 6: Commit

Analyze the diff and group changes into logical commits. Each commit should represent **one coherent change**.

**Commit ordering:**
- Infrastructure: config, dependencies
- Core logic: models, services (with tests)
- UI: controllers, views, components (with tests)
- VERSION + CHANGELOG + TODOS: always in the final commit

**Rules:**
- A model and its test go in the same commit
- A service and its test go in the same commit
- If total diff is small (< 50 lines, < 4 files), a single commit is fine
- Each commit must be independently valid (no broken imports)

Commit message format: `<type>: <summary>` (type = feat/fix/chore/refactor/docs)

---

## Step 7: Push

```bash
git push -u origin <branch-name>
```

---

## Step 8: Create PR

Check if `gh` (GitHub CLI) is available:

```bash
gh --version 2>/dev/null && echo "GH_AVAILABLE"
```

If `gh` is available, create the PR:

```bash
gh pr create --title "<type>: <summary>" --body "<structured body>"
```

Include in the PR body:
- Summary from CHANGELOG
- Pre-Landing Review findings
- TODOS updates
- Test results

**Output the PR URL** — this should be the final output.

If `gh` is not available, instruct the user to push and create a PR manually, providing the branch name and suggested PR description.

---

## Important Rules

- **Never skip tests.** If tests fail, stop.
- **Never skip the pre-landing review.**
- **Never force push.** Use regular `git push` only.
- **Never ask for confirmation** except for MAJOR version bumps and CRITICAL review findings.
- **Split commits for bisectability** — each commit = one logical change.
- **TODOS completion detection must be conservative.** Only mark items when the diff clearly shows completion.
