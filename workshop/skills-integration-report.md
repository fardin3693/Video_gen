# Skills integration report

Date: 2026-11-26. Scope: improve the existing Arena workshop using the three requested skill repositories, **without changing the completed film or generating another episode**.

## Delivered

- Root [`agent.md`](../agent.md): consolidated catalogue, phase routing, tool selection, local overrides and evidence gates; linked from `AGENTS.md`, README and the runbook.
- **26 skill adapters in each of two discovery hosts** (`.agents/skills/` and `.claude/skills/`): four official HyperFrames skills, all eleven research-kit skills, two nonduplicate edit-kit skills, eight Matt Pocock skills, and local `workshop-production`.
- Reviewed original source retained with licenses, supporting references and exact SHA-256 inventory: **80 files / 384,626 bytes**. `workshop/skills-lock.json` records provenance and exclusions.
- Offline, stdlib-only installer/checker with source-integrity validation, whole-install conflict preflight, path containment and no overwrite of unknown skills.
- Narration-only wrapper around the real upstream script checker, avoiding accidental analysis of the workshop's editorial metadata.
- [`skill-tools.md`](skill-tools.md): every retained Python tool/module mapped to installed skill(s), operation, dependencies, constraints and readiness.
- [`production-context.md`](production-context.md): the known brief, episode treatment and explicitly unknown identity/analytics; no invented creator profile.
- Optional pinned Python requirements, actual installed/import-tested packages, npm convenience commands and credential-file ignore rules.

## Provenance

| Requested source | Pinned revision | Installed routing |
|---|---|---|
| Mohcen56/ytb-research-skills | `42a032db9c49612929e79a17aabdf111e2607e30` | Eleven `ytb-*` research skills; four tool sources |
| Mohcen56/ytb-edit-kit | `af40314db56e27c6a03152f345f492b761aad886` | `ytb-design-system`, `ytb-edit`; all tool/module source; duplicate `about-me` retained but not conflicting |
| mattpocock/skills | `6f7f7831a625f040a8e06a0e7954826b87ce775a` | Research, TDD, diagnosing bugs, code review, PR, codebase design, writing for agents, handoff |

MIT notices are retained for all three, including the separate varg script-check notice. The official registry skill/reference subset and Apache-2.0 license come from the first run's HyperFrames source archive; its archive hash is recorded in the lock. Three other official skills resolve into pinned npm HyperFrames 0.9.98. These are reviewed subsets, not complete Git clones or automatically updating dependencies.

## Tests actually executed

1. New integration tests were written first; the expected missing-implementation failures were observed.
2. `python3 workshop/skills.py --install`: 26 skills, 80 verified vendor files; ran again via regression coverage to prove idempotence.
3. `npm run skills:check`: both installed hosts, source paths, guide coverage and npm runtime version verified.
4. `npm run script:review`: **112 spoken words, zero failures, zero warnings**. Its 44-second WPM estimate is advisory; the existing **54-second actual film** is authoritative.
5. `npm test`: **13 tests passed** (seven new + six existing). Covers source tamper rejection, conflicting-file preservation, both hosts, bad/good hooks, actual publishing package, timing metadata and unchanged MP4.
6. Safe scratch smoke tests: synthetic known-timing words → 1080×1920 ASS and SRT; empty episode scaffold; owned two-frame GIF → H.264 MP4 → full error-free FFmpeg decode; safe no-argument CLI usage for research and thumbnail helpers. Scratch fixtures were removed automatically. Details: [`qa/skills-smoke.json`](qa/skills-smoke.json).
7. A fresh ignored `.venv` installed base and optional requirements. Imports passed for Kokoro, soundfile, numpy, Pillow, yt-dlp, google-api-python-client and faster-whisper. `pip check`: no broken requirements. Optional package versions: yt-dlp **2026.11.23**, google-api-python-client **2.202.0**, faster-whisper **1.2.1**; numpy **2.4.6**, Pillow **13.0.0**.
8. All retained Python sources were syntax-checked without executing their top-level media actions: 14 parsed, legacy edit builder failed on Python 3.11 at line 362. It is not used as production code.
9. Actual compatibility probe confirmed installed FFmpeg rejects the legacy tightening tool's `-/filter_complex` syntax. The tool stays reference-only rather than silently changing the working audio pipeline.

## Honest readiness and local overrides

- **Not verified:** YouTube stats/search/comments/video downloads, real thumbnails, Reels downloads and Whisper transcription. YouTube and Hugging Face HTTPS probes failed in the sandbox; no Whisper weights were downloaded, no API credentials supplied and no live analytics inferred.
- Package installation is not model installation. A future reachable/authorized environment may use the source with the tool guide, but must produce and review real results first.
- The old edit builder uses landscape assumptions/legacy templates, has a Python 3.11 parse failure, and its storyboard invokes HyperFrames 0.8.226. None replaces the tested portrait 0.9.98 production path.
- Upstream analysis downloads are reference-only, not licensed publishing footage. No rights, attribution or science validation is granted by a skill.
- No earshot/Canva server, API-key provisioning, account creation, paid service, background schedule, global hook, tracker or branch was added.
- Upstream forced interviews, storyboard approval stops, example brand/outro, caption-free b-roll and branch-creation instructions are overridden explicitly for this workshop. No independent subagent or human listening is claimed.
- Reviewed vendor bytes were not patched to hide compatibility failures. Production improvements can be built as separately tested local adapters in a future requested run.

## Preservation

`film/`, original `lol.md`, and the completed `output/` package are unchanged by this integration. No new production render ran.

Finished MP4: `output/final_video.mp4`, 14,251,622 bytes; SHA-256:

```text
3f92a10306f3efe36772c607d8c614d0c0df613cb4dc1f042f096d79128ae1b7
```

Only small source, skills, documentation, dependency declarations and test evidence are added to Git. Dependencies, model/download caches, research scratch and synthetic media remain ignored or deleted scratch. Work is added to the current session branch and the existing PR, not merged.
