---
name: hermes-skill-publishing
description: "Package, publish, and monetize Hermes Agent skills on marketplaces — preparing SKILL.md files, creating GitHub tap repos, publishing to the Skills Hub, and listing on Gumroad. Use when packaging skill collections for sale, setting up a skills registry, or publishing to the Hermes ecosystem."
version: 1.0.0
author: Scott Gilbert Mills
license: MIT
metadata:
  hermes:
    tags: ["Hermes Skills", "Marketplace", "Publishing", "Monetization"]
    related_skills: ["gumroad-digital-product", "github-repo-management", "hermes-agent-skill-authoring"]
---

# Hermes Skill Publishing

Package, publish, and monetize Hermes Agent skills on marketplaces.

## When to Use

- You have a collection of SKILL.md files you want to sell or distribute
- Setting up a `hermes skills tap` repo so others can install your skills
- Publishing to the Skills Hub
- Listing a skill bundle on Gumroad
- Deciding what to charge and how to structure product tiers

## The Three-Tier Strategy

| Tier | Channel | Price | Purpose |
|------|---------|-------|---------|
| **Free tap** | GitHub repo + `hermes skills tap add` | Free | Awareness, community, updates |
| **Complete bundle** | Gumroad (all skills in .zip) | $39-49 | Income, convenience download |
| **Niche packs** | Gumroad (by category) | $15-19 each | Lower-friction entry point |

## Step 1: Audit and Curate

Before packaging, inspect your skills collection:

```bash
# Count and list by category
ls ~/.hermes/skills/*/*/SKILL.md | wc -l
ls -d ~/.hermes/skills/*/*/

# Find skills that need cleanup
hermes skills list
```

Look for:
- **Stale/empty skills** — prune or merge into umbrellas
- **Missing metadata** — each SKILL.md should have tags, description, version
- **Overlap** — consolidate narrow skills into class-level umbrellas
- **User-specific content** — strip paths, env vars, and credentials that won't work for others

## Step 2: Create the GitHub Tap Repo

Users install from your repo via:

```bash
hermes skills tap add YOUR_USERNAME/YOUR_SKILLS_REPO
hermes skills install <skill-name>
```

### Repo structure

```
hermes-skills/
├── README.md              # Overview + install instructions
├── CHANGELOG.md
├── audio-dsp/
│   ├── mamba3-dsp-methodology/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── plugin-ci-cd/
│   │   └── SKILL.md
│   └── ...
├── software-development/
│   ├── frontend-build/
│   │   └── SKILL.md
│   └── ...
└── ...
```

### Requirements

- Must mirror the Hermes skill directory structure: `<category>/<skill-name>/SKILL.md`
- GitHub repo must be **public** for `hermes skills tap add` to work
- Master branch (`main`) is the default source

### README template

```markdown
# Hermes Skills by [Your Name]

[tagline]

## Install

\`\`\`bash
hermes skills tap add YOUR_USERNAME/hermes-skills
hermes skills install <skill-name>
\`\`\`

## Available Skills

| Category | Skills | Count |
|----------|--------|-------|
| Audio DSP | mamba3, JUCE, CLAP, ARA, plugin CI/CD, ... | 28 |
| Frontend | Next.js, Tailwind, shadcn/ui, deployment, ... | 10 |
| ... | ... | ... |

## License

All skills are MIT unless otherwise noted.
```

### Push the repo

```bash
git init
git add -A
git commit -m "Initial release: X skills across Y categories"
git remote add origin https://github.com/YOUR_USERNAME/hermes-skills.git
git branch -M main
git push -u origin main
```

## Step 3: Publish to Skills Hub (optional)

Skills Hub is the official Hermes discovery catalog. Publish individual skills:

```bash
hermes skills publish audio-dsp/mamba3-dsp-methodology --to github --repo YOUR_USERNAME/hermes-skills
```

This makes the skill searchable via `hermes skills search` and the Hub web UI.

## Step 4: List on Gumroad

### Product structure

For a **Complete Skills Bundle** ($39-49):
- **Attached file:** Versioned .zip of all skill directories
- **Post-purchase content:** GitHub tap URL + install instructions
- **License key:** Optional — gating the .zip discourages unauthorized sharing

For **Niche Packs** ($15-19 each):
- Same structure but scoped to a category
- Makes the buying decision easier for price-sensitive buyers

### Listing copy formula

```
[Benefit-driven headline]

[1-2 sentence value prop]

What's included:
- [Category 1]: [N] skills covering [scope]
- [Category 2]: [N] skills covering [scope]
- ...

Free updates — the GitHub tap repo is public and always current.
```

See the `gumroad-digital-product` skill for detailed Gumroad setup (license keys, MoR tax handling, post-purchase content).

### Pricing signals

- Skills Hub has 88k+ skills but most are free/community
- A curated, high-quality library at $39-49 is reasonable for professionals
- Niche packs at $15-19 are impulse-buy territory
- Bundle discount: $49 for the complete set vs. $70+ buying packs individually

## Step 5: Updates and Maintenance

- **GitHub tap repo is the source of truth** — update skills there
- **Gumroad .zip** — update when you push a major batch of changes
- **CHANGELOG** — keep one in the repo root so tap users see what changed
- Announce updates on Discord (#skills channel)

## Pitfalls

- **Never include .env, credentials, or local paths** — sanitize ALL files before publishing
- **Don't publish as a single .zip without the tap repo** — users can't auto-update from a zip
- **Don't overprice** — community expects skills to be free or cheap; value is curation and convenience, not exclusivity
- **Don't abandon** — if you stop updating, the Hub marks skills as stale
- **YAML frontmatter must be valid** — broken metadata = skill won't load
- **Category names must match Hermes convention** — lowercase-kebab-case
- **GH username in tap must match the repo owner** — org vs personal matters; changing it breaks existing taps
- **Test from a clean install before telling anyone** — `hermes skills tap add` then `hermes skills install` must work

## Verification

Before publishing:

```bash
# Check all SKILL.md files parse correctly
hermes skills check

# Verify the repo structure is navigable
ls -R | head -40

# Test from a clean install
hermes skills tap add YOUR_USERNAME/hermes-skills
hermes skills install a-test-skill
```

## Related Skills

- `gumroad-digital-product` — detailed Gumroad listing setup
- `github-repo-management` — creating and managing the tap repo
- `hermes-agent-skill-authoring` — writing SKILL.md files
