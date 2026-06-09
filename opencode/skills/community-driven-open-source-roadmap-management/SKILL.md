---
name: community-driven-open-source-roadmap-management
description: >-
  Use this skill when the user is working on or asking about open source roadmap, community governance, feature voting, public roadmap management, or open source project strategy.
version: 1.0.0
---

# Skill: Community-Driven Open Source Roadmap Management
## 📖 1. Overview
Manages feature requests via GitHub Discussions, Discord, and Upvoty to prioritize roadmap while maintaining product focus.
## ⚙️ 2. Core Functionality
- Request Aggregation: Sync GitHub/Discord to Upvoty/Jira
- Voting System: Weighted votes (paid users, contributors)
- Prioritization Matrix: Impact vs effort scoring
- Transparency: Public roadmap, status updates
## 📥📤 3. Input/Output Schema
| Inputs | Community requests, votes, dev capacity | Outputs | Prioritized backlog, roadmap status, update posts |
## 🏗️ 4. Architecture
Webhooks from GitHub/Discord → `n8n`/`Make` → Jira/Upvoty. Score: `votes * user_tier / effort`. Publish roadmap site.
## 🔗 5. Dependencies
`GitHub API`, `Discord API`, `Upvoty/Jira`, `n8n`
## ⚠️ 6. Edge Cases
| Vote Manipulation | Skewed priority | Require account verification, weight tiers |
| Scope Creep | Delayed releases | Cap roadmap, defer low-impact items |
| Community Friction | Negative feedback | Transparent communication, explain trade-offs |
## 🛡️ 7. Constraints
- Transparency: 100% public backlog
- Balance: 70% community / 30% core vision
- Velocity: Consistent delivery cadence
## 🤖 8. Usage
- *Prompt:* "Design a workflow that syncs GitHub Discussions to Jira, scores requests by votes and effort, and publishes a public roadmap."
## 🧪 9. Testing
- Vote integrity validation
- Prioritization logic audit
- Public sync accuracy
## 📝 10. Best Practices
- Weight paid user votes higher
- Explain rejected requests clearly
- Update roadmap weekly
*Skill Version: 1.0.0 | Standards: GitHub, Upvoty, Agile | Domain: Solo-Founder AI-Ops*