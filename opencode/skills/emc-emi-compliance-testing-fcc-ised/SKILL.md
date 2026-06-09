---
name: emc-emi-compliance-testing-fcc-ised
description: >-
  Use this skill when the user is working on or asking about EMC compliance, FCC certification, ISED Canada, EMI testing for audio hardware, or CE marking for audio devices.
version: 1.0.0
---

# SKILL: EMC/EMI Compliance Testing (FCC/ISED)

## CAPABILITIES
- Conduct electromagnetic compatibility (EMC) and electromagnetic interference (EMI) testing
- Ensure compliance with FCC (US) and ISED (Canada) regulations for electronic devices
- Identify and mitigate sources of emissions and susceptibility
- Perform pre-compliance testing to avoid costly redesigns
- Generate compliance documentation for certification

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Device under test (DUT) specifications | Test plan and procedure |
| Target regulations (FCC Part 15, ISED RSS-Gen) | Test setup and equipment list |
| Emission limits (conducted, radiated) | Measurement results and comparison to limits |
| Immunity requirements (ESD, surge, etc.) | Test results and pass/fail determination |
| Modification requirements | Mitigation strategies and redesign recommendations |

## IMPLEMENTATION PATTERN

```c
// Example: Design considerations for EMC compliance in audio hardware
#include <stdint.h>
#include <stdbool.h>

// EMC-friendly design practices for audio circuits
void emc_friendly_design_init(void) {
    // 1. Power supply decoupling
    // Place 0.1uF ceramic capacitors as close as possible to IC power pins
    // Use 10uF tantalum or ceramic capacitors for bulk decoupling
    
    // 2. Signal integrity
    // Control trace impedance for high-speed signals (I2S, SPI, USB)
    // Use controlled impedance traces (50 ohms single-ended, 100 ohms differential)
    // Match trace lengths for differential pairs
    
    // 3. Grounding
    // Use solid ground plane on inner layer
    // Partition analog and digital grounds, connect at single point
    // Avoid ground loops
    
    // 4. Shielding
    // Shield sensitive analog circuits (audio inputs, outputs)
    // Use conductive shielding on enclosures for radiated emissions
    // Properly ground shields at one end to avoid ground loops
    
    // 5. Filtering
    // Add ferrite beads on I/O cables (USB, audio, power)
    // Implement common-mode chokes on differential signals
    // Use RC or LC filters on noisy digital signals
    
    // 6. Component selection
    // Choose low-EMI components (oscillators, regulators)
    // Use spread-spectrum clock generators where possible
    // Select components with proper EMC ratings
    
    // 7. PCB layout
    // Keep high-current traces short and wide
    // Separate analog and digital sections
    // Route sensitive traces away from noisy sources (switching regulators, oscillators)
    
    // 8. Enclosure
    // Use conductive enclosure for shielding
    // Ensure good conductivity at seams (conductive gaskets, overlapping edges)
    // Ground enclosure to circuit ground at multiple points
}

// Example: EMI reduction in switching power supply
void powersupply_emc_reduction(void) {
    // 1. Spread spectrum clocking (if available in regulator)
    // Enable frequency dithering to spread energy over wider band
    
    // 2. Snubber circuits
    // Add RCD snubber across switching transistor to reduce ringing
    
    // 3. Proper layout
    // Minimize loop area of high-current paths
    // Place input and output capacitors close to regulator
    // Use ground plane under switching nodes
    
    // 4. Shielding
    // Shield inductor if it's a source of radiation
    // Use shielded inductor for power supply
    
    // 5. Filtering
    // Add pi-filter (LC-LC) at input and output
    // Use common-mode choke on input lines
}

// Example: Audio I/O EMC protection
void audio_io_emc_protection(void) {
    // 1. Overvoltage protection
    // Use TVS diodes or clamping diodes on audio jacks
    
    // 2. RF filtering
    // Add ferrite beads on audio cables
    // Implement RC low-pass filter (e.g., 100ohm + 10nF) on audio lines
    
    // 3. Grounding
    // Connect audio jack shells to ground via 10ohm resistor (to avoid ground loops)
    // Or use isolated jacks with separate ground connection
    
    // 4. Shielding
    // Use shielded audio cables
    // Ground shield at source end only (or both ends if required by standard)
    
    // 5. Common-mode impedance
    // Add common-mode choke on balanced audio lines (XLR, TRS)
}
```

