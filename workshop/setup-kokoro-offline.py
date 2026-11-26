"""Optional, explicit sandbox workaround for HyperFrames 0.9.98 only.
Uses Apache-2.0 Kokoro-82M q8 weights and the same 54 voice tensors from npm.
Does NOT bypass authentication or call a hosted TTS provider. It changes the
installed CLI's model integrity pins to the alternative files' verified hashes.
Normal environments should use the stock `npx hyperframes tts` download instead.
Run with a Python that has numpy: .venv/bin/python workshop/setup-kokoro-offline.py
"""
import pathlib, subprocess, tempfile, tarfile, hashlib, os, re, json, shutil
import numpy as np
R=pathlib.Path(__file__).resolve().parents[1]
MODEL_SHA='fbae9257e1e05ffc727e951ef9b9c98418e6d79f1c9b6b13bd59f5c9028a1478'
VOICE_SHA='774702d974ab0e2fda871948a17baa8f8b2e348e77e436c122b1be95c168e865'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
cache=pathlib.Path(os.environ.get('HYPERFRAMES_CACHE_DIR',str(pathlib.Path.home()/'.cache/hyperframes')))
model=cache/'tts/models/kokoro-v1.0.onnx';voices=cache/'tts/voices/voices-v1.0.bin'
model.parent.mkdir(parents=True,exist_ok=True);voices.parent.mkdir(parents=True,exist_ok=True)
if not (model.exists() and sha(model)==MODEL_SHA and voices.exists() and sha(voices)==VOICE_SHA):
 with tempfile.TemporaryDirectory(prefix='kokoro-npm-') as tmp:
  tmp=pathlib.Path(tmp)
  for package,folder in [('kokoro-q8-shards@1.0.0','weights'),('kokoro-js@1.2.1','voicepack')]:
   name=subprocess.check_output(['npm','pack',package,'--silent','--pack-destination',str(tmp)],text=True).strip().splitlines()[-1]
   dst=tmp/folder;dst.mkdir()
   with tarfile.open(tmp/name) as tar:
    # Extract only ordinary files below package/, never symlinks or traversal paths.
    for member in tar.getmembers():
     parts=pathlib.PurePosixPath(member.name).parts
     if member.isfile() and parts and parts[0]=='package' and '..' not in parts:
      target=dst.joinpath(*parts);target.parent.mkdir(parents=True,exist_ok=True)
      target.write_bytes(tar.extractfile(member).read())
  content=b''.join((tmp/f'weights/package/kokoro-q8.part{i}.bin').read_bytes() for i in range(6))
  assert hashlib.sha256(content).hexdigest()==MODEL_SHA
  model.write_bytes(content)
  data={p.stem:np.fromfile(p,dtype=np.float32).reshape(510,1,256) for p in sorted((tmp/'voicepack/package/voices').glob('*.bin'))}
  assert len(data)==54
  with voices.open('wb') as f:np.savez(f,**data)
assert sha(model)==MODEL_SHA and sha(voices)==VOICE_SHA,'Unexpected model/voice content; refuse to patch.'
cli=R/'node_modules/hyperframes';version=json.loads((cli/'package.json').read_text())['version'];assert version=='0.9.98',version
p=cli/'dist/chunk-Q2E472MZ.js';src=p.read_text()
old_model='bytes: 325532387,\n    sha256: "7d5df8ecf7d4b1878015a32686053fd0eebe2bc377234608764cc0ef3636a6c5"'
new_model=f'bytes: {model.stat().st_size},\n    sha256: "{MODEL_SHA}"'
old_voice='bytes: 28214398,\n  sha256: "bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d"'
new_voice=f'bytes: {voices.stat().st_size},\n    sha256: "{VOICE_SHA}"'
assert old_model in src or new_model in src,'Unknown CLI layout'
assert old_voice in src or new_voice in src,'Unknown voice pin layout'
src=src.replace(old_model,new_model).replace(old_voice,new_voice);p.write_text(src)
print('Seeded verified Kokoro-82M q8 / 54 voices and explicitly retargeted installed HyperFrames 0.9.98 pins.')
print('Next: HYPERFRAMES_PYTHON=<venv>/bin/python npx hyperframes tts "A real synthesis test." -v am_michael -o /tmp/tts-test.wav --json')
