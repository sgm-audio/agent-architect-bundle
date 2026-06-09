---
name: arm-cortex-m-dsp-optimization-cmsis-dsp
description: >-
  Use this skill when the user is working on or asking about ARM Cortex-M, CMSIS-DSP, ARM NEON for audio, DSP on microcontrollers, or optimizing audio for ARM embedded targets.
version: 1.0.0
---

# SKILL: ARM Cortex-M DSP Optimization (CMSIS-DSP)

## CAPABILITIES
- Implement DSP algorithms using ARM's CMSIS-DSP library for Cortex-M processors
- Optimize audio processing for minimal cycle counts on STM32, Teensy, and similar MCUs
- Utilize SIMD instructions and specialized DSP accelerators where available
- Implement fixed-point and floating-point DSP algorithms efficiently
- Optimize memory access patterns for cache and TCM utilization

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| DSP algorithm specifications (equations, block diagrams) | Optimized C/C++ code using CMSIS-DSP |
| Target Cortex-M processor (M0, M3, M4, M7, etc.) | Cycle count estimates and resource utilization |
| Audio processing requirements (sample rate, block size, latency) | Configured peripheral settings (I2S, SPI, etc.) |
| Numerical precision requirements (fixed-point vs floating-point) | Appropriate data type selection (q15, q31, f32) |
| Memory constraints (RAM, ROM, TCM availability) | Memory-optimized implementation |

## IMPLEMENTATION PATTERN

