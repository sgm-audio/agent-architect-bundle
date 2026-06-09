---
name: reascript-licensing
description: Choose and apply the right license for REAPER ReaScripts — free scripts submitted to ReaTeam, paid proprietary bundles sold on Gumroad, and handling the ReaImGui LGPLv3 dependency without violating it. Use whenever deciding what license to put on a script, writing a EULA for a paid script bundle, worrying about whether a dependency forces you open-source, or preparing a release for distribution.
---

# Licensing REAPER ReaScripts

**Not legal advice.** This is the practical landscape for a solo dev shipping
Lua scripts; for anything high-stakes, consult an actual lawyer.

## The core fact that shapes everything: Lua ships as source

Your `.lua` is distributed as readable text. There is **no meaningful
obfuscation/compilation moat** — anyone who buys it can read it. So "protecting"
a paid script is **contractual** (EULA forbidding redistribution) plus
**access-gating** (Gumroad + private repo URL), not technical.

## Two tiers, two licenses

### Free tier → ReaTeam/ReaScripts → MIT

Recommended: **MIT**. Least-friction, lets others learn from your code, keeps
your name on it, and — importantly — **lets you reuse your own MIT code in your
paid bundle** (MIT is not copyleft).

Put this at the top (under @metadata) and a `LICENSE` file:
```
MIT License — Copyright (c) 2026 Scott Mills
Permission is hereby granted, free of charge...
```

Avoid GPL for free scripts if you want to reuse that code in a closed paid
product — GPL would force the paid product open too.

### Paid tier → Gumroad bundle → Proprietary EULA

A normal commercial software license: buyer gets a **license to use**, not
ownership and not redistribution rights.

Minimal proprietary EULA:
```
TrackClear Pro — End User License Agreement
Copyright (c) 2026 Scott Mills. All rights reserved.

1. Grant. Non-exclusive, non-transferable license to install and use on
   machines you own or control, for your own music production.
2. Restrictions. You may not redistribute, resell, sublicense, publish, or
   share the scripts or your repository access URL/license key.
3. Ownership. The scripts remain the property of Scott Mills.
4. No warranty. Provided "as is", without warranty of any kind.
5. Termination. Terminates on breach; must stop using and delete scripts.
```

## The ReaImGui dependency — LGPLv3, and why you're fine

- Your Lua **calls ReaImGui's API at runtime** — does not bundle, statically
  link, or modify the LGPL binary.
- LGPL permits proprietary software to use the library through its interface
  if the user can replace/upgrade it. Users install ReaImGui via ReaPack — they
  can replace it freely.
- **Never redistribute the `reaper_imgui` binary inside your package.** Bundling
  is what triggers LGPL obligations; depending on it does not.

Same for SWS and js_ReaScriptAPI — depend, don't bundle.

## Quick decision table

| Situation | License / action |
|---|---|
| Free script → ReaTeam | MIT, `LICENSE` file in repo |
| Paid bundle → Gumroad | Proprietary EULA (`LICENSE.txt` in zip) |
| Reusing your free code in the paid one | Fine — MIT permits it (don't use GPL free) |
| Depends on ReaImGui / SWS | Declare as dependency; never bundle binary |
| Worried LGPL forces you open | It doesn't — runtime API use is permitted |
