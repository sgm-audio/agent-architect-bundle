---
name: bilingual-ux-accessibility-compliance-bill-96-aoda
description: >-
  Use this skill when the user is working on or asking about Bill 96, AODA, Quebec French language law, bilingual UI, Canadian accessibility compliance, or French-English software requirements.
version: 1.0.0
---

# Skill: Bilingual UX & Accessibility Compliance (Bill 96 / AODA)
## 📖 1. Overview
Designs dual-language (EN/FR) interfaces complying with Quebec Bill 96 and Ontario AODA/WCAG accessibility standards.
## ⚙️ 2. Core Functionality
- i18n Architecture: String tables, locale detection, RTL support
- WCAG 2.2: Contrast ratios, keyboard nav, screen reader labels
- Bill 96: French prominence, auto-locale on Quebec IPs
- Accessibility Testing: Automated scanners, manual audits
## 📥📤 3. Input/Output Schema
| Inputs | UI strings, locale settings, accessibility rules | Outputs | Localized UI, compliance reports, audit logs |
## 🏗️ 4. Architecture
`gettext`/`QtTr` for i18n. WCAG contrast checker in CI. Keyboard focus rings. Screen reader ARIA labels in UI components.
## 🔗 5. Dependencies
`gettext`, `axe-core`, `Bill 96 Guidelines`, `WCAG 2.2`
## ⚠️ 6. Edge Cases
| Incomplete Translation | Legal risk | Fallback to English, log missing strings |
| Contrast Failure | Accessibility violation | Enforce palette validator in build |
| Keyboard Trap | Usability failure | Test tab order, focus management |
## 🛡️ 7. Constraints
- Compliance: 100% Bill 96/AODA
- Latency: Zero UI performance impact
- Accuracy: Professional translation QA
## 🤖 8. Usage
- *Prompt:* "Generate a CI pipeline that scans UI strings for missing FR translations and validates WCAG 2.2 AA contrast ratios."
## 🧪 9. Testing
- Automated contrast/accessibility checks
- French locale smoke test
- Screen reader validation
## 📝 10. Best Practices
- Use professional translators
- Test with actual assistive tech
- Document compliance in manual
*Skill Version: 1.0.0 | Standards: Bill 96, WCAG 2.2, AODA | Domain: Canadian Music Infrastructure*