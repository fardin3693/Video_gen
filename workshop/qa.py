"""Validate the actual delivery MP4; save compact, independently reproducible evidence."""
import pathlib, subprocess, json, re, hashlib, io, os
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFont
R=pathlib.Path(__file__).resolve().parents[1]; O=R/'output'; Q=O/'qa';Q.mkdir(exist_ok=True)
V=O/'final_video.mp4'
def run(args): return subprocess.run(args,capture_output=True,check=True).stdout
j=json.loads(run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(V)])); (Q/'ffprobe.json').write_text(json.dumps(j,indent=2)+'\n')
v=next(s for s in j['streams'] if s['codec_type']=='video');a=next(s for s in j['streams'] if s['codec_type']=='audio')
assert v['width']==1080 and v['height']==1920 and v['codec_name']=='h264' and v['avg_frame_rate']=='30/1'
assert a['codec_name']=='aac' and 50<=float(j['format']['duration'])<=60
p=subprocess.run(['ffmpeg','-hide_banner','-v','error','-i',str(V),'-f','null','-'],capture_output=True,check=True)
(Q/'decode-errors.txt').write_bytes(p.stderr); assert not p.stderr
p=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-af','loudnorm=I=-16:TP=-1.5:LRA=9:print_format=json','-vn','-f','null','-'],capture_output=True,check=True,text=True)
m=re.search(r'\{\s*"input_i"[\s\S]*?\}',p.stderr); assert m
loud=json.loads(m[0]); (Q/'loudness.json').write_text(json.dumps(loud,indent=2)+'\n')
assert -18<float(loud['input_i'])<-13 and float(loud['input_tp'])<0
# Detect unexpected fully black intervals; a dark but legible scene is intentional.
p=subprocess.run(['ffmpeg','-hide_banner','-i',str(V),'-vf','blackdetect=d=0.08:pix_th=0.03','-an','-f','null','-'],capture_output=True,check=True,text=True)
black=[l for l in p.stderr.splitlines() if 'black_start:' in l]; assert not black,black
# Decode the final AAC and original master to the same PCM clock, verify A/V mux
# didn't introduce a significant offset (downsampled correlation over first 5 sec).
def pcm(path): return np.frombuffer(run(['ffmpeg','-v','error','-i',str(path),'-vn','-ac','1','-ar','8000','-f','f32le','-']),dtype='<f4')
x=pcm(V);y=pcm(R/'film/assets/audio/master.m4a')
lo,hi=2000,40000
scores=[]
for lag in range(-240,241):
 xx=x[lo+lag:hi+lag]; yy=y[lo:hi]
 scores.append(float(np.dot(xx,yy)/(np.linalg.norm(xx)*np.linalg.norm(yy)+1e-12)))
lag=int(np.argmax(scores))-240
assert abs(lag/8000)<.04
# Actual frames, not source mockups.
times=[0,.8,4,8,11.4,14,20,22,25,30,35,40,45,50,53.9]
thumbs=[]
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
for t in times:
 b=run(['ffmpeg','-v','error','-ss',str(t),'-i',str(V),'-frames:v','1','-vf','scale=216:384','-f','image2pipe','-vcodec','png','-'])
 im=Image.open(io.BytesIO(b)).convert('RGB'); panel=Image.new('RGB',(216,410),'#13212a');panel.paste(im,(0,26));ImageDraw.Draw(panel).text((8,6),f'{t:.2f}s',fill='white',font=ImageFont.truetype(font,14));thumbs.append(panel)
sheet=Image.new('RGB',(216*5,410*3),'#13212a')
for i,im in enumerate(thumbs):sheet.paste(im,((i%5)*216,(i//5)*410))
sheet.save(Q/'decoded-frames.jpg',quality=88)
# Motion check: consecutive one-second thumbnails must not all be identical.
b=run(['ffmpeg','-v','error','-i',str(V),'-vf','fps=1,scale=108:192','-pix_fmt','rgb24','-f','rawvideo','-'])
frames=np.frombuffer(b,dtype=np.uint8).reshape(-1,192,108,3).astype(np.float32)
diffs=np.mean(abs(np.diff(frames,axis=0)),axis=(1,2,3))
assert np.all(diffs>.01),diffs
# Check all narration phrases are non-silent, using the actual per-phrase ranges.
t=json.loads((R/'workshop/timeline.json').read_text())
phrase_rms=[]
for s in t['sections']:
 seg=x[round(s['start']*8000):round(s['end']*8000)]
 rms=float(np.sqrt(np.mean(seg**2))); assert rms>.004
 phrase_rms.append(round(float(20*np.log10(rms)),2))
result={'passed':True,'duration':float(j['format']['duration']),'resolution':[v['width'],v['height']],'fps':v['avg_frame_rate'],'frames':int(v['nb_frames']),'videoCodec':v['codec_name'],'audioCodec':a['codec_name'],'fileBytes':V.stat().st_size,'sha256':hashlib.sha256(V.read_bytes()).hexdigest(),'decodeErrors':0,'blackIntervals':black,'integratedLUFS':float(loud['input_i']),'truePeakDBTP':float(loud['input_tp']),'masterVsRenderedOffsetSeconds':lag/8000,'masterVsRenderedCorrelation':max(scores),'minimumOneSecondFrameDifference':float(diffs.min()),'speechPhrasesChecked':len(phrase_rms),'phraseRangeRMSdBFS':phrase_rms,'captionSyncMethod':'Actual generated phrase PCM sample boundaries; individually generated revelation word boundaries. No forced-alignment claim.','reviewLimitation':'Programmatic audio analysis, not human listening. Visual decoded frames are reviewed separately by Arena.'}
(Q/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
# Every required package file must exist when --complete is requested.
if '--complete' in __import__('sys').argv:
 required=['final_video.mp4','thumbnail.jpg','script.md','subtitles.srt','description.md','sources.md','asset-credits.md','storyboard.md','production-report.md']
 for name in required: assert (O/name).stat().st_size>0,name
 print('Publishing package: all 9 required files exist.')
