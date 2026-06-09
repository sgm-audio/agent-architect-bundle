---
name: lock-free-concurrency-and-real-time-safety
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Lock Free Concurrency And Real Time Safety", "opencode-migrated"]
    related_skills: []
---


# Skill: Lock-Free Concurrency & Real-Time Safety

## 📖 1. Overview
This skill focuses on designing thread-safe, zero-blocking communication channels between the high-priority real-time audio thread and the non-real-time UI/main thread. It implements Single-Producer/Single-Consumer (SPSC) queues, atomic parameter snapshots, and memory-ordering guarantees to prevent audio dropouts, clicks, and DAW freezes.

## ⚙️ 2. Core Functionality
- **SPSC Ring Buffers:** Wait-free message passing for MIDI events, parameter automation, and state updates
- **Atomic Snapshots & Double Buffering:** Thread-safe parameter exchange using `std::atomic` load/store with proper memory fences
- **Cache-Line Alignment & False Sharing Prevention:** Padding structures to avoid CPU cache contention
- **RT-Safe State Machines:** Implementing non-blocking control flow for modulation, bypass, and mode switching

## 📥📤 3. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | UI parameter changes, MIDI events, host automation curves, thread synchronization signals |
| **Outputs** | Processed parameter buffers, event queues, atomic read flags, drop-out warnings |
| **Return Types** | `bool` (push success/fail), `std::atomic<uint64_t>` (sequence counters), `struct ParamSnapshot` |

## 🏗️ 4. Architecture & Implementation Guide
### 4.1 Atomic Parameter Snapshot Pattern
```cpp
struct alignas(64) ParamSnapshot { // 64B cache line
    float gain{0.5f};
    float cutoff{2000.0f};
    bool bypass{false};
};

class ParamManager {
    std::atomic<bool> updated{false};
    alignas(64) ParamSnapshot rtBuffer{}, uiBuffer{};
public:
    void pushFromUI(float g, float c, bool b) {
        uiBuffer.gain = g; uiBuffer.cutoff = c; uiBuffer.bypass = b;
        updated.store(true, std::memory_order_release);
    }
    ParamSnapshot pullForRT() {
        if (updated.load(std::memory_order_acquire)) {
            rtBuffer = uiBuffer;
            updated.store(false);
        }
        return rtBuffer;
    }
};
```
### 4.2 SPSC Queue Skeleton
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

## 🔗 5. Dependencies & Toolchain
- C++ `<atomic>`, `<memory>`, `<array>`
- JUCE `juce::AbstractFifo`, `moodycamel::ConcurrentQueue` (optional)
- Clang/GCC with `-march=native` for optimal atomic instructions

## ⚠️ 6. Edge Cases & Error Handling
| Edge Case | Symptom | Mitigation |
|-----------|---------|------------|
| **ABA Problem** | Stale pointer reuse, crashes | Use versioned pointers or hazard pointers; avoid raw pointer queues |
| **Memory Reordering** | Inconsistent state reads | Enforce `std::memory_order_acquire/release` pairs on load/store |
| **False Sharing** | Cache thrashing, latency spikes | `alignas(64)` padding for hot variables; group RT data separately |
| **Queue Overflow** | Dropped automation, parameter jumps | Implement bounded queues with drop/overwrite policy; log under load |

## 🛡️ 7. Real-Time Safety & Performance Constraints
- **Zero Locks:** No `std::mutex`, `std::condition_variable`, or `pthread_mutex` in RT path
- **Wait-Free:** Max operations = O(1) regardless of queue size
- **Cache Efficiency:** Pack frequently accessed fields; align to cache lines
- **Budget:** `< 100ns` per push/pop operation at 192kHz / 16 sample block

## 🤖 8. Usage Examples & AI Integration
- *Prompt:* "Generate a C++20 `SpscQueue` with `std::atomic_ref` and `std::memory_order_seq_cst` for high-priority audio event logging."
- *Prompt:* "Implement a double-buffered LFO parameter system with atomic swap on UI thread boundary."

## 🧪 9. Testing & Validation Strategy
1. **ThreadSanitizer (TSan):** Run heavy UI/RT interaction; verify zero data races
2. **Fuzz Testing:** Flood queue with random pushes/pops across threads; validate consistency
3. **Latency Profiling:** Measure `push()`/`pop()` cycles using `rdtsc`; ensure < 50 cycles
4. **Dropout Simulation:** Intentionally overflow queues; verify graceful degradation, no RT hangs

## 📝 10. Best Practices & Maintenance
- Prefer `std::atomic<T>` with `load()`/`store()` over `fetch_add()` unless needed
- Use `[[gnu::aligned(64)]]` or `alignas` explicitly; document cache layout
- Log queue depth in telemetry; trigger UI warnings at >75% capacity
- Never pass `std::shared_ptr` or heap objects through RT queues; use value types or pre-allocated pools

---
*Skill Version: 1.0.0 | Standards: C++17/20 Atomics, SPSC, JUCE RT-Safe | Domain: Real-Time Audio & Plugin Architecture*