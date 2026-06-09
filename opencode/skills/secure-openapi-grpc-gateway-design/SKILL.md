---
name: secure-openapi-grpc-gateway-design
description: >-
  Use this skill when the user is working on or asking about OpenAPI, gRPC gateway, secure API design for audio services, REST/gRPC bridge, or API authentication for audio backends.
version: 1.0.0
---

# Skill: Secure OpenAPI & gRPC Gateway Design
## 📖 1. Overview
Designs low-latency, secure APIs connecting desktop plugins to cloud services (AI generation, licensing) without disrupting DAW stability.
## ⚙️ 2. Core Functionality
- Async HTTP/gRPC: Background thread communication, non-blocking I/O
- Protocol Buffers: Efficient serialization, versioned schemas
- Authentication: OAuth2, JWT, short-lived tokens
- Rate Limiting & Retry: Exponential backoff, circuit breakers
## 📥📤 3. Input/Output Schema
| Inputs | Plugin state, user token, cloud endpoint | Outputs | API responses, validation status, fallback data |
## 🏗️ 4. Architecture
`gRPC client` runs on `juce::Thread`. Queue requests via lock-free ring buffer. Parse protobufs. Update UI via `MessageManager`.
## 🔗 5. Dependencies
`grpc`, `protobuf`, `curl`, `JWT-CPP`
## ⚠️ 6. Edge Cases
| Network Timeout | Plugin freeze | Circuit breaker, timeout < 3s, fallback |
| Token Expiry | 401 errors | Auto-refresh, cache refresh token |
| Payload Bloat | Dropped frames | Compress with gzip, chunk large uploads |
## 🛡️ 7. Constraints
- Latency: < 100ms round-trip
- Reliability: 99.5% success with retries
- Security: TLS 1.3, zero plaintext secrets
## 🤖 8. Usage
- *Prompt:* "Generate a gRPC C++ client wrapper with circuit breaker and JWT auth for a cloud AI audio generation service."
## 🧪 9. Testing
- Network fault injection
- Token rotation validation
- Payload size benchmarking
## 📝 10. Best Practices
- Keep payloads < 1MB
- Use unary RPCs for simple queries
- Implement offline mode gracefully
*Skill Version: 1.0.0 | Standards: gRPC, Protobuf, OAuth2 | Domain: Opencode Architecture*