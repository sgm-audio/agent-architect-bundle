---
name: real-time-neural-network-inference-rtneural-onnx
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Real Time Neural Network Inference Rtneural Onnx", "opencode-migrated"]
    related_skills: []
---


# Skill: Real-Time Neural Network Inference (RTNeural / ONNX)
## 📖 1. Overview
Embeds trained deep learning models into C++ plugins using lightweight runtimes (RTNeural, ONNX Runtime C++ API) for <10ms latency audio transformation.
## ⚙️ 2. Core Functionality
- Model Export: PyTorch → ONNX → `rtneural`/`onnx` optimized graph
- Memory Layout: Interleaved vs planar, batch=1 inference
- Quantization: INT8/FP16 fallback for mobile/low-power CPUs
- State Management: LSTM/GRU hidden state carry-over across blocks
## 📥📤 3. Input/Output Schema
| Inputs | ONNX model, input tensor buffers, hidden state vectors | Outputs | Inference tensor, latency metrics, fallback status |
## 🏗️ 4. Architecture
`rtneural::ModelT<float>` with `setInputs()`, `forward()`, `getOutputs()`. Pre-allocate tensors. Use `onnxruntime::Env::Global()` singleton.
## 🔗 5. Dependencies
`RTNeural`, `ONNX Runtime C++`, `Eigen` (backend), `protobuf`
## ⚠️ 6. Edge Cases
| Hidden State Overflow | NaN propagation | Clamp/normalize per block |
| Graph Optimizer Failure | Slow inference | Disable `ORT_ENABLE_ALL`, force `ORT_ENABLE_BASIC` |
| Memory Fragmentation | Tab crash | Pool allocators, fixed tensor sizes |
## 🛡️ 7. Constraints
- Latency: < 5ms/block at 48kHz
- CPU: < 15% single-core
- Memory: Fixed allocation, zero GC
## 🤖 8. Usage
- *Prompt:* "Generate an ONNX export script from PyTorch with `dynamic_axes` set to batch=1 for real-time audio."
## 🧪 9. Testing
- Phase match against Python inference
- State reset verification
- Cross-platform ONNX validation
## 📝 10. Best Practices
- Strip debug nodes from ONNX export
- Use `RTNeural::ModelT` for CPU-optimized inference
- Profile with `perf` or `Instruments`
*Skill Version: 1.0.0 | Standards: ONNX 1.15+, RTNeural 2.0+ | Domain: Audio AI & ML*