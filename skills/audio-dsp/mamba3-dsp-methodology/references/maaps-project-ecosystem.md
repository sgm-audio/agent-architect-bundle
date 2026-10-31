# MAAPS Project Ecosystem — Master Reference

> **Purpose:** One-stop inventory of every MAAPS project, its real filesystem path, deployment targets, trained models, dataset dependencies, SDK requirements, and integration relationships. Update this file whenever a project's status changes significantly (new checkpoint, new build target, new dataset, path reorganization).

---

## Project Inventory

### CLARA (MambaSuite)

| Field | Value |
|-------|-------|
| **Path** | `/mnt/c/dev/Audio Development/0 CLARA/` |
| **Type** | C++17 CLAP + ARA2 plugin, ONNX Runtime inference |
| **Model** | None trained yet (would be Mamba-3 PerTrackProcessor via ONNX) |
| **SDKs** | CLAP (FetchContent), ARA SDK (vendored at `extern/ARA_SDK/`) |
| **Build** | `cmake --preset linux-release && cmake --build` |
| **Status** | ~25-30% — builds clean, needs conditioning bridge, GUI, CI |
| **Deps fetched** | CLAP SDK (`29ffcc27`), ARA SDK (`1ca0b0aa`), ONNX Runtime 1.17.1 |
| **Key files** | `AGENTS.md`, `ADR-001` through `ADR-008`, `CMakePresets.json` |

### Mamba DAW (the real one — not EmT)

| Field | Value |
|-------|-------|
| **Path** | `/mnt/c/dev/mamba3/mamba3/Mamba Based/MambaDAW/` |
| **Type** | CPU-only C++17 Mamba-SSM CLAP plugin, .mmbw weights, per-sample inference |
| **Trained model** | **✅ best.pt** (8MB, 100K steps) at `/mnt/c/dev/mamba3/mamba3/checkpoints_laptop/` |
| **SDKs** | CLAP (vendored), VST3 (Phase 2), LV2 (Phase 3) |
| **Build** | `cmake -B build -G Ninja . && cmake --build build -j$(nproc)` |
| **Status** | Phase 1 complete (CMake restructure, 13 tests passing). Phase 2-5 pending (VST3/LV2/GUI/CI) |
| **Model architecture** | EffectControllerMamba: mel → 80 logits → EffectDecoder → 17 EffectParamBlock params → DSP chain |
| **DSP chain** | EQ (6-band ZDF), compressor, saturator, reverb, spectral feedback |
| **Tests** | 13 tests: dsp, inference_thread, mamba_layer, param_gate, state_serialization, bench_mamba, latency, noise_floor, soak, cpu_budget, spectral_feedback, alloc_audit, tsan |
| **Key files** | `TODO_LV2_VST3.md`, `python_training/models/effect_controller.py`, `tools/simple_mamba.py` |
| **VST3 skeleton** | `/mnt/c/Users/<user>/OneDrive/Desktop/MambaDAW.vst3/` (empty) |

### EmT (separate from Mamba DAW!)

| Field | Value |
|-------|-------|
| **Path** | `/mnt/c/dev/Audio Development/0 EmT/` |
| **Type** | Mamba-SSM CLAP/ARA prototype (hand-rolled CLAP headers, Euler SSM) |
| **Model** | None trained |
| **Status** | ~15-20% — needs complete SSM rewrite, official CLAP SDK, ARA integration |
| **Note** | **This is NOT the same as Mamba DAW.** EmT is a prototype with hand-rolled CLAP headers and crude math. Mamba DAW has official CLAP SDK, proper SSM discretization, and a 100K-step trained model. |

### Stem Surgeon

| Field | Value |
|-------|-------|
| **Path** | `/mnt/c/dev/Audio Development/Stem Surgeon/stem-surgeon/` |
| **Type** | Monorepo: Python/PyTorch training + JUCE VST3/AU/ARA2 plugin + Rust inference server |
| **Model** | None trained — needs real LAION CLAP encoder export + MUSDB18-HQ training |
| **SDKs** | JUCE (FetchContent), CLAP (FetchContent), ARA (vendored), VST3 |
| **Build** | `just plugin-build` (CMake) |
| **Status** | ~60% — P0-P5 all done, needs real CLAP encoder → training → ONNX export → UI polish |
| **Key files** | `TODO.md` (14 GAPs), `ROADMAP.md`, `AGENTS.md` |

