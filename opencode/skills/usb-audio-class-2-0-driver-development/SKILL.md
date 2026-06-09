---
name: usb-audio-class-2-0-driver-development
description: >-
  Use this skill when the user is working on or asking about USB Audio Class 2.0, UAC2 driver development, USB audio device firmware, isochronous transfers for audio, or implementing USB audio on embedded systems.
version: 1.0.0
---

# SKILL: USB Audio Class 2.0 Driver Development

## CAPABILITIES
- Develop custom USB audio interfaces compliant with USB Audio Class 2.0 specification
- Implement isochronous audio streaming for low-latency audio I/O
- Create vendor-specific extensions for proprietary features
- Support multiple audio formats and sample rates
- Handle USB device enumeration, configuration, and hot-plugging

## CAPABILITY TAXONOMY
| Input | Output |
|-------|--------|
| USB controller specifications (hardware) | USB device descriptor and configuration |
| Audio interface requirements (channels, sample rate, bit depth) | USB audio format descriptors |
| Latency and jitter requirements | Isochronous endpoint configuration |
| Vendor-specific feature requests | Class-specific requests and descriptors |
| Operating system target (Windows/macOS/Linux) | OS-specific driver framework implementation |

## IMPLEMENTATION PATTERN

```c
// USB Audio Class 2.0 Device Example (using LUFA/LVGL/HAL-based pseudocode)
#include "usb_audio.h"

// Audio format capabilities
#define AUDIO_CHANNELS        2
#define AUDIO_FORMAT_BITS     24
#define AUDIO_FORMAT_TYPE     AUDIO_FORMAT_TYPE_I  // PCM
#define AUDIO_SAMPLE_FREQ_LO  (UINT16_L(44100))
#define AUDIO_SAMPLE_FREQ_HI  (UINT16_H(44100))
#define AUDIO_SAMPLE_FREQ     (AUDIO_SAMPLE_FREQ_LO | (AUDIO_SAMPLE_FREQ_HI << 8))

// Audio streaming interface
USB_ClassInfo_Audio_Device_t PhoneAudio_Interface = {
    .Config = {
        .ControlInterfaceNumber   = INTERFACE_ID_AudioControl,
        .StreamingInterfaceNumber = INTERFACE_ID_AudioStream,
        .DataINEndpoint           = {
            .Address          = AUDIO_STREAM_IN_EPADDR,
            .Size             = AUDIO_STREAM_EPSIZE,
            .Banks            = 1,
        },
        .DataOUTEndpoint          = {
            .Address          = AUDIO_STREAM_OUT_EPADDR,
            .Size             = AUDIO_STREAM_EPSIZE,
            .Banks            = 1,
        },
        .ControlEndpointSize      = ENDPOINT_CTRLSIZE,
    },
};

// USB Device Descriptor
USB_Descriptor_Device_t PROGMEM DeviceDescriptor = {
    .Header                 = {.Size = sizeof(USB_Descriptor_Device_t), .Type = DTYPE_Device},
    .USBSpecification       = VERSION_BCD(02.00),
    .Class                  = USB_CSCP_NoDeviceClass,
    .SubClass               = USB_CSCP_NoDeviceSubclass,
    .Protocol               = USB_CSCP_NoDeviceProtocol,
    .VendorID               = 0x1234,  // Replace with your VID
    .ProductID              = 0x5678,  // Replace with your PID
    .ReleaseNumber          = VERSION_BCD(00.01),
    .ManufacturerStrIndex   = 0x01,
    .ProductStrIndex        = 0x02,
    .SerialNumStrIndex      = USE_INTERNAL_SERIAL,
    .NumberOfConfigurations = FIXED_NUM_CONFIGURATIONS
};

// USB Configuration Descriptor
USB_Descriptor_Configuration_t PROGMEM ConfigurationDescriptor = {
    .Config = {
        .Header                   = {.Size = sizeof(USB_Descriptor_Configuration_Header_t), .Type = DTYPE_Configuration},
        .TotalConfigurationSize   = sizeof(USB_Descriptor_Configuration_t),
        .TotalInterfaces          = 2,
        .ConfigurationNumber      = 1,
        .ConfigurationStrIndex    = NO_DESCRIPTOR,
        .ConfigAttributes         = (USB_CONFIG_ATTR_RESERVED | USB_CONFIG_ATTR_SELFPOWERED),
        .MaxPowerConsumption      = USB_CONFIG_POWER_MA(100)
    },
    
    // Audio Control Interface
    .AudioControlInterface = {
        .Header                   = {.Size = sizeof(USB_Descriptor_Interface_t), .Type = DTYPE_Interface},
        .InterfaceNumber          = INTERFACE_ID_AudioControl,
        .AlternateSetting         = 0,
        .TotalEndpoints           = 1,
        .Class                    = AUDIO_CSCP_AudioControl,
        .SubClass                 = AUDIO_SCP_ControlProxy,
        .Protocol                 = AUDIO_PCP_None,
        .InterfaceStrIndex        = NO_DESCRIPTOR
    },
    
    .AudioControl_Specific = {
        .Header                   = {.Size = sizeof(USB_Audio_Descriptor_Interface_AC_t), .Type = DTYPE_CSInterface},
        .Subtype                  = AUDIO_DSUBTYPE_Header,
        .bcdADC                   = VERSION_BCD(02.00),
        .bCategory                = AUDIO_CAT_IoBox,
        .wTotalLength             = sizeof(USB_Audio_Descriptor_Interface_AC_t),
        .bmControls               = 0
    },
    
    // Input Terminal
    .InputTerminal = {
        .Header                   = {.Size = sizeof(USB_Audio_Descriptor_InputTerminal_t), .Type = DTYPE_CSInterface},
        .Subtype                  = AUDIO_DSUBTYPE_InputTerminal,
        .bTerminalID              = 1,
        .wTerminalType            = AUDIO_TERMINAL_USBStreaming,
        .bAssocTerminal           = 0,
        .bNrChannels              = AUDIO_CHANNELS,
        .wChannelConfig           = 0,
        .iChannelNames            = NO_DESCRIPTOR,
        .bmControls               = 0,
        .iTerminalIndex           = NO_DESCRIPTOR
    },
    
    // Output Terminal
    .OutputTerminal = {
        .Header                   = {.Size = sizeof(USB_Audio_Descriptor_OutputTerminal_t), .Type = DTYPE_CSInterface},
        .Subtype                  = AUDIO_DSUBTYPE_OutputTerminal,
        .bTerminalID              = 3,
        .wTerminalType            = AUDIO_TERMINAL_USBStreaming,
        .bAssocTerminal           = 0,
        .bNrChannels              = AUDIO_CHANNELS,
        .wChannelConfig           = 0,
        .iChannelNames            = NO_DESCRIPTOR,
        .bmControls               = 0,
        .iTerminalIndex           = NO_DESCRIPTOR
    },
    
    // Feature Unit
    .FeatureUnit = {
        .Header                   = {.Size = sizeof(USB_Audio_Descriptor_FeatureUnit_t), .Type = DTYPE_CSInterface},
        .Subtype                  = AUDIO_DSUBTYPE_FeatureUnit,
        .bUnitID                  = 2,
        .bSourceID                = 1,
        .bControlSize             = 1,
        .bmaControls[0]           = AUDIO_FU_CTRL_Mute | AUDIO_FU_CTRL_Volume,
        .bmaControls[1]           = 0,
        .bmaControls[2]           = 0,
        .iFeatureIndex            = NO_DESCRIPTOR
    },
    
    // Audio Streaming Interface
    .AudioStreamInterface = {
        .Header                   = {.Size = sizeof(USB_Descriptor_Interface_t), .Type = DTYPE_Interface},
        .InterfaceNumber          = INTERFACE_ID_AudioStream,
        .AlternateSetting         = 0,
        .TotalEndpoints           = 2,
        .Class                    = AUDIO_CSCP_AudioStreaming,
        .SubClass                 = AUDIO_SCP_Streaming,
        .Protocol                 = AUDIO_PCP_None,
        .InterfaceStrIndex        = NO_DESCRIPTOR
    },
    
    .AudioStream_Specific = {
        .Header                   = {.Size = sizeof(USB_Audio_Descriptor_Interface_AS_t), .Type = DTYPE_CSInterface},
        .Subtype                  = AUDIO_DSUBTYPE_General,
        .bTerminalLink            = 3,
        .bDelay                   = 1,
        .wFormatTag               = AUDIO_FORMAT_TYPE_I
    },
    
    .AudioStream_FormatType = {
        .Header                   = {.Size = sizeof(USB_Audio_Descriptor_FormatType_t), .Type = DTYPE_CSInterface},
        .Subtype                  = AUDIO_DSUBTYPE_FormatType,
        .bFormatType              = AUDIO_FORMAT_TYPE_I,
        .bNrChannels              = AUDIO_CHANNELS,
        .bSubframeSize            = ((AUDIO_FORMAT_BITS + 7) / 8),
        .bBitResolution           = AUDIO_FORMAT_BITS,
        .bSamFreqType             = 1,  // Discrete
        .tSamFreq[0]              = AUDIO_SAMPLE_FREQ
    },
    
    // Audio Stream Endpoints
    .AudioStream_INEndpoint = {
        .Header                   = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},
        .EndpointAddress          = (ENDPOINT_DIR_IN  | AUDIO_STREAM_IN_EPADDR),
        .Attributes               = (EP_TYPE_ISOCHRONOUS | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
        .EndpointSize             = AUDIO_STREAM_EPSIZE,
        .Interval                 = 0x01
    },
    
    .AudioStream_OUTEndpoint = {
        .Header                   = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},
        .EndpointAddress          = (ENDPOINT_DIR_OUT | AUDIO_STREAM_OUT_EPADDR),
        .Attributes               = (EP_TYPE_ISOCHRONOUS | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
        .EndpointSize             = AUDIO_STREAM_EPSIZE,
        .Interval                 = 0x01
    }
};

// USB Event Handlers
void EVENT_USB_Device_Connect(void) {
    // Device connected - enable audio processing
    USB_Audio_Device_EnableStreaming(&PhoneAudio_Interface);
}

void EVENT_USB_Device_Disconnect(void) {
    // Device disabled - disable audio processing
    USB_Audio_Device_DisableStreaming(&PhoneAudio_Interface);
}

void EVENT_USB_Device_ConfigurationChanged(void) {
    // Device configured - configure endpoints
    bool ConfigSuccess = true;
    
    ConfigSuccess &= USB_Device_ConfigureEndpoints(&ConfigurationDescriptor.Config);
    
    // Configure audio streaming endpoints
    USB_Audio_Device_ConfigureEndpoints(&PhoneAudio_Interface);
    
    if (!ConfigSuccess) {
        // Handle configuration failure
    }
}

// Audio Processing Callback
bool CALLBACK_USB_AudioDevice_GetSample(const USB_ClassInfo_Audio_Device_t* const AudioInterfaceInfo,
                                        const uint8_t Sample[][2],
                                        const uint16_t SampleCount) {
    // Input audio processing - samples coming FROM host
    // Process incoming audio from host PC
    for (uint16_t i = 0; i < SampleCount; i++) {
        int32_t leftSample  = ((int32_t)Sample[i][0] << 8) | ((int32_t)Sample[i][1] & 0xFF);
        int32_t rightSample = ((int32_t)Sample[i][2] << 8) | ((int32_t)Sample[i][3] & 0xFF);
        
        // Your DSP processing here
        // Process leftSample and rightSample
        
        // Output processed samples
        Sample[i][0] = (processedLeftSample  >> 8) & 0xFF;
        Sample[i][1] = (processedLeftSample  & 0xFF);
        Sample[i][2] = (processedRightSample >> 8) & 0xFF;
        Sample[i][3] = (processedRightSample & 0xFF);
    }
    
    return true;
}

bool CALLBACK_USB_AudioDevice_SetSample(const USB_ClassInfo_Audio_Device_t* const AudioInterfaceInfo,
                                        uint8_t Sample[][2],
                                        const uint16_t SampleCount) {
    // Output audio processing - samples going TO host
    // Prepare audio to send to host PC
    for (uint16_t i = 0; i < SampleCount; i++) {
        // Get audio from your DSP/output buffer
        int32_t leftSample  = getNextLeftSample();  
        int32_t rightSample = getNextRightSample();
        
        // Pack into USB audio format
        Sample[i][0] = (leftSample  >> 8) & 0xFF;
        Sample[i][1] = (leftSample  & 0xFF);
        Sample[i][2] = (rightSample >> 8) & 0xFF;
        Sample[i][3] = (rightSample & 0xFF);
    }
    
    return true;
}
```

