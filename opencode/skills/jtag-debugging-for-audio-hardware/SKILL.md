---
name: jtag-debugging-for-audio-hardware
description: >-
  Use this skill when the user is working on or asking about JTAG debugging, OpenOCD, hardware debug probes, debugging embedded audio firmware, or ARM SWD debugging.
version: 1.0.0
---

# SKILL: JTAG Debugging for Audio Hardware

## CAPABILITIES
- Debug hardware audio systems using JTAG/SWD interfaces
- Trace real-time audio processing and identify timing violations
- Inspect register contents and memory during audio stream processing
- Set hardware breakpoints and watchpoints for deterministic debugging
- Analyze power consumption and clock behavior during audio operations

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Hardware target specifications (CPU, debug interface) | Debugger connection and configuration |
| Audio processing symptoms (glitches, dropouts, latency) | Root cause analysis and debugging session |
| Breakpoint/watchpoint requirements | Conditional breakpoints and data tracing |
| Performance analysis needs (timing, profiling) | Execution traces and timing reports |
| Memory inspection requirements | Register dumps and memory content analysis |

## IMPLEMENTATION PATTERN

```c
// Example: Debug-enabled audio processing code for JTAG analysis
#include <stdint.h>
#include <stdbool.h>

// Debug configuration macros
#define DEBUG_ENABLED 1
#define DEBUG_GPIO_PORT   GPIOA
#define DEBUG_GPIO_PIN    GPIO_PIN_5
#define DEBUG_TOGGLE()    HAL_GPIO_TogglePin(DEBUG_GPIO_PORT, DEBUG_GPIO_PIN)

// Audio processing state with debug hooks
typedef struct {
    uint32_t sampleCount;
    uint32_t underrunCount;
    uint32_t overrunCount;
    uint32_t maxProcessTime;
    uint32_t minProcessTime;
    uint32_t lastProcessTime;
    bool     debugFlag;
} AudioDebugState_t;

static AudioDebugState_t gDebugState;

// Initialize debug state
void audio_debug_init(void) {
    gDebugState.sampleCount = 0;
    gDebugState.underrunCount = 0;
    gDebugState.overrunCount = 0;
    gDebugState.maxProcessTime = 0;
    gDebugState.minProcessTime = 0xFFFFFFFF;
    gDebugState.lastProcessTime = 0;
    gDebugState.debugFlag = false;
    
    // Configure debug GPIO (if using GPIO toggling for timing analysis)
    #ifdef USE_DEBUG_GPIO
    __HAL_RCC_GPIOA_CLK_ENABLE();
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = DEBUG_GPIO_PIN;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(DEBUG_GPIO_PORT, &GPIO_InitStruct);
    #endif
}

// Audio processing function with debug instrumentation
void audio_process_callback(int16_t* inputBuffer, int16_t* outputBuffer, uint32_t numSamples) {
    uint32_t startTime, endTime, processTime;
    
    // Start debug timing
    #ifdef USE_DEBUG_GPIO
    DEBUG_TOGGLE();  // Toggle GPIO to mark start
    #endif
    startTime = DWT->CYCCNT;  // ARM Cortex-M cycle counter
    
    // Process audio samples
    for (uint32_t i = 0; i < numSamples; i++) {
        // Simple gain example (replace with your DSP)
        int32_t sample = inputBuffer[i];
        sample = (sample * 3) / 2;  // 1.5x gain
        if (sample > 32767) sample = 32767;
        if (sample < -32768) sample = -32768;
        outputBuffer[i] = (int16_t)sample;
    }
    
    // End debug timing
    endTime = DWT->CYCCNT;
    #ifdef USE_DEBUG_GPIO
    DEBUG_TOGGLE();  // Toggle GPIO to mark end
    #endif
    processTime = endTime - startTime;
    
    // Update debug statistics
    gDebugState.sampleCount += numSamples;
    gDebugState.lastProcessTime = processTime;
    if (processTime > gDebugState.maxProcessTime) {
        gDebugState.maxProcessTime = processTime;
    }
    if (processTime < gDebugState.minProcessTime) {
        gDebugState.minProcessTime = processTime;
    }
    
    // Check for buffer underrun/overrun conditions (example)
    if (gDebugState.debugFlag) {
        // Additional debug processing when flag is set
        // This could be triggered by a watchpoint or breakpoint
    }
}

// Debug monitoring task (RTOS) or main loop polling
void audio_debug_monitor(void) {
    static uint32_t lastSampleCount = 0;
    uint32_t currentSampleCount = gDebugState.sampleCount;
    
    // Calculate audio buffer rate
    uint32_t samplesPerSecond = currentSampleCount - lastSampleCount;
    lastSampleCount = currentSampleCount;
    
    // Check for anomalies
    if (samplesPerSecond == 0) {
        // Possible underrun - no samples processed
        gDebugState.underrunCount++;
    }
    
    // Periodic debug output (every second)
    static uint32_t lastDebugTime = 0;
    uint32_t currentTime = HAL_GetTick();
    if (currentTime - lastDebugTime >= 1000) {
        // Output debug statistics via UART, SWO, or semihosting
        debug_printf("Audio Stats: %lu samp/s, %lu underruns, max time: %lu cycles\n",
                     samplesPerSecond, gDebugState.underrunCount, gDebugState.maxProcessTime);
        lastDebugTime = currentTime;
    }
}

// JTAG breakpoint handlers (compiler-specific)
void __attribute__((weak)) DebugMon_Handler(void) {
    // Debug monitor exception - can be used for semi-hosting or custom debug actions
    gDebugState.debugFlag = true;
    // Execute debug actions here
}

// Example: Using data watchpoints to detect buffer corruption
// Set watchpoint on audio buffer via JTAG debugger to catch overflows
```

