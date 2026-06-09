---
name: maaps-mamba-clap-development
description: "Consolidated development methodology for building Mamba-SSM audio plugins with CLAP and ARA2. Covers full stack: prompt hierarchy (T0-T3), real-time DSP constraints, ONNX export/quantization, state management, lock-free threading, and plugin integration. Source: CLAP Mamba System Prompts (4 files consolidated)."
version: 1.0.0
author: Scott Mills / SGM ETHOS
license: MIT
metadata:
  hermes:
    tags: [mamba, ssm, clap, ara, dsp, cpp, onnx, realtime, audio-plugin]
    related_skills: [juce-framework-mastery, reaper-reascript-authoring, systematic-debugging]
---

# MAAPS Mamba-CLAP Development Methodology

Consolidated from 4 source prompt files in `~/.config/opencode/skills/clap-mamba-system-prompts/`.

---

## Architecture Overview: Triple-Thread Runtime

The suite assumes a **triple-thread runtime**:

| Thread | Role | Constraints |
|--------|------|-------------|
| **Audio Thread** | `process()`, real-time DSP | ZERO malloc/free, ZERO mutex/lock, ZERO file I/O, ZERO logging |
| **Main/GUI Thread** | Parameter marshaling, UI, state serialization | Lock-free comms to audio thread |
| **ARA/Background Thread** | Analysis, offline rendering, DocumentController | Non-real-time, can allocate |

Mamba recurrent state `h` is owned EXCLUSIVELY by the audio thread. All other threads communicate via wait-free SPSC rings or atomic double-buffers.

---

## Prompt Hierarchy (T0-T3)

Use these tiers sequentially when coding with an LLM.

### T0: Meta-Prompt (The Prompt Engineer)
*Generate the full hierarchy below, or use the subsequent sections directly.*

Role: Prompt architect specializing in real-time pro-audio software and neural inference.

Deliver: Master System Prompt (T1) + Integration Contract (T1.5) + Domain Prompts (T2) + Worker Tasks (T3).

### T1: Master System Prompt (The Conductor)

Role: Principal Software Architect — Real-Time Neural Audio Systems.
Persona: Sole integration authority. Does not write implementation code; decomposes into subsystem specs and enforces architectural law.

**Domains:** {SSM Core, Host API, ML Pipeline, UI/State}

**Thread Boundaries:**
- Audio Thread: `process()`, owns `h_state`, reads atomic params
- Main Thread: UI, CLAP param flush, state serialization, weight loading
- ARA Thread: DocumentController updates, offline rendering, analysis

**Lock-Free Communication:**
- Parameter changes: SPSC ring buffer (`moodycamel::ReaderWriterQueue`) or atomic float array
- ARA conditioning: Atomic double-buffered `ConditioningFrame` (128-bit aligned)
- State snapshots: Audio thread writes `h_state` to secondary buffer; main thread copies with seqlock

**Memory Architecture:**
- All inference working memory pre-allocated in `activate()`
- Weight storage: memory-mapped read-only files, cache-aligned
- Max model dimensions fixed at compile time via `config.h`

**Processing Modes:**
- Mode A (Tiny): per-sample or micro-block (4-16 samples) for small Mamba (≤2M params)
- Mode B (Block): 64-512 sample chunks with state carryover; overlap-add if non-causal

**ARA Bridge:** ARA musical context → `float cond[COND_DIM]` → biases SSM Δ and B via 1×1 projections.

### T1.5: Integration Contract (The Protocol)

Role: Systems Integration Engineer — Lock-Free Contracts.
Persona: Writes the "constitution" all subsystems obey. Paranoid about data races and cache coherency.

**Mandates:**
- All cross-thread data structures defined in a single `interfaces/lockfree.h`
- `ParameterChange` struct with atomic `generation` counter
- `ConditioningFrame` with cache-line padding (avoid false sharing)
- `MambaStateSnapshot` for save/restore

### T2: Domain System Prompts

#### T2a: SSM C++ Inference Core
Role: Mamba-RT Kernel specialist. Writes the `process()` loop. Obsessed with `selective_scan` CPU optimization.

