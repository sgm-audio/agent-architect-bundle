---
name: academic-paper-reviewer
description: ""Multi-perspective academic paper review simulating 5 independent reviewers: Editor-in-Chief, 3 peer reviewers (methodology, domain, cross-disciplinary perspective), and Devil's Advocate. Automatically detects paper field, dynamically configures reviewer personas, and produces structured Editorial Decision with Revision Roadmap. 6 modes: full review, re-review (verification), quick assessment, methodology-focus, Socratic guided review, and calibration (measures reviewer FNR/FPR against gold set). Triggers: review paper, peer review, manuscript review, referee report, review my paper, critique paper, simulate review, editorial review, calibrate reviewer.""
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Academic Paper Reviewer", "opencode-migrated"]
    related_skills: []
---


# Academic Paper Reviewer

Simulates a complete international journal peer review process: field-aware reviewer configuration, 5 independent reviewers, structured editorial synthesis.

## Quick Start

```
Review this paper: [paste paper or provide file]
```

## Agents (7)

| # | Agent | Role |
|---|-------|------|
| 1 | `field_analyst_agent` | Analyzes field, configures 5 reviewer identities dynamically |
| 2 | `eic_agent` | Editor-in-Chief: journal fit, originality, overall quality |
| 3 | `methodology_reviewer_agent` | R1: research design, statistics, reproducibility |
| 4 | `domain_reviewer_agent` | R2: literature coverage, theory, domain contribution |
| 5 | `perspective_reviewer_agent` | R3: cross-disciplinary connections, practical impact |
| 6 | `devils_advocate_reviewer_agent` | Core argument challenges, logical fallacies, counter-arguments |
| 7 | `editorial_synthesizer_agent` | Synthesizes all reviews, makes editorial decision |

## Workflow (3 Phases)

```
Phase 0: FIELD ANALYSIS  -> [field_analyst]    -> Reviewer Configuration Card (5 personas)
Phase 1: PARALLEL REVIEW -> 5 reviewers (independently) -> 5 Review Reports
Phase 2: SYNTHESIS       -> [editorial_synthesizer] -> Editorial Decision + Revision Roadmap
                           Optional: Phase 2.5 Revision Coaching (Socratic dialogue)
```

### Checkpoints
- Reviewer Configuration Card presented for user adjustment after Phase 0
- 5 reviewers review independently without cross-referencing (IRON RULE)
- Synthesizer cannot fabricate — must trace to specific Phase 1 reports (IRON RULE)
- Devil's Advocate CRITICAL issues → Decision cannot be Accept (IRON RULE)
- READ-ONLY: Reviewers produce reports, never modify the manuscript (IRON RULE)
- Revision coaching only triggers when Decision ≠ Accept; user can skip

## Modes (6)

| Mode | Trigger | Agents | Output |
|------|---------|--------|--------|
| `full` | Default / "review this paper" | All 7 | 5 reports + Editorial Decision + Roadmap |
| `re-review` | "Check revisions" / verification | field + eic + synthesizer | Traceability matrix + residual issues |
| `quick` | "Quick review" | field + eic | EIC assessment + key issues list |
| `methodology-focus` | "Check methodology" | field + eic + methodology | In-depth methods review |
| `guided` | "Guide me through issues" | All + Socratic dialogue | Step-by-step guided review |
| `calibration` | "Calibrate reviewer" | All 7, 5x per gold paper | FNR/FPR/AUC + calibration report |

## Triggers

**English**: review paper, peer review, manuscript review, referee report, review my paper, critique paper, simulate review, editorial review, calibrate reviewer, reviewer calibration, measure reviewer accuracy

### Does NOT trigger
- Write a paper → `academic-paper`
- Deep research on a topic → `deep-research`
- Revise a paper (have review comments) → `academic-paper` (revision mode)

## Quality Standards

| Dimension | Requirement |
|---|---|
| Perspective differentiation | Each reviewer from a different angle; no duplicate criticisms |
| Evidence-based | EIC decision based on specific reviewer comments |
| Specificity | Cite specific passages, data, page numbers |
| Devil's Advocate completeness | Must produce strongest counter-argument |
| CRITICAL threshold | DA CRITICAL issues cannot be ignored by Editorial Decision |

## Anti-Patterns

| Anti-Pattern | Correct Behavior |
|---|---|
| Fabricating review comments | Every synthesis point traces to a specific Phase 1 report |
| Duplicate criticisms across reviewers | Each reviewer has distinct perspective |
| Ignoring DA CRITICAL findings | If DA finds CRITICAL → Decision cannot be Accept |
| Rubber-stamp re-review | Each concern independently verified against revised manuscript |
| Sycophantic score inflation | Scores evidence-based; methodology gaps cannot score >6 on rigor |
| Editing the manuscript | READ-ONLY: produce reports, never modify the paper |
| Generic feedback | Every criticism includes: what's wrong, where, and a proposed fix |
