"""Phase 3 layered character / caption / multi-shot animation. Phase 1 and 2 untouched."""
import json, math, shutil, subprocess, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

COLORS={"lavender":(172,145,230),"coral":(248,149,131),"mint":(124,204,174)}
BACKGROUNDS={"studio":(239,232,249),"garden":(191,225,201),"stage":(49,42,79)}
def font(size):
    path="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path,size) if Path(path).exists() else ImageFont.load_default()
def actor_layer(w,h,actor,progress):
    layer=Image.new("RGBA",(w,h),(0,0,0,0));d=ImageDraw.Draw(layer)
    cx=int(w*.5);cy=int(h*.56)
    pose=actor.get("pose","wave");emotion=actor.get("expression","happy")
    assert pose in ("wave","idle","jump") and emotion in ("happy","surprised","sleepy")
    if pose=="jump":cy-=int(34*abs(math.sin(progress*math.pi)))
    skin=(242,192,153);color=COLORS[actor.get("color","lavender")]
    # body behind face
    d.rounded_rectangle((cx-49,cy+40,cx+49,cy+140),radius=22,fill=color)
    # legs
    d.line((cx-20,cy+125,cx-24,cy+173),fill=(70,65,85),width=15)
    d.line((cx+20,cy+125,cx+24,cy+173),fill=(70,65,85),width=15)
    # arms, including waving motion
    d.line((cx-43,cy+67,cx-83,cy+110),fill=skin,width=15)
    hand_y=cy-25-int(16*math.sin(progress*math.pi*4)) if pose=="wave" else cy+109
    d.line((cx+43,cy+67,cx+82,hand_y),fill=skin,width=15)
    # head and hair layers
    d.ellipse((cx-48,cy-58,cx+48,cy+43),fill=skin)
    d.pieslice((cx-50,cy-66,cx+50,cy+24),180,360,fill=(72,52,78))
    if emotion=="sleepy":
        for dx in (-19,19):d.arc((cx+dx-10,cy-5,cx+dx+10,cy+8),0,180,fill=(40,40,60),width=3)
    else:
        for dx in (-19,19):d.ellipse((cx+dx-4,cy-3,cx+dx+4,cy+5),fill=(38,37,51))
    if emotion=="surprised":d.ellipse((cx-6,cy+16,cx+6,cy+32),fill=(100,44,60))
    elif emotion=="happy":d.arc((cx-17,cy+8,cx+17,cy+30),0,180,fill=(100,44,60),width=3)
    else:d.line((cx-9,cy+23,cx+9,cy+23),fill=(100,44,60),width=2)
    return layer
def render(config,root=Path("output")):
    name=config["name"]
    assert name and all(c.isalnum() or c in "-_" for c in name)
    fps=int(config.get("fps",12));w,h=map(int,config.get("size",[640,360]))
    assert 1<=fps<=24 and 320<=w<=1280 and 240<=h<=720
    shots=config["shots"];assert 1<=len(shots)<=12
    folder=root/name;frames=folder/"frames";frames.mkdir(parents=True,exist_ok=True)
    total=0
    for shot in shots:
        duration=float(shot["duration"]);assert .5<=duration<=10
        background=shot["background"];assert background in BACKGROUNDS
        actor=shot["actor"];assert actor.get("color","lavender") in COLORS
        caption=str(shot.get("caption",""));assert len(caption)<=90
        count=round(duration*fps)
        for j in range(count):
            im=Image.new("RGBA",(w,h),BACKGROUNDS[background]+(255,));d=ImageDraw.Draw(im)
            d.rectangle((0,int(h*.82),w,h),fill=(110,105,135,255))
            if background=="garden":
                for x in range(35,w,100):d.ellipse((x,h*.75,x+28,h*.84),fill=(103,174,122))
            elif background=="stage":
                d.ellipse((w*.3,h*.08,w*.7,h*.5),outline=(225,207,135),width=4)
            layer=actor_layer(w,h,actor,j/max(1,count-1));im.alpha_composite(layer)
            if caption:
                text_font=font(20);padding=14
                box=(22,h-75,w-22,h-18)
                d.rounded_rectangle(box,radius=12,fill=(255,255,255,235),outline=(70,60,95),width=2)
                bbox=d.textbbox((0,0),caption,font=text_font)
                tw=bbox[2]-bbox[0]
                if tw>w-75:raise ValueError("Caption too wide; shorten text")
                d.text(((w-tw)/2,h-58),caption,font=text_font,fill=(30,28,46))
            im.convert("RGB").save(frames/f"frame_{total:04d}.png");total+=1
    paths=sorted(frames.glob("frame_*.png"))
    imgs=[Image.open(p) for p in paths]
    imgs[0].save(folder/(name+".gif"),save_all=True,append_images=imgs[1:],duration=round(1000/fps),loop=0,optimize=True)
    for img in imgs:img.close()
    if not shutil.which("ffmpeg"):raise RuntimeError("ffmpeg required")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(folder/(name+".mp4"))],check=True)
    print("Rendered",name,"shots",len(shots),"frames",total)
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--config",default="storyboard.json");args=parser.parse_args()
    data=json.loads(Path(args.config).read_text());assert 1<=len(data["stories"])<=6
    for story in data["stories"]:render(story)