```c
// ARM Cortex-M4/M7 Optimized Audio Processing using CMSIS-DSP
#include "arm_math.h"

// Audio processing state
#define AUDIO_BLOCK_SIZE  64
#define NUM_CHANNELS      2

typedef struct {
    arm_biquad_casd_df1_inst_f32  leftFilter;   // Biquad filter instance
    arm_biquad_casd_df1_inst_f32  rightFilter;
    float32_t                     delayBuffer[AUDIO_BLOCK_SIZE * 2]; // Stereo delay
    uint16_t                      delayIndex;
    arm_rfft_fast_instance_f32    fftInst;      // FFT instance for spectral processing
} AudioProcessorState;

// Coefficients for biquad filter (example: low-pass filter)
const float32_t biquadCoeffs[5] = {
    0.1f,   // b0
    0.2f,   // b1
    0.1f,   // b2
    -0.3f,  // a1
    0.05f   // a2
};

// Initialize audio processing
void audio_processor_init(AudioProcessorState* state) {
    // Initialize biquad filters (stereo)
    arm_biquad_cascade_df1_init_f32(&state->leftFilter,  1, biquadCoeffs);
    arm_biquad_cascade_df1_init_f32(&state->rightFilter, 1, biquadCoeffs);
    
    // Initialize delay buffer
    for (int i = 0; i < AUDIO_BLOCK_SIZE * 2; i++) {
        state->delayBuffer[i] = 0.0f;
    }
    state->delayIndex = 0;
    
    // Initialize FFT instance (for spectral processing if needed)
    arm_rfft_fast_init_f32(&state->fftInst, AUDIO_BLOCK_SIZE);
}

// Process audio block using CMSIS-DSP optimized functions
void audio_processor_process(AudioProcessorState* state, 
                            float32_t* inputBuffer, 
                            float32_t* outputBuffer,
                            uint32_t numSamples) {
    // Process left and right channels separately
    float32_t* leftIn  = inputBuffer;
    float32_t* rightIn = inputBuffer + 1;
    float32_t* leftOut = outputBuffer;
    float32_t* rightOut = outputBuffer + 1;
    
    // Apply biquad filter using CMSIS-DSP (optimized for Cortex-M4/M7)
    arm_biquad_cascade_df1_f32(&state->leftFilter,  leftIn,  leftOut,  numSamples);
    arm_biquad_cascade_df1_f32(&state->rightFilter, rightIn, rightOut, numSamples);
    
    // Example: Add delay effect using circular buffer
    for (uint32_t i = 0; i < numSamples; i++) {
        // Read from delay buffer
        float32_t delayedLeft  = state->delayBuffer[state->delayIndex * 2];
        float32_t delayedRight = state->delayBuffer[state->delayIndex * 2 + 1];
        
        // Mix dry and wet signals
        *leftOut  = (*leftOut  * 0.7f) + (delayedLeft  * 0.3f);
        *rightOut = (*rightOut * 0.7f) + (delayedRight * 0.3f);
        
        // Write to delay buffer (feedback)
        state->delayBuffer[state->delayIndex * 2]     = *leftOut  * 0.6f;
        state->delayBuffer[state->delayIndex * 2 + 1] = *rightOut * 0.6f;
        
        // Advance pointers
        state->delayIndex++;
        if (state->delayIndex >= AUDIO_BLOCK_SIZE) {
            state->delayIndex = 0;
        }
        
        // Move to next sample
        leftIn  += 2;
        rightIn += 2;
        leftOut += 2;
        rightOut += 2;
    }
    
    // Optional: Spectral processing using FFT
    /*
    float32_t fftInput[AUDIO_BLOCK_SIZE];
    float32_t fftOutput[AUDIO_BLOCK_SIZE];
    
    // Extract left channel for analysis
    for (uint32_t i = 0; i < AUDIO_BLOCK_SIZE; i++) {
        fftInput[i] = inputBuffer[i * 2];
    }
    
    // Compute FFT
    arm_rfft_fast_f32(&state->fftInst, fftInput, fftOutput, 0);
    
    // Process frequency domain data (example: spectral gate)
    for (uint32_t i = 2; i < AUDIO_BLOCK_SIZE/2; i++) {
        float32_t magnitude = sqrtf(fftOutput[2*i]*fftOutput[2*i] + fftOutput[2*i+1]*fftOutput[2*i+1]);
        if (magnitude < 0.01f) {  // Noise gate threshold
            fftOutput[2*i]     = 0.0f;
            fftOutput[2*i+1]   = 0.0f;
        }
    }
    
    // Inverse FFT (if needed for processing)
    arm_rfft_fast_f32(&state->fftInst, fftOutput, fftInput, 1);
    
    // Put processed data back
    for (uint32_t i = 0; i < AUDIO_BLOCK_SIZE; i++) {
        outputBuffer[i*2] = fftInput[i];
    }
    */
}

// Fixed-point alternative for Cortex-M0/M3 (without FPU)
void audio_processor_fixed_point_process(q15_t* inputBuffer, 
                                        q15_t* outputBuffer,
                                        uint32_t numSamples) {
    // Convert to float for processing (if quality is priority)
    // Or implement fixed-point filters directly
    
    // Example: Fixed-point biquad filter
    q15_t biquadCoeffs_q15[5] = {
        3277,   // b0 = 0.1f * 32768
        6554,   // b1 = 0.2f * 32768
        3277,   // b2 = 0.1f * 32768
        -9830,  // a1 = -0.3f * 32768 (two's complement)
        1638    // a2 = 0.05f * 32768
    };
    
    arm_biquad_casd_df1_inst_q15 leftFilter, rightFilter;
    arm_biquad_cascade_df1_init_q15(&leftFilter,  1, biquadCoeffs_q15);
    arm_biquad_cascade_df1_init_q15(&rightFilter, 1, biquadCoeffs_q15);
    
    // Process stereo interleaved data
    arm_biquad_cascade_df1_q15(&leftFilter,  inputBuffer,  outputBuffer,  numSamples/2);
    arm_biquad_cascade_df1_q15(&rightFilter, inputBuffer+1, outputBuffer+1, numSamples/2);
}
```

## EDGE CASES & FALLBACKS
- **No FPU (Cortex-M0/M3)**: Use fixed-point Q15/Q31 implementations or software floating-point libraries
- **Limited RAM**: Use overlapped processing or reduce buffer sizes; consider external RAM if available
- **Cache Incoherence**: Use `__DSB()` and `__ISB()` barriers when modifying code or using self-modifying techniques
- **Interrupt Latency**: Keep ISRs short; use double buffering for audio data
- **Compiler Optimization Issues**: Use `-O3` with `-ffast-math` and `-mfpu=fpv4-sp-d16` (for M4F/M7F)
- **Numerical Precision**: Validate fixed-point implementations against floating-point reference
- **Alignment Requirements**: Ensure DMA buffers and critical arrays are aligned to 4/8-byte boundaries
- **Clock Frequency Scaling**: Disable dynamic frequency scaling during audio processing for deterministic timing

