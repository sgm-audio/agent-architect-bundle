---
name: cmrra-soproq-royalty-workflow-design
description: >-
  Use this skill when the user is working on or asking about CMRRA, SOPROQ, mechanical royalties in Canada, Quebec music licensing, or Canadian mechanical royalty workflow.
version: 1.0.0
---

# Skill: CMRRA & SOPROQ Royalty Workflow Design
## 📖 1. Overview
Tracks and routes mechanical royalties (CMRRA) and equitable remuneration (SOPROQ) for Canadian independent artists.
## ⚙️ 2. Core Functionality
- Split Sheet Management: Contributor percentages, IPI/IPN mapping
- Usage Tracking: Stream/download counts, territory routing
- Payout Calculation: Rate application, currency conversion
- Audit Logging: Transparent ledger for all transactions
## 📥📤 3. Input/Output Schema
| Inputs | Usage data, split sheets, royalty rates | Outputs | Payout statements, ledger logs, compliance reports |
## 🏗️ 4. Architecture
Database: `contributors`, `splits`, `usage`. Cron job calculates: `payout = usage * rate * split`. Export to CMRRA/SOPROQ format.
## 🔗 5. Dependencies
`PostgreSQL`, `CMRRA API`, `SOPROQ Portal`, `currency converter`
## ⚠️ 6. Edge Cases
| Split Discrepancy | Legal dispute | Require dual signature for changes |
| Currency Fluctuation | Payout variance | Use mid-day rates, document conversions |
| Missing IPI | Rejection | Enforce pre-registration validation |
## 🛡️ 7. Constraints
- Accuracy: < 0.01% calculation error
- Compliance: CMRRA/SOPROQ standards
- Transparency: Immutable audit trail
## 🤖 8. Usage
- *Prompt:* "Generate a royalty calculation engine that processes stream counts, applies split percentages, and exports CMRRA/SOPROQ-compliant statements."
## 🧪 9. Testing
- Calculation accuracy validation
- Split change audit trail
- Currency conversion stress
## 📝 10. Best Practices
- Immutable ledger entries
- Require contributor approval for splits
- Archive all rate changes
*Skill Version: 1.0.0 | Standards: CMRRA, SOPROQ, Accounting | Domain: Canadian Music Infrastructure*