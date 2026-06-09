---
name: infrastructure-as-code-iac-for-audio-rendering
description: >-
  Use this skill when the user is working on or asking about IaC, Terraform, cloud audio rendering, scalable audio processing infrastructure, or deploying audio workloads on cloud.
version: 1.0.0
---

# Skill: Infrastructure-as-Code (IaC) for Audio Rendering
## 📖 1. Overview
Uses Terraform + Docker to provision scalable cloud environments with virtual audio drivers (JACK/ALSA) for batch/heavy audio processing.
## ⚙️ 2. Core Functionality
- Cloud Provisioning: AWS/GCP EC2/ECS, GPU optional
- Virtual Audio: PulseAudio/JACK/ALSA loopback, null sinks
- Container Orchestration: Docker Compose, Kubernetes
- Auto-Scaling: Batch job queues, cost-aware scaling
## 📥📤 3. Input/Output Schema
| Inputs | Terraform config, Dockerfiles, job manifests | Outputs | Provisioned instances, audio processing results, cost logs |
## 🏗️ 4. Architecture
`terraform apply` → EC2 + `docker-compose up` → JACK null sink → render jobs → S3 upload. Use `headless` mode, `ffmpeg` for output.
## 🔗 5. Dependencies
`terraform`, `docker`, `JACK`, `ALSA`, `AWS CLI`
## ⚠️ 6. Edge Cases
| Audio Driver Failure | Silent output | Verify `snd-dummy`, fallback to `libpulse` |
| GPU Unavailable | CPU bottleneck | Fallback to AVX/SIMD rendering |
| Cost Overrun | Budget breach | Implement spot instances, hard limits |
## 🛡️ 7. Constraints
- Cost: < $0.50/hr per instance
- Latency: N/A (offline batch)
- Reliability: 99.9% job success
## 🤖 8. Usage
- *Prompt:* "Generate a Terraform module for AWS EC2 that provisions Docker with JACK virtual audio driver for headless batch rendering."
## 🧪 9. Testing
- Dry-run provisioning validation
- Audio loopback test
- Cost estimation simulation
## 📝 10. Best Practices
- Use spot/preemptible instances
- Automate teardown after job
- Store results in versioned S3 buckets
*Skill Version: 1.0.0 | Standards: Terraform, Docker, JACK/ALSA | Domain: Opencode Architecture*