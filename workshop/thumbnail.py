"""Create the vertical publishing thumbnail from the Arena-generated hero image."""
from PIL import Image, ImageOps, ImageDraw, ImageFont
from pathlib import Path
R=Path(__file__).resolve().parents[1]
im=ImageOps.fit(Image.open(R/'film/assets/sun-earth.jpg').convert('RGB'),(1080,1920))
shade=Image.new('RGBA',im.size)
p=shade.load()
for y in range(1920):
    alpha=round(165*max(0,1-y/850)) if y<850 else round(110*max(0,(y-1000)/920))
    for x in range(1080):p[x,y]=(2,9,15,alpha)
im=Image.alpha_composite(im.convert('RGBA'),shade);d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def text(x,y,s,size,color):d.text((x,y),s,font=ImageFont.truetype(font,size),fill=color,stroke_width=1)
d.rectangle((112,275,188,281),fill='#65e0dd')
text(112,305,'WHAT IF THE',43,'#f5f5ec')
text(103,360,'SUN',158,'#f5f5ec')
text(103,510,'VANISHED?',124,'#ffd383')
d.rounded_rectangle((112,1080,790,1320),radius=16,fill=(2,9,15,235),outline='#65e0dd',width=3)
text(148,1100,'08:20',126,'#ffd383')
text(152,1250,'UNTIL WE NOTICE',36,'#f5f5ec')
im.convert('RGB').save(R/'output/thumbnail.jpg',quality=94,subsampling=0)
print('output/thumbnail.jpg: 1080 x 1920')
