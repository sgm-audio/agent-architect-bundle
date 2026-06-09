---
name: mamba3-dsp-methodology
description: "Use when working on real-time audio DSP plugins with Mamba SSM models — lock-free concurrency, ONNX quantization, CLAP/ARA protocol, RT-safe inference, and deterministic sandboxing. Covers the Cynical Engineer edge-DSP meta-prompt stack."
version: 1.0.0
author: Hermes Agent (ported from OpenCode skills)
license: MIT
metadata:
  hermes:
    tags: [dsp, mamba, real-time-audio, clap, onnx, lock-free, quantization, plugin]
    related_skills: [opencode, hermes-agent-skill-authoring]
---

# Mamba3 DSP Methodology

## Overview

This skill encodes the methodologies from the Mamba-3 training and edge-DSP meta-prompt stack used in the CLARA (CLAP + ARA) plugin framework. It covers the full pipeline: real-time-safe concurrency, Mamba SSM model training + quantization, ONNX inference in plugins, CLAP/ARA protocol implementation, and deterministic sandboxing.

The principles here are what you "stand by" — lock-free audio threads, INT8 quantized neural DSP on NPU/iGPU, C-clean CLAP protocol, and open-source everything.

## When to Use

- Building or debugging a CLAP/ARA audio plugin (CLARA suite)
- Working on RT-safe lock-free concurrency (SPSC queues, atomic parameter snapshots)
- Training, exporting, or quantizing a Mamba SSM model for real-time inference
- Quantizing audio ML models from FP32 to INT8/FP16 for ONNX Runtime deployment
- Writing or reviewing Reaper ReaScripts (Lua) for plugin workflow testing
- Designing deterministic sandboxing for user DSP code (WASM, seccomp)
- Setting up agentic tool-use / function calling from an LLM into a DAW
- Cross-compiling or building for NPU / iGPU targets (ROCm on APU)

Don't use for: general ML training (not audio-specific), frontend web dev, non-realtime signal processing.

## Project Reference

Your key project paths on this machine:

| Project | Path | Deployment | Trained model |
|---------|------|------------|---------------|
| CLARA (MambaSuite) | `/mnt/c/dev/Audio Development/0 CLARA/` | CLAP + ARA2, ONNX Runtime | Mamba-3 PerTrackProcessor (training at Mamba-3-training/) |
| **MambaDAW** (not EmT!) | `/mnt/c/dev/mamba3/mamba3/Mamba Based/MambaDAW/` | CLAP (.clap), VST3 (P2), LV2 (P3), .mmbw | **best.pt** (8MB, 100K steps) at checkpoints_laptop/ — EffectControllerMamba → 80 logits → 17 DSP params |
| EmT (separate from MambaDAW) | `/mnt/c/dev/Audio Development/0 EmT/` | CLAP + ARA2 prototype | None trained yet |
| Stem Surgeon | `/mnt/c/dev/Audio Development/Stem Surgeon/stem-surgeon/` | JUCE VST3/AU/ARA2, ONNX | Needs training (no checkpoint yet) |
| MambaCompressor | `/mnt/c/dev/Audio Development/mamba-compressor/` | Python research | Pre-alpha, no checkpoint |
| Stem+MIDI Pro | `/mnt/c/dev/stem_midi_pro/` | SaaS (FastAPI + NeMo) | No checkpoint (needs training) |
| Mamba-3 training | `/mnt/c/dev/mamba3/mamba3/Mamba-3-training/` | — | Failed run at step 6.5K, archived |
| Mamba Based (research hub) | `/mnt/c/dev/mamba3/mamba3/Mamba Based/` | — | Contains MambaDAW, ADRs, system designs, FMA dataset, emotion-aware DSP research |
| Edge DSP meta-prompt | `/mnt/c/dev/mamba3/mamba3/edge_dsp_meta_prompt/` | Rust CLAP via nih-plug | Arch complete, needs training |
| Checkpoints (100K model) | `/mnt/c/dev/mamba3/mamba3/checkpoints_laptop/` | — | **best.pt** (8MB) + 283 checkpoints, 1.8GB total |

### Mamba3 Training — Quick Reference (from REFERENCE_THIS_SHIT.md)

