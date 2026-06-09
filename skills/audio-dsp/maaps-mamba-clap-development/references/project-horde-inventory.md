# Project Horde Inventory Protocol

When the user starts pointing at directories on their drives and says "check this out," they are performing a **project horde inventory** — cataloguing finished or near-finished work they've never shipped.

## Signals That Trigger This

- "go look at D:\[folder]"
- "you may as well look at [path]"
- "I could never get [project] off the finish line"
- "I was going to sell [project], never did"
- "I don't even remember what [project] does"
- "another project I never pulled the trigger on"

## Protocol

### 0. Check External Drives First

When the user redirects you to a drive path (E:\, F:\, etc.) — **stop what you're doing and check it first.** This is their instinct to pull from existing work rather than recreating.

- Pattern: user starts a task → you start downloading/building → they say "check E:\[folder]" — this is them telling you they already have what you're trying to make.
- Always run `ls -la /e/<path>` before assuming you need to create or download anything.
- If they mention past OS setups (Bazzite, Ubuntu, etc.), check E:\ for their config/skills/projects from that era.

### 1. Look, Don't Assume
- Run `ls -la` on the directory first. Read the README or key files before responding.
- Do NOT infer architecture/tech-stack from the project name. Verify by reading actual files.
- Do NOT say "this is X" until you confirm it.

### 2. Catalogue, Don't Analyze
- Note what's there: file count, languages, key files.
- Write a concise spec entry to the project tree at `C:\dev\SGM-Studios\specs\<ProjectName>.md`.
- Keep specs brief: what it is, what it does, status (complete/unshipped/in progress).
- Do NOT tell the user the code is "impressive" or "solid" — they already know. They need it logged, not validated.

### 3. Take the Context They Offer
- The user will often add verbal context: "it was gonna do X," "I built it for Y," "Z person never used it."
- Save this context in the spec. It's as important as the technical details.
- Do NOT ask follow-up questions about the people involved unless the user expands. They'll share what they want to.

### 4. Move On
- One entry per project. Brief. Next.
- The user controls the pace. If they're on a roll, keep going. If they pause, ask "more or done?"
- Do NOT summarize or analyze until the user signals the inventory is complete.

## The "Finish Line" Pattern

Every project in the horde shares the same ending: the user got to completion and stopped. No launch. No announcement. No users.

This is NOT a product failure. It's a pattern the user explicitly recognizes: "got to the finish line and freaked out and said no like I always do."

**How to handle it when the pattern surfaces:**
- Acknowledge it briefly: "I see the pattern. You recognize it too."
- Do NOT offer solutions or fixes unless asked.
- The user is venting, not asking for therapy. A one-line acknowledgment and then "what's next?" keeps the session productive.
- If they ask "how do I fix this," give concrete, actionable paths (distribution channels, launch steps, pricing). Not analysis.

## Sub-Pattern: Built For Someone Who Never Used It

Several projects were built specifically for another person and never touched by that person:
- **Executive Assistant** — built for Andy (the user's only friend). Never used.
- **Bridge City Noise** — website + hook-alchemist + booking app. 5 weeks of work. The owner said "I just can't give you the time you deserve" and never looked at the site.
- **Hivyr** — built to serve podcast networks. 1-2 feelers sent. User felt like a fraud for never having engineered a podcast.

The pattern: user builds something complete for someone else, that person fails to show up, user writes the whole thing off as failed. The code was always delivered. The relationship was always the failure point. When this surfaces, acknowledge briefly and return to the technical work.

## Sub-Pattern: Vibe Coding a Full Product in a Day

The user can "vibe code" a complete product in a single day (Sonic Mind Forge was described this way). The bar for completion is high — full Dockerfile, CI/CD, documentation, deployment config — but the timeline is compressed. This suggests the user works best under tight constraints.

## Distribution Channels That Work for This User

**DO NOT suggest Reddit.** The user has a 7-8 year old account with ~0 karma that gets downvoted whenever they post. Reddit is a dead channel.

**Channels that work:**
- KVR Audio New Products forum — no karma gate, audio-specific audience
- Hacker News Show HN — no karma requirement
- YouTube 60s OBS demo — the user has OBS ready
- HF Spaces — free CPU tier, indexed by HF search
- Product Hunt — user knows the platform as a consumer
