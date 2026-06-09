---
name: gumroad-digital-product
description: "Package, price, and ship a digital product on Gumroad — license keys, merchant-of-record tax handling, content/file delivery, and update delivery. Use whenever setting up or refining a Gumroad listing for software/scripts/downloads, deciding how to gate access to a paid ReaPack repo, generating or verifying license keys, or writing the product page copy. Especially use it when turning a finished tool into a paid release."
version: 1.0.0
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Gumroad Digital Product", "opencode-migrated"]
    related_skills: ["hermes-skill-publishing"]
---


# Selling a digital product on Gumroad

Built for the concrete case: a paid REAPER ReaScript bundle (TrackClear Pro)
delivered as a private ReaPack repo URL + a fallback zip, sold by Scott Gilbert
Mills. Generalizes to any digital download.

> Verify the current **fee** and any **policy** specifics at gumroad.com before
> launch — Gumroad has changed its fee structure before and this skill does not
> assert a current percentage.

## Why Gumroad for this (vs a processor like Square)

Gumroad is a **merchant of record**: it collects and remits VAT/GST/sales tax
on your behalf across jurisdictions, and handles digital delivery, license
keys, and refunds. A raw payment processor (Square, Stripe) makes *you* the
seller of record — you'd owe the global tax compliance yourself. For a
sub-$30 download sold worldwide, MoR is the whole point. Keep Square for
in-person and service work; use Gumroad for the download.

## Setting up the ReaPack GitHub repo (for script delivery)

Before you can give buyers a ReaPack URL, you need a GitHub repo with an `index.xml`. This is the infrastructure step between "scripts exist on your desktop" and "buyers install via Extensions > ReaPack > Import."

### Step-by-step

1. **Create the repo directory** alongside your existing scripts:
   ```bash
   mkdir my-scripts-repo
   cd my-scripts-repo
   ```

2. **Copy your .lua files** to the repo root (ReaPack expects them relative to `index.xml`).

