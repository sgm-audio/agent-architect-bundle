# WebView Plugin UI Architecture for CLAP Plugins

## Overview

Conventional plugin UIs use JUCE LookAndFeel, VSTGUI, or raw OpenGL rendering via
custom C++ frameworks. All require C++ compilation for every UI change, tight
coupling between DSP and presentation, and significant framework lock-in.

The WebView approach (used by iZotope RX/Ozone, Output Arcade, Baby Audio, LANDR)
renders the plugin UI as HTML/CSS/JavaScript inside a system-native webview,
communicating with the C++ plugin via JSON messages. This decouples UI
development from DSP development entirely.

## Architecture

```
┌──────────────────────────────────────────────────┐
│  CLAP Plugin (C++)                               │
│  ┌────────────────────────────────────────────┐  │
│  │  MambaInferenceEngine (ONNX RT)            │  │
│  │  ParamManager (atomic params)              │  │
│  │  WebUI Client (JSON message bridge)        │  │
│  └──────────┬─────────────────────────────────┘  │
│             │ JSON messages (std::string)         │
│  ┌──────────▼─────────────────────────────────┐  │
│  │  WebView (system native)                   │  │
│  │  ┌──────────────────────────────────┐      │  │
│  │  │  index.html + style.css + app.js │      │  │
│  │  │  (Figma → HTML export pipeline)   │      │  │
│  │  └──────────────────────────────────┘      │  │
│  └─────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────┘
```

## Library Choice: WebUI (webui.me)

| Criterion | WebUI | CEF (Chromium Embedded) |
|-----------|-------|------------------------|
| Binary size | ~100KB | ~50-100MB |
| Dependencies | 2 C files, MIT license | Full Chromium build |
| WebView used | System native (Edge/WKWebView/WebKitGTK) | Bundled Chromium |
| Setup | Single `.h` + `.c` | Complex build integration |
| API | `webui_interface` JSON bridge | C++ IPC, heavy |

**WebUI is strongly preferred for solo developers.** It uses the OS-native
webview — no bundling a browser. On Windows uses Edge WebView2 (ships with
Win11, redistributable for Win10), on macOS uses WKWebView (built-in), on
Linux uses WebKitGTK (installable via package manager).

## JSON Message Protocol

### C++ → JavaScript (state updates)

```json
{
  "type": "paramUpdate",
  "id": "gain",
  "value": 0.75,
  "confidence": 88,
  "bypassed": false
}
```

```json
{
  "type": "mambaState",
  "activity": 0.42,
  "stateSaturation": 0.15
}
```

### JavaScript → C++ (user actions)

```json
{
  "type": "setParam",
  "id": "intensity",
  "value": 0.6
}
```

```json
{
  "type": "loadPreset",
  "name": "Vocals Clean"
}
```

### C++ Bridge (skeleton)

```cpp
#include "webui.h"

class UiBridge {
    webui::window ui;
public:
    UiBridge() {
        ui.bind("setParam", [](const webui::event& e) {
            auto msg = nlohmann::json::parse(e.data);
            auto paramId = msg["id"].get<std::string>();
            auto value = msg["value"].get<float>();
            engine.setParameter(paramId, value);
        });
    }

    void sendToUI(const std::string& json) {
        ui.run(json);
    }

    void show() {
        ui.show("ui/index.html");
    }
};
```

## UI Development Workflow

1. **Design in Figma** — export to HTML/CSS
2. **Develop UI standalone** — open `index.html` in a browser, mock JSON
   messages with `setInterval` to test animations and state transitions
3. **Drop into plugin** — copy HTML+CSS+JS files to `plugin/assets/ui/`
4. **Wire JSON bridge** — implement the C++ message handlers
5. **Iterate** — CSS changes don't need recompilation; just WebView refresh

## CLAP Plugin GUI Extension Integration

CLAP plugins use the `clap_plugin_gui` extension to provide a window. The
WebView approach works within this extension:

