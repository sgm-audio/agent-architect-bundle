---
name: embedded-linux-audio-programming-bela-elk-audio-os
description: >-
  Use this skill when the user is working on or asking about Bela board, Elk Audio OS, embedded Linux audio, bare-metal audio programming, or low-latency embedded audio systems.
version: 1.0.0
---

# SKILL: Embedded Linux Audio Programming (Bela/Elk Audio OS)

## CAPABILITIES
- Port C++ DSP code to embedded Linux platforms (Bela, Elk Audio OS)
- Achieve sub-millisecond latency audio processing on ARM-based hardware
- Access hardware peripherals (ADCs, DACs, GPIO) for sensor integration
- Develop standalone audio instruments and effects processors
- Optimize real-time performance for deterministic audio processing

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Desktop C++ audio processing code | Cross-compiled embedded Linux binaries |
| Hardware peripheral specifications (ADC/DAC channels) | Sensor-to-audio mapping code |
| Real-time constraints (latency, jitter) | Optimized audio processing loops |
| Audio buffer size requirements | Memory allocation and management strategies |
| Build system configuration | Makefiles/CMake configurations for embedded targets |

## IMPLEMENTATION PATTERN

```cpp
// Bela/Elk Audio OS Real-time Audio Processing Example
#include <Bela.h>  // For Bela
// #include < ElkAudio.h >  // For Elk Audio OS (hypothetical include)

// Audio processing state
struct AudioState {
    float gInPrevious = 0.0f;  // For envelope following
    float gainSmoothed = 0.5f;
    float delayBuffer[DELAY_MAX_SIZE];
    unsigned int delayWritePos = 0;
    // Add your DSP state variables here
};

// Global state (required for real-time audio processing)
AudioState gAudioState;

// Setup function (called once when audio starts)
bool setup(BelaContext *context, void *userData) {
    // Initialize your DSP here
    // Example: initialize delay buffer to zero
    for (unsigned int n = 0; n < DELAY_MAX_SIZE; n++) {
        gAudioState.delayBuffer[n] = 0.0f;
    }
    
    // Initialize any hardware peripherals
    // Example: configure analog inputs
    pinMode(Bela::AnalogInput0, INPUT);
    
    return true;  // Return true if setup was successful
}

// Render function (called for every audio block)
void render(BelaContext *context, void *userData) {
    // Process audio frames
    for (unsigned int n = 0; n < context->audioFrames; n++) {
        // Read audio input (stereo example)
        float inLeft  = audioRead(context, n, 0);
        float inRight = audioRead(context, n, 1);
        
        // Example DSP: simple delay with feedback
        // Read from delay buffer
        float delayed = gAudioState.delayBuffer[gAudioState.delayWritePos];
        
        // Process input (simple mix of dry and delayed signal)
        float outLeft  = inLeft  * 0.5f + delayed * 0.5f;
        float outRight = inRight * 0.5f + delayed * 0.5f;
        
        // Write to delay buffer (with feedback)
        gAudioState.delayBuffer[gAudioState.delayWritePos] = 
            inLeft * 0.7f + delayed * 0.3f;  // Input plus delayed feedback
        
        // Advance write position (with wraparound)
        gAudioState.delayWritePos++;
        if (gAudioState.delayWritePos >= DELAY_MAX_SIZE) {
            gAudioState.delayWritePos = 0;
        }
        
        // Write audio output
        audioWrite(context, n, 0, outLeft);  // Left channel
        audioWrite(context, n, 1, outRight); // Right channel
        
        // Optional: process control signals (e.g., from potentiometers)
        // Every few frames, read analog controls to update parameters
        if (n % 100 == 0) {  // Read controls less frequently to save CPU
            float potValue = analogRead(context, n / 100, 0);  // Read first analog input
            // Map potValue (0.0-1.0) to your parameter range
            // Example: control delay feedback amount
        }
    }
}

// Cleanup function (called when audio stops)
void cleanup(BelaContext *context, void *userData) {
    // Free any allocated resources
    // Nothing to cleanup in this simple example
}
```

## EDGE CASES & FALLBACKS
- **Buffer Underruns**: Increase audio frame size, optimize DSP code, or reduce CPU load
- **Sample Rate Mismatch**: Resample audio between different rates using lightweight algorithms
- **Hardware Initialization Failure**: Implement fallback to software-only mode or safe defaults
- **Memory Constraints**: Use static allocation instead of dynamic where possible
- **GPIO Conflicts**: Check pin multiplexing settings in device tree or board configuration
- **Real-time Priority Issues**: Ensure audio thread has highest priority, avoid blocking calls
- **Power Management Interference**: Disable CPU frequency scaling during audio processing
- **Audio Clicking**: Implement proper parameter smoothing to avoid zipper noise