## EDGE CASES & FALLBACKS
- **Bandwidth Limitations**: Reduce channel count, bit depth, or sample rate if USB bandwidth insufficient
- **Endpoint Stall Recovery**: Implement proper stall handling and clear feature requests
- **Clock Drift**: Use adaptive feedback or synchronous mode isochronous endpoints
- **Hot-plugging During Streaming**: Implement graceful start/stop of audio streams on connect/disconnect
- **Incorrect Descriptor Parsing by OS**: Validate descriptors with USB compliance testing tools
- **Power Budget Exceeded**: Reduce device power consumption or use external power supply
- **Latency Too High**: Optimize buffer sizes and use lowest possible polling interval
- **Driver Conflicts**: Use unique VID/PID combinations and proper device class/subclass codes

## INTEGRATION POINTS
- USB Stacks: LUFA (AVR), TinyUSB, STM32 USB Device Library, NXP USB Stack
- Microcontrollers: ARM Cortex-M (STM32, NXP LPC), AVR (ATmega32U4), ESP32-S2/S3
- Audio Codecs: I2S interfacing with PCM1808, PCM5102A, ES9018, WM8731
- Operating Systems: Windows (WDM/KSFT), macOS (CoreAudio), Linux (ALSA)
- Audio Frameworks: JUCE, VST SDK, Audio Units, LV2
- Debugging Tools: USB protocol analyzers (Beagle480, Ellisys), oscilloscopes, logic analyzers
- Testing Tools: USB compliance test suites, Audio Precision analyzers
- Descriptor Generation Tools: USB Device Descriptor Generator, Audio Class Driver Wizard

