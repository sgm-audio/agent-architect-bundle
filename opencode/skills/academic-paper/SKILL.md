---
name: academic-paper
description: "12-agent academic paper writing pipeline with 10 modes: full write, plan (Socratic chapter-by-chapter), outline-only, revision, revision-coach (parse reviewer comments), abstract-only, literature-review, format-convert (LaTeX/DOCX), citation-check, and disclosure (AI usage statements). Supports 6 paper types (IMRaD, literature review, case study, theoretical, policy brief, conference), 5 citation formats (APA 7, Chicago, MLA, IEEE, Vancouver), bilingual abstracts (zh-TW + EN), and multiple output formats (LaTeX, DOCX via Pandoc, PDF, Markdown). Includes simulated peer review, citation verification, and publication-quality figure generation (matplotlib/ggplot2). Triggers: write paper, academic paper, paper outline, write abstract, revise paper, literature review paper, check citations, convert to LaTeX, format paper, conference paper, journal article, thesis chapter, research paper, guide my paper, parse reviews, revision roadmap."
metadata:
  source: "https://github.com/cheng-i/ars-academic-research-skills"
  version: "3.1.2"
  related_skills:
    - deep-research
    - academic-paper-reviewer
    - academic-pipeline
---

# Academic Paper

A general-purpose academic paper writing tool — 12-agent pipeline covering all disciplines.

## Quick Start

```
Write a paper on the impact of AI on higher education quality assurance
```

## Agents (12)

| # | Agent | Phase |
|---|-------|-------|
| 1 | `intake_agent` | Configuration interview: paper type, discipline, citation/output format, language |
| 2 | `literature_strategist_agent` | Search strategy, source screening, annotated bibliography | 
| 3 | `structure_architect_agent` | Outline, word count allocation, evidence mapping |
| 4 | `argument_builder_agent` | Claim-evidence chains, logical flow, counter-arguments |
| 5 | `draft_writer_agent` | Section-by-section drafting, register adjustment |
| 6 | `citation_compliance_agent` | Format verification, DOI checking, reference completeness |
| 7 | `abstract_bilingual_agent` | zh-TW + EN bilingual abstract, 5-7 keywords each |
| 8 | `peer_reviewer_agent` | Simulated double-blind review, 5-dimension scoring, max 2 rounds |
| 9 | `formatter_agent` | LaTeX/DOCX/PDF/Markdown output, citation format conversion |
| 10 | `socratic_mentor_agent` | Chapter-by-chapter guidance in plan mode (4 question types) |
| 11 | `visualization_agent` | Publication-quality figures (matplotlib/ggplot2), APA 7, colorblind-safe |
| 12 | `revision_coach_agent` | Parse unstructured reviewer comments into structured Revision Roadmap |

## Workflow (8 Phases)

```
Phase 0: CONFIG        -> [intake_agent]             -> Paper Configuration Record
Phase 1: RESEARCH      -> [literature_strategist]    -> Search Strategy + Sources
Phase 2: ARCHITECTURE  -> [structure_architect]      -> Outline + Evidence Map
Phase 3: ARGUMENTATION -> [argument_builder]         -> Argument Blueprint
Phase 4: DRAFTING      -> [draft_writer]             -> Complete Draft (+ figures if applicable)
Phase 5a: CITATIONS    -> [citation_compliance]      -> Citation Audit Report
Phase 5b: ABSTRACT     -> [abstract_bilingual]       -> Bilingual Abstract + Keywords
Phase 6: PEER REVIEW   -> [peer_reviewer]            -> Review Report (max 2 revision loops)
Phase 7: FORMAT        -> [formatter]                -> Final Output Package
```

### Checkpoints
- User must confirm Paper Configuration Record before Phase 1 (IRON RULE)
- Outline must be user-approved before Phase 3
- Max 2 revision loops; unresolved items → "Acknowledged Limitations"
- Critical peer review issues block progression to Phase 7

## Modes (10)

| Mode | Trigger | Agents | Output |
|------|---------|--------|--------|
| `full` | "Write a paper" | All | Complete paper draft |
| `plan` | "Guide my paper" | intake → mentor → architect → argument | Chapter Plan + INSIGHT Collection |
| `outline-only` | "Paper outline" | intake → strategist → architect | Detailed outline + evidence map |
| `revision` | "Revise paper" | reviewer → writer → citation | Revised draft with tracked changes |
| `revision-coach` | "Parse reviews" | revision_coach only | Revision Roadmap + Response Letter Skeleton |
| `abstract-only` | "Write abstract" | intake → abstract | Bilingual abstract + keywords |
| `lit-review` | "Literature review" | intake → strategist | Annotated bibliography + synthesis |
| `format-convert` | "Convert to LaTeX" / "Convert citations to [format]" | formatter only | Formatted document (LaTeX/DOCX/PDF/MD) |
| `citation-check` | "Check citations" | citation only | Citation error report |
| `disclosure` | "Generate AI usage statement" | formatter only | Venue-specific AI disclosure paragraph(s) |

### Quick selection
- Starting from scratch → `full`
- Need guidance before writing → `plan`
- Have a draft with reviewer feedback → `revision`
- Have unstructured reviewer comments → `revision-coach`

## Output

**Formats**: LaTeX (.tex + .bib), DOCX (via Pandoc), PDF (via LaTeX or Pandoc), Markdown

**Citation formats**: APA 7 (default), Chicago (Author-Date / Notes-Bibliography), MLA 9, IEEE, Vancouver

**Figures**: matplotlib/seaborn (Python) or ggplot2 (R), APA 7 formatting, colorblind-safe

**Mandatory inclusions** (IRON RULE): Data Availability Statement, Ethics Declaration, Author Contributions (CRediT), Conflict of Interest, Funding Acknowledgment, AI disclosure, Limitations section

## Triggers

**English**: write paper, academic paper, paper outline, write abstract, revise paper, literature review paper, check citations, convert to LaTeX, convert format, format paper, conference paper, journal article, thesis chapter, research paper, guide my paper, help me plan my paper, step by step paper, draft manuscript, write methodology, write discussion, parse reviews, revision roadmap, I got reviewer comments, convert citations

**中文**: 寫論文, 學術論文, 論文大綱, 寫摘要, 修改論文, 文獻回顧論文, 檢查引用, 轉 LaTeX, 轉換格式, 研討會論文, 期刊文章, 學位論文, 研究論文, 引導我寫論文, 幫我規劃論文, 審查意見, 修訂路線圖

## Anti-Patterns & Quality

| Anti-Pattern | Correct Behavior |
|---|---|
| AI-typical overused terms ("delve", "crucial") | Use discipline-specific vocabulary |
| Em dash abuse (>2 per page) | Use parentheses, commas, or restructure |
| Throat-clearing openers | Start with the claim or finding directly |
| Uniform paragraph lengths (4-5 sentences each) | Vary naturally (2-8 sentences) |
| Fabricated citations (IRON RULE) | Every citation verified via DOI or WebSearch |
| Sycophantic revision | Use REVIEWER_DISAGREE when warranted |
| Scope creep during revision | Address reviewer concerns only |

**Quality**: Zero citation orphans, consistent register, +/-10% word count compliance. Bilingual abstracts independently composed (not translations). Every paper must include mandatory ethics/author/disclosure statements.
