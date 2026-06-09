---
name: ableton-live
description: >-
  Ableton Live music production, MIDI sequencing, audio recording, mixing, mastering, sound design, and live performance. Use when working with Ableton Live, Live sets, Session view, Arrangement view, Max for Live, Ableton push, music production, electronic music, audio engineering, or DAW operations.
version: 1.1.0
---

# Skill: Ableton Live Music Production

## 1. Overview
This skill covers the use of Ableton Live for music production, including MIDI sequencing, audio recording, mixing, mastering, sound design, and live performance. It encompasses workflow optimization, device racks, automation, and integration with external hardware and software.

## 2. Core Functionality
- **Session and Arrangement Views:** Clip launching, scene management, and linear timeline editing
- **MIDI Sequencing:** MIDI clip editing, quantization, groove pool, and MIDI effects
- **Audio Recording:** Multi-track recording, input monitoring, comping, and warp modes
- **Mixing and Mastering:** Track grouping, return tracks, audio effects, and mastering chain
- **Sound Design:** Instrument racks, drum racks, simpler/sampler, and Max for Live devices
- **Live Performance:** Follow actions, MIDI mapping, and external instrument integration

## 3. Session View
### Clip Operations
- **Creating clips:** Record MIDI or audio into clip slots
- **Clip launching:** Launch clips in Scene or individual mode
- **Loop settings:** Adjust loop length and position within clips
- **Clip envelopes:** Automation for clip parameters (volume, pitch, filter)
- **Quantization:** Set clip launch quantization (1/4, 1/8, 1/16, etc.)
### Scene Management
- **Scene creation:** Organize clips into scenes
- **Scene launching:** Trigger entire scenes at once
- **Follow actions:** Configure automatic clip transitions
- **Scene naming:** Label scenes for easy navigation

## 4. Arrangement View
### Track Operations
- **Track types:** MIDI, Audio, Return, and Master tracks
- **Track freezing:** Freeze tracks for CPU optimization
- **Track grouping:** Group tracks for organization
- **Crossfades:** Configure auto-crossfade on overlapping clips
### Arrangement Editing
- **Moving clips:** Drag and drop with snapping
- **Time stretching:** Adjust clip length without pitch change
- **Looping:** Set loop region in arrangement
- **Automation lanes:** Show automation for any parameter
- **Time signature changes:** Handle multiple time signatures

## 5. MIDI and Instruments
### MIDI Clips
- **Note editor:** Piano roll and drum grid views
- **Note manipulation:** Velocity, length, pitch, and position editing
- **Scale quantization:** Snap notes to musical scales
- **MIDI effects:** Chord, Scale, Random, and other MIDI effects
### Built-in Instruments
- **Analog:** Subtractive synthesis synthesizer
- **Operator:** FM synthesis instrument
- **Wavetable:** Wavetable synthesis
- **Drift:** Polyphonic analog-style synth
- **Electric:** Electric piano simulation
- **Sampler:** Multi-sample instrument
- **Drum Kits:** Acoustic and electronic drum kits
- **External instruments:** Route to hardware synthesizers
### MIDI Remote Scripts
- **Controller mapping:** Map hardware controllers to parameters
- **Max for Live devices:** Custom MIDI and audio processing

## 6. Audio Recording
### Recording Setup
- **Input configuration:** Set audio input routes
- **Input monitoring:** Monitor input with zero latency
- **Record quantization:** Quantize recorded MIDI in real-time
- **Punch in/out:** Record within specific time ranges
- **Loop recording:** Multiple takes within a loop
### Take Management
- **Comp takes:** Select best parts from multiple takes
- **Take lanes:** View and edit multiple takes
- **Auto-punch:** Automatically start recording at set point

