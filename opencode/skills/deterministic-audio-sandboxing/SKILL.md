---
name: deterministic-audio-sandboxing
description: >-
  Use this skill when the user is working on or asking about audio sandboxing, deterministic audio processing, reproducible plugin output, or isolating plugin state.
version: 1.0.0
---

# Skill: Deterministic Audio Sandboxing
## 📖 1. Overview
Designs secure execution environments (WASM/isolated processes) to run third-party DSP scripts safely inside host applications without compromising stability or security.
## ⚙️ 2. Core Functionality
- WASM Isolation: Linear memory, no syscalls, limited imports
- Process Sandboxing: Seccomp filters, namespace isolation, resource caps
- API Boundaries: Whitelisted DSP functions only
- Timeout & Kill: Hard limits on execution time/memory
## 📥📤 3. Input/Output Schema
| Inputs | User scripts, sandbox config, resource limits | Outputs | Processed audio, sandbox logs, violation alerts |
## 🏗️ 4. Architecture
Load WASM via `wasmtime`. Restrict imports to `audio_process`, `get_param`. Spawn Linux process with `unshare`, `cgroups`, `seccomp`. Monitor via watchdog.
## 🔗 5. Dependencies
`wasmtime`, `libseccomp`, `cgroups`, `Docker`/`Firejail`
## ⚠️ 6. Edge Cases
| Escape Attempt | Host compromise | Strict syscall filter, WASM no-mem-export |
| Resource Exhaustion | DAW crash | Cgroup limits, OOM killer integration |
| Timeout | Infinite loop | Hard kill after 100ms, log failure |
## 🛡️ 7. Constraints
- Latency: < 1ms overhead
- Security: Zero host access
- Reliability: 100% isolation guarantee
## 🤖 8. Usage
- *Prompt:* "Generate a wasmtime sandbox config with restricted imports, cgroup limits, and seccomp filter for safe user DSP execution."
## 🧪 9. Testing
- Escape attempt simulation
- Resource limit stress
- Timeout validation
## 📝 10. Best Practices
- Deny by default, allow explicitly
- Log all sandbox violations
- Provide user feedback on failure
*Skill Version: 1.0.0 | Standards: WASM, Seccomp, Cgroups | Domain: Opencode Architecture*