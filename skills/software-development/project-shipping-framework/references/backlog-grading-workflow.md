# Backlog Grading Workflow

Use when the user asks you to clean up, triage, or grade a backlog directory (e.g. `C:/backlog`, a download folder, an archive).

## Principle

Don't ask — just execute. "Should I clean this up?" → clean it up. "Grade these files" → grade them AND execute the cleanup in the same turn.

## 6-Phase Workflow

### Phase 1: Inventory
Get the full picture first — don't read files blind.

```bash
# Count everything
find "TARGET" -type f | wc -l

# By extension distribution
find "TARGET" -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Subdirectory structure
find "TARGET" -maxdepth 2 -type d | sort

# Large files (sorted by size)
find "TARGET" -type f -exec ls -lh {} \; | sort -k 5 -rh | head -30
```

### Phase 2: Parallel Analysis (Key Efficiency Pattern)
Delegate two sub-agents simultaneously — one for root-level files, one for subdirectories. This cuts analysis time in half.

- **Sub-agent 1**: Sample first 10-20 lines of every root-level file to determine content type (AI prompt, session log, code, doc, script, paper, binary noise)
- **Sub-agent 2**: Inspect each subdirectory — read READMEs, key source files, check status (prototype/alpha/beta/abandoned), count real code vs cache

### Phase 3: Grade Each Item
Three tiers:

| Grade | Meaning | Action |
|-------|---------|--------|
| **SHIP** | Valuable code, doc, or tool that belongs in active workspace | Move to `C:\dev\<category>\` |
| **ARCHIVE** | Useful reference but not actively needed | tar.gz to `C:\archive\` |
| **TRASH** | No unique value | Delete immediately |

### Trash categories (always delete):
- Raw AI agent session logs (full of tool call records — no extracted artifact)
- Duplicate AI system prompts (same XML format, same genre)
- Stale lead gen output (>1 month old)
- Abandoned prototypes where <50% of components were built
- All caches: `__pycache__`, `.pyc`, `venv`, `node_modules`, `.exe`, `.pyd`, `.dll` (regeneratable)
- Mystery large PNGs with no context

### Phase 4: Execute Cleanup
Order matters — do trash first to free space, then move ships, then archive.

1. **Delete trash** — `rm -rf` for projects, `rm -f` for files
2. **Move ships** — `mv` to `C:\dev\<category>\`
3. **Create archive** — `tar czf "/c/archive/backlog-name.tar.gz" <remaining items>`
4. **Delete archived originals**

### Phase 5: Flatten nested paths
Moves often create extra nesting (e.g. `Lead Hunter` → `/c/dev/lead-hunter/Lead Hunter/`). Fix:

```bash
mv "/c/dev/target/nested"/* "/c/dev/target/"
mv "/c/dev/target/nested"/.* "/c/dev/target/"
rmdir "/c/dev/target/nested"
```

### Phase 6: Verify
```bash
# Source should be empty (except . and ..)
ls -la "SOURCE"

# Destination should have clean structure
du -sh "/c/dev/<project>"

# Archive should exist with reasonable size
ls -lh "/c/archive/"
```

## Common Pitfalls

1. **Asking permission** — "Want me to run the cleanup?" violates the JUST DO IT rule. Run it, tell them what happened after.
2. **Not checking for hidden content** — `.Musician_something` directories are easy to miss. Always `find` not `ls`.
3. **Not flattening moved paths** — Extra nesting makes the workspace feel messy. Always flatten after move.
4. **Forgetting caches** — `venv/`, `node_modules/`, `__pycache__` triple disk usage. Delete them; they're `pip install` away from being recreated.
5. **Not removing `.git/` from archives** — If you're compressing a project to archive, strip `.git/` first (reduces size drastically).
6. **Judge session logs by content not name** — A file named "Code Refactoring Guide" is likely a raw agent session log full of tool calls, not an actual guide.
7. **Batch all deletes** — Delete all trash files with a single `rm` command, not one-by-one.
