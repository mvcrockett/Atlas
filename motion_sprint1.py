"""Zero-cost motion reference MVP: self-authored marker video -> decoded video -> tracked pose JSON -> retargeted character.
Explicitly NOT MediaPipe, human pose estimation, or external public-domain footage.
"""
import json, math, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw
ROOT=Path("output/motion_sprint1"); FPS=12; N=36; W=480; H=270
def run(*args):subprocess.run(["ffmpeg","-y","-loglevel","error",*map(str,args)],check=True)
def main():
    src=ROOT/"source_frames";decoded=ROOT/"decoded";out=ROOT/"render_frames"
    for folder in (src,decoded,out):folder.mkdir(parents=True,exist_ok=True)
    truth=[]
    for i in range(N):
        t=i/(N-1)
        # original studio-owned stylized reference actor, not third-party footage
        shoulder=(175,123);elbow=(218,133-round(48*t));wrist=(260,150-round(105*t))
        truth.append({"frame":i,"shoulder":shoulder,"elbow":elbow,"wrist":wrist})
        im=Image.new("RGB",(W,H),(29,35,54));d=ImageDraw.Draw(im)
        d.ellipse((135,78,195,138),fill=(216,172,151))
        d.polygon([(146,133),(204,133),(214,255),(130,255)],fill=(89,118,172))
        d.line([shoulder,elbow,wrist],fill=(213,174,152),width=16,joint="curve")
        # lossless red marker centers recovered from actual encoded/decoded source
        for x,y in (shoulder,elbow,wrist):d.ellipse((x-4,y-4,x+4,y+4),fill=(255,0,0))
        d.text((15,14),"ORIGINAL SYNTHETIC REFERENCE - RIGHTS: PROJECT OWNED",fill=(238,226,242))
        im.save(src/f"frame_{i:04d}.png")
    run("-framerate",FPS,"-i",src/"frame_%04d.png","-c:v","ffv1",ROOT/"reference.mkv")
    run("-i",ROOT/"reference.mkv",decoded/"frame_%04d.png")
    detected=[]
    for i in range(N):
        im=Image.open(decoded/f"frame_{i+1:04d}.png").convert("RGB")
        # cluster red pixels into three independent connected components
        px=im.load();spots=set()
        for y in range(H):
            for x in range(W):
                r,g,b=px[x,y]
                if r>240 and g<35 and b<35:spots.add((x,y))
        components=[]
        while spots:
            seed=spots.pop();todo=[seed];group=[seed]
            while todo:
                x,y=todo.pop()
                for neighbor in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
                    if neighbor in spots:spots.remove(neighbor);todo.append(neighbor);group.append(neighbor)
            if len(group)>15:components.append((sum(x for x,y in group)/len(group),sum(y for x,y in group)/len(group)))
        if len(components)!=3:raise RuntimeError(f"frame {i}: expected 3 tracked markers, got {len(components)}")
        components.sort(key=lambda p:p[0])
        tracked={name:[round(v,2) for v in pt] for name,pt in zip(("shoulder","elbow","wrist"),components)}
        detected.append({"frame":i,"time_seconds":round(i/FPS,4),**tracked})
    errors=[]
    for a,b in zip(truth,detected):
        for name in ("shoulder","elbow","wrist"):
            errors.append(math.dist(a[name],b[name]))
    mae=sum(errors)/len(errors);assert mae<1.0,mae
    assert detected[-1]["wrist"][1]<detected[0]["wrist"][1]-90
    (ROOT/"motion.json").write_text(json.dumps({"source":"original studio-owned synthetic marker video","method":"red marker connected-component tracking after FFV1 video decode; not MediaPipe","fps":FPS,"mean_marker_error_px":round(mae,3),"frames":detected},indent=2))
    images=[]
    for f in detected:
        im=Image.new("RGB",(W,H),(20,24,44));d=ImageDraw.Draw(im)
        d.ellipse((132,71,196,135),fill=(241,187,170),outline=(73,49,87),width=3)
        d.polygon([(139,132),(200,132),(220,258),(120,258)],fill=(92,66,149))
        d.line([(169,138),(146,184),(134,228)],fill=(237,178,165),width=16,joint="curve")
        shoulder=tuple(f["shoulder"]);elbow=tuple(f["elbow"]);wrist=tuple(f["wrist"])
        d.line([shoulder,elbow,wrist],fill=(241,187,170),width=18,joint="curve")
        for x,y in (shoulder,elbow,wrist):d.ellipse((x-4,y-4,x+4,y+4),fill=(255,219,181))
        d.text((15,14),"RENDERED FROM DECODED VIDEO TRACKING JSON",fill=(239,223,252))
        im.save(out/f"frame_{f['frame']:04d}.png");images.append(im)
    delays=[10*(round((i+1)*100/FPS)-round(i*100/FPS)) for i in range(N)]
    images[0].save(ROOT/"motion.gif",save_all=True,append_images=images[1:],duration=delays,loop=0,disposal=2)
    run("-framerate",FPS,"-i",out/"frame_%04d.png","-c:v","libx264","-pix_fmt","yuv420p",ROOT/"motion.mp4")
    print(f"PASS: video decoded and tracked, {N} frames, 3 landmarks, mean error {mae:.3f}px, retargeted animation")
if __name__=="__main__":main()
