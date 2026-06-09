---
name: rocm-on-igpu
description: Use this skill when the user is working on or asking about AMD ROCm on integrated GPUs, iGPU acceleration for ML inference, ROCm on APUs (Ryzen AI, Phoenix, Hawk Point, Strix Point), or HIP programming for integrated graphics.
version: 1.0.0
---

# Skill: ROCm on iGPU

## 1. Overview
Covers deploying AMD ROCm on integrated GPUs (iGPUs) found in AMD APUs — Ryzen AI 300 series (Strix Point), Ryzen 7040/8040 (Phoenix/Hawk Point), and older Cezanne/Lucienne. Focuses on ROCm kernel compatibility, memory pressure management (shared DRAM vs. dedicated VRAM), and practical ML inference on consumer hardware without a discrete GPU.

## 2. Core Functionality
- **iGPU Detection:** `rocminfo` output parsing, identifying gfx1030/gfx1100/gfx1150 targets
- **ROCm Install on iGPU:** `amdgpu-full` vs `amdgpu-pro` drivers, kernel mode-setting, IOMMU groups
- **HIP Programming:** Porting CUDA kernels to HIP for iGPU execution, warp size (64 vs 32), local data share usage
- **Memory Constraints:** Unified memory architecture (UMA) — total system RAM shared with GPU, `hipMalloc` vs `hipHostMalloc`, avoiding OOM
- **Inference Optimization:** ROCm-compatible ONNX Runtime, MIGraphX, TensorFlow ROCm on iGPU, vLLM with NPD backend
- **Performance Tuning:** Wavefront occupancy, L1/L2 cache pressure, avoiding register spilling, using `hipcc` optimization flags
- **ROCm Components:** HIP runtime, ROCclr, ROCr, ROCKernel drivers, MIOpen, rocBLAS, rocThrust, RCCL

## 3. Input/Output Schema
| Inputs | `rocminfo` output, GPU architecture string, model size (params), batch size, DRAM capacity |
| Outputs | Supported ROCm version, max model size, recommended kernel config, expected tokens/sec |
| Config | `HSA_OVERRIDE_GFX_VERSION`, `GPU_MAX_HW_QUEUES`, `HIP_VISIBLE_DEVICES` |

## 4. Architecture
iGPU memory is a contiguous slice of system RAM (typically 512MB–8GB configurable via BIOS/UMA Frame Buffer). ROCm uses the `amdgpu` kernel driver with `amdkfd` for compute dispatch. Pointer chasing and shared memory patterns differ from dGPUs — the iGPU competes with CPU for memory bandwidth (DDR5/LPDDR5).

## 5. Dependencies
`rocm-smi`, `rocminfo`, `hipcc`, `hipRuntime`, `MIOpen`, `rocBLAS`, `ROCm 5.7+` / `ROCm 6.x`, Linux kernel 6.x with `amdgpu` driver

## 6. Edge Cases
| Unsupportable iGPU | Older GCN (gfx803/gfx900) | Install `rocm-5.7.3` max; ROCm 6.x drops GCN |
| IOMMU Groups | Broken DMA on consumer boards | `iommu=soft` or `amd_iommu=off` kernel params |
| Shared Memory OOM | Model too large for UMA buffer | `hipHostMalloc` with `hipHostMallocNonCoherent` flag |
| ROCm Missing Device | `hipGetDeviceCount` returns 0 | Check driver: `dkms install amdgpu`, reboot, verify `kfd` loaded |

## 7. Constraints
- Max model size ≈ (UMA buffer size — OS reservation) / model weight size (FP16)
- Typical inference: 2–7B param LLMs at 4-bit, 7–13B at 2-bit (GPTQ/AWQ)
- Windows ROCm support is limited — prefer Linux (Ubuntu 22.04+, Arch, or Fedora)
- `gfx1030` (RDNA 2) lacks `dot2` / `dot3` instructions; `gfx1100+` (RDNA 3) has them
- ROCm 6.2+ adds partial support for Strix Point (`gfx1150`)

## 8. Usage
- *Prompt:* "I have a Ryzen 7 8840U (Phoenix iGPU). Install ROCm and run Llama 3.2 8B Q4_K_M on it."
- *Prompt:* "Convert this CUDA kernel to HIP for my AMD iGPU."
- *Prompt:* "My Strix Point iGPU OOMs with a 7B model — how to optimize memory usage?"

## 9. Testing
- Run `rocminfo` to confirm device enumeration
- `hipInfo` to verify memory pool and compute capability
- `rocm-smi --showmeminfo` for current UMA usage
- Inference benchmark: `llama.cpp` with `--no-kvcache` on iGPU

## 10. Best Practices
- Set `HSA_OVERRIDE_GFX_VERSION=<target>` only for unsupported but compatible iGPUs
- Use `hipMallocManaged` for transparent CPU/GPU page migration
- Prefer 4-bit quantization for models >3B params on iGPU
- Set `GPU_MAX_HEAP_SIZE=80%` of UMA buffer in environment
- For ROCm 6.x, install `rocm-hip-libraries` metapackage, not `rocm-dkms` alone
*Skill Version: 1.0.0 | Standards: ROCm 6.x, HIP 5.7+ | Domain: ML Inference on APUs*
