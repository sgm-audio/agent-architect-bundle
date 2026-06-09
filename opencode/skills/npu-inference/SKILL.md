---
name: npu-inference
description: Use this skill when the user is working on or asking about NPU inference, Neural Processing Units for local ML, ONNX Runtime NPU execution, Intel NPU, AMD Ryzen AI NPU (XDNA), Qualcomm Hexagon NPU, Apple Neural Engine, or dedicated NPU acceleration for audio/ML models.
version: 1.0.0
---

# Skill: NPU Inference

## 1. Overview
Covers inference on Neural Processing Units (NPUs) — specialized AI accelerators integrated into modern CPUs and SoCs. Focuses on ONNX Runtime with NPU execution providers (EPs), model compilation for NPU ISA, memory and data-movement constraints, and practical integration into audio plugins and local inference pipelines.

## 2. Core Functionality
- **NPU Detection:** Identifying available NPUs via OS/driver APIs (Windows `coreai`, Linux `libnpu`, macOS `ANE`)
- **ONNX Runtime NPU Execution Providers:** Intel OpenVINO EP, AMD Ryzen AI EP (Vitis AI), Qualcomm QNN EP, Apple CoreML EP
- **Model Compilation:** Converting ONNX/Pytorch to NPU-specific format (`.xmodel`, `.blob`, `.mlmodelc`, `.cmx`)
- **Audio-Specific Inference:** Real-time audio classification, source separation, denoising on NPU with `block_size` / `hop_size` alignment
- **Memory Management:** NPU-local SRAM constraints, DMA transfer scheduling, zero-copy buffers via `iommu`
- **Hybrid CPU/NPU Pipelines:** Pre/post-processing on CPU, inference on NPU, overlap with async dispatch
- **Driver/Firmware:** NPU driver model (Windows WDDM vs Linux kernel `npu` driver), firmware version requirements

## 3. Input/Output Schema
| Inputs | ONNX model, NPU target name, batch size, input/output tensor shapes, execution provider config |
| Outputs | Inference handle, tensor I/O bindings, latency stats (μs), power usage (mW) |
| Platform | Intel Core Ultra (Meteor Lake/Lunar Lake), AMD Ryzen AI 300 (XDNA 2), Snapdragon X Elite (Hexagon), Apple M-series (ANE) |

## 4. Architecture
NPUs consist of systolic arrays / dataflow units (e.g., AMD XDNA 2's AI Engine array, Intel NPU's NCE). Inference data moves: DDR → NPU SRAM (tile-local) → compute → SRAM → DDR. Tile-level dataflow scheduling is handled by the NPU driver/compiler, not user code. Audio use-cases benefit from NPU's deterministic latency (typically 1–8ms per inference pass).

## 5. Dependencies
`onnxruntime`, `onnxruntime-directml` / `onnxruntime-openvino` / `onnxruntime-vitisai`, Intel NPU driver, AMD NPU driver (IPU 6.x), Qualcomm QNN SDK, Apple CoreML

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
- `npu-smi` (Intel), `coreai-enumerate` (Windows), `ls /dev/npu*` (Linux AMD)
- ONNX Runtime session creation with targeted EP: `OrtSessionOptions::AppendExecutionProvider_VitisAI`
- Inference latency: `OrtSession::Run` with `Ort::RunOptions` timing callbacks
- Memory: `coreai-peek-memory` / `npu-smi stats --memory`

## 10. Best Practices
- Always set a fallback execution provider (CPU EP) in case NPU session creation fails
- For audio processing, use `OrtSessionOptions::SetInterOpNumThreads(0)` to disable inter-op parallelism
- Prefer INT8 quantized models — NPU dataflow units are optimized for 8-bit integer MATH
- ONNX `GraphOptimizationLevel::ORT_ENABLE_EXTENDED` can fuse ops for NPU efficiency
- Profile with `npu-smi stats --interval 10` to confirm NPU utilization exceeds 70%
- Use `OrtSessionOptions::AppendExecutionProvider_DML` as a simpler alternative for Windows GPU/NPU unified path
*Skill Version: 1.0.0 | Standards: ONNX Runtime 1.18+, NPU Drivers 2024+ | Domain: Local AI Inference*
