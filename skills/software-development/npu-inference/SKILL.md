---
name: npu-inference
description: "Use this skill when the user is working on or asking about NPU inference, Neural Processing Units for local ML, ONNX Runtime NPU execution, Intel NPU, AMD Ryzen AI NPU (XDNA), Qualcomm Hexagon NPU, Apple Neural Engine, or dedicated NPU acceleration for audio/ML models."
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Npu Inference", "opencode-migrated"]
    related_skills: []
---


# Skill: NPU Inference

## 1. Overview
Covers inference on Neural Processing Units (NPUs) — specialized AI accelerators integrated into modern CPUs and SoCs. Focuses on ONNX Runtime with NPU execution providers (EPs), model compilation for NPU ISA, memory and data-movement constraints, and practical integration into audio plugins and local inference pipelines.

## 2. Core Functionality
- **NPU Detection:** Identifying available NPUs via OS/driver APIs (Windows `Get-PnpDevice` / ComputeAccelerator class for AMD, `coreai-enumerate` for Intel; Linux `libnpu`; macOS `ANE`)
- **NPU ≠ GPU expectation-set:** NPUs are NOT general-purpose compute. They only run models compiled offline to their ISA, delivered through a vendor-specific ONNX Runtime EP. Nothing uses them by default — zero consumer apps, no browser, no DAW.
- **ONNX Runtime NPU Execution Providers:** Intel OpenVINO EP, AMD Ryzen AI EP (Vitis AI), Qualcomm QNN EP, Apple CoreML EP
- **Model Compilation:** Converting ONNX/Pytorch to NPU-specific format (`.xmodel`, `.blob`, `.mlmodelc`, `.cmx`)
- **Audio-Specific Inference:** Real-time audio classification, source separation, denoising on NPU with `block_size` / `hop_size` alignment
- **Memory Management:** NPU-local SRAM constraints, DMA transfer scheduling, zero-copy buffers via `iommu`
- **Hybrid CPU/NPU Pipelines:** Pre/post-processing on CPU, inference on NPU, overlap with async dispatch
- **Driver/Firmware:** NPU driver model (Windows WDDM vs Linux kernel `npu` driver), firmware version requirements
- **AMD VitisAI EP Target Selection:** The VitisAI provider has many valid target names auto-discovered at runtime. For Ryzen AI 1.7.1, targets include `X1` (XDNA 1), `X2` (XDNA 2), `PSO`, `PSD`, etc. Ryzen AI 7 350 (Strix Point, XDNA 2) uses **`X2`**. `KRK` is NOT a valid target in 1.7.1. Passing an invalid target logs all valid names as an ERROR-level auto-discovery message. Check `ort.get_available_providers()` first, then iterate valid targets if session creation fails.
- **`session.get_providers()` is NOT a guarantee of NPU usage:** The EP listed first is registration order only. The NPU may be at 0% while ORT silently falls all ops back to CPU. Always verify NPU utilization via Task Manager NPU % or by watching for `F... pass_main.cpp:59] Check failed:` in stderr. A fatal C++ CHECK failure means the NPU EP errored and ORT caught it.
- **Large ONNX graphs (>~10K nodes) hang the VitisAI compiler:** Even with identical ops and opset, graphs over ~25K nodes cause the NPU compiler to enter an infinite loop with 0% NPU utilization. Node count scales linearly with unrolled sequence length. Fix: export a per-sample model (seq_len=1, ~400 nodes) and keep the outer loop in C++ code.
- **Dynamic shape limitation:** The AMD VitisAI EP does NOT support dynamic sequence-length dimensions. Models exported with `dynamic_axes={'input': {1: 'seq_len'}}` will fail with `Check failed: input_shape[i] != -1`. Only the batch dimension can be dynamic. Re-export with fixed sequence length for NPU deployment. Patching ONNX metadata (`dim_value = 256`) is NOT sufficient — graph internals still reference -1.
- **Per-sample vs batched export strategy:** For models with an unrolled time loop (Mamba SSM scan), exporting with `seq_len=1` produces a ~400-node graph that compiles on NPU in ~9s. The outer loop over samples lives in the plugin's C++ code. This trades per-call ORT overhead for NPU-compilability. The batched model (seq_len=64, ~6,500 nodes) compiles in ~6s but fails beyond ~10K nodes. Measure both and pick based on your latency budget. For a 76K-param model, per-sample NPU is 1.07x CPU — marginal — but for larger models the NPU compute advantage will outweigh per-call overhead.
- **Constant-folded parameter reconstruction:** During ONNX export with `do_constant_folding=True`, PyTorch may fold deterministic parameters (zero-initialized FiLM weights/biases, `log_A_real` from `torch.arange` formula, `D=torch.ones`, LayerNorm weight=ones) into constants. These parameters exist only in layer 0 of the ONNX and are absent for layers 1-3. Reconstruct them from their initialization formulas. Always verify 50/50 parameters loaded post-reconstruction.
- **Small model performance parity:** For models under ~500K params, NPU latency ≈ CPU latency because DMA transfer overhead dominates the tiny compute cost. NPU advantage only appears with INT8-quantized or larger (10M+ param) models. Always benchmark before promising NPU speedup on small audio models.
- **⚠️ NPU tinkering is a shipping blocker for small models:** The NPU ecosystem on Windows is immature (conda env required, VitisAI compiler fragile, graph size limits, Quark/MSVC toolchain friction). For a solo developer shipping products, the NPU is a distraction until you have a >10M param INT8 model ready. When the user says "fuck the NPU" or "this is going nowhere" — listen. They're signaling that NPU work is blocking shipping. Pivot to the shippable artifact immediately.
- **INT8 models can be SLOWER on NPU than CPU:** QDQ (QuantizeLinear/DequantizeLinear) nodes inserted by Quark may not be supported by the VitisAI EP, causing mixed CPU/NPU execution. The data marshaling overhead between devices makes total latency worse than pure CPU. Check for `Some nodes were not assigned to the preferred execution providers` warning. Mitigate by excluding MatMul/Gemm from output quantization or disabling CLE/SmoothQuant.