### MambaCompressor

| Field | Value |
|-------|-------|
| **Path** | `/mnt/c/dev/Audio Development/mamba-compressor/` |
| **Type** | Python research — Mamba predicts compressor params (gain, attack, release) via differentiable DSP |
| **Model** | None — pre-alpha, no checkpoint |
| **Status** | README is aspirational. Needs honesty pass → blind pretraining → visualization tool → VST3 plugin |
| **Key insight** | "Mamba predicts parameters, NOT audio. Engineers can SEE the gain envelope." |

### Stem+MIDI Pro

| Field | Value |
|-------|-------|
| **Path** | `/mnt/c/dev/stem_midi_pro/` |
| **Type** | SaaS (FastAPI + NeMo) for guitar/bass stem separation + MIDI transcription |
| **Model** | No checkpoint — fast path to cash flow via Square payments |
| **Status** | Backend exists with 6 runtime-crashing bugs (B1-B6). GTM plan at `~/Downloads/STEMMIDI_GTM_PLAN.md` |
| **Budget** | **$0** — no money, no job. GitHub Actions (free public), OpenRouter free credits, Ollama local |
| **Differentiator** | Expression detection (bends, slides, vibrato) for guitar/bass specifically |
| **GTM timeline** | 30-day window from GTM plan. First: fix bugs → Square payments → async queue → minimal frontend → GCP deploy |

### Mamba-3 Adaptive Filter Bank (Cynical Engineer)

| Field | Value |
|-------|-------|
| **Path** | `/mnt/c/dev/mamba3/mamba3/edge_dsp_meta_prompt/` |
| **Type** | Rust CLAP via nih-plug + ONNX Runtime (ort crate) |
| **Model** | Mamba3Controller — 785K params, 8 spectral bands → 4-layer Mamba-3 MIMO → 32 DSP coeffs |
| **Status** | Architecture complete. Needs: training → ONNX export → `cargo xtask bundle` → Reaper test |
| **Key files** | `compiler/prompt_stack.py`, `compiler/train_controller.py`, `compiler/quantize.py` |
| **Specs** | `specs/prd_cynical_engineer.md`, `specs/prd_intelligent_mix_engine.md`, `specs/prd_precision_surgical_tool.md` |
| **STFT chain** | 1024-pt FFT, 256-hop, 1024-sample latency (23ms @44.1k) |
| **Note** | Rust-based, separate codebase from all C++ projects. NOT the same as the PerTrackProcessor or EffectControllerMamba. |

### Precision Surgical Tool (De-Esser/De-Clicker)

| Field | Value |
|-------|-------|
| **Path** | `specs/prd_precision_surgical_tool.md` within edge_dsp_meta_prompt |
| **Type** | Spec only — zero-crossing aligned micro-fades, sibilance detection |
| **Status** | Not implemented. Would be a separate CLAP plugin sharing Cynical Engineer patterns. |

---

## Model ↔ Project Integration Map

