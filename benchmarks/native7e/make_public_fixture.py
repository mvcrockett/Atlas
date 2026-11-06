#!/usr/bin/env python3
"""PUBLIC SYNTHETIC calibration fixture; not the lavender heroine."""
from pathlib import Path
from PIL import Image,ImageDraw
import json
P=Path('art');P.mkdir(exist_ok=True)
W=480;H=480
def save(name,paint):
    im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im);paint(d);im.save(P/(name+'.png'))
def base(d):
    d.rectangle((0,0,W,H),fill=(248,241,255,255))
    d.ellipse((75,40,405,440),fill=(225,182,169,255),outline=(65,47,65,255),width=5)
save('face_base',base)
def eyes(d):
    d.ellipse((140,170,215,210),fill=(255,255,255,255),outline=(42,26,50,255),width=4)
    d.ellipse((263,170,338,210),fill=(255,255,255,255),outline=(42,26,50,255),width=4)
    for x in (180,303):d.ellipse((x-13,176,x+13,205),fill=(50,138,100,255))
save('eyes_open',eyes)
def closed(d):
    d.arc((140,175,215,210),0,180,fill=(42,26,50,255),width=5)
    d.arc((263,175,338,210),0,180,fill=(42,26,50,255),width=5)
save('eyes_closed',closed)
for name,h,width in [('rest',4,62),('small',13,56),('medium',26,60),('wide',40,66),('rounded',39,25)]:
    def mouth(d,name=name,h=h,width=width):
        x=240;y=306
        d.ellipse((x-width,y-h//2,x+width,y+h//2),fill=(80,33,52,255),outline=(47,20,41,255),width=3)
        if name!='rest':d.arc((x-width//2,y-h//3,x+width//2,y+h//2),0,180,fill=(245,160,170,255),width=3)
    save('mouth_'+name,mouth)
layers=[{'id':n,'path':n+'.png','order':i} for i,n in enumerate(['face_base','eyes_open','eyes_closed','mouth_rest','mouth_small','mouth_medium','mouth_wide','mouth_rounded'])]
(P/'manifest.json').write_text(json.dumps({'status':'SYNTHETIC_CALIBRATION_ONLY','approval':False,'canvas':{'width':W,'height':H},'layers':layers},indent=2))
print('Created calibration-only layers; no private portrait bytes used.')
