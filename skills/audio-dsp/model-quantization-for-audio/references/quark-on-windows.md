# AMD Quark on Windows — Known Roadblocks

## Custom Ops DLL Compilation (the main blocker)

Quark's `onnx` module attempts to build a `custom_ops.dll` C++ extension on first import. This requires:

1. **Ninja** build system — install via `choco install ninja` or `pip install ninja`
2. **MSVC compiler** (`cl.exe`) — install via Visual Studio Build Tools 2022 (Community edition is free: `winget install Microsoft.VisualStudio.2022.BuildTools`)
3. **CMake** — already available at `C:\Program Files\CMake\bin\cmake.exe`

If the DLL doesn't exist and Ninja isn't available, Quark warns:
```
[QUARK-WARNING]: The custom ops library ... custom_ops.dll does NOT exist.
[QUARK-ERROR]: CPU version of custom ops library compilation failed: Ninja is required
```

This does NOT block all Quark functionality — some quantization paths work without it — but it does block `quark.onnx.quantization` and the `quark-cli onnx-ptq` subcommand.

## False ROCM_HOME Detection

The `torch.utils.cpp_extension` module (imported by Quark) tries to find ROCm by:
1. Checking `ROCM_HOME` / `ROCM_PATH` env vars
2. Running `shutil.which('hipcc')`
3. Checking `/opt/rocm`

On Windows, if a `hipcc.exe` binary exists anywhere in PATH (e.g. `C:\Program Files\Python313\Scripts\hipcc.EXE`), PyTorch will detect it and set `ROCM_HOME` to its grandparent directory, then immediately crash because Windows ROCm is not supported.

**Fix:** Rename or remove the fake `hipcc.exe`:
```bash
mv "C:\Program Files\Python313\Scripts\hipcc.EXE" "C:\Program Files\Python313\Scripts\hipcc.EXE.bak"
```

## Workarounds When Quark Won't Build

### Option A: Use onnxruntime's built-in quantization

For simpler models, `onnxruntime.quantization.quantize_dynamic()` works without any C++ extensions:

```python
from onnxruntime.quantization import quantize_dynamic, QuantType
quantize_dynamic(
    'model_fp32.onnx',
    'model_int8.onnx',
    weight_type=QuantType.QInt8,
)
```

This produces a dynamically-quantized model (activations computed in FP32, weights stored as INT8). Less optimal than static quantization but works immediately.

### Option B: Install Ninja + MSVC

```powershell
choco install ninja
winget install Microsoft.VisualStudio.2022.BuildTools
```
Then restart the terminal and try importing Quark again. MSVC will be auto-detected by `setuptools` / `torch.utils.cpp_extension`.

### Option C: Skip quantization entirely

The NPU (VitisAI EP) can run FP32 ONNX models — it internally casts to INT8 for its compute units. Performance won't be as good as a properly quantized model, but it works without any quantization toolchain.

## Verifying Quark Is Usable

```python
import quark.onnx.quantization
# If no error, the custom ops DLL was either found or not needed
from quark.onnx.quantization.config.custom_config import get_default_config
config = get_default_config('XINT8')
print(config)
```
