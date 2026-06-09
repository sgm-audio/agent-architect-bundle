---
name: interactive-mdx-gitbook-documentation-engineering
description: >-
  Use this skill when the user is working on or asking about MDX documentation, GitBook, interactive docs, documentation engineering, or building developer documentation sites.
version: 1.0.0
---

# Skill: Interactive MDX & GitBook Documentation Engineering
## 📖 1. Overview
Writes searchable, interactive manuals with embedded audio players and live parameter demos using MDX/GitBook.
## ⚙️ 2. Core Functionality
- MDX Components: Custom React/WASM audio players
- Search: Full-text, parameter index, versioned docs
- Live Demos: Embedded plugin UI, real-time parameter tweaking
- Versioning: Docs per release, migration guides
## 📥📤 3. Input/Output Schema
| Inputs | Markdown/MDX, audio samples, plugin WASM | Outputs | Interactive docs, search index, live demos |
## 🏗️ 4. Architecture
`next.js` + `@mdx-js/react`. Embed `AudioPlayer` component with `WASM DSP`. GitBook sync for versioning. Algolia search.
## 🔗 5. Dependencies
`MDX`, `GitBook`, `Web Audio API`, `Algolia`
## ⚠️ 6. Edge Cases
| WASM Load Failure | Broken demo | Fallback to static audio, retry button |
| Search Index Stale | Outdated results | Auto-sync on deploy, cache bust |
| Cross-Browser UI | Inconsistent rendering | Test Chrome/Safari/Firefox |
## 🛡️ 7. Constraints
- Performance: < 1s page load
- Accessibility: WCAG compliant
- Accuracy: 100% param match
## 🤖 8. Usage
- *Prompt:* "Generate an MDX component that embeds a WebAssembly DSP player with live parameter controls and audio preview."
## 🧪 9. Testing
- WASM compatibility check
- Search accuracy validation
- Accessibility audit
## 📝 10. Best Practices
- Version docs with releases
- Provide fallbacks for broken demos
- Update search index on deploy
*Skill Version: 1.0.0 | Standards: MDX, GitBook, Web Audio | Domain: Solo-Founder AI-Ops*