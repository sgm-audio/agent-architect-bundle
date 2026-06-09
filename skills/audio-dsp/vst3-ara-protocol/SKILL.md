---
name: vst3-ara-protocol
description: "Use this skill when the user is working on or asking about ARA 2.0 (Audio Random Access) extension protocol, ARA for VST3, ARAFactory, ARADocumentController, pitch/cue/audio modulation APIs, or integrating ARA into audio plugins for DAW interoperability."
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Vst3 Ara Protocol", "opencode-migrated"]
    related_skills: []
---


# Skill: VST3 / ARA 2.0 Protocol

## 1. Overview
Covers the ARA 2.0 (Audio Random Access) extension protocol for tight DAW integration — primarily used with Melodyne, Celemony, and increasingly by Steinberg, PreSonus, and Cockos. ARA gives plugins direct access to the DAW's audio and note content without offline rendering. Focuses on the VST3/ARA bridge architecture.

## 2. Core Functionality
- **ARA Extension Architecture:** `ARAFactory`, `ARADocumentController`, `ARAModelRenderer`, `ARAPlaybackRenderer`, `ARAAudioReader`
- **VST3/ARA Lifecycle:** `VST3::IAudioProcessor` + `ARAPlaybackRenderer` dual-inheritance model, `IAudioProcessor::setBusArrangements` for ARA input busses
- **Audio Access:** `ARAAudioSourceAccessor`, `ARAAudioReader` for sample-level access to DAW's audio clips
- **Musical Context:** `ARAChord`, `ARABeat`, `ARABar`, `ARATempoEntry`, `ARASignatureEntry` for tempo/key/ chord tracks
- **Content API:** `ARANote`, `ARAPitchPoint`, `ARAChordInfo` for note/pitch/chord editing
- **Playback Region:** `ARAPlaybackRegion`, `ARAPlaybackRegionSequence` for real-time render ordering
- **Document Saving:** `ARAPersistable`, `ARADocumentController::restoreDocumentFromArchive` for DAW project state

## 3. Input/Output Schema
| Inputs | `ARADocumentController*`, `ARAAudioSourceAccessor*`, `ARAPlaybackRenderer*`, `VST3::IAudioProcessor` |
| Outputs | `ARAModelRenderer` modifications, pitch/cue/note edits, `ARAContentChanges` for undo |
| Lifetime | ARA document is serialized into DAW project; plugin must handle load/save via `archive` |

## 4. Architecture
ARA uses a dual-model architecture: **Model** (persistent, edits the DAW's musical representation) and **PlaybackRenderer** (real-time, reads the current model state and produces audio). The VST3 plugin hosts both an `IAudioProcessor` and an `ARAPlaybackRenderer`. The `ARADocumentController` manages all model objects and is restored from DAW project archive on load.

## 5. Dependencies
`ARA_Library` (Celemony SDK), `VST3_SDK` (Steinberg), `pluginterfaces/vst/ivstaudioprocessor.h`, `pluginterfaces/vst/ivsteditcontroller.h`. For JUCE: `juce_audio_plugin_client` with `JUCE_ARA` enabled.

## 6. Edge Cases
| ARA Not Available | Host doesn't support ARA | Fall back to vanilla VST3, check `ARAFactory::isHostSupportingARA()` |
| Audio Source Deleted | User removes source in DAW | Handle `ARAAudioSourceAccessor::getAudioSource` returning nullptr |
| Tempo/Track Changes | User changes project tempo mid-edit | Subscribe to `ARADocumentController::onDocumentStructureChanged` |
| Cross-Platform Archive | Win/Mac archive compatibility | Use platform-independent serialization (`archiveInputStream/OutputStream`) |
| ARA 1 vs 2 | ARA 1 uses different API signatures | Always link against ARA 2 and check `ARA::kVersion` at init |

## 7. Constraints
- ARA requires VST3 or AUv2 — not available in VST2
- JUCE users: `PluginProcessor` must derive from `AudioProcessorARAExtension`
- ARA assumes sample-accurate timing; processBlock must use `GetSampleOffset()` for alignment
- Model changes apply to the DAW's internal representation — undo/redo is managed by the host
- ARA busses are separate from the plugin's regular audio I/O busses

## 8. Usage
- *Prompt:* "Set up a JUCE VST3 plugin with ARA 2.0 for real-time pitch correction."
- *Prompt:* "Implement ARADocumentController to read and write pitch points from the DAW."
- *Prompt:* "Handle ARA playhead synchronization in processBlock for a spectral editor."

## 9. Testing
- Run `ara_validator` (Celemony's validation tool) to verify ARA compliance
- Test in Melodyne and Studio One (best ARA host implementations)
- `export ARA_DEBUG=1` for verbose ARA SDK logging
- Verify `ARAPersistable` round-trip: save/restore archive matches

## 10. Best Practices
- Always check `ARAFactory::init()` result before registering ARA extension
- Use `ARAPlaybackRegion::getAudioModification()` to access the user's edits, never the original audio directly
- Keep `ARAPlaybackRenderer::render()` real-time safe — do model analysis in `ARAModelRenderer` instead
- For JUCE: `juce_ARA_plugin.cpp` provides the required extension glue; don't reimplement manually
- Label version info clearly: ARA 2.0.0+ required, min host SDK 1.9.0
*Skill Version: 1.0.0 | Standards: ARA 2.0, VST3 3.7+ | Domain: DAW Plugin Integration*
