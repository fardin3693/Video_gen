# Asset ledger

Access/generation date: 2026-11-26. All render assets are local files. No remote media is fetched during frame rendering. No external image-generation API, API key, paid TTS provider, or HeyGen catalog was used.

## Original images — Arena native generation

| File in `film/assets/` | Origin and purpose | Terms / attribution |
|---|---|---|
| `sun-earth.jpg` | Arena built-in image tool; original vertical Earth/Sun scientific illustration | AI-generated via the user's Arena session; subject to applicable Arena/platform terms. Not NASA photography, not asserted to be CC0. No third-party source URL or required third-party credit identified. |
| `daylight-city.jpg` | Arena built-in image tool; normal daylight city and blackout comparison | Same as above; hypothetical location, no real-city claim |
| `frozen-world.jpg` | Arena built-in image tool; speculative long-term sunless-Earth landscape | Same as above; illumination is illustrative, not literal sunlight |
| `vent-life.jpg` | Arena built-in image tool; hydrothermal vent with microbes/animals | Same as above; ROV-style illumination, not sunlight |
| `output/thumbnail.jpg` | Derived from `sun-earth.jpg`; local typography/layout using Pillow | Arena imagery plus new layout; DejaVu font terms below |

**Visual count:** 4 Arena-generated scene images; 0 sourced photographs/footage; 3 original animated diagrams (orbit, heat reservoir, core). The thumbnail reuses the hero image; it is not a fifth generated image.

Prompts are retained in `workshop/image-prompts.md`. Generated depictions are illustrations, not observational evidence.

## Audio

| File | Origin / source | License and obligations |
|---|---|---|
| `film/assets/voice/00.wav`–`23.wav` | Local Kokoro-82M, voice `am_michael`, via the official `hyperframes tts` command; speeds per `workshop/episode.json` | Kokoro model and kokoro-js voice distributions declare Apache-2.0. No cloned human voice or hosted paid voice. Model/source notices preserved in `workshop/licenses/`. AI-generated output; do not misrepresent as a human recording. |
| `film/assets/audio/music.mp3` | **Space Ambience**, Alexander Nakarada, 2017 metadata. Composer: https://creatorchords.com/music/space-ambience/ . Downloaded from GitHub mirror: https://github.com/SoundSafari/CC0-1.0-Music/blob/655388f987eacf6d08d73080fcc3e727f267bfde/freepd.com/Space%20Ambience.mp3 . Original blob SHA: `17ee64af98ee03a9b98adfa9a2eeef0e417e6d11` | **CC BY 4.0**, verified on the composer's own track page. The mirror's broad CC0 categorization conflicts with the track metadata/composer; this production follows the composer's attribution-required terms. Excerpt from 00:18; trimmed, re-encoded, faded and ducked. Required credit appears verbatim in `description.md`. |
| `film/assets/audio/whoosh.mp3` | **Air Whoosh**, SoundKit by Soundza. https://github.com/soundza/soundkit/blob/c9ec55f61fcbc784f1f0d1390c7a6f79b0e68cd4/registry/soundza/sounds/air-whoosh.ts . Audio decoded from the repository's embedded data URI | CC0 1.0, declared in that source file and `LICENSE-AUDIO`; no attribution required. Voluntary credit given. |
| `film/assets/audio/impact.mp3` | **Cinematic Braam**, SoundKit by Soundza. https://github.com/soundza/soundkit/blob/c9ec55f61fcbc784f1f0d1390c7a6f79b0e68cd4/registry/soundza/sounds/cinematic-braam.ts | Same CC0 terms; timed to the blackout, reduced gain |
| `film/assets/audio/master.m4a` | Local automatic mix of the above narration, licensed bed and two effects | Composite output inherits music attribution obligation. Narration-triggered sidechain ducking and loudness normalization applied. |

No raw Pixabay effects were used. HyperFrames' bundled Pixabay pack was investigated but rejected in favor of the explicit per-repository CC0 ledger above.

## Fonts, animation sources and tools

- `film/assets/fonts/Inter-{400,700}.woff2` — Inter, Rasmus Andersson / Inter project, SIL OFL 1.1. https://github.com/rsms/inter . Copied from HyperFrames' bundled fonts.
- `film/assets/fonts/EBGaramond-700.woff2` — EB Garamond project, SIL OFL 1.1. https://github.com/octaviopardo/EBGaramond12 . Used for large revelation-word emphasis.
- `film/assets/fonts/JetBrainsMono-400.woff2` — JetBrains Mono, SIL OFL 1.1. https://github.com/JetBrains/JetBrainsMono . Used for labels.
- Thumbnail typography — system DejaVu Sans Bold. https://github.com/dejavu-fonts/dejavu-fonts . Bitstream Vera/DejaVu license; no font is embedded in the JPEG. System copyright/license copied into `workshop/licenses/DEJAVU.txt`.
- Font license texts are retained in `workshop/licenses/`; fonts are not offered under this workshop's own terms.
- `film/assets/vendor/gsap.min.js` — GSAP 3.15.0 bundled by official HyperFrames; GSAP Standard License, not an OSI license. https://gsap.com/standard-license/ . License header retained. Free use here; no standalone animation-tool redistribution service is being built.
- `film/compositions/components/caption-editorial-emphasis.html`, `fade-through.html` — official HyperFrames registry source copied from the official repository archive after live registry access failed. https://github.com/heygen-com/hyperframes/tree/main/registry/components . Apache-2.0; license retained in `workshop/HYPERFRAMES-LICENSE`. Caption emphasis, scale/fade entrance, and incoming fade recipe were adapted to portrait typography and actual audio boundaries in `workshop/build.py`. Original snippets remain editable references, not mounted demo scenes.
- Original SVG diagrams, scene layouts, moving particles and timeline construction — authored locally in this Arena session.
- HyperFrames 0.9.98 — official npm package, Apache-2.0. https://github.com/heygen-com/hyperframes . FFmpeg/FFprobe, serverless Chromium, Kokoro/ONNX Runtime and Pillow retain their respective upstream licenses; they are dependencies, not relicensed workshop assets.

## Required music credit (preserve on publishing)

Music: Space Ambience by Alexander Nakarada (https://creatorchords.com)
Licensed under Creative Commons Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/

Changes: excerpted, trimmed, re-encoded, faded, ducked and mixed with narration and effects.
