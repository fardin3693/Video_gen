---
name: research
description: Save YouTube videos to the creator's ideas table in Canva. One row per video with title, thumbnail file name, short description (channel, views, outlier score, views per hour) and link; the thumbnail is downloaded to research/thumbnails/. Use when the creator drops a video link, a channel or a playlist and says "research this", "add this to my ideas", "save this video", or just pastes links with no other ask. For a full breakdown of a video, use the `analyse` skill.
---

# Research: links → ideas table

The table is the only thing that goes to Canva. Everything else (stats, transcripts, frames) stays on the computer in `research/`.

## 1. Find the ideas doc
- Read `brand/ideas_doc.md`. If it has a Canva link, use that doc.
- If the creator gives a doc link in the message, use it and save it in `brand/ideas_doc.md` (replace the old one).
- If there is no link anywhere, create a new Canva doc called **"Video ideas"** with the table below, then save its link in `brand/ideas_doc.md` so next time it fills the same doc.
- No Canva connector connected? Say so, show where to connect it, and meanwhile keep the table in `research/ideas_table.md` (same columns).

`brand/ideas_doc.md` format:
```
# Ideas doc
Canva: <link>
Saved: <YYYY-MM-DD>
```

## 2. The table
| # | Title | Thumbnail | Short description | Link | Analysis |
|---|---|---|---|---|---|

- **#**: next number after the last row.
- **Title**: the exact video title.
- **Thumbnail**: the file name in `research/thumbnails/` (for example `dap2O7RdLAI.jpg`).
- **Short description**: `Channel (subs). Views. Outlier ×, VPH. One line on what the video is.` Example: `Chase AI (181K subs). 478K views. 10.1x outlier, 174 VPH. 3 steps to stop AI-slop websites.`
- **Link**: `https://youtu.be/<id>`
- **Analysis**: empty. The `analyse` skill fills it with the link to its doc.

If the doc's table is missing the Thumbnail or Analysis column, ask once before adding them. Never delete or reorder the creator's rows.

## 3. For each link
1. Stats: `python tools/yt.py video <url>` (views, publish date) and `python tools/yt.py channel <channel> --days 120` (subs, median, this video's **outlier ×**). *(needs the API key in `tools/.env`)*
2. **VPH** (views per hour) = views ÷ hours since publish, rounded. Add "(still growing)" if it's under a week old.
3. Thumbnail: `python tools/thumbs.py <url>` → `research/thumbnails/<id>.jpg`. A channel or playlist link: `python tools/thumbs.py <url> --max 30`, then ask which videos go in the table (best outliers first) before adding 30 rows.
4. The one-line description: from the title and thumbnail. Read the transcript (`python tools/yt.py transcript <url>`) only if the title doesn't make it clear.
5. Skip a video that's already in the table (same link) and say so.
6. Add the row(s), then reply with the doc link and a short list of what was added.

## Rules
- Never invent a number. No API key → leave views, outlier and VPH out and write "no stats (no API key)".
- If the video is too new or the channel too small for an outlier score, say "no outlier score" and give views ÷ subs instead.
- The API key never goes on screen, in chat or in Canva.
