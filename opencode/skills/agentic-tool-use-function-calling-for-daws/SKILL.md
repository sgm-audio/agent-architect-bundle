---
name: agentic-tool-use-function-calling-for-daws
description: >-
  Use this skill when the user is working on or asking about AI agents controlling a DAW, tool-calling for audio plugins, LLM-to-DAW bridge, or function calling for music production.
version: 1.0.0
---

# Skill: Agentic Tool-Use (Function Calling) for DAWs
## 📖 1. Overview
Enables LLM agents to execute DAW actions by translating natural language to exact plugin parameters, MIDI routing, and automation curves via structured tool schemas.
## ⚙️ 2. Core Functionality
- Tool Definition: JSON schema for `set_param`, `create_track`, `insert_plugin`
- Intent Parsing: LLM → structured JSON → DAW host API
- Parameter Mapping: Natural language ("compress vocal 3dB") → exact ratio/threshold
- Safety Gating: User confirmation for destructive actions
## 📥📤 3. Input/Output Schema
| Inputs | User intent, tool schemas, DAW API state, plugin descriptors | Outputs | JSON action queue, execution status, parameter diffs |
## 🏗️ 4. Architecture
LLM returns `{"tool": "set_plugin_param", "args": {"id": "comp_1", "param": "threshold", "value": -15}}`. Validate against schema, execute via host API, return confirmation.
## 🔗 5. Dependencies
`jsonschema`, DAW host extensions (CLAP/JUCE), LLM function-calling API
## ⚠️ 6. Edge Cases
| Invalid Parameter ID | Execution fails | Fuzzy matching, UI picker fallback |
| Destructive Action | Accidental bypass/mute | Require modal confirmation for `delete`/`bypass` |
| Ambiguous Intent | Wrong track modified | Clarify prompt, return options |
## 🛡️ 7. Constraints
- Execution Latency: < 200ms per action
- Safety: 100% user-confirmed for state changes
- Rollback: Maintain undo stack for all actions
## 🤖 8. Usage
- *Prompt:* "Generate a JSON schema for DAW tool-calling that maps 'EQ high-shelf boost 4dB at 10k' to APVTS parameters."
## 🧪 9. Testing
- Intent-to-parameter accuracy tests
- Undo/redo round-trip validation
- Safety gate bypass attempts
## 📝 10. Best Practices
- Always return structured JSON, never raw text
- Validate params before execution
- Log actions for audit/undo
*Skill Version: 1.0.0 | Standards: JSON Schema, Function Calling, DAW API | Domain: Audio AI & ML*