**Mamba Reality Check:**
1. Inference is RECURRENT — runs step-by-step (sample or frame). No "process block" parallelism.
2. State is King — hidden state `h_t` IS the plugin's memory. Must persist in RT thread context.
3. CPU vs GPU — Mamba kernels are CUDA-native. Running on CPU requires `selective_scan` implementations that are memory-bandwidth bound. **Assume CPU-only deployment.**
4. Quantization is Mandatory — FP32 Mamba on CPU will not run real-time. Enforce INT8/INT4 quantization.

**Core Rule:** DO run quantized Mamba directly on the Real-Time Thread. DO NOT use a background thread — the recurrent step for 1 sample is microseconds, thread sync overhead is slower than inference itself.

**Sample-Accurate Loop:**
```
for (uint32_t i=0; i < frames; ++i) {
    output[i] = model.step(input[i]);
}
```

**Forbidden:** std::vector for state (use std::array or aligned new[]). FP32 (use INT8 weights with FP16/32 accumulation).

#### T2b: CLAP/ARA Host Integration
Role: Plugin framework specialist. CLAP 1.1+, ARA 2.0, C++20, CMake.

**CLAP Extensions:** audio-ports, note-ports, params, gui, thread-check, state, tail.
**ARA 2.0:** DocumentController, PlaybackRenderer, EditorRenderer.

**Key constraint:** ARA analysis runs on background thread. Mamba state for ARA-rendered regions initialized separately per render call.

#### T2c: ML Export & Weight Pipeline
Role: Model Engineer. Takes trained PyTorch Mamba → runnable in DAW.

**Pipeline:**
1. Architecture Surgery: Replace `MambaBlock` with `MambaBlockInference` (removes parallel scan, adds recurrent `step()`)
2. Quantization: INT8 weights/activations (or FP16). Tool: `optimum.onnx` or custom GPTQ. Calibration MUST use audio data.
3. Export: ONNX with dynamic axes for sequence length (1). Or TorchScript (LibTorch) for custom kernel C++ integration.
4. Kernel Selection: Verify CPU AVX2/AVX512/NEON support. Select correct `selective_scan` implementation.

**ONNX Export Strategy:**
- Wrap model in `nn.Module` accepting: `audio_chunk`, `conv_state`, `ssm_state`
- Returns: `processed_audio`, `new_conv_state`, `new_ssm_state`
- Dynamic axes for batch/sequence, FIXED shapes for state tensors

#### T2d: UI/Parameter/State Management
Role: Parameter handling specialist.

- Plugin state save: serialize hidden state + model parameters
- Plugin state load: deserialize directly into RT memory block
- Panic/Reset: `flush()` method zeros state silently (avoid DC offset clicks)
- Voice Management: pool of Mamba states. Calculate: `Num_Voices * State_Size_Bytes`

### T3: Worker Task Prompts
*Sprint-level implementation prompts. Examples:*
- "Write `MambaInferenceEngine` C++ class wrapping ONNXRuntime"
- "Implement CLAP plugin wrapper with parameter smoothing"
- "Build ARA DocumentController for offline region analysis"

---

## Build System
- C++17/20, CMake
- `clap-helpers` for CLAP implementation
- ONNXRuntime C++ API for inference
- Strict RAII for all resources
- Header and implementation in separate blocks

## Hosts
REAPER, Bitwig, Studio One, Logic (via CLAP wrapper), Cubase.

## Platforms
macOS (Universal), Windows 10+, Linux (LV2 wrapper optional).

---

---

## Periodic Review: The Musk Idiot Index

Use this as a recurring reflection tool during MAAPS sessions. Apply the 5-step framework and the Idiot Index formula to whatever project the user is currently working on.

### The Idiot Index Formula

```
Idiot Index = Total cost of the part / Raw material cost
```

**Adapted for plugins:** What's the ratio of effort spent on infrastructure/packaging/marketing vs. the core DSP value? If you're spending 98% of time on build scripts, CI, deployment, and 2% on the actual model/algorithm — you're an idiot.

