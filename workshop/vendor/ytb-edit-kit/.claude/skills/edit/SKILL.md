---
name: edit
description: Edit a long YouTube video (or a reel) in code from the creator's voiceover - word screens, website and app screens with markers, b-roll, GIFs and memes, versus cards, bars, gauges, flows, node diagrams, maps, re-created chats and terminals - in their own design system, rendered with HyperFrames. Use when the creator says "edit this video", "make the edit", "build the video", or drops a voiceover and assets for a new video.
---

# Edit a video

Engine: [HyperFrames](https://github.com/heygen-com/hyperframes) (HTML → MP4, run with `npx hyperframes`). The kit in `tools/edit_kit/` writes the HyperFrames project; you never hand-write the HTML. HyperFrames and its own skills are installed by the creator from the source ([github.com/heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)); this kit never installs them. If `npx hyperframes` or its skills are missing, stop and send the creator to that link. With earshot installed, use it to pick sound effects and check the final mix.

## Before anything
1. **Design system check.** If `brand/design.json` doesn't exist, first look for a brand they already made elsewhere in the project (the "find a brand they already made" steps in the `design-system` skill). If one is found, import it and carry on with the edit; never ask them to do the grill again. Only if nothing is found, stop and suggest it before editing: *"You don't have a design system yet, so this edit would use the kit's neutral default look (off-white, black text, one blue accent). Want to build yours first? It takes about 10 minutes and every video after uses it."* Then:
   - **Yes** → run the `design-system` skill, then come back to the edit.
   - **No** → edit in the neutral default (`build.py` uses it automatically) and remind them once at the end that `build my design system` makes it theirs.
   With a design system, every colour and font comes from it.
   Check `sfx/` has a file for each sound the shots use; if some are missing, tell the creator before building (the edit would have no sound there).
2. Read the script and ask what's unclear (which screen a line means, which file, what text). Never guess: ask with options.
3. Gather the assets with the creator: screenshots and screen recordings of the real thing they talk about, b-roll, GIFs, logos. If a folder has nothing fitting, say what to search for or record. Only use files they have the rights to.

## Steps
1. `python tools/edit_kit/new_video.py videos/<name>` → put the voiceover in `audio/voice.mp3`, files in `assets/`.
2. Word timings: `cd videos/<name>/audio && python ../../../tools/transcribe.py voice.mp3 ../script.txt`, then `python ../../../tools/tighten.py` (cuts long pauses, evens loudness).
3. Write `videos/<name>/shots.py`: one shot per visual change, kinds and options in `tools/edit_kit/KINDS.md`.
4. `python tools/edit_kit/build.py videos/<name>`: read its warnings and fix them.
5. **Beat plan first:** `python tools/edit_kit/storyboard.py videos/<name>` and show the creator `storyboard/storyboard.jpg` (one still per shot with its words). Wait for their go. Change shots they flag, rebuild, show again.
6. Render: `cd videos/<name>/project && npx hyperframes check && npx hyperframes render . -o ../renders/<name>_v01.mp4`. Never overwrite a render: bump v02, v03.
7. **Check the render yourself before showing it:** make a contact sheet of frames (ffmpeg, about one per second) and look at it, then run `python tools/edit_kit/final_check.py videos/<name> videos/<name>/renders/<name>_v01.mp4` (re-transcribes the render: no sound may hide a word; prints loudness). Fix, re-render, then hand it over with what changed.

## Default rules (the creator can change any of them in brand/design.md)
**Pace and structure**
- Something new on screen every 2-3 s. No dead time, no shot over ~4.5 s unless it's a screen recording that shows an action.
- A new beat in the voice gets a new visual. Reveals wait for the voice: every graphic lands on its word (the kit snaps to word onsets).
- Visuals are literal: show the exact thing the line says (the real page, the real app, the real number). Only real names, dates and numbers on screen.
- On-screen text uses the creator's exact script words, never a paraphrase. Big-word screens are rare (3-4 per video).
- The hook shows the result or the problem in the first seconds. No intro card.

**Screens**
- Show whole windows, not tight crops. One smooth zoom in, hold, zoom out per shot, never slow drifting zooms.
- Screenshots stay still unless a move is planned.
- One marker per screen, only on the exact thing the line names.
- Mix framed and full screen: framed when an action must read, full screen for mood.

**B-roll, GIFs, memes**
- No text on b-roll: full-screen b-roll plays clean, with no captions, stamps or labels on top. If a line needs words on screen, give it its own shot.
- B-roll full screen unless the quality suffers. The same clip at most twice per video (another angle counts as new).
- GIFs sit straight (no 3D tilt). Never stretch a short GIF to fill a slot: chain another one.
- Captions under memes use the creator's words.

**Explainers**
- Never the same chart type in two shots in a row. Bars and meters: real numbers only.
- Diagrams show only what the line says; one idea per diagram.
- Maps: the hub shows the whole video with the current item in focus; give other levels their own layout (flow, nodes).

**Sound**
- Follow the music rule in `brand/design.md`.
- A sound only where something visibly changes, under the voice, one at a time, never stacked (the kit enforces a 0.35 s gap). Only the creator's own files in `sfx/` (names: click, whoosh, pop, ding, typing, error, hit, boom, scratch).

**Never**
- Flashy preset transitions (spins, glitches, star wipes), shaky cam, flashing, more than one animated element entering at once.
- Clips cut from another creator's video.

## After the creator's notes
Write each note they give as a dated rule in `brand/design.md` (so the next edit starts with it), then rebuild only what changed.