## EDGE CASES & FALLBACKS
- **Test Failure**: Perform root cause analysis using near-field probes, EMI receivers
- **Cost Constraints**: Prioritize fixes based on emission severity and frequency
- **Time-to-Pressure**: Use pre-compliance testing early in design
- **Component Substitution**: Verify EMC performance of alternative components
- **Firmware Changes**: Re-test after firmware updates that may change emission characteristics
- **Temperature Effects**: Test at extreme temperatures as some components behave differently
- **Portable/Battery Operation**: Test with different power sources (battery vs supply)
- **Cable Effects**: Test with various cable lengths and types
- **Grounding Variations**: Test with different grounding configurations
- **Modular Systems**: Test individual modules and complete system

## INTEGRATION POINTS
- Test Equipment: Spectrum analyzers, EMI receivers, LISNs, current probes, near-field probes
- Test Chambers: Anechoic chambers, GTEM cells, shielded rooms
- Software: EMI analysis tools, PCB design tools with EMC rules (Altium, Cadence, Mentor)
- Standards: FCC Part 15 Subpart B, ISED RSS-Gen, CISPR 22/32, EN 55022/24, IEC 61000 series
- Testing Labs: FCC-recognized telecommunication certification bodies (TCBs), ISED recognized bodies
- Consulting: EMC engineering consultants, specialized testing services
- Design Tools: SPICE simulators with EMI models, field solvers (HFSS, CST)
- Component Vendors: EMI suppression components (ferrites, common-mode chokes, TVS diodes)
- Enclosure Manufacturers: Shielded enclosures, conductive gaskets, EMI windows
- Cable Suppliers: Shielded cables, EMC-rated connectors

## EXECUTION EXAMPLES

**Input:** "Reduce radiated emissions from a USB audio device at 30-88 MHz range"
**Output:**
```
// Likely causes: USB data lines, oscillator harmonics, power supply switching
// Solutions:
// 1. Add common-mode choke on USB data lines (D+ and D-)
// 2. Series termination resistors (22-33 ohms) on USB data lines near host controller
// 3. Shield USB cable and ground shield at host end
// 4. Check oscillator grounding and load capacitors
// 5. Add ferrite bead on USB VBUS line
// 6. Ensure proper return paths for USB signals (solid ground plane under traces)
// 7. Reduce oscillator drive strength if possible
// 8. Add patch ground stitching vias around oscillator
// 9. Implement spread spectrum clocking if available in USB controller
// 10. Shield USB controller IC with copper tape grounded to ground plane
```

**Input:** "Fix conducted emissions above 10V on AC mains port at 150kHz-30MHz"
**Output:**
```
// Likely causes: Switching power supply, poor input filtering
// Solutions:
// 1. Replace input filter with proper pi-filter (LC-LC)
//    - Two 10uF X2 capacitors (line-to-line)
//    - Two common-mode chokes (e.g., 10mH, 1A rating)
//    - 0.1uF Y2 capacitors (line-to-ground)
// 2. Add shielding around power supply and ground shield to input connector
// 3. Minimize loop area of high-frequency switching currents
// 4. Use snubber circuit across switching transistor
// 5. Add ferrite bead on DC output line of power supply
// 6. Check for grounding issues between primary and secondary sides
// 7. Consider using external power supply (adapter) to isolate noisy circuitry
// 8. Verify polarity of X2 and Y2 capacitors (must be correctly oriented)
// 9. Add transient suppression (MOV or TVS) across input terminals
// 10. Ensure proper creepage and clearance distances for safety
```