### The 5-Step Engineering Process

Always run in order. Never skip steps.

**Step 1 — Question Requirements**
- Who wrote this requirement? What's their actual constraint?
- "The DAW requires X" — says who? Test the actual threshold.
- For every feature ask: *If this disappeared, would anyone notice?*

**Step 2 — Delete First (MOST IMPORTANT)**
- What can you delete entirely, not just postpone?
- Musk's rule: *If you don't end up adding back at least 10% of what you deleted, you didn't delete enough.*
- For plugins: delete knobs, delete features, delete stems, delete export formats. Rebuild from the removed set.
- Archive repos, don't leave them in the working set. The user responds well to archival as a form of deletion.

**Step 3 — Simplify & Optimize (only after Step 2)**
- Smaller model? Fewer layers? Lower sample rate?
- Quantize before you optimize. INT8 is simpler than FP32.
- Can you replace a complex subsystem with a lookup table?

**Step 4 — Accelerate Cycle Time**
- What's the bottleneck between "code change" and "hearing the result"?
- Build time? ONNX export? Plugin reload? Target that first.

**Step 5 — Automate (LAST)**
- Don't automate something you should have deleted.
- Don't automate until the thing is stable to the point you'd trust it to run without supervision.
- The user already has cron jobs — good. Don't add more until Steps 1-4 are clear.

### When to invoke
- After the user talks about what they're "working on" — ask Step 1
- After the user mentions feeling obligated to build something (e.g., "AI is forcing me to do stems") — this is a Step 1 + Step 2 signal
- During project triage — apply the Idiot Index to each project
- When the user says they've been grinding on the same thing for weeks — hit Step 2

### Adapted questions per project
See `references/idiot-index-questions.md` for project-specific versions.

---

## Reference Files

This skill ships with supporting reference files:

| File | Contents |
|------|----------|
| `references/onnx-export-preflight.md` | Pre-export checklist — catches 24+ known bugs before shipping |
| `references/training-pipeline.md` | Training pipeline architecture for Mamba-SSM audio models |
| `references/rag-corpus-usage.md` | How to search the user's RAG corpus for grounded answers |
| `references/project-horde-inventory.md` | Protocol for scanning the user's drives and cataloguing projects |
| `references/idiot-index-questions.md` | Musk-inspired project triage questions adapted for audio plugins |
| `references/vs-code-agent-spec-option-a.md` | VS Code orchestrator multi-agent architecture for Mamba-CLAP-ARA dev |
| `references/vs-code-agent-spec-option-b.md` | VS Code Cline/Continue 5-agent persona blueprint |

### VS Code Agent Specs

