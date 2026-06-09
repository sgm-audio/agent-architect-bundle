---
name: decentralized-storage-ipfs-for-sample-libraries
description: >-
  Use this skill when the user is working on or asking about IPFS, decentralized storage for audio samples, content-addressed audio files, or distributing sample libraries via Web3.
version: 1.0.0
---

# Skill: Decentralized Storage & IPFS for Sample Libraries
## 📖 1. Overview
Architects distribution using IPFS/BitTorrent to offload hosting costs for multi-gigabyte sample libraries while ensuring integrity via content addressing.
## ⚙️ 2. Core Functionality
- IPFS Pinning: `ipfs add`, gateway retrieval, CID verification
- Torrent Seeding: `aria2c`/`libtorrent` for P2P distribution
- Content Verification: SHA256 hash matching
- Bandwidth Throttling: Fair usage, CDN fallback
## 📥📤 3. Input/Output Schema
| Inputs | Sample library files, IPFS node, gateway config | Outputs | CIDs, download links, integrity logs, bandwidth stats |
## 🏗️ 4. Architecture
Plugin downloads `manifest.json` with CIDs. Fetches via `ipfs-http-client` or BitTorrent. Verifies hash on arrival. Caches locally.
## 🔗 5. Dependencies
`ipfs-http-client`, `libtorrent`, `aria2`, `checksum` utils
## ⚠️ 6. Edge Cases
| Gateway Downtime | Download stall | Fallback to CDN/mirror list |
| Hash Mismatch | Corrupt files | Retry, clear cache, verify manifest |
| High Cost | Pinning fees | Use decentralized pinning services, seed locally |
## 🛡️ 7. Constraints
- Integrity: 100% hash verification
- Latency: < 30s initial fetch
- Cost: < $0.01/GB distribution
## 🤖 8. Usage
- *Prompt:* "Generate a Python script that pins a sample library to IPFS, generates a manifest with CIDs, and verifies download integrity."
## 🧪 9. Testing
- Hash validation post-download
- Gateway fallback simulation
- Bandwidth stress test
## 📝 10. Best Practices
- Use `ipfs-cluster` for redundancy
- Document fallback mirrors
- Provide direct download option for low-bandwidth users
*Skill Version: 1.0.0 | Standards: IPFS, CID, BitTorrent | Domain: Opencode Architecture*