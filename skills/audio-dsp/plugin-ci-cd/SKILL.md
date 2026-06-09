---
name: plugin-ci-cd
description: "Use this skill when the user is working on or asking about CI/CD for audio plugins, GitHub Actions matrix builds for Windows/Mac/Linux, code signing, notarization, plugin validation, PDB symbol management, or automated release pipelines for CLAP/VST3/AAX/AU plugins."
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Plugin Ci Cd", "opencode-migrated"]
    related_skills: []
---


# Skill: Audio Plugin CI/CD Pipeline

## 1. Overview
Covers automated build, test, validate, sign, and release pipelines for audio plugins across Windows (CLAP/VST3), macOS (AU/VST3), and Linux (CLAP/VST3). Designed for matrix builds with artifact collection, pluginval/auval validation, and notarized installer generation.

## 2. Core Functionality
- **Matrix Builds:** GitHub Actions matrix for `{os: [windows, macos, ubuntu], arch: [x86_64, arm64], config: [Debug, Release]}`
- **Signing & Notarization:** Windows Authenticode (Azure Key Vault / `signtool`), macOS `codesign` + `notarytool` + stapling, Linux no signing
- **Plugin Validation:** `pluginval` (JUCE — VST3/AU validation), `auval` (macOS AudioUnit), CLAP validator (`clap-validator`), `validateplugin` (AAX)
- **Installer Generation:** CPack for cross-platform, `Inno Setup` (Windows .exe), `pkgbuild` (macOS .pkg), `dpkg`/`AppImage` (Linux)
- **Artifact Management:** GitHub Actions artifacts for build artifacts, PDB/dSYM for debugging, symbols in `_symbols` folder
- **Release Automation:** GitHub Releases with changelog via `git-cliff` / `release-please`, semantic versioning
- **Testing:** CTest integration, audio regression tests (reference WAV comparison), sanitizer runs (ASan/UBSan)
- **Dependency Cache:** `ccache` (C++) and `FetchContent` path caching across workflow runs

## 3. Input/Output Schema
| Inputs | Source repo, git tag/sha, signing certificates (secrets), runner OS image |
| Outputs | Signed installers (.exe/.pkg/.deb/.AppImage), symbols (.pdb/.dSYM), validation report |
| Platforms | `windows-2025`, `macos-15` (arm64 + x86_64), `ubuntu-24.04` |

## 4. Architecture
A CI pipeline has sequential stages: (1) **configure** — CMake with preset, caching, SDK fetch → (2) **build** — matrix by config and arch → (3) **test** — CTest + pluginval → (4) **package** — CPack/Inno/pkgbuild → (5) **sign** — code signing + notarize → (6) **release** — GitHub Release + upload artifacts.

## 5. Dependencies
GitHub Actions (or GitLab CI / Jenkins), `ccache`, `cmake`, `ninja`, `pluginval` (v1.0.0+), `clap-validator`, `signtool` (Windows SDK), `Xcode` + `Developer ID Application` cert (macOS), `jq`, `curl`, `git-cliff`

## 6. Edge Cases
| Notarization Fail | Apple notary server timeout | Retry with `--wait` and exponential backoff |
| Cert Expired | Dev ID certificate expired | Add `codesign --verify --strict` check, alert on rotation |
| AAX Build | Requires PACE/iLok SDK | Private repo, license-restricted; conditionally skip in open source |
| pluginval Crash | Plugin crashes during validation | Capture minidump on Windows, enable `/DEBUG` symbols |
| Cross-Arch macOS | x86_64 build on arm64 runner | Use Rosetta: `arch -x86_64 cmake ...` and `universal2` lipo |

## 7. Constraints
- macOS signing requires a physical Apple device (not GitHub macOS runners if restricted — use self-hosted or Mac Stadium)
- AAX validation requires Pro Tools installed (not available on CI runners — skip or use self-hosted)
- `pluginval` tests must run headless: `--strictness-level 5 --timeout-ms 30000`
- Windows ARM is currently experimental for most DAWs — skip if CLAP only
- Code signing keys must be stored in GitHub secrets (never in source)

## 8. Usage
- *Prompt:* "Create a GitHub Actions workflow that builds, signs, and notarizes my plugin for Win/Mac/Linux on tag push."
- *Prompt:* "Add pluginval validation to the CI pipeline with strictness level 5."
- *Prompt:* "Set up ccache and intelligent SDK caching to speed up matrix builds."

## 9. Testing
- Trigger a tag build and verify all 3 platform artifacts are generated
- Run `pluginval --validate-in-process /path/to/plugin.vst3` manually on each artifact
- Check `codesign -dv /path/to/AU.component` for signing status
- `spctl --assess --verbose /path/to/plugin.app` for macOS Gatekeeper

## 10. Best Practices
- Cache `~/.ccache` and `_deps` separately with per-OS keys + fallback to global cache
- Use `CMAKE_BUILD_TYPE: Release` for distributable artifacts, `Debug` for CI-only symbol generation
- Always validate before signing — caught issues are cheaper to fix pre-signing
- Set `pluginval --output-on-failure` for actionable CI logs
- Version release artifacts as `{name}-{version}-{os}-{arch}.{ext}`
- Use `soft-serve` or `Nix` for reproducible build environments across developers and CI
*Skill Version: 1.0.0 | Standards: GitHub Actions, pluginval 1.x, CMake | Domain: DevOps for Audio*