```
src/  (Mamba3 training: model.py, train.py, extract_crepe.py)
├── model.py               — PerTrackProcessor: Mamba-3 MIMO + FiLM conditioning
├── train.py                — 3-phase: contrastive → MR-STFT+Mel-L1 → cross-track SI-SDR
├── extract_crepe.py        — Offline CREPE f0 extraction per stem
├── smoke_test.py           — 793-line pre-training smoke test (9 sections)
├── run_train.ps1           — Windows wrapper (ROCm on gfx1152)
└── run_train.sh            — Linux wrapper (HSA_OVERRIDE_GFX_VERSION=11.0.0)

Edge DSP meta-prompt (compiler/):
├── prompt_stack.py         — 5-layer compiler structures
├── train_controller.py     — Mamba3Controller + dynamic losses
└── quantize.py             — ONNX exporter + INT8 dynamic quantizer
```

## 1. Lock-Free Concurrency & Real-Time Safety

Audio threads must never block. Use these patterns from your Cynical Engineer DSP engine:

### SPSC Ring Buffer (wait-free message passing)

```cpp
template<typename T, size_t N>
class SpscQueue {
    std::array<T, N> buf{};
    std::atomic<size_t> head{0}, tail{0};
public:
    bool push(const T& item) {
        size_t h = head.load(std::memory_order_relaxed);
        size_t next = (h + 1) % N;
        if (next == tail.load(std::memory_order_acquire)) return false;
        buf[h] = item;
        head.store(next, std::memory_order_release);
        return true;
    }
    bool pop(T& item) {
        size_t t = tail.load(std::memory_order_relaxed);
        if (t == head.load(std::memory_order_acquire)) return false;
        item = buf[t];
        tail.store((t + 1) % N, std::memory_order_release);
        return true;
    }
};
```

### Atomic Triple-Buffer (parameter snapshot pattern)

```cpp
struct alignas(64) ParamSnapshot {
    float gain{0.5f};
    float cutoff{2000.0f};
    bool bypass{false};
};

class ParamManager {
    std::atomic<bool> updated{false};
    alignas(64) ParamSnapshot rtBuffer{}, uiBuffer{};
public:
    void pushFromUI(float g, float c, bool b) { /* store + release */ }
    ParamSnapshot pullForRT() { /* acquire + load */ }
};
```

### Key constraints from your architecture:
- **Zero heap allocations** in the audio callback — pre-allocate everything
- **Cache-line alignment** (`alignas(64)`) to prevent false sharing
- **`std::memory_order_release/acquire`** for SPSC sync (not seq_cst)
- **Deferred state reset** via atomic flag (your `resetRequested_` pattern)
- **Thread-local** `std::vector<Ort::Value>` with `reserve()` at init

## 2. Mamba SSM Model Training & Export

### Training (3-phase strategy from train.py)

| Phase | Steps | Loss | Purpose |
|-------|-------|------|---------|
| 1 | 0-20% | NT-Xent contrastive | Learn embedding space |
| 2 | 20-50% | MR-STFT + Mel-L1 | Single-track reconstruction |
| 3 | 50%+ | SI-SDR ramp | Cross-track source separation |

### ROCm on Windows (APU / iGPU) — your hardware quirk notes:

- Device string: `cuda` (API-compat layer, not real CUDA)
- Required env vars: `HSA_ENABLE_SDMA=0`, `PYTORCH_ALLOC_CONF=garbage_collection_threshold:0.8,max_split_size_mb:256`
- Checkpoint every 500 steps (GPU hang bug `MES:0x82` mitigation)
- Smart App Control MUST be OFF (one-way disable)
- Detect Linux vs Windows venv: check `pyvenv.cfg` for `home = /usr/bin`

### ONNX Export

```bash
python3 export_mamba_onnx.py
```

Exports `models/mamba_rt.onnx` + `.onnx.data` via `torch.jit.trace`, opset 18. Self-verifies: runs ONNX inference, checks shapes, validates state continuity across chunks.

## 3. Model Quantization for Audio (INT8/FP16)

Your pipeline: FP32 PyTorch → ONNX export → calibration → INT8 quantized ONNX → deploy in plugin.

### Quantization types

| Type | When | Tradeoff |
|------|------|----------|
| Static PTQ | Most audio models | Best perf, needs calibration dataset |
| Dynamic PTQ | Recurrent layers | Runtime overhead, no calibration needed |
| QAT | Accuracy-critical | Slower training, best quality |

### Audio-aware calibration rules

