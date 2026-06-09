# Bulk GitHub Repo Triage via Parallel Subagents

## When to use

You have 20+ repos and need to categorize them into SHIP / MERGE / ARCHIVE / DELETE. One agent doing sequential `gh repo view` calls takes forever. Parallel subagents cut this down to ~60-90 seconds total.

## Workflow

### Phase 1: Gather raw data

```bash
# Dump all repos with metadata to JSON
gh repo list <owner> --limit 100 --json name,description,isPrivate,url,primaryLanguage,diskUsage,isEmpty,updatedAt > all_repos.json
```

### Phase 2: Split across parallel subagents

Split repos by owner (personal vs org) or alphabetically. Each subagent gets its own batch.

Use `delegate_task` with `tasks` array (not `goal`):

```
delegate_task(
    tasks=[
        {"goal": "Categorize all GitHub repos under <owner1>...", "context": "Repo data is in JSON. Use gh repo list...", "toolsets": ["terminal", "web"]},
        {"goal": "Categorize all GitHub repos under <owner2>...", "context": "Same approach...", "toolsets": ["terminal", "web"]}
    ]
)
```

Each subagent should return structured output:

| Category | Criteria |
|----------|----------|
| SHIP | Active project with substance, worth showing |
| MERGE | Fragment/duplicate of another SHIP repo |
| ARCHIVE | Old version, side project, template noise |
| DELETE | Empty stub (0KB, isEmpty=true), pure template |

### Phase 3: Synthesize

Combine subagent results. Resolve cross-account duplicates (same project in personal AND org account). Produce final count matrix.

### Phase 4: Execute (require user sign-off on DELETE)

- DELETE: `gh repo delete <owner>/<repo> --yes` (needs `delete_repo` scope on PAT)
- ARCHIVE: `gh repo edit <owner>/<repo> --archived`
- RENAME: `gh repo rename <new-name> --repo <owner>/<old-name>`
- MERGE: Manual process — clone, combine, push, then archive old

## Phase 5: Profile README updates\n\nAfter cleanup, update the user's profile and org READMEs:\n\n```bash\n# Create/recreate personal profile repo (must match username)\ngh repo create <user>/<user> --private --description \"GitHub profile\"\ncd /tmp && git clone https://github.com/<user>/<user>.git profile && cd profile\n# Write README.md with accurate projects, links, bio\ngh repo clone SGM-Studios/.github && cd .github\n# Write profile/README.md — check for:\n#   - Wrong username (typos like scottmill306 instead of scottmills306)\n#   - Wrong DAW (Ableton when user uses REAPER)\n#   - Enterprise/team language for a solo dev\n#   - Placeholder banner images\n```\n\n**What to check in org READMEs:**\n- Username handle accuracy (typos in @mentions)\n- DAW/pipeline claims (don't say Ableton if user uses REAPER)\n- Infrastructure claims (don't say Kubernetes for a solo laptop dev)\n- Copyright/legal language (\"All Rights Reserved\" + enterprise tone vs pragmatic)\n\n## Phase 6: Push local dirty repos\n\nUsers often have local clones with uncommitted changes. After org cleanup, find and push them:\n\n```bash\n# Find repos with uncommitted changes\nfor dir in /c/Dev/*/; do\n  if [ -d \"$dir/.git\" ]; then\n    dirty=$(git -C \"$dir\" status --porcelain 2>/dev/null | wc -l)\n    if [ \"$dirty\" -gt 0 ]; then\n      origin=$(git -C \"$dir\" remote get-url origin 2>/dev/null)\n      echo \"$dirty dirty | $origin | $dir\"\n    fi\n  fi\ndone\n\n# Commit and push each (use background=true for large repos with ML model files)\ngit -C <dir> add -A\ngit -C <dir> commit -m \"<descriptive message about the changes>\"\ngit -C <dir> push origin <branch>\n```\n\n**Large repos:** Use `notify_on_complete=true` for pushes >100MB (checkpoint files, ONNX models, venvs).\n\n## Pitfalls

1. **Fine-grained PATs don't inherit org access.** If the user gives you a \"YOLO\" PAT, check `gh auth status` to see the token scopes. If `read:org` is missing, org repos return 404.
2. **Name conflicts.** When renaming repos (e.g., moving a project into the portfolio slot), check if the target name already exists first. If so, archive/rename the old one first.
3. **Remix/Blink template repos aren't always empty.** The user may have pushed real code to a template-named repo. Always check file tree before categorizing as DELETE.
4. **`gh repo delete` silently says OK for already-deleted repos.** The 404 from the first attempt means it worked — don't re-attempt.

## Subagent context template

For each subagent, include a concise background about the user:

> "The user (Scott Mills, scottmills306) is a Berklee-trained audio engineer/solo dev building the MAAPS suite (CLARA, MambaDAW, Stem Surgeon, MambaCompressor, Stem+MIDI Pro). He wants a clean portfolio. Most repos were built over the last 6 months. Many are fragmented/duplicated across personal and org accounts. Some are Next.js/Blink template sites that don't represent his audio work. Categorize honestly."
