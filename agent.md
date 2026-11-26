# Agent skill map — Arena video workshop

**Read this file at the start of video work.** This is the root routing guide requested by the owner; `AGENTS.md` is the production contract. Load only the skill needed for the current phase, then its supporting references. Do not load all vendor instructions into every task.

## Start here

1. Read [AGENTS.md](AGENTS.md), [production context](workshop/production-context.md), and the [runbook](workshop/agent-runbook.md).
2. Run `python3 workshop/skills.py --check`. If entry points are missing, run `python3 workshop/skills.py --install`; if npm-provided core skills are missing, run `npm ci`. Installation is offline, project-local and non-destructive.
3. Choose a skill below. Read its `.agents/skills/<name>/SKILL.md` adapter, then its upstream source. The equivalent `.claude/skills/` entry is also installed. Names are routing identifiers; use file reads in Arena, not a fictitious slash-command executor.
4. Before a tool call, consult [tool setup and compatibility](workshop/skill-tools.md). **Skill installed ≠ service reachable ≠ model downloaded ≠ operation verified.**
5. For a new production, complete the actual render and all QA/package gates. Installing skills alone must not trigger a second video or overwrite the completed episode.

## Local rules that take priority over third-party defaults

- **Arena remains the operator.** No separate AI service/dashboard. Primary visuals use Arena native image generation; narration uses local Kokoro via `hyperframes tts`, free Edge only on real Kokoro failure. No paid provider, billing, key-requiring image API, automatic catalog resolver or sign-in workflow.
- **Shorts, not landscape.** Official installed HyperFrames **0.9.98**, 1080×1920, 30fps, 50–60 seconds; use `workshop/build.py`. The edit kit's `0.8.226` renderer, 1920×1080 layouts, remote fonts and fixed shot engine are **reference-only**, not the production renderer.
- **Autonomous, not an interview funnel.** Use the known brief. No forced `about-me`, `grill-me`, design interview, storyboard approval or tracker setup. Ask only if the current request truly cannot be completed safely without an answer. Unknown channel identity, creator biography, competitors and analytics stay unknown.
- **No invented branding or CTA.** The current palette is an episode treatment, not a channel brand. Never import the upstream example outro, personal success claims or a subscription reminder.
- **Captions remain mandatory over all scenes.** The edit kit's “no captions on b-roll” default does not apply. Preserve Shorts safe zones, contrast and real audio timing. Do not tighten narration without regenerating all dependent timing/captions/scenes. Do not call phrase timing word-level alignment.
- **Evidence before metrics.** Search/reference videos inspire presentation; NASA/NOAA/university/peer-reviewed sources support science. An outlier needs real view counts, a stated comparison window/baseline and provenance. No stats access → unavailable, not zero or an invented score. Editorial hook scores are explicitly subjective.
- **External services optional.** Local Markdown replaces mandatory Canva. YouTube API tools may use only an already configured authorized free key; no billing/account creation or credential collection in chat. If blocked, use accessible sources/local reference files and disclose missing metrics. No cookies, login tricks, DRM/paywall bypass or proxy evasion.
- **Rights stay separate.** Reference-video downloads are private analysis only, subject to applicable rights and platform terms; they do not become licensed b-roll, thumbnails or copied narration. Production music/SFX need verified licenses and attribution. Do not install extra MCP servers or claim listening through earshot; it is not installed here.
- **Available tools only.** Matt Pocock skills sometimes assume a Skill tool, fresh subagents, tracker setup or an interview. Arena may instead read files and perform separated research/review passes itself; disclose that no independent subagent ran. Use this request as the spec and document chosen test boundaries.
- **Git stays on the Arena session branch.** Never adopt upstream branch-creation/switching instructions. Commit/push only the assigned current branch; use `gh` for PRs; do not merge, configure repo settings, add labels/issues or schedule tasks without a separate request.

## Skill directory

### Official HyperFrames and native production tools

