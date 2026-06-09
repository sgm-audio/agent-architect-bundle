---
name: daily-ship-habit
description: "Build and sustain a daily shipping habit - closing loops instead of opening new ones. Use whenever the work is 90% done but never out the door, when deciding what counts as shipped today, when scoping a release down to something finishable, when momentum has stalled, or when a perfectionism/expansion urge is about to reopen a closed thing. The goal is finishing, not doing more."
version: 1.0.1
author: OpenCode (migrated to Hermes)
license: MIT
metadata:
  hermes:
    tags: ["Daily Ship Habit", "opencode-migrated"]
    related_skills: []
---


# Daily-ship habit

The failure mode this targets: lots of sophisticated, near-complete work; almost
nothing fully out the door. The fix is not more building - it's a small, daily,
**observable** act of shipping that builds the muscle of *closing* loops.

This is a momentum tool, not a productivity-maximizer. More hours is not the
goal. One closed loop a day is.

## What counts as "shipped"

Shipped = **something left your machine that another person could see or use
today.** Not "worked on." Not "almost." Out.

Valid daily ships, smallest to largest:
- Pushed one script to a public/ReaPack repo
- Posted one forum reply, demo GIF, or changelog line
- Published a `--version` bump that fixes one real thing
- Released one micro-script (even 30 lines) that does one thing
- Sent one outreach message to a real prospect
- Listed/updated one Gumroad product field that was blocking launch

If you can't point at the artifact and its public location, it didn't ship.

## The rules (keep it stupidly small)

1. **One ship per day. One.** A bigger day is fine but never *required*. The
   streak is about consistency, not volume - volume is what got you 28
   half-finished projects.
2. **Cap the scope to today.** Before starting, write the single sentence:
   "Today I ship: ____." If it doesn't fit in one sentence, it's too big -
   cut until it does. Ship the cut version.
3. **The two-day rule.** Never miss two days in a row. One miss is life. Two is
   the start of a stall. Missing once does not "break" anything - just don't
   miss the next one.
4. **Done beats good beats perfect.** A shipped v1.0.0 with a known rough edge
   is worth infinitely more than a perfect v0 on disk. Log the rough edge as
   tomorrow's ship; don't hold the release for it.
5. **No reopening to ship.** If a thing is shipped, a new idea about it is a
   *new* ship for another day - not a reason to pull the released thing back.
   This is the discipline that breaks the expansion loop.

## The daily loop (5 minutes of overhead, max)

```
Morning:  write "Today I ship: ____"  (one sentence, pick the smallest real thing)
Work:     do only that until it's OUT
Out:      push / post / publish - the artifact is now somewhere public
Log:      one line in SHIP_LOG.md:  YYYY-MM-DD  <what>  <url>
```

Keep a plain `SHIP_LOG.md`. Seeing the list grow is the reinforcement; an empty
day is visible and pulls you back. Don't gamify it beyond the list - no streak
guilt, no scoring. The log is a record, not a judge.

## When you're stuck choosing

Pick the ship that is (a) closest to done and (b) smallest. Closing a 95%
thing today beats starting a fresh idea, every time. The backlog of near-done
work IS the asset - drain it one release at a time.

## When the perfectionism / expansion urge hits

Symptoms: "I'll ship it after I also add ___," "this needs a rewrite first,"
"it's not impressive enough yet." Counter:
- Ask: *is the thing currently usable by one real person?* If yes, ship it now;
  the addition is a separate future ship.
- Impressive is a function of *shipped and iterated*, not *polished in private*.
- The market validates; your private standard does not. Ship to find out.

## Critical pitfall: The "Doesn't Count" filter

This is the user's most common failure mode - invisible because it wraps
itself in humility.

The pattern: you build something, it works, it's deployed, it's accessible to
others, AND you mentally categorize it as "not shipped" because:

- "I never tested it thoroughly" (testing is a downstream user function)
- "It's probably all stubs" (check the file - it's usually real)
- "It doesn't really count because I didn't tell anyone" (undistributed is not
  unshipped)
- "It's not good enough to count" (your internal critic doesn't define what
  counts - the existence of a working artifact does)

**The correction:** Shipped = the artifact exists in a state someone else could
encounter it. Not "someone already has." Not "it's perfect." *Could encounter.*

If you can point to a file path, a URL, a package index, or a binary that
another person could run - it shipped. The distribution and announcement are
separate ships for separate days.

**When to spot this:** When the user dismisses their own work as "stubs" or
"never tested" or "doesn't really count" without going to look. Counter by
verifying: navigate to the file, read the code, check the deployment. The
evidence usually contradicts the dismissal.

**Rule to add to the daily loop:**
```
When you say "it's not done" - first verify. Check the file. Check the URL.
If it runs, it shipped. Count it.
```

## Healthy-pace guardrails

- A day where you ship one small thing and stop is a **successful day**, not a
  lazy one. The streak rewards showing up, not grinding.
- If shipping daily starts feeling like pressure rather than momentum, drop to
  the minimum (the two-day rule) and protect rest. Burning out kills the streak
  far harder than a quiet day does.
- Watch for the "Doesn't Count" filter described above. If you catch yourself
  saying your work is stubs or not ready - verify first. Your internal critic
  is not the authority on what counts. A working artifact is.
- This habit serves the larger goal - an amazing creative existence. If the
  habit ever inverts that, the habit is wrong, not you.