## EDGE CASES & FALLBACKS
- **No JTAG Available**: Fall back to printf debugging, GPIO toggling, or LED indicators
- **Heisenbug Effect**: Debugging changes timing; use non-intrusive trace methods (SWO, ETB)
- **Optimization Removes Variables**: Use `volatile` or `__attribute__((used))` for debug variables
- **Interrupt Masking**: Ensure debug code doesn't disable interrupts for too long
- **Memory Overhead**: Minimize debug structures in production builds
- **Security Concerns**: Remove debug interfaces in production firmware or secure them
- **Trace Buffer Overflow**: Configure circular tracing or trigger-based capture
- **Clock Cycle Counter Access**: Enable DWT cycle counter via `CoreDebug->DEMCR |= CoreDebug_DEMCR_TRCENA_Msk;`
- **Multi-core Debugging**: Use core-specific debug resources and synchronization

## INTEGRATION POINTS
- Debug Probes: SEGGER J-Link, ST-Link/V2, CMSIS-DAP, TI XDS110, Lauterbach TRACE32
- Debug Interfaces: JTAG (IEEE 1149.1), SWD (ARM Serial Wire Debug), ETM, ITM
- Tracing Technologies: SWO (Single Wire Output), ETB (Embedded Trace Buffer), PTM (Program Trace Macrocell)
- Debugging Tools: GDB with remote server, SEGGER Ozone, Keil MDK, IAR C-SPY, STM32CubeIDE
- Semihosting: Redirect printf to debugger via JTAG
- Trace Analyzers: Percepio Tracealyzer, SEGGER SystemView, ARM Streamline
- Performance Counters: DWT (Data Watchpoint and Trace), PMU (Performance Monitoring Unit)
- Security Features: Debug authentication, secure debug ports, invasive debug disable
- Target Voltage Detection: Automatic voltage detection in debug adapters
- Power Measurement: Current probes, power analysis JTAG adapters

## EXECUTION EXAMPLES

**Input:** "Set up JTAG debugging to measure audio processing interrupt latency"
**Output:**
```c
// Latency measurement with JTAG/GPIO toggling
#define LATENCY_TEST_PIN   GPIO_PIN_6  // Connected to oscilloscope or logic analyzer
#define LATENCY_TEST_PORT  GPIOA

void audio_latency_init(void) {
    // Configure GPIO for latency measurement
    __HAL_RCC_GPIOA_CLK_ENABLE();
    GPIO_InitTypeDef GPIO_InitStruct = {0};
    GPIO_InitStruct.Pin = LATENCY_TEST_PIN;
    GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(LATENCY_TEST_PORT, &GPIO_InitStruct);
}

// In audio interrupt service routine
void AUDIO_IRQHandler(void) {
    // Toggle pin at start of ISR
    HAL_GPIO_TogglePin(LATENCY_TEST_PORT, LATENCY_TEST_PIN);
    
    // Process audio interrupt
    process_audio_interrupt();
    
    // Toggle pin at end of ISR
    HAL_GPIO_TogglePin(LATENCY_TEST_PORT, LATENCY_TEST_PIN);
}

// In main audio processing function
void audio_process(void) {
    // Toggle pin at start of processing
    HAL_GPIO_TogglePin(LATENCY_TEST_PORT, LATENCY_TEST_PIN);
    
    // Process audio buffer
    process_audio_buffer();
    
    // Toggle pin at end of processing
    HAL_GPIO_TogglePin(LATENCY_TEST_PORT, LATENCY_TEST_PIN);
}
```
*On oscilloscope/logic analyzer:*
- Measure time between first toggle pair (ISR latency)
- Measure time between second toggle pair (processing latency)
- Total latency = ISR latency + processing latency

**Input:** "Use data watchpoint to detect audio buffer overflow"
**Output:**
```
# In GDB with SEGGER J-Link:
# Set watchpoint on audio buffer end address
(gdb) watch *0x20001000
Hardware watchpoint 1: *0x20001000

# When buffer overflows and writes past the boundary:
Hardware watchpoint 1: *0x20001000

Old value = 0
New value = 1234
0x08000124 in audio_process () at audio.c:45
45	        outputBuffer[i] = sample;
```