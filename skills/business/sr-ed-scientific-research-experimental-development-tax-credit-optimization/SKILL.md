---
name: sr-ed-scientific-research-experimental-development-tax-credit-optimization
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Sr Ed Scientific Research Experimental Development Tax Credit Optimization", "opencode-migrated"]
    related_skills: []
---


# Skill: SR&ED (Scientific Research & Experimental Development) Tax Credit Optimization
## 📖 1. Overview
Documents technical uncertainties, experiments, and hours in Git logs to claim Canada’s SR&ED refunds (up to 64% of R&D wages).
## ⚙️ 2. Core Functionality
- Uncertainty Mapping: Identify technological unknowns, document hypotheses
- Experiment Tracking: Method, results, iterations, conclusions
- Time Allocation: Git commit timestamps linked to SR&ED tasks
- Report Generation: Automated T661 form drafting
## 📥📤 3. Input/Output Schema
| Inputs | Git history, technical docs, experiment logs | Outputs | SR&ED reports, T661 drafts, audit trails |
## 🏗️ 4. Architecture
Parse Git logs for `SR&ED` tags. Map commits to project uncertainties. Generate chronological narrative. Export to accountant format.
## 🔗 5. Dependencies
`Git`, `T661 Guidelines`, `Markdown/PDF gen`
## ⚠️ 6. Edge Cases
| Insufficient Documentation | Claim rejection | Enforce commit message standards, weekly logs |
| Commercial Development | Ineligible | Separate R&D from production tasks |
| Audit Failure | Penalty risk | Maintain raw experiment logs, version control |
## 🛡️ 7. Constraints
- Compliance: 100% CRA guidelines
- Documentation: Real-time logging
- Accuracy: No fabricated experiments
## 🤖 8. Usage
- *Prompt:* "Generate a Git hook that prompts for SR&ED uncertainty tags and experiment results on each commit to R&D branches."
## 🧪 9. Testing
- CRA guideline compliance check
- Log completeness audit
- Export format validation
## 📝 10. Best Practices
- Tag commits with `#SR&ED`
- Document failures as valuable results
- Review quarterly with accountant
*Skill Version: 1.0.0 | Standards: CRA SR&ED, T661, Git | Domain: Solo-Founder AI-Ops*