## INTEGRATION POINTS
- Development Platforms: Bela, Elk Audio OS, Raspberry Pi with real-time kernel, BeagleBone Black
- Audio Codecs: TI TLV320AIC3106 (Bela), WM8731, AK4558
- Development Environments: Eclipse, VS Code with remote debugging, command-line make
- Debugging Tools: printf to UART, oscilloscope, logic analyzer, JTAG/SWD
- Libraries: Bela SDK, ALSA, JACK, SuperCollider, Pure Data, Csound
- Hardware Interfaces: Analog inputs/outputs, digital I/O, I2C, SPI, UART, USB
- Build Systems: Makefile, CMake with cross-compilation toolchains (arm-linux-gnueabihf)

## EXECUTION EXAMPLES

**Input:** "Create a tremolo effect with LFO rate controlled by potentiometer"
**Output:**
```cpp
#include <Bela.h>

// Tremolo state
struct TremoloState {
    float phase = 0.0f;
    float frequency = 5.0f;  // Hz
    float depth = 0.8f;      // 0.0 to 1.0
} gTremoloState;

bool setup(BelaContext *context, void *userData) {
    // Initialize potentiometer input
    pinMode(Bela::AnalogInput0, INPUT);
    return true;
}

void render(BelaContext *context, void *userData) {
    for (unsigned int n = 0; n < context->audioFrames; n++) {
        // Read stereo input
        float inLeft  = audioRead(context, n, 0);
        float inRight = audioRead(context, n, 1);
        
        // Update LFO phase every audio frame
        gTremoloState.phase += 2.0f * (float)M_PI * gTremoloState.frequency / (float)context->audioSampleRate;
        if (gTremoloState.phase >= 2.0f * (float)M_PI) {
            gTremoloState.phase -= 2.0f * (float)M_PI;
        }
        
        // Read potentiometer every 100 frames to update frequency
        if (n % 100 == 0) {
            float potValue = analogRead(context, n / 100, 0);  // 0.0 to 1.0
            // Map potentiometer to frequency range (1-20 Hz)
            gTremoloState.frequency = 1.0f + potValue * 19.0f;
        }
        
        // Calculate tremolo gain: 0.5 * (1 + depth * sin(phase))
        float tremoloGain = 0.5f * (1.0f + gTremoloState.depth * sinf(gTremoloState.phase));
        
        // Apply tremolo to both channels
        float outLeft  = inLeft  * tremoloGain;
        float outRight = inRight * tremoloGain;
        
        // Write output
        audioWrite(context, n, 0, outLeft);
        audioWrite(context, n, 1, outRight);
    }
}

void cleanup(BelaContext *context, void *userData) {
    // No cleanup needed
}
```

**Input:** "Implement a stereo panner controlled by two potentiometers (X/Y position)"
**Output:**
```cpp
#include <Bela.h>

// Panner state
struct PannerState {
    float panX = 0.5f;  // -1.0 (left) to +1.0 (right)
    float panY = 0.5f;  // -1.0 (back) to +1.0 (front) for pseudo-stereo
} gPannerState;

bool setup(BelaContext *context, void *userData) {
    // Configure two analog inputs for X/Y position
    pinMode(Bela::AnalogInput0, INPUT);  // X-axis pot
    pinMode(Bela::AnalogInput1, INPUT);  // Y-axis pot
    return true;
}

void render(BelaContext *context, void *userData) {
    for (unsigned int n = 0; n < context->audioFrames; n++) {
        // Read audio input (assume mono input for panning)
        float inMono = audioRead(context, n, 0);
        
        // Update panner position from potentiometers every 50 frames
        if (n % 50 == 0) {
            // Read X-axis potentiometer (0.0 to 1.0) -> panX (-1.0 to +1.0)
            float potX = analogRead(context, n / 50, 0);
            gPannerState.panX = potX * 2.0f - 1.0f;
            
            // Read Y-axis potentiometer (0.0 to 1.0) -> panY (-1.0 to +1.0)
            float potY = analogRead(context, n / 50, 1);
            gPannerState.panY = potY * 2.0f - 1.0f;
        }
        
        // Simple stereo panning law (constant power)
        // For more accurate panning, use sqrt(2)/2 scaling
        float angle = (gPannerState.panX + 1.0f) * (float)M_PI / 4.0f;  // 0 to pi/2
        float leftGain  = cosf(angle);
        float rightGain = sinf(angle);
        
        // Apply panning
        float outLeft  = inMono * leftGain;
        float outRight = inMono * rightGain;
        
        // Write stereo output
        audioWrite(context, n, 0, outLeft);
        audioWrite(context, n, 1, outRight);
    }
}

void cleanup(BelaContext *context, void *userData) {
    // No cleanup needed
}
```