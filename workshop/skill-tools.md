# Skill-to-tool guide

Read [agent.md](../agent.md) for policies and entry-point routing. All command paths below are relative to the repository root unless noted. Tools are reviewed source, **not all enabled production steps**.

## Install levels

| Level | Installed here | What that actually means |
|---|---|---|
| Agent instructions | 26 `.agents/skills/` adapters and matching `.claude/skills/` adapters | Discoverable files with source links and local policy overrides; no service permission |
| Reviewed upstream source | 80 locked files under `workshop/vendor/` | Exact retained source and licenses; not remote code fetched at run time |
| Core CLI guidance | HyperFrames 0.9.98 npm skill files, plus retained official registry skill | Requires `npm ci` after a fresh checkout; production CLI remains pinned |
| Optional utility packages | Installed into ignored `.venv/` during this integration | Imports tested, **no Whisper model downloaded**, no API credentials provisioned |
| External research | YouTube, thumbnails, captions, stats, Reels/TikTok | Conditional on reachable endpoints, authorized data access and rights; YouTube blocked in this sandbox |
| Speech recognition | faster-whisper `small.en` | Package installed; model not installed, Hugging Face blocked; no word-level transcription claimed |
| Earshot / Canva | Not installed or activated | No MCP setup, sign-in or new connector required for this workshop |

Install the same Python tool set on a future checkout:

```bash
python3 -m venv .venv
.venv/bin/pip install -r workshop/requirements.txt -r workshop/requirements-skills.txt
.venv/bin/pip check
eval "$(node workshop/runtime.mjs)"  # FFmpeg/ffprobe/browser paths, if needed
export HYPERFRAMES_PYTHON="$PWD/.venv/bin/python"
python3 workshop/skills.py --check
```

The base requirements are installed too so selecting `.venv` for optional research cannot accidentally remove Kokoro availability. Dependencies are free local tools; installing them does not make their model/data hosts reachable or authorize a hosted service. Do not print environment variables containing credentials.

## Research helpers — every upstream tool

Source root: `workshop/vendor/ytb-research-skills/`. Research outputs must **not** be written into locked vendor source. For optional output-writing tools, copy the reviewed kit into an ignored scratch workspace first:

```bash
# One-time preparation; use a new empty directory, never overlay user work.
mkdir -p .cache/skill-workspaces
cp -R workshop/vendor/ytb-research-skills .cache/skill-workspaces/research
# Resolve the interpreter before cd, if using one.
# From repo root, invoke tools with full repo-relative paths, as below.
```

Example commands below requiring URLs are conditional documentation, **not successful live research from this run**. Replace `<authorized-url>` only with a real user-provided or discovered public reference that can legitimately be studied. Never pass a leading-dash URL or arbitrary shell text. Do not import copied clips/thumbnail images into production without independent usage rights.

| Tool (retained source path) | Installed skill(s) | Input/output and use | Status / requirements |
|---|---|---|---|
| `workshop/vendor/ytb-research-skills/tools/yt.py` | `ytb-research`, `ytb-analyse`, `ytb-channel-analysis`, `ytb-outlier-pulse`, `ytb-breakout-detector`, `ytb-study`, `ytb-video-breakdown`, `ytb-hook-machine` | `video`, `channel`, `comments`, `search`: observed metadata; `transcript`, `watch`: captions/frames/private notes | Usage smoke-tested only. Stats need an already authorized free `YOUTUBE_API_KEY` and reachable YouTube API. Transcripts/watch use yt-dlp, with optional model fallback. Network blocked here. No key was obtained or account configured. |
| `workshop/vendor/ytb-research-skills/tools/reel_fetch.py` | `ytb-study`, `ytb-video-breakdown` | Reels/TikTok public URLs → scratch `research/reels/<id>/` video/audio/frame sheets | Conditional, not run on live media; yt-dlp + FFmpeg; private rights-respecting analysis only. No login workaround. |
| `workshop/vendor/ytb-research-skills/tools/thumbs.py` | `ytb-research`, `ytb-hook-machine` | Video/channel/playlist URLs → scratch `research/thumbnails/` and CSV | Usage smoke-tested. Needs yt-dlp / image hosts; not a source of licensed production thumbnails. |
| `workshop/vendor/ytb-research-skills/tools/script_check.py` | `ytb-script`, `ytb-hook-machine` | Spoken text → length estimate, weak-opener/AI-phrase/long-sentence checks | **Executed successfully on current narration.** Stdlib only. Use the wrapper below; the upstream parser treats `##` sections specially and would otherwise check editorial notes instead of our actual script. WPM is not audio timing. |

