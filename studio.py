"""Free configuration-driven 2D animation studio. Legacy animate.py remains untouched."""
import argparse, json, math, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw

def render(scene, root=Path("output")):
    name=scene["name"]
    assert name.replace("_","").replace("-","").isalnum(), "Unsafe scene name"
    w,h=map(int,scene.get("size",[640,360]))
    fps=int(scene.get("fps",12)); seconds=float(scene.get("duration",3))
    assert 1<=fps<=30 and 0.5<=seconds<=15 and 64<=w<=1920 and 64<=h<=1080
    character=scene["character"]; background=scene["background"]; motion=scene["motion"]
    assert character in ("fish","ball","star")
    assert background in ("ocean","sky","night")
    assert motion in ("swim","bounce","orbit","still")
    palette={"ocean":(14,60,92),"sky":(130,205,242),"night":(27,24,64)}
    folder=root/name; frames=folder/"frames"; frames.mkdir(parents=True,exist_ok=True)
    count=round(fps*seconds)
    for i in range(count):
        t=i/max(1,count-1); phase=2*math.pi*t
        im=Image.new("RGB",(w,h),palette[background]); d=ImageDraw.Draw(im)
        if background=="ocean":
            for x in range(0,w,80): d.arc((x,15,x+100,60),0,180,fill=(57,132,164),width=2)
        elif background=="night":
            for j in range(28):
                x=(j*97+13)%w;y=(j*53+19)%h
                d.ellipse((x,y,x+3,y+3),fill=(240,230,170))
        else:
            d.ellipse((w-120,30,w-65,85),fill=(255,236,142))
        x=int(w*(.18+.64*t)); y=int(h*.52)
        if motion=="bounce": y+=int(-h*.24*abs(math.sin(2*phase)))
        if motion=="swim": y+=int(h*.06*math.sin(3*phase))
        if motion=="orbit":
            x=int(w*.5+w*.25*math.cos(phase));y=int(h*.5+h*.25*math.sin(phase))
        if motion=="still":x=int(w*.5)
        r=max(12,min(w,h)//10)
        if character=="fish":
            d.polygon([(x-r+3,y),(x-2*r,y-r),(x-2*r,y+r)],fill=(247,126,71))
            d.ellipse((x-r,y-r//2,x+r,y+r//2),fill=(255,172,70),outline=(255,221,140),width=3)
            d.polygon([(x-r//3,y-r//2),(x-r//2,y-r),(x+r//3,y-r//2)],fill=(252,201,90))
            d.ellipse((x+r//2,y-r//5,x+r//2+5,y-r//5+5),fill=(16,31,40))
        elif character=="ball":
            d.ellipse((x-r,y-r,x+r,y+r),fill=(245,104,134),outline=(255,225,225),width=3)
            d.ellipse((x-r//2,y-r//2,x-r//4,y-r//4),fill=(255,211,220))
        else:
            pts=[]
            for k in range(10):
                a=-math.pi/2+k*math.pi/5
                rad=r if k%2==0 else r*.44
                pts.append((x+rad*math.cos(a),y+rad*math.sin(a)))
            d.polygon(pts,fill=(255,218,88))
        im.save(frames/f"frame_{i:04d}.png")
    imgs=[Image.open(p) for p in sorted(frames.glob("*.png"))]
    imgs[0].save(folder/(name+".gif"),save_all=True,append_images=imgs[1:],duration=round(1000/fps),loop=0,optimize=True)
    for im in imgs: im.close()
    if not shutil.which("ffmpeg"): raise RuntimeError("FFmpeg required for MP4 export")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(folder/(name+".mp4"))],check=True)
    print("Rendered",name,character,background,motion,count,"frames")
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--config",default="scenes.json")
    args=parser.parse_args()
    scenes=json.loads(Path(args.config).read_text())["scenes"]
    assert 1<=len(scenes)<=12
    for scene in scenes:render(scene)
