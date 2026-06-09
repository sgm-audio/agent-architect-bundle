---
name: gumroad-digital-product
description: Package, price, and ship a digital product on Gumroad — license keys, merchant-of-record tax handling, content/file delivery, and update delivery. Use whenever setting up or refining a Gumroad listing for software/scripts/downloads, deciding how to gate access to a paid ReaPack repo, generating or verifying license keys, or writing the product page copy. Especially use it when turning a finished tool into a paid release.
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

## Delivery model for a ReaPack bundle

Don't just dump `.lua` files. Deliver, in this priority:

1. **Primary: the private ReaPack repo import URL** (your own GitHub
   `.../raw/master/index.xml`). Buyer pastes it into Extensions > ReaPack >
   Import a repository → installs + **auto-updates forever**. This is the
   product's stickiness and your update channel.
2. **Fallback: a versioned `.zip`** of the `.lua` files for buyers who won't
   touch ReaPack. Gumroad lets you attach files AND post-purchase "content"
   (rich text / links) — put the URL + install GIF in the content, the zip as
   the file.
3. **A one-page install README** (the #1 refund-preventer): how to add the
   repo, the ReaImGui dependency note, "build peaks first" for the DSP scripts.

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

## Pre-launch gotchas

- **ReaImGui dependency must be obvious on the page**, or buyers hit a wall and refund
- **Test the repo URL from a clean REAPER install** before listing
- **Tax/VAT is handled** — don't add your own tax line; Gumroad does it at checkout
