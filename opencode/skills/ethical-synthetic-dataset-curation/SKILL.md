---
name: ethical-synthetic-dataset-curation
description: >-
  Use this skill when the user is working on or asking about synthetic audio dataset curation, ethical training data for music AI, data provenance, or building compliant audio datasets.
version: 1.0.0
---

# Skill: Ethical Synthetic Dataset Curation
## 📖 1. Overview
Builds legally cleared, high-quality audio datasets for training ML models without copyright infringement.
## ⚙️ 2. Core Functionality
- Source Selection: Public domain, Creative Commons, commissioned sessions
- License Verification: Automated metadata scraping, contract tracking
- Quality Filtering: SNR > 40dB, no clipping, phase-coherent
- Synthetic Augmentation: DSP transformations preserving musical intent
## 📥📤 3. Input/Output Schema
| Inputs | Raw audio, license docs, QC thresholds | Outputs | Clean dataset, metadata JSON, audit logs |
## 🏗️ 4. Architecture
Pipeline: `scrape → verify_license → analyze_quality → augment → split → index`. Store in Git LFS/IPFS with SHA256 checksums.
## 🔗 5. Dependencies
`audiostream`, `mutagen`, `librosa`, `hashlib`
## ⚠️ 6. Edge Cases
| Hidden Copyright | Legal risk | Cross-reference ISRC, use content ID API |
| Low Quality | Model degradation | Reject if RMS < -30dBFS or > 0.1% clipping |
| Bias Overrepresentation | Skewed model | Stratified sampling by genre/instrument |
## 🛡️ 7. Constraints
- Legal: 100% auditable licenses
- Quality: > 95% pass rate on QC
- Scale: 10TB+ manageable
## 🤖 8. Usage
- *Prompt:* "Generate a Python script that filters WAVs for SNR > 40dB, checks metadata, and logs audit trails for synthetic dataset creation."
## 🧪 9. Testing
- License audit spot-check
- Model training stability with curated vs raw
- Bias metric analysis
## 📝 10. Best Practices
- Store license text alongside audio hash
- Use `CC0` or `MIT Audio` when possible
- Document augmentation pipeline transparently
*Skill Version: 1.0.0 | Standards: CC0, SNR, Audit Logging | Domain: Audio AI & ML*