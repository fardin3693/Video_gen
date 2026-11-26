"""Nine hand-drawn, procedural 2D compositions, in a 540x960 design space."""
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import numpy as np, math, random
import aggdraw
from bpm_clock import bpm,phase
W,H=540,960
INK=(7,9,13); WHITE=(245,248,255); MUTED=(156,173,195); CYAN=(61,214,245); RED=(255,59,48); AMBER=(255,176,32)
F='assets/inter-bold.ttf'; M='assets/jetbrains-mono-bold.ttf'
def font(s,mono=False): return ImageFont.truetype(M if mono else F,s)
FONTS={(s,m):font(s,m) for s in [10,11,12,13,14,15,16,17,18,19,20,22,24,27,30,32,34,36,40,48,56] for m in [False,True]}
def text(d,xy,s,size=16,fill=WHITE,anchor=None,mono=False):
    d.text(xy,s,font=FONTS[(size,mono)],fill=fill,anchor=anchor,stroke_width=0)
def centered(d,y,s,size=20,fill=WHITE,mono=False): text(d,(270,y),s,size,fill,'mt',mono)
def path(im, commands, fill, stroke=None, width=1):
    p=aggdraw.Path()
    for op,pts in commands:
        getattr(p,op)(*pts)
    c=aggdraw.Draw(im); c.path(p,aggdraw.Brush(fill) if fill else None,aggdraw.Pen(stroke,width) if stroke else None); c.flush()
def heart_asset():
    # Painted anatomical silhouette: a consistent reusable model rather than stock imagery.
    im=Image.new('RGBA',(400,430)); mask=Image.new('L',(400,430));
    shape=[('moveto',(185,92)),('curveto',(151,35,74,75,58,144)),('curveto',(31,246,105,353,197,405)),('curveto',(236,370,340,288,344,184)),('curveto',(349,107,291,64,237,86)),('curveto',(220,91,202,105,185,92)),('close',())]
    path(mask,shape,255)
    yy,xx=np.mgrid[:430,:400]; glow=np.exp(-((xx-100)**2/12000+(yy-150)**2/32000)); edge=np.exp(-((xx-290)**2/6000+(yy-160)**2/23000))
    arr=np.zeros((430,400,4),dtype=np.uint8); arr[:,:,0]=np.clip(54+116*glow+24*edge,0,255); arr[:,:,1]=np.clip(7+12*glow+9*edge,0,255); arr[:,:,2]=np.clip(20+23*glow+26*edge,0,255); arr[:,:,3]=np.asarray(mask)
    im=Image.fromarray(arr,'RGBA')
    # Great vessels, broad rimmed silhouettes.
    path(im,[('moveto',(144,105)),('curveto',(130,60,138,24,166,19)),('curveto',(183,15,204,32,207,55)),('lineto',(214,96)),('lineto',(183,116)),('curveto',(180,69,174,48,164,48)),('curveto',(160,62,165,83,170,99)),('close',())], '#7d1724','#df3c4a',3)
    path(im,[('moveto',(208,98)),('curveto',(206,67,222,36,247,42)),('curveto',(273,46,273,76,267,102)),('lineto',(244,112)),('curveto',(249,76,248,65,240,65)),('curveto',(233,66,230,86,229,103)),('close',())], '#591625','#c93848',3)
    path(im,shape,None,'#e54c56',3)
    # Coronary paths branch across the muscle.
    for pts,col,w in [([(179,101),(178,148),(202,192),(213,226),(198,289),(184,344)],'#ff666b',5),([(177,143),(146,163),(118,188),(98,225)],'#f14b59',3),([(199,191),(235,181),(273,197),(296,229)],'#ff4857',4),([(213,226),(241,249),(250,292)],'#ca3647',3),([(144,163),(137,205),(119,247)],'#f68b80',2),([(235,181),(256,156),(281,151)],'#f17a78',2)]:
        d=ImageDraw.Draw(im); d.line(pts,fill=col,width=w,joint='curve');
    d=ImageDraw.Draw(im); d.arc((65,91,275,363),85,182,fill=(255,144,137,100),width=3)
    return im
HEART=heart_asset()
# static textured backdrop and subtle radial haze
rng=np.random.default_rng(13); y,x=np.mgrid[:H,:W]; haze=np.exp(-((x-270)**2/85000+(y-390)**2/120000)); noise=rng.normal(0,.7,(H,W)); arr=np.zeros((H,W,3),np.uint8)
for c,(base,mult) in enumerate([(7,17),(9,5),(13,11)]): arr[:,:,c]=np.clip(base+haze*mult+noise,0,255)
BG=Image.fromarray(arr,'RGB'); bd=ImageDraw.Draw(BG)
for y0 in range(220,630,24):
 for x0 in range(45,500,24): bd.ellipse((x0,y0,x0+1,y0+1),fill=(30,36,49))
