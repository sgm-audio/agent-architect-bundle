---
name: amd-ryzen-ai-npu-inference
description: "AMD Ryzen AI NPU (XDNA 2) on Windows — setup, model export, Quark quantization, ONNX Runtime VitisAI EP. Covers Strix Point / Krackan Point with Ryzen AI 7 350."
version: 1.0.0
author: Hermes (from session 2026-06-07)
license: MIT
---

# AMD Ryzen AI NPU Inference — Windows Guide

## 1. Hardware Target

- **CPU:** AMD Ryzen AI 7 350 (Strix Point)
- **NPU:** XDNA 2 (PCI\\VEN_1022&DEV_17F0)
- **iGPU:** Radeon 860M (ROCm via `HSA_OVERRIDE_GFX_VERSION=11.0.0`)
- **Laptop:** ASUS Vivobook 16 M1607KA

## 2. Software Stack

| Component | Path / Version |
|-----------|---------------|
| Ryzen AI Software | `C:\Program Files\RyzenAI\1.7.1\` |
| Conda env | `ryzen-ai-1.7.1` at `C:\pinokio\bin\miniconda\envs\ryzen-ai-1.7.1\` |
| PyTorch | 2.4.1+cpu (ryzen-ai env) |
| ONNX Runtime | 1.23.3.dev20260320 (VitisAI-enabled) |
| Quark | 0.11rc1 |
| Python | 3.12.11 |

## 3. NPU Verification

```powershell
# Check NPU device
Get-PnpDevice | Where-Object { $_.FriendlyName -match 'NPU|Compute Accelerator' }

# Quick NPU test
conda activate ryzen-ai-1.7.1
$env:RYZEN_AI_INSTALLATION_PATH = 'C:\Program Files\RyzenAI\1.7.1'
python quicktest/quicktest.py
```

Expected: "Test Finished" and `providers: ['VitisAIExecutionProvider', 'DmlExecutionProvider', 'CPUExecutionProvider']`

## 4. ONNX Runtime NPU Inference

```python
import onnxruntime as ort

session = ort.InferenceSession('model.onnx',
    providers=['VitisAIExecutionProvider'],
    provider_options=[{'target': 'X2', 'xlnx_enable_py3_round': 0}])

# X2 = XDNA 2 target (Strix Point / Krackan Point)
# Other valid targets: PSO, PSD, RyzenAI_pso3_v4_dd
```

## 5. Model Export for NPU

**Critical constraints for VitisAI:**
- NO dynamic sequence lengths (only batch can be -1/dynamic)
- Fixed-shape models only for non-batch dims
- Small graphs compile fast (< 1000 nodes = seconds, > 5000 nodes = minutes/hours)
- Per-sample models (seq_len=1) compile reliably (438 nodes, ~9s)

**Per-sample export (recommended for plugins):**
```python
torch.onnx.export(model, args, 'model_1x1.onnx',
    opset_version=18,
    dynamic_axes={'input': {0: 'batch'}, 'output': {0: 'batch'}})
```

**Batched export (for larger models only):**
Use original torch training env (torch 2.11.0+rocm). Graphs >5000 nodes may hang VitisAI compiler.

## 6. INT8 Quantization with Quark

**Prerequisites:**
- MSVC compiler (VS 2022 BuildTools with C++ workload)
- Ninja build system (`choco install ninja`)
- Patch distutils for Python 3.12 compatibility:
```python
import distutils, setuptools._distutils._msvccompiler
distutils._msvccompiler = setuptools._distutils._msvccompiler
```

**Quantization:**
```python
from quark.onnx import ModelQuantizer, Config
from quark.onnx.quantization.config.custom_config import get_default_config

quant_config = get_default_config('XINT8')
quant_config.extra_options['UseRandomData'] = True
config = Config(global_quant_config=quant_config)
quantizer = ModelQuantizer(config)
quantizer.quantize_model('input.onnx', 'output_int8.onnx')
```

NOTE: INT8 on NPU may be slower than FP32 for small models due to QDQ node overhead. The NPU's custom ops DLL needs to be compiled (done automatically when MSVC + Ninja are available).

## 7. Weight Extraction from Existing ONNX

When re-exporting from an existing ONNX (e.g., one exported from a different env or lost source):

- ONNX stores Linear weights transposed: shape is `[in_features, out_features]` vs PyTorch's `[out_features, in_features]`
- ONNX constant-folds certain params: `nn.Parameter(torch.ones(...))`, `torch.zeros(...)` inits, and formula-based params like `log_A_real` get folded away for layers beyond the first
- Map `onnx::MatMul_XXXXX` tensors by shape, then transpose
- Fill missing constant-folded weights from their initialization formulas

## 8. Performance Characteristics (CLARA MambaRT, 76K params)

| Configuration | Time/64 samples | Notes |
|--------------|----------------|-------|
| CPU per-sample FP32 | 19.7ms | Baseline |
| NPU per-sample FP32 | 18.5ms | 1.07x — marginal, ORT call overhead dominates |
| CPU batched-64 FP32 | 15.3ms | Fastest overall for this model size |
| NPU batched-64 FP32 | Hangs | Graph > 5000 nodes, VitisAI compiler can't handle |
| NPU per-sample INT8 | 40.1ms | QDQ overhead, slower than FP32 |

**Key insight:** For models < 1M params, CPU is competitive. The NPU shines on models 10M+ params where compute outweighs data movement overhead.

## 9. Memory Constraints & Segfaults

Models with large intermediate tensors (spectrograms, multi-channel STFT) can **segfault the VitisAI driver** because the NPU's local SRAM is limited (~8-64MB on XDNA 2). This is a kernel-level crash (exit code 139), not a recoverable error.

**Known crash cases:**
- Stem Surgeon (10M params, 708 nodes): FP32 and INT8 both segfault because spectrogram intermediates (refined_specs [1,5,2,2049,431] = 35MB per tensor) exceed NPU local SRAM
- Any model processing full-length audio spectrograms in one pass

**Solutions:**
1. **Chunk the input** — process audio in shorter segments (1-2 seconds) with state carryover
2. **Per-sample processing** — process one audio sample/frame at a time (tiny intermediates, but high ORT call overhead)
3. **FP32 fallback** — if INT8 also segfaults, the problem is tensor size, not quantization

## 9. Known Issues

- **HIP/ROCm `hipcc.EXE` collision:** A `hipcc.exe` binary in `C:\Program Files\Python313\Scripts\` triggers false ROCm detection in PyTorch. Rename to `.bak` to fix.
- **Conda openssl deactivation warning:** `Remove-Item Env:\SSL_CERT_DIR` on conda activate is harmless.
- **`distutils._msvccompiler` error:** PyTorch cpp_extension.py on Python 3.12 needs the distutils patch above.
- **dynamic_axes warning:** Export with `dynamo=False` (old API) for torch >= 2.11, otherwise use `dynamic_shapes`.

## 10. CLARA Project Files (after 2026-06-07)

| File | Purpose |
|------|---------|
| `models/mamba_rt.onnx` | Original dynamic-shape model (6,575 nodes, works CPU-only) |
| `models/mamba_rt_npu.onnx` | Fixed-shape model from original ONNX (6,575 nodes, hangs NPU) |
| `models/mamba_rt_1x1.onnx` | Per-sample model (438 nodes, runs NPU, 38/50 weights) |
| `models/mamba_rt_1x1_complete.onnx` | Per-sample with all 50 weights (437 nodes, runs NPU) |
| `train_clara_model.py` | Reconstructed training + export model classes |
| `train_clara_export.py` | ONNX export wrapper |
