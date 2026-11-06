"""Character Rig 2.1: actual transparent PNG import, anchors and layer transforms.
All sample assets are generated as original RGBA PNG files, then re-opened from disk.
"""
import argparse, json, math, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw
from anime_layers import SKY, CITY, W, H

LAYER_NAMES=("back_hair","body","head","eyes_open","eyes_closed","brows","mouth_smile","mouth_open","mouth_line","front_hair")
def make_assets(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    for name in LAYER_NAMES:
        im=Image.new("RGBA",(360,380));d=ImageDraw.Draw(im)
        if name=="back_hair":
            d.ellipse((62,28,295,330),fill=(54,38,91))
            for k in range(8):
                x=76+k*26;d.polygon([(x,172),(x-15,325+(k%3)*14),(x+20,267)],fill=(87,54,132))
        elif name=="body":
            d.polygon([(92,269),(261,269),(320,380),(42,380)],fill=(40,42,92))
            d.polygon([(144,268),(180,332),(216,268)],fill=(178,97,155))
            d.line((104,294,88,379),fill=(117,109,180),width=5)
        elif name=="head":
            d.rounded_rectangle((153,211,209,283),radius=18,fill=(244,179,164))
            d.ellipse((100,78,265,261),fill=(251,199,180))
            d.ellipse((110,184,128,191),fill=(244,148,158,110))
            d.ellipse((235,184,253,191),fill=(244,148,158,110))
        elif name.startswith("eyes_"):
            for x in (141,216):
                if name=="eyes_closed":
                    d.arc((x-20,160,x+16,179),0,180,fill=(49,32,78),width=4)
                else:
                    d.ellipse((x-19,156,x+16,186),fill=(255,251,248))
                    d.ellipse((x-9,158,x+10,183),fill=(109,71,175))
                    d.ellipse((x-2,160,x+6,177),fill=(35,30,70))
                    d.ellipse((x,161,x+4,165),fill="white")
                    d.arc((x-21,151,x+17,173),185,348,fill=(50,32,80),width=4)
        elif name=="brows":
            for x in (141,216):d.arc((x-22,135,x+17,151),190,345,fill=(67,42,97),width=4)
        elif name=="mouth_smile":d.arc((164,194,205,216),5,170,fill=(162,70,102),width=4)
        elif name=="mouth_open":d.ellipse((177,194,194,218),fill=(133,55,92))
        elif name=="mouth_line":d.rounded_rectangle((164,201,205,206),radius=2,fill=(162,75,108))
        elif name=="front_hair":
            d.pieslice((91,41,274,171),180,356,fill=(70,45,115))
            d.polygon([(107,97),(139,41),(151,170)],fill=(103,67,157))
            d.polygon([(160,60),(191,37),(184,157)],fill=(82,51,136))
            d.polygon([(215,69),(266,92),(237,169)],fill=(110,71,166))
        im.save(folder/(name+".png"))
    return folder

def load_manifest(path):
    path=Path(path).resolve();config=json.loads(path.read_text())
    if config.get("format_version")!=1:raise ValueError("Unsupported manifest version")
    layers=config["layers"]
    if set(layers)!=set(LAYER_NAMES):raise ValueError("Missing or unknown rig layers")
    loaded={}
    for name in LAYER_NAMES:
        entry=layers[name]
        rel=Path(entry["file"])
        if rel.is_absolute() or ".." in rel.parts:raise ValueError("Unsafe layer path")
        src=(path.parent/rel).resolve()
        if not src.is_relative_to(path.parent):raise ValueError("Layer outside manifest folder")
        if src.suffix.lower()!=".png":raise ValueError("Only PNG layers accepted")
        with Image.open(src) as im:
            if im.mode!="RGBA":raise ValueError(f"{name} must be transparent RGBA PNG")
            if im.size!=(360,380):raise ValueError("Layer dimensions must be 360x380")
            loaded[name]=im.copy()
        anchor=entry["anchor"]
        if len(anchor)!=2 or not all(isinstance(v,(int,float)) and math.isfinite(v) for v in anchor):
            raise ValueError("Invalid anchor")
        if any(abs(v)>400 for v in anchor):raise ValueError("Anchor outside safe bounds")
    return config,loaded

def composite(config,loaded,t):
    im=Image.new("RGBA",(360,380));phase=t*2*math.pi
    body=round(3*math.sin(phase*.7));head=round(2*math.sin(phase*.9))
    hair=round(7*math.sin(phase*.65));fringe=round(5*math.sin(phase*.95))
    blink=any(abs(t-at)<.105 for at in (1.12,2.82,4.20))
    mouth=("mouth_smile","mouth_open","mouth_line")[int(t*3.5)%3]
    selected=("back_hair","body","head","eyes_closed" if blink else "eyes_open","brows",mouth,"front_hair")
    for name in selected:
        entry=config["layers"][name]
        ax,ay=entry["anchor"]
        motion={"back_hair":(hair,0),"body":(body,round(2*math.sin(phase*.7))),
                "head":(body,head),"eyes_open":(body,head),"eyes_closed":(body,head),
                "brows":(body,head+round(3*math.sin(phase*.3))),
                "mouth_smile":(body,head),"mouth_open":(body,head),"mouth_line":(body,head),
                "front_hair":(body+fringe,head)}[name]
        x=round(ax+motion[0]);y=round(ay+motion[1])
        scale=float(entry.get("scale",1))
        if not (.8<=scale<=1.2):raise ValueError("Scale outside supported range")
        layer=loaded[name]
        if scale!=1:
            w,h=layer.size;layer=layer.resize((round(w*scale),round(h*scale)),Image.Resampling.BICUBIC)
            x-=round((layer.width-w)/2);y-=round((layer.height-h)/2)
        im.alpha_composite(layer,(x,y))
    return im,{"blink":blink,"mouth":mouth,"hair":hair}

def render(manifest,output):
    config,loaded=load_manifest(manifest)
    root=Path(output);root.mkdir(parents=True,exist_ok=True)
    frames=root/"frames";frames.mkdir(exist_ok=True)
    fps=12;count=60;images=[];states=[]
    for i in range(count):
        t=i/fps;camera=round(11*math.sin(t*.85))
        scene=Image.new("RGBA",(W,H))
        scene.alpha_composite(SKY,(-110+round(camera*.2),-38))
        scene.alpha_composite(CITY,(-105+round(camera*.55),-23))
        actor,state=composite(config,loaded,t);states.append(state)
        scene.alpha_composite(actor,(145+camera,2))
        d=ImageDraw.Draw(scene)
        d.rectangle((0,0,W,18),fill=(13,14,32))
        d.rectangle((0,H-22,W,H),fill=(13,14,32))
        d.text((25,28),"NO PANTS / IMPORTED PNG RIG 2.1",fill=(255,224,231))
        image=scene.convert("RGB");image.save(frames/f"frame_{i:04d}.png");images.append(image)
    delays=[10*(round((i+1)*100/fps)-round(i*100/fps)) for i in range(count)]
    images[0].save(root/"rig21.gif",save_all=True,append_images=images[1:],duration=delays,loop=0,disposal=2,optimize=False)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-profile:v","baseline","-level","3.1","-pix_fmt","yuv420p","-movflags","+faststart",str(root/"rig21.mp4")],check=True)
    assert any(s["blink"] for s in states) and any(not s["blink"] for s in states)
    assert len({s["mouth"] for s in states})==3
    assert len({s["hair"] for s in states})>3
    print("Rig 2.1 imported",len(loaded),"RGBA PNG layers; rendered",count,"frames; independent blinking, mouths and hair verified")

def main():
    p=argparse.ArgumentParser();p.add_argument("--manifest",default="assets/rig21/manifest.json");p.add_argument("--make-demo",action="store_true");p.add_argument("--output",default="output/rig21")
    args=p.parse_args()
    if args.make_demo:
        folder=make_assets(Path(args.manifest).parent)
        layers={name:{"file":name+".png","anchor":[0,0],"scale":1} for name in LAYER_NAMES}
        (folder/"manifest.json").write_text(json.dumps({"format_version":1,"canvas":[360,380],"layers":layers},indent=2))
        print("Created original test asset pack:",folder)
    else:render(args.manifest,args.output)
if __name__=="__main__":main()
