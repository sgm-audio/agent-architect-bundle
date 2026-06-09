---
name: setup-browser-cookies
version: 1.0.0
description: >
  Use this skill to import cookies from your real browser (Comet, Chrome, Arc, Brave, Edge) into a headless browse session. Opens an interactive picker UI where you select which cookie domains to import. Use before QA testing authenticated pages.
allowed-tools:
  - Bash
  - Read
  - Question
---

# Setup Browser Cookies

Import logged-in sessions from your real Chromium browser into the headless browse session.

## How it works

1. Check that Playwright/Chromium is available
2. Ask the user which browser to import from and which domains
3. Guide the user through cookie setup

## Workflow

Since opencode does not have the gstack compiled `$B` binary, cookie import requires an alternative approach:

### Option A: Playwright script (recommended if Playwright is installed)

```bash
npx playwright
```

Check if Playwright is available. If not, offer to install it:

```bash
npx playwright install chromium
```

### Option B: Manual cookie setup

If Playwright is not available or the user prefers manual setup:

1. Ask the user to open their browser's DevTools (F12) on the target site
2. Go to Application → Cookies → Select domain
3. Export cookies or provide session details
4. Ask the user: "What domain(s) do you need authenticated access to?"

### Cookie handling

When testing authenticated pages:
- Never store real credentials in files or logs
- Session cookies typically expire; ask the user to refresh if auth fails
- For local dev apps, suggest creating a test user with known credentials instead

### Verify

After cookies are set up, verify by navigating to the target domain and checking that the page loads as an authenticated user would see it.