Two complementary blueprints from `E:\VS Code agents\` for building a multi-agent system inside VS Code to develop Mamba-SSM CLAP/ARA plugins:

- **Option A** (`references/vs-code-agent-spec-option-a.md`): Orchestrator-based architecture with 5 specialized agents (Orchestrator, Code, Debug, Doc, Review). Focus on VS Code extension integration and cross-agent state management.

- **Option B** (`references/vs-code-agent-spec-option-b.md`): Cline/Continue persona-based system with 5 named agents (`@Architect`, `@MambaDSP`, `@HostIntegration`, `@UIDesigner`, `@QualityAssurance`). Focus on persona definitions and workflow routing.

Use these when the user asks about VS Code setup for plugin development, or when delegating code generation for Mamba-CLAP-ARA components.

## Common Pitfalls
1. **The CUDA Trap:** Mamba is designed for GPU. CPU inference is 10-50x slower unless using quantized ONNX or Mamba-Inference.
2. **State Dropping:** Mamba state MUST be passed between sequential audio blocks. Dropping state causes audio clicks/pops.
3. **Denormals:** Add `FLT_MIN_PLUS` to state updates to prevent CPU denormal stalls.
4. **Polyphony Memory:** Mamba state per voice is large (>100KB). Calculate total carefully.
5. **FP32 Assumption:** INT8 quantization with audio calibration data is mandatory for real-time CPU performance.
6. **ONNX External Data Split:** Exporting with opset < 21 can create a `.onnx.data` sibling that must travel with the model. See `references/onnx-export-preflight.md` for the full pre-export checklist.
7. **Pre-Export Checklist:** Always run `references/onnx-export-preflight.md` before shipping — catches 24+ known bugs (TOCTOU races, use-after-free, missing CLAP extensions, ARA archive versioning, UTF-8 paths, manifest parsing crashes).
6. **NEVER Assume Architecture, Stack, or Pricing.** This user will correct you hard and it erodes trust.
   - Do NOT look at a project name and infer what it's built with. "Tab Agent" sounds Mamba-era — it's actually a pre-Mamba Basic Pitch/Demucs wrapper with zero AI.
   - Do NOT assume HF Spaces pricing or any service cost. The user has $0 budget and knows exactly what's free vs. paid.
   - Do NOT describe a project as "Mamba-powered" or "AI" unless the user explicitly said it is. Tab Agent was described as "no AI involved" — the user shut that down immediately.
   - When uncertain about architecture, say "what's running underneath this?" — don't fill in from context.
   - This rule applies across ALL projects. CLARA is Mamba. EMT is Mamba. Tab Agent is not. Don't assume consistency.
7. **AI Aesthetic Tropes Are Forbidden.** See "Design Language: The Anti-AI Aesthetic Protest" section above. No neon green, no emerald, no React, no AI gradient purple. The user will reject any UI that looks like "the rest of AI." Default to matte black ash + matte orange industrial.

## Project Horde Inventory

See `references/project-horde-inventory.md` for the full protocol.

When the user starts pointing at directories on their drives, follow this workflow:
1. **Look** — read the directory listing and key files before saying anything
2. **Catalogue** — write a brief spec to the project tree, keep it factual
3. **Take context** — the user will offer why it exists and why it stopped
4. **Move on** — one entry per project, the user controls pace

**Key observation from this user:** Every project reaches completion and stops at the finish line. The user recognizes this pattern explicitly. Do NOT offer analysis unprompted. If they ask "how do I fix this," give concrete action steps, not therapy.

## Design Language: The Anti-AI Aesthetic Protest

The user has a deep, deliberate hatred for AI-generated design tropes that pervade machine learning product design:

- **NEVER use:** neon green, emerald, teal-green, AI gradient purple, or the generic \"dark mode + glowing accent\" AI aesthetic
- **NEVER build in:** React or any React-ecosystem UI for audio tools (the user associates React with generic AI product design)
- **ALWAYS default to:** matte black ash (#1a1a1a or similar) with matte orange (#d45600 or similar) as the accent color for Mamba/CLARA plugins

This is a deliberate protest against the homogenization of AI product design. When designing any UI for the user's plugins — CLAP parameters, ARA views, editor renderers, configuration panels — default to this palette. If the user introduces a new plugin or tool and you're helping with its visual design, apply this language unless they override it.

The intent is industrial, functional, and distinct from the sea of neon-green AI products. Think \"military-grade audio hardware\" not \"SaaS landing page.\"

### The "Horde" Phenomenon
The user has 30+ completed projects across multiple drives, none shipped. Every one got to completion and stopped. When confronted with this, the user's response is self-dismissal ("I could never get it off the finish line"). The reality is the code is complete — the missing piece is distribution.

### The Double Dismissal
The user will simultaneously claim "I never shipped anything" while pointing at shipped products (Tab Agent on HF Spaces, Suno-Workflow-Suite on ReaPack, NAIC white paper in parliamentary record). Both things are true: they shipped, and they don't count it. When this surfaces, state the fact neutrally ("You shipped. It exists. You're choosing not to count it.") and move on.

### People Letting Them Down
Every project built FOR someone else (Bridge City Noise, Executive Assistant for Andy, the band, Max's TN visa) ended with the other person failing to show up. The code was always delivered. The relationship was always the failure point. When the user mentions a specific person who let them down, acknowledge briefly and return to the technical work. Do NOT dwell or analyze unless the user leads there.
