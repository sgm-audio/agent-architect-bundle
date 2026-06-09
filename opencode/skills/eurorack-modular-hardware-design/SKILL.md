---
name: eurorack-modular-hardware-design
description: >-
  Use this skill when the user is working on or asking about Eurorack module design, modular synthesis hardware, CV/gate signals, Eurorack PCB design, or building modular synth hardware.
version: 1.0.0
---

# SKILL: Eurorack Modular Hardware Design

## CAPABILITIES
- Design analog/digital hybrid Eurorack modules (3U format, 1.8" pitch)
- Implement CV/Gate integration with proper scaling and buffering
- Create bipolar signal handling (-5V to +5V range standard)
- Design power-efficient circuits for +12V/-12V/+5V Eurorack power bus
- Develop firmware for microcontroller-based digital Eurorack modules

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Functional specifications (signal ranges, response curves) | Schematic diagrams and PCB layouts |
| Power requirements (current draw on +12V/-12V/+5V rails) | Power budget calculations and protection circuits |
| Interface specifications (CV, Gate, Trigger, Audio) | Connector pinouts and signal conditioning circuits |
| Microcontroller firmware requirements | Firmware architecture and I/O mapping |
| Mechanical constraints (panel size, depth, knob placement) | Front panel design and mechanical drawings |

## IMPLEMENTATION PATTERN

```cpp
// Example: Eurorack Digital Oscillator Module Firmware (Teensy/Arduino)
#include <Arduino.h>
#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>
#include <SerialFlash.h>

// GUItool: begin automatically generated code
AudioSynthWaveform       waveform1;      //xy=148,96
AudioOutputI2S           i2s1;           //xy=328,96
AudioConnection          patchCord1(waveform1, 0, i2s1, 0);
AudioConnection          patchCord2(waveform1, 0, i2s1, 1);
AudioControlSGTL5000     sgtl5000_1;     //xy=184,163
// GUItool: end automatically generated code

// Eurorack-specific constants
const float CV_SCALE_FACTOR = 0.1f;    // 1V/octave = 0.0833V per semitone
const int   CV_INPUT_PIN    = A0;      // CV input for pitch control
const int   GATE_INPUT_PIN  = 2;       // Gate input (trigger)
const int   OUTPUT_LEFT_PIN = 9;       // I2S left channel output (to DAC)
const int   OUTPUT_RIGHT_PIN= 10;      // I2S right channel output (to DAC)

// Module state
struct ModuleState {
    float   currentFrequency = 440.0f; // Hz
    bool    gateActive       = false;
    uint8_t waveformType     = 0;      // 0=sine, 1=square, 2=saw, 3=triangle
    float   cvOffset         = 0.0f;   // CV offset calibration
} gState;

// CV to frequency conversion (1V/octave standard)
float cvToFrequency(float cvVoltage) {
    // Standard 1V/octave: f = f0 * 2^(cvVoltage)
    // Assuming A4 = 440Hz at 0V CV input
    return 440.0f * pow(2.0f, (cvVoltage + gState.cvOffset) * CV_SCALE_FACTOR * 12.0f);
}

// Read and scale CV input (0-3.3V or 0-5V to -5V to +5V Eurorack standard)
float readCvInput() {
    // Read analog input (assuming 3.3V ADC like Teensy)
    int rawValue = analogRead(CV_INPUT_PIN);
    float voltage = (rawValue / 1023.0f) * 3.3f; // Convert to voltage
    
    // Scale to Eurorack CV range (-5V to +5V)
    // Assuming input circuit offsets and scales 0-3.3V to -5V to +5V
    float cvVoltage = (voltage - 1.65f) * (10.0f / 3.3f); // -5V to +5V range
    
    return cvVoltage;
}

// Read gate input (threshold-based)
bool readGateInput() {
    // Simple threshold: >2.5V = HIGH for 3.3V logic
    return digitalRead(GATE_INPUT_PIN) == HIGH;
}

void setup() {
    // Initialize audio
    AudioMemory(12);
    sgtl5000_1.enable();
    sgtl5000_1.volume(0.5f);
    
    // Initialize oscillator
    waveform1.begin(WAVEFORM_SINE);
    
    // Configure I/O pins
    pinMode(CV_INPUT_PIN, INPUT);
    pinMode(GATE_INPUT_PIN, INPUT);
    
    // Calibrate CV input (optional)
    // gState.cvOffset = measureCvOffset();
}

void loop() {
    // Read CV input for pitch control
    float cvVoltage = readCvInput();
    float frequency = cvToFrequency(cvVoltage);
    
    // Update oscillator frequency
    waveform1.frequency(frequency);
    
    // Read gate input for note triggering
    bool gateState = readGateInput();
    
    // Simple gate-to-envelope conversion
    if (gateState && !gState.gateActive) {
        // Note on - trigger envelope
        // In a real module, you'd trigger an ADSR envelope here
    } else if (!gateState && gState.gateActive) {
        // Note off - release envelope
    }
    gState.gateActive = gateState;
    
    // Update waveform type based on control (e.g., potentiometer or switch)
    // This would typically be read from additional analog/digital inputs
    
    // Small delay to prevent CPU overuse (optional for simple modules)
    delay(1);
}
```

## EDGE CASES & FALLBACKS
- **Power Supply Noise**: Implement proper decoupling (100nF ceramic + 10uF tantalum per IC), use ferrite beads on power rails
- **Signal Clipping**: Add output buffering with opamps capable of rail-to-rail output, implement soft clipping circuits
- **CV Input Protection**: Use diodes and resistors to protect against overvoltage (-12V to +12V tolerance)
- **Ground Loops**: Implement star grounding, isolate digital and analog grounds where necessary
- **Temperature Drift**: Use temperature-compensated references (TCXO, bandgap references) for critical circuits
- **Calibration Drift**: Implement user calibration procedures for CV inputs and outputs
- **Firmware Updates**: Design bootloader field-update capability via USB or serial
- **EMC/EMI**: Add common-mode chokes on I/O lines, shield sensitive analog circuits
- **Incompatible Power Supplies**: Implement reverse polarity protection and overvoltage protection

## INTEGRATION POINTS
- Development Platforms: Teensy 3.x/4.x, Arduino Due, STM32F4/F7, ESP32-S2/S3
- Audio Codecs: PCM5102A, PCM1808, WM8731, ES9018, AK44xx
- Op-Amps: TL072/074, OPA2134, LMH6624, AD8628 (low noise, audio grade)
- Comparators: LM339, TLV3701 (for gate/trigger detection)
- Multiplexers/Demultiplexers: CD4051, ADG708 (for routing multiple CVs)
- Digital Potentiometers: MCP41xxx, AD52xx (for programmable parameters)
- Rotary Encoders: Bourns PEC11R, Alps EC11 (with detents for parameter control)
- Jacks: Thonkiconn, Kobiconn, Switchcraft (3.5mm mono/switched)
- Power Protection: Polyswitch fuses, TVS diodes, reverse polarity protection (Schottky diodes)
- PCB Design: KiCad, Eagle, Altium Designer with Eurorack-specific templates
- Panel Design: Front Panel Express, Ponoshop, Lasergraves for laser-etched aluminum
- Standards: Doepfer A-100 bus standard, Eurorack power connector (10-pin or 16-pin)

## EXECUTION EXAMPLES

**Input:** "Design a Eurorack VCF (Voltage Controlled Filter) with CV control of cutoff and resonance"
**Output:**
```cpp
// Eurorack VCF Firmware Example
#include <Audio.h>
#include <Bounce.h>

// Audio processing objects
AudioFilterStateVariable filter1;  // State variable filter (SVF)
AudioInputI2S            i2sIn;    // Audio input from codec
AudioOutputI2S           i2sOut;   // Audio output to codec
AudioConnection          patchCord1(i2sIn, 0, filter1, 0);
AudioConnection          patchCord2(filter1, 0, i2sOut, 0);
AudioConnection          patchCord3(filter1, 1, i2sOut, 1); // For stereo output
AudioControlSGTL5000     audioShield;

// Control inputs
const int CV_CUTOFF_PIN  = A0;   // CV input for filter cutoff
const int CV_RESONANCE_PIN = A1; // CV input for resonance
const int GATE_INPUT_PIN   = 2;  // Gate/envelope trigger input

// Filter state
struct FilterState {
    float cutoffFreq  = 1000.0f; // Hz
    float resonance   = 0.7f;    // Q factor (0.5 to 10+)
    bool  bypass      = false;
} gFilterState;

// Convert CV voltage to filter parameters
float cvToCutoff(float cvVoltage) {
    // Exponential response: 50Hz to 20kHz range
    return 50.0f * exp2f((cvVoltage + 5.0f) * (14.0f / 10.0f)); // -5V to +5V -> 50Hz-20kHz
}

float cvToResonance(float cvVoltage) {
    // Linear response: 0.5 to 10.0 Q
    return 0.5f + (cvVoltage + 5.0f) * (9.5f / 10.0f); // -5V to +5V -> 0.5-10.0 Q
}

void setup() {
    // Audio setup
    AudioMemory(10);
    audioShield.enable();
    audioShield.volume(0.5f);
    audioShield.inputSelect(AUDIO_INPUT_LINEIN);
    
    // Initialize filter
    filter1.resonance(gFilterState.resonance);
    filter1.frequency(gFilterState.cutoffFreq);
    filter1.octaveControl(1.0f); // 1V/octave for cutoff CV
    
    // Configure inputs
    pinMode(CV_CUTOFF_PIN, INPUT);
    pinMode(CV_RESONANCE_PIN, INPUT);
    pinMode(GATE_INPUT_PIN, INPUT_PULLUP);
}

void loop() {
    // Read CV inputs
    float cvCutoff  = readCvInput(CV_CUTOFF_PIN);
    float cvResonance = readCvInput(CV_RESONANCE_PIN);
    
    // Update filter parameters
    float cutoff  = cvToCutoff(cvCutoff);
    float resonance = cvToResonance(cvResonance);
    
    // Smooth parameter changes to avoid zipper noise
    static float smoothedCutoff  = cutoff;
    static float smoothedResonance = resonance;
    smoothedCutoff  = smoothedCutoff  * 0.9f  + cutoff  * 0.1f;
    smoothedResonance = smoothedResonance * 0.9f  + resonance * 0.1f;
    
    filter1.frequency(smoothedCutoff);
    filter1.resonance(smoothedResonance);
    
    // Handle gate input for envelope triggering (optional)
    bool gateState = digitalRead(GATE_INPUT_PIN) == LOW; // Active low
    // Trigger ADSR envelope here if implemented
    
    delay(1); // Small delay for stability
}

// Helper function to read and scale CV input
float readCvInput(int pin) {
    int rawValue = analogRead(pin);
    float voltage = (rawValue / 1023.0f) * 3.3f; // Teensy 3.3V ADC
    // Scale -2.5V to +2.5V (assuming centered input circuit)
    return (voltage - 1.65f) * (5.0f / 1.65f);
}
```

**Input:** "Create a Eurorack dual LFO module with waveform selection and CV control of rate"
**Output:**
```cpp
// Eurorack Dual LFO Firmware
#include <Audio.h>
#include <Bounce.h>

// Audio objects for LFO outputs
AudioSynthWaveformModulated lfo1;
AudioSynthWaveformModulated lfo2;
AudioOutputI2S i2sOut;
AudioConnection patchCord1(lfo1, 0, i2sOut, 0);
AudioConnection patchCord2(lfo2, 0, i2sOut, 1);
AudioControlSGTL5000 audioShield;

// Control inputs
const int CV_RATE1_PIN   = A0;   // CV input for LFO1 rate
const int CV_RATE2_PIN   = A1;   // CV input for LFO2 rate
const int CV_SHAPE_PIN   = A2;   // CV input for waveform shape (shared)
const int RESET_INPUT_PIN = 2;   // Sync reset input

// LFO state
struct LFOState {
    float   rate1    = 2.0f;    // Hz
    float   rate2    = 2.0f;    // Hz
    int8_t  shape    = 0;       // 0=sine,1=triangle,2=saw up,3=saw down,4=square
    bool    reset    = false;
    uint32_t lastReset = 0;
} gLFOState;

// Convert CV to LFO rate (exponential: 0.01Hz to 100Hz)
float cvToLfoRate(float cvVoltage) {
    return powf(10.0f, (cvVoltage + 5.0f) * (4.0f / 10.0f)); // -5V to +5V -> 0.01-100Hz
}

// Convert CV to waveform shape (0-4 range)
int8_t cvToShape(float cvVoltage) {
    // Map -5V to +5V to 0-4 range
    float normalized = (cvVoltage + 5.0f) * (4.0f / 10.0f); // 0 to 4
    return constrain((int8_t)roundf(normalized), 0, 4);
}

void setup() {
    AudioMemory(8);
    audioShield.enable();
    audioShield.volume(0.5f);
    
    // Configure LFOs
    lfo1.begin(WAVEFORM_SINE);
    lfo2.begin(WAVEFORM_TRIANGLE);
    lfo1.frequency(gLFOState.rate1);
    lfo2.frequency(gLFOState.rate2);
    lfo1.amplitude(0.8f); // +/-0.8V range (~5Vpp after scaling)
    lfo2.amplitude(0.8f);
    
    // Configure inputs
    pinMode(CV_RATE1_PIN, INPUT);
    pinMode(CV_RATE2_PIN, INPUT);
    pinMode(CV_SHAPE_PIN, INPUT);
    pinMode(RESET_INPUT_PIN, INPUT_PULLUP);
}

void loop() {
    // Read CV inputs
    float cvRate1   = readCvInput(CV_RATE1_PIN);
    float cvRate2   = readCvInput(CV_RATE2_PIN);
    float cvShape   = readCvInput(CV_SHAPE_PIN);
    bool  resetIn   = digitalRead(RESET_INPUT_PIN) == LOW;
    
    // Update parameters
    float rate1     = cvToLfoRate(cvRate1);
    float rate2     = cvToLfoRate(cvRate2);
    int8_t  shape   = cvToShape(cvShape);
    
    // Smooth rate changes
    static float smoothedRate1 = rate1;
    static float smoothedRate2 = rate2;
    smoothedRate1 = smoothedRate1 * 0.95f + rate1 * 0.05f;
    smoothedRate2 = smoothedRate2 * 0.95f + rate2 * 0.05f;
    
    lfo1.frequency(smoothedRate1);
    lfo2.frequency(smoothedRate2);
    
    // Update waveform shape (both LFOs)
    if (shape != gLFOState.shape) {
        gLFOState.shape = shape;
        switch(shape) {
            case 0: lfo1.begin(WAVEFORM_SINE);    lfo2.begin(WAVEFORM_SINE);    break;
            case 1: lfo1.begin(WAVEFORM_TRIANGLE);lfo2.begin(WAVEFORM_TRIANGLE);break;
            case 2: lfo1.begin(WAVEFORM_SAWTOOTH);lfo2.begin(WAVEFORM_SAWTOOTH);break;
            case 3: lfo1.begin(WAVEFORM_SAWTOOTH_REVERSE); lfo2.begin(WAVEFORM_SAWTOOTH_REVERSE); break;
            case 4: lfo1.begin(WAVEFORM_SQUARE);  lfo2.begin(WAVEFORM_SQUARE);  break;
        }
    }
    
    // Handle reset input
    if (resetIn && !gLFOState.reset && (millis() - gLFOState.lastReset > 10)) {
        // Reset LFO phases
        lfo1.reset();
        lfo2.reset();
        gLFOState.lastReset = millis();
    }
    gLFOState.reset = resetIn;
    
    delay(2);
}

// Helper function to read and scale CV input
float readCvInput(int pin) {
    int rawValue = analogRead(pin);
    float voltage = (rawValue / 1023.0f) * 3.3f;
    return (voltage - 1.65f) * (5.0f / 1.65f); // -5V to +5V range
}
```