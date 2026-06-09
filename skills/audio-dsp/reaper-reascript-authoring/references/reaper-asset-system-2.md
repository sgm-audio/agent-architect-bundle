# REAPER Asset System 2 — Advanced Prompt Engineering for REAPER Assets

Source: `E:\Reaper Prompting Systems\Reaper Asset System 2` — Added to RAG Jun 2026.

## Overview

Advanced layer on top of Asset System 1. Focuses on engineering intent, constraints, and iterative refinement. This system treats the AI as an audio engineer you're directing, not a magic box.

## Process Pipeline

### Step 1: Define the Target (Tier 1)
- **Genre:** Specific sub-genre (not just "rock" — "alt-rock with modern metal production, 2015+")
- **Reference Tracks:** 2-3 with specific aspects to emulate
- **Role in Mix:** Lead/backing/accent — this determines the entire processing philosophy
- **Delivery Format:** What format will this be loaded in? (REAPER FX Chain `.RfxChain`, Track Template `.RTrackTemplate`, etc.)

### Step 2: Constraint Injection (Tier 2)
- "Use only stock REAPER plugins" vs "Use only ValhallaDSP + FabFilter"
- "No parallel processing" vs "NY bus compression is mandatory"
- "Zero latency monitoring" vs "Maximum quality, latency irrelevant"
- "CPU budget: 5% per instance" vs "Use whatever it takes"

### Step 3: Implementation Request (Tier 3)
- "Generate the FX chain signal flow"
- "For each plugin, provide exact settings"
- "Include gain staging between each stage"
- "Note which parameters should be automated"

### Step 4: Validation & Revision (Tier 4)
- "Verify this chain against known phase issues"
- "Alternative: what changes if we swap ReaComp for a FET-style comp?"
- "Simplify: reduce to 3 essential plugins — what's the minimal viable signal path?"

## Signal Flow Template

```
INPUT → [HPF @ X Hz] → [Stage 1: Tonal] → [Stage 2: Dynamic] → [Stage 3: Spatial] → [Stage 4: Saturation] → OUTPUT
                              ↓                    ↓                    ↓                    ↓
                         Plugin A             Plugin B             Plugin C             Plugin D
                         Param 1: X           Param 1: Y           Param 1: Z           Param 1: W
                         Param 2: X           Param 2: Y           Param 2: Z
```

## Mix Bus vs Individual Track

### Mix Bus Philosophy
- Minimal processing — catch the 2-bus is about glue, not fixing
- Start with nothing, add only what's necessary
- Reference before and after at matched gain

### Individual Track Philosophy
- Process for role in the arrangement
- Remove before you add (HPF, subtractive EQ first)
- Dynamic control after tonal shaping
- Spatial effects last (or on send)
