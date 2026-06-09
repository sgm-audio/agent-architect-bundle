---
name: simd-vectorization-and-avx-neon-optimization
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Simd Vectorization And Avx Neon Optimization", "opencode-migrated"]
    related_skills: []
---


# Skill: SIMD Vectorization & AVX/NEON Optimization
## 📖 1. Overview
Leverages CPU-specific SIMD instruction sets (AVX/AVX2/AVX-512, NEON, SSE4.1) to process multiple audio samples per clock cycle, maximizing throughput for filters, oscillators, and neural inference while maintaining <10ms latency.
## ⚙️ 2. Core Functionality
- ISA Dispatch: Runtime CPU feature detection (`cpuid`, `getauxval`)
- Vector Math: Parallelized sin/cos, exp, log, fast approximations
- Memory Alignment: 16/32/64-byte buffer alignment for load/store
- Compiler Hints: `#pragma omp simd`, `[[gnu::vector_size]]`, intrinsics fallbacks
## 📥📤 3. Input/Output Schema
| Inputs | `float*` aligned buffers, SIMD width enum, CPU feature flags |
| Outputs | Processed SIMD vectors, performance counters, fallback status |
## 🏗️ 4. Architecture
Implement ISA dispatch table: `void (*process_ptr)(const float* in, float* out, int n);` Initialize via `detect_simd()`. Use aligned allocators: `aligned_alloc(32, size)`. NEON uses `vld1q_f32`, AVX uses `_mm256_load_ps`.
## 🔗 5. Dependencies
`<immintrin.h>`, `<arm_neon.h>`, `cpuinfo` library, `gcc/clang -march=native`
## ⚠️ 6. Edge Cases
| Misaligned Load | Crash on ARM | Use `unaligned_load` fallback or align buffers |
| Denormals | 10x CPU spike | `FTZ/DAZ` CPU flags, `_mm256_setcsr` |
| Compiler Fallback | No auto-vectorization | Explicit intrinsics, `__restrict__` pointers |
## 🛡️ 7. Constraints
- Budget: <50 cycles/sample
- Alignment: 32-byte minimum for AVX, 16 for NEON
- Fallback: Scalar path always compiled
## 🤖 8. Usage
- *Prompt:* "Generate an ISA-dispatched biquad filter using AVX2 intrinsics with NEON fallback."
## 🧪 9. Testing
- `perf stat` cycle counting
- Phase cancellation against scalar reference
- Cross-CPU architecture validation (Intel, AMD, Apple Silicon)
## 📝 10. Best Practices
- Prefer compiler auto-vectorization first, intrinsics second
- Use `std::aligned_allocator` for all DSP buffers
- Document ISA requirements in plugin manifest
*Skill Version: 1.0.0 | Standards: AVX2/AVX-512, NEON, C++20 | Domain: Real-Time Audio*