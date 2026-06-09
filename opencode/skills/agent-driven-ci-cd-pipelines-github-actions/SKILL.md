---
name: agent-driven-ci-cd-pipelines-github-actions
description: >-
  Use this skill when the user is working on or asking about AI-driven CI/CD, GitHub Actions for audio plugins, automated plugin builds, or agentic DevOps pipelines.
version: 1.0.0
---

# Skill: Agent-Driven CI/CD Pipelines (GitHub Actions)
## 📖 1. Overview
Builds AI-managed CI/CD that compiles, signs, notarizes, and distributes audio plugins securely across platforms.
## ⚙️ 2. Core Functionality
- Matrix Builds: macOS/Windows/Linux × VST3/AU/CLAP/AAX
- Code Signing: macOS Hardened Runtime + Notarization, Windows Authenticode
- AI Agent Integration: Automated changelog, release notes, PR triage
- Secure Secrets: Keychain/SignTool isolation, no plaintext certs
## 📥📤 3. Input/Output Schema
| Inputs | Git commit, signing certs, distribution tokens, AI prompts | Outputs | Signed installers, notarized binaries, GitHub Releases, AI changelog |
## 🏗️ 4. Architecture
GitHub Actions workflow: `build → sign → notarize → upload → AI_release_draft`. Use `actions/checkout`, `macos-codesign`, `signtool`, `openapi-generator` for changelog.
## 🔗 5. Dependencies
`GitHub Actions`, `codesign`, `signtool`, `notarytool`, `release-drafter`
## ⚠️ 6. Edge Cases
| Notarization Rejection | Gatekeeper block | Fix hardened runtime entitlements, resubmit |
| Cert Expiration | Build failure | Alert 30 days prior, auto-renewal pipeline |
| Secret Leakage | Security breach | Use OIDC, never store p12/pfx in repo |
## 🛡️ 7. Constraints
- Build Time: < 45 mins full matrix
- Security: 0 secrets in logs
- Compliance: GDPR/PIPEDA telemetry opt-in by default
## 🤖 8. Usage
- *Prompt:* "Generate a GitHub Actions workflow that builds JUCE plugins, signs with Authenticode, notarizes for macOS, and drafts an AI-generated release."
## 🧪 9. Testing
- Sandbox build validation
- Signature verification (`codesign -vv`)
- Notarization status polling
## 📝 10. Best Practices
- Pin runner versions
- Use OIDC for signing
- Cache compiler toolchains
- Automate release tagging
*Skill Version: 1.0.0 | Standards: GitHub Actions, Codesign, NotaryTool | Domain: Opencode Architecture*