- **Calibration dataset must match target domain** — don't use ImageNet
- Use 500-2000 representative audio clips (10-60s total) at 16/24-bit, 44.1/48kHz
- Measure quality with PESQ / STOI / SI-SDR — target < 0.5 dB drop
- Skip quantization on sensitive layers (attention, GRU) — use FP16 there

### ONNX quantization command

```python
from onnxruntime.quantization import quantize_dynamic, QuantType
quantize_dynamic(
    model_input="mamba3_controller.onnx",
    model_output="mamba3_controller_quant.onnx",
    weight_type=QuantType.QInt8
)
```

For static quantization with calibration:
```python
from onnxruntime.quantization import quantize_static, QuantFormat
quantize_static(
    model_input="mamba_rt.onnx",
    model_output="mamba_rt_int8.onnx",
    calibration_data_reader=AudioCalibrationReader(dataset_path, num_samples=1000),
    quant_format=QuantFormat.QDQ,  # Quantize-Dequantize nodes for NPU
    per_channel=True,
    activation_type=QuantType.QUInt8,
    weight_type=QuantType.QInt8
)
```

### Your model's tensor interface (from REFERENCE_THIS_SHIT.md)

| Tensor | Shape | Type | Description |
|--------|-------|------|-------------|
| `observer_features` (in) | `[1, 100, 12]` | f32 | Sliding window (100 frames of 12 features) |
| `session_state` (in) | `[1, 16]` | f32 | Track type, BPM, beat offset, SR |
| `hidden_state_in` (in) | `[1, 64]` | f32 | Mamba recurrent state carry-over |
| `dsp_parameters` (out) | `[1, 32]` | f32 | 32 dynamic DSP coefficients |
| `hidden_state_out` (out) | `[1, 64]` | f32 | Next recurrent state |

## 4. CLAP Protocol Implementation

Your CLARA plugin uses CLAP (Clever Audio Plugin) — an open-source, license-free alternative to VST3.

### Core plugin structure

```c
static const clap_plugin_descriptor descriptor = {
    .id = "com.yourcompany.mambasuite.v1",
    .name = "MambaSuite",
    .vendor = "SGM Studios",
    .features = (const char*[]){"effect", "audio", NULL},
};
```

### RT-safe process loop (from CLARA's MambaClapPlugin)

```c
bool process(const clap_plugin *plugin, const clap_process *process) {
    // Sample-accurate event handling
    for (uint32_t i = 0; i < process->in_events->size(process->in_events); ++i) {
        const clap_event_header_t* ev = process->in_events->get(process->in_events, i);
        if (ev->type == CLAP_EVENT_NOTE_ON) handleNoteOn((clap_event_note_t*)ev);
    }
    // Audio processing
    for (uint32_t f = 0; f < process->frames_count; ++f) {
        for (uint32_t ch = 0; ch < plugin->audio_ports->count; ++ch)
            process_sample(process->audio_inputs[0].data32[ch][f],
                          process->audio_outputs[0].data32[ch][f]);
    }
    return true;
}
```

### CLARA-specific architecture notes (from the AGENTS.md):

- **`MambaInferenceEngine`** — RT-safe ONNX wrapper with `thread_local std::vector<Ort::Value>` and `reserve()` for zero per-call heap allocs
- **Deferred state reset** via `resetRequested_` atomic flag
- **Click-free bypass** via 50ms linear crossfade (per-sample ramp, shared across channels)
- **Model path resolution** using `dladdr()` relative to `.clap` binary
- **3 atomics**: bypass (stepped), wet/dry, intensity
- ARA2 library (`MambaSuiteARA.so`) shares the same `MambaCore` static library

### Build (from CLARA's CMakeLists.txt)

```bash
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build . --parallel
```

Outputs to `build/plugins/`: `MambaSuiteClap.clap`, `MambaSuiteARA.so`, and ONNX models + `libonnxruntime.so.1.17.1`.

### Key CLAP extensions to register

| Extension | Purpose |
|-----------|---------|
| `CLAP_EXT_PARAMS` | Plugin parameters |
| `CLAP_EXT_STATE` | State save/load |
| `CLAP_EXT_AUDIO_PORTS` | Audio I/O config |
| `CLAP_EXT_LATENCY` | Report latency |
| `CLAP_EXT_NOTE_PORTS` | MIDI note I/O |
| `CLAP_EXT_THREAD_POOL` | Thread-safe host calls |

