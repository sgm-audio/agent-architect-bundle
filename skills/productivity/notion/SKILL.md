---
name: notion
description: "Notion API + ntn CLI: pages, databases, markdown, Workers."
version: 1.0.0
author: SGM Studios
license: MIT
tags: [notion, productivity, api]
---

# Notion Skill

## Tools

- **ntn CLI** — Notion Terminal Native. Install: `pip install ntn` or `npx ntn`
- **Notion API** — Direct REST via curl with `NTN_TOKEN` or `NOTION_TOKEN`

## Common Operations

### Pages
```bash
ntn page create --parent <database_id> --title "Page Title" --content "Markdown body"
ntn page read <page_id>
ntn page update <page_id> --property "Status" --select "Done"
```

### Databases
```bash
ntn db list
ntn db query <database_id> --filter '{"property":"Status","select":{"equals":"In Progress"}}'
```

### Quick notes
```bash
echo "- Item to add" | ntn append <page_id>
```

## Config
```bash
export NOTION_TOKEN=ntn_xxxxx  # Or use ntn config set
```

## Pitfalls
- Notion API rate limit: 3 req/sec per integration
- ntn CLI uses the Notion API via `NTN_TOKEN`, not a separate credential
- Database IDs look like UUIDs — find them in the Notion page URL or via `ntn db list`
- Markdown import drops unsupported blocks (tables > 3 cols, etc.)
