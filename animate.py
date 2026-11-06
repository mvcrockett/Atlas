from PIL import Image, ImageDraw
from pathlib import Path
import math, subprocess, shutil

OUT=Path("output")
FRAMES=OUT/"frames"
FRAMES.mkdir(parents=True,exist_ok=True)
W,H=640,360
for i in range(48):
    im=Image.new("RGB",(W,H),(13,51,85))
    d=ImageDraw.Draw(im)
    for x in range(0,W,70):
        d.arc((x,15,x+120,75),0,180,fill=(36,105,145),width=2)
    cx=int(110+420*i/47)
    cy=int(175+18*math.sin(i*.25))
    d.ellipse((cx-65,cy-37,cx+65,cy+37),fill=(255,171,71),outline=(255,221,140),width=4)
    d.polygon([(cx-58,cy),(cx-115,cy-48),(cx-115,cy+48)],fill=(247,126,71))
    d.ellipse((cx+34,cy-17,cx+44,cy-7),fill=(18,35,45))
    d.arc((cx+40,cy-4,cx+58,cy+14),0,140,fill=(18,35,45),width=2)
    d.polygon([(cx-10,cy-33),(cx-35,cy-60),(cx+20,cy-35)],fill=(252,201,90))
    for j in range(5):
        bx=(i*7+j*115)%W
        by=H-((i*4+j*75)%H)
        d.ellipse((bx,by,bx+9,by+9),outline=(118,202,227),width=2)
    im.save(FRAMES/f"frame_{i:04d}.png")
if shutil.which("ffmpeg"):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","12","-i",str(FRAMES/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(OUT/"fish.mp4")],check=True)
images=[Image.open(p) for p in sorted(FRAMES.glob("*.png"))]
images[0].save(OUT/"fish.gif",save_all=True,append_images=images[1:],duration=83,loop=0,optimize=True)
print("Created",OUT/"fish.gif")