| Installed skill | When to read it | Source / completion condition |
|---|---|---|
| [hyperframes](.agents/skills/hyperframes/SKILL.md) | Composition contract, scenes, motion, captions, image placement | Pinned npm core skill; complete editable portrait timeline |
| [hyperframes-cli](.agents/skills/hyperframes-cli/SKILL.md) | Setup, doctor, check, snapshot, preview, render, audio, clean | Pinned npm core skill; real exported MP4, not a claimed CLI success |
| [hyperframes-registry](.agents/skills/hyperframes-registry/SKILL.md) | Search/adopt captions, overlays, transitions and camera recipes | Official retained source; use documented `catalog` / `add`, or local reviewed source if blocked |
| [media-use](.agents/skills/media-use/SKILL.md) | Audio treatment, mixing, captions and local media conventions | Pinned npm core skill; only local/free permitted routes; no provider auto-selection |
| [workshop-production](.agents/skills/workshop-production/SKILL.md) | Arena images, Kokoro/Edge, FFmpeg/ffprobe, Pillow thumbnail and publishing QA | Local runbook; verified video + nine-file package + licenses |

### YouTube research — Mohcen56/ytb-research-skills

All 11 research skills are installed. The edit kit's duplicate `about-me` is retained as source but not installed under a conflicting second name.

| Installed skill | Use | Output / access condition |
|---|---|---|
| [ytb-research](.agents/skills/ytb-research/SKILL.md) | Gather topic/reference ideas and observed metadata | Local ideas table; stats absent if no authorized access |
| [ytb-analyse](.agents/skills/ytb-analyse/SKILL.md) | Deep, timestamped report of one reference video | Local Markdown analysis; no mandatory Canva doc |
| [ytb-about-me](.agents/skills/ytb-about-me/SKILL.md) | Reuse known audience/workflow constraints; optional context interview | `workshop/production-context.md`; personal interview only if requested |
| [ytb-bullseye](.agents/skills/ytb-bullseye/SKILL.md) | Check whether topics suit general science-curious viewers | Qualitative topic/audience map; no made-up audience counts |
| [ytb-channel-analysis](.agents/skills/ytb-channel-analysis/SKILL.md) | Compare real winners with normal uploads | Conditional on a reference channel and observed metadata |
| [ytb-outlier-pulse](.agents/skills/ytb-outlier-pulse/SKILL.md) | Fresh candidate discovery from competitor outliers | Conditional; no automatic schedule, fabricated competitor list or “trending” claim |
| [ytb-breakout-detector](.agents/skills/ytb-breakout-detector/SKILL.md) | Find a channel's historical change in performance | Real stats and window required; current totals are not historical view curves |
| [ytb-hook-machine](.agents/skills/ytb-hook-machine/SKILL.md) | Draft and compare several first-line hooks | Evidence-backed rubric if data exists; otherwise clearly editorial rubric |
| [ytb-script](.agents/skills/ytb-script/SKILL.md) | Plain-English science narration, tension and payoff | Complete verified short script; `npm run script:review` checks narration only |
| [ytb-study](.agents/skills/ytb-study/SKILL.md) | Study batches of authorized reference videos | Timestamped notes, missing-data labels; propose lessons rather than inventing a locked style |
| [ytb-video-breakdown](.agents/skills/ytb-video-breakdown/SKILL.md) | Inspect real frames/transcript for pacing and visual lessons | State what was observed versus inferred, especially sound |

### Editing — Mohcen56/ytb-edit-kit

| Installed skill | Use | Integration boundary |
|---|---|---|
| [ytb-design-system](.agents/skills/ytb-design-system/SKILL.md) | Consistent episode colours, fonts, safe captions, sound rules | Reuse documented episode treatment; no invented channel brand or mandatory interviews |
| [ytb-edit](.agents/skills/ytb-edit/SKILL.md) | Voice-led storyboarding, literal visuals, selective effects and self-review | Use kit shot-kind ideas and caption tools selectively; retain the current portrait builder and official HyperFrames |

### Engineering — mattpocock/skills

Eight relevant skills selected; unrelated productivity systems, exercise scaffolds, software-factory services and repository-management hooks were not installed.

