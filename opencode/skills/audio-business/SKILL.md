---
name: audio-business
description: >-
  Use this skill when the user is working on or asking about audio industry business, music tech startup, audio software monetization, or building a business around audio products.
version: 1.0.0
---

# Skill: Audio Business Management
## 📖 1. Overview
This skill covers audio business management including music licensing, copyright, business development, marketing, and financial management for audio professionals. It encompasses the business side of audio production, from rights management to revenue generation and strategic planning.
## ⚙️ 2. Core Functionality
- **Music Licensing:** Mechanical, synchronization, performance, and print licenses
- **Copyright Management:** Registration, enforcement, and infringement prevention
- **Business Development:** Partnerships, collaborations, and market expansion
- **Marketing & Promotion:** Brand building, audience engagement, and campaign strategy
- **Financial Management:** Budgeting, accounting, royalty tracking, and revenue optimization
## 📥📤 3. Input/Output Schema
| Category | Specification |
|----------|---------------|
| **Inputs** | Creative works, market data, legal documents, financial records, audience analytics |
| **Outputs** | Licensed works, copyright registrations, business plans, marketing campaigns, financial reports |
| **Return Types** | License agreements, royalty statements, marketing analytics, financial statements |
## 🏗️ 4. Architecture & Implementation Guide
### 4.1 Licensing Workflow
```python
def manage_music_licensing(work, usage_type, territory):
    # Identify rights holders
    rights_holders = identify_rights_holders(work)
    
    # Determine license type
    license_type = determine_license_type(usage_type)
    
    # Negotiate terms
    terms = negotiate_license_terms(rights_holders, license_type, territory)
    
    # Generate agreement
    agreement = create_license_agreement(work, license_type, terms)
    
    return agreement
```
### 4.2 Royalty Tracking System
```sql
CREATE TABLE royalty_tracking (
    id SERIAL PRIMARY KEY,
    work_id INTEGER REFERENCES works(id),
    usage_date DATE,
    territory VARCHAR(50),
    usage_type VARCHAR(30),
    gross_revenue DECIMAL(10,2),
    net_revenue DECIMAL(10,2),
    royalty_rate DECIMAL(5,4),
    royalty_amount DECIMAL(10,2),
    paid BOOLEAN DEFAULT FALSE,
    payment_date DATE
);
```
## 🔗 5. Dependencies & Toolchain
- Legal databases (ASCAP, BMI, SESAC, SOCAN, PRS)
- Accounting software (QuickBooks, Xero, FreshBooks)
- CRM systems (HubSpot, Salesforce, Zoho)
- Marketing platforms (Google Ads, Facebook Ads, Mailchimp)
- Project management tools (Asana, Trello, Notion)
- Rights management platforms (Songtrust, Tunecore, CD Baby)
## ⚠️ 6. Edge Cases & Error Handling
| Edge Case | Symptom | Mitigation |
|-----------|---------|------------|
| **Unclear Ownership** | Disputes over rights | Conduct thorough chain of title research |
| **International Royalties** | Missing foreign payments | Use global collection societies, audit statements |
| **License Expiration** | Unauthorized continued use | Implement renewal tracking, automated alerts |
| **Royalty Underpayment** | Revenue discrepancy | Regular audits, compare statements across societies |
## 🛡️ 7. Compliance & Legal Constraints
- **Copyright Term:** Life + 70 years (US), varies internationally
- **License Scope:** Territory, duration, media specific
- **Royalty Rates:** Statutory vs negotiated rates
- **Data Privacy:** GDPR, CCPA for customer information
## 🤖 8. Usage Examples & AI Integration
- *Prompt:* "Generate a music licensing agreement template for sync usage in film and television."
- *Prompt:* "Create a royalty tracking dashboard that aggregates income from multiple PROs and digital distributors."
## 🧪 9. Testing & Validation Strategy
1. **License Validation:** Verify against copyright office records
2. **Royalty Accuracy:** Sample audits against source data
3. **Contract Review:** Legal review of generated agreements
4. **Market Testing:** A/B test marketing campaigns
## 📝 10. Best Practices & Maintenance
- Maintain detailed records of all creative works
- Register copyrights promptly upon creation
- Diversify income streams beyond royalties
- Stay current with copyright law changes
- Use specialized audio industry accounting practices
---
*Skill Version: 1.0.0 | Standards: Copyright Law, Licensing Agreements, Royalty Structures | Domain: Audio Business*