---
name: study
description: Study a batch of reels, TikToks or YouTube videos - extract the exact script, on-screen text, hook, structure and idea, find what worked, and save lessons. Use when the creator pastes links and says "check these", "learn from these", or "extract the ideas/scripts". Works in Claude Code and in Antigravity/Gemini.
---

# study: learn from videos

## 1. Get each video (no guessing)
- **Instagram / TikTok:** `python tools/reel_fetch.py <link> <link> ...` saves `research/reels/<id>/` with `video.mp4`, `audio.mp3`, `frames/` (1 per second), `contact.jpg` and `meta.json` (likes, comments, views if public, caption, date).
- **YouTube:** `python tools/yt.py watch <url>` (captions + frames in `research/<id>/`) and `python tools/yt.py video <url>` for views, likes and comments.
- If a download fails, list the failed links and go on with the rest. Never use other sites or log-in tricks.
- Skip duplicate links (same id).

## 2. Watch it, then write `notes.md` in the video's folder
Listen to `audio.mp3` (or read the transcript) and look at the frames or contact sheet. Write:
- **TRANSCRIPT:** every spoken word, exactly, in the language spoken. Write `[unclear]` where you can't hear. Fix nothing: if a name sounds wrong, write what you hear and add `[Name?]` after it.
- **ON-SCREEN TEXT:** with timestamps.
- **HOOK:** first line or first visual, and why it stops the scroll.
- **STRUCTURE:** hook, setup, payoff, CTA, with timestamps.
- **EDITING:** cuts per 10 s, caption style, b-roll, zooms, sound effects, length.
- **IDEA:** the core idea in one plain sentence.
- **NUMBERS:** views (or likes + comments when views are hidden), date, account.
- **YOUR VERSION:** 3 ways the creator could make their own take for their audience (`brand/about_me/`). Never copy lines.

## 3. The batch summary
In `research/batches/<YYYY-MM-DD>_<short-name>/`:
- `ideas.csv` with columns `#,Idea,Video,Script,Likes,Comments,Views` (clean links: cut everything after `?`).
- `summary.md`: the 3 patterns the best ones share (hook type, length, format), ranked by numbers, plus the 5 best ideas for the creator.
- New lessons go to `research/lessons_proposed.md` (date, lesson, source). Only move them into `brand/` files when the creator says "lock it".
