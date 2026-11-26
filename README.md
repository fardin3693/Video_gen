# Arena-operated science Shorts workshop

A small **Arena Agent Mode workflow**, not a standalone AI application or dashboard. Arena researches, writes and directs each episode, generates its original images with its native image tool, then operates the local free production tools in this repository.

## Finished first production

**What if the Sun vanished?** — [`output/final_video.mp4`](output/final_video.mp4)

- 54.000 seconds · 1080 × 1920 · 30 fps · H.264 + AAC
- Official HyperFrames 0.9.98 composition/render; local Kokoro-82M `am_michael` narration
- Four Arena-generated images, original animated science diagrams, hybrid captions, attributed music and CC0 effects
- Publishing package and independent QA evidence: [`output/`](output/), including [`production-report.md`](output/production-report.md)

## Layout

```text
film/
  index.html                 # 1080×1920 / 30fps root; editable scene/audio hosts
  compositions/              # 11 visual sub-compositions + one captions track
    components/              # official registry recipes retained as editable references
  assets/                    # original images, phrase takes, licensed audio, local fonts/GSAP
workshop/
  episode.json               # reviewed script, scene assignments, voice and adaptive speeds
  voice.py                   # calls official HyperFrames TTS, one phrase at a time
  build.py                   # sample-clock timeline, SRT, HTML and automatic audio mix
  qa.py                      # independent ffprobe/decode/audio/frame/package validation
  thumbnail.py               # typography over Arena hero imagery
  runtime.mjs                # optional sandbox browser/FFmpeg environment setup
  setup-kokoro-offline.py     # explicit, version-gated npm model-cache workaround
  tests/                     # package/timing/media regression checks
output/                      # exactly one delivery MP4 + publishing package + compact QA
lol.md                       # original unrelated user file; preserved
```

## Free local setup

Requires Node.js **22+**, npm/npx, Python **3.10+**, FFmpeg, ffprobe and Chromium. Linux package managers are not required by the sandbox path below. Dependencies are pinned in `package-lock.json`.

```bash
npm ci
python3 -m venv .venv
.venv/bin/pip install -r workshop/requirements.txt
# Optional serverless-Chromium/FFmpeg setup, useful in Arena's restricted sandbox:
eval "$(node workshop/runtime.mjs)"
export HYPERFRAMES_PYTHON="$PWD/.venv/bin/python"

npx hyperframes skills update
npx hyperframes doctor
npx hyperframes tts --list
npx hyperframes tts "A real voice test." -v am_michael -o /tmp/voice-test.wav --json
```

If browser downloads are available, the stock supported setup is `npx hyperframes browser ensure`. `runtime.mjs` uses the freely distributed Chromium package instead when that download host is inaccessible. It exports browser, shared-library and binary paths; it does not replace HyperFrames rendering.

### Restricted-network Kokoro workaround used for this film

The stock CLI model download failed in Arena. The run therefore used the same Kokoro-82M family in a quantized ONNX export distributed through npm, and the 54 Kokoro voice tensors shipped by `kokoro-js`. Narration still went through **`npx hyperframes tts`**, not a substitute hosted provider.

```bash
# Only if the normal Kokoro model download fails:
.venv/bin/python workshop/setup-kokoro-offline.py
# Then repeat the real synthesis test above.
```

This is an **explicit installed-package patch**, not a stock HyperFrames feature: it seeds local files, verifies fixed SHA-256 hashes and retargets the 0.9.98 CLI's model/voice integrity pins. It refuses unknown CLI layouts. `npm ci` resets that patch; rerun it only when needed. Weights/caches are not committed. Do not casually remove the hash checks or claim this is the full-precision upstream model.

If Kokoro genuinely fails after setup, the approved free fallback is `edge-tts`:

```bash
.venv/bin/pip install edge-tts
.venv/bin/edge-tts --voice en-US-GuyNeural --text "A real fallback test." --write-media /tmp/edge-test.mp3
```

Edge requires access to Microsoft's speech endpoint and may also be blocked. Verify the actual audio before adopting it, regenerate timing metadata/captions, and record the engine honestly. Never choose paid TTS automatically. Edge was **not used or needed** for this film.

### Installed agent skills and tool routing

Start with **[`agent.md`](agent.md)**: the consolidated catalogue, phase-by-phase skill routing, local overrides and completion gates. The project includes **26 namespaced skills in both `.agents/skills/` and `.claude/skills/`**, pinned reviewed source from both Mohcen56 repositories and eight relevant Matt Pocock engineering/productivity skills.

