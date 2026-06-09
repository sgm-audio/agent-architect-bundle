---
name: power-management-thermal-design
description: >-
  Use this skill when the user is working on or asking about power management for audio hardware, thermal design, battery-powered audio devices, or managing heat in DSP hardware.
version: 1.0.0
---

# SKILL: Power Management & Thermal Design

## CAPABILITIES
- Design efficient power supplies for audio hardware (low noise, high efficiency)
- Implement thermal management strategies for fan-less operation
- Optimize battery life for portable audio devices
- Manage power sequencing and reset behavior
- Reduce electromagnetic interference from power regulation

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| Power requirements (voltage, current, power consumption) | Power supply schematic and component selection |
| Thermal constraints (max temperature, enclosure size) | Thermal solution (heatsink, thermal vias, etc.) |
| Battery specifications (capacity, voltage) | Battery management circuit and charging algorithm |
| Noise requirements (audio band noise) | Power supply filtering and regulation design |
| Sequencing requirements (power-on/reset timing) | Reset controller and power sequencer design |

## IMPLEMENTATION PATTERN

```c
// Example: Power management for battery-operated audio device
#include <stdint.h>
#include <stdbool.h>
#include "battery.h"
#include "regulator.h"

// Power state definitions
typedef enum {
    POWER_STATE_OFF,
    POWER_STATE_STANDBY,
    POWER_STATE_ON,
    POWER_STATE_LOW_POWER
} PowerState_t;

// Battery monitoring
typedef struct {
    uint16_t voltage_mv;   // Millivolts
    uint16_t current_ma;   // Milliamperes (charge/discharge)
    uint16_t remaining_mah; // Remaining capacity
    uint8_t  temperature;  // Degrees Celsius
    bool     charging;
    bool     full;
} BatteryState_t;

// Global power state
typedef struct {
    PowerState_t state;
    BatteryState_t battery;
    uint32_t     uptime_seconds;
    bool         usb_connected;
    bool         low_battery_warned;
} PowerManagerState_t;

static PowerManagerState_t gPowerState;

// Initialize power management
void power_manager_init(void) {
    // Initialize battery monitor
    battery_init();
    
    // Initialize voltage regulators
    regulator_init();
    
    // Set initial state
    gPowerState.state = POWER_STATE_OFF;
    gPowerState.uptime_seconds = 0;
    gPowerState.usb_connected = false;
    gPowerState.low_battery_warned = false;
    
    // Start battery monitoring timer
    start_battery_monitoring();
}

// Main power management task (called periodically)
void power_manager_task(void) {
    // Update battery state
    battery_update(&gPowerState.battery);
    
    // Check USB connection
    gPowerState.usb_connected = usb_present();
    
    // State machine
    switch (gPowerState.state) {
        case POWER_STATE_OFF:
            // Check for power-on conditions
            if (gPowerState.usb_connected || button_pressed(POWER_BUTTON)) {
                power_on_sequence();
            }
            break;
            
        case POWER_STATE_STANDBY:
            // Check for wake conditions
            if (should_wake_from_standby()) {
                power_on_sequence();
            }
            // Check for power-off conditions (long press)
            if (button_held(POWER_BUTTON, 3000)) { // 3 second hold
                power_off_sequence();
            }
            break;
            
        case POWER_STATE_ON:
            // Check for low battery
            if (gPowerState.battery.voltage_mv < LOW_BATTERY_THRESHOLD_MV &&
                !gPowerState.low_battery_warned) {
                trigger_low_battery_warning();
                gPowerState.low_battery_warned = true;
            }
            
            // Check for shut down conditions
            if (!gPowerState.usb_connected && 
                gPowerState.battery.remaining_mah < SHUTDOWN_THRESHOLD_MAH) {
                power_off_sequence();
            }
            // Check for standby trigger (inactivity)
            if (inactivity_timeout_exceeded()) {
                enter_standby();
            }
            break;
            
        case POWER_STATE_LOW_POWER:
            // Reduce functionality to conserve power
            reduce_performance();
            // Check for wake conditions
            if (should_wake_from_low_power()) {
                power_on_sequence();
            }
            break;
    }
    
    // Update uptime
    if (gPowerState.state != POWER_STATE_OFF) {
        gPowerState.uptime_seconds++;
    }
}

// Power on sequence
void power_on_sequence(void) {
    // Enable regulators in correct order
    regulator_enable(REGULATOR_3V3);
    delay_ms(10);  // Allow settle
    regulator_enable(REGULATOR_1V8);
    delay_ms(10);
    regulator_enable(REGULATOR_AVDD);
    
    // Initialize hardware after power stable
    hardware_init();
    
    gPowerState.state = POWER_STATE_ON;
    gPowerState.uptime_seconds = 0;
    gPowerState.low_battery_warned = false;
}

// Power off sequence
void power_off_sequence(void) {
    // Notify application of shutdown
    notify_shutdown();
    
    // Disable hardware
    hardware_shutdown();
    
    // Disable regulators in reverse order
    regulator_disable(REGULATOR_AVDD);
    delay_ms(5);
    regulator_disable(REGULATOR_1V8);
    delay_ms(5);
    regulator_disable(REGULATOR_3V3);
    
    gPowerState.state = POWER_STATE_OFF;
}

// Enter low power standby
void enter_standby(void) {
    // Reduce clock frequency
    set_cpu_frequency(CPU_FREQ_LOW);
    
    // Disable non-essential peripherals
    peripheral_disable(PERIPHERAL_DISPLAY);
    peripheral_disable(PERIPHERAL_USB_HOST);
    
    gPowerState.state = POWER_STATE_STANDBY;
}

// Enter low power mode
void enter_low_power_mode(void) {
    // Further reduce clock
    set_cpu_frequency(CPU_FREQ_VERY_LOW);
    
    // Disable more peripherals
    peripheral_disable(PERIPHERAL_AUDIO_CODEC);
    peripheral_disable(PERIPHERAL_USB_DEVICE);
    
    gPowerState.state = POWER_STATE_LOW_POWER;
}

// Thermal management callback (called from temperature sensor interrupt or task)
void thermal_management_task(void) {
    int16_t temperature = read_temperature_sensor();
    
    if (temperature > THERMAL_THROTTLE_TEMPERATURE) {
        // Overheating - reduce performance
        reduce_clock_frequency();
        enable_thermal_throttling();
    } else if (temperature < THERMAL_THROTTLE_TEMPERATURE - HYSTERESIS) {
        // Cool enough - restore performance
        restore_clock_frequency();
        disable_thermal_throttling();
    }
    
    // Check for over-temperature shutdown
    if (temperature > THERMAL_SHUTDOWN_TEMPERATURE) {
        emergency_shutdown();
    }
}

// Helper functions (platform-specific)
bool usb_present(void) { /* Implementation */ return false; }
bool button_pressed(uint8_t button) { /* Implementation */ return false; }
bool button_held(uint8_t button, uint32_t ms) { /* Implementation */ return false; }
bool should_wake_from_standby(void) { /* Implementation */ return false; }
bool inactivity_timeout_exceeded(void) { /* Implementation */ return false; }
void trigger_low_battery_warning(void) { /* Implementation */ }
void power_on_sequence(void) { /* Implementation */ }
void power_off_sequence(void) { /* Implementation */ }
void notify_shutdown(void) { /* Implementation */ }
void hardware_init(void) { /* Implementation */ }
void hardware_shutdown(void) { /* Implementation */ }
void reduce_performance(void) { /* Implementation */ }
bool should_wake_from_low_power(void) { /* Implementation */ return false; }
void enter_standby(void) { /* Implementation */ }
void enter_low_power_mode(void) { /* Implementation */ }
int16_t read_temperature_sensor(void) { /* Implementation */ return 0; }
void reduce_clock_frequency(void) { /* Implementation */ }
void enable_thermal_throttling(void) { /* Implementation */ }
void restore_clock_frequency(void) { /* Implementation */ }
void disable_thermal_throttling(void) { /* Implementation */ }
void emergency_shutdown(void) { /* Implementation */ }
```

