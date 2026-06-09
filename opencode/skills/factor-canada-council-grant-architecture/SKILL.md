---
name: factor-canada-council-grant-architecture
description: >-
  Use this skill when the user is working on or asking about FACTOR grants, Canada Council for the Arts funding, Canadian music industry grants, or government funding for music projects.
version: 1.0.0
---

# Skill: FACTOR & Canada Council Grant Architecture
## 📖 1. Overview
Structures R&D roadmaps to align with Canadian funding (FACTOR, Canada Council, Ontario Creates) for non-dilutive cultural/tech grants.
## ⚙️ 2. Core Functionality
- Eligibility Mapping: Project scope, budget, cultural impact alignment
- Milestone Tracking: Deliverable documentation, timeline adherence
- Financial Reporting: Expense categorization, audit readiness
- Compliance Automation: Form generation, submission scheduling
## 📥📤 3. Input/Output Schema
| Inputs | Project plan, budgets, grant guidelines | Outputs | Application drafts, progress reports, compliance logs |
## 🏗️ 4. Architecture
Map project tasks to grant criteria. Track hours/expenses in Git/Jira. Auto-generate PDF reports matching FACTOR templates.
## 🔗 5. Dependencies
`FACTOR Guidelines`, `Canada Council Portal`, `LaTeX/PDF gen`
## ⚠️ 6. Edge Cases
| Scope Creep | Ineligible expenses | Freeze budget changes, pre-approve |
| Deadline Miss | Application rejected | Automated calendar alerts, buffer weeks |
| Audit Failure | Clawback risk | Maintain receipt logs, separate grant accounts |
## 🛡️ 7. Constraints
- Compliance: 100% guideline match
- Documentation: Audit-ready at all times
- Transparency: Clear public benefit mapping
## 🤖 8. Usage
- *Prompt:* "Generate a grant tracking system that maps Jira tasks to FACTOR eligibility criteria and auto-generates progress reports."
## 🧪 9. Testing
- Guideline compliance check
- Audit trail simulation
- Budget allocation validation
## 📝 10. Best Practices
- Document cultural impact explicitly
- Separate grant funds in accounting
- Submit interim reports proactively
*Skill Version: 1.0.0 | Standards: FACTOR, Canada Council, Grant Mgmt | Domain: Canadian Music Infrastructure*