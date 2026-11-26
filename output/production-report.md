# Production report — What if the Sun vanished?

**Date:** 2026-11-26 UTC
**Repository:** `fardin3693/video_gen`
**Working branch:** `arena/58b24915-video-gen`
**Delivery file:** `output/final_video.mp4`

## Delivered artifact

| Property | Verified result |
|---|---|
| Duration | **54.000 seconds** |
| Dimensions / orientation | **1080 × 1920**, portrait 9:16 |
| Frame rate / frame count | **30/1 fps**, **1,620 frames** |
| Container / video / audio | MP4 / H.264 / AAC stereo, 48 kHz |
| File size | **14,251,622 bytes** (~13.6 MiB), ordinary Git file, below GitHub's 100 MB file limit |
| SHA-256 | `3f92a10306f3efe36772c607d8c614d0c0df613cb4dc1f042f096d79128ae1b7` |
| Narrator | **Local Kokoro-82M q8**, `am_michael` English male, through official HyperFrames TTS CLI |
| Narration | 24 verified WAV sections, 48.405 s total source speech; 3.750 s planned pauses; begins 0.180 s, final phrase ends 51.735 s |
| Primary visual assets | **4 Arena-native generated images**, **0 sourced photos/footage** |
| Other visuals | 3 original full scientific diagrams plus a travelling-light pulse, deterministic particles, varied camera moves, typography and captions |
| Composition | 11 visual sub-compositions + 1 dedicated captions sub-composition |
| Sound | Attributed cinematic music bed, 2 CC0 effects, automatic narration-driven music ducking |
| Branding | No invented channel, logo, intro, or subscription reminder |

Exactly one finished video is retained. A preliminary export was replaced at the same path after QA; it is not delivered as another film.

## Execution and environment

The initial repository inspection found only `lol.md` and Git history. The original sample file and history are untouched. No obsolete pre-existing video implementation existed to remove.

