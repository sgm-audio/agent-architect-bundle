---
name: bootstrap-financial-engineering-unit-economics
description: ">-"
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Bootstrap Financial Engineering Unit Economics", "opencode-migrated"]
    related_skills: []
---


# Skill: Bootstrap Financial Engineering & Unit Economics
## 📖 1. Overview
Manages cash flows, models LTV/CAC ratios, and optimizes hosting/AI API costs for profitable independence.
## ⚙️ 2. Core Functionality
- Cash Flow Tracking: Revenue, expenses, runway monitoring
- LTV/CAC Modeling: Cohort analysis, churn prediction
- Cost Optimization: AI API batching, cloud instance right-sizing
- Profitability Metrics: Gross margin, net profit, break-even
## 📥📤 3. Input/Output Schema
| Inputs | Sales data, API usage, cloud bills, churn rates | Outputs | Financial models, unit economics reports, optimization plans |
## 🏗️ 4. Architecture
`Stripe` + `QuickBooks` API → `Python/Excel` model. Calculate `LTV = ARPU / Churn`, `CAC = Marketing / New Users`. Optimize API calls via batching.
## 🔗 5. Dependencies
`Stripe`, `QuickBooks`, `Python/Pandas`, `Cloud Billing API`
## ⚠️ 6. Edge Cases
| Churn Spike | LTV drop | Investigate root cause, improve retention |
| API Overrun | Profit margin loss | Implement quotas, caching, fallback models |
| Tax Liability | Cash flow crunch | Quarterly estimates, reserve fund |
## 🛡️ 7. Constraints
- Profitability: > 20% net margin
- Runway: > 12 months cash
- Efficiency: < $0.01/API request
## 🤖 8. Usage
- *Prompt:* "Generate a Python LTV/CAC model that ingests Stripe data, calculates cohort retention, and optimizes cloud/AI costs."
## 🧪 9. Testing
- Model accuracy vs actuals
- Cost optimization validation
- Runway stress testing
## 📝 10. Best Practices
- Review metrics monthly
- Batch AI API calls aggressively
- Maintain 3-month emergency reserve
*Skill Version: 1.0.0 | Standards: SaaS Metrics, Unit Economics, Financial Modeling | Domain: Solo-Founder AI-Ops*