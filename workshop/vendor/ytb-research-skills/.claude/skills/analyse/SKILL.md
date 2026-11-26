---
name: analyse
description: Full research breakdown of one YouTube video saved as its own Canva doc (cover banner, executive summary, timestamped breakdown table, summary table, key takeaways, conclusion), with the doc's link put in that video's row of the ideas table. Use when the creator says "analyse this", "analyze this video", "break this down" on a video link (for a chat-only breakdown with no doc, use `video-breakdown`), or asks to analyse a row that's already in the ideas table. Works with the `research` skill, which builds the table.
---

# Analyse: one video → one Canva doc, linked from the ideas table

## 1. Make sure the video has a row
- Find the ideas doc in `brand/ideas_doc.md` (see the `research` skill; if there is none, create it the way `research` does).
- If the video isn't in the table yet, run the `research` steps for it first (row + thumbnail).

## 2. Watch it, don't only read it
- `python tools/yt.py watch <url>`: frames every 2 s, contact sheets and transcript in `research/<id>/`. **Read every contact sheet in order** and line it up with the transcript, so the "Visual & Retention Strategy" column comes from what's really on screen.
- `python tools/yt.py video <url>` for views, length and date. *(needs the API key in `tools/.env`)*
- Sound: Claude can't hear by default. Infer it from transcript tags like [music] and say it's inferred.

## 3. The doc (this exact layout)
Create a Canva doc named **"YouTube Research Breakdown: <video title>"**, in this order:

1. **Cover banner** (full width, top of page 1): dark navy background, on the left small caps `YOUTUBE RESEARCH BREAKDOWN:`, then the video title in big bold caps with **one key word in blue**, a short blue line, and one subtitle line ("A structured analysis of …"). On the right, a simple picture of the video's main idea (a flow diagram or the 3 main points on cards). Make it with the image generator if one is available; if not, build it from shapes and text in Canva.
2. **Title**: `YouTube Research Breakdown: <video title>`, then one small line: `<channel> · <views> views · <length> · <link>`.
3. **EXECUTIVE SUMMARY**: one paragraph (4-6 sentences): the core thesis, what the video argues, and why it matters.
4. **COMPREHENSIVE STRUCTURED RESEARCH BREAKDOWN**: one table, one row per part of the video:
   | Timestamp | Section / Stage | Core Insight & Problem | Visual & Retention Strategy | Actionable Takeaway |
   - Timestamp as `[0:00 - 0:40]`, from the transcript. Cover the whole video, hook to outro.
5. **SUMMARY TABLE: <the video's main framework>**: a second table built around the video's own structure. Pick the columns that fit the video (for example a habits video: `Habit | Old Habit | New Habit | Implementation Tool`; a tools video: `Tool | What it does | Cost | When to use it`).
6. **KEY TAKEAWAYS & ACTION PLAN**: 4-6 numbered, short action lines.
7. **Conclusion**: 1-2 sentences.

Style: white page, black headings in bold caps, light grey table header row, thin grey lines between sections. No other colors except the banner's blue.

Then put the doc's link in the **Analysis** column of that video's row and reply with both links (analysis doc + ideas doc).

## 4. What stays local
Frames, contact sheets, the downloaded video and the full transcript stay in `research/<id>/`. Don't upload them to Canva. Short quotes only (under 15 words), and only when needed.

## Rules
- Never invent numbers, timestamps or facts; say what's missing (for example no API key).
- Ideas and structure can be borrowed. Wording and clips can't.
- Videos are downloaded only for private analysis.
