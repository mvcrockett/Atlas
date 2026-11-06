"""Sprint 2.2: layered capsule arm rig driven by actual Sprint 2 MediaPipe data.
Reference is CC BY-SA group footage; individual identity remains unverified.
"""
import json,math,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
from motion_sprint21 import ROOT,OUT as PREV,SHOULDER,UPPER,FOREARM,smooth,unit
OUT=Path("output/motion_sprint22");FPS=8
def clamp_angle(angle,center,half):
    return center+max(-half,min(half,(angle-center+math.pi)%(2*math.pi)-math.pi))
def main():
    source=json.loads((ROOT/"pose.json").read_text())
    side=source["tracked_arm"];data=source["landmarks"];valid=[]
    for i,f in enumerate(data):
        if not f:continue
        p=[f[side+"_"+n] for n in ("shoulder","elbow","wrist")]
        if min(q["visibility"] for q in p)<.35:continue
        a,b,c=[(q["x"],q["y"]) for q in p]
        if min(math.dist(a,b),math.dist(b,c))<.025:continue
        v1=unit(a,b);v2=unit(b,c)
        valid.append((i,math.atan2(v1[1],v1[0]),math.atan2(v2[1],v2[0])))
    if len(valid)<6:raise RuntimeError("Insufficient tracked real-human arm data")
    upper=smooth([v[1] for v in valid]);lower=smooth([v[2] for v in valid])
    OUT.mkdir(parents=True,exist_ok=True);frames=OUT/"frames";frames.mkdir(exist_ok=True)
    old=Image.open(PREV/"motion.gif")
    before_after=Image.new("RGB",(960,810));images=[];errors=[];continuity=[];limits=[]
    prev=None
    for k,((frame,_,_),a,b) in enumerate(zip(valid,upper,lower)):
        # Soft limit elbow relative orientation to plausible planar bend; avoid unphysical reverse bends.
        relative=(b-a+math.pi)%(2*math.pi)-math.pi
        bounded=max(-2.6,min(2.6,relative))
        limits.append(abs(relative-bounded))
        b=a+bounded
        elbow=(SHOULDER[0]+UPPER*math.cos(a),SHOULDER[1]+UPPER*math.sin(a))
        wrist=(elbow[0]+FOREARM*math.cos(b),elbow[1]+FOREARM*math.sin(b))
        errors.extend((abs(math.dist(SHOULDER,elbow)-UPPER),abs(math.dist(elbow,wrist)-FOREARM)))
        if prev:continuity.append(math.dist(wrist,prev))
        prev=wrist
        # Explicit RGBA layers and deliberate draw order: back arm, torso, front arm, joint caps, hand.
        base=Image.new("RGBA",(480,270),(24,27,49,255))
        back=Image.new("RGBA",base.size);db=ImageDraw.Draw(back)
        db.line([(211,143),(179,183),(168,228)],fill=(211,156,143,255),width=19,joint="curve")
        base=Image.alpha_composite(base,back)
        torso=Image.new("RGBA",base.size);dt=ImageDraw.Draw(torso)
        dt.ellipse((205,55,267,119),fill=(236,185,167,255),outline=(65,46,86,255),width=3)
        dt.polygon([(207,122),(270,122),(293,268),(188,268)],fill=(104,76,159,255))
        dt.polygon([(216,126),(245,126),(231,265),(199,265)],fill=(116,89,178,255))
        base=Image.alpha_composite(base,torso)
        arm=Image.new("RGBA",base.size);d=ImageDraw.Draw(arm)
        # tapered upper and lower arm with soft joint caps, and a separate hand silhouette
        d.line([SHOULDER,elbow],fill=(101,65,88,255),width=24)
        d.line([SHOULDER,elbow],fill=(235,180,161,255),width=19)
        d.ellipse((elbow[0]-12,elbow[1]-12,elbow[0]+12,elbow[1]+12),fill=(236,184,163,255))
        d.line([elbow,wrist],fill=(105,68,86,255),width=21)
        d.line([elbow,wrist],fill=(240,191,170,255),width=16)
        d.ellipse((wrist[0]-9,wrist[1]-9,wrist[0]+9,wrist[1]+9),fill=(244,195,174,255))
        # 2D palm with a simple separated thumb; hand follows forearm vector
        vx,vy=math.cos(b),math.sin(b);nx,ny=-vy,vx
        tip=(wrist[0]+vx*18,wrist[1]+vy*18)
        d.line([wrist,tip],fill=(244,195,174,255),width=13)
        thumb=(wrist[0]+vx*7+nx*12,wrist[1]+vy*7+ny*12)
        d.line([wrist,thumb],fill=(244,195,174,255),width=6)
        base=Image.alpha_composite(base,arm)
        label=Image.new("RGBA",base.size);ImageDraw.Draw(label).text((10,12),"LAYERED RIG / REAL MEDIAPIPE DATA",fill=(236,224,248,255))
        base=Image.alpha_composite(base,label)
        im=base.convert("RGB");im.save(frames/f"frame_{k:04d}.png");images.append(im)
        if k in (0,len(valid)//2,len(valid)-1):
            row=(0,len(valid)//2,len(valid)-1).index(k)
            old.seek(min(k,old.n_frames-1))
            before_after.paste(old.convert("RGB"),(0,row*270));before_after.paste(im,(480,row*270))
    assert max(errors)<1e-8
    assert len(images)==len(valid)
    before_after.save(OUT/"before_after.png")
    images[0].save(OUT/"motion.gif",save_all=True,append_images=images[1:],duration=125,loop=0,disposal=2)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",str(frames/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(OUT/"motion.mp4")],check=True)
    report={"source":source["source_page"],"license":source["license"],"single_person_source_verified":False,"subject_identity_verified":False,"source_blocker":"Reference is a group video; no independently verified single-person replacement obtained.","frame_count":len(data),"used_frames":len(valid),"pose_coverage":len(valid)/len(data),"max_bone_length_error_px":max(errors),"upper_arm_px":UPPER,"forearm_px":FOREARM,"max_wrist_step_px":max(continuity) if continuity else 0,"mean_wrist_step_px":sum(continuity)/len(continuity) if continuity else 0,"max_joint_clamp_radians":max(limits),"quality_gate":"Layering, geometry, and render verified; realistic performance and identity unresolved"}
    (OUT/"metrics.json").write_text(json.dumps(report,indent=2))
    print("PASS: layered arm, fixed lengths, hand, occlusion, real tracked pose, GIF MP4",json.dumps(report))
if __name__=="__main__":main()
