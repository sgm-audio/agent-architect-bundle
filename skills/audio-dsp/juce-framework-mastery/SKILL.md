---
name: juce-framework-mastery
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Juce Framework Mastery", "opencode-migrated"]
    related_skills: []
---


# Skill: JUCE Framework Mastery

## 📖 1. Overview
This skill covers the comprehensive use of the JUCE C++ framework to build cross-platform, DAW-compatible audio plugins (VST3, AU, AAX, CLAP). It encompasses plugin lifecycle management, `AudioProcessorValueTreeState` (APVTS) parameter handling, component-based GUI architecture, host communication, and cross-platform build automation.

## ⚙️ 2. Core Functionality
- **Plugin Lifecycle & Host Integration:** Implementing `juce::AudioProcessor` for audio/MIDI routing, `prepareToPlay()`, `processBlock()`, and state serialization.
- **APVTS Parameter Management:** Binding parameters to UI components, handling undo/redo stacks, and ensuring thread-safe parameter exchange.
- **Modular GUI Architecture:** Building responsive UIs using `juce::Component`, layout managers, and custom `LookAndFeel` overrides.
- **Cross-Platform Build & Export:** Configuring CMake/Projucer for VST3, AU, AAX, CLAP exports with proper signing and bundling.

## 📥📤 3. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | Audio/MIDI buffers, APVTS `ValueTree` state, DAW host callbacks, UI mouse/touch/keyboard events, plugin instance count |
| **Outputs** | Processed audio/MIDI, serialized `ValueTree` XML/JSON, UI repaint events, host status flags (`BusesProperties`, `PluginDescriptor`) |
| **Return Types** | `bool` (process status), `juce::String` (state dump), `std::unique_ptr<juce::AudioProcessorEditor>` (editor factory) |

## 🏗️ 4. Architecture & Implementation Guide
### 4.1 Processor/Editor Separation
```cpp
// PluginProcessor.h
class MyPlugin : public juce::AudioProcessor {
public:
    MyPlugin() : apvts(*this, &undoManager, "Parameters", createParameterLayout()) {}
    void prepareToPlay(double sr, int samples) override { /* init buffers */ }
    void processBlock(juce::AudioBuffer<float>&, juce::MidiBuffer&) override { /* RT-safe */ }
    juce::AudioProcessorValueTreeState apvts;
};
```
### 4.2 Editor Binding
```cpp
// PluginEditor.h
class MyEditor : public juce::AudioProcessorEditor, private juce::Timer {
    juce::AudioProcessorValueTreeState::SliderAttachment sliderAtt;
public:
    MyEditor(MyPlugin& p) : AudioProcessorEditor(p), sliderAtt(p.apvts, "gain", gainSlider) {
        addAndMakeVisible(gainSlider);
        startTimerHz(30);
    }
    void timerCallback() override { gainSlider.setValue(apvts.getRawParameterValue("gain")->load()); }
};
```

## 🔗 5. Dependencies & Toolchain
- JUCE 7.0+, CMake 3.20+, Projucer (optional)
- VST3 SDK (Steinberg), Core Audio (macOS), ASIO (Windows)
- `juce::APVTS`, `juce::UndoManager`, `juce::ValueTree`

## ⚠️ 6. Edge Cases & Error Handling
| Edge Case | Symptom | Mitigation |
|-----------|---------|------------|
| **APVTS Race Conditions** | Parameter tearing, crashes | Use `apvts.state.copyState()` snapshots; avoid direct `load()` in `processBlock()` |
| **Editor Detach on Host Close** | UI disappears, audio continues | Implement `~MyEditor()` cleanup; detach listeners; stop timers |
| **High-DPI Font Clipping** | Text truncation, blurry rendering | Use `setUsingNativeTitleBar(false)`; query `desktopScaleFactor`; embed subset fonts |
| **Host Callback Deadlock** | DAW freezes on load | Never call blocking host methods from UI thread; defer to `AsyncUpdater` |

## 🛡️ 7. Real-Time Safety & Performance Constraints
- **RT Thread:** Zero allocations, no locks, no APVTS UI methods in `processBlock()`
- **UI Thread:** Cap updates to 30-60Hz via `Timer` or `MessageManager::callAsync`
- **Memory:** `< 10MB` per instance; pre-allocate `AudioBuffer` in `prepareToPlay()`

## 🤖 8. Usage Examples & AI Integration
- *Prompt:* "Generate a JUCE `AudioProcessorParameter` layout for a 4-band parametric EQ with APVTS attachment."
- *Prompt:* "Implement a custom `juce::LookAndFeel_V5` that draws a skeuomorphic rotary slider with SVG paths."

## 🧪 9. Testing & Validation Strategy
1. **Host Compatibility Matrix:** Test in Ableton, Logic, Reaper, FL Studio, Pro Tools
2. **State Preservation:** Save/load project, verify parameter recall and undo/redo integrity
3. **RT-Safety Scan:** Run ThreadSanitizer + custom `juce::MessageManager::isThisTheMessageThread()` checks in `processBlock()`
4. **Cross-Platform GUI:** Verify scaling on Windows 1x/125%/150%, macOS Retina, Linux GTK/Wayland

## 📝 10. Best Practices & Maintenance
- Prefer `AudioParameterFloat` over raw `float*` for DAW automation compatibility
- Use `juce::ComponentBoundsConstrainer` for resizable editors with min/max aspect ratios
- Keep `processBlock()` strictly audio/MIDI; defer heavy math or string parsing to background threads
- Bundle `LookAndFeel` assets via `BinaryData` to avoid external file dependencies

---
*Skill Version: 1.0.0 | Standards: JUCE 7.0+, VST3/AU/AAX/CLAP | Domain: Real-Time Audio & Plugin Architecture*