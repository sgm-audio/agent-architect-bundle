---
name: model-quantization-for-audio
description: "Use this skill when the user is working on or asking about quantizing audio ML models, INT8/FP16 quantization for audio inference, PTQ (Post-Training Quantization) and QAT (Quantization-Aware Training) for audio neural networks, ONNX quantization for audio models, or reducing model size for real-time audio plugin deployment."
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Model Quantization For Audio", "opencode-migrated"]
    related_skills: []
---


# Skill: Model Quantization for Audio ML

## 1. Overview
Covers quantizing machine learning models for audio inference — reducing precision from FP32 to INT8/FP16 to fit into real-time audio plugin constraints (low latency, limited memory, NPU/iGPU targets). Focuses on quantization techniques that preserve audio quality for tasks like source separation, denoising, pitch estimation, and embedding extraction.

## 2. Core Functionality
- **Quantization Types:** PTQ (Post-Training Quantization) vs QAT (Quantization-Aware Training), static vs dynamic quantization, per-tensor vs per-channel
- **Precision Targets:** FP32 → FP16 (half) → INT8 (W8A8) → INT4/AWQ/GPTQ (for LLM-based audio models)
- **ONNX Quantization:** `onnxruntime.quantization.quantize_static`, `quantize_dynamic`, `QuantizationMode::IntegerOps`
- **Audio-Aware Calibration:** Calibration dataset must match audio domain (not ImageNet) — use representative audio samples at 16/24-bit, 44.1/48kHz
- **Quantization Sensitivity Analysis:** Per-layer KL divergence between FP32 and INT8 output, identifying sensitive layers to skip quantization
- **NPU-Optimized Formats:** INT8 symmetric for NPU dataflow engines, NHWC layout for NPU/GPU tensor cores
- **Deploy:** ONNX Runtime with INT8 execution provider, TensorRT INT8, CoreML FP16, OpenVINO INT8
- **AMD Quark on Windows (known roadblock):** Quark 0.11rc1 requires Ninja + MSVC to build its `custom_ops.dll` C++ extension on first import. Without it, `quark.onnx.quantization` fails to load. Additionally, a `hipcc.exe` false positive in PATH triggers a PyTorch ROCM_HOME detection crash (`Building PyTorch extensions using ROCm and Windows is not supported`). See `references/quark-on-windows.md` for workarounds including onnxruntime built-in quantization and Ninja+MSVC installation.

## 3. Input/Output Schema
| Inputs | FP32 ONNX/PyTorch model, calibration dataset (audio chunks), target precision, calibration method |
| Outputs | Quantized ONNX/PT model, per-layer sensitivity report, accuracy vs size tradeoff curve |
| Metrics | Model size (MB), throughput (inferences/sec), PESQ/SISDR change, INT8 vs FP32 accuracy delta |

## 4. Architecture
Quantization pipeline: export trained model to FP32 ONNX → run calibration with audio dataset (collect activation histograms) → apply quantization (per-tensor symmetric INT8 for weights, per-channel asymmetric INT8 for activations) → evaluate accuracy on validation set → iterate on sensitive layers. For real-time, prefer static quantization over dynamic (dynamic quantization of activations adds runtime overhead).

## 5. Dependencies
`onnxruntime` + `onnxruntime.quantization`, `torch.ao.quantization` (PyTorch), `onnxconverter-common`, `pytorch-quantization` (NVIDIA), calibration dataset in `.wav`/`.flac`, `pesq` / `pystoi` for audio quality metrics

## 6. Edge Cases
| Accuracy Collapse | Certain layers (attention, GRU) highly sensitive to INT8 | Use FP16 for these layers, skip quantization |
| Calibration Mismatch | Dataset doesn't cover full dynamic range | Use diverse audio (speech, music, noise floor, transients) |
| NPU Rejecting INT8 | NPU requires specific quantization scheme (symmetric, per-channel) | Match NPU's `QDQ` configuration from ONNX EP docs |
| Quark Fails to Import on Windows | Custom ops DLL needs Ninja+MSVC to build; or fake `hipcc.exe` triggers ROCM_HOME crash | Install Ninja (`choco install ninja`), VS Build Tools; rename/remove fake `hipcc.exe` in Python Scripts dir. See `references/quark-on-windows.md`. |
| BatchNorm Folding | INT8 + BN causes distribution shift | Fuse BN into preceding conv layer before quantization |
| Dequantize Overhead | Frequent DQ nodes in ONNX graph increase latency | Use `onnxruntime.quantization` with `QDQ` format, optimize graph |
| **ONNX External Data (.data) Split** | Exporting a model <2GB still produces a `.onnx.data` sibling if `opset < 21` or `large_model=True` is implicitly triggered. The `.data` file must travel with the `.onnx` or model fails to load in ONNX Runtime. | Re-export with `opset_version=21` (ONNX IR v10) which can inline larger weights. Or always bundle `.onnx` + `.onnx.data` together — but verify with `sess.run(None, feeds)` first. Check: `onnx.load(onnx_path)` reports external data path. |

## 7. Constraints
- INT8 quantization typically yields 2-4x speedup on NPU/GPU, 1.5x on CPU (with VNNI)
- Audio quality degradation: SISDR drop of < 0.5 dB is acceptable for most tasks
- Calibration set must be 500-2000 representative audio clips (~10-60 seconds total)
- Recurrent layers (LSTM/GRU) are harder to quantize than convolutional layers
- For LLM-based audio models (e.g., audio captioning), use GPTQ/AWQ 4-bit with calibration from audio transcripts

## 8. Usage
- *Prompt:* "Quantize a PyTorch audio denoiser from FP32 to INT8 for ONNX Runtime NPU deployment."
- *Prompt:* "Run quantization sensitivity analysis on a source separation model to find the best per-layer precision."
- *Prompt:* "Create a calibration dataset from my audio test corpus and apply PTQ."
- *Prompt:* "Compare FP16 vs INT8 throughput and accuracy for a real-time pitch estimation model."

## 9. Testing
- Pre/post quantization: compute PESQ, STOI, or SISDR on a held-out test set
- Measure latency: `OrtSession::Run` timing with FP32 vs INT8 model on target hardware
- Verify INT8 model output dynamic range matches FP32 within 1% RMS
- `onnxruntime_perf_test -m int8_model.onnx -e cpu` for baseline

## 10. Best Practices
- Always calibrate with audio samples that match the target domain (don't use generic ImageNet calibration)
- Use per-channel quantization for weights (`axis=1` for conv, `axis=0` for linear)
- Export sensitivity reports after first quantization pass; iterate on the top 5 most-degraded layers
- For real-time audio plugins, export as INT8 ONNX with `GraphOptimizationLevel::ORT_ENABLE_EXTENDED`
- Version both FP32 and INT8 models — always keep the FP32 reference for debugging deployment issues
- Use `PowerOfTwo` scale rounding for NPU targets that only support powers-of-two scaling
*Skill Version: 1.1.0 | Standards: ONNX Runtime, INT8, PTQ/QAT | Domain: Audio ML Deployment*"
