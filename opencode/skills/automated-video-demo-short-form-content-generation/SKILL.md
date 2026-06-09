---
name: automated-video-demo-short-form-content-generation
description: >-
  Use this skill when the user is working on or asking about automated product demo videos, short-form content generation, AI video creation, or marketing content automation.
version: 1.0.0
---

# Skill: Automated Video Demo & Short-Form Content Generation
## 📖 1. Overview
Uses CLI tools (Remotion, FFmpeg) + AI voiceover/screenplay to auto-generate plugin demos, tutorials, and social shorts from code.
## ⚙️ 2. Core Functionality
- Script Generation: LLM → screenplay → timestamps
- Rendering: Remotion/FFmpeg compositing, screen capture
- Voiceover: TTS API, lip-sync optional
- Scheduling: Auto-publish to YouTube/TikTok
## 📥📤 3. Input/Output Schema
| Inputs | Plugin API state, LLM script, TTS voice, brand assets | Outputs | MP4 videos, social shorts, metadata, publish logs |
## 🏗️ 4. Architecture
`node remotion render` → captures plugin UI → overlays TTS → FFmpeg encode → `yt-dlp` upload. Cron job triggers on releases.
## 🔗 5. Dependencies
`Remotion`, `FFmpeg`, `ElevenLabs/TTS`, `yt-dlp`
## ⚠️ 6. Edge Cases
| TTS Mispronunciation | Unnatural audio | Custom phonetic spelling, voice fine-tuning |
| Render Crash | Delayed release | Fallback to static image + voiceover |
| Platform Rejection | Copyright flag | Clear licensing, original assets only |
## 🛡️ 7. Constraints
- Quality: 1080p60, clean audio
- Latency: < 10 mins per video
- Compliance: Platform guidelines
## 🤖 8. Usage
- *Prompt:* "Generate a Remotion template that renders plugin UI, adds AI voiceover, and exports short-form videos from code."
## 🧪 9. Testing
- Render consistency check
- TTS quality audit
- Upload success validation
## 📝 10. Best Practices
- Keep scripts under 60s for shorts
- Use brand-consistent templates
- Schedule posts during peak hours
*Skill Version: 1.0.0 | Standards: Remotion, FFmpeg, TTS | Domain: Solo-Founder AI-Ops*