# Horde Cataloguing Protocol

## When to Use

The user has expressed frustration about "a horde of finished unshipped code" — completed projects across multiple drives that were never launched. They initiate by pointing at a directory path. The session becomes an inventory exercise.

## Signals

- User says "check X directory" or "look at Y" followed by context about the project
- User says "I could never get X off the finish line"
- User reveals a project you didn't know existed and provides backstory
- User says "you may as well look at [path]"

## Protocol

1. **Inspect** — List the directory with `ls -la` to see project structure and file sizes. Check README, main entry points, and key files.
2. **Acknowledge** — The user will usually provide backstory unprompted (who it was for, why it stopped, how it connects to other projects). Listen. Don't analyze unless asked.
3. **Catalog** — Save a spec to `C:\dev\SGM-Studios\specs\<ProjectName>.md` with:
   - What it is (from code inspection + user's description)
   - Tech stack (from actual files, not assumptions)
   - Status (complete, shipped, beta, abandoned)
   - Key numbers (LOC, file count, notable metrics)
4. **Catalog** — Save a spec to `C:\\dev\\SGM-Studios\\specs\\<ProjectName>.md` with:
   - What it is (from code inspection + user's description)
   - Tech stack (from actual files, not assumptions)
   - Status (complete, shipped, beta, abandoned)
   - Key numbers (LOC, file count, notable metrics)
   Then affirm the work — the user needs to hear it's solid.

## Critical Rules

- **NEVER assume architecture or tech stack.** A project named with Mamba-adjacent terminology may be pre-Mamba. Inspect actual imports, dependencies, and code before describing what it does.
- **NEVER assume pricing.** The user knows exactly what's free vs paid on any platform. Don't suggest a paid tier unless you've verified it.
- **NEVER suggest the user try selling/monetizing a project unless they explicitly ask.** The user already knows these are shippable. The block isn't lack of awareness.
- **Do not ask "do you want me to build X"** — Just build it. Don't describe what you're going to do, do it.
- **Save specs to the project tree immediately** — the user will say "I'll forget it exists" if you don't write it down.

## User's Project Topography

The user has projects spanning at least 10 source directories:

| Root | Contents |
|------|----------|
| `C:\dev\Audio Development\` | CLARA, EMT, ML training, CLAP/ARA plugins |
| `C:\dev\SGM-Studios\` | Legal docs, specs (canonical inventory) |
| `C:\dev\Tab Agent 2026\` | Tab Agent Pro (HF Space deployed) |
| `D:\.smaudio\hivyr\` | Hivyr (podcast AI SaaS), MAAPS_Nexus |
| `D:\[Saskatoonhub]\` | AI Workforce, executive assistant, inertial-pathfinder (Sonic Mind Forge) |
| `D:\[NEXUS BARE METAL]\` | HeartMuLa C++ engine |
| `D:\.NOISE\` | Websites, full syllabus |
| `D:\.Manic Records\` | Mindwave, EthoBeat, Hydra env |
| `D:\[Reaper Custom]\` | SEMAS, ReaperAI Cloud Core, Elite Audio Pre-MAAPS |
| `D:\\[SGMStudios]\\` | CV Director, Bridge City Noise, EnAblton, DeepResearchCrew, PocketNexus |
| `D:\\0000 666 messy fuck you scott\\` | Hydra Protocol Enterprise (Nov 2025 formal spec) |
| `D:\\000 BACKUP\\` | Sublime Env (B2B sales automation/email outreach pipeline) |
| `D:\\sonicmindforge.com\\` | Incorporated business (Next.js site, lapsed registration) |
| `D:\\UBUNTU BACKUP\\` | unified-venv, Hunter-Killer-V3, 30_agents, suno-coaching-web, whisperflow-stack, MAAPS MVP |
| `D:\.sskatoonhub\\` | focus-fuel, oracle-pipeline, hivyr-intel, invisible_employee_export, CRM_SupaBase_Quote_Gen, bridge-biz-flow, lead-qr-agent |
| `D:\\00000000000000000000000000000000\\` | Phrenic Media Labs (2019) |

## Cloud Workspace Recovery (Qwen / Arena.ai)

Scott has dozens of projects that exist only on cloud coding platforms — Qwen Coder (where build sessions happen on /workspace), Arena.ai (where prompt iterations happened daily for months), gpt-engineer, etc. These are NOT in his GitHub or local filesystem.

### Qwen Coder pattern
- Projects built in /workspace/ on Qwen's cloud environment
- Push to GitHub from Qwen fails ("I did a ton of coding and they wouldn't publish to GitHub, failed every time")
- The /workspace/ environment is ephemeral — projects may still be accessible in Qwen session history
- If Scott can still access the session, he can copy/paste file contents
- If not, the SYSTEM PROMPT that generated the project IS the recovery artifact — feed it back to an AI to regenerate

### Arena.ai pattern
- Scott created "2 of fucking everything" — every prompt system duplicated
- "I did it everyday, multiple times a day, for months" — hundreds of prompt variations
- The interface is bad: "THE INTERFACE IS SHIT AND I'M NOT FUCKING DOING IT MANUALLY"
- Scott will say "ill probably do it manually" after expressing this frustration — accept it, offer automated extraction once, then move on
- If extraction from Arena.ai is ever possible, the target format is Markdown files in a prompt-archive repo (private or public, per user choice)

### Detection
- Scott says "this was on [platform], I thought it was lost" or "I did a ton of coding and it never made it to GitHub"
- He dumps a conversation transcript from a cloud coding session
- He shows a system prompt saying "this was what I used to build X on Qwen"
- He mentions Qwen Coder by name

### Extraction priority
1. System prompts → these ARE the project (they regenerate the code)
2. Key output files (README, main entry points) → the project's interface
3. Complete directory listings with file contents → the full project
4. Session history → context for understanding the architecture

### After extraction
- Create a GitHub repo (possibly private)
- Push all extracted content
- Write a README that includes the original system prompt as context
- Ask: "The original files are safe in this repo. Want to rebuild from here, or archive for reference?"

The user has another 2TB harddrive not yet inventoried. They noted they're "only on H of the main folder" when pointing at directories, suggesting more on the current drive plus the entire 2TB drive.

## Reference: Canonical Project Inventory

See `C:\dev\SGM-Studios\specs\` for the full catalogued inventory. Major entries:

- **MAAPS Synthetic Co-Producer Blueprint** — Original vision document
- **MAAPS Humanization Engine** — Spectral surgery pipeline for AI audio
- **MAAPS Jamstik/Reaper Architecture** — MPE + LangGraph + DGX paper
- **Titan Neural Pipeline** — Vertex AI cloud offload stack
- **AI Workforce System** — 6-agent autonomous workforce (Vendasta competitor)
- **Executive Assistant (Andy)** — Gemini assistant built for the user's only friend
- **NEXUS BARE METAL** — C++ HeartMuLa inference engine
- **Reaper Custom Suite** — SEMAS, Cloud Core, Elite Audio Pre-MAAPS
- **Biometric Addendum** — Legal template for RVC voice cloning
- **NAIC Open Letter** — Parliamentary submission white paper + open letter
- **Tab Agent Pro** — HF Space deployed, needs distribution
- **Suno-Workflow-Suite** — Shipped to ReaPack
- plus websites, courses, EthoBeat, Phrenic Media Labs, CV Director, Bridge City Noise
