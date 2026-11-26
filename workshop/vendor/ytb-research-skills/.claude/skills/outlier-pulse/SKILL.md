---
name: outlier-pulse
description: Give the creator a daily ranked list of competitor videos that are beating their channel's average (outliers), so they never have to scroll for research. Use when the creator asks "what's working in my niche", "outlier pulse", "what did competitors post", or wants a daily or weekly research feed.
---

# Outlier video pulse

## Watch list
`brand/about_me/competitors.md`: one channel per line (name, handle or ID, why it's relevant, long or short). If it's short, suggest new channels found in step 3 and let the creator approve them.

## Run (with `tools/yt.py`, needs the API key in `tools/.env`)
1. For each channel: `python tools/yt.py channel <id|@handle> --days 90 --json`. The outlier × is computed against the 90-day median; keep only videos from the **last 7 days** (changeable).
2. **Outlier mode (default):** keep videos with ≥ 25,000 views OR outlier ≥ 1.5× (thresholds are changeable). **All-recent mode:** keep everything.
3. Discovery: `python tools/yt.py search "<keyword>" --days 7` for the niche keywords in `brand/about_me/who_i_am.md`. Each search costs 100 of the 10,000 free daily units, so max ~5 per run. Videos with high views per subscriber are outliers from channels not on the list: mark them "new channel".
4. Sort by outlier ×. For each: title, channel, views, outlier ×, age, link, and one line on *why it might be working* (topic, hook or format, from the title and thumbnail). Deep analysis only if asked.
5. If the key is missing or quota runs out, say so and list what was checked.

## Output
- A short table in chat, newest run on top in `research/outlier_pulse.md` (keep the last 14 runs).
- Mark ideas that fit the bullseye (`brand/about_me/bullseye.md`) with their ring number.

## Scheduling
Only if the creator asks: set a scheduled task (for example daily 07:00) that runs this skill. Never schedule on your own.