## EXECUTION EXAMPLES

**Input:** "Create a 2-in/2-out USB audio interface at 48kHz/24-bit with hardware gain control"
**Output:**
```c
// In the ConfigurationDescriptor section, modify:
// Audio Channels
#define AUDIO_CHANNELS        2
#define AUDIO_FORMAT_BITS     24

// Add feature unit for volume control in both channels
.FeedbackUnit = {
    .Header                   = {.Size = sizeof(USB_Audio_Descriptor_FeatureUnit_t), .Type = DTYPE_CSInterface},
    .Subtype                  = AUDIO_DSUBTYPE_FeatureUnit,
    .bUnitID                  = 4,
    .bSourceID                = 3,  // From output terminal
    .bControlSize             = 2,
    .bmaControls[0]           = AUDIO_FU_CTRL_Mute | AUDIO_FU_CTRL_Volume,
    .bmaControls[1]           = AUDIO_FU_CTRL_Mute | AUDIO_FU_CTRL_Volume,
    .bmaControls[2]           = 0,
    .iFeatureIndex            = NO_DESCRIPTOR
},
// And connect it properly in the signal flow
```

**Input:** "Implement MIDI over USB Audio Class 2.0 device"
**Output:**
```c
// Add MIDI Streaming Interface to ConfigurationDescriptor
.MIDIStreamInterface = {
    .Header                   = {.Size = sizeof(USB_Descriptor_Interface_t), .Type = DTYPE_Interface},
    .InterfaceNumber          = INTERFACE_ID_MIDIStream,
    .AlternateSetting         = 0,
    .TotalEndpoints           = 2,
    .Class                    = AUDIO_CSCP_MIDIStreaming,
    .SubClass                 = 0x00,
    .Protocol                 = 0x00,
    .InterfaceStrIndex        = NO_DESCRIPTOR
},
.MIDIStream_Jack = {
    .Header                   = {.Size = sizeof(USB_MIDI_Descriptor_Jack_t), .Type = DTYPE_CSInterface},
    .Subtype                  = MIDI_DSUBTYPE_Jack,
    .bJackType                | MIDI_JACKTYPE_Embedded,
    .bJackID                  = 1
},
.MIDIStream_Endpoint = {
    .Header                   = {.Size = sizeof(USB_Descriptor_Endpoint_t), .Type = DTYPE_Endpoint},
    .EndpointAddress          = (ENDPOINT_DIR_OUT | MIDI_STREAM_OUT_EPADDR),
    .Attributes               = (EP_TYPE_ISOCHRONOUS | ENDPOINT_ATTR_NO_SYNC | ENDPOINT_USAGE_DATA),
    .EndpointSize             = MIDI_STREAM_EPSIZE,
    .Interval                 = 0x01
}
```
