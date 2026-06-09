# AMD XDNA NPU on Windows — Full Setup & Debugging Reference

This file captures the full workflow for setting up, verifying, and using the AMD Ryzen AI NPU (XDNA) on Windows, specifically for the Ryzen AI 7 350 (Strix Point, XDNA 2) with Radeon 860M iGPU.

---

## Hardware Detection

The NPU appears in Device Manager as **"NPU Compute Accelerator Device"** under the `ComputeAccelerator` class, not under System Devices or Processors.

PowerShell check:
```powershell
Get-PnpDevice | Where-Object Class -eq 'ComputeAccelerator'
```

Expected: FriendlyName="NPU Compute Accelerator Device", Status="OK"

## PCI Device ID → Architecture Mapping

| PCI ID | Code | Architecture | Generation | TOPS |
|--------|------|-------------|------------|------|
| 1022:1502 | PHX/HPT | Phoenix/Hawk Point | XDNA 1 | ~10 |
| 1022:17F0 rev 00/10/11 | STX | Strix Point | XDNA 2 | ~45-50 |
| 1022:17F0 rev 20 | KRK (PCI) | Krackan Point (PCI id) OR Strix Point (marketing name) — Ryzen AI 7 350 is STRIX POINT despite rev 20 | XDNA 2 | ~50 |

**Naming note:** PCI revision alone does NOT determine marketing name. Ryzen AI 7 350 has PCI `DEV_17F0 REV_20` but is marketed as Strix Point. Use CPU model from `Get-CimInstance Win32_Processor` to disambiguate.

## Ryzen AI SDK Installation

Installed to `C:\Program Files\RyzenAI\<version>\` by the AMD installer. Key packages:
- `onnxruntime_vitisai` — ONNX Runtime with VitisAI EP
- `onnxruntime_providers_ryzenai` — Ryzen AI provider DLLs
- `amd_quark` — INT8 quantization tool
- `ryzenai_dynamic_dispatch` — runtime dispatch kernels
- `flexml_lite` / `flexmlrt` — FlexML runtime

Deployment DLLs in `deployment/`: `onnxruntime_providers_ryzenai.dll`, `onnxruntime_vitisai_ep.dll`, `flexmlrt.dll`, `DirectML.dll`.

## Conda Environment

SDK ships `env.yaml` defining conda env `ryzen-ai-<version>`. **Must activate for NPU work.**
Contains Python 3.12, PyTorch 2.4.1+cpu, custom ONNX Runtime with VitisAI EP.

## Quicktest — Verify NPU Works

```bash
cd "C:\Program Files\RyzenAI\<version>"
/path/to/conda/envs/ryzen-ai-<version>/python.exe quicktest/quicktest.py
```
Set `RYZEN_AI_INSTALLATION_PATH` env var if not set.

## VitisAI Target Selection

| Chip | Target |
|------|--------|
| Phoenix/Hawk Point (XDNA 1) | `X1` |
| Strix Point / Krackan Point (XDNA 2) | `X2` |

Do NOT use `KRK` as target — not valid in Ryzen AI 1.7.1.

## ⚠️ CRITICAL: Does the NPU Actually Run Your Model?

`session.get_providers()` returns `['VitisAIExecutionProvider', ...]` even when all ops fall back to CPU. The EP name is registration order, NOT a guarantee of NPU usage.

### How to actually verify:

1. **Watch NPU % in Task Manager** — Performance tab → NPU. If it stays 0%, NPU is not being used regardless of what ORT reports.

2. **Check for VitisAI CHECK failure** — Session creation logging:
   ```
   F... pass_main.cpp:59] Check failed: input_shape[i] != -1
   ```
   The `F` is a FATAL C++ CHECK failure caught by ORT. All ops fell back to CPU silently.

3. **Check for mixed EP assignment** — Warning:
   ```
   [W:onnxruntime:, session_state.cc:1316] Some nodes were not assigned to the preferred execution providers
   ```
   Means some ops ran on CPU. INT8 models with QDQ nodes commonly trigger this, sometimes slower than pure CPU.

4. **Benchmark vs CPU** — If NPU is actually running, latency characteristics differ from CPU.

## Dynamic Shape Limitation

VitisAI EP does NOT support dynamic sequence-length dimensions. Only batch dimension can be -1.
Re-export with `dynamic_axes={'input': {0: 'batch'}}` keeping all other dims fixed.

Patching ONNX metadata alone (`dim_value = 256`) does NOT fix this — graph internals still reference -1.

## ONNX Graph Size Limits

VitisAI compiler hangs on large graphs (>~10K nodes).

| seq_len | Nodes | Compiles? |
|---------|-------|-----------|
| 1 | ~440 | ✅ ~9s |
| 64 | ~6,500 | ✅ ~6s |
| 256 | ~25,000 | ❌ hangs |

**Fix:** Export per-sample model (seq_len=1). Outer loop in plugin code calls ORT per sample.

## Quark INT8 Quantization on Windows

### Prerequisites
- MSVC compiler (VS 2022 BuildTools, "Desktop dev with C++" workload)
- Ninja (`choco install ninja`)
- Python 3.12

### MSVC from bash
```bash
export PATH="/c/Program Files (x86)/.../MSVC/<ver>/bin/Hostx64/x64:$PATH"
export INCLUDE="/c/Program Files (x86)/.../MSVC/<ver>/include"
export LIB="/c/Program Files (x86)/.../MSVC/<ver>/lib/x64"
```

### Distutils._msvccompiler Patch (Python 3.12 fix)
```python
import distutils, setuptools._distutils._msvccompiler
distutils._msvccompiler = setuptools._distutils._msvccompiler
```
Apply BEFORE importing Quark's build script.

### Build Quark Custom Ops
```python
from quark.onnx.operators.custom_ops.build_custom_ops import compile_library
compile_library()
```
Output: `lib/custom_ops.dll` (~576KB). "list index out of range" after success is OK — DLL was built, file-handling step failed.

### INT8 Quantization
```python
from quark.onnx import ModelQuantizer, Config
from quark.onnx.quantization.config.custom_config import get_default_config

