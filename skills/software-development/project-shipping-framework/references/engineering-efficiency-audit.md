# Engineering Efficiency Audit (Musk's Idiot Index)

## Why This Exists

Part of the Project Shipping Framework. Before you decide what to ship, you need to know which parts are worth shipping at all. This diagnostic tool catches the pattern where you're spending 98% on complexity and 2% on actual value.

## The Idiot Index

```
Idiot Index = Total cost of a part / Raw material cost
```

For a solo audio plugin dev, "cost" means **engineering time + compute cost + complexity**:

```
Idiot Index ≈ Total engineering effort / Core value-producing effort
```

**Thresholds:**
- `< 5`: Good. You're spending proportionally.
- `5–10`: Warning. There's probably a simpler way.
- `10–50`: Problem. Part needs redesign.
- `> 50`: You're an idiot. Rethink from scratch.

### Plugin-specific examples

| Item | Total Dev Time | Core ALGORITHM Time | Index | Verdict |
|------|---------------|---------------------|-------|---------|
| Custom FFT implementation | 2 weeks | 3 days | 3:1 | Worth it (core DSP) |
| Model training pipeline | 4 weeks | 2 weeks | 2:1 | Good (core tech) |
| Button painting / UI | 3 days | 2 hours | 12:1 | Find existing UI lib |
| Installer/updater | 1 week | 0 | ∞ | Use CMake CPack/Inno Setup |
| DAW-specific workaround | 3 days | 0 | ∞ | Ask if that DAW matters at all |

## The 5-Step Engineering Process

Apply to every feature, plugin, or pipeline before writing code.

### Step 1: Make Requirements Less Dumb

**The question:** "Says who?"

Every requirement came from a person — not physics, not the market, not god.

- "It needs a resizable UI" — says who? Can it ship with a fixed 600x400?
- "Must support VST3, AU, AAX" — says who? Does your target user (Reaper/CLAP) need all three?
- "GPU acceleration for inference" — says who? Would int8 quantized CPU inference pass an ABX test?
- "Supports all sample rates" — says who? Can you document 44.1/48 and defer the rest?

**For Scott specifically:** When Max or anyone says "we need feature X," ask "has anyone actually run the code?" Believing words over artifacts is the #1 drift pattern.

### Step 2: Delete the Part/Step/Process

**The test:** If you don't end up adding back at least 10% of what you deleted, you didn't delete enough.

Concrete deletions for MAAPS suite:

- **CLARA:** Delete the spectrogram visualization. Ship with just a bypass + mix knob. Add vis in v1.1.
- **MambaDAW:** Delete VST3 support. Ship CLAP-only. Add VST3 if users ask.
- **Stem Surgeon:** Delete stem #5. User studies show 4-stem covers 95% of use cases.
- **Stem+MIDI Pro:** Delete any "AI" description from the landing page. Sell the outcome, not the tech.
- **All plugins:** Delete the custom license/activation system. Use Gumroad's built-in license keys or ReaPack's free model.

### Step 3: Simplify and Optimize

Only after Step 2. Never optimize something you should have deleted.

- After deleting the spectrogram vis: now optimize the FFT pipeline that's left.
- After deleting VST3: optimize the CLAP path — fewer code paths, less to test.
- After deleting features: INT8 quantization instead of FP16. Fewer parameters. Shorter context window.

### Step 4: Accelerate Cycle Time

Speed up what remains after deletion and simplification.

- Can training go from 50K steps to 20K steps with comparable quality?
- Can you incremental build instead of full rebuild? Use ccache/sccache?
- Can the cron pipeline run every day instead of once to catch regressions?

### Step 5: Automate Last

Never automate what you haven't simplified.

- **Good:** Automate ONNX export after the export script is simplified and tested.
- **Bad:** Automate plugin packaging before you've decided what goes in the zip.
- **Worse:** Automate training before you've established whether 20K steps is enough.

## Quick Audit Protocol (5 min)

Run this on any feature or project before committing dev time:

```
1. Ratio check: total_effort / core_value_effort = ?
   If > 10, delete first.

2. Requirement challenge: pick one requirement and ask "says who?"
   If no external constraint justifies it, drop it.

3. Delete test: what's the Single Thing to remove?
   If nothing comes to mind, delete something random and see if anyone notices.

4. Ship or polish?: does this move the product to a user's hands?
   If no, stop. Do something that does.
```

## Integration with Drift Detection

| Drift Pattern | Idiot Index Cue |
|---------------|-----------------|
| Building for people who won't ship | Index on their feature requests: what's the ratio of their requests to their shipped products? |
| Premature monetization | Index on the monetization infrastructure vs. the product itself. If DRM/licensing takes more code than the DSP, wrong priorities. |
| Scope creep (new project) | Run the 5-min audit on the new idea before starting. Most ideas fail Step 2 (Delete). |
| Selling the tech, not the outcome | The tech stack IS the idiot index everything-else. Strip it. |
