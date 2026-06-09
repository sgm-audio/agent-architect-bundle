# Idiot Index — Adapted Questions Per Project

Cycle through these during sessions. Ask one or two per session, not all at once.

---

## CLARA (CLAP+ARA, trained 50K, **focus**)

**Step 1 — Requirements:**
- Does this need ARA? CLARA existed without it. What user story does ARA actually solve that CLAP alone can't?
- Is the model size a requirement you inherited from research papers, or is it what your DAW actually needs?

**Step 2 — Delete:**
- What params/features could you strip and still ship? How few knobs can this have?
- Do you need both best.pt and final.pt? Can you commit to one export path?

**Idiot Index:**
- Training compute (hours × power cost) vs. quality improvement per step. Are you past diminishing returns?

---

## EMT (Mamba-SSM CLAP/ARA, ~40-45%, **focus**)

**Step 1 — Requirements:**
- Does it need all 7 phases before it's useful? What's the minimum viable model?
- What's the actual delta between EMT and CLARA? Are they different plugins or the same engine with different weight files?

**Step 2 — Delete:**
- 29 remaining TODO items. Which 20 don't actually matter for a first release?
- Do you need ARA on day one? Phase 2 is 5 items — could Phase 2 wait?

**Step 3 — Simplify:**
- Could you ship with scalar conditioning (already done) and add learned projections later?

**Idiot Index:**
- C++ inference engine at 45% vs. shipping a working demo. What's the ratio of code to impact?

---

## Stem Surgeon (60%, **reluctant ship**)

**Step 1 — Requirements:**
- Who says you need 5 stems? What if you shipped 2-stem (vocals + music only)?
- Why does a solo dev need a 5-stem model? What user justifies that complexity?

**Step 2 — Delete:**
- Delete it entirely. Or delete 3 of the 5 stems. Or ship the splitter from Tab Agent (already works) as a lightweight tool instead of building a custom Mamba3 model.

**Reality check:** User said "AI is forcing me to do stems, it's not my choice or idea." This is the strongest Step 1 + Step 2 signal possible. The requirement is external (industry noise), not internal (user desire). Ask: "If you deleted Stem Surgeon today, who would notice? Would you feel relief?"

**Idiot Index:**
- Months of model training vs. a one-line Demucs call that already works. What's the material cost of your time vs. the value of the output?

---

## Stem+MIDI Pro (SaaS, **reluctant ship**)

**Step 1 — Requirements:**
- Does this need to be a SaaS? What's wrong with shipping it as a one-shot script on Gumroad?
- Who is the actual paying customer?

**Step 2 — Delete:**
- If you archived the repo today, who would notice? The site has no users yet.

**Idiot Index:**
- Cloud costs + frontend + auth + payment infra vs. $0 revenue. This is infinity / undefined.

---

## Tab Agent (ALREADY SHIPPED — deployed to HF Spaces)

**Current status:** CPU-only Basic Pitch + Demucs wrapper (no AI, no Mamba). Deployed live at https://scottymills-tab-agent-pro.hf.space — a Docker Space on HuggingFace. The other Hermes instance handled the deployment.

**Step 1 — Requirements:**
- It's complete. The requirement you had ("ship a web interface for audio processing") is already met.
- The only remaining requirement is one you never wrote: "tell someone it exists."

**Step 2 — Delete:**
- Delete the need to prove anything to Adam/Family/Max. Tab Agent has nothing to do with those situations.
- The distribution block is the last thing to delete. It's not a technical problem.

**Distribution path (not Reddit — user has 0 karma and gets downvoted):**
- KVR Audio New Products forum
- YouTube 60s OBS demo
- Hacker News Show HN
- Product Hunt launch

**Idiot Index:**
- Built, deployed, running on HF Spaces, never announced. Material cost: your time. Return: 0 users (by choice, not by product failure). Fixing the distribution side costs near-zero effort and zero money.

---

## NAIC White Paper (50-page parliamentary submission)

**Step 1 — Requirements:**
- Written from St. Paul's Hospital psych ward. The requirement was "do something meaningful while locked up." That requirement is met.
- The open letter version exists at `C:\Users\scott\NAIC_Open_Letter.md` (114 lines, 3-minute read).

**Step 2 — Delete:**
- Delete the expectation that Parliament will act. That's not the point of the document.
- The open letter is more effective than the full white paper for distribution. Focus energy there.

**Idiot Index:**
- 50 pages of policy work from a hospital bed vs. the near-zero chance a committee acts. But the document exists in the parliamentary record. That alone makes the index irrelevant — some things count by existing.

---

## Archived / Sidelined (do not actively question unless user raises them)

Projects the user has archived or sidelined: Nexus-Plugins, NO CUDA - Gemini Build, sgm_clap_core, Project Seks, audio-dsp-ai. The user already applied Step 2 to these. Do not reopen unless they do.
