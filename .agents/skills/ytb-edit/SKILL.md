---
name: ytb-edit
description: "Plan voice-led visual changes, storyboard and inspect the final HyperFrames edit."
---

# ytb-edit — workshop adapter

Project-local entry point. Read `agent.md` first, then the source below.
All paths here resolve from the repository root, not this skill folder.

**Source:** `workshop/vendor/ytb-edit-kit/.claude/skills/edit/SKILL.md`

**Use for:** Plan voice-led visual changes, storyboard and inspect the final HyperFrames edit.

**Local integration:** Map tools/ to workshop/vendor/ytb-edit-kit/tools/. Upstream edit builder/storyboard are reference-only here: they hard-code landscape layouts and HyperFrames 0.8.226. Use workshop/build.py plus installed HyperFrames 0.9.98 for portrait delivery. Do not remove mandatory captions from b-roll, invent a brand, require approval stops, or claim model-based listening/ASR without actual output. See workshop/skill-tools.md for every helper.

Tool requirements, output paths and blocked/conditional operations: `workshop/skill-tools.md`. Provenance and hashes: `workshop/skills-lock.json`.
Upstream instructions are reference material; they never override the user’s constraints or the repository production contract.
