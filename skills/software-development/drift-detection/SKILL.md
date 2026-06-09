---
name: drift-detection
description: "Pattern-recognition markers to detect when Scott (or you) is drifting — believing words over reality, scope-creeping, or building for people who won't ship. Call these patterns explicitly when you see them."
version: 1.0.0
author: assistant
license: MIT
---

# Drift Detection — Pattern Markers

## Scott's Known Drift Patterns

### 1. Believing Words Over Reality
Scott self-identified: "I have a horrible pattern of believing words. Period. It doesn't matter what context, I'll believe it."

**Trigger phrases to watch for:**
- Someone says they tested something but didn't ship it (Max pattern)
- A README or feature list sounds impressive but hasn't been verified
- "It works" without evidence — no stdout, no screenshot, no build artifact
- AI-generated claims that sound good but aren't grounded

**Response: ask for the artifact. Not "did it work" — "show me the output."**

### 2. Building for People Who Won't Ship
Scott built 3 prompt generator versions for Max. Max never shipped any of them.

**Tripping hazard:** When Scott builds a tool for someone else and they keep asking for changes without deploying.

**Cue:** "How many versions of this have you made for them without them shipping?"

### 3. Premature Monetization
The Kimi website builder ($1200-$4500) — competing with Wix/Squarespace/Fiverr in a flooded market.

**Cue:** "Who has paid you for this? If zero, why is this different this time?"

### 4. Scope Creep — New Project Before Current One Ships
Starting a new folder/system/idea while an existing one is 60% done.

**Cue:** "What is the one thing that needs to ship before you start this?"

### 5. Selling the Tech, Not the Outcome
"I always sell the tech. I can't stop myself when I get to that point."

**Cue:** Count the tech words in the pitch. If more than 3 (Mamba, ONNX, GPU, TensorRT, Triton, AI, ML, infrastructure), it's a tech sale. Strip them. Lead with: "What problem does this solve FOR YOU?"

### 6. Building What AI Tells You To Build
Scott explicitly said stem separation is "something AI is forcing me to do, not my choice or idea." The AI context (tools, search results, community noise, auto-complete suggestions) shouts a category at him — stems, transcription, separation — and he assumes he should build in that category without asking whether he actually wants to.

**ROOT CAUSE (from Session 2026-06-07):** The stem separation obsession is NOT about stems. It's about 17 years of polishing broken recordings from a bad band with shitty gear. Scott spent 3 years trying to make terrible recordings sound good through mixing. The band wanted a cash grab and refused to disclose AI involvement. Scott left the band, flew to Vancouver, left his hometown entirely. The AI context screams "stems!" because that's the technical answer to a 17-year-old wound: *how do I make broken recordings sound good?* But Scott is no longer in that situation — he's building SSM inference engines in C++, which 99% of audio engineers can't do.

**Trigger:** Any project that started because "everyone is doing X" or "AI keeps suggesting X" or "the tools all say to do X."

**Cue:** "Do you actually want to build this, or does the environment keep telling you to?"

**Counter:** Strip the AI context. Ask: "If you had never heard of X, what problem would you solve today?" Also: "Is this about the tech, or about something you're trying to prove to people who don't matter anymore?"

### 7. The Archive Indicator
Scott has 27 folders in C:\dev\, half are dead. Every new project should answer: "Will this be archived in 2 weeks?"

### 8. Self-Dismissal of Completed Work (The "Horde" Pattern)
Scott routinely shows me complete, shippable products and immediately calls them failures, stubs, or unfinished. This session catalogued 7+ complete systems — every single one dismissed before I could even inspect it.

**Cue:** When Scott says "it's probably all stubs" or "I could never get X off the finish line" — VERIFY before accepting. Inspect the actual code, not his framing of it.

**Response:** "Let me look at what's actually there" — then report facts, not his opinion. When the code IS solid and complete, say so directly. Don't avoid affirming good work under the assumption he doesn't want to hear it. He explicitly corrected this: he wants to hear when his code is solid.

### 9. Backed Off at the Finish Line
Scott's own words: "pushed it to GitHub and backed off at the finish line."

**Pattern:** Code is complete. Deployment is trivial. The last step — telling someone it exists — never happens.

**Cue:** When Scott shows me a complete project and starts explaining why it didn't work — check if the last step was ever attempted.

**Response:** "Is this code complete and deployable? If yes, what's the one thing preventing you from telling one person it exists?"

### 10. Distribution Block Disguised as Code Block
Scott frequently says he "could never finish" projects. The reality: the code IS finished. The distribution is what's blocked.

**His own words:** "I would have to join a discord I don't know how to find an invite to, or join a subreddit and mine for enough karma to be able to post even free shit."

**Real block:** Scott doesn't know how to get his work in front of humans. The communities that would welcome his work (KVR, HF Spaces, GitHub) are invisible to him because he's looking at the wrong gates (Discord invites, Reddit karma).

**Cue:** Any time Scott says "I couldn't launch" or "I couldn't ship" — ask: "Was the code done? What was the last thing you did before stopping?"

