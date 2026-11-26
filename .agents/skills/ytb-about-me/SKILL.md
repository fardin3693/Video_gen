---
name: ytb-about-me
description: "Read known creator constraints; optional creator-context interview only when requested."
---

# ytb-about-me — workshop adapter

Project-local entry point. Read `agent.md` first, then the source below.
All paths here resolve from the repository root, not this skill folder.

**Source:** `workshop/vendor/ytb-research-skills/.claude/skills/about-me/SKILL.md`

**Use for:** Read known creator constraints; optional creator-context interview only when requested.

**Local integration:** Read agent.md before upstream instructions. Map tools/ to workshop/vendor/ytb-research-skills/tools/. Run output-writing tools only in an isolated research workspace (see tool guide). No mandatory interviews, fabricated identity/metrics, CTA, or Canva dependency. Statistics tools need a preconfigured free key and reachable YouTube; otherwise record unavailable. Do not ask for or store credentials in chat. Research media is not licensed production media.

Tool requirements, output paths and blocked/conditional operations: `workshop/skill-tools.md`. Provenance and hashes: `workshop/skills-lock.json`.
Upstream instructions are reference material; they never override the user’s constraints or the repository production contract.
