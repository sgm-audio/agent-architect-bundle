# Portfolio Cleanup Workflow

## When to Use

The user has accumulated 30-70 repos across personal and org GitHub accounts. They want a clean portfolio: repos accurately described, stubs deleted, local changes pushed, READMEs rewritten. They're ready to show their work and generate income.

## Signals

- User says "I need to go through my repos"
- User mentions ~70 repos they can't keep track of
- User is ready to ship but wants a clean profile first
- User has local dirty clones that haven't been pushed
- User has repos they pushed from hospital that they barely remember

## Full Workflow

### Phase 0: Gather Data

Get the full repo list from both accounts:

```bash
gh repo list scottmills306 --limit 100 --json name,description,isPrivate,url,primaryLanguage,diskUsage,isEmpty,updatedAt
gh repo list SGM-Studios --limit 100 --json name,description,isPrivate,url,primaryLanguage,diskUsage,isEmpty,updatedAt
```

Find local clones with dirty state:

```bash
for dir in "/c/Dev/Audio Development/0 CLARA" "/c/Dev/mamba3" "/c/Dev/stem_midi_pro" ...; do
  if [ -d "$dir/.git" ]; then
    origin=$(git -C "$dir" remote get-url origin 2>/dev/null)
    status=$(git -C "$dir" status --porcelain 2>/dev/null | wc -l)
    echo "$status dirty | $origin | $dir"
  fi
done
```

### Phase 1: Categorize (via parallel subagents)

Run one subagent per account. Each subagent gets:
- Full repo list via `gh repo list`
- Instructions to categorize: SHIP / MERGE / ARCHIVE / DELETE
- Reasoning for each verdict
- README-rewrite flags

Subagent prompt template:
> Categorize all GitHub repos under [account] into: SHIP (active project worth showing), MERGE (combine into another repo), ARCHIVE (keep but mark as stale/archived), DELETE (empty or stub repos with no value). For each repo, state your reasoning in 1 sentence. Also flag any repo that needs its README rewritten.

### Phase 2: Verify Before Deleting

**Critical step:** Not all "empty" repos are empty. Check for hidden projects:

```bash
# Check for user-authored spec files
gh api repos/owner/repo-name/contents --jq '.[].name'
gh api repos/owner/repo-name/contents/src --jq '.[].name'

# Check git log for AI authorship vs template clone
gh api repos/owner/repo-name/commits --jq '.[].commit.author.name'

# Check for PLAN.md, SPECIFICATION.md, CLAUDE.md
gh api repos/owner/repo-name/contents/PLAN.md --jq '.content' 2>/dev/null | base64 -d
```

**Signs of a hidden project:**
- PLAN.md, SPECIFICATION.md, or CLAUDE.md present (user-authored specs)
- Custom components in `src/components/` beyond template boilerplate
- Multiple pages in `src/pages/`
- `supabase/` or backend configs
- git log shows multiple commits from different sessions
- Large disk usage (50MB+) that's not just node_modules

### Phase 3: Execute Deletions

```bash
gh repo delete scottmills306/empty-repo --yes
```

Can be parallelized — deletions don't depend on each other.

### Phase 4: Push Dirty Local Clones

For each dirty repo:

```bash
cd /path/to/repo
git remote get-url origin  # verify remote
git status --short         # review changes
git add -A
git commit -m "Portfolio audit: [summary of changes]"
git push origin main
```

**Pitfall:** Some local repos point to a different remote (e.g., `username/repo` instead of the actual org/personal account). Fix the remote before pushing:
```bash
git remote set-url origin https://github.com/correct-owner/repo-name.git
```

### Phase 5: Fix READMEs

Every SHIP repo gets a README that answers three questions:

1. **What IS this project?** — One-line elevator pitch. First sentence tells someone whether to care.
2. **What DOES it do?** — 3-5 bullet features. Not what you hope it will do. Current reality.
3. **How do I INSTALL and use it?** — Exact commands. Dependencies. Platform requirements.

README structure:
```markdown
# Project Name

One-line description.

## What It Does
- Feature 1
- Feature 2
- Feature 3

## Quick Start
```bash
pip install -r requirements.txt
python main.py
```

## Requirements
- Python 3.10+
- [Other deps]
```

### Phase 6: Archive Stale Repos

```bash
gh repo edit owner/repo-name --visibility private  # if public
gh api -X PATCH repos/owner/repo-name -f archived=true
```

Add an archival notice to the README:
> **This project is archived.** See [active project URL] for current work.

## Subagent Delegation Pattern

```python
results = delegate_task(
    goal="Categorize all GitHub repos under [account]",
    context="Full repo list + categorization instructions...",
    toolsets=['terminal', 'web']
)
```

Run personal and org accounts in parallel (2 subagents). Each returns a categorization table. Combine results for the user's review.

## Decision Tree for Each Repo

```
Is the repo empty (0KB, no files)?
  └─ Yes → Check for hidden content via API
       ├─ Hidden project found → SHIP (with README fix)
       └─ Actually empty → DELETE
  └─ No → Is it a duplicate/fragment of another repo?
       ├─ Yes → MERGE into parent repo
       └─ No → Is it a stale side-project or template?
            ├─ Yes → ARCHIVE
            └─ No → SHIP (fix README if needed)
```

## Common Pitfalls

1. **Don't trust `isEmpty` flag alone.** Some "empty" repos have content pushed directly (not through the GitHub auto-init). Always verify via API file listing.
2. **"remix-of-*" repos may have real projects.** The user used Qwen Coder at the hospital and pushed to whatever repo didn't break. Template-named repos may contain real projects.
3. **Not all dirty local repos have the right remote.** Some clones point to a generic `username/repo` URL that doesn't exist. Verify before pushing.
4. **Large repos with no description might still be the flagship.** `CLARA` (23MB C++) had no README but was the most important repo. Size + language detection helps here.
5. **Personal and org accounts have overlapping repos.** The same project may exist in both (e.g., `CLARA` in personal, `clara` in org). Decide which is canonical, point the other via archival notice.
