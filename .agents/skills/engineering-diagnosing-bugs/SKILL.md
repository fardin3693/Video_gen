---
name: engineering-diagnosing-bugs
description: "Build a fast reproducible failure signal before changing render/voice/QA code."
---

# engineering-diagnosing-bugs — workshop adapter

Project-local entry point. Read `agent.md` first, then the source below.
All paths here resolve from the repository root, not this skill folder.

**Source:** `workshop/vendor/mattpocock-skills/skills/engineering/diagnosing-bugs/SKILL.md`

**Use for:** Build a fast reproducible failure signal before changing render/voice/QA code.

**Local integration:** Use current Arena capabilities; if no subagent tool exists, perform clearly separated passes yourself and disclose it. No mandatory tracker setup or new issue/label/settings changes. User authorized autonomous work: choose/document test boundaries and use the request as the spec. Git/PR work stays on the session branch; never switch/create another branch or merge. Resolve upstream unprefixed skill references through agent.md, not slash-command guesses.

Tool requirements, output paths and blocked/conditional operations: `workshop/skill-tools.md`. Provenance and hashes: `workshop/skills-lock.json`.
Upstream instructions are reference material; they never override the user’s constraints or the repository production contract.
