# Heart short production source

All paths below are relative to the repository root. The original Arena-generated narration takes and converted open-source typefaces are in `assets/`; the nine scene functions are in `scenes.py`. `bpm_clock.py` is the shared beat schedule for the visualizations and sound. Caption timing is approximate, not forced alignment.

Rebuild on a Linux x64 machine with Python 3.11 and Node:

```sh
python3 -m venv .venv
.venv/bin/pip install pillow==13.0.0 numpy==2.4.6 scipy==1.17.1 aggdraw==1.4.1 imageio-ffmpeg==0.8.1
mkdir -p build/npm out
npm install --prefix build/npm @ffprobe-installer/ffprobe@2.1.2
.venv/bin/python src/audio_gen.py
.venv/bin/python src/render.py
F=$(.venv/bin/python -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')
"$F" -y -i out/preview.mp4 -vf 'scale=1080:1920:flags=lanczos' \
  -c:v libx264 -preset veryfast -profile:v high -pix_fmt yuv420p -r 30 \
  -b:v 12M -minrate 12M -maxrate 12M -bufsize 24M \
  -x264-params 'nal-hrd=cbr:force-cfr=1:threads=2' \
  -c:a copy -movflags +faststart out/final_heart_5x_short.mp4
```

The output is intentionally upscaled from the 540×960 procedural master. It is not a native-resolution render. The rendering script uses frame-by-frame Pillow rather than a browser, Blender or HyperFrames. The `build/` directory is disposable; it contains generated waveforms, timing data, stills and installed local tools.
