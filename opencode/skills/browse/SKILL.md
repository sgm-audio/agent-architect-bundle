---
name: browse
version: 1.1.0
description: >
  Use this skill for headless browser automation, QA testing, and site dogfooding. Navigate URLs, interact with elements, verify page state, take screenshots, check responsive layouts, test forms, and assert element states. Adapts to available tooling — Playwright via npx, Puppeteer, or built-in tools.
allowed-tools:
  - Bash
  - Read
  - Write
  - Question
---

# Browse: QA Testing & Dogfooding

Headless browser automation for testing web applications. Since opencode does not include the gstack compiled `$B` binary, this skill adapts to whatever browser automation tools are available.

## Setup (run this check before any browse command)

Check which browser tools are available:

```bash
# Check for Playwright (via npx)
if npx playwright --version 2>/dev/null; then
  echo "PLAYWRIGHT_AVAILABLE"
# Check for Puppeteer
elif npx puppeteer --version 2>/dev/null || node -e "require('puppeteer')" 2>/dev/null; then
  echo "PUPPETEER_AVAILABLE"
else
  echo "NEEDS_SETUP"
fi
```

### If NEEDS_SETUP

Offer to install Playwright:

```bash
npm install -g playwright && npx playwright install chromium
```

Or ask the user which browser tool they prefer.

### Using Playwright directly

When Playwright is available, write small scripts on-the-fly to `%TEMP%` or the project root:

```bash
# Example: navigate and screenshot
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('$URL');
  await page.screenshot({ path: 'screenshot.png', fullPage: true });
  const title = await page.title();
  console.log('Title:', title);
  const content = await page.textContent('body');
  console.log('Body text (first 1000 chars):', content.substring(0, 1000));
  await browser.close();
})();
"
```

### Using Puppeteer directly

```bash
node -e "
const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('$URL');
  await page.screenshot({ path: 'screenshot.png', fullPage: true });
  const title = await page.title();
  console.log('Title:', title);
  await browser.close();
})();
"
```

## Core QA Patterns

### 1. Verify a page loads correctly

Write a script that:
- Navigates to the URL
- Captures page text content
- Checks for key elements
- Reports any console errors

### 2. Test a user flow

For interactive flows (login, form submission, etc.), write a Playwright script that:
- Navigates to the starting page
- Fills form fields
- Clicks submit buttons
- Takes screenshots before/after actions
- Asserts the expected success state appears

### 3. Visual evidence for bug reports

Generate annotated screenshots and console logs:

```bash
# Capture full-page screenshot
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  page.on('console', msg => console.log('CONSOLE:', msg.type(), msg.text()));
  page.on('pageerror', err => console.log('PAGE_ERROR:', err.message));
  await page.goto('$URL', { waitUntil: 'networkidle' });
  await page.screenshot({ path: 'bug-report.png', fullPage: true });
  await browser.close();
})();
"
```

### 4. Test responsive layouts

```bash
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  for (const [name, vp] of Object.entries({mobile: [375,812], tablet: [768,1024], desktop: [1280,720]})) {
    const ctx = await browser.newContext({ viewport: { width: vp[0], height: vp[1] } });
    const page = await ctx.newPage();
    await page.goto('$URL', { waitUntil: 'networkidle' });
    await page.screenshot({ path: name + '.png', fullPage: true });
    await ctx.close();
  }
  await browser.close();
})();
"
```

### 5. Check console for errors

Monitor console messages during page load and interactions. Log all errors and warnings.

### 6. Assert element states

Check for element visibility, enabled/disabled state, and text content:

```bash
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('$URL');
  console.log('visible:', await page.isVisible('$SELECTOR'));
  console.log('enabled:', await page.isEnabled('$SELECTOR'));
  console.log('text:', await page.textContent('$SELECTOR'));
  await browser.close();
})();
"
```

## Output structure

When running QA tasks with browse:

```
qa-reports/
├── qa-report-{domain}-{YYYY-MM-DD}.md
└── screenshots/
    ├── homepage.png
    ├── issue-001-before.png
    ├── issue-001-after.png
    └── ...
```

## Important notes

- Screenshots are saved to the project root or `qa-reports/screenshots/` directory
- Console errors are captured and logged for every page
- Never store credentials in scripts or logs — use environment variables or prompt the user
- For authenticated pages, use the `setup-browser-cookies` skill or ask the user for test credentials