```bash
# Ready offline, on existing narration only:
python3 workshop/review_script.py
# Optional future network commands, from repo root after scratch setup:
.venv/bin/python .cache/skill-workspaces/research/tools/yt.py transcript '<authorized-url>'
.venv/bin/python .cache/skill-workspaces/research/tools/yt.py watch '<authorized-url>' --every 2
.venv/bin/python .cache/skill-workspaces/research/tools/thumbs.py '<authorized-url>' --max 5
.venv/bin/python .cache/skill-workspaces/research/tools/reel_fetch.py '<authorized-url>'
```

No network here → record the unavailable fields and proceed with institutional science research and an explicitly editorial hook rubric. Do not write “viral”, “winner”, view counts, outlier scores or quotations as observed evidence without actual data. No Canva document is created by these Python tools; the skills' local Markdown fallback suffices.

## Editing helpers — every upstream tool/module

Source root: `workshop/vendor/ytb-edit-kit/`. Map upstream `tools/` paths to that root. If experimenting with output-writing helpers, copy this kit into a new `.cache/skill-workspaces/edit` directory just like the research workspace. Never run the legacy builder against `film/` or `output/`.

| Tool/module (retained source path) | Installed skill(s) | Use / output | Compatibility and gate |
|---|---|---|---|
| `workshop/vendor/ytb-edit-kit/tools/transcribe.py` | `ytb-edit`, `workshop-production` | Run inside scratch audio directory: real voice file → `words.json` with word timestamps | **Conditional, not verified synthesis/transcription.** faster-whisper + numpy + FFmpeg; attempts `small.en` weights from blocked host. Review actual output and every key anchor before captions. Never split phrase timings into fake word timestamps. |
| `workshop/vendor/ytb-edit-kit/tools/tighten.py` | `ytb-edit` | `voice.mp3` + `words.json` → tightened WAV, mapped words/cuts | **Reference-only here.** Installed FFmpeg rejects upstream `-/filter_complex`. Also changes the audio clock and deliberate pauses. Do not use on this completed episode; requires a reviewed compatibility port and full retiming/rerender. |
| `workshop/vendor/ytb-edit-kit/tools/captions.py` | `ytb-edit`, `hyperframes`, `workshop-production` | Actual `words.json`/`words_tight.json` → SRT + styled ASS; pass `--size 1080x1920 --max 32` | **Synthetic known-timing portrait smoke test passed.** Stdlib only. Default is landscape, and default ASS margins are not a Shorts-safe guarantee; inspect layout yourself. Current episode's exact SRT remains built from verified phrase samples. |
| `workshop/vendor/ytb-edit-kit/tools/gif2mp4.py` | `ytb-edit`, `workshop-production` | Licensed/owned animated image + duration → H.264 MP4 / alpha WebM | **Owned synthetic GIF → H.264 → full decode passed.** Needs Pillow/FFmpeg. Converts an asset, does not replace HyperFrames composition. No unlicensed meme sourcing. |
| `workshop/vendor/ytb-edit-kit/tools/edit_kit/new_video.py` | `ytb-edit` | Empty scratch episode path → assets/audio/render folders and `shots.py` | **Scratch scaffold tested.** Not the authoritative workshop layout. Never point it at existing delivery directories. |
| `workshop/vendor/ytb-edit-kit/tools/edit_kit/build.py` | `ytb-edit`, `hyperframes` | Legacy `shots.py` + real word timings → its own HyperFrames project | **Reference-only.** Python 3.11 syntax failure at line 362; landscape geometry, legacy template/version and remote asset assumptions. It imports/executes `shots.py`, so treat shot files as code. Do not substitute it for the working portrait builder. |
| `workshop/vendor/ytb-edit-kit/tools/edit_kit/storyboard.py` | `ytb-edit`, `hyperframes-cli` | Legacy shot times/project → storyboard | **Reference-only.** Invokes `npx --yes hyperframes@0.8.226`, resizes sheets to 16:9 and deletes/recreates its target `storyboard/`. Use pinned installed `hyperframes snapshot --review` instead. |
| `workshop/vendor/ytb-edit-kit/tools/edit_kit/final_check.py` | `ytb-edit`, `engineering-diagnosing-bugs` | Real render + expected words → Whisper comparison/loudness | **Conditional ASR aid, not a QA gate.** Needs unavailable model. Prints missing words but does not exit nonzero for mismatches. Its “every word is clear” text is not proof of human listening. Mandatory `workshop/qa.py` still runs. |
| `workshop/vendor/ytb-edit-kit/tools/edit_kit/kinds.py` | `ytb-edit`, `hyperframes-registry` | Library of shot CSS/markup recipes, not a CLI | Reference only; review individual geometry/animation/network assumptions, port appropriate ideas into deterministic portrait scenes. See adjacent `KINDS.md`. |
| `workshop/vendor/ytb-edit-kit/tools/edit_kit/theme.py` | `ytb-design-system` | Reads legacy `brand/design.json`, recolours markup | Reference only; emitted Google Fonts links need replacing with local fonts. Does not define an approved channel identity. |
| `workshop/vendor/ytb-edit-kit/tools/edit_kit/shots_template.py` | `ytb-edit` | Example Python shot plan used by `new_video.py` | Example data/code, not an episode or standalone CLI. Replace facts/media/geometry; never execute untrusted shot code. |

