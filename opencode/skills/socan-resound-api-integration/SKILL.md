---
name: socan-resound-api-integration
description: >-
  Use this skill when the user is working on or asking about SOCAN, Re:Sound, Canadian music royalties, performing rights reporting, or integrating with Canadian PRO APIs.
version: 1.0.0
---

# Skill: SOCAN & Re:Sound API Integration
## 📖 1. Overview
Architects software to interact with Canadian PROs (SOCAN) and neighboring rights (Re:Sound) for automated cue-sheet submission and performance logging.
## ⚙️ 2. Core Functionality
- API Authentication: OAuth2, API keys, rate limiting
- Cue Sheet Formatting: XML/JSON mapping to SOCAN standards
- Submission Pipeline: Queue, validate, retry, log
- Status Tracking: Poll for acceptance/rejection
## 📥📤 3. Input/Output Schema
| Inputs | Track metadata, usage logs, API credentials | Outputs | Submission receipts, status updates, compliance reports |
## 🏗️ 4. Architecture
`POST /api/v1/cuesheets` with ISRC/ISWC, timestamps, usage type. Validate against schema. Queue with exponential backoff. Store receipts.
## 🔗 5. Dependencies
`SOCAN API`, `Re:Sound Portal`, `libcurl`, `XML/JSON parsers`
## ⚠️ 6. Edge Cases
| API Downtime | Failed submissions | Queue locally, retry on recovery |
| Invalid Metadata | Rejection | Pre-validate ISRC, enforce strict schema |
| Rate Limits | Blocked | Throttle requests, respect `Retry-After` |
## 🛡️ 7. Constraints
- Accuracy: 100% schema compliance
- Latency: Async submission (< 5s UI impact)
- Compliance: PIPEDA data handling
## 🤖 8. Usage
- *Prompt:* "Generate a C++ API client that formats DAW project metadata into SOCAN-compliant cue sheets and handles submission retries."
## 🧪 9. Testing
- Mock API validation
- Schema compliance check
- Retry/backoff logic test
## 📝 10. Best Practices
- Cache credentials securely
- Log submission IDs for audit
- Provide user status dashboard
*Skill Version: 1.0.0 | Standards: SOCAN, Re:Sound, OAuth2 | Domain: Canadian Music Infrastructure*