```bash
npm run skills:install   # offline; never clobbers unknown skill files
npm run skills:check     # verify all vendor hashes, adapters and npm skill sources
npm run skills:list
npm run script:review    # narration-only checker; not an audio-duration estimate
# Optional research/edit utility packages (no model or key installed by this):
.venv/bin/pip install -r workshop/requirements-skills.txt
```

Read [`workshop/skill-tools.md`](workshop/skill-tools.md) before running an upstream helper. It maps every retained tool/module to its skill, input/output, setup and verified compatibility. The old edit-kit builder is reference-only; portrait rendering stays on the proven local workflow. YouTube access and Whisper weights remain blocked in this sandbox, despite successful package imports. See the [integration report](workshop/skills-integration-report.md) for exact results and limitations.

The installed npm package supplies three official HyperFrames skill sources; the fourth, registry guidance, is retained from official source with its license. No network fetch is necessary to install the project adapters after checkout. `npm ci` is required for npm-provided sources. An optional `hyperframes skills update` must not silently replace these locked project-local adapters.

Use the documented registry commands `npx hyperframes catalog --query "…" --json` and `npx hyperframes add <name> --json` when reachable. They were attempted here but the HTTPS registry host was blocked; the official archive supplied the retained caption/fade-through source. No fictitious `registry` or `captions` CLI commands are used. See the production report for deviations.

## Rebuild this episode

Committed phrase takes, assets and metadata allow rebuilding **without network inference**. Explicitly set the runtime first if Chromium/FFmpeg are not on PATH.

```bash
eval "$(node workshop/runtime.mjs)"
export HYPERFRAMES_PYTHON="$PWD/.venv/bin/python"
# Existing phrase takes are reused; a changed script requires new takes and re-audit.
python3 workshop/voice.py
python3 workshop/build.py

cd film
npx hyperframes lint
npx hyperframes check --safe-zone shorts --json
npx hyperframes snapshot --review
npx hyperframes preview --no-open
# Render in another shell, after inspecting preview/snapshots:
npx hyperframes render --quality delivery --fps 30 --workers 1 --no-browser-gpu --crf 20 -o ../output/final_video.mp4
cd ..
.venv/bin/python workshop/thumbnail.py
.venv/bin/python workshop/qa.py --complete
npm test
```

The composition declares portrait dimensions and `data-fps="30"`; the render also explicitly requests 30 fps. HyperFrames handles deterministic GSAP seeking, screenshot capture, encoding and muxing. FFmpeg is used separately for legal audio preparation/mixing and independent QA, not as an alternative composition engine.

`build.py` reconstructs a temporary `film/assets/audio/narration.wav`, automatically ducks music using the narration signal, places two timed effects, normalizes the mix, and writes `master.m4a`. Caption cues use **actual generated PCM sample boundaries**, not estimated words-per-minute. Three individually generated revelation words provide genuine word-level emphasis; explanatory captions and the hook are phrase-based. This is not forced alignment or an ASR transcript. A final AAC offset of about 21 ms was measured (less than one video frame).

Preview networking: the upstream local preview binds loopback in this version. Arena exposed a temporary 0.0.0.0 reverse proxy on port 3003 for browser access; browser requests stayed on the same origin. That proxy is session-only, not a new dashboard or part of the production architecture. Never put sandbox `localhost` URLs into browser-facing cross-service API calls.

## Future Arena sessions

Read [`agent.md`](agent.md), [`AGENTS.md`](AGENTS.md), [`workshop/agent-runbook.md`](workshop/agent-runbook.md), and the relevant installed skills. Ask Arena to make **one** new science Short. The agent must independently choose/research the topic, edit the episode script and scene builder, generate new primary imagery through Arena, verify free asset licenses, execute the real render and QA, update all publishing files, and open a PR on the session's current branch. The helpers do **not** discover topics or call external models independently.

Do not reuse a stale voice take after changing text: remove only that episode's identified derived takes, then regenerate them. Do not overwrite an earlier completed video unless the run explicitly replaces it; archive approved previous outputs under a clearly named episode directory first. Keep the delivery count at one new finished film per run.

## Licensing / cleanup

Music requires the attribution already included in `output/description.md`. Preserve it when publishing. Original AI images are not NASA media and are not declared public domain. See [`asset-credits.md`](output/asset-credits.md) and `workshop/licenses/`.

Preserve unrelated files and history. Remove only identified obsolete or current-run intermediate files; record paths in each production report. Use `npx hyperframes clean --dry-run` before `clean`; never delete `.git`, hard-reset, force-push, or indiscriminately clean the tree. Ignore dependency/model caches and large frame sequences. The finished MP4 is deliberately tracked as an ordinary Git file (~14 MB), below GitHub's per-file limit; no LFS or external link substitutes for the deliverable.
