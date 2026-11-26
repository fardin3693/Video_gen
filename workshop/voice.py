"""Synthesize editorial phrases with the official HyperFrames Kokoro CLI.
Existing takes are reused only when their saved text, speed and voice match.
"""
import json, os, subprocess, pathlib, wave
ROOT=pathlib.Path(__file__).resolve().parents[1]
episode=json.loads((ROOT/'workshop/episode.json').read_text())
manifest=ROOT/'workshop/voice-takes.json'
cached=json.loads(manifest.read_text()) if manifest.exists() else {}
env=os.environ.copy()
python=ROOT/'.venv/bin/python'
env.setdefault('HYPERFRAMES_PYTHON',str(python) if python.exists() else os.path.expanduser('~/.venvs/kokoro/bin/python'))
for i,s in enumerate(episode['sections']):
    dst=ROOT/f'film/assets/voice/{i:02d}.wav'; dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists():
        old=cached.get('sections',[])
        if i>=len(old) or any(old[i].get(k)!=s.get(k) for k in ['text','speed']) or cached.get('voice')!=episode['voice']:
            raise RuntimeError(f'Stale/unverified take {dst.name}: archive or remove this identified derived take before regenerating.')
    else:
        cmd=[str(ROOT/'node_modules/.bin/hyperframes'),'tts',s['text'],'-v',episode['voice'],'-s',str(s['speed']),'-o',str(dst),'--json']
        p=subprocess.run(cmd,env=env,text=True,capture_output=True,cwd=ROOT)
        print(i,p.stdout.strip(),p.stderr.strip(),flush=True)
        if p.returncode or not dst.exists():
            raise RuntimeError(f'TTS failed for section {i}; no fallback engine is selected automatically.')
    with wave.open(str(dst)) as w:
        s['rawDuration']=w.getnframes()/w.getframerate()
    s['audio']=f'assets/voice/{i:02d}.wav'
    # Persist verified partial progress so an interrupted synthesis can resume.
    progress=dict(episode);progress['sections']=episode['sections'][:i+1]
    manifest.write_text(json.dumps(progress,indent=2)+'\n')
manifest.write_text(json.dumps(episode,indent=2)+'\n')
print('Total speech:',sum(s['rawDuration'] for s in episode['sections']))
print('Total pauses:',sum(s['pause'] for s in episode['sections']))
