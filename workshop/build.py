"""Build the editable HyperFrames film from verified phrase audio, never estimated WPM."""
import json, pathlib, wave, html, subprocess, math
R=pathlib.Path(__file__).resolve().parents[1]; F=R/'film'; O=R/'output'
e=json.loads((R/'workshop/voice-takes.json').read_text()); D=e['duration']; assert 50<=D<=60
cursor=.18; sr=24000; samples=bytearray(b'\0'*round(cursor*sr)*2)
for i,s in enumerate(e['sections']):
    with wave.open(str(F/s['audio'])) as w:
        assert w.getframerate()==sr and w.getnchannels()==1 and w.getsampwidth()==2
        audio=w.readframes(w.getnframes())
    s['start']=len(samples)/2/sr; samples.extend(audio); s['end']=len(samples)/2/sr
    samples.extend(b'\0'*round(s['pause']*sr)*2)
assert len(samples)/2/sr<D
samples.extend(b'\0'*(round(D*sr)*2-len(samples)))
with wave.open(str(F/'assets/audio/narration.wav'),'wb') as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes(samples)
scenes=[]
for s in e['sections']:
    if not scenes or scenes[-1]['id']!=s['scene']: scenes.append({'id':s['scene'],'start':s['start']})
scenes[0]['start']=0
for i,s in enumerate(scenes): s['end']=scenes[i+1]['start'] if i+1<len(scenes) else D
O.mkdir(exist_ok=True)
(R/'workshop/timeline.json').write_text(json.dumps(e|{'scenes':scenes},indent=2)+'\n')
def stamp(t):
    m=round(t*1000);return f'{m//3600000:02d}:{m//60000%60:02d}:{m//1000%60:02d},{m%1000:03d}'
