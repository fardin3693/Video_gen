# ytb-research-skills

Skills and tools that turn Claude Code (or Antigravity / Gemini) into a YouTube research partner. It watches and breaks down other videos, pulls transcripts, analyzes channels, finds what's working in your niche this week, grabs thumbnails and writes scripts in your voice.

Everything runs on your computer and is free. You only need a free YouTube API key for view counts and channel stats.

## What's inside

**Skills** (`.claude/skills/`)
| Skill | What it does |
|---|---|
| `research` | Drop a video, channel or playlist link: adds a row to your ideas table in Canva (title, thumbnail, views, outlier score, link) and saves the thumbnail |
| `analyse` | Research breakdown of one video in its own Canva doc (cover, summary, timestamped breakdown table, takeaways), linked from that video's row in your ideas table |
| `about-me` | Interviews you once so Claude always knows who you are, your goals, your audience and how you talk |
| `bullseye` | Maps your audience from your exact niche to the broadest one, and sets your weekly content mix |
| `channel-analysis` | Full report on any channel: which topics, hooks and formats win and why |
| `outlier-pulse` | Daily list of competitor videos that beat their channel's average |
| `breakout-detector` | Finds the exact video where a channel blew up and what changed |
| `hook-machine` | Builds a hook rubric from real winning videos, then writes or grades hooks |
| `script` | Writes and fixes scripts so they sound like you and hold viewers |
| `study` | Paste reel / TikTok / YouTube links: gets the exact script, hook, structure and ideas |
| `video-breakdown` | Watches a whole video frame by frame and explains why it worked |

**Tools** (`tools/`)
| Tool | What it does |
|---|---|
| `yt.py` | YouTube stats, channel scans with outlier scores, comments, search, transcripts, and `watch` (downloads a video, saves frames + contact sheets so the AI can *see* it) |
| `reel_fetch.py` | Same for Instagram Reels and TikTok: video, audio, frames, contact sheet, likes and views |
| `thumbs.py` | Downloads thumbnails for a video, a playlist or a whole channel |
| `script_check.py` | Checks a script: length, part timings, weak openers, AI-sounding phrases, long sentences |

## Setup (about 10 minutes)

1. Install **Python 3.10+**, **FFmpeg** and **Claude Code** (or Antigravity).
   - Windows: `winget install Gyan.FFmpeg` · Mac: `brew install ffmpeg`
2. Get the repo and install the Python packages:
   ```bash
   git clone https://github.com/Mohcen56/youtube-research-skills
   cd youtube-research-skills
   pip install -r requirements.txt
   ```
3. Optional but recommended: a free YouTube API key for views, channels and comments (transcripts and `watch` work without it). Follow [tools/YT_API_KEY_SETUP.md](tools/YT_API_KEY_SETUP.md). The key goes in `tools/.env`, which is never uploaded.
4. Open the folder in Claude Code and say: **"run the about me interview"**.

**Antigravity / Gemini:** copy the skills to the folder it reads, and tell it to read `GEMINI.md` first:
```bash
cp -r .claude/skills .agents/skills
```

## Try it

```bash
python tools/yt.py watch https://youtu.be/VIDEO_ID
python tools/yt.py transcript https://youtu.be/VIDEO_ID
python tools/yt.py channel @somechannel --days 90
python tools/reel_fetch.py https://www.instagram.com/reel/XXXX/
python tools/thumbs.py https://www.youtube.com/@somechannel/videos --max 20
python tools/script_check.py my_script.md
```

Or just talk to Claude: *"research this <link>"*, *"analyse this <link>"*, *"analyze @somechannel"*, *"what's working in my niche this week"*, *"study these 5 reels"*, *"why did this video blow up?"*, *"write a script about X"*, *"is this hook good?"*

## Your ideas table in Canva (optional)

`research` and `analyse` write to Canva, so connect the Canva connector/plugin in Claude Code or Antigravity first. The first time, give it your ideas doc link, or let it create a new doc called "Video ideas". It saves the link in `brand/ideas_doc.md` and fills the same doc every time after that. Without Canva, the table is kept in `research/ideas_table.md`.

## Hear the sound (optional)

Claude can't hear audio on its own. [earshot](https://github.com/Leonxlnx/earshot) by Leon Lin (MIT) gives it ears. Install it from its repo, add it to Claude Code as an MCP server, and copy its `skills/earshot` folder into `.claude/skills/`. The `video-breakdown` skill uses it to check the sound of a video it studies.

## Rules the skills follow
- Your own words stay yours: Claude fixes grammar, never rewrites your lines without asking.
- It asks when unsure instead of guessing, and never invents numbers.
- Other creators' videos are downloaded only to study them. Ideas can be borrowed, wording and clips can't.

## License
MIT, see [LICENSE](LICENSE).
