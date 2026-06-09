---
name: plugin-quality-gates
description: "Real hooks/guards for C++ CMake CLAP/ARA audio plugins + Python ONNX export pipeline. Pre-commit hooks, RT-safety grep, format/lint gates, build guard, ONNX smoke test. Not aspirational boilerplate — actual scripts that go in the project."
version: 1.0.0
author: SGM Studios
license: MIT
tags: [hooks, quality-gates, cmake, clap, onnx, rt-safety, ci]
---

# Plugin Quality Gates — Real Hooks for C++ Audio Plugin Projects

## The Stack These Fit

- **C++ Plugins**: CMake + clang-cl/clang, CLAP/ARA/VST3, JUCE optional
- **Python ML**: PyTorch → ONNX → INT8 quantization
- **Build**: `cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build --parallel`
- **Host**: Windows (clang-cl), macOS, Linux (GCC/Clang)

## Files to Generate

Place in `scripts/` at project root:

### 1. `run-checks.sh` / `run-checks.py` — One-shot quality gate

Runs ALL checks, exits non-zero on any failure. Pipeline:

1. **CMake configure + build (Release)** — fail on warnings (`-Werror` / `/WX`)
2. **clang-format** — `cmake --build build --target clang-format`
3. **RT-Safety grep** — scan `src/` for malloc/free/new/delete/mutex/sleep/printf in audio thread code
4. **CTest** — `ctest --test-dir build --output-on-failure`
5. **ONNX export smoke test** — run export script with `--verify` flag
6. **(optional) clang-tidy** — `cmake --build build --target clang-tidy`

### 2. `rt-safety.sh` / `rt-safety.bat` — Real-time safety audit

Greps for forbidden calls, excludes whitelisted patterns:
- `thread_local` (allowed — pre-allocated per-thread)
- `// RT-SAFE` or `// NOLINT` comments (false-positive marker)
- `std::make_unique` + `.release()` (C-ABI lifetime pattern)
- `deferred_*` (cleanup on main thread, not audio thread)

### 3. `pre-commit` — Git hook

Runs clang-format, RT-safety, build, and tests on commit.
ONNX export is optional via `PRE_COMMIT_FULL=1` (slow).

Install: `cp scripts/pre-commit .git/hooks/ && chmod +x .git/hooks/pre-commit`

## RT-Safety Check Pattern

```bash
grep -rn \
    --include="*.cpp" --include="*.h" \
    -e 'malloc(' -e 'free(' -e '\bnew\b' -e '\bdelete\b' \
    -e 'std::mutex' -e 'sleep(' -e 'printf(' -e 'fopen(' \
    src/ \
    | grep -v 'thread_local\|// RT-SAFE\|// NOLINT\|std::make_unique\|\.release()\|deferred_'
```

## Key Principles

- **Deterministic, not advisory** — scripts exit non-zero, block CI/commit
- **Works with existing build system** — reuses CMake targets, not a parallel toolchain
- **Fast path for commits** — pre-commit skips ONNX export (slow); CI runs full set
- **Cross-platform** — Windows uses `run-checks.py` (Python), Unix uses `.sh`
- **False-positive handling** — explicit comment markers (`// RT-SAFE`, `// NOLINT`) so devs can annotate intentional violations