```
┌─ Trained Models ─────────────────────────────────────────────────┐
│                                                                  │
│  checkpoints_laptop/best.pt (8MB, 100K steps)                   │
│  Architecture: EffectControllerMamba                             │
│  Pipeline: Mel → Mamba SSM → 80 logits → EffectDecoder          │
│           → 17 EffectParamBlock params → DSP chain               │
│  Feeds into: Mamba DAW (Mamba Based/MambaDAW/)                   │
│  NOT for: CLARA, Stem Surgeon, Adaptive Filter Bank               │
│                                                                  │
│  mamba3/mamba3/Mamba-3-training/ (failed at 6.5K, archived)      │
│  Architecture: PerTrackProcessor (Mamba-3 MIMO, d_model=256)     │
│  Pipeline: STFT → Mamba-3 backbone → mask heads → iSTFT          │
│  Would feed into: CLARA (via ONNX export) — if training resumes  │
│                                                                  │
│  edge_dsp_meta_prompt/compiler/ (arch complete, untrained)       │
│  Architecture: Mamba3Controller (785K params)                    │
│  Pipeline: Observer features → Mamba-3 → 32 DSP coefficients      │
│  Feeds into: Cynical Engineer (Rust CLAP via nih-plug)            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Datasets

| Dataset | Path | Size | Status |
|---------|------|------|--------|
| MUSDB18-HQ | `/mnt/c/dev/mamba3/mamba3/datasets/musdb18hq/` | ~?GB | Extracted |
| MAESTRO v3.0.0 | `/mnt/c/dev/mamba3/mamba3/datasets/maestro-v3.0.0.zip` | 108GB | ⏳ Downloading (101GB done as of Jun 6) |
| FMA | `/mnt/c/dev/mamba3/mamba3/Mamba Based/Training Datasets/fma/` | ~?GB | Available |
| Slakh2100 | Not yet downloaded | — | Planned (after MAESTRO) |

Note: The training scripts reference `./datasets/musdb18hq/train` (relative to mamba3 dir). The actual data is at the absolute path above. The relative path works when running from `mamba3/mamba3/`.

---

## Shared SDK Repository

| SDK | Path | Used By |
|-----|------|---------|
| CLAP headers | `/mnt/c/dev/mamba3/mamba3/sdks/clap/` | CLARA, Mamba DAW, EmT |
| CLAP helpers | `/mnt/c/dev/mamba3/mamba3/sdks/clap-helpers/` | CLARA |
| ARA SDK | `/mnt/c/dev/mamba3/mamba3/sdks/ARA_SDK/` | CLARA (vendored copy at `0 CLARA/extern/ARA_SDK/`) |
| VST3 SDK | `/mnt/c/dev/mamba3/mamba3/sdks/vst3sdk/` | Stem Surgeon, Mamba DAW (Phase 2) |

---

## Archive Structure

| Archive | Contents | Recoverable? |
|---------|----------|-------------|
| `_archive/MAAPS Builds/` | 14 items — 10+ Nexus duplicates from different agent builds | ✅ Yes, move back |
| `_archive/mamba3-scaffolding/` | JUCE, Jucer, .venv_nightly (local copies, CMake fetches these) | ✅ Yes |
| `_archive/training-failed-runs/` | PerTrackProcessor checkpoints (step 1000-6500, 19.5MB each, 7 files) | ✅ Yes |
| `_archive/agent-stubs/` | .stubs, .sskatoonhub (agent scaffolding) | ✅ Yes |

---

## Tracking System

Three WhatsApp cron jobs deliver status to the user's phone:

| Job | Time | Type | Script |
|-----|------|------|--------|
| maaps-morning | 8:30 AM | no_agent watchdog | `~/.hermes/scripts/maaps-tracker.py` |
| maaps-midday | 12:00 PM | no_agent watchdog | `~/.hermes/scripts/maaps-tracker.py` |
| maaps-evening | 8:30 PM | no_agent watchdog | `~/.hermes/scripts/maaps-tracker.py` |

The tracker checks: OpenCode worker PIDs + uptime, training checkpoints count/latest, dataset availability, ollama model status, provider config. Delivers to WhatsApp self-chat (130620039762).

---

## $0 Budget Operating Model

| Resource | Approach | Cost |
|----------|----------|------|
| CI/CD | GitHub Actions (public repos) | Free |
| LLM API | OpenRouter free credits + DeepSeek ($4 already deposited) | ~$0 ongoing |
| Local inference | Ollama (7 local models, 0 API calls) | Free |
| Workers | OpenCode free tier | Free |
| Model hosting | Hugging Face (open-weight, public) | Free |
| Internet | Vancouver Central Library wifi | Free |
| Compute (training) | Already paid — failed RunPod was $85, no more spending | No new spend |
| Code hosting | GitHub free tier | Free |
| Messaging | WhatsApp self-chat via Hermes gateway | Free |
| Design | Figma free tier (Figma → HTML/CSS export for WebView UI) | Free |
| Cloud deploy | GCP free tier / Cloud Run (if needed for Stem+MIDI Pro) | Free tier limits |