(O/'subtitles.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(s["start"])} --> {stamp(s["end"])}\n{s["text"]}' for i,s in enumerate(e['sections']))+'\n')
(O/'script.md').write_text('# What if the Sun vanished?\n\n'+ ' '.join(s['text'] for s in e['sections'])+'\n\n## Editorial guardrails\nThe disappearance violates conservation of mass-energy: this is explicitly an impossible thought experiment, not a prediction or a solar explosion. The frozen landscape is a long-term illustrative outcome with no cooling deadline asserted. Survival means some microbial life could persist, not that all vent animals or humans would survive indefinitely.\n')
style='''@font-face{font-family:Inter;src:url('assets/fonts/Inter-400.woff2');font-weight:400}@font-face{font-family:Inter;src:url('assets/fonts/Inter-700.woff2');font-weight:700}@font-face{font-family:Editorial;src:url('assets/fonts/EBGaramond-700.woff2');font-weight:700}@font-face{font-family:Mono;src:url('assets/fonts/JetBrainsMono-400.woff2')}*{box-sizing:border-box}#root{position:absolute;inset:0;overflow:hidden;color:#f5f5ec;font-family:Inter} .photo{position:absolute;inset:-100px;width:1280px;height:2120px;object-fit:cover}.shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(2,9,15,.88),rgba(2,9,15,.72) 26%,transparent 45%,rgba(2,9,15,.42) 57%,#02090f 88%)}.kicker{position:absolute;left:142px;top:306px;color:#66e4e0;font:28px Mono;letter-spacing:5px}.heading{position:absolute;left:138px;top:364px;width:738px;font-size:88px;line-height:1.01;letter-spacing:-4px;font-weight:700;margin:0}.accent{color:#ffd383}.note{position:absolute;left:144px;top:968px;width:700px;font:28px Mono;color:#d9e7e9;line-height:1.5;background:rgba(2,9,15,.82);padding:8px 12px}.rule{position:absolute;left:144px;top:282px;width:60px;height:4px;background:#ffd383}.diagram{position:absolute;left:130px;top:566px;width:740px;height:470px}.detail{position:absolute;inset:0;pointer-events:none}.particle{position:absolute;width:4px;height:4px;border-radius:50%;background:#8bf3eb;opacity:.45}'''
# Registry sources are retained as editable snippets; their fade and caption recipes are adapted below.
def scene_file(s,i):
    name=s['id']; dur=s['end']-s['start']; custom=''; anim=''
    config={
      'cosmos':('sun-earth.jpg','WHAT IF?','THE SUN<br><span class="accent">VANISHED?</span>','An impossible thought experiment'),
      'city':('daylight-city.jpg','01 / THE DELAY','08<span class="accent">:</span>20','Approximate light-travel time'),
      'light':('sun-earth.jpg','02 / LIGHT IN FLIGHT','STILL ON<br>ITS WAY','Light already travelling keeps going'),
      'dark':('daylight-city.jpg','03 / THE BLACKOUT','DAYLIGHT<br><span class="accent">ENDS.</span>','No Sun. No new sunlight.'),
      'orbit':(None,'04 / THE PHYSICS','GRAVITY ISN’T<br><span class="accent">INSTANT.</span>','Simplified diagram · not to scale'),
      'heat':(None,'05 / STORED ENERGY','NOT AN<br>INSTANT FREEZE','Oceans + atmosphere store heat'),
      'ice':('frozen-world.jpg','06 / A COOLING WORLD','NO LIGHT.<br><span class="accent">LESS HEAT.</span>','Long-term illustration · no fixed timescale'),
      'vent':('vent-life.jpg','07 / THE TWIST','LIFE COULD<br><span class="accent">SURVIVE.</span>','Not all life depends on sunlight directly'),
      'microbes':('vent-life.jpg','08 / CHEMOSYNTHESIS','CHEMISTRY.<br>NOT SUNLIGHT.','Some microbes use chemical energy'),
      'core':(None,'09 / HEAT FROM WITHIN','EARTH HAS<br>ITS OWN HEAT','Residual heat + radioactive decay'),
      'ending':('vent-life.jpg','THE BIGGER PICTURE','A STAR ISN’T<br><span class="accent">ALL OF LIFE.</span>','Some life could persist · not a guarantee')}
    photo,kicker,title,note=config[name]
    if photo: custom+=f'<img id="{name}-photo" class="photo" data-layout-allow-overflow src="assets/{photo}" alt="Arena-generated scientific illustration"><div class="shade"></div>'
    else: custom+='<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,#123341,#02090f 68%)"></div>'
    if name=='dark': custom+='<div id="dark-veil" class="detail" style="background:#020b16;opacity:.82"></div>';anim+='tl.fromTo("#dark-veil",{opacity:.15},{opacity:.9,duration:.65},0);'
    if name=='orbit':
      custom+='''<svg class="diagram" viewBox="0 0 740 470" aria-label="Earth leaves a solar orbit along a tangent"><defs><radialGradient id="orbit-glow"><stop stop-color="#ffdf93"/><stop offset="1" stop-color="#bd752a"/></radialGradient></defs><circle cx="350" cy="215" r="160" fill="none" stroke="#628089" stroke-width="3" stroke-dasharray="8 10"/><circle id="orbit-sun" cx="350" cy="215" r="34" fill="url(#orbit-glow)"/><path id="orbit-path" d="M510 215 L510 440" stroke="#ffd383" stroke-width="5" fill="none" stroke-dasharray="225" stroke-dashoffset="225"/><circle id="orbit-earth" cx="510" cy="215" r="20" fill="#68e2e5"/><text x="100" y="215" fill="#c9dadd" font-size="28" font-family="Inter">Solar orbit</text></svg>'''
      anim+=f'tl.fromTo("#orbit-sun",{{opacity:1,scale:1,transformOrigin:"center"}},{{opacity:0,scale:.2,duration:.5}},2.8);tl.to("#orbit-path",{{strokeDashoffset:0,duration:3,ease:"none"}},{max(3,dur-4)});tl.to("#orbit-earth",{{y:215,duration:3,ease:"none"}},{max(3,dur-4)});'
    if name=='light':
      custom+='''<svg class="diagram" viewBox="0 0 740 470"><path d="M75 170 L655 345" fill="none" stroke="#ffd383" stroke-width="3" stroke-dasharray="12 14"/><circle id="light-dot" cx="75" cy="170" r="13" fill="#ffe6a1"/></svg>'''; anim+=f'tl.fromTo("#light-dot",{{x:0,y:0}},{{x:580,y:175,duration:{dur-.1},ease:"none"}},0);'
    if name=='heat':
      custom+='''<svg class="diagram" viewBox="0 0 740 470"><rect x="30" y="150" width="650" height="270" rx="12" fill="#12516c"/><path d="M30 150 Q110 125 190 150T350 150T510 150T680 150" fill="none" stroke="#6ee1e3" stroke-width="5"/><text x="75" y="100" fill="#c6dce3" font-size="30" font-family="Inter">Atmosphere</text><text x="75" y="275" fill="#d0eff0" font-size="38" font-family="Inter">Ocean: stored heat</text><g id="heat-arrows" stroke="#ffd383" stroke-width="5" fill="none"><path d="M460 340V190m-12 20 12-20 12 20 M540 340V190m-12 20 12-20 12 20 M620 340V190m-12 20 12-20 12 20"/></g></svg>'''; anim+=f'tl.fromTo("#heat-arrows",{{y:25,opacity:.4}},{{y:-20,opacity:1,duration:{dur-.1},ease:"none"}},0);'
    if name=='core':
      custom+='''<svg class="diagram" viewBox="0 0 740 470"><circle cx="360" cy="240" r="205" fill="#1c7389"/><path d="M360 35 A205 205 0 0 1 360 445 Z" fill="#c94e2f"/><path d="M360 80 A160 160 0 0 1 360 400 Z" fill="#ec9d47"/><path d="M360 145 A95 95 0 0 1 360 335 Z" fill="#ffe3a4"/><g id="core-rays" stroke="#ffd383" stroke-width="5"><path d="M580 200l48 -20 M580 260l55 0 M570 320l45 25"/></g></svg>''';anim+=f'tl.fromTo("#core-rays",{{x:0,opacity:.3}},{{x:18,opacity:1,duration:{dur-.1},ease:"none"}},0);'
    if name in ['orbit','heat','core']:
      custom=custom.replace('class="diagram"',f'id="{name}-diagram" class="diagram"')
      anim+=f'tl.fromTo("#{name}-diagram",{{scale:.97,transformOrigin:"center center"}},{{scale:1.045,duration:{dur},ease:"none"}},0);'
    if name in ['vent','microbes','ending']:
      for p in range(14):
        x=150+(p*127)%690;y=620+(p*83)%800
        custom+=f'<i id="{name}-p{p}" class="particle" style="left:{x}px;top:{y}px"></i>'
        anim+=f'tl.fromTo("#{name}-p{p}",{{y:0,x:0}},{{y:{-100-(p%4)*35},x:{(p%3-1)*18},duration:{dur},ease:"none"}},0);'
    if photo:
      motion=[(1.0,1.075,0,-28),(1.05,1.05,-30,30),(1.03,1.10,14,-20),(1.08,1.02,0,0),(1.0,1.05,-20,30)][i%5]
      a,b,x,y=motion;anim+=f'tl.fromTo("#{name}-photo",{{scale:{a},x:{x},y:0}},{{scale:{b},x:{-x},y:{y},duration:{dur},ease:"none"}},0);'
    # Fade-through registry incoming opacity recipe, adapted to .55 for a non-black cut.
    if photo: anim+=f'tl.fromTo("#{name}-photo",{{opacity:.55}},{{opacity:1,duration:.3,ease:"power2.out"}},0);'
    anim+='tl.fromTo("#'+name+'-copy",{y:22,opacity:0},{y:0,opacity:1,duration:.36,ease:"power2.out"},0);'
    doc=f'''<template><style>{style}</style><div id="root" data-composition-id="{name}" data-width="1080" data-height="1920">{custom}<div id="{name}-copy" class="scene-copy"><div class="rule"></div><div class="kicker">{kicker}</div><h1 class="heading">{title}</h1><div class="note">{note}</div></div></div><script>const tl=gsap.timeline({{paused:true}});{anim}window.__timelines["{name}"]=tl;</script></template>'''
    (F/f'compositions/{name}.html').write_text(doc)
