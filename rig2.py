"""Reusable layered character rig MVP. All artwork generated locally with Pillow."""
import argparse, json, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from anime_layers import SKY, CITY, W, H

def palette(config):
    def rgb(key):
        v=config["palette"][key]
        if not isinstance(v,list) or len(v)!=3 or any(not isinstance(x,int) or not 0<=x<=255 for x in v):
            raise ValueError("Palette colors must be RGB triples")
        return tuple(v)
    return {k:rgb(k) for k in ("hair","hair_highlight","skin","jacket","iris")}

def actor(config, t):
    """Transparent character layer; independent head, eyes, brows, mouth and hair."""
    p=palette(config); im=Image.new("RGBA",(360,380));d=ImageDraw.Draw(im)
    sway=round(3*math.sin(t*2*math.pi*.7)); nod=round(2*math.sin(t*2*math.pi*.9))
    # Torso: body motion independent of head and hair.
    d.polygon([(89+sway,272),(260+sway,272),(320+sway,380),(43+sway,380)],fill=p["jacket"])
    d.polygon([(143+sway,268),(179+sway,335),(216+sway,269)],fill=(172,105,159))
    d.line([(104+sway,291),(92+sway,374)],fill=(116,106,184),width=5)
    # Back hair layer moves in its own direction.
    hair_sway=round(8*math.sin(t*2*math.pi*.65))
    d.ellipse((64+hair_sway,30,293+hair_sway,331),fill=p["hair"])
    for k in range(7):
        x=77+k*28+hair_sway
        d.polygon([(x,185),(x-13,328+(k%3)*12),(x+25,276)],fill=p["hair_highlight"])
    # Neck and head.
    d.rounded_rectangle((153+sway,215+nod,207+sway,284+nod),radius=18,fill=p["skin"])
    d.ellipse((101+sway,79+nod,263+sway,259+nod),fill=p["skin"])
    # Eyes blink independently from eyebrows and mouth.
    blink=min(abs(t-1.12),abs(t-2.82),abs(t-4.20)) < .105
    for x in (140,214):
        x+=sway
        if blink:
            d.arc((x-21,164+nod,x+17,175+nod),0,180,fill=(50,31,80),width=4)
        else:
            d.ellipse((x-19,156+nod,x+16,185+nod),fill=(255,251,249))
            d.ellipse((x-9,158+nod,x+10,183+nod),fill=p["iris"])
            d.ellipse((x-3,160+nod,x+6,177+nod),fill=(34,30,68))
            d.ellipse((x,161+nod,x+4,166+nod),fill="white")
            d.arc((x-21,151+nod,x+17,173+nod),184,347,fill=(49,30,79),width=4)
        brow_lift=4*math.sin(t*2*math.pi*.3)
        d.arc((x-22,133+nod-brow_lift,x+17,150+nod-brow_lift),188,342,fill=(63,39,96),width=3)
    # Three explicit mouth poses, timed independently of eye blinking.
    mouth=int(t*3.5)%3
    if mouth==0:d.arc((164+sway,197+nod,204+sway,215+nod),3,173,fill=(158,70,104),width=3)
    elif mouth==1:d.ellipse((176+sway,195+nod,193+sway,216+nod),fill=(137,62,103))
    else:d.rounded_rectangle((164+sway,198+nod,205+sway,205+nod),radius=3,fill=(153,75,109))
    # Foreground hair with a separately oscillating fringe.
    fringe=round(5*math.sin(t*2*math.pi*.95))
    d.pieslice((91+sway,43+nod,273+sway,172+nod),178,357,fill=p["hair"])
    d.polygon([(108+sway+fringe,97+nod),(137+sway+fringe,42+nod),(148+sway+fringe,169+nod)],fill=p["hair_highlight"])
    d.polygon([(160+sway-fringe,58+nod),(191+sway-fringe,39+nod),(183+sway-fringe,160+nod)],fill=p["hair"])
    d.polygon([(214+sway+fringe,67+nod),(264+sway+fringe,93+nod),(236+sway+fringe,165+nod)],fill=p["hair_highlight"])
    d.ellipse((262+sway,185+nod,271+sway,194+nod),fill=(255,222,142))
    return im, {"blink":blink,"mouth":mouth,"hair_offset":fringe,"head_offset":nod}

def render(config):
    if config.get("format_version")!=1:raise ValueError("Unsupported rig config version")
    if not config.get("name","").replace("_","").isalnum():raise ValueError("Unsafe name")
    fps=int(config.get("fps",12));seconds=float(config.get("seconds",5))
    if not (8<=fps<=24 and 2<=seconds<=10):raise ValueError("Invalid fps or duration")
    count=round(fps*seconds);root=Path("output")/config["name"];root.mkdir(parents=True,exist_ok=True)
    frames=root/"frames";frames.mkdir(exist_ok=True)
    for stale in frames.glob("frame_*.png"):stale.unlink()
    images=[];states=[]
    for i in range(count):
        t=i/fps;camera=round(11*math.sin(t*.85))
        canvas=Image.new("RGBA",(W,H))
        canvas.alpha_composite(SKY,(-110+round(camera*.2),-38))
        canvas.alpha_composite(CITY,(-105+round(camera*.55),-23))
        character,state=actor(config,t);states.append(state)
        canvas.alpha_composite(character,(145+camera,2+round(2*math.sin(t*2))))
        d=ImageDraw.Draw(canvas)
        d.rectangle((0,0,W,18),fill=(13,14,32))
        d.rectangle((0,H-22,W,H),fill=(13,14,32))
        d.text((25,28),config.get("title","CHARACTER RIG 2.0"),fill=(255,224,231))
        img=canvas.convert("RGB");img.save(frames/f"frame_{i:04d}.png");images.append(img)
    delays=[10*(round((i+1)*100/fps)-round(i*100/fps)) for i in range(count)]
    images[0].save(root/(config["name"]+".gif"),save_all=True,append_images=images[1:],duration=delays,loop=0,optimize=False,disposal=2)
    if not shutil.which("ffmpeg"):raise RuntimeError("FFmpeg required")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-profile:v","baseline","-level","3.1","-pix_fmt","yuv420p","-movflags","+faststart",str(root/(config["name"]+".mp4"))],check=True)
    assert any(s["blink"] for s in states) and any(not s["blink"] for s in states)
    assert len({s["mouth"] for s in states})==3
    assert len({s["hair_offset"] for s in states})>3
    print("Rig 2.0 verified:",count,"frames",len({s["mouth"] for s in states}),"mouth poses, blink and hair movement")
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--config",default="rig2.json")
    args=parser.parse_args();render(json.loads(Path(args.config).read_text()))
