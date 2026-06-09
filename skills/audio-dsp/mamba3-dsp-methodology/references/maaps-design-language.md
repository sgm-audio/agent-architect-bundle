# MAAPS Plugin Suite — Design Language & UI Specs

> From Gemini system prompt for MAAPS UI/UX design. This defines the visual identity across all MAAPS plugins.

## Brand Identity

- **Product name:** MAAPS — "Mamba-3 Audio Adaptive Processing System"
- **Manufacturer:** SGM Studios (www.SGMStudios.com)
- **Formats:** VST3, CLAP, LV2, Standalone
- **Plugin window:** 900×600 px default, resizable (600×400 min, 1400×900 max)
- **Rendering:** OpenGL-accelerated (no external web views for shipped builds)
- **Font:** Inter or system sans-serif; monospace for operation log

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Obsidian | `#0D1117` | Primary background |
| Charcoal | `#161B22` | Secondary background, panels |
| Emerald | `#10B981` | Auditor / confidence-high |
| Cyan | `#06B6D4` | Observer / sync indicator |
| Amber | `#F59E0B` | Surgery highlights / confidence-medium |
| Rose | `#F43F5E` | Warnings / confidence-low |
| **Orange** | `#FF6B35` | **Primary accent (paramount)** |
| Text primary | `#E6EDF3` | Body text |
| Text muted | `#8B949E` | Secondary labels |

**Non-negotiable:** Matte black ash base (#0D1117-#161B22 range) with vibrant orange accents. No light mode. The aesthetic is Linear, Rive, or a high-end Eurorack module.

## Design Philosophy

1. **Dark mode only** — Deep charcoal/obsidian backgrounds, HSL-tailored accents
2. **No skeuomorphic knobs** — Clean sliders, number fields, horizontal LED-style meters. Precision instrument, not guitar pedal.
3. **Confidence is first-class** — Every AI suggestion annotated with 0-100% confidence. Low-confidence renders at reduced opacity or dashed outline. User sets a "confidence floor."
4. **Immutable Operation Log** — Scrollable timestamped audit trail at bottom. Each entry: what changed, from→to, confidence, click-to-revert. Builds trust.
5. **Progressive disclosure** — Default view shows ~6 essential sliders. "Advanced" chevron expands full params. Keyboard: `A`.
6. **Do no harm** — Bypass states prominent. Wet/dry always visible. Global "Safety Margin" slider biases toward doing less.
7. **Transient-coherent always** — Compression/saturation display shows "attack preserved" indicator.
8. **No latency reported** — Async hybrid architecture (0ms added latency). UI shows "Sync" indicator (green=in sync, amber=updating, red=stale).

## Component Inventory

| Component | Description |
|-----------|-------------|
| Header bar | Plugin name, preset browser, A/B compare, undo/redo, bypass, settings gear |
| Mode selector | Three-tab toggle: Cynical Engineer / Mix Engine / Surgical Tool |
| Meter bridge | Horizontal peak/RMS/LUFS meters per track, mini frequency thumbnail |
| Operation Log | Bottom-anchored, collapsible, timestamped event feed |
| Confidence indicator | Small arc/donut next to each AI-suggested parameter showing confidence % |
| Safety Margin slider | Global, always visible, biases entire processing chain |
| Cynicism Intensity slider | Mode-specific (Cynical Engineer), controls AI influence |
| Waveform Canvas | Mode-specific (Surgical Tool), scrollable with artifact overlays |
| Cross-Track Matrix | Mode-specific (Mix Engine), heatmap of frequency occupancy per track |
| Status bar | Sync indicator, model version, latency report, CPU usage |
| Bypass per module | Individual toggles for Gate, EQ, Compressor, Saturator |
| Advanced chevron | Toggle to reveal full parameter panels |

## UI Technical Approach

### WebView bridge (development) vs OpenGL (shipped)

For a single developer without a design team:

1. **Prototype in browser HTML/CSS/JS** — Design the UI as a standalone webpage. Use CSS transitions for glow effects. No C++ compilation needed for iteration.
2. **Bridge to plugin** via WebUI (webui.me) — 2 C files, uses OS-native webview (Edge/WKWebView/WebKitGTK). JSON message protocol between JS and C++.
3. **Migrate to OpenGL for shipping** — JUCE's `OpenGLAppComponent` or raw OpenGL can render the same layout for production builds without the webview dependency.

### JSON Bridge Protocol

```javascript
// JavaScript (UI) sends:
plugin.send({type: "setParam", id: "gain", value: 0.75});
plugin.send({type: "setMode", mode: "cynical_engineer"});

// C++ (plugin) sends:
sendToUI({type: "mambaState", value: 0.42});
sendToUI({type: "confidence", param: "gain", score: 87});
```

```cpp
// C++ receives:
void onMessageFromUI(const std::string& json) {
    auto msg = nlohmann::json::parse(json);
    if (msg["type"] == "setParam") setParameter(msg["id"], msg["value"]);
}
```

## Mode-Specific Designs

### 1. The Cynical Engineer — Self-Correcting Channel Strip
- DSP: Gate → 6-band ZDF EQ → feedback compressor → ADAA saturator
- AI: Predicts DSP parameter starting positions from signal + session context
- Key UX: "Auditor" with confidence scores. "Cynicism Intensity" slider controls AI influence
- Philosophy: A bored 55-year-old engineer who has heard it all. Does the minimum.

### 2. The Intelligent Mix Engine — Cross-Track Aggregator
- DSP: Multi-head attention across tracks, Bark-scale psychoacoustic masking
- AI: Coordinates frequency real estate across full session
- Key UX: Matrix/radar view showing frequency occupancy per track, draggable priority zones

### 3. The Precision Surgical Tool — De-Esser & De-Clicker
- DSP: Zero-crossing aligned micro-fades, sibilance detection via spectral classification
- AI: Detects/classifies transient artifacts, proposes surgical edits
- Key UX: "Waveform Surgery Canvas" — scrolling waveform with colored artifact highlights. Hover to audition, click to bypass, drag to adjust.

## Constraints

- WCAG AA contrast ratios
- Full keyboard navigation
- Screen reader labels
- Must feel native to DAW (Reaper, Ableton, Bitwig, Logic)
- No pop-up windows or dialogs
- Undo/redo integrates with DAW's native undo history
- Works at 1x, 1.5x, 2x DPI scaling (HiDPI/Retina)
