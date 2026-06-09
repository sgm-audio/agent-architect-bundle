---
name: telemetry-privacy-first-analytics
description: >-
  Use this skill when the user is working on or asking about privacy-first telemetry, anonymous usage analytics, GDPR-compliant analytics, or crash reporting without user tracking.
version: 1.0.0
---

# Skill: Telemetry & Privacy-First Analytics
## 📖 1. Overview
Implements GDPR/PIPEDA-compliant, opt-in telemetry tracking crashes, CPU usage, and feature popularity without identifying user data.
## ⚙️ 2. Core Functionality
- Anonymous IDs: Hashed machine IDs, no PII
- Event Batching: Queue events, periodic flush
- Privacy Controls: Opt-in toggle, data deletion endpoint
- Crash Reporting: Symbolicated stack traces, memory snapshots
## 📥📤 3. Input/Output Schema
| Inputs | Event data, user consent status, crash dumps | Outputs | Aggregated analytics, crash reports, compliance logs |
## 🏗️ 4. Architecture
`PostHog`/`Matomo` SDK. Background thread collects, encrypts, batches to `/api/batch`. Store local consent in `~/.config/`.
## 🔗 5. Dependencies
`PostHog C++`, `libcurl`, `libsentry`
## ⚠️ 6. Edge Cases
| Consent Revocation | Data retention violation | Immediately purge queue, block future sends |
| Network Failure | Lost metrics | Retry with backoff, drop oldest if full |
| PII Leak | Legal breach | Strip IPs, hash all strings, audit payloads |
## 🛡️ 7. Constraints
- Privacy: 0 PII collection
- Latency: < 10ms per event batch
- Storage: Local cache < 50MB
## 🤖 8. Usage
- *Prompt:* "Generate a C++ telemetry wrapper with opt-in consent, anonymous hashing, and PostHog batch flushing for audio plugin analytics."
## 🧪 9. Testing
- PII payload scanning
- Consent toggle validation
- Crash report anonymization check
## 📝 10. Best Practices
- Default to opt-out until explicit consent
- Document data retention policy
- Provide clear privacy policy link in UI
*Skill Version: 1.0.0 | Standards: GDPR, PIPEDA, PostHog | Domain: Opencode Architecture*