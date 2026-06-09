# RAG Corpus — Ground Answers in Project Docs

## Location
`C:\Users\scott\AppData\Local\hermes\rag_corpus\`

## What's Indexed
63 files, 1.1M chars across 6 categories:
- `corpus_systems.rag` — MAAPS, Nexus, Hydra, CLAP prompts, AI Founder, SOTA, etc.
- `corpus_ethos-db.rag` — 25 ETHOS Digital Media database entries
- `corpus_code.rag` — Training pipeline code (RL agents)
- `corpus_projects.rag` — Project documentation
- `corpus_prompts.rag` — Master/Suno prompts, ANGER PROMPTS
- `corpus_root.rag` — Inventory and top-level files

## How to Search
Before answering any question about the user's MAAPS systems, architecture, or code:
```bash
rg "search term" C:\Users\scott\AppData\Local\hermes\rag_corpus\corpus_*.rag
```

Category-specific:
```bash
rg "mamba state space" C:\Users\scott\AppData\Local\hermes\rag_corpus\corpus_systems.rag
rg "training" C:\Users\scott\AppData\Local\hermes\rag_corpus\corpus_code.rag
```
## Rebuild

After adding new docs to `C:\\Users\\scott\\notion-export\\`:
```bash
python C:\\Users\\scott\\AppData\\Local\\hermes\\scripts\\build_rag_corpus_fast.py
```

## Adding External Files from Drives

When the user points you at files on external drives (E:, F:, etc.) or other directories, add them to the RAG corpus:

1. **Copy to rag_corpus:** `cp -r <source> "/c/Users/scott/AppData/Local/hermes/rag_corpus/<name>/"`
2. **Fix extensions:** Files without `.md` extension won't be searchable. Copy with `.md` suffix: `cp <file> "<dest>/$(basename).md"`
3. **Update index.json:** Bump `total_files`, add entry to `added` dict
4. **Blob files stay as-is in rag_corpus/
