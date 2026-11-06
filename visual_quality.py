"""Visual-quality A/B: original hand-authored procedural PNG embellishments, imported by Rig 2.1.
This is an artwork pipeline test, NOT production-grade anime or an AI model.
"""
import json, math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from rig21 import make_assets, load_manifest, composite, LAYER_NAMES
from anime_layers import SKY, CITY, W, H

BASE=Path("assets/visual_quality")
def manifest(folder):
    return {"format_version":1,"canvas":[360,380],"layers":{n:{"file":n+".png","anchor":[0,0],"scale":1} for n in LAYER_NAMES}}
def prepare():
    old=make_assets(BASE/"before")
    new=make_assets(BASE/"after")
    (old/"manifest.json").write_text(json.dumps(manifest(old),indent=2))
    (new/"manifest.json").write_text(json.dumps(manifest(new),indent=2))
    def edit(name,fn):
        path=new/(name+".png")
        with Image.open(path) as source:im=source.convert("RGBA")
        fn(im)
        im.save(path)
    def back(im):
        d=ImageDraw.Draw(im,"RGBA")
        for j in range(15):
            x=79+j*12
            d.line([(x,115),(x-17,240+j%4*12),(x-22,310)],fill=(174,124,205,85),width=2)
        d.arc((80,45,279,290),190,330,fill=(191,126,222,140),width=4)
    edit("back_hair",back)
    def head(im):
        d=ImageDraw.Draw(im,"RGBA")
        # Facial contour and delicate shadows, no edits to existing animation mechanics.
        d.arc((103,79,265,261),20,158,fill=(125,77,110,105),width=3)
        d.ellipse((117,190,150,204),fill=(243,119,147,52))
        d.ellipse((224,190,251,203),fill=(243,119,147,52))
        d.polygon([(185,170),(177,191),(192,194)],fill=(190,111,118,50))
        d.line([(175,192),(188,194)],fill=(147,85,111,95),width=2)
        d.arc((133,115,237,226),200,327,fill=(255,234,218,100),width=3)
        d.ellipse((125,108,135,119),fill=(255,242,220,95))
        d.ellipse((231,108,242,118),fill=(255,242,220,95))
    edit("head",head)
    def eyes(im):
        d=ImageDraw.Draw(im,"RGBA")
        for x in (141,216):
            d.arc((x-23,147,x+20,174),190,349,fill=(39,26,69,220),width=2)
            d.line([(x-21,163),(x-28,157)],fill=(39,26,69,230),width=2)
            d.ellipse((x+4,164,x+8,170),fill=(255,247,244,215))
            d.arc((x-9,158,x+10,182),45,140,fill=(186,129,225,140),width=2)
    edit("eyes_open",eyes)
    def outfit(im):
        d=ImageDraw.Draw(im,"RGBA")
        d.polygon([(92,277),(145,282),(170,337),(128,322)],fill=(112,107,167,70))
        d.polygon([(250,277),(218,292),(192,343),(234,323)],fill=(122,111,170,80))
        d.line([(91,292),(68,370)],fill=(182,152,206,145),width=3)
        d.line([(261,295),(288,370)],fill=(182,152,206,125),width=3)
        d.polygon([(171,272),(180,289),(190,272)],fill=(237,193,209,170))
        d.ellipse((179,285,185,291),fill=(252,220,181,245))
    edit("body",outfit)
    def fringe(im):
        d=ImageDraw.Draw(im,"RGBA")
        for j in range(9):
            x=113+j*15
            d.line([(x,78),(x+4,98),(x-3,123)],fill=(181,122,205,95),width=2)
        d.arc((108,43,267,149),200,315,fill=(222,159,234,125),width=3)
    edit("front_hair",fringe)
    for n in LAYER_NAMES:
        im=Image.open(new/(n+".png"))
        assert im.mode=="RGBA" and im.size==(360,380),n
    return old,new

def scene(config,loaded,t,title):
    camera=round(11*math.sin(t*.85))
    image=Image.new("RGBA",(W,H))
    image.alpha_composite(SKY,(-110+round(camera*.2),-38))
    image.alpha_composite(CITY,(-105+round(camera*.55),-23))
    actor,_=composite(config,loaded,t)
    image.alpha_composite(actor,(145+camera,2))
    d=ImageDraw.Draw(image)
    d.rectangle((0,0,W,18),fill=(13,14,32))
    d.rectangle((0,H-22,W,H),fill=(13,14,32))
    d.text((25,28),title,fill=(255,224,231))
    return image.convert("RGB")

def main():
    old,new=prepare()
    a,old_layers=load_manifest(old/"manifest.json")
    b,new_layers=load_manifest(new/"manifest.json")
    assert all(old_layers[n].tobytes()!=new_layers[n].tobytes() for n in ("head","eyes_open","body","front_hair","back_hair"))
    output=Path("output/visual_quality");frames=output/"frames";frames.mkdir(parents=True,exist_ok=True)
    original=scene(a,old_layers,0,"BEFORE / RIG 2.1")
    upgraded=scene(b,new_layers,0,"AFTER / ORIGINAL ART REFINEMENT")
    side=Image.new("RGB",(W*2,H))
    side.paste(original,(0,0));side.paste(upgraded,(W,0))
    side.save(output/"before_after.png")
    images=[]
    for i in range(48):
        t=i/12
        image=scene(b,new_layers,t,"AFTER / IMPORTED ARTWORK")
        image.save(frames/f"frame_{i:04d}.png");images.append(image)
    delays=[10*(round((i+1)*100/12)-round(i*100/12)) for i in range(48)]
    images[0].save(output/"visual_quality.gif",save_all=True,append_images=images[1:],duration=delays,loop=0,disposal=2)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","12","-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-profile:v","baseline","-level","3.1","-pix_fmt","yuv420p","-movflags","+faststart",str(output/"visual_quality.mp4")],check=True)
    print("PASS: real before/after imported RGBA PNG layers, visual comparison, 48-frame MP4/GIF")
if __name__=="__main__":main()