# heart diffuse glow
GLOW=Image.new('RGBA',(400,430)); gd=ImageDraw.Draw(GLOW); gd.ellipse((50,60,350,405),fill=(193,18,31,80)); GLOW=GLOW.filter(ImageFilter.GaussianBlur(36))
def paste_heart(im,cx,cy,size,t,opacity=255):
    ph=phase(t); pulse=1+.028*math.exp(-ph*12); w=int(size*pulse); h=int(w*430/400)
    glow=GLOW.resize((int(w*1.35),int(h*1.35)),Image.Resampling.BILINEAR); im.paste(glow,(int(cx-glow.width/2),int(cy-glow.height/2)),glow)
    heart=HEART.resize((w,h),Image.Resampling.BILINEAR)
    if opacity<255: heart.putalpha(heart.getchannel('A').point(lambda v:v*opacity//255))
    im.paste(heart,(int(cx-w/2),int(cy-h/2)),heart)
def base(t,section):
    im=BG.copy(); d=ImageDraw.Draw(im)
    d.line((32,100,508,100), fill=(42,57,70),width=1)
    d.rounded_rectangle((32,109,158,139),radius=6,fill=(12,23,31),outline=(41,82,92),width=1)
    r=bpm(t); c=CYAN if r<110 else AMBER if r<260 else RED
    d.ellipse((43,119,51,127),fill=c); text(d,(58,114),f'{round(r):03d} BPM',15,c,mono=True)
    text(d,(468,117),section,11,MUTED,'rt',True)
    return im
def ecg(d,t,x0=50,y0=595,w=440,h=28,chaos=False):
    d.line((x0,y0,x0+w,y0),fill=(28,48,59),width=1)
    pts=[]
    for x in range(w+1):
        age=(w-x)/w*2.5; tt=t-age; ph=phase(max(0,tt))
        # Sharp R wave, small positive T wave. Uses exact shared beat history.
        val=-math.exp(-((ph-.065)/.026)**2)+.18*math.exp(-((ph-.28)/.10)**2)
        if chaos: val=val*.65 + .20*math.sin(tt*39)+.12*math.sin(tt*71)
        pts.append((x0+x,y0+val*h))
    d.line(pts,fill=CYAN if bpm(t)<110 else RED,width=2)
def card(d,title,sub=None):
    centered(d,157,title,27,WHITE)
    if sub: centered(d,192,sub,13,MUTED)
def label(d,x,y,s,color=MUTED,size=13): text(d,(x,y),s,size,color)
def s1(im,t):
    d=ImageDraw.Draw(im); centered(d,164,'WHAT IF YOUR HEART',18,MUTED); centered(d,192,'BEAT 5× FASTER?',30,WHITE)
    size=245*(1+.12*min(t/4,1))*(1+.05*math.exp(-((t-2.3)/.16)**2)); paste_heart(im,270,379,size,t)
    d=ImageDraw.Draw(im); centered(d,526,f'{round(bpm(t))} BPM',40,RED if bpm(t)>=260 else AMBER if bpm(t)>=110 else CYAN,True)
    if t>2.15: text(d,(408,537),'×5',22,AMBER,mono=True)
    ecg(d,t,y0=602)
def s2(im,t):
    d=ImageDraw.Draw(im); card(d,'THE BASELINE','A TYPICAL RESTING EXAMPLE')
    paste_heart(im,270+3*math.sin(t*.5),365+2*math.sin(t*.7),216,t); d=ImageDraw.Draw(im)
    d.arc((116,211,424,519),-90,270,fill=(37,56,66),width=3); d.arc((116,211,424,519),-90,-90+int(360*phase(t)),fill=CYAN,width=4)
    centered(d,528,'0.86 s PER BEAT',18,CYAN,True)
    centered(d,565,'70 × 5 =',27,WHITE,True); text(d,(364,565),'350',27,AMBER,mono=True)
    centered(d,610,'RESTING: ~70 BPM',14,MUTED)
def s3(im,t):
    d=ImageDraw.Draw(im); card(d,'HOW FAST IS FAST?','HEART RATE DURING EXERCISE')
    paste_heart(im,270+5*math.sin(t*.4),365,200,t); d=ImageDraw.Draw(im)
    box=(88,228,452,555); d.arc(box,180,360,fill=(42,56,66),width=10); d.arc(box,180,213,fill=CYAN,width=10); d.arc(box,213,275,fill=AMBER,width=10); d.arc(box,275,360,fill=(104,42,45),width=10)
    angle=math.radians(180+180*min(1,(bpm(t)-60)/290)); cx,cy=270,392; d.line((cx,cy,cx+170*math.cos(angle),cy+155*math.sin(angle)),fill=WHITE,width=3)
    text(d,(92,398),'60',12,CYAN,mono=True); text(d,(407,398),'350',12,RED,mono=True)
    centered(d,535,'HARD EXERCISE ~190 BPM',20,AMBER)
    centered(d,567,'YOUNG ADULT · ESTIMATE',13,MUTED)
    ecg(d,t,y0=613,h=15)
def s4(im,t):
    d=ImageDraw.Draw(im); card(d,'THE FILLING PROBLEM','LESS TIME BETWEEN BEATS')
    paste_heart(im,206,350,220+6*min(1,(t-17)/8),t,220); d=ImageDraw.Draw(im)
    # stylized chamber inset, level lowers as rate rises
    d.ellipse((165,290,240,400),fill=(20,9,19),outline=(255,136,124),width=3)
    fill=max(.12,1-(bpm(t)-70)/350); bottom=397; top=int(bottom-100*fill)
    d.ellipse((171,top,234,bottom-3),fill=(180,26,42),outline=(255,81,87),width=2)
    text(d,(282,303),'VENTRICLE',13,MUTED); text(d,(282,330),'FILLING',18,WHITE); d.line((245,354,273,354),fill=CYAN,width=2)
    centered(d,460,'LESS TIME TO FILL',22,WHITE)
    for i,(n,v,col) in enumerate([('70 BPM',.86,CYAN),('190 BPM',.32,AMBER),('350 BPM',.17,RED)]):
        yy=505+i*37; text(d,(48,yy),n,13,MUTED,mono=True); d.rounded_rectangle((155,yy+3,378,yy+17),4,fill=(28,35,46)); d.rounded_rectangle((155,yy+3,155+int(205*v/.86),yy+17),4,fill=(80,70,76)); fill_width=[132,29,7][i]; d.rounded_rectangle((155,yy+3,155+fill_width,yy+17),4,fill=col); text(d,(468,yy),f'{v:.2f} s',13,WHITE,'rt',True)
    text(d,(48,623),'COLOR: FILLING · ILLUSTRATIVE',11,MUTED)
def s5(im,t):
    d=ImageDraw.Draw(im); card(d,'LESS IN. LESS OUT.','BLOOD FLOW CAN FALL')
    # artery tunnel with moving cellular particles
    for i in range(7):
        r=210-i*26; d.ellipse((270-r,367-r*.68,270+r,367+r*.68),outline=(max(30,125-i*14),22+i*2,29+i*2),width=9)
    for i in range(22):
        a=i*2.399; r=((i*41+(t-25)*48)%200); x=270+math.cos(a)*r; y=367+math.sin(a)*r*.65
        radius=max(2,7-int(r/45)); d.ellipse((x-radius,y-radius*.55,x+radius,y+radius*.55),fill=(min(200,95+int(r*.45)),28,39))
    centered(d,500,'LESS BLOOD PER BEAT',22,WHITE)
    for j,(lab,frac) in enumerate([('BLOOD PER BEAT',.42),('PRESSURE',.34)]):
        y0=543+j*39; text(d,(48,y0),lab,13,MUTED); d.rounded_rectangle((245,y0+2,488,y0+16),4,fill=(36,37,48)); d.rounded_rectangle((245,y0+2,245+int(243*frac),y0+16),4,fill=RED if j else AMBER)
    centered(d,624,'QUALITATIVE · HYPOTHETICAL',11,MUTED)
def s6(im,t):
    d=ImageDraw.Draw(im); card(d,'THE BRAIN NOTICES','LOW BLOOD FLOW')
    # head profile and brain: layered vector illustration
    path(im,[('moveto',(213,479)),('curveto',(211,456,186,441,181,416)),('curveto',(154,404,151,391,168,372)),('curveto',(177,360,177,347,177,327)),('curveto',(176,262,212,228,273,228)),('curveto',(350,227,384,273,375,342)),('curveto',(370,390,347,414,330,440)),('lineto',(328,493)),('close',())],(15,35,46),(50,111,122),3)
    d=ImageDraw.Draw(im); bright=int(145-85*min(1,(t-32)/7))
    for j in range(5):
        xx=216+j*25; yy=294-14*math.sin(j*.8); d.ellipse((xx,yy,xx+56,yy+66),outline=(25,bright,bright+30),width=3)
    for i in range(5):
        x=216+i*27; d.arc((x,276,x+35,345),30,290,fill=(33,bright,bright+35),width=2)
    d.arc((191,248,359,407),195,335,fill=(48,bright,bright+35),width=2)
    centered(d,525,'DIZZINESS  ·  TUNNEL VISION',19,CYAN); centered(d,558,'FAINTING COULD FOLLOW',19,WHITE)
    ecg(d,t,y0=615,h=12)
def s7(im,t):
    d=ImageDraw.Draw(im); card(d,'THE HEART NEEDS BLOOD','MOSTLY WHILE RELAXING')
    paste_heart(im,270+2*math.sin(t*3),363,250-10*min(1,(t-39)/8),t); d=ImageDraw.Draw(im)
    for x,y in [(230,325),(302,373),(214,405)]: d.ellipse((x-16,y-10,x+16,y+10),fill=(104,64,70),outline=(150,95,96))
    centered(d,519,'RELAXATION WINDOW',16,MUTED)
    d.rounded_rectangle((82,548,458,562),5,fill=(45,38,49)); d.rounded_rectangle((82,548,117,562),5,fill=RED)
    centered(d,578,'RHYTHM CAN COLLAPSE',20,WHITE)
    ecg(d,t,y0=622,h=14,chaos=True)
def s8(im,t):
    d=ImageDraw.Draw(im); card(d,'BUILT FOR A FASTER BEAT','HUMMINGBIRD CONTRAST')
    # Anatomical hummingbird silhouette, tail, bill and translucent wings.
    wing=math.sin(t*22)*8
    path(im,[('moveto',(265,337)),('curveto',(228,303,197,253+wing,168,243+wing)),('curveto',(173,290,186,331,241,368)),('close',())],(22,79,85),(58,182,185),2)
    path(im,[('moveto',(278,340)),('curveto',(303,302,336,274-wing,369,261-wing)),('curveto',(351,311,329,345,291,366)),('close',())],(36,41,81),(100,118,185),2)
    path(im,[('moveto',(195,400)),('curveto',(229,370,239,332,272,326)),('curveto',(311,318,329,348,321,377)),('curveto',(315,404,286,430,254,432)),('lineto',(195,460)),('lineto',(216,424)),('lineto',(185,439)),('close',())],(18,74,76),(87,211,204),2)
    d=ImageDraw.Draw(im); d.ellipse((296,320,343,365),fill=(25,105,102),outline=CYAN,width=2); d.line((339,336,410,320),fill=(187,220,219),width=3); d.ellipse((329,330,334,335),fill=WHITE)
    d.ellipse((269,365,283,379),fill=(255,77,90)); d.ellipse((273,369,279,375),fill=WHITE)
    centered(d,470,'HUMMINGBIRD: 1,000+ BPM',20,CYAN); centered(d,499,'BUILT FOR IT.',16,WHITE)
    # chart is qualitative and displays only supplied figures
    for j,(lab,num,width,col) in enumerate([('HUMAN REST','~70',35,CYAN),('HUMAN PEAK','~190',90,AMBER),('HUMMINGBIRD','1,000+',215,(161,95,198))]):
        yy=536+j*27; text(d,(48,yy),lab,11,MUTED); d.rounded_rectangle((179,yy+2,179+width,yy+14),3,fill=col); text(d,(468,yy),num,12,WHITE,'rt',True)
    d.line((264,527,264,622),fill=RED,width=2); text(d,(279,620),'YOUR 5×: 350',11,RED,mono=True)
def s9(im,t):
    d=ImageDraw.Draw(im); centered(d,164,'YOUR HEART',18,MUTED); centered(d,192,'KEEPS TIME.',30,WHITE)
    paste_heart(im,270,379,245,t); d=ImageDraw.Draw(im)
    centered(d,526,f'{round(bpm(t))} BPM',40,RED if bpm(t)>=260 else AMBER if bpm(t)>=110 else CYAN,True)
    if t<59.1:
        centered(d,576,'FOLLOW FOR MORE WHAT IFS',15,WHITE)
        centered(d,615,'HYPOTHETICAL SCENARIO. NOT MEDICAL ADVICE.',10,MUTED)
    else: ecg(d,t,y0=602)
SCENES=[s1,s2,s3,s4,s5,s6,s7,s8,s9]
ENDS=[4,10,17,25,32,39,47,55,60]
NAMES=['01 / THE QUESTION','02 / RESTING','03 / THE LIMIT','04 / FILLING','05 / OUTPUT','06 / BRAIN','07 / RHYTHM','08 / CONTRAST','09 / KEEP TIME']
def render(t):
    idx=next(i for i,e in enumerate(ENDS) if t<e); im=base(t,NAMES[idx]); SCENES[idx](im,t)
    if t>=59.4:
        target=base(0,NAMES[0]); s1(target,0)
        im=Image.blend(im,target,min(1.,(t-59.4)/.5))
    return im
