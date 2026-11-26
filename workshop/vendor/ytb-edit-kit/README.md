<p align="center">
  <img src="assets/banner.png" alt="ytb-edit-kit: edit your videos in code" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-F2C200?style=flat-square&labelColor=16171B" alt="MIT license">
  <img src="https://img.shields.io/badge/works%20with-Claude%20Code-F4F4F2?style=flat-square&labelColor=16171B" alt="Claude Code">
  <img src="https://img.shields.io/badge/works%20with-Antigravity-F4F4F2?style=flat-square&labelColor=16171B" alt="Antigravity">
  <img src="https://img.shields.io/badge/renders%20with-HyperFrames-F4F4F2?style=flat-square&labelColor=16171B" alt="HyperFrames">
</p>

<p align="center">
  <b>Give it your voiceover. Get back a finished YouTube edit, in your own style.</b><br>
  Skills and tools that let Claude Code or Antigravity edit your videos in code: real screens, b-roll, GIFs, charts, diagrams and sound effects, every one landing on the word you say.
</p>

---

## ✦ How it works

| | Step | What happens |
|:-:|---|---|
| **1** | **Your style** | Say *"build my design system"*. It asks you a few questions (colours, fonts, captions, sound, pace) and saves your answers. Every video after follows them. |
| **2** | **Your voiceover** | Drop your take and your screenshots or clips in, and say *"edit this video"*. It times every word. |
| **3** | **Storyboard first** | You get one still per shot before anything renders. Change what you don't like. |
| **4** | **Render + self-check** | It renders with HyperFrames, then looks at its own frames and re-listens to the result before handing it over. |
| **5** | **It learns** | Every note you give (*"no text on b-roll"*) is saved as a dated rule, so the next edit already follows it. |

> **Already made your brand** (with another grill-me skill, a style guide, notes)? It finds it in your project and uses it. You won't be asked twice.
>
> **No design system yet?** It suggests building one first (about 10 minutes). Say no and it edits in a clean neutral look you can replace any time.

## ✦ What it can put on screen

Word screens · real website and app screens with markers · full-screen b-roll · GIFs and memes · versus cards · bars and gauges · flow and node diagrams · maps · re-created chats and terminals. All recoloured to your brand. See every shot type in [KINDS.md](tools/edit_kit/KINDS.md).

## ✦ Install

**1. Install these first**
- **Python 3.10+** and **FFmpeg** (Windows: `winget install Gyan.FFmpeg` · Mac: `brew install ffmpeg`)
- **Claude Code** or **Antigravity**
- **HyperFrames**, the free engine that renders the edits, from its source: **[github.com/heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)**. Follow its own setup. This kit doesn't install it for you.

**2. Get the kit**
```bash
git clone https://github.com/Mohcen56/ytb-edit-kit
cd ytb-edit-kit
pip install -r requirements.txt
```

**3. Start**

Open the folder in Claude Code and say:
```
build my design system
```

**Using Antigravity?** Copy the skills to the folder it reads, and tell it to read `GEMINI.md` first:
```bash
cp -r .claude/skills .agents/skills
```

## ✦ Your first edit

1. Add your own sound effects to `sfx/` (names and tips in [sfx/README.md](sfx/README.md)).
2. Say **"edit this video"** and give it your voiceover and your files.
3. Check the storyboard, give notes, get your MP4.

<details>
<summary><b>Prefer running it by hand?</b></summary>

```bash
python tools/edit_kit/new_video.py videos/my_video        # then put voice.mp3 in videos/my_video/audio/
cd videos/my_video/audio && python ../../../tools/transcribe.py voice.mp3 && python ../../../tools/tighten.py && cd ../../..
python tools/edit_kit/build.py videos/my_video             # after writing videos/my_video/shots.py
python tools/edit_kit/storyboard.py videos/my_video        # one still per shot, check before rendering
cd videos/my_video/project && npx hyperframes render . -o ../renders/my_video_v01.mp4
```
Only want captions for CapCut, Premiere or DaVinci? `python tools/captions.py words_tight.json captions` makes `.srt` + `.ass`.
</details>

## ✦ What's inside

**Skills** (`.claude/skills/`)
| Skill | What it does |
|---|---|
| `design-system` | Asks you questions, with visual previews, until you have your own colours, fonts, captions, sound and editing rules |
| `edit` | Edits your video from your voiceover: storyboard first, then render, then it checks its own work |
| `about-me` | Interviews you once so Claude always knows who you are, your audience and how you talk |

**Tools** (`tools/`)
| Tool | What it does |
|---|---|
| `transcribe.py` | Word-by-word timing of your voiceover (local Whisper) |
| `tighten.py` | Cuts long pauses and breaths, evens the loudness |
| `captions.py` | `.srt` and styled `.ass` captions in your colours and font |
| `gif2mp4.py` | Turns a GIF into a clean clip of a set length |
| `edit_kit/` | The engine: `new_video.py`, `build.py`, `storyboard.py`, `final_check.py` |

## ✦ Optional: let it hear

Claude can't hear audio on its own. [earshot](https://github.com/Leonxlnx/earshot) by Leon Lin (MIT) gives it ears: it picks sound effects, checks your mix and lines sound up with cuts. Install it from its repo, add it as an MCP server, and copy its `skills/earshot` folder into `.claude/skills/`.

## ✦ Rules it follows

- **Your words stay yours.** On-screen text uses your exact script words.
- **It asks instead of guessing** when a line, a file or a shot is unclear.
- **Only media you have the rights to:** your recordings, your screenshots, free stock, your own sound effects.

## ✦ Also free

**[ytb-research-skills](https://github.com/Mohcen56/ytb-research-skills)**: drop a YouTube link and it fills your ideas table, breaks videos down, finds outliers in your niche and helps write your scripts.

---

<p align="center">MIT license · see <a href="LICENSE">LICENSE</a></p>
