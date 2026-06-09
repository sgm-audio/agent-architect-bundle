---
name: digital-signal-processing-dsp-mathematics
description: >-
  Use this skill when the user is working on or asking about DSP mathematics, FIR/IIR filters, FFT, convolution, z-transforms, windowing functions, or signal processing algorithms.
version: 1.0.0
---

# Skill: Digital Signal Processing (DSP) Mathematics
## 📖 1. Overview
Designs and implements mathematically precise DSP algorithms for filtering, spectral processing, nonlinear waveshaping, and fractional delay, optimized for real-time execution and numerical stability.
## ⚙️ 2. Core Functionality
- IIR/FIR Design: Biquad transforms, windowed sinc FIR, zero-pole stability checks
- FFT: O(N log N) spectral analysis, overlap-add/save for block processing
- Waveshaping: Polynomial/tanh distortion, aliasing suppression (polyBLEP)
- Delay Lines: Fractional delay via Lagrange/Thiran interpolation, circular buffers
## 📥📤 3. Input/Output Schema
| Inputs | Coefficients, block size, sample rate, input signal, interpolation factor |
| Outputs | Filtered/transformed buffer, phase response data, latency compensation value |
## 🏗️ 4. Architecture
State-space filter design (`A, B, C, D` matrices). FFT using pre-computed twiddle factors. Delay line: `float* buffer`, `int read_ptr`, `float frac = fmodf(time, 1.0f)`, cubic interpolation.
## 🔗 5. Dependencies
`<complex>`, `KISSFFT`/`FFTW` (static link), `Eigen` (matrix math optional)
## ⚠️ 6. Edge Cases
| IIR Instability | NaN/Infinity | Pole-zero checking, clamp coeffs, reset on bypass |
| FFT Aliasing | Spectral folding | Windowing (Hann/Kaiser), overlap-save |
| Delay Artifacts | "Zipper" noise on pitch shift | Higher-order interpolation, envelope smoothing |
## 🛡️ 7. Constraints
- Precision: Double for coeff calc, float for RT processing
- Latency: FIR linear-phase latency = `(N-1)/2` samples
- Stability: `|poles| < 1.0` enforced at init
## 🤖 8. Usage
- *Prompt:* "Generate a polyBLEP sawtooth oscillator with anti-aliasing correction at 44.1kHz."
## 🧪 9. Testing
- Impulse/step response analysis
- Phase linearity verification
- Reference comparison against MATLAB/Octave
## 📝 10. Best Practices
- Pre-compute static tables at `constexpr` time
- Cache FFT plans; never reallocate in `processBlock()`
- Document mathematical derivations in code comments
*Skill Version: 1.0.0 | Standards: IIR/FIR, FFT, PolyBLEP | Domain: Real-Time Audio*