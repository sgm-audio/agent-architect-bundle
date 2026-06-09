# Idiot Index — Elon Musk's Engineering Efficiency Framework

Applied periodically (per Scott's request during Session 2026-06-07). Ask these questions routinely during sessions to help Scott gain efficiency and deliver better products faster.

## The Idiot Index (Cost Question)

**Formula:**
```
Idiot Index = Total cost of a part / Raw material cost
```

If the ratio is high (50:1 or 100:1), you're spending 2% on materials and 98% on manufacturing/assembly — you're an "idiot." Redesign so the part can be made cheaper.

**For software/plugins:** Total development effort / core value delivered. If you're spending 98% of time on stuff users don't care about, stop.

## The 5-Step Engineering Process

### Step 1: Make the requirements less dumb
Question every requirement. Requirements come from people, not physics. Ask WHO wrote it, WHAT actual constraint governs it, WHY it exists.

**Adapted for Scott:** When he says "I have to ship stem separation," ask "Who says? What actual constraint?"

### Step 2: Delete the part/step/process
If you don't end up adding at least 10% back, you didn't delete enough. This is the MOST important step.

**Adapted for Scott:** "What feature/plugin could you delete entirely and lose the least revenue/satisfaction?" If nothing comes to mind, that's the one to delete.

### Step 3: Simplify & optimize
Only AFTER Step 2. Optimizing something you should have deleted is waste.

### Step 4: Accelerate cycle time
Speed up whatever remains. For Scott: what's the bottleneck in his pipeline? ONNX export? CMake build? Training config? Speed that up.

### Step 5: Automate last
Scott already uses cron for morning tasks. Don't automate until the thing is stable.

## When to ask
- When Scott mentions a new feature/plugin idea
- When he's spending time on something that feels like a grind
- When the project list is growing faster than the shipping list
- Any time he says "I need to build X" — ask Step 1 first

## Scott-specific trident (current focus)
| Project | Idiot Index Question |
|---|---|
| CLARA | What's the ratio of inference complexity to perceived quality? |
| EMT (~40%) | What could you delete before finishing? |
| Stem Surgeon (60%) | Is this about stems or about proving something? |
| Stem+MIDI Pro | Has anyone paid for this? If not, why is it active? |

## Meta-pattern: The Horde Idiot Index

After Session 2026-06-07, Scott acknowledged a pattern: "a horde of finished unshipped code." 7+ complete systems exist on his drives, all never distributed.

**The real Idiot Index for Scott:**
```
Total development time across all projects / Total users who have touched any of them
```

If the denominator is 0 (or close to it), the index is infinite. That's the real idiot — not in the code, but in never letting anyone see it.

**The one question to ask before any new project:**
"Is this going to join the horde, or are you going to tell someone it exists?"

**When to apply:**
- When Scott mentions a new project idea
- When he shows me a complete project and calls it a failure
- When the conversation drifts to "what's next" instead of "what exists"
