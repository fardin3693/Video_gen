"""Estimated word highlighting based on weighted TTS duration (not forced alignment)."""
import json
from PIL import ImageDraw,ImageFont
from scenes import F,WHITE,CYAN
WORDS=json.load(open('build/words.json'))
# Group within scene, no more than five words; gaps mark scene changes.
GROUPS=[]; g=[]
for w in WORDS:
    if g and (len(g)>=5 or w[0]-g[-1][1]>.3): GROUPS.append(g); g=[]
    g.append(w)
if g: GROUPS.append(g)
FNT=ImageFont.truetype(F,32)
def draw(im,t):
    group=next((g for g in GROUPS if g[0][0]<=t<=g[-1][1]),None)
    if not group:return
    d=ImageDraw.Draw(im)
    # Break phrases onto two short rows, to stay inside x=32..468.
    rows=[[]]; width=0
    for word in group:
        ww=d.textlength(word[2]+' ',font=FNT)
        if width+ww>425 and rows[-1]: rows.append([]); width=0
        rows[-1].append(word); width+=ww
    if len(rows)>2: rows=rows[:2] # rare overflow is avoided by five word group limit
    top=655 if len(rows)==2 else 674
    for j,row in enumerate(rows):
        content=' '.join(x[2] for x in row); total=d.textlength(content,font=FNT); x=(540-total)/2; y=top+j*39
        for i,(start,end,word) in enumerate(row):
            col=CYAN if start<=t<=end else WHITE
            d.text((x+1,y+2),word,font=FNT,fill=(0,0,0),stroke_width=3,stroke_fill=(0,0,0))
            d.text((x,y),word,font=FNT,fill=col,stroke_width=1,stroke_fill=(0,0,0))
            x+=d.textlength(word+' ',font=FNT)
