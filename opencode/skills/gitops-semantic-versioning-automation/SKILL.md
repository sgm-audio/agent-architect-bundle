---
name: gitops-semantic-versioning-automation
description: >-
  Use this skill when the user is working on or asking about GitOps, semantic versioning, automated releases, conventional commits, changelog generation, or semver for audio plugin releases.
version: 1.0.0
---

# Skill: GitOps & Semantic Versioning Automation
## 📖 1. Overview
Automates releases via commit parsing, changelog generation, version tagging, and package distribution using Conventional Commits.
## ⚙️ 2. Core Functionality
- Commit Parsing: `feat`, `fix`, `chore` → version bump (MAJOR.MINOR.PATCH)
- Changelog Gen: Markdown from git log
- Artifact Push: GitHub Releases, package managers
- Rollback Strategy: Git tag revert, binary archive
## 📥📤 3. Input/Output Schema
| Inputs | Git history, release templates, CI tokens | Outputs | Version tags, changelogs, published binaries |
## 🏗️ 4. Architecture
`conventional-changelog` CLI + `git tag`. GitHub Actions triggers on `main` merge. Upload to `releases/` + `apt/brew` repos.
## 🔗 5. Dependencies
`semantic-release`, `conventional-changelog`, `GitHub CLI`
## ⚠️ 6. Edge Cases
| Version Conflict | Duplicate tags | Enforce strict bump rules, lock version file |
| Broken Changelog | Missing context | Require PR descriptions, validate template |
| Failed Push | Manual intervention | Rollback tag, retry with clean state |
## 🛡️ 7. Constraints
- Accuracy: 100% version compliance
- Speed: < 5 mins release pipeline
- Traceability: Every binary linked to commit SHA
## 🤖 8. Usage
- *Prompt:* "Generate a GitHub Actions workflow that parses conventional commits, bumps semver, generates changelog, and publishes to GitHub Releases."
## 🧪 9. Testing
- Dry-run release validation
- Changelog accuracy spot-check
- Rollback simulation
## 📝 10. Best Practices
- Require PRs for `main`
- Use `package.json`/`CMakeLists.txt` version sync
- Automate asset checksums (SHA256)
*Skill Version: 1.0.0 | Standards: SemVer, Conventional Commits, GitOps | Domain: Opencode Architecture*