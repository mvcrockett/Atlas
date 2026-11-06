"""Phase 4: reusable characters, eased poses, wrapped captions, shot transitions."""
import argparse, json, math, shutil, subprocess, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PALETTES={"lavender":(169,143,222),"coral":(240,135,122),"mint":(115,190,158),"blue":(112,159,215)}
SCENERY={"garden":(196,230,206),"studio":(234,223,243),"night":(36,39,83)}
def ease(t):return t*t*(3-2*t)
def font(sz):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,sz) if Path(p).exists() else ImageFont.load_default()
def backdrop(w,h,kind):
    im=Image.new("RGB",(w,h),SCENERY[kind]);d=ImageDraw.Draw(im)
    if kind=="garden":
        for x in range(0,w,90):
            d.ellipse((x,h*.69,x+100,h*.95),fill=(115,185,131))
        d.rectangle((0,int(h*.84),w,h),fill=(119,160,115))
    elif kind=="night":
        for j in range(35):
            x=(j*113+19)%w;y=(j*71+17)%int(h*.7)
            d.ellipse((x,y,x+3,y+3),fill=(248,236,179))
        d.rectangle((0,int(h*.84),w,h),fill=(53,49,87))
    else:
        d.rectangle((0,int(h*.84),w,h),fill=(178,164,193))
        d.ellipse((w-125,28,w-70,83),fill=(255,246,206))
    return im
def draw_actor(im,profile,pose,expression,t):
    w,h=im.size;d=ImageDraw.Draw(im)
    x=int(w*profile.get("x",.5));y=int(h*.49)
    assert .2<=profile.get("x",.5)<=.8
    skin=(241,191,153);cloth=PALETTES[profile["color"]]
    lift=30*math.sin(math.pi*ease(t)) if pose=="jump" else 0
    bob=4*math.sin(2*math.pi*t) if pose=="walk" else 0
    y=int(y-lift+bob)
    # silhouette, legs, arms, torso, head, hair and facial expression are independent draw layers
    leg=14*math.sin(4*math.pi*t) if pose=="walk" else 0
    d.line((x-19,y+123,x-20-leg,y+174),fill=(57,57,76),width=13)
    d.line((x+19,y+123,x+20+leg,y+174),fill=(57,57,76),width=13)
    d.rounded_rectangle((x-47,y+38,x+47,y+137),radius=21,fill=cloth)
    d.line((x-41,y+62,x-76,y+112),fill=skin,width=13)
    arm_y=y+108
    if pose=="wave":arm_y=y-18-14*math.sin(4*math.pi*t)
    d.line((x+41,y+62,x+78,arm_y),fill=skin,width=13)
    d.ellipse((x-46,y-57,x+46,y+42),fill=skin)
    hair=profile.get("hair","dark")
    hair_color={"dark":(65,47,73),"brown":(108,67,47),"gold":(192,142,72)}[hair]
    d.pieslice((x-49,y-66,x+49,y+24),180,360,fill=hair_color)
    if expression=="sleepy":
        for dx in (-19,19):d.arc((x+dx-9,y-2,x+dx+9,y+8),0,180,fill=(44,36,52),width=3)
    else:
        for dx in (-19,19):d.ellipse((x+dx-4,y-2,x+dx+4,y+6),fill=(44,36,52))
    if expression=="happy":d.arc((x-15,y+10,x+15,y+29),0,180,fill=(117,57,73),width=3)
    elif expression=="surprised":d.ellipse((x-6,y+15,x+6,y+30),fill=(117,57,73))
    elif expression=="sad":d.arc((x-15,y+19,x+15,y+38),180,360,fill=(117,57,73),width=3)
    else:d.line((x-10,y+23,x+10,y+23),fill=(117,57,73),width=3)
def caption(im,message):
    if not message:return
    w,h=im.size;d=ImageDraw.Draw(im)
    f=font(19);maxwidth=w-86;lines=[];current=""
    for word in message.split():
        test=(current+" "+word).strip()
        if d.textbbox((0,0),test,font=f)[2]>maxwidth and current:
            lines.append(current);current=word
        else:current=test
    if current:lines.append(current)
    if len(lines)>3:raise ValueError("Caption exceeds three lines")
    height=18+len(lines)*26
    top=h-height-12
    d.rounded_rectangle((22,top,w-22,h-12),radius=12,fill=(255,255,255),outline=(69,62,94),width=2)
    for j,line in enumerate(lines):
        width=d.textbbox((0,0),line,font=f)[2]
        d.text(((w-width)/2,top+8+j*26),line,font=f,fill=(36,32,55))
def frame(w,h,shot,profile,t,show_caption=True):
    bg=shot["background"];assert bg in SCENERY
    pose=shot.get("pose","idle");expression=shot.get("expression","happy")
    assert pose in ("idle","wave","jump","walk")
    assert expression in ("happy","surprised","sad","sleepy","neutral")
    im=backdrop(w,h,bg)
    draw_actor(im,profile,pose,expression,t)
    if show_caption:caption(im,shot.get("caption",""))
    return im
def render(story,profiles,root=Path("output")):
    name=story["name"];assert name and all(c.isalnum() or c in "_-" for c in name)
    w,h=map(int,story.get("size",[640,360]));fps=int(story.get("fps",12))
    assert 320<=w<=1280 and 240<=h<=720 and 1<=fps<=24
    shots=story["shots"];assert 1<=len(shots)<=12
    folder=root/name;folder.mkdir(parents=True,exist_ok=True)
    frames=folder/"frames";frames.mkdir(exist_ok=True)
    for stale in frames.glob("frame_*.png"):stale.unlink()
    all_frames=[]
    for shot in shots:
        profile=profiles[shot["character"]]
        assert profile["color"] in PALETTES and profile.get("hair","dark") in ("dark","brown","gold")
        count=round(float(shot["duration"])*fps);assert fps//2<=count<=fps*10
        sequence=[frame(w,h,shot,profile,i/max(1,count-1),show_caption=False) for i in range(count)]
        # Crossfade the first few frames of each new shot into the previous shot.
        if all_frames and shot.get("transition","cut")=="fade":
            fade=min(6,len(sequence),len(all_frames))
            prior=all_frames[-1]
            for i in range(fade):
                alpha=ease((i+1)/fade)
                sequence[i]=Image.blend(prior,sequence[i],alpha)
        for im in sequence:caption(im,shot.get("caption",""))
        all_frames.extend(sequence)
    for i,im in enumerate(all_frames):im.save(frames/f"frame_{i:04d}.png")
    # GIF delay is quantized to 10 ms. Distribute rounding error across frames.
    delays=[round((i+1)*100/fps)-round(i*100/fps) for i in range(len(all_frames))]
    delays=[10*d for d in delays]
    all_frames[0].save(folder/(name+".gif"),save_all=True,append_images=all_frames[1:],duration=delays,loop=0,optimize=False,disposal=2)
    if not shutil.which("ffmpeg"):raise RuntimeError("FFmpeg required")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(fps),"-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(folder/(name+".mp4"))],check=True)
    print("Phase4:",name,"shots",len(shots),"frames",len(all_frames))
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--config",default="phase4.json");a=p.parse_args()
    data=json.loads(Path(a.config).read_text())
    for story in data["stories"]:render(story,data["characters"])