- Node 22.22.3; npm 10.9.8; Python 3.11.2; approximately 3.8 GB RAM / 2 CPUs and 19–20 GB initially free disk.
- Installed official `hyperframes@0.9.98`, `@sparticuz/chromium@158.0.0`, npm-provided FFmpeg and ffprobe. Chromium **158.0.8127.0** was extracted and verified to run with the bundled shared libraries.
- FFmpeg is the working static npm build `N-47683-g0e8eb07980` (2018); ffprobe is a newer npm static build. Both were tested, not assumed. The older FFmpeg still supported this render, normalization and all independent QA.
- OS package downloads and the normal Chromium CDN were blocked. No paid/cloud fallback was used.
- `npx hyperframes skills update` was executed but failed because its raw GitHub manifest could not be reached. The official source archive was fetched from codeload.github.com; all four requested skills (`hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `media-use`) were installed from that archive and read.
- Official source archive used for skill/registry inspection: `https://codeload.github.com/heygen-com/hyperframes/tar.gz/refs/heads/main`; archive SHA-256 `504fc293d114c360663b95a767d4fcf4634615b5272745b7ac81255e79c79b86`.
- Official `catalog` and `add` commands were attempted, but live registry access failed. A local HTTP source was also rejected by the CLI's HTTPS-only registry validation. The original `caption-editorial-emphasis` and `fade-through` snippets were copied from the official source archive instead and their timing/entrance recipes adapted. No network security check was disabled for registry access.

### Kokoro details — explicit deviation from stock downloads

`tts --list` was inspected, and a male `am_michael` voice selected. Actual stock synthesis failed first because Python dependencies were absent, then because the GitHub release-model fetch failed. Python dependencies were installed into a virtual environment. A verified alternative **Kokoro-82M q8 ONNX export** was obtained from the free `kokoro-q8-shards@1.0.0` npm distribution; the original 54 voice tensors were obtained from `kokoro-js@1.2.1` and rebuilt into the NPZ layout required by kokoro-onnx.

The installed HyperFrames 0.9.98 model/voice integrity pins were **explicitly retargeted** to these alternative files; the stock CLI itself was otherwise retained for narration. This is documented and reproducible in `workshop/setup-kokoro-offline.py`. It is not claimed to be an unmodified full-precision model download.

- Model SHA-256: `fbae9257e1e05ffc727e951ef9b9c98418e6d79f1c9b6b13bd59f5c9028a1478`.
- Rebuilt voices SHA-256: `774702d974ab0e2fda871948a17baa8f8b2e348e77e436c122b1be95c168e865`.
- Real test audio was generated and probed before making the narration. Then all 24 production sections were successfully synthesized with the official `hyperframes tts` command.
- Speeds range from 0.92 to 1.02, with deliberate section pauses and consistent voice identity.
- **Edge TTS was not used:** Kokoro succeeded after this workaround. No paid TTS fallback or Arena speech voice was substituted.
- Weights, downloaded source tarballs and dependency caches are not Git deliverables.

## Scientific / editorial decisions

Selected the evergreen Sun question using a candidate comparison rather than claiming an unverified trend ranking. See `sources.md` for the comparison and the full claim audit.

The premise is explicitly called an **impossible thought experiment** in narration and on-screen. Real conservation of mass-energy forbids a Sun simply disappearing; an explosion would not remove its mass-energy. Light travel time is approximate. The orbit is an idealized tangent, not a full N-body simulation. No fabricated cooling deadline is given. The frozen landscape is labelled long-term illustration. Survival is conditional and applies to some microbial life, not indefinite human survival or every vent animal. NOAA, NASA/JPL, NASA climate references, University of Illinois physics explanations and USGS heat references were consulted.

## Captions and audio

- Captions and SRT are timed to **actual PCM sample counts** of each generated phrase, not a guessed script WPM.
- Explanations and the hook use phrase cues with highlighted keywords. The dramatic “Life / could / survive” revelation uses individually generated, individually timed word cues and larger editorial typography. Full word-by-word forced alignment of the hook was **not** performed or claimed.
- Captions occupy the YouTube Shorts safe region; the target is not the narrower lower-right TikTok safe box.
- Music: Alexander Nakarada's **Space Ambience**, used under the composer's **CC BY 4.0** terms with the required description credit. A GitHub mirror misleadingly categorizes its collection as CC0; that broad categorization was not relied upon. The composer's own page and embedded track metadata were checked.
- Two effects are Soundza SoundKit CC0 assets with explicit source/license records. No unverified copyrighted music or paid catalog was used.
- Automatic sidechain ducking keeps music below the narration. Fade-in/out, selective effects and normalization were applied. Rendering used the prepared local master track.

## Render

Actual command, from `film/`:

```bash
npx hyperframes render --quality delivery --fps 30 --workers 1 --no-browser-gpu --crf 20 -o ../output/final_video.mp4
```

**Status: complete.** Official HyperFrames performed timeline seeking, all 1,620 frame captures, H.264 encoding and AAC muxing. Screenshot capture / software GPU, one worker. Final render took **4m 14.3s**. No other composition framework was used. FFmpeg was used for audio preparation and independent QA, not as a replacement scene/timeline renderer.

The HyperFrames preview was opened and returned HTTP 200. Because this CLI version binds loopback, an ephemeral same-origin proxy on 0.0.0.0:3003 exposed the editor in Arena. This is session tooling, not a new video-generation dashboard.

## QA results

Saved machine-readable evidence is in `output/qa/`.

- **ffprobe:** duration, frame count, codecs, exact dimensions and 30 fps all verified against the exported MP4.
- **Full FFmpeg decode:** exit 0, **zero decode errors**; `decode-errors.txt` is intentionally empty.
- **Black detection:** no fully black interval of 80 ms or more at the stated threshold.
- **Frame review:** inspected actual decoded opening, middle and ending frames, including 0.0, 0.8, 4, 8, 11.4, 14, 20, 22, 25, 30, 35, 40, 45, 50 and 53.9 seconds. No missing image, unintended blank scene, text collision or broken crop observed. The dark-city scene is intentionally dark but has legible titles/captions.
- **Motion QA:** the initial render had near-static portions in the orbital diagram. Continuous diagram camera movement was added, then the film was rerendered. The replacement passes the consecutive one-second decoded-frame difference check; minimum mean pixel difference at 108×192 is **0.03467**. This is a useful freeze smoke test, not proof of physically accurate animation.
- **HyperFrames check:** `ok: true`, **zero errors**, no runtime, layout, contrast or audio warnings. Two reviewed non-blocking warnings: (1) 24 caption clips intentionally share one captions file, (2) the minor “Solar orbit” diagram label briefly scales to 27.17 px at the start of its slow camera move, just below the 28px craft recommendation. Main captions remain 48px. Both are retained as documented tradeoffs, not hidden as a warning-free pass.
- **Snapshot workflow:** used initial scene snapshots plus official `snapshot --review` and phone-sized sheets. Corrected bright-city contrast, small notes, caption layout and a scientifically confusing daylight cutaway before the final render.
- **Measured final audio:** **−15.63 LUFS integrated**, **−1.44 dBTP true peak**, **3.20 LU** loudness range. No clipping indicated.
- **Narration presence:** all 24 intended speech ranges have non-silent decoded audio. Pauses and the ~2.3s final music/image tail are deliberate.
- **Audio/caption alignment:** comparison of decoded rendered audio with the prepared master found approximately **−21.375 ms** offset, under one 30fps frame, normalized correlation **0.9870**. SRT phrase boundaries derive from the same master clock.
- **Review limitation:** audio was verified by decode, waveform/energy, correlation and loudness analysis. **No human-style listening audition is claimed**, and these measurements cannot certify subjective pronunciation or emotional quality.
- Thumbnail verified visually as a 1080×1920 JPEG using the Arena-generated hero image and local typography.

## Publishing files and workshop files

All nine requested deliverables are in `output/`:

1. `final_video.mp4`
2. `thumbnail.jpg`
3. `script.md`
4. `subtitles.srt`
5. `description.md`
6. `sources.md`
7. `asset-credits.md`
8. `storyboard.md`
9. `production-report.md`

Additional necessary files: editable HyperFrames HTML/config/assets in `film/`; pinned npm dependencies; production helpers, metadata, tests, native-image prompts, workflow instructions and third-party notices in `workshop/`; compact QA evidence in `output/qa/`. The final MP4 is tracked, not merely linked to external storage.

## Cleanup ledger

No original repository file was removed. The original `lol.md` remains byte-for-byte unchanged. Identified current-run files removed after retaining required evidence:

- `.ttstest/test.wav` and the now-empty `.ttstest/` — early synthesis verification, not a production take.
- `film/assets/audio/narration.wav` — temporary concatenated PCM mix input; reproducible from retained 24 source takes. The final mixed `master.m4a` is retained.
- `film/.hyperframes/artifacts/snapshots/` — ~89.3 MB official review captures, removed using `hyperframes clean --snapshots` after its dry run.
- `film/.hyperframes/artifacts/checks/` — transient check runs; final report copied to `output/qa/hyperframes-check.json` first.
- `film/.hyperframes/artifacts/inspection/` — initial diagnostic frame captures, superseded by compact decoded-frame evidence.
- `film/CLAUDE.md` — unused boilerplate generated by the new project scaffold; replaced by the focused root `AGENTS.md` and concise film pointer.
- `workshop/sfx-origin.md` — research copy for an unused Pixabay pack; unused pack audio was never imported.

The preliminary MP4 was overwritten by the corrected final export, not kept as an extra deliverable. HyperFrames project history was preserved; node_modules, browser/model caches and other generated state are ignored. No hard reset, blanket Git clean, force push, unrelated configuration change, repository setting change or PR merge was performed.

## Financial and delivery status

No subscription purchased, paid service/API invoked, billing enabled or API key required. Tools were free/local; imagery used Arena's available native tool. The repository branch is `arena/58b24915-video-gen`; deliver through a pull request to `main` without merging. The PR URL and actual commit/push status are supplied in the final chat delivery after those operations, rather than predicted here.
