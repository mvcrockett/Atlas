"""Motion Sprint 2.1: fixed-length 2D IK retargeting of real MediaPipe landmarks.
Reuses documented CC BY-SA 4.0 group footage; single-person identity NOT verified.
"""
import json,math,subprocess
from pathlib import Path
from PIL import Image,ImageDraw
from motion_sprint2 import ROOT
OUT=Path("output/motion_sprint21")
FPS=8; SHOULDER=(238,132); UPPER=62.; FOREARM=59.
def unit(a,b,fallback=(1.,0.)):
    dx,dy=b[0]-a[0],b[1]-a[1];r=math.hypot(dx,dy)
    return (dx/r,dy/r) if r>1e-6 else fallback
def smooth(v):
    # circular angle smoothing via weighted unit vectors, not naive wrapped-angle averaging
    out=[]
    for i in range(len(v)):
        pts=v[max(0,i-1):min(len(v),i+2)]
        x=sum(math.cos(t) for t in pts);y=sum(math.sin(t) for t in pts)
        out.append(math.atan2(y,x))
    return out
def main():
    source=json.loads((ROOT/"pose.json").read_text())
    frames=source["landmarks"];side=source["tracked_arm"]
    records=[]
    for i,f in enumerate(frames):
        if f is None:continue
        points=[f[side+"_"+part] for part in ("shoulder","elbow","wrist")]
        if min(p["visibility"] for p in points)<.35:continue
        a,b,c=[(p["x"],p["y"]) for p in points]
        if math.dist(a,b)<.025 or math.dist(b,c)<.025:continue
        v1=unit(a,b);v2=unit(b,c)
        records.append((i,math.atan2(v1[1],v1[0]),math.atan2(v2[1],v2[0])))
    if len(records)<6:raise RuntimeError("Not enough reliable real-person landmarks")
    angles1=smooth([r[1] for r in records]);angles2=smooth([r[2] for r in records])
    OUT.mkdir(parents=True,exist_ok=True);folder=OUT/"frames";folder.mkdir(exist_ok=True)
    pictures=[];errors=[];raw_steps=[];smoothed_steps=[]
    for k,((i,a,b),aa,bb) in enumerate(zip(records,angles1,angles2)):
        elbow=(SHOULDER[0]+UPPER*math.cos(aa),SHOULDER[1]+UPPER*math.sin(aa))
        wrist=(elbow[0]+FOREARM*math.cos(bb),elbow[1]+FOREARM*math.sin(bb))
        errors.extend([abs(math.dist(SHOULDER,elbow)-UPPER),abs(math.dist(elbow,wrist)-FOREARM)])
        if k:
            raw_steps.append(math.hypot(math.cos(a)-math.cos(records[k-1][1]),math.sin(a)-math.sin(records[k-1][1])))
            smoothed_steps.append(math.hypot(math.cos(aa)-math.cos(angles1[k-1]),math.sin(aa)-math.sin(angles1[k-1])))
        im=Image.new("RGB",(480,270),(20,24,45));d=ImageDraw.Draw(im)
        d.ellipse((206,57,269,120),fill=(235,181,163),outline=(73,49,91),width=3)
        d.polygon([(207,122),(270,122),(292,268),(190,268)],fill=(97,76,155))
        d.line([(207,137),(177,184),(160,227)],fill=(235,181,163),width=16,joint="curve")
        d.line([SHOULDER,elbow,wrist],fill=(240,186,166),width=18,joint="curve")
        for x,y in (SHOULDER,elbow,wrist):d.ellipse((x-5,y-5,x+5,y+5),fill=(252,221,194))
        d.text((12,14),"FIXED-LENGTH RETARGET / REAL MEDIAPIPE DATA",fill=(235,220,250))
        im.save(folder/f"frame_{k:04d}.png");pictures.append(im)
    assert max(errors)<1e-8,max(errors)
    assert len(pictures)>=6
    pictures[0].save(OUT/"motion.gif",save_all=True,append_images=pictures[1:],duration=125,loop=0,disposal=2)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",str(folder/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(OUT/"motion.mp4")],check=True)
    # compare first/mid/end of original and new renders using actual output GIF frames
    old=Image.open(ROOT/"motion.gif");new=Image.open(OUT/"motion.gif")
    sheet=Image.new("RGB",(960,270*3))
    for row,idx in enumerate((0,len(pictures)//2,len(pictures)-1)):
        old.seek(min(idx,old.n_frames-1));new.seek(min(idx,new.n_frames-1))
        sheet.paste(old.convert("RGB"),(0,row*270));sheet.paste(new.convert("RGB"),(480,row*270))
    sheet.save(OUT/"before_after.png")
    report={"source_pose_json":"output/motion_sprint2/pose.json","source_license":source["license"],"source_page":source["source_page"],"identity_verified":False,"reason":"Existing reference shows a group; cannot establish same tracked person","original_detected_coverage":source["detection_coverage"],"frames_total":len(frames),"frames_used":len(records),"usable_coverage":round(len(records)/len(frames),4),"upper_arm_length_px":UPPER,"forearm_length_px":FOREARM,"maximum_bone_length_error_px":max(errors),"mean_raw_upper_arm_direction_step":sum(raw_steps)/len(raw_steps) if raw_steps else None,"mean_smoothed_upper_arm_direction_step":sum(smoothed_steps)/len(smoothed_steps) if smoothed_steps else None,"jitter_note":"Angular step contains genuine movement as well as jitter; smoothing may reduce real motion.","quality_gate":"fixed-length IK verified; single-person identity and artistic quality not verified"}
    (OUT/"metrics.json").write_text(json.dumps(report,indent=2))
    print("PASS fixed bone lengths, tracked frame coverage, actual GIF/MP4 and before-after",json.dumps(report))
if __name__=="__main__":main()
