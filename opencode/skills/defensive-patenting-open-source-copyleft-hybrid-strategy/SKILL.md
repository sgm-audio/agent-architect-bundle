---
name: defensive-patenting-open-source-copyleft-hybrid-strategy
description: >-
  Use this skill when the user is working on or asking about patent strategy, defensive patents, copyleft licensing, GPL/AGPL strategy, or hybrid open-source/proprietary IP strategy.
version: 1.0.0
---

# Skill: Defensive Patenting & Open-Source Copyleft Hybrid Strategy
## 📖 1. Overview
Protects core DSP algorithms via provisional patents while open-sourcing UI/integration libs to build trust and ecosystem.
## ⚙️ 2. Core Functionality
- Novelty Search: Prior art validation, patentability assessment
- Provisional Filing: Draft specs, claims, diagrams
- Dual Licensing: Core proprietary, UI/SDK open-source
- Community Engagement: Contributor agreements, CLA
## 📥📤 3. Input/Output Schema
| Inputs | Algorithm specs, prior art, license templates | Outputs | Patent drafts, open-source repos, CLA agreements |
## 🏗️ 4. Architecture
Patent attorney drafts → provisional filing. Open-source UI under MIT. Core DSP under commercial license. Enforce CLA for contributions.
## 🔗 5. Dependencies
`USPTO/CIPO Guidelines`, `CLA Assistant`, `GitHub Licensing`
## ⚠️ 6. Edge Cases
| Infringement Claim | Legal risk | Prior art defense, modify claims |
| License Violation | IP leak | Automated SBOM scan, legal notices |
| Contributor Conflict | Ownership dispute | Require signed CLA before merge |
## 🛡️ 7. Constraints
- Protection: Strong patent claims
- Trust: Transparent open-source
- Compliance: Clear licensing boundaries
## 🤖 8. Usage
- *Prompt:* "Generate a dual-licensing strategy that patents core DSP algorithms while open-sourcing UI components under MIT with CLA enforcement."
## 🧪 9. Testing
- Prior art search validation
- License compliance audit
- CLA signing workflow test
## 📝 10. Best Practices
- File provisional within 12 months of disclosure
- Clearly separate proprietary/open repos
- Require CLA for all external PRs
*Skill Version: 1.0.0 | Standards: USPTO/CIPO, MIT, CLA | Domain: Solo-Founder AI-Ops*