## EDGE CASES & FALLBACKS
- **Brownout Conditions**: Implement brownout detection and safe shutdown
- **Battery Failure**: Detect open circuit, short circuit, or cell imbalance
- **Thermal Runaway**: Implement hardware thermal shutdown fuse as backup
- **Inrush Current**: Use inrush current limiting (NTC thermistor or active circuit)
- **Regulator Oscillation**: Proper compensation and output capacitance
- **Voltage Spikes**: TVS diodes and proper sequencing
- **Battery Fuel Gauge Inaccuracy**: Periodic calibration through full charge/discharge
- **USB Suspend/Resume**: Handle USB suspend events to save power
- **Multiple Power Sources**: Implement power source selection (USB vs battery)
- **Leakage Current**: Minimize quiescent current in standby modes

## INTEGRATION POINTS
- Power Management ICs: TI BQ series, Linear Technology LTC, Maxim MAX17xxx
- Voltage Regulators: LDO (TPS7Axx, MCP1700), Buck (TI TPS62xxx, LT86xx), Boost
- Battery Management: Fuel gauges (MAX17043, BQ27xxx), charge controllers (BQ240xx)
- Temperature Sensors: NTC thermistors, digital sensors (TMP102, LM75)
- Current Sensors: Hall effect (ACS712), shunt amplifiers (INA219, INA226)
- Power Path Controllers: Load switches, ideal diodes, ORing FETs
- Supervisory Circuits: Reset generators, watchdog timers, voltage detectors
- Energy Harvesting: Solar (BQ25504), thermoelectric, piezoelectric
- PCB Design: Power plane splitting, star grounding, via stitching for thermal
- Enclosure Design: Thermal pads, heat pipes, phase change materials
- Standards: USB Power Delivery, Qualcomm Quick Charge, USB Battery Charging

