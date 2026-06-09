---
name: ai-assisted-software-engineering-cursor-copilot-pro
description: >-
  Use this skill when the user is working on or asking about AI coding tools, Cursor IDE, GitHub Copilot, AI pair programming, or using AI assistants in the software development workflow.
version: 1.0.0
---

# Skill: AI-Assisted Software Engineering (Cursor / Copilot Pro)
## 📖 1. Overview
Masters advanced prompting, `.cursorrules`, and system instructions to accelerate C++ DSP, test generation, and debugging.
## ⚙️ 2. Core Functionality
- Context Management: `.cursorrules` for code style, architecture, DSP constraints
- Prompt Chaining: Multi-step generation, validation loops
- Code Review Automation: Lint suggestions, bug detection, performance hints
- Debugging Assistance: Stack trace analysis, memory leak identification
## 📥📤 3. Input/Output Schema
| Inputs | Source code, error logs, `.cursorrules`, prompts | Outputs | Generated code, PR reviews, debug suggestions, refactors |
## 🏗️ 4. Architecture
Configure `~/.cursorrules` with `RT-Safe`, `No-Exceptions`, `JUCE7` constraints. Use `@workspace` context. Chain prompts for test + implementation.
## 🔗 5. Dependencies
`Cursor`, `GitHub Copilot`, `clang-tidy`, `LLM API`
## ⚠️ 6. Edge Cases
| Hallucination | Incorrect DSP math | Validate against reference, unit tests |
| Context Overflow | Lost constraints | Chunk prompts, use explicit references |
| Style Drift | Inconsistent code | Enforce `.cursorrules` on every commit |
## 🛡️ 7. Constraints
- Accuracy: 100% RT-safe compliance
- Speed: 5x dev velocity
- Safety: Review all AI output before merge
## 🤖 8. Usage
- *Prompt:* "Generate a `.cursorrules` file enforcing JUCE7, RT-safe constraints, and C++20 standards for audio plugin development."
## 🧪 9. Testing
- AI output vs reference validation
- Context window stress test
- Style consistency check
## 📝 10. Best Practices
- Explicitly define RT constraints
- Always run CI/CD before merging AI code
- Maintain human code review gate
*Skill Version: 1.0.0 | Standards: Cursor, Copilot, .cursorrules | Domain: Solo-Founder AI-Ops*