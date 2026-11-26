import os, subprocess, json, wave, re
import numpy as np
from scipy.signal import butter, sosfilt
from bpm_clock import BEATS,bpm
import imageio_ffmpeg
F=imageio_ffmpeg.get_ffmpeg_exe(); SR=48000
texts=["What if your heart suddenly beat five times faster?", "At rest, it beats about seventy times a minute. Five times that is three hundred fifty.", "Speeding up is normal. Hard exercise can push a healthy young adult's heart to around one hundred ninety beats per minute.", "But at three hundred fifty, each beat lasts under two-tenths of a second. The chambers barely have time to refill between beats.", "Faster doesn't mean more blood. With less filling, each beat pushes out less, and blood pressure drops.", "Your brain notices first. Dizziness, tunnel vision, and fainting could follow within seconds.", "Worse: the heart feeds itself while relaxing. Now it barely does, and its rhythm can collapse into chaos.", "A hummingbird's heart can top one thousand beats a minute, but it's built for it. Yours isn't.", "Your heart doesn't just beat. It keeps time. Follow for more what-ifs."]
starts=[.4,4.2,10.3,17.3,25.3,32.4,39.3,47.4,55.2]
windows=[3.45,5.55,6.4,7.45,6.45,6.3,7.35,7.35,4.65]
probe='build/npm/node_modules/@ffprobe-installer/linux-x64/ffprobe'
voice=np.zeros(SR*60,dtype=np.float32); timings=[]; details=[]
for i,(text,start,win) in enumerate(zip(texts,starts,windows),1):
    path=f'assets/vo{i}.wav'
    dur=float(subprocess.check_output([probe,'-v','error','-show_entries','format=duration','-of','csv=p=0',path]))
    tempo=max(1.,dur/win)
    out=f'build/fit{i}.wav'
    subprocess.run([F,'-y','-loglevel','error','-i',path,'-af',f'atempo={tempo:.6f},highpass=f=80,acompressor=threshold=0.12:ratio=2:attack=10:release=100','-ar',str(SR),'-ac','1','-c:a','pcm_s16le',out],check=True)
    with wave.open(out) as w: a=np.frombuffer(w.readframes(w.getnframes()),dtype='<i2').astype(np.float32)/32768
    # Speech from the service contains natural margins. Trim only leading/trailing silence.
    nz=np.flatnonzero(np.abs(a)>.006)
    if len(nz): a=a[max(0,nz[0]-240):min(len(a),nz[-1]+1200)]
    n=min(len(a),int(win*SR)); a=a[:n]; pos=int(start*SR); voice[pos:pos+n]+=a*.77
    # Approximate word timing, weighted by word length; not forced aligned.
    words=text.split(); weights=[max(2,len(re.sub(r'[^a-zA-Z]','',w)))**.65 for w in words]; total=sum(weights); cursor=start
    for word,weight in zip(words,weights):
        end=cursor+(n/SR)*weight/total; timings.append([cursor,end,word]); cursor=end
    details.append({'scene':i,'raw_seconds':dur,'atempo':tempo,'placed_seconds':n/SR,'start':start})
# original synthesized dark score and beat impacts
N=60*SR; tt=np.arange(N,dtype=np.float32)/SR
music=np.zeros(N,np.float32)
# dark drone, pulse, warm resolve; no sampled or copyrighted material
amp=np.interp(tt,[0,1.5,10,17,32,39,46.5,47,49,55,59,60],[.0,.095,.07,.09,.05,.075,.0,0,.055,.065,.06,0]).astype(np.float32)
music += amp*(.50*np.sin(2*np.pi*55*tt)+.22*np.sin(2*np.pi*82.41*tt)+.13*np.sin(2*np.pi*110.2*tt))
music += amp*.16*np.sin(2*np.pi*164.8*tt)*(.5+.5*np.sin(2*np.pi*.11*tt))
# duck continuous pad whenever narration is active, 9 dB
active=(np.abs(voice)>.001).astype(np.float32)
# smooth envelope over 150ms
kernel=np.ones(7200,dtype=np.float32)/7200
# efficient envelope via cumulative sum
cs=np.r_[0,np.cumsum(active,dtype=np.float64)]; k=7200; env=np.minimum(1,(cs[np.minimum(np.arange(N)+k,N)]-cs[np.arange(N)])/k*3).astype(np.float32)
music*=1-.645*env
sfx=np.zeros(N,np.float32); rng=np.random.default_rng(918)
for bt in BEATS:
    if 46.5<=bt<47: continue
    rate=bpm(bt); dur=.17 if rate>250 else .42; nn=int(dur*SR); x=np.arange(nn)/SR
    gap=min(.16, .4*60/rate)
    thump=np.sin(2*np.pi*55*x)*np.exp(-x*26)+.58*np.sin(2*np.pi*70*np.maximum(0,x-gap))*np.exp(-np.maximum(0,x-gap)*32)*(x>=gap)
    click=rng.normal(0,1,nn)*np.exp(-x*110)*.08
    vol=.085 if rate>250 else .16
    if 32<bt<39: vol*=.5
    if 47<bt<55: vol*=.35
    idx=int(bt*SR); end=min(N,idx+nn); sfx[idx:end]+=(thump[:end-idx]+click[:end-idx])*vol
# understated synthesized accents
for bt in [2.3,4,10,17,25,32,39,47,55]:
    n=int(.35*SR); x=np.arange(n)/SR; idx=int(bt*SR); sfx[idx:idx+n]+=(.045*np.sin(2*np.pi*(95*x-80*x*x))*np.exp(-x*9)).astype(np.float32)
# brief quiet wing hum, only in bird scene
mask=(tt>=47)&(tt<55); music[mask]+=.012*np.sin(2*np.pi*95*tt[mask])*(.5+.5*np.sin(2*np.pi*16*tt[mask]))
mix=voice+music+sfx
mix=np.clip(mix,-.96,.96)
stereo=np.stack([mix,mix],axis=1); pcm=(stereo*32767).astype('<i2')
with wave.open('build/mix.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
subprocess.run([F,'-y','-loglevel','error','-i','build/mix.wav','-af','loudnorm=I=-14:TP=-1.5:LRA=11','-ar','48000','-ac','2','-c:a','pcm_s16le','build/master.wav'],check=True)
with open('build/words.json','w') as f: json.dump(timings,f)
with open('build/audio_timing.json','w') as f: json.dump(details,f,indent=2)
def stamp(t):
    ms=round(t*1000); return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'
# Phrase SRT, using the same approximate word estimates as highlighted captions.
with open('out/captions.srt','w') as f:
    group=[]; idx=1
    for item in timings:
        if group and (len(group)>=6 or item[0]-group[-1][1]>.3):
            f.write(f'{idx}\n{stamp(group[0][0])} --> {stamp(group[-1][1])}\n'+ ' '.join(x[2] for x in group)+'\n\n'); idx+=1; group=[]
        group.append(item)
    if group: f.write(f'{idx}\n{stamp(group[0][0])} --> {stamp(group[-1][1])}\n'+ ' '.join(x[2] for x in group)+'\n\n')
print(json.dumps(details,indent=2))