3. **Create `index.xml`** — the ReaPack manifest. Use `<source>` with full raw.githubusercontent.com URLs, NOT `<files><file>` (the relative format silently fails on GitHub's CDN):

   ```xml
   <?xml version="1.0" encoding="utf-8"?>
   <index version="1" name="Your Name - Script Bundle Name">
     <description>One-line description of what the bundle does.</description>
     <website>https://github.com/yourusername/your-repo</website>
     <license>MIT</license>

     <category name="YourCategory">
       <reapack name="YourScriptName" type="script"
                desc="Description for ReaPack browser">
         <version name="1.0.0" author="Your Name"
                  time="2026-01-15T12:00:00Z">
           <changelog><![CDATA[+ Initial release]]></changelog>
           <source main="main">
             https://raw.githubusercontent.com/yourusername/your-repo/main/your_script.lua
           </source>
         </version>
       </reapack>
     </category>
   </index>
   ```

   **Requirements**: one `<category>` per functional area, one `<reapack>` block per script, `<version>` tags with `time` (ISO 8601 datetime) and `author` attribute. Single-line `-- @provides [main] script_name.lua` header in each .lua file (multi-line format silently fails). See the `reapack-publishing` skill for full index.xml details.

4. **Create `.gitignore`**:
   ```
   .DS_Store
   Thumbs.db
   *.swp
   ```

5. **Init git and push**:
   ```bash
   git init
   git add -A
   git commit -m "Initial release: description"
   git remote add origin https://github.com/yourusername/your-repo.git
   git branch -M main
   git push -u origin main
   ```

6. **The ReaPack URL** becomes:
   ```
   https://raw.githubusercontent.com/yourusername/your-repo/main/index.xml
   ```

7. **Test it**: Open REAPER → Extensions → ReaPack → Import repositories → paste the URL. Search for your script in Browse packages. Install. The script should appear in the Actions list.

### index.xml gotchas

- **Use `<source>` not `<files>`** — the `<files><file>` relative format silently fails on GitHub's raw CDN. Scripts appear imported but nothing shows in Browse packages. Always use `<source>` with full raw.githubusercontent.com URLs.
- **`@provides` must be single-line** — `-- @provides [main] script.lua`, not multi-line with indented continuation. ReaPack silently ignores the multi-line format.
- **Version field matters** — ReaPack only updates when the `<version>` tag changes or `time` advances. Bump both on every release.
- **Category names** are what users see in Browse Packages. Use descriptive nouns: "Track", "Editing", "Tempo", "Import" — not abbreviations.
- **Raw GitHub URL** (raw.githubusercontent.com/.../main/index.xml) is the canonical ReaPack endpoint. The regular GitHub.com URL will NOT work.
- **Test from a clean REAPER** (portable install or temp config) before telling buyers it works.

### Updates

When you push a new script version:
1. Bump `@version` in the .lua file header
2. Update the `<version>` tag and `time` in index.xml
3. Update `@changelog` in the .lua file
4. `git commit -am "v1.0.1: fix X" && git push`
5. ReaPack users see "1 update available" next time they run Synchronize Packages

## Delivery model for a ReaPack bundle

Don't just dump `.lua` files. Deliver, in this priority:

1. **Primary: the ReaPack repo import URL** (your GitHub
   `.../raw/main/index.xml`). Buyer pastes it into Extensions > ReaPack >
   Import a repository → installs + **auto-updates forever**. This is the
   product's stickiness and your update channel.
2. **Fallback: a versioned `.zip`** of the `.lua` files for buyers who won't
   touch ReaPack. Gumroad lets you attach files AND post-purchase "content"
   (rich text / links) — put the URL + install GIF in the content, the zip as
   the file.
3. **A one-page install README** (the #1 refund-preventer): how to add the
   repo, the ReaImGui dependency note, "build peaks first" for the DSP scripts.

## Two distribution models

### Paid (private repo)

Scripts are sold for a price. The ReaPack repo is **private** — only buyers
with a valid Gumroad license key get the URL. See "License keys" below.

### Free + donation (public repo)

Scripts are free and open source via a **public** GitHub repo + public ReaPack.
Gumroad is optional — a "buy me a coffee" / donation link for users who want
to support development. The ReaPack URL is published in the README and INSTALL
docs, not gated behind a license key.

**Why choose this:** No friction for adoption, no support burden from gated
access, builds goodwill and reputation. Works well when:
- The scripts are a side effect of your real product (e.g., your VST plugins)
- The scripts are a lead magnet for your brand
- You want to build a user base before introducing a paid Pro version
- The user community for your niche is hostile to paid tools

**Setup for free/public:**

1. Create a GitHub repo (personal or org) with the scripts + index.xml
2. The ReaPack URL is the raw GitHub URL:
   ```
   https://raw.githubusercontent.com/your-org/your-repo/main/index.xml
   ```
3. Publish the URL in your README/INSTALL docs so users paste it into REAPER
4. Optionally create a Gumroad product priced at $0+ (pay what you want) or
   a fixed "donation" tier — attach a zip of the scripts as the file, and
   put the ReaPack URL in the post-purchase content so buyers who pay get
   the same install experience as free users
5. If using an **org repo** (e.g., `YourBrand/your-repo`), update ALL docs
   — README.md, INSTALL.md, index.xml `<website>` tag — to use the org URL,
   not your personal username

**Gotchas:**
- **No license keys needed** for public repos — anyone can clone the repo
- **Org vs personal:** if you start with a personal repo then move to an org,
  the old ReaPack URL stops working for existing users. Choose early.
- **README/INSTALL consistency:** after changing URLs, grep for stale
  references to the old personal username across all .md files and index.xml
- **First push forces a branch decision:** GitHub's default is `main`; the
  raw URL uses `main` in the path. If your local branch is `master`, rename:
  `git branch -M main` before push
- **ReaPack caches the index.xml** — users need to run Synchronize Packages
  to pick up changes after you push updates

## License keys (gate the repo URL)

Toggle **"Generate a unique license key per sale"** on the product. Each buyer
gets a key. You can verify keys programmatically:

```
POST https://api.gumroad.com/v2/licenses/verify
  product_id   = <your product id>
  license_key  = <the buyer's key>
  increment_uses_count = false
```

Returns the sale record + a `uses` count if valid. For a ReaScript bundle you
generally don't need runtime key-checking inside Lua (it's source-visible
anyway — see the licensing skill), but the key gives you: proof of purchase for
support, a way to revoke/track, and an optional "enter your key to reveal the
repo URL" step if you build a tiny gate.

## Listing setup checklist

- **Product type:** digital product, one-time (not subscription)
- **Price:** set the number; consider a **first-week launch discount code**
- **Updates:** when you push a new version, update the attached file. ReaPack repo auto-updates.
- **Page copy:** lead with the outcome, one demo GIF/video, dependency + DAW requirements, trust line
- **Refund policy:** state it plainly; MoR means Gumroad processes refunds

## Selling Hermes Agent skills

This skill covers Gumroad mechanics generally. For the specific workflow of
packaging and publishing Hermes SKILL.md files — GitHub tap repos, Skills Hub
publishing, three-tier product strategy, and audit/curation — see the
`hermes-skill-publishing` skill.

## Pre-launch gotchas

- **ReaImGui dependency must be obvious on the page**, or buyers hit a wall and refund
- **Test the repo URL from a clean REAPER install** before listing
- **Tax/VAT is handled** — don't add your own tax line; Gumroad does it at checkout