```c
static bool gui_create(const clap_plugin* plugin, const char* api, bool is_floating) {
    // api is CLAP_WINDOW_API_WIN32, CLAP_WINDOW_API_COCOA, or CLAP_WINDOW_API_X11
    // Create WebUI window, embed in the host-provided parent window
    auto* bridge = (UiBridge*)plugin->plugin_data;
    bridge->show();
    return true;
}
```

WebUI supports embedding into a parent window handle, which is exactly what
CLAP's `gui_create` provides. Pass the host's window handle to `webui_set_parent()`.

## Pros and Cons vs Conventional C++ UI

| | WebView | Conventional (JUCE/VSTGUI) |
|---|---|---|
| Development speed | Fast — CSS hot-reload, browser devtools | Slow — recompile for every UI change |
| Visual quality | Unlimited — CSS transitions, Canvas, WebGL | Limited to framework primitives |
| Tooling | Chrome DevTools, Figma export | Plugin-specific debuggers |
| Binary size | +~100KB (WebUI) | +~2MB (JUCE GUI module) |
| Build time | Zero recompile for UI changes | Full rebuild |
| Skill requirement | HTML/CSS/JS | C++ + framework API |
| CLAP integration | Via `clap_plugin_gui` + `webui_set_parent()` | Via JUCE's CLAP support or raw C API |

## Cynical Engineer UI Layout (900×600)

Based on the MAAPS design spec (matte black ash #0D1117–#161B22, orange accents):

```
┌─ Header ──────────────────────────────────────────────┐
│  [MAAPS]  [Preset: ──────▼]  [A/B]  [↶]  [↷]  [⏻]  │
├─ Mode Selector ───────────────────────────────────────┤
│  [Cynical Engineer] [Mix Engine] [Surgical Tool]      │
├─ Main Content ────────────────────────────────────────┤
│                                                       │
│  ┌─ Gate ─┐  ┌─ EQ ───────────┐  ┌─ Comp ─┐  ┌─ Sat ─┐│
│  │ Thr ── │  │ 20Hz  200  2k  │  │ Thr ── │  │ Drv ── ││
│  │ Rel ── │  │ ┌──────────────┐│  │ Rat ── │  │ Mix ── ││
│  │       │  │ │  spectrum     ││  │ Atk ── │  │       ││
│  │ [B]   │  │ └──────────────┘│  │ Rel ── │  │ [B]   ││
│  └───────┘  └─────────────────┘  └────────┘  └───────┘│
│                                                       │
│  ┌── Observer ──┐  ┌── Auditor ──┐  ┌── Safety ─────┐│
│  │ ⬤ 0.88      │  │ ◕ 0.72     │  │ [──────────]  ││
│  │ Session: 67% │  │ Cynicism:  │  │ 85% confidence ││
│  └──────────────┘  └─────────────┘  └───────────────┘│
├─ Operation Log ───────────────────────────────────────┤
│ 12:34:22  gain +2.3dB  (88%)  [↩]                    │
│ 12:34:20  eq @4.2kHz -1.1dB (72%)  [↩]               │
│ [+ show more]                                         │
└───────────────────────────────────────────────────────┘
```

Color palette: bg=#0D1117, surface=#161B22, accent=#FF6B35 (orange),
text=#E6EDF3, dim=#8B949E, green=#10B981, cyan=#06B6D4, amber=#F59E0B

## Key Design Principles (from MAAPS spec)

1. **No skeuomorphic knobs** — use sliders, number fields, LED-style meters
2. **Confidence is first-class** — AI-suggested params show confidence %;
   low confidence = reduced opacity or dashed outline
3. **Immutable Operation Log** — scrollable, timestamped audit trail at bottom
4. **Progressive disclosure** — default shows ~6 sliders, "Advanced" chevron
   expands full params (keyboard shortcut: `A`)
5. **Safety Margin always visible** — biases the entire chain toward doing less
6. **Sync indicator** — green = in sync, amber = updating, red = stale/fallback