for i,s in enumerate(scenes):scene_file(s,i)
# Phrase captions use the actual synthesized clip sample boundaries. Revelation words
# were synthesized individually, so their word arrivals have real audio boundaries.
caps=''; ca=''
for i,s in enumerate(e['sections']):
    txt=html.escape(s['text']);
    for key in ['Sun','nothing','gravity','light speed','freeze','heat','photosynthesis','cooling','chemical energy','sunlight','survive','Life']:
        txt=txt.replace(key,f'<em>{key}</em>')
    cls='word' if s.get('word') else ''
    caps+=f'<div id="caption-{i}" class="clip cap {cls}" data-start="{s["start"]:.6f}" data-duration="{s["end"]-s["start"]:.6f}"><span>{txt}</span></div>'
    ca+=f'tl.fromTo("#caption-{i} span",{{y:12,scale:1.025,opacity:0}},{{y:0,scale:1,opacity:1,duration:.10,ease:"power2.out"}},{s["start"]});'
captiondoc=f'''<template><style>{style}.cap{{position:absolute;left:140px;top:1080px;width:700px;text-align:left;color:#fff;font-size:48px;line-height:1.17;font-weight:700;overflow:visible}}.cap span{{display:inline-block;background:rgba(2,9,15,.88);padding:14px 20px;box-decoration-break:clone;border-left:4px solid #65e0dd}}.cap em{{font-style:normal;color:#ffd383}}.cap.word{{font-family:Editorial;font-size:86px}}</style><div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{caps}</div><script>const tl=gsap.timeline({{paused:true}});{ca}tl.to({{}},{{duration:{D}}},0);window.__timelines.captions=tl;</script></template>'''
(F/'compositions/captions.html').write_text(captiondoc)
hosts='\n'.join(f'<div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" data-start="{s["start"]:.6f}" data-duration="{s["end"]-s["start"]:.6f}" data-track-index="0" data-track-kind="graphics" data-width="1080" data-height="1920"></div>' for s in scenes)
(F/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"><title>What if the Sun vanished?</title><script src="assets/vendor/gsap.min.js"></script><style>*{{margin:0;box-sizing:border-box}}html,body{{width:1080px;height:1920px;overflow:hidden;background:#02090f}}#root{{position:relative;width:1080px;height:1920px}}#progress{{position:absolute;left:144px;top:1300px;width:660px;height:3px;background:#66e4e0;transform-origin:left center;opacity:.6;z-index:20}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="1080" data-height="1920" data-fps="30">{hosts}<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{D}" data-track-index="1" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:15"></div><div id="progress" aria-hidden="true"></div><audio id="master-audio" class="clip" src="assets/audio/master.m4a" data-start="0" data-duration="{D}" data-track-index="2" data-volume="1"></audio></div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});tl.fromTo('#progress',{{scaleX:0}},{{scaleX:1,duration:{D},ease:'none'}},0);window.__timelines.main=tl;</script></body></html>''')
# Audio mixing: narration triggers automatic music ducking; sparse effects follow picture cuts.
def start(scene): return next(s['start'] for s in scenes if s['id']==scene)
fx=f'''[0:a]asplit=2[voice][key];[1:a]volume=0.20[music];[music][key]sidechaincompress=threshold=0.015:ratio=6:attack=15:release=300[ducked];[2:a]volume=0.10,adelay={round(start('dark')*1000)}|{round(start('dark')*1000)}[hit];[3:a]volume=0.13,adelay={round(start('vent')*1000)}|{round(start('vent')*1000)}[swish];[voice][ducked][hit][swish]amix=inputs=4:duration=longest:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=9,afade=t=out:st=53:d=1[out]'''
# Older distro FFmpeg lacks amix's normalize flag; use its default then loudnorm.
fx=fx.replace(':normalize=0','')
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(F/'assets/audio/narration.wav'),'-i',str(F/'assets/audio/music.mp3'),'-i',str(F/'assets/audio/impact.mp3'),'-i',str(F/'assets/audio/whoosh.mp3'),'-filter_complex',fx,'-map','[out]','-t',str(D),'-ar','48000','-ac','2','-c:a','aac','-b:a','192k',str(F/'assets/audio/master.m4a')]
subprocess.run(cmd,check=True)
(O/'storyboard.md').write_text('# Storyboard\n\n| Start | End | Scene | Visual purpose |\n|---|---|---|---|\n'+''.join(f'| {s["start"]:.3f} | {s["end"]:.3f} | {s["id"]} | '+{'cosmos':'Instant question; moving Earth/Sun illustration','city':'Ordinary daylight persists; 08:20 number','light':'Animated travelling light pulse','dark':'City descends into darkness, impact','orbit':'Sun fades; tangent trajectory reveals; schematic not to scale','heat':'Return to ocean thermal reservoir; reverse dolly','ice':'Long-term frozen landscape; horizontal drift','vent':'Revelation; word-sized captions and particles','microbes':'Closer view of vent; chemical-energy explanation','core':'Animated cutaway: independent internal heat','ending':'Living vent and final thought; no brand outro'}[s['id']]+' |\n' for s in scenes)+'\nAll times derive from actual Kokoro sample counts. Captions are rendered on a separate editable captions track. The slow, deep-ocean particles are illustrative, not physical simulation.\n')
print('Built',len(scenes),'scenes; final speech ends',e['sections'][-1]['end'],'seconds; duration',D)