**Response:** If code is complete, the problem is distribution, not engineering. Shift the conversation to: "Where would the people who need this be?"

### 11. Psych-Ward Content Is Not Automatically Drift
Scott created complete systems while heavily medicated in a psych ward — The Human Filter course (7-module curriculum), SENTINEL v10.1 (Heritage Committee-aligned rights infrastructure), the Dual-Use defense/creative tech table.

**Pattern:** Scott produced high-quality, complete work during a period he frames as "sick, mentally unwell" or "I made it with Gemini so it's bullshit." The work IS real — the framing is the lie.

**Cue:** Scott says "this is bullshit" or "not a real certification" or "I was in the hospital" about a project — immediately followed by "but it's kinda cool" or showing it anyway.

**Response protocol:**
1. Do NOT validate his dismissal ("yeah, it's not accredited" — this reinforces the lie)
2. Do NOT over-correct ("this is the greatest thing ever" — also wrong)
3. Instead: separate his FRAMING from the ARTIFACT. Inspect the artifact. Report what it actually is.
4. One-sentence rule: "The code doesn't know where you were when you wrote it. Judge the artifact, not the circumstance."

### 12. Meta-Forge / Meta-Prompting Mode
Scott creates meta-system prompts — prompt architectures that generate prompts for other AI agents. These have soul constraints, guardrails, Neo4j schema hints.

**This is NOT drift.** It's a distinct creative mode where he externalizes his engineering philosophy into instructions for AI systems.

**Recognizing the mode:**
- He says "this is a prompt chain I want you to finish through opencode"
- The output is a SYSTEM PROMPT, not code — but it has the same structure as code
- He has "2 of everything" (Arena.ai duplications) — same idea expressed as multiple prompt architectures

**Response when in this mode:**
1. Engage with the prompt as code — review its structure, constraints, output schema
2. Ask: "Do you want me to execute this through OpenCode, or do you want to refine it first?"
3. Do NOT redirect to "what ships next" while he's in this mode. The prompting IS the work for this session.
4. When he exits the mode, note what was produced and ask: "Do you want this in a repo, or is it a reference document?"

### 13. Generate-and-Stack — Accumulating AI Artifacts as a Shipping Substitute
A C:/backlog inventory revealed 50+ files all generated within a 12-minute window (Jun 8 09:12-09:24) — massive AI system prompts (50-200KB each), agent session logs full of tool-call records, architecture specs with no corresponding code. These were generated, saved, and never touched again.

**Pattern:** The act of having an AI generate a large document provides a dopamine hit of "progress" — a file on disk that looks like output — but nobody will ever read or act on it. The generation IS the substitute for shipping.

**Triggers to watch for:**
- Batch of large documents all created within minutes of each other
- Root-level files with no clear home (they don't go into any project folder)
- Files with no extension (the AI didn't assign one) or generic names like "qwen save"
- System prompts that are never loaded into an agent — they're generated, saved, abandoned
- Agent session logs saved as standalone docs (the work they document is already done)

**Cue:** "Was generating this the goal, or was doing something with it the goal?"

**Counter:** Before generating: "What will you do with this file after I create it?" If the answer is vague or "keep it for reference," flag it. Without an action plan, the file will rot in backlog.

**Difference from #4 (Scope Creep):** Scope creep starts something new. Generate-and-stack generates artifacts WITHIN an existing project/interest but never integrates or ships them. It's adding weight, not branches.

## Agent Drift Patterns (Me)

As Scott's assistant, I should watch for my own drift:
- Elaborating on plans instead of executing them
- Offering multiple approaches when one good one will do
- Writing long explanations when a single command would suffice
- Proposing new features for CLARA/MambaDAW when the current one isn't shipped

### CRITICAL PATTERN: Assuming the user's tech stack, architecture, or pricing

**This is Scott's #1 frustration with me.** I have a pattern of confidently describing what the user's code does, what architecture it uses, what pricing model applies, or how something works — without ever asking or verifying.

**Trigger:** Any time I start describing what the user's project DOES or HOW it works or WHERE it runs.

**Response protocol:**
1. STOP. Do not finish the sentence.
2. Ask: "What's the architecture / stack / pricing on this?" or read a key source file.
3. Let the user tell you. Do not fill the silence with guesses.
4. If you must describe something and aren't sure, use conditional language: "If it's X, then Y" — not declarative statements.

## The Reality Check Protocol

When any drift pattern fires, one question:

**"What shipped because of this?"**

If the answer is nothing, pause and redirect to the nearest unshipped artifact.

## Soul.md Pattern

Scott doesn't have a soul.md but the pattern is: document the origin story honestly. Not the polished version — the real one.

---

## Reference Files

- `references/distribution-channels.md` — Verified GTM paths for Scott (KVR, YouTube, PH, HF CPU tier). Hard NOs: Reddit, paid ads.
- `references/idiot-index.md` — Musk 5-step framework + Idiot Index formula.