## 5. Real-Time Neural Network Inference (ONNX Runtime)

### Architecture (from your CLARA plugin)

```cpp
// thread_local Ort::Value pre-allocation
thread_local std::vector<Ort::Value> rtTensors;
// At init:
rtTensors.reserve(3); // input, hidden_state_in, etc.
// In processBlock():
auto output = session.Run(Ort::RunOptions{nullptr},
                          inputNames.data(), rtTensors.data(), rtTensors.size(),
                          outputNames.data(), outputNames.size());
```

### Constraints you enforce:
- **Latency**: < 5ms/block at 48kHz
- **CPU**: < 15% single-core
- **Memory**: Fixed allocation, zero GC
- **State management**: LSTM/GRU/Mamba hidden state carry-over across blocks
- ONNX Runtime singleton via `Ort::Env::Global()` (shared across plugin instances)

## 6. Deterministic Audio Sandboxing

For running third-party DSP code safely inside the plugin:

- **WASM isolation**: Linear memory, no syscalls, limited imports via `wasmtime`
- **Process sandboxing**: `seccomp` filters on Linux, `cgroups` for resource limits
- **Whitelist** only `audio_process`, `get_param` as allowed imports
- **Hard timeout**: 100ms kill, log failure
- **Deny by default** — allow explicitly

## 7. Agentic Tool-Use for DAWs (Function Calling)

When an LLM agent (Hermes or OpenCode) controls the DAW, use this schema pattern:

```json
{
  "tool": "set_plugin_param",
  "args": {
    "id": "mamba_comp_1",
    "param": "intensity",
    "value": 0.75
  }
}
```

Validate against JSON schema, execute via host API. Safety rules:
- Always return structured JSON, never raw text
- Require user confirmation for destructive actions (delete/bypass/mute)
- Maintain undo stack for all actions
- Fuzzy-match parameter names for natural language input

## 8. Hermes ↔ OpenCode Delegation (Your Hybrid Workflow)

The user works in a hybrid model: **Hermes orchestrates the big picture; OpenCode writes the code**. This section codifies that pattern.

### When to delegate to OpenCode vs handle in Hermes

| Situation | Run in | Why |
|-----------|--------|-----|
| Understanding the mamba3 methodology (lock-free, quantization, CLAP) | Hermes (load this skill) | This skill has the patterns |
| Writing new C++/Rust code for the plugin | OpenCode | OpenCode has 22 Reaper + 146 total skills; it's the code generator |
| Debugging a build failure or CMake error | Hermes first, then delegate | Hermes inspects, then sends the fix to OpenCode to implement |
| Training a Mamba3 model | Hermes orchestrates the pod, OpenCode runs the training script | Hermes manages RunPod lifecycle, OpenCode writes the script |
| Writing a ReaScript (Lua) | OpenCode | OpenCode's 22 reaper-* skills were specifically built for this |
| Quantizing an ONNX model | Either | Both Hermes (this skill §3) and OpenCode's `model-quantization-for-audio` have the knowledge |
| Code review / PR review | OpenCode | OpenCode has a built-in `opencode pr <number>` command |
| Cross-project context (how does CLARA relate to Mamba-3 training?) | Hermes | Hermes sees the whole dev directory and this skill |

### Delegation syntax

```bash
# Bounded one-shot task (no pty needed)
terminal(command="opencode run 'Add a new MambaInferenceEngine method for stereo processing'", workdir="/mnt/c/dev/Audio Development/0 CLARA")

# Attach context files
terminal(command="opencode run 'Review this CMakeLists.txt for portability issues' -f CMakeLists.txt -f CMakePresets.json", workdir="/mnt/c/dev/Audio Development/0 CLARA")

# Iterative session (start TUI, send follow-ups)
terminal(command="opencode", workdir="/mnt/c/dev/mamba3/mamba3/Mamba-3-training", background=true, pty=true)
process(action="submit", session_id="<id>", data="Debug the NaN loss in Phase 3 training")
process(action="poll", session_id="<id>")
process(action="submit", session_id="<id>", data="Now add gradient clipping and re-run")
# Exit with Ctrl+C
process(action="write", session_id="<id>", data="\x03")
```

### Pitfalls in the hybrid workflow