| Installed skill | Use | Local adaptation |
|---|---|---|
| [engineering-research](.agents/skills/engineering-research/SKILL.md) | Primary-source science, API and implementation research | Cited local findings; use sequential work when no subagent tool exists |
| [engineering-tdd](.agents/skills/engineering-tdd/SKILL.md) | Change helpers through tested public CLI behavior | Pick documented seams autonomously; observe failing then passing tests |
| [engineering-diagnosing-bugs](.agents/skills/engineering-diagnosing-bugs/SKILL.md) | Broken captions, media, dependencies, timing, render or QA | Reproducible red-capable command; fix cause, rerun it |
| [engineering-code-review](.agents/skills/engineering-code-review/SKILL.md) | Audit changes for standards and scope independently | Two labelled review passes; never claim absent subagents ran |
| [engineering-pr](.agents/skills/engineering-pr/SKILL.md) | Clear changes, evidence and risk in delivery PRs | Existing branch/PR, concise evidence, no merge |
| [engineering-codebase-design](.agents/skills/engineering-codebase-design/SKILL.md) | Small maintainable helper interfaces | No speculative dashboard, platform or alternative video engine |
| [engineering-writing-for-agents](.agents/skills/engineering-writing-for-agents/SKILL.md) | Keep this guide and future agent handoffs readable | Short entry points; detail behind explicit paths, checkable completion gates |
| [engineering-handoff](.agents/skills/engineering-handoff/SKILL.md) | Resume interrupted production accurately | Actual state, blockers, paths and next commands; no fabricated success |

Unprefixed upstream references resolve here: research/yt/idea work → `ytb-research`; primary-source implementation investigation → `engineering-research`; `script` → `ytb-script`; `edit` → `ytb-edit`; `tdd`, `code-review`, `codebase-design`, `pr`, `writing-for-agents`, `handoff` → corresponding `engineering-` entry. Other uninstalled skills are references, not instructions to install or invoke automatically.

## Phase-by-phase reading order

| Phase | Read | Done means |
|---|---|---|
| Inspect/setup | production contract → `hyperframes-cli` → tool guide | Branch/status known; actual tool readiness checked |
| Topic/research | `ytb-bullseye`, `ytb-research`, `engineering-research`; conditional outlier/channel skills | One chosen topic with credible claim sources and unknowns labelled |
| Hook/script | `ytb-hook-machine`, `ytb-script` | Several candidate hooks compared; complete scientific script; no checker failures |
| Voice | `workshop-production`, local-audio references in `media-use` | Verified approved-engine audio and real timing metadata |
| Images/style | `ytb-design-system`, `workshop-production` | Original Arena-native images saved, local typography, ledger |
| Compose | `hyperframes`, `hyperframes-registry`, `ytb-edit` | All scene/caption/audio clips follow the actual audio clock |
| Review/render | `hyperframes-cli`, `engineering-diagnosing-bugs` if needed | Checked previews/snapshots then actual portrait MP4 |
| QA/package | `workshop-production`, `engineering-code-review` | Decode, frames, audio, science, licenses and all nine files verified |
| Code changes | `engineering-codebase-design`, `engineering-tdd` as needed | Focused tested change, no media overwritten incidentally |
| Delivery | `engineering-pr`, `engineering-handoff` | Actual committed/pushed deliverables on current branch; PR open, not merged |

## Verify, use and update

```bash
npm ci
python3 workshop/skills.py --install    # .agents + .claude, never clobbers another skill
python3 workshop/skills.py --check      # source hashes + entries + guide + pinned HF source
python3 workshop/skills.py --list       # JSON catalogue
python3 workshop/review_script.py       # real upstream checker on current narration
npm test
```

Source revisions, licenses and exact vendored-file hashes live in [skills-lock.json](workshop/skills-lock.json); provenance/security findings and actual smoke-test results live in [skills integration report](workshop/skills-integration-report.md). Those files, not upstream HEAD, define the installed set. Updates are explicit: inspect a pinned upstream revision, copy only reviewed source, update the lock, regenerate adapters in a clean reviewed change and run tests. Never run an upstream installer/hook just because a skill mentions one. `--install` deliberately refuses different existing content; review changes rather than forcing an overwrite.

The installed entry points teach usage; they do not grant external service access. Core HyperFrames sources become available with `npm ci`; conditional YouTube downloads, API stats, Whisper transcription and legacy edit-kit builders retain their restrictions described in the tool guide. No video re-render is needed for this skills-only integration.
