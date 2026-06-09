---
name: academic-pipeline
description: "Orchestrator for the full academic research pipeline: research -> write -> integrity check -> review -> revise -> re-review -> final integrity check -> finalize. Coordinates deep-research, academic-paper, and academic-paper-reviewer into a seamless 10-stage workflow with mandatory integrity verification (citation/data verification + 7-mode AI research failure mode checklist), two-stage peer review, adaptive checkpoint system, revision loop management (max 1 re-revision), and process documentation. Supports mid-entry from any stage, cross-session resume via Material Passport, and optional claim-faithfulness audit. Triggers: academic pipeline, research to paper, full paper workflow, paper pipeline, end-to-end paper, research-to-publication, complete paper workflow."
metadata:
  source: "https://github.com/cheng-i/ars-academic-research-skills"
  version: "3.9.4"
  related_skills:
    - deep-research
    - academic-paper
    - academic-paper-reviewer
---

# Academic Pipeline

A lightweight orchestrator that manages the complete academic pipeline from research exploration to final manuscript. Detects stages, recommends modes, dispatches skills, manages transitions, and tracks state — does not perform substantive work.

## Quick Start

```
# Full workflow
I want to write a research paper on the impact of AI on higher education quality assurance

# Mid-entry (existing paper)
I already have a paper, help me review it

# Revision mode (received reviewer feedback)
I received reviewer comments, help me revise
```

## Agents (5)

| # | Agent | Role |
|---|-------|------|
| 1 | `pipeline_orchestrator_agent` | Detects stage, recommends mode, dispatches skills, manages transitions |
| 2 | `state_tracker_agent` | Records completed stages, materials, revision counts |
| 3 | `integrity_verification_agent` | 100% reference/citation/data verification (blocking gate) |
| 4 | `collaboration_depth_agent` | Observer (advisory only — never blocks). Scores user-AI collaboration pattern |
| 5 | `claim_ref_alignment_audit_agent` | Opt-in claim faithfulness auditor (v3.8). Audits citation-claim alignment |

## Pipeline Stages (10)

| Stage | Name | Skill Called | Notes |
|-------|------|-------------|-------|
| 1 | RESEARCH | `deep-research` | socratic/full/quick modes |
| 2 | WRITE | `academic-paper` | plan/full modes |
| 2.5 | INTEGRITY | `integrity_verification_agent` | Pre-review. Must PASS (max 3 rounds) |
| 3 | REVIEW | `academic-paper-reviewer` | Full 5-reviewer panel + DA |
| 4 | REVISE | `academic-paper` (revision) | Revised draft + Response to Reviewers |
| 3' | RE-REVIEW | `academic-paper-reviewer` (re-review) | Verification with traceability matrix |
| 4' | RE-REVISE | `academic-paper` (revision) | Second revision (if needed) |
| 4.5 | FINAL INTEGRITY | `integrity_verification_agent` | Must PASS with zero issues |
| 5 | FINALIZE | `academic-paper` (format-convert) | MD → DOCX → LaTeX → PDF |
| 6 | PROCESS SUMMARY | orchestrator | Process record (bilingual) |

## State Machine

```
Stage 1 RESEARCH -> confirm -> Stage 2 WRITE -> confirm -> Stage 2.5 INTEGRITY
  -> PASS -> Stage 3 REVIEW -> Accept -> Stage 4.5
                             -> Minor/Major -> Stage 4 REVISE -> confirm -> Stage 3' RE-REVIEW
                                                               -> Accept/Minor -> Stage 4.5
                                                               -> Major -> Stage 4' RE-REVISE -> confirm -> Stage 4.5
  -> FAIL -> fix & re-verify (max 3 rounds)
Stage 4.5 FINAL INTEGRITY -> PASS -> Stage 5 FINALIZE -> Stage 6 PROCESS SUMMARY
                          -> FAIL -> fix & re-verify
```

### Revision Loop Management
- Max 1 round of RE-REVISE (Stage 4'). If Stage 3' gives Major → Stage 4' → Stage 4.5 (no return to review)
- Early stopping: if delta < 3 points on rubric AND no P0 issues → suggest stopping
- Hard cap: 2 full revision loops (Stage 4 + Stage 4')

### Adaptive Checkpoint System
- FULL: First checkpoint, after integrity boundaries, before finalization
- SLIM: After 2+ consecutive "continue" responses on non-critical stages
- MANDATORY: Integrity FAIL, Review decision, Stage 5 — cannot be skipped
- Awareness guard: after 4 consecutive "continue" → insert FULL checkpoint

### Mid-Entry Protocol
- Can enter from any stage; orchestrator detects available materials
- Mid-entry cannot skip Stage 2.5 (integrity)
- Materials auto-detected: research data → Stage 2, paper draft → Stage 2.5, verified paper → Stage 3, review comments → Stage 4

## Triggers

**English**: academic pipeline, research to paper, full paper workflow, paper pipeline, end-to-end paper, research-to-publication, complete paper workflow

### Does NOT trigger (use individual skills instead)
- Only literature search → `deep-research`
- Only write paper → `academic-paper`
- Only review → `academic-paper-reviewer`
- Only check citations / convert format → `academic-paper` (mode)

## Quality Standards

| Rule | Detail |
|------|--------|
| Mandatory integrity | Stage 2.5 and 4.5 cannot be skipped, must PASS |
| Mandatory checkpoints | User confirmation required after each stage |
| Failure mode checklist | 7-mode AI research failure checklist at Stage 2.5 + 4.5 (blocking) |
| No overstepping | Orchestrator dispatches only; no substantive work |
| No forcing | User can pause/exit anytime (but cannot skip integrity) |
| Convergence-aware | Stop revision loop when converged (delta < 3, no P0) |
| Budget transparency | Token cost estimate + confirmation at pipeline start |

## Anti-Patterns

| Anti-Pattern | Correct Behavior |
|---|---|
| Skipping integrity checks | Integrity checks are MANDATORY — cannot auto-skip |
| Orchestrator doing substantive work | Orchestrator only dispatches and coordinates |
| Auto-advancing past MANDATORY checkpoints | MANDATORY checkpoints require explicit user input |
| Quality degradation across stages | If Stage N output < Stage N-1, PAUSE before continuing |
| Silently dropping reviewer concerns | R&R tracking table accounts for every concern |
| Re-verifying only known issues at Stage 4.5 | Stage 4.5 verifies from scratch — revision may introduce new issues |
| Bypassing failure mode checklist | 7-mode checklist is MANDATORY and BLOCKING; overrides require reasoning |