## 7. Audio Effects
### Effects Devices
- **EQ Eight:** 8-band parametric EQ
- **Compressor:** Dynamic range compression
- **Limiter:** Brick-wall limiting
- **Gate:** Noise gating
- **Delay:** Tape, Echo, and Filter Delay
- **Reverb:** Reverb, Convolution Reverb
- **Chorus/Flanger/Phaser:** Modulation effects
- **Resonators:** Resonant filter bank
- **Utility:** DC offset, gain staging, phase manipulation
### Audio Effect Racks
- **Creating racks:** Group multiple effects
- **Chain selection:** Select and control effect chains
- **Macro controls:** Map multiple parameters to single knobs
- **Randomization:** Randomize rack parameters

## 8. Mixing
### Mixer Section
- **Volume automation:** Automate fader movements
- **Pan automation:** Stereo positioning automation
- **Sends:** Route to return tracks
- **Solo/Mute:** Track isolation and silencing
### Grouping and Buses
- **Audio grouping:** Group tracks for collective processing
- **Parallel processing:** A/B or wet/dry parallel chains
- **Subgrouping:** Create submixes
### Master Channel
- **Master processing:** Final processing on master
- **Metering:** LUFS and peak metering
- **Reference tracks:** A/B against reference tracks

## 9. Export and Rendering
### Audio Export
- **Render to audio:** Export arrangement as audio file
- **Format options:** WAV, AIFF, MP3, OGG
- **Bit depth:** 16-bit, 24-bit
- **Sample rate:** 44.1kHz, 48kHz, 96kHz
- **Dither:** Apply dithering for mastering
### MIDI Export
- **Export MIDI:** Export MIDI clips
- **MIDI export options:** Include or exclude velocity
### Video Export
- **Video sync:** Synchronize audio to video
- **Video export:** Export with video track

## 10. Max for Live
### Devices
- **M4L instruments:** Custom synthesizers
- **M4L effects:** Custom audio and MIDI effects
- **M4L utilities:** MIDI tools, controllers
### Development
- **Max environment:** Create custom devices
- **Live API:** Programmatic access to Live
- **Patching:** Visual programming

## 11. Workflow Optimization
### Keyboard Shortcuts
- **Space:** Play/Stop
- **Enter:** Rename selected
- **Cmd+D:** Duplicate
- **Tab:** Switch between Session/Arrangement
- **Cmd+M:** Mute selected
- **Cmd+L:** Solo selected
### Productivity
- **Templates:** Create template Live Sets
- **Browser tagging:** Organize instruments and effects
- **Search:** Quick browser searching
- **Context menus:** Right-click operations

## 12. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | Audio/MIDI interfaces, MIDI controllers, samples, VST/AU plugins, Ableton Link, video |
| **Outputs** | Audio interface outputs, MIDI outputs, Ableton Link sync, exported audio/video |
| **Return Types** | Live Set (.als), exported stems, mixed/mastered audio files |

## 13. Dependencies & Toolchain
- Ableton Live Suite (latest version)
- Audio interface (ASIO/Core Audio)
- MIDI controller (optional)
- VST/AU plugins (optional)
- Ableton Link (for sync with other apps)

## 14. Performance & Troubleshooting
### Performance Issues
- **CPU optimization:** Freeze tracks, reduce buffer size, monitor via CPU meter
- **Latency:** Adjust buffer size (128-512 samples), use direct monitoring
- **Dropouts:** Increase buffer, reduce plugin count, use SSD for sample library
- **Monitoring:** Use external monitoring
### Audio Issues
- **Driver settings:** ASIO configuration (Windows), Core Audio (macOS)
- **Sample rate:** Match hardware and project settings
- **Clipping:** Reduce input gain
- **Noise:** Check cables and ground loops
### Plugin Compatibility
- **Crashes:** Update plugins, use 64-bit versions
- **Missing features:** Check plugin format support (VST3, AU, AAX)

## 15. Best Practices & Maintenance
- Save incremental versions of your Live Set
- Use templates for recurring project types
- Organize user library with tags and folders
- Backup projects to cloud or external drive
- Collect all samples on save
- Use color coding and naming conventions for tracks