## EXECUTION EXAMPLES

**Input:** "Design a power supply for a portable audio interface with phantom power"
**Output:**
```
// Block diagram:
// USB 5V -> [Power Path Controller] -> [Li-ion Battery Charger] -> [Battery]
//                          -> [5V to 48V Boost Converter] -> [Phantom Power Relay]
// USB 5V -> [LDO 3.3V] -> [Digital Circuits]
// USB 5V -> [LDO 1.8V] -> [Audio DSP, ADC/DAC]
// Battery -> [Boost 5V] -> [USB OTG when acting as host]
//
// Key components:
// - Battery charger: BQ24075 (USB/Li-ion)
// - Boost converter: TPS61088 (5V from battery)
// - Phantom power: TPS65130 (48V boost) + relay for enable
// - LDOs: TPS7A4700 (3.3V), TPS7A02 (1.8V)
// - Power path: TPS2115A (autoswitch between USB and battery)
// - Battery monitor: INA226 (current/voltage) + fuel gauge
```

**Input:** "Implement thermal throttling for a fan-less audio amplifier"
**Output:**
```
// Thermal throttling algorithm
#define TEMPERATURE_SENSOR_CHANNEL   ADC_CHANNEL_0
#define TEMPERATURE_UPDATE_INTERVAL  1000  // ms
#define THROTTLE_THRESHOLD_CELSIUS   85
#define THROTTLE_RELEASE_CELSIUS     75
#define MAX_THROTTLE_PERCENT         70  // Maximum CPU usage when throttling

static uint32_t lastTempCheck = 0;
static bool     isThrottling = false;

void thermal_management_task(void) {
    uint32_t now = get_system_time_ms();
    if (now - lastTempCheck < TEMPERATURE_UPDATE_INTERVAL) {
        return;
    }
    lastTempCheck = now;
    
    int16_t temp = read_temperature(TEMPERATURE_SENSOR_CHANNEL);
    
    if (temp > THROTTLE_THRESHOLD_CELSIUS && !isThrottling) {
        // Enter throttling mode
        set_cpu_max_percentage(MAX_THROTTLE_PERCENT);
        isThrottling = true;
        activate_throttling_indicator(); // e.g., blink LED
    } else if (temp < THROTTLE_RELEASE_CELSIUS && isThrottling) {
        // Exit throttling mode
        set_cpu_max_percentage(100);
        isThrottling = false;
        deactivate_throttling_indicator();
    }
}
```