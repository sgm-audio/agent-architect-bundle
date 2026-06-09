---
name: permissive-vs-copyleft-licensing-strategy
description: >-
  Use this skill when the user is working on or asking about MIT vs GPL, open source licensing strategy, choosing a license, copyleft vs permissive for audio software, or dual licensing.
version: 1.0.0
---

# Skill: Permissive vs. Copyleft Licensing Strategy
## 📖 1. Overview
Navigates open-source licenses (MIT, Apache 2.0, GPLv3, LGPL) to legally combine third-party libraries with proprietary commercial DSP code.
## ⚙️ 2. Core Functionality
- License Compatibility Matrix: Mapping dependencies to allowed usage
- Static vs Dynamic Linking: LGPL compliance strategies
- SPDX Identifier Tracking: Automated SBOM generation
- Commercial Waiver Negotiation: Dual-licensing paths
## 📥📤 3. Input/Output Schema
| Inputs | Dependency tree, license texts, commercial targets | Outputs | SBOM report, compliance status, risk matrix |
## 🏗️ 4. Architecture
`license-compliance-checker` scans `CMakeLists.txt`/`package.json`. Cross-references with SPDX database. Flags copyleft conflicts pre-build.
## 🔗 5. Dependencies
`syft`, `spdx-sbom-generator`, `FOSSA`/`Snyk`
## ⚠️ 6. Edge Cases
| Copyleft Contagion | Forced open-sourcing | Isolate via plugin boundary, dynamic linking |
| License Versioning | GPLv2 vs GPLv3 mismatch | Lock dependency versions, audit annually |
| Patent Clauses | Apache 2.0 patent retaliation | Document, seek legal counsel for commercial use |
## 🛡️ 7. Constraints
- Compliance: 100% audit-ready
- Risk: Zero critical conflicts in release
- Documentation: Clear license notices in `About` dialog
## 🤖 8. Usage
- *Prompt:* "Generate a compliance report script that scans CMake dependencies, maps to SPDX, and flags GPLv3 contamination in a proprietary build."
## 🧪 9. Testing
- SBOM validation against dependency tree
- Legal review simulation
- Build pipeline gating on license failures
## 📝 10. Best Practices
- Prefer MIT/Apache 2.0 for DSP libs
- Document license exceptions clearly
- Run compliance check on every PR
*Skill Version: 1.0.0 | Standards: SPDX, GPLv3, MIT, Apache 2.0 | Domain: Opencode Architecture*