qc = get_default_config('XINT8')
qc.extra_options['UseRandomData'] = True
qc.extra_options['CalibDataSize'] = 64
config = Config(global_quant_config=qc)
quantizer = ModelQuantizer(config)
quantizer.quantize_model(input_model, output_model)
```

### INT8 NPU Performance Caveat
INT8 models may be **slower on NPU** than CPU if QDQ nodes cause mixed CPU/NPU execution.
Check for `Some nodes were not assigned to the preferred execution providers` warning.
Fix: `quant_config.include_cle = False`, or exclude MatMul/Gemm from output quantization.

## Weight Extraction from Existing ONNX

When checkpoint has incompatible architecture (e.g. STFTMambaModel vs MambaRTModel), extract from existing ONNX.

ONNX stores Linear weights as `[in_features, out_features]` (transposed vs PyTorch's `[out_features, in_features]`). Must `.T.contiguous()` on load.

Shape-based mapping for onnx::MatMul tensors:
```python
shape_keys = {
    (9, 64):   ['input_proj.proj.weight'],
    (64, 128): ['layer0.in_proj.weight', 'layer1.in_proj.weight', ...],
    (64, 48):  ['layer0.ssm_proj.x_proj.weight', ...],
    (16, 64):  ['layer0.ssm_proj.dt_proj.weight', ...],
    (64, 64):  ['layer0.out_proj.weight', ...],
    (64, 1):   ['output_proj.proj.weight'],
}
# onnx::MatMul tensors are ordered in the proto by layer — zip with keys.
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| No NPU in Device Manager | Driver not installed | Reinstall AMD chipset driver, check BIOS |
| "Session initialized" but NPU 0% | CPU fallback | Check stderr for CHECK failures, verify shapes |
| VitisAI EP disappeared after pip | Vanilla ORT overwrote Ryzen AI build | Reinstall Ryzen AI wheels in order: voe → onnxruntime_vitisai → ryzenai_dynamic_dispatch → onnxruntime_providers_ryzenai |
| Export fails "48 unmatched keys" | Checkpoint architecture mismatch | Extract from existing ONNX via shape-based mapping |
| INT8 slower on NPU | QDQ ops forced CPU fallback for some nodes | Exclude MatMul/Gemm from quantization, disable CLE |
| Session creation hangs | Graph >10K nodes | Export per-sample model (seq_len=1) |
| conda activate removes SSL env var | Harmless conda-forge openssl bug | Ignore |
| hipcc.exe found, ROCM_HOME leaks | Leaked binary in Python313\Scripts | Rename to .bak |