1. **Hermes runs in WSL, OpenCode runs in Windows** — OpenCode binary at `/mnt/c/Users/scott/AppData/Roaming/npm/opencode`. Paths to Windows projects like `/mnt/c/dev/...` work from both sides.
2. **Don't re-explain the methodology** — when delegating to OpenCode, the prompt should focus on *what to code*, not the DSP theory (that's in this skill). If OpenCode needs context, attach a file rather than re-educating.
3. **OpenCode's default provider may fail** — if `opencode run` gives "Unexpected server error", force a provider with `--model`. User has 5 providers configured (Nvidia, Google, GitHub Copilot, OpenCode Go, DeepSeek).
4. **Smoke test before trusting** — Always verify OpenCode works before delegating a long task: `opencode run 'Respond with exactly: OPENCODE_SMOKE_OK'`. If it fails on the default provider, try forcing `--model`.

## 9. CLAP Plugin UI (WebView Pattern)

For a professional plugin UI without JUCE's LookAndFeel burden, use the WebView bridge pattern. See `references/webview-plugin-ui.md` for:

- Complete architecture: CLAP plugin → JSON bridge → system WebView → HTML/CSS/JS
- The MAAPS design spec: 900×600px, matte black ash (`#0D1117`), orange accent
- UI component layout (header, module chain, meter bridge, operation log, status bar)
- Confidence-as-visual-weight system: low-confidence = reduced opacity/dashed outline
- Immutable operation log: timestamped, click-to-revert every AI decision
- Figma → HTML export pipeline: all UI dev in browser, no C++ recompilation needed
- Implementation steps: WebUI library choice, CLAP GUI extension, JSON bridge protocol
- Minimal HTML template with CSS variables for the MAAPS color palette

For releasing a plugin that needs to "look as good as it sounds," this is the fastest path:
- **Figma → HTML/CSS** direct pipeline — no C++ UI compilation
- **CSS animations** for glow effects, meter transitions, state visualization
- **webui.me** — 2 C files, renders in the OS native webview (WebView2/WKWebView/WebKitGTK)
- **JSON message bridge** between C++ audio thread and JS UI thread
- **Zero threading bugs** — browser event loop handles all repaints

This is the approach used by iZotope, Output, and Baby Audio.

## Deep-Copy of Key OpenCode Skills

This Hermes skill subsumes the following OpenCode skills you've been relying on:

| OpenCode Skill | Content absorbed here |
|----------------|----------------------|
| `lock-free-concurrency-and-real-time-safety` | §1 SPSC queues, atomic snapshots, cache-line alignment |
| `deterministic-audio-sandboxing` | §6 WASM/seccomp/cgroups sandboxing |
| `digital-signal-processing-dsp-mathematics` | Referenced in §4 (ZDF SVF, ADAA saturator in REFERENCE_THIS_SHIT) |
| `model-quantization-for-audio` | §3 INT8/FP16 quantization pipeline |
| `real-time-neural-network-inference-rtneural-onnx` | §5 ONNX Runtime C++ inference |
| `clap-protocol-implementation` | §4 CLAP C-API, extensions, RT-safe process loop |
| `agentic-tool-use-function-calling-for-daws` | §7 LLM-to-DAW tool-calling schema |
| `neural-audio-codec-implementation-encodec-soundstream` | Referenced architecture in model.py (Mamba SSM encoding) |
| `ml-audio` | General audio ML context (feature extraction, datasets) |

## MAAPS Design Language

The MAAPS plugin family shares a unified visual identity. See `references/maaps-design-language.md` for the complete design spec:

- **900×600px**, matte black ash (`#0D1117`–`#161B22`), **orange accent** (`#FF6B35`)
- No skeuomorphic knobs — sliders, number fields, LED meters only
- Confidence scores as first-class UI element (0-100%, opacity/dashed outlines)
- Immutable Operation Log (timestamped audit trail with click-to-revert)
- Three mode-specific layouts: Cynical Engineer, Mix Engine, Surgical Tool
- WebView bridge for prototyping; OpenGL for shipped builds

## MAAPS Product Suite

The full MAAPS lineup spans 5+ products sharing the Mamba-3 inference core:

