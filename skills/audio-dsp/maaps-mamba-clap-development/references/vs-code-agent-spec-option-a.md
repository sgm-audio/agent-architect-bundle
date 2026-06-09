# VS Code Multi-Agent Spec — Option A: Orchestrator Architecture

Source: `E:\VS Code agents\option a.md` — Added to RAG Jun 2026.

## Overview

Proposed architecture for a system of AI agents embedded in VS Code to streamline Mamba-SSM CLAP/ARA plugin development. Designed as a suite of specialised VS Code extensions coordinated by a plugin-aware orchestrator.

## Agent Roster

### 1. Orchestrator Agent (Hub)
Central coordinator routing tasks to appropriate sub-agents. Maintains project state (target SDK, platform, build config) and cross-agent memory.

- Parses user commands (`@plugin` prefix)
- Routes by intent: `#code` → Code Agent, `#debug` → Debug Agent, `#docs` → Doc Agent
- Stores project-wide context: CLAP version, ARA v2.1, target platform
- Enables concurrent agents for multi-step workflows

### 2. Code Agent (Mamba-SSM + Plugin)
Generates, refactors, and autocompletes C/C++ code integrating Mamba-SSM within CLAP/ARA plugin skeletons.

**Knowledge bases:**
- Mamba-SSM inference patterns (selective scan, state carry, quantization)
- CLAP host extensions (audio-ports, note-ports, params, gui, state, tail, thread-check)
- ARA 2.0 (DocumentController, PlaybackRenderer, EditorRenderer)
- ONNX Runtime / LibTorch C++ API for ML inference
- Lock-free programming patterns

### 3. Debug Agent (Real-Time + ML)
Diagnoses audio-thread violations, real-time crashes, parameter glitches.
- Detects: `malloc`/`free` on audio thread, priority inversion
- Uses: CLAP thread-check extension, latency tracing, state freeze analysis

### 4. Doc Agent
Generates CLAP descriptors, ARA XML schemas, README, plugin manual.
- Extracts from source: parameter definitions via `@clap-param` comments
- Generates: `plugin-descriptor.json`, `ara-schema.xml`, user manual stubs

### 5. Review Agent
Performs pre-commit review focused on:
- CLAP extension compliance checklist
- ARA contract violations
- RT safety (no blocking calls on audio thread)
- Quantization correctness

## Workflow
1. User defines task → Orchestrator
2. Orchestrator dispatches to Code Agent for implementation
3. Debug Agent verifies RT safety on each compile
4. Doc Agent generates docs from source annotations
5. Review Agent runs pre-commit compliance check