For a future **real** word-timing file, a scratch caption export looks like:

```bash
# Inputs must exist; this is not a claim that Whisper worked in this sandbox.
.venv/bin/python workshop/vendor/ytb-edit-kit/tools/captions.py \
  path/to/actual-words.json .cache/caption-review --size 1080x1920 --max 32
```

## Current production helpers and stack coverage

| Tool / technology | Skill(s) | Authoritative operation |
|---|---|---|
| Arena native image generation | `workshop-production`, `ytb-design-system`, `hyperframes` | Invoke Arena's built-in image tool and save originals/prompts. No external image provider or API keys. |
| HyperFrames scene/GSAP animation | `hyperframes`, `ytb-edit` | `film/index.html` + scene sub-compositions, deterministic paused timelines, local assets |
| HyperFrames registry | `hyperframes-registry` | Actual `catalog` / `add` CLI or already reviewed official source, not invented registry commands |
| HyperFrames doctor/browser/check/snapshot/preview/render/clean | `hyperframes-cli` | Use installed 0.9.98 `--help`; keep portrait root and explicit 30fps |
| `workshop/voice.py`, Kokoro / Edge fallback | `workshop-production`, `media-use` | Actual CLI synthesis; matching-take cache check; explicit fallback only on failure |
| `workshop/setup-kokoro-offline.py` | `workshop-production`, `engineering-diagnosing-bugs` | Explicit version/hash-gated q8 model workaround; no hidden provider change |
| `workshop/runtime.mjs`, Chromium, npm FFmpeg/ffprobe | `hyperframes-cli`, `workshop-production` | Print shell exports for local binaries/shared libs; no server/framework replacement |
| `workshop/build.py`, FFmpeg mixing | `hyperframes`, `media-use`, `ytb-edit` | Sample-clock HTML/SRT, sidechain ducking, licensed effects, normalization; renders still go through HyperFrames |
| `workshop/qa.py`, ffprobe/full decode/audio/frame checks | `workshop-production`, `engineering-diagnosing-bugs`, `engineering-code-review` | Independent analysis of exported MP4; no human-listening claim |
| `workshop/thumbnail.py`, Pillow | `workshop-production`, `ytb-design-system`, `ytb-hook-machine` | Typography over original Arena imagery, check actual portrait JPG |
| `workshop/review_script.py` | `ytb-script`, `ytb-hook-machine` | Narration-only adapter to upstream script checker; review warnings, do not retime from WPM |
| `workshop/skills.py` | `engineering-codebase-design`, `engineering-tdd`, `engineering-writing-for-agents` | Offline non-clobbering install, hash verification and catalogue |
| `git`, `gh` and regression tests | `engineering-pr`, `engineering-code-review`, `engineering-tdd` | Current-session branch only; evidence and unchanged-media hash; no merge/settings changes |

## Boundaries verified in this integration

- Local source and adapter integrity, installation idempotence and refusal to clobber unknown skill files.
- Corrupt source hashes reject installation **before** any adapter writes.
- Upstream weak-opener detector fails a deliberately bad hook; current 112-word narration passes without checking editorial guardrails as spoken text.
- Portrait SRT/ASS conversion and short owned GIF decode work with existing free tools.
- Original finished-video SHA-256 is unchanged. No second production or incidental re-render.
- Live YouTube research, external thumbnails, Whisper `small.en` transcription, legacy kit rendering and earshot listening were **not** successfully executed. The source/skills exist; do not describe those operations as completed.

Actual run evidence: [skills smoke-test JSON](qa/skills-smoke.json), [integration report](skills-integration-report.md). Optional downloaded videos, frame sequences, model caches and API credentials must remain ignored scratch data, never vendored source or publishing assets.
