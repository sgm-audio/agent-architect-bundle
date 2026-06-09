---
name: subscription-micro-transaction-billing-architecture-stripe-paddle
description: >-
  Use this skill when the user is working on or asking about subscription billing, Stripe integration, Paddle payments, micro-transactions for audio plugins, or SaaS billing architecture.
version: 1.0.0
---

# Skill: Subscription & Micro-Transaction Billing Architecture (Stripe/Paddle)
## 📖 1. Overview
Configures payment gateways for Canadian tax collection (HST/GST/PST), subscriptions, and micro-transactions.
## ⚙️ 2. Core Functionality
- Tax Automation: Stripe Tax, Paddle merchant-of-record
- Subscription Lifecycle: Trials, proration, dunning, cancellations
- Micro-Transactions: In-app purchases, preset packs, usage credits
- Compliance: PIPEDA, PCI-DSS, Canadian tax rules
## 📥📤 3. Input/Output Schema
| Inputs | User location, product catalog, tax rates | Outputs | Invoices, tax receipts, subscription status, payout reports |
## 🏗️ 4. Architecture
`Stripe Checkout` or `Paddle.js`. Webhook handlers for `invoice.paid`, `subscription.canceled`. Local cache for entitlements.
## 🔗 5. Dependencies
`Stripe API`, `Paddle SDK`, `TaxJar/Stripe Tax`
## ⚠️ 6. Edge Cases
| Tax Rate Change | Revenue mismatch | Auto-sync rates, backdate adjustments |
| Failed Payment | Churn | Dunning retries, grace periods |
| Webhook Delay | Access denied | Local polling fallback, idempotent handlers |
## 🛡️ 7. Constraints
- Compliance: PCI-DSS Level 4+
- Accuracy: 100% tax calculation
- Reliability: < 1% failed payments
## 🤖 8. Usage
- *Prompt:* "Generate a Stripe webhook handler for subscription lifecycle with Canadian tax compliance and entitlement caching."
## 🧪 9. Testing
- Tax calculation validation
- Webhook retry simulation
- Dunning flow testing
## 📝 10. Best Practices
- Use Paddle for MoR simplicity
- Cache entitlements locally
- Audit tax reports monthly
*Skill Version: 1.0.0 | Standards: Stripe, Paddle, HST/GST/PST | Domain: Solo-Founder AI-Ops*