# ONNX Export Preflight Checklist

Run this checklist BEFORE exporting a trained Mamba model to ONNX for plugin deployment.
Based on findings from CLARA audit (24 bugs fixed across 2 sessions, June 2026).

## 1. Environment Checks

- [ ] `torch >= 2.0` — verify with `torch.__version__`
- [ ] `onnx < 1.17` (opset 18) or `onnx >= 1.17` (opset 21+)
- [ ] `onnxruntime` installed and importable
- [ ] Checkpoint loads: `torch.load(path, map_location='cpu', weights_only=False)`
- [ ] State dict keys match: `checkpoint.keys() == model.state_dict().keys()`
  - If mismatch: `{k: v for k, v in sd.items() if k in model.state_dict()}`
  - Missing keys warn. Don't export with random-init weights for production.

## 2. Model Architecture Verification

- [ ] Dry-run forward pass: `model(x, *convs, *ssms, cond)` — confirm shapes match
  - Expected: `audio_chunk [1, seq_len, 1]`, `conv{i} [1, d_model, conv_width]`, `ssm{i} [1, d_model, d_state]`, `cond [1, 8]`
- [ ] Output shape: `processed_audio [1, seq_len, 1]`
- [ ] Output variance > 1e-6 (if trained) or > 1e-2 (if trained with meaningful weights)
- [ ] Output is NOT all zeros, NaN, or Inf

## 3. ONNX Export Config

- [ ] `opset_version=18` for ONNX Runtime 1.15–1.16
- [ ] `opset_version=21` for ONNX Runtime 1.17+ (supports inlined weights, avoids .data split)
- [ ] `dynamic_axes={'audio_chunk': {1: 'seq_len'}, 'processed_audio': {1: 'seq_len'}}`
- [ ] `do_constant_folding=True`
- [ ] `dynamo=False` (jit.trace style, not dynamo — recurrent models)
- [ ] Input names match exactly what the C++ engine expects: `['audio_chunk', 'conv0', 'conv1', 'conv2', 'conv3', 'ssm0', 'ssm1', 'ssm2', 'ssm3', 'cond']`
- [ ] Output names: `['processed_audio', 'new_conv_state', 'new_ssm_state']`

## 4. Post-Export Verification

- [ ] **ONNX loads**: `onnx.load(path)` — no errors
- [ ] **ONNX Runtime infers**: `sess.run(None, feeds)` — no session creation errors
- [ ] **ONNX vs PyTorch match**: Cosine similarity > 0.999, max abs diff < 1e-4
  - Use same random seed (42) for reproducible comparison
- [ ] **No external .data file check**: If `.onnx.data` was created:
  - Test: bundle `.onnx` alone and try `sess.run()`. Does it fail?
  - Fix: re-export with `opset_version=21`, or accept the split and document it
- [ ] **State continuity**: Process chunk 1, feed state to chunk 2 — chunk 2 output is NOT all zeros
- [ ] **Output sanity**: `np.all(np.isfinite(output))` — no NaN/Inf
- [ ] **Manifest generated**: `models/manifest.json` with sha256 checksums, arch params, io contract

## 5. Known ONNX Export Pitfalls (from CLARA audit)

| Bug | Symptom | Fix |
|-----|---------|-----|
| External .data split | `.onnx` is 5.6MB with a 270KB `.data` sibling | Use `opset_version=21` or suppress `large_model` |
| Use-after-free on reload | Engine pointer dangles after model reload | Use `std::atomic<Engine*> enginePtr` for RT-safe access |
| TOCTOU on conditioning | Two separate reads of `condFrame` disagree | Snapshot once per block for both inference + modulation |
| `ORT_ENABLE_BASIC` not `ALL` | Operator fusion disabled, 10-30% perf loss | Set `ORT_ENABLE_ALL` |
| Negative `numSamples` UB | Crash with empty buffers | Guard with `if (nSamples <= 0) return` |
| Missing CLAP extensions | No state context / render / tail | Add `CLAP_EXT_STATE_CONTEXT`, `CLAP_EXT_RENDER`, `CLAP_EXT_TAIL` |
| Missing ARA content types | `doGetContentTypes` not implemented | Add stub returning `ARA_CONTENT_TYPE_MUSICAL_CONTEXT` |
| ARA archive no versioning | Forward compatibility broken | Add magic `0x4D424152` + version byte header |
| Windows UTF-8 path corruption | Non-ASCII paths fail | Use `MultiByteToWideChar(CP_UTF8)` before `CreateFileW` |
| Data race on static bool | `warnedOnce` race in RT thread | Use `static std::atomic<bool> warnedOnce` |
| `std::stoi` crash on malformed manifest | Missing try/catch causes crash | Add try/catch for `invalid_argument` / `out_of_range` |