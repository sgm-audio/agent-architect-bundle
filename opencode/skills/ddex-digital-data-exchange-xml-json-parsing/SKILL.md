---
name: ddex-digital-data-exchange-xml-json-parsing
description: >-
  Use this skill when the user is working on or asking about DDEX, digital data exchange for music, ERN messages, parsing music metadata XML/JSON, or music rights metadata standards.
version: 1.0.0
---

# Skill: DDEX (Digital Data Exchange) XML/JSON Parsing
## 📖 1. Overview
Implements DDEX ERN/MEAD standards to preserve metadata integrity from plugin/DAW through to streaming platforms.
## ⚙️ 2. Core Functionality
- Schema Validation: XSD/JSON Schema compliance
- Metadata Mapping: ISRC, IPI, IPN, contributor roles
- Batch Processing: Large catalog export/import
- Versioning: ERN 4.2 vs 4.3 support
## 📥📤 3. Input/Output Schema
| Inputs | Track/project data, DDEX schemas | Outputs | Validated XML/JSON files, mapping logs, error reports |
## 🏗️ 4. Architecture
`libxml2`/`jsonschema` validators. Map DAW metadata to `NewReleaseMessage`. Validate, export, archive.
## 🔗 5. Dependencies
`libxml2`, `jsonschema`, DDEX 4.3 XSD
## ⚠️ 6. Edge Cases
| Missing Mandatory Fields | Invalid DDEX | Enforce pre-export validation |
| Character Encoding | XML parse errors | Force UTF-8, sanitize strings |
| Schema Version Mismatch | Platform rejection | Detect version, transform accordingly |
## 🛡️ 7. Constraints
- Compliance: 100% DDEX valid
- Speed: < 2s per track export
- Accuracy: Zero metadata loss
## 🤖 8. Usage
- *Prompt:* "Generate a DDEX 4.3 ERN parser that validates ISRC, contributor roles, and exports to streaming-compliant XML."
## 🧪 9. Testing
- XSD validation suite
- Cross-platform compatibility check
- Metadata round-trip test
## 📝 10. Best Practices
- Version schemas explicitly
- Use strict validation pre-export
- Document field mappings clearly
*Skill Version: 1.0.0 | Standards: DDEX ERN 4.3, XSD, JSON Schema | Domain: Canadian Music Infrastructure*