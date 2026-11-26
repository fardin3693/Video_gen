# Arena production contract

This is an **Arena-operated workshop**, not an autonomous external model service. Read README.md and workshop/agent-runbook.md before a run.

- Work only on the branch assigned to the current Arena session. Inspect git status and all existing files first. Preserve `lol.md` and unrelated user content.
- Make exactly one new finished science-based What If? Short per run, normally 50–60 seconds. Never stop at plans, images, or HTML.
- Use official HyperFrames for scene composition, deterministic animation and final rendering. Read the four core official skills. Use documented CLI commands; verify `--help` when uncertain.
- Use local Kokoro through `npx hyperframes tts`, male English voice; free Edge TTS only if Kokoro fails. Verify actual audio. The optional q8 cache workaround is explicit and version-gated; don't present it as stock full-precision Kokoro.
- Use Arena native image generation as primary image source. No image API keys or external image models. Prefer scene-specific vertical images with no embedded text; save prompts and attribution.
- Scientific premise and claims must be defensible and cited to credible primary/institutional references. Explicitly mark impossible assumptions and conditional inferences. Never invent dates, papers, cooling timelines, survival promises, or trend metrics.
- No paid APIs, paid catalogs, subscriptions, billing, or provider auto-selection. No invented channel name, logo, brand intro or subscribe reminder.
- License every downloaded asset, including music. Verify the author's terms rather than trusting mirrors. Preserve required music attribution in the publishing description.
- Derive captions from actual audio timing; use phrase captions for explanation and word-level emphasis where genuine timing is available. Keep captions in Shorts safe zones.
- Keep files understandable: one visual scene per sub-composition, one captions track, assets local, fonts vendored. Arena should edit the creative mappings; don't build a dashboard, database, separate inference service, or a generic video SaaS.
- Mandatory gates: HyperFrames check/snapshot, real render, independent ffprobe, complete decode, decoded-frame review, audio measurements, all nine output files, tests. Fix failures and rerender. Do not claim human listening when audio was only measured.
- Keep model caches, node_modules and temporary frame sequences out of Git. Preserve reusable current assets and phrase takes needed for reproducibility. Record cleanup paths; no hard reset, indiscriminate git clean, force push or deletion of unrelated files.
- Commit the actual MP4 and package to the current branch, push only that branch, open a PR without merging. Verify tracking, dimensions, codecs and file size before claiming delivery.
