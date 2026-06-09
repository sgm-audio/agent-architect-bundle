---
name: website-design
description: "Design system creation, UI/UX planning, and visual specification for modern websites. Use when starting a new web project, creating design systems, choosing color palettes, planning layouts, or specifying typography. Covers design tokens, component libraries, responsive grids, accessibility in design, and design-to-development handoff."
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Website Design", "opencode-migrated"]
    related_skills: []
---


# Website Design Skill

## Design System Fundamentals

### Design Tokens
Define these tokens before any component work:

**Colors:**
- Primary brand color + 10 shades (50-950)
- Secondary/accent color + 5 shades
- Neutral grays (at least 9 steps)
- Semantic colors (success, warning, error, info)
- Background/surface colors

**Typography:**
- Font families (heading, body, mono)
- Scale: 12px, 14px, 16px, 18px, 20px, 24px, 30px, 36px, 48px, 60px, 72px
- Line heights: 1.25 (headings), 1.5 (body), 1.75 (long-form)
- Font weights: 400, 500, 600, 700
- Letter spacing: -0.02em (large headings), 0 (body), 0.05em (small/caps)

**Spacing:**
- Base unit: 4px
- Scale: 0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96
- Container max-widths: 640px, 768px, 1024px, 1280px, 1536px

**Breakpoints:**
- sm: 640px, md: 768px, lg: 1024px, xl: 1280px, 2xl: 1536px

### shadcn/ui Component Setup

Standard components to install:
```bash
npx shadcn add button card input label textarea select dialog sheet tabs accordion avatar badge separator skeleton
```

## Page Structure Templates

### Landing Page Sections (in order)
1. Navigation (sticky, transparent -> solid on scroll)
2. Hero (value prop + CTA + visual)
3. Social proof (logos, testimonials)
4. Features/benefits (3-6 cards)
5. How it works (3-4 steps)
6. Pricing (if applicable)
7. FAQ (accordion)
8. CTA section
9. Footer

### Common Page Types
- Home/Landing, About, Services/Features, Pricing, Contact, Blog/Resources, Case Studies, Legal (Privacy, Terms)

## Accessibility Checklist

- [ ] Color contrast 4.5:1 minimum (7:1 for large text)
- [ ] Focus indicators visible on all interactive elements
- [ ] Heading hierarchy logical (no skips)
- [ ] Alt text for all meaningful images
- [ ] Form labels associated with inputs
- [ ] Skip navigation link
- [ ] Keyboard accessible dropdowns/menus
- [ ] Reduced motion respected (`prefers-reduced-motion`)

## Performance Budget

- First Contentful Paint: < 1.8s
- Largest Contentful Paint: < 2.5s
- First Input Delay: < 100ms
- Cumulative Layout Shift: < 0.1
- Total page weight: < 2MB (initial load)
