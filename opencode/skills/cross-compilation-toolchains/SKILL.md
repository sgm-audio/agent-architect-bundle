---
name: cross-compilation-toolchains
description: >-
  Use this skill when the user is working on or asking about cross-compiling audio plugins, targeting ARM from x86, sysroots, CMake toolchain files, or multi-platform plugin builds.
version: 1.0.0
---

# Skill: Cross-Compilation Toolchains
## 📖 1. Overview
Configures Linux build servers to cross-compile binaries for Apple Silicon (macOS), x86 (Windows), ARM64 (Linux/RPi) via `osxcross`, `mingw`, `aarch64`.
## ⚙️ 2. Core Functionality
- Target SDK Setup: macOS SDK extraction, Windows MinGW, ARM sysroot
- CMake Toolchain Files: Platform-specific flags, cross-linkers
- CI Integration: Matrix builds, artifact upload
- Testing: QEMU emulation, remote device flashing
## 📥📤 3. Input/Output Schema
| Inputs | Source code, SDK archives, CMake toolchains | Outputs | Cross-platform binaries, debug symbols, test logs |
## 🏗️ 4. Architecture
Docker image with `osxcross`, `mingw-w64`, `gcc-aarch64-linux-gnu`. CMake `-DCMAKE_SYSTEM_NAME=Darwin/Windows/Linux`. Build in parallel, upload artifacts.
## 🔗 5. Dependencies
`Docker`, `osxcross`, `mingw`, `CMake`, `QEMU`
## ⚠️ 6. Edge Cases
| SDK Licensing | macOS SDK redistribution | Use official Apple SDKs, document EULA |
| Linker Errors | Missing symbols | Verify sysroot, static vs dynamic linking |
| Architecture Mismatch | Wrong binary output | Validate `file` command post-build |
## 🛡️ 7. Constraints
- Build Time: < 30 mins per target
- Accuracy: 100% architecture match
- Size: Optimized binaries via `-Os`/`-O3`
## 🤖 8. Usage
- *Prompt:* "Generate a Dockerfile with osxcross and mingw for cross-compiling JUCE plugins to macOS ARM64 and Windows x64."
## 🧪 9. Testing
- `file` architecture verification
- QEMU smoke test
- Symbol stripping validation
## 📝 10. Best Practices
- Cache SDKs and toolchains
- Use `ccache` for speed
- Document cross-build steps in `README`
*Skill Version: 1.0.0 | Standards: CMake, osxcross, mingw, Docker | Domain: Opencode Architecture*