## 3. Input/Output Schema
| Inputs | ONNX model, NPU target name, batch size, input/output tensor shapes, execution provider config |
| Outputs | Inference handle, tensor I/O bindings, latency stats (μs), power usage (mW) |
| Platform | Intel Core Ultra (Meteor Lake/Lunar Lake), AMD Ryzen AI 300 (XDNA 2), Snapdragon X Elite (Hexagon), Apple M-series (ANE) |

## 4. Architecture
NPUs consist of systolic arrays / dataflow units (e.g., AMD XDNA 2's AI Engine array, Intel NPU's NCE). Inference data moves: DDR → NPU SRAM (tile-local) → compute → SRAM → DDR. Tile-level dataflow scheduling is handled by the NPU driver/compiler, not user code. Audio use-cases benefit from NPU's deterministic latency (typically 1–8ms per inference pass).

## 5. Dependencies
`onnxruntime`, `onnxruntime-directml` / `onnxruntime-openvino` / `onnxruntime-vitisai`, Intel NPU driver, AMD NPU driver (IPU 6.x), Qualcomm QNN SDK, Apple CoreML

**AMD XDNA on Windows specifically:** Requires the Ryzen AI Software SDK (installed via AMD installer, lives at `C:\Program Files\RyzenAI\<version>\`). SDK ships as a conda environment (`ryzen-ai-<version>`) — MUST activate it before any NPU work. The conda env contains the patched ONNX Runtime with VitisAI EP, the deployment DLLs (`onnxruntime_providers_ryzenai.dll`, `onnxruntime_vitisai_ep.dll`), and the Quark quantizer for INT8 model prep. See `references/amd-xdna-windows.md` for the full verification and setup workflow.

## 6. Edge Cases
| Session Creation Fail | NPU driver not installed or outdated | `npu-smi` / `coreai-enumerate` to verify |
| Model Compile Fail | Opset not supported on NPU | Fall back CPU EP for unsupported ops, split graph |
| Bandwidth Starved | Large tensor moving to/from NPU | Quantize to INT8, use NHWC layout for NPU fusion |
| Batch=1 Overhead | NPU is bandwidth- rather than compute-limited | Prefer async batching, pipeline multiple inferences |

## 7. Constraints
- NPU SRAM limited: typically 8–64 MB per tile/engine
- Models must be compiled offline for the target NPU ISA (not JIT-compiled like GPU)
- Max supported opset varies by NPU generation (check `npu-smoke-test`)
- Audio real-time use: inference must complete in < block_size / sample_rate seconds
- NPU drivers on Windows are still maturing — prefer Linux for AMD XDNA, Windows for Intel NPU

## 8. Usage
- *Prompt:* "Run a PyTorch denoiser model on the Intel NPU (Meteor Lake) via ONNX Runtime."
- *Prompt:* "Set up AMD Ryzen AI NPU inference for a real-time audio classifier with sub-5ms latency."
- *Prompt:* "Convert a Kaldi ASG model to ONNX and deploy on Qualcomm Hexagon NPU."
- *Prompt:* "How do I benchmark NPU vs CPU vs iGPU for my audio embedding model?"

## 9. Testing
- Intel NPU: `npu-smi`, `coreai-enumerate` (Windows)
- **AMD XDNA Windows:** `Get-PnpDevice | Where-Object Class -eq 'ComputeAccelerator'` to confirm detection. Then run the quicktest (see `references/amd-xdna-windows.md`). Check PCI device IDs: 1022:1502 = Phoenix/Hawk Point, 1022:17F0 rev 00/10/11 = Strix Point, 1022:17F0 rev 20 = Krackan Point.
- Linux AMD: `ls /dev/npu*`, `rocminfo` for iGPU path
- ONNX Runtime session creation with targeted EP: `OrtSessionOptions::AppendExecutionProvider_VitisAI`
- Inference latency: `OrtSession::Run` with `Ort::RunOptions` timing callbacks
- Memory: `coreai-peek-memory` / `npu-smi stats --memory`

## 10. Best Practices
- **ALWAYS lead with expectation-setting** — NPU is NOT a GPU. Nothing uses it by default. The user bought an "AI laptop" expecting magical acceleration. State upfront that NPU only runs compiled INT8 ONNX models through a vendor-specific EP, and requires manual conda env activation + quantized model prep.
- Always set a fallback execution provider (CPU EP) in case NPU session creation fails
- For audio processing, use `OrtSessionOptions::SetInterOpNumThreads(0)` to disable inter-op parallelism
- Prefer INT8 quantized models — NPU dataflow units are optimized for 8-bit integer MATH
- ONNX `GraphOptimizationLevel::ORT_ENABLE_EXTENDED` can fuse ops for NPU efficiency
- Profile with `npu-smi stats --interval 10` to confirm NPU utilization exceeds 70%
- Use `OrtSessionOptions::AppendExecutionProvider_DML` as a simpler alternative for Windows GPU/NPU unified path
- **AMD XDNA specific:** Always activate the `ryzen-ai-<version>` conda env first. Verify EP is actually used with `session.get_providers()`. See `references/amd-xdna-windows.md` for full setup and verification.
*Skill Version: 1.3.0 | Standards: ONNX Runtime 1.18+, NPU Drivers 2024+ | Domain: Local AI Inference*
