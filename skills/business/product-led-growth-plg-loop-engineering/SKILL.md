---
name: product-led-growth-plg-loop-engineering
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Product Led Growth Plg Loop Engineering", "opencode-migrated"]
    related_skills: []
---


# Skill: Product-Led Growth (PLG) Loop Engineering
## 📖 1. Overview
Implements viral sharing features (preset links, watermark-free demos) to drive organic user acquisition.
## ⚙️ 2. Core Functionality
- Shareable Presets: Encoded URLs, cloud sync, version control
- Demo Mode: Watermarked exports, time-limited features
- Referral Tracking: Unique codes, attribution analytics
- In-App Virality: "Share preset", "Challenge" modes
## 📥📤 3. Input/Output Schema
| Inputs | User presets, demo state, referral codes | Outputs | Shareable links, attribution logs, conversion metrics |
## 🏗️ 4. Architecture
`Base64` encode preset params → short URL → landing page → install → track referral. Watermark demo exports with "Try Pro".
## 🔗 5. Dependencies
`Short.io`, `Analytics SDK`, `Preset Serializer`
## ⚠️ 6. Edge Cases
| Expired Links | Broken UX | Auto-regenerate, cache fallback |
| Watermark Bypass | Revenue loss | Server-side validation, hard limit |
| Spam/Abuse | Platform ban | Rate limit shares, monitor anomalies |
## 🛡️ 7. Constraints
- Friction: < 3 clicks to share
- Conversion: > 15% free → paid
- Tracking: GDPR-compliant
## 🤖 8. Usage
- *Prompt:* "Generate a preset encoding/decoding system with shareable URLs and referral tracking for a DAW plugin."
## 🧪 9. Testing
- Link generation validation
- Watermark persistence test
- Referral attribution accuracy
## 📝 10. Best Practices
- Make sharing native to UI
- Reward referrals with credits
- Track conversion funnel meticulously
*Skill Version: 1.0.0 | Standards: PLG, Viral Loops, Analytics | Domain: Solo-Founder AI-Ops*