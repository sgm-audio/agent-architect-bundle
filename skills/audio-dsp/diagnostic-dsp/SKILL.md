---
name: diagnostic-dsp
description: "Use this skill when the user is working on or asking about DSP plugin diagnostics, real-time monitoring, performance telemetry, CPU/X-run logging, CLAP thread-pool extension, debug builds for audio plugins, or profiling DSP code without breaking real-time safety."
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Diagnostic Dsp", "opencode-migrated"]
    related_skills: []
---


# Skill: DSP Plugin Diagnostics & Telemetry

## 1. Overview
Covers instrumentation and diagnostics for real-time audio plugins — measuring per-block latency, CPU load, X-run (underrun/overrun) detection, parameter smoothing glitch detection, and DSP state logging. Focuses on non-intrusive telemetry that doesn't violate real-time safety.

## 2. Core Functionality
- **Per-Block Timing:** `QueryPerformanceCounter` (Win) / `mach_absolute_time` (macOS) / `clock_gettime(CLOCK_THREAD_CPUTIME_ID)` (Linux) — measure `processBlock()` duration
- **X-Run Detection:** Tracking `processBlock()` against wall clock — fire warning callback when block takes longer than `frames / sampleRate * safety_margin`
- **CPU Load Estimation:** Rolling average of block processing time vs available budget — flag at 70%/85%/95% thresholds
- **Parameter Smoothing Glitch Detection:** Log `sample_rate * delta_param` — detect clicks from unsmoothed parameter changes
- **Memory Diagnostics:** `mallinfo` / `malloc_stats` — non-RT-safe, gated behind `#if JUCE_DEBUG`
- **CLAP Thread-Pool Extension:** `CLAP_EXT_THREAD_POOL` for parallel DSP tasks, measuring per-task dispatch and completion
- **Real-Time Safe Logging:** SPSC ring buffer of diagnostic events → background thread writes to file or telemetry socket
- **Plugin Console:** `OutputDebugString` (Win), `os_log` (macOS), `stderr` (Linux) — for debug-build logging

## 3. Input/Output Schema
| Inputs | `processBlock` entry/exit times, block size, sample rate, parameter change delta, thread-pool task durations |
| Outputs | JSON/CSV telemetry log, per-block timing histogram, X-run event stream, CPU load % over time |
| Storage | SPSC lock-free ring buffer (`MoodyCamel::ReaderWriterQueue` or custom `boost::lockfree::spsc_queue`) |

## 4. Architecture
Diagnostic producers (timers, counters) run on the audio thread and write events into a fixed-size, lock-free SPSC queue. A low-priority background consumer thread drains the queue and writes to a file, sends over UDP, or prints to console. The consumer is never on the critical path. Configuration (enabled levels) is read atomically from `std::atomic<uint32_t>` flags.

## 5. Dependencies
`std::chrono` (high_resolution_clock), `std::atomic`, custom SPSC or `readerwriterqueue` (MoodyCamel), optional: `nlohmann/json` for formatting

## 6. Edge Cases
| Ring Buffer Overflow | Too many events in one block | Drop oldest events (`try_enqueue`), increment overflow counter |
| Timestamp Wrapping | `QueryPerformanceCounter` 49.7 day wrap | Use deltas from session start, not absolute times |
| Thread Pool Starvation | Diagnostic consumer competes with audio | Set consumer `SetThreadPriority(THREAD_MODE_BACKGROUND_BEGIN)` |
| Release Build Telemetry | Overhead in shipping plugin | Gate behind `JUCE_DEBUG` / `_DEBUG` preprocessor, disable in Release |
| Block Called With Zero Frames | Host flushes on parameter change | Guard division by zero: `if (frameCount == 0) return` |

## 7. Constraints
- Never allocate (malloc/new), lock (mutex), or call blocking I/O on the audio thread
- SPSC queue must be pre-allocated at init (size determined by `maxExpectedEvents * maxBlockCount`)
- Timers must use `std::chrono::steady_clock` (monotonic, never jumps)
- Diagnostic overhead must stay < 1% of block processing budget
- Telemetry disabled by default in Release builds — enabled via `MAMBA3_DIAGNOSTICS=1` env var

## 8. Usage
- *Prompt:* "Add per-block CPU timing diagnostics to my CLAP plugin using an SPSC ring buffer."
- *Prompt:* "Detect X-runs from the audio thread and write them to a real-time-safe log."
- *Prompt:* "Profile the CLAP thread-pool extension dispatches in my spectral processor."
- *Prompt:* "Log parameter changes that cause audible clicks due to insufficient smoothing."

## 9. Testing
- Build with `-DMAMBA3_DIAGNOSTICS=ON` and run in a DAW with stress-test (low buffer, many instances)
- Verify no X-runs are reported with buffer > 256 samples at 44.1kHz
- Check SPSC queue never overflows with `--log-overflow-events`
- Run `rg "malloc|free|new|delete|mutex" src/diagnostics/` — must have zero matches in processBlock path

## 10. Best Practices
- Use `std::chrono::steady_clock::now()` for timestamps, store as `int64_t` nanoseconds
- Struct per event type (TimingEvent, XRunEvent, ParamGlitchEvent) to minimize ring buffer overhead
- Pre-allocate ring buffer at `prepareToPlay()` size = `sampleRate / blockSize * 100` (~100 blocks of headroom)
- Wrap diagnostics behind `if constexpr (enableDiagnostics)` for zero-cost in Release builds
- Export diagnostic data as JSON Lines (`.jsonl`) for easy ingestion into analysis tools
- For production telemetry: use UDP send (non-blocking) or write to shared memory for an external process
*Skill Version: 1.0.0 | Standards: RT-Safe, SPSC, CLAP Thread-Pool | Domain: Plugin Instrumentation*
