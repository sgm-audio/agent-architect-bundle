---
name: deep-research
description: "Universal deep research agent team for rigorous academic research. 13 agents across 7 modes: full research report, quick brief, paper review, literature review, fact-check, Socratic guided dialogue, and PRISMA-compliant systematic review with meta-analysis. Covers research question formulation, methodology design, systematic literature search, source verification (evidence hierarchy grading, predatory journal detection), cross-source synthesis, risk-of-bias assessment (RoB 2 / ROBINS-I), meta-analysis, APA 7 report compilation, editorial review, ethics review, devil's advocate challenges, and post-research literature monitoring. Triggers: research, deep research, literature review, systematic review, meta-analysis, evidence synthesis, fact-check, guide my research, help me think through."
metadata:
  source: "https://github.com/cheng-i/ars-academic-research-skills"
  version: "2.9.4"
  related_skills:
    - academic-paper
    - academic-pipeline
---

# Deep Research

A domain-agnostic 13-agent team for rigorous academic research on any topic.

## Quick Start

```
Research the impact of AI on higher education quality assurance
Guide my research on the impact of declining birth rates on private universities
```

## Agents (13)

| # | Agent | Role |
|---|-------|------|
| 1 | `research_question_agent` | Transforms vague topics into FINER-scoped research questions |
| 2 | `research_architect_agent` | Designs methodology blueprint (paradigm, method, data strategy) |
| 3 | `bibliography_agent` | Systematic literature search, screening, annotated bibliography |
| 4 | `source_verification_agent` | Evidence hierarchy grading, predatory journal detection |
| 5 | `synthesis_agent` | Cross-source integration, contradiction resolution, gap analysis |
| 6 | `report_compiler_agent` | Full APA 7 report drafting (Title through References) |
| 7 | `editor_in_chief_agent` | Q1 editorial review: originality, rigor, evidence sufficiency |
| 8 | `devils_advocate_agent` | Challenges assumptions, logical fallacies, confirmation bias |
| 9 | `ethics_review_agent` | AI disclosure, attribution integrity, dual-use screening |
| 10 | `socratic_mentor_agent` | Guides research thinking via Socratic questioning (5 layers) |
| 11 | `risk_of_bias_agent` | RoB 2 / ROBINS-I assessment with traffic-light visualization |
| 12 | `meta_analysis_agent` | Effect sizes, heterogeneity, GRADE for systematic reviews |
| 13 | `monitoring_agent` | Post-research literature monitoring (alerts, retractions) |

## Workflow (6 Phases)

```
Phase 1: SCOPING     -> RQ + Methodology Blueprint + Devil's Advocate checkpoint
Phase 2: INVESTIGATE -> Systematic search + Source verification + Grading
Phase 3: ANALYSIS    -> Cross-source synthesis + Gap analysis + DA checkpoint
Phase 4: COMPOSE     -> Full APA 7 report draft
Phase 5: REVIEW      -> Editorial + Ethics + Devil's Advocate (parallel)
Phase 6: REVISION    -> Address feedback, max 2 loops
```

### Checkpoints
- Devil's Advocate has 3 mandatory checkpoints; CRITICAL issues block progression
- Ethics Review can halt delivery for critical concerns
- User confirmation required after Phase 1

## Modes (7)

| Mode | Agents | Output |
|------|--------|--------|
| `full` | 9 core | Full APA 7 report (3000-8000 words) |
| `socratic` | Mentor + RQ + DA | Guided dialogue → Research Plan Summary |
| `quick` | RQ + Biblio + Verification + Report | Research brief (500-1500 words) |
| `lit-review` | Biblio + Verification + Synthesis | Annotated bibliography + synthesis |
| `fact-check` | Source Verification only | Per-claim verification report |
| `review` | Editor + DA + Ethics | Reviewer report on provided text |
| `systematic-review` | All except Mentor | PRISMA 2020 report + forest plot + GRADE |

### Mode selection
- Vague idea, need guidance → `socratic` (default when ambiguous)
- Clear RQ, need comprehensive research → `full`
- Need quick brief → `quick`
- Need PRISMA-compliant review → `systematic-review`
- Verify specific claims → `fact-check`
- Evaluate a paper before citing → `review`

## Triggers

**English**: research, deep research, literature review, systematic review, meta-analysis, PRISMA, evidence synthesis, fact-check, methodology, APA report, academic analysis, policy analysis, guide my research, help me think through, monitor this topic

**中文**: 研究, 深度研究, 文獻回顧, 系統性回顧, 後設分析, 事實查核, 引導我的研究, 幫我釐清

### Socratic mode activation (intent-based, any language)
1. No clear research question, wants guided thinking
2. Asks to be guided/mentored through research
3. Expresses uncertainty about where to start
4. Wants to brainstorm or clarify a direction
5. Describes a vague interest without specific question

### Does NOT trigger
- Writing a paper → `academic-paper`
- Reviewing a paper → `academic-paper-reviewer`
- Full pipeline → `academic-pipeline`

## Handoff to academic-paper

After research completes, say "write a paper based on this" → materials auto-detected by `academic-paper` intake:
- RQ Brief → skip topic scoping
- Bibliography → skip literature search
- Synthesis → accelerate findings/discussion

## Anti-Patterns & Quality

| Anti-Pattern | Correct Behavior |
|---|---|
| Confirmation bias in source selection | DA checkpoint must include counter-evidence search |
| Cherry-picking evidence | Report full evidence landscape including conflicts |
| Fabricated citations | Every reference verified independently; gray zone = FAIL |
| Skipping phases | Complete each phase fully before advancing |
| Shallow Socratic mode | Genuine questions, never lead to predetermined conclusions |
| Source tier inflation | Strict evidence hierarchy (peer-reviewed > preprint > gray lit) |

**IRON RULES**: Every claim needs a citation. CRITICAL severity issues block progression. Gray zone references = FAIL. Socratic mode never gives direct answers.
