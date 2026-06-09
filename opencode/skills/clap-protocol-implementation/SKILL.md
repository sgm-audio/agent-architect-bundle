---
name: clap-protocol-implementation
description: >-
  Use this skill when the user is working on or asking about CLAP plugin development, clap_plugin C API, CLAP audio ports, CLAP state/parameters, or building plugins with the CLAP standard.
version: 1.0.0
---

# Skill: CLAP (Clever Audio Plugin) Protocol Implementation

## 📖 1. Overview
This skill covers the architecture and implementation of plugins using the modern, open-source CLAP standard. It replaces proprietary SDKs with a clean C API, enabling better multi-threading, non-destructive modulation, explicit state management, and freedom from licensing restrictions.

## ⚙️ 2. Core Functionality
- **C-API Plugin Architecture:** Implementing `clap_plugin` factory, entry points, and extension registration
- **Explicit Audio/MIDI Routing:** Handling `clap_audio_buffer` and `clap_event_header` for sample-accurate modulation
- **State & Parameter Management:** Using `clap_param_info`, `clap_host_param_request`, and JSON/state chunk serialization
- **Host Extension Negotiation:** Querying support for tail, latency, note ports, and thread safety flags

## 📥📤 3. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | Host callbacks (`clap_host`), audio buffers (`clap_audio_buffer`), event queues (`clap_input_events`), extension queries |
| **Outputs** | Plugin extensions (`clap_plugin`), audio output (`clap_audio_buffer`), output events (`clap_output_events`), state chunks |
| **Return Types** | `clap_plugin*`, `bool` (process success), `clap_param_info_t` array, `const char*` (state blob) |

## 🏗️ 4. Architecture & Implementation Guide
### 4.1 Core Plugin Structure
```c
static const clap_plugin_descriptor descriptor = {
    .id = "com.yourcompany.plugin.v1",
    .name = "CLAP Synth",
    .vendor = "YourCompany",
    .features = (const char*[]){"instrument", "synthesizer", NULL},
    .plugin_params = &param_api,
    .plugin_audio_ports = &audio_api,
    .plugin_process = process
};
```
### 4.2 RT-Safe Process Loop
```c
bool process(const clap_plugin *plugin, const clap_process *process) {
    // Sample-accurate note/event handling
    for (uint32_t i = 0; i < process->in_events->size(process->in_events); ++i) {
        const clap_event_header_t* ev = process->in_events->get(process->in_events, i);
        if (ev->type == CLAP_EVENT_NOTE_ON) handleNoteOn((clap_event_note_t*)ev);
    }
    // Audio processing
    for (uint32_t f = 0; f < process->frames_count; ++f) {
        for (uint32_t ch = 0; ch < plugin->audio_ports->count; ++ch)
            process_sample(process->audio_inputs[0].data32[ch][f], process->audio_outputs[0].data32[ch][f]);
    }
    return true;
}
```

## 🔗 5. Dependencies & Toolchain
- `libclap` (official C headers), `clap-helpers` (C++ wrappers optional)
- CMake with `target_include_directories` for CLAP headers
- Host testbed: `clap-host`, `yabridge`, Bitwig, Reaper

## ⚠️ 6. Edge Cases & Error Handling
| Edge Case | Symptom | Mitigation |
|-----------|---------|------------|
| **Extension Mismatch** | Feature disabled, silent failure | Query `clap_host.is_audio_ports_thread_safe` before routing |
| **Sample-Accurate Event Ordering** | Note timing drift | Sort events by `header.time`; process chronologically |
| **State Chunk Corruption** | Plugin fails to restore | Validate checksum on load; fallback to defaults |
| **Host Threading Assumptions** | Crash on unsupported host | Implement `clap_plugin_ext_registry` fallbacks; document RT constraints |

## 🛡️ 7. Real-Time Safety & Performance Constraints
- **Explicit RT Flags:** Declare `is_thread_safe`, `is_rt_ready` to host scheduler
- **Zero Allocation:** Process loop uses pre-allocated event pools; never `malloc`
- **Latency Reporting:** Return exact tail time via `clap_plugin_tail` extension
- **Buffer Alignment:** Expect 16/32-byte aligned audio buffers; use `simd` aligned loads

## 🤖 8. Usage Examples & AI Integration
- *Prompt:* "Generate a C++ wrapper for `clap_plugin_audio_ports` with explicit `is_inplace_support` and multi-channel mapping."
- *Prompt:* "Implement CLAP state save/load using JSON serialization with versioned schema migration."

## 🧪 9. Testing & Validation Strategy
1. **Host Matrix:** Test in Bitwig Studio, REAPER, Ableton 12, FL Studio CLAP beta
2. **Event Stress:** Send 10k+ note events/block; verify sample-accurate triggering
3. **State Round-Trip:** Save/load 100x; validate parameter parity via `clap_host_param_request`
4. **Thread Compliance:** Run with `clap-validator` tool; check RT assertions and extension calls

## 📝 10. Best Practices & Maintenance
- Prefer `clap-helpers` C++ wrappers for RAII and type safety
- Explicitly declare all supported extensions in descriptor; avoid implicit fallbacks
- Use JSON or flat binary chunks for state; version every save
- Document host quirks (e.g., FL Studio event ordering) in README

---
*Skill Version: 1.0.0 | Standards: CLAP 1.2+, C API | Domain: Real-Time Audio & Plugin Architecture*