| Product | Type | Path | Status |
|---------|------|------|--------|
| **CLARA** (MambaSuite) | CLAP + ARA2 plugin, C++17, ONNX RT | `Audio Development/0 CLARA/` | ~25-30% |
| **MambaDAW** (EmT) | CPU-only CLAP, .mmbw weights, C++17 | `Audio Development/0 EmT/` | ~15-20% |
| **Stem Surgeon** | 5-stem separator, JUCE/ARA2 | `Audio Development/Stem Surgeon/stem-surgeon/` | ~60% |
| **MambaCompressor** | Mamba→DSP params, Python research | `Audio Development/mamba-compressor/` | Pre-alpha |
| **Stem+MIDI Pro** | SaaS, guitar/bass separation + MIDI | `dev/stem_midi_pro/` | Fastest to revenue |
| **Mamba-3 Adaptive Filter Bank** | Rust CLAP via nih-plug, STFT→iSTFT | `mamba3/mamba3/edge_dsp_meta_prompt/` | Arch complete |
| **Precision Surgical Tool** | De-esser/de-clicker, spec only | (in edge_dsp_meta_prompt specs/) | Spec only |

## Common Pitfalls

> **Reference:** `references/webview-plugin-ui.md` documents the WebView-based plugin UI architecture for CLAP plugins. Use it when building the visual interface for any plugin in the MAAPS suite.
> **Reference:** `references/maaps-project-ecosystem.md` catalogs the full MAAPS project inventory with real paths, integration maps, dataset locations, SDK deps, and training checkpoint registry.

1. **SPSC queue overflow in audio callback** — Always check `push()` return value and log drops; never block
2. **Quantization accuracy collapse on recurrent layers** — Mamba SSM layers are sensitive to INT8; test per-layer, use FP16 fallback
3. **ONNX model path resolution** — Use `dladdr()` relative to `.clap` binary, not hardcoded paths (CLARA pattern)
4. **ROCm vs CUDA confusion** — On Windows ROCm, `torch.cuda.is_available()` returns True but no ROCm tools (rocprofiler, HIP) are available
5. **Static quantization calibration mismatch** — Must use audio-domain calibration data, not generic ImageNet
6. **GPU hang on Radeon 860M** — The `MES:0x82` bug; mitigate with aggressive checkpointing and `HSA_ENABLE_SDMA=0`
7. **Mamba state overflow across blocks** — Clamp hidden state, validate continuity across chunks in ONNX export
8. **Linux vs Windows venv** — `.venv/` built on Linux has `home=/usr/bin` in `pyvenv.cfg`; must delete before running on Windows
9. **Forgetting `memory_order_release/acquire`** on SPSC atomics — default seq_cst is correct but 5-10x slower
10. **Click on bypass transition** — Use 50ms linear crossfade ramp (your CLARA pattern), don't gate instantly
11. **Don't confuse MambaDAW with EmT** — EmT (in `Audio Development/0 EmT/`) is a separate CLAP+ARA2 prototype. The REAL Mamba DAW (CPU-only, .mmbw, 100K-step trained model) lives at `mamba3/mamba3/Mamba Based/MambaDAW/`. They have different architectures, different model formats, and different TODO lists. Verify the project path before loading code or delegating work.
12. **best.pt (8MB) is for Mamba DAW, not CLARA or the adaptive filter bank** — The 100K-step model at `mamba3/mamba3/checkpoints_laptop/best.pt` is the EffectControllerMamba, which feeds 80 logits → 17 DSP parameters for the Mamba DAW effect chain. CLARA uses ONNX Runtime with a different model format. The adaptive filter bank (edge_dsp_meta_prompt/) has its own separate training pipeline.
13. **Failed vs successful training runs** — The `mamba3/mamba3/Mamba-3-training/checkpoints/` (7 files, step 6.5K) are from a failed RunPod run and are archived. The real 100K model is at `mamba3/mamba3/checkpoints_laptop/` (~1.8GB, 283 checkpoints + best.pt). Check BOTH locations before assuming no trained model exists.

## Verification Checklist

- [ ] SPSC queue does not allocate in push/pop
- [ ] Atomic parameter swap uses `memory_order_release/acquire`
- [ ] Model exports via ONNX opset 18 and self-validates
- [ ] Quantization preserves SI-SDR within 0.5 dB of FP32
- [ ] CLAP plugin registers all required extensions (params, state, audio-ports)
- [ ] Mamba hidden state carries correctly across processBlock() calls
- [ ] Cmake build succeeds with `--preset linux-release` (or platform equivalent)
- [ ] Smoke test passes before and after training resume
- [ ] WASM sandbox denies all imports except explicit whitelist
- [ ] Tool-calling schema validates against JSON Schema and returns safe errors