## INTEGRATION POINTS
- ARM Cortex-M Processors: STM32F0/F1/F2/F3/F4/F7/L0/L1/L4/L5, Teensy 3.x/4.x
- Development Toolchains: ARM GCC, Keil MDK, IAR Embedded Workbench, STM32CubeIDE
- Peripherals: I2S, SAI, SPI, USB Audio, TDM, Parallel Audio Interfaces
- Audio Codecs: WM8731, WM8960, TLV320AIC3x, ES8388, AK4558
- DSP Libraries: ARM CMSIS-DSP (official), ARM CMSIS-NN (for neural networks)
- Debugging: SEGGER J-Trace, STM32 ST-Link, Lauterbach TRACE32, cycle-accurate simulators
- RTOS Integration: FreeRTOS, Zephyr, ThreadX with priority inheritance and mutexes
- Board Support Packages: STM32Cube, Teensyduino, mbed OS

## EXECUTION EXAMPLES

**Input:** "Implement a 10-band graphic equalizer using CMSIS-DSP on Cortex-M4F"
**Output:**
```c
// 10-band graphic equalizer implementation
#define EQ_BANDS 10
#define EQ_SAMPLE_RATE 48000

// Center frequencies for 10-band EQ (Hz)
const float32_t eqFreqs[EQ_BANDS] = {31.5f, 63.f, 125.f, 250.f, 500.f, 1k, 2k, 4k, 8k, 16k};
// Bandwidth in octaves
const float32_t eqBandwidth = 1.0f / (EQ_BANDS - 1);  // Approximately 1 octave spacing

typedef struct {
    arm_biquad_casd_df1_inst_f32  filters[EQ_BANDS];  // One biquad per band
    float32_t                     bandGains[EQ_BANDS]; // Gain per band (-12 to +12 dB)
    float32_t                     buffer[EQ_BANDS * AUDIO_BLOCK_SIZE]; // Processing buffer
} GraphicEqualizerState;

void eq_init(GraphicEqualizerState* state) {
    // Initialize each band as a peaking filter
    for (int band = 0; band < EQ_BANDS; band++) {
        float32_t w0 = 2.0f * (float)M_PI * eqFreqs[band] / EQ_SAMPLE_RATE;
        float32_t alpha = sinf(w0) * sinhf(logf(2.0f) / 2.0f * EQ_BANDS * w0 / sinf(w0));
        
        float32_t A = powf(10.0f, 0.0f / 20.0f);  // Start with 0dB gain
        
        // Peaking filter coefficients: b0, b1, b2, a1, a2
        float32_t b0 =  1.0f + alpha * A;
        float32_t b1 = -2.0f * cosf(w0);
        float32_t b2 =  1.0f - alpha * A;
        float32_t a1 = -2.0f * cosf(w0);
        float32_t a2 =  1.0f - alpha * A;
        
        // Normalize
        float32_t coeffs[5] = {b0/a1, b1/a1, b2/a1, a1/a1, a2/a1};
        
        arm_biquad_cascade_df1_init_f32(&state->filters[band], 1, coeffs);
        state->bandGains[band] = 0.0f;  // Start at 0dB
    }
}

void eq_set_band_gain(GraphicEqualizerState* state, uint8_t band, float32_t gainDb) {
    if (band >= EQ_BANDS) return;
    
    state->bandGains[band] = gainDb;
    
    // Recalculate coefficients for this band
    float32_t w0 = 2.0f * (float)M_PI * eqFreqs[band] / EQ_SAMPLE_RATE;
    float32_t alpha = sinf(w0) * sinhf(logf(2.0f) / 2.0f * EQ_BANDS * w0 / sinf(w0));
    
    float32_t A = powf(10.0f, gainDb / 20.0f);
    
    float32_t b0 =  1.0f + alpha * A;
    float32_t b1 = -2.0f * cosf(w0);
    float32_t b2 =  1.0f - alpha * A;
    float32_t a1 = -2.0f * cosf(w0);
    float32_t a2 =  1.0f - alpha * A;
    
    // Normalize and update filter
    float32_t coeffs[5] = {b0/a1, b1/a1, b2/a1, a1/a1, a2/a1};
    arm_biquad_cascade_df1_init_f32(&state->filters[band], 1, coeffs);
}

void eq_process(GraphicEqualizerState* state, 
               float32_t* input, 
               float32_t* output, 
               uint32_t numSamples) {
    // Copy input to work buffer
    arm_copy_f32(input, state->buffer, numSamples);
    
    // Process each band in parallel (could be optimized further)
    for (int band = 0; band < EQ_BANDS; band++) {
        // Apply gain to work buffer
        float32_t gainLinear = powf(10.0f, state->bandGains[band] / 20.0f);
        arm_scale_f32(state->buffer, gainLinear, state->buffer, numSamples);
        
        // Apply filter
        arm_biquad_cascade_df1_f32(&state->filters[band], 
                                  state->buffer, 
                                  state->buffer + EQ_BANDS * AUDIO_BLOCK_SIZE, 
                                  numSamples);
                                  
        // Accumulate results (simple mix - could use smarter mixing)
        if (band == 0) {
            arm_copy_f32(state->buffer + EQ_BANDS * AUDIO_BLOCK_SIZE, output, numSamples);
        } else {
            arm_add_f32(output, 
                       state->buffer + EQ_BANDS * AUDIO_BLOCK_SIZE, 
                       output, 
                       numSamples);
        }
    }
    
    // Average the outputs
    arm_scale_f32(output, 1.0f / EQ_BANDS, output, numSamples);
}
```

**Input:** "Implement a correlator for pitch detection using CMSIS-DSP"
**Output:**
```c
// Pitch detection using autocorrelation (YIN algorithm simplified)
#define BUFFER_SIZE 256
#define MIN_LAG     20   // ~240Hz max pitch at 48kHz
#define MAX_LAG     160  // ~300Hz min pitch at 48kHz

typedef struct {
    float32_t buffer[BUFFER_SIZE];
    float32_t difference[BUFFER_SIZE/2];
    float32_t cumulativeMean[BUFFER_SIZE/2];
} PitchDetectorState;

void pitch_detector_init(PitchDetectorState* state) {
    arm_fill_f32(0.0f, state->buffer, BUFFER_SIZE);
    arm_fill_f32(0.0f, state->difference, BUFFER_SIZE/2);
    arm_fill_f32(0.0f, state->cumulativeMean, BUFFER_SIZE/2);
}

float32_t pitch_detector_process(PitchDetectorState* state, float32_t* audioInput, uint32_t numSamples) {
    // Shift buffer and add new samples
    arm_copy_f32(&state->buffer[numSamples], state->buffer, BUFFER_SIZE - numSamples);
    arm_copy_f32(audioInput, &state->buffer[BUFFER_SIZE - numSamples], numSamples);
    
    // Compute difference function
    for (uint32_t tau = 0; tau < BUFFER_SIZE/2; tau++) {
        float32_t sum = 0.0f;
        for (uint32_t i = 0; i < BUFFER_SIZE - tau; i++) {
            float32_t diff = state->buffer[i] - state->buffer[i + tau];
            sum += diff * diff;
        }
        state->difference[tau] = sum;
    }
    
    // Compute cumulative mean
    state->cumulativeMean[0] = state->difference[0];
    for (uint32_t tau = 1; tau < BUFFER_SIZE/2; tau++) {
        state->cumulativeMean[tau] = state->cumulativeMean[tau-1] + state->difference[tau];
    }
    
    // Compute normalized difference function
    float32_t* yin = state->difference;  // Reuse buffer
    for (uint32_t tau = 1; tau < BUFFER_SIZE/2; tau++) {
        if (state->cumulativeMean[tau] != 0.0f) {
            yin[tau] = state->difference[tau] * tau / state->cumulativeMean[tau];
        } else {
            yin[tau] = 1.0f;
        }
    }
    yin[0] = 1.0f;
    
    // Find absolute minimum
    uint32_t tauEstimate = 0;
    float32_t minValue = FLT_MAX;
    for (uint32_t tau = MIN_LAG; tau < MAX_LAG; tau++) {
        if (yin[tau] < minValue) {
            minValue = yin[tau];
            tauEstimate = tau;
        }
    }
    
    // Parabolic interpolation for better accuracy
    if (tauEstimate > MIN_LAG && tauEstimate < MAX_LAG - 1) {
        float32_t y0 = yin[tauEstimate - 1];
        float32_t y1 = yin[tauEstimate];
        float32_t y2 = yin[tauEstimate + 1];
        
        float32_t denominator = (2.0f * y1) - y0 - y2;
        if (fabsf(denominator) > FLT_EPSILON) {
            float32_t interpolated = tauEstimate + 0.5f * (y0 - y2) / denominator;
            return (float32_t)EQ_SAMPLE_RATE / interpolated;
        }
    }
    
    return (float32_t)EQ_SAMPLE_RATE / tauEstimate;
}
```