"""Sprint 2.3 diagnostic: real source video with MediaPipe overlay beside rig.
Conservative identity flags: no single-person source verified, so no identity success claim.
"""
import json,math,subprocess,statistics
from pathlib import Path
from PIL import Image,ImageDraw
from motion_sprint21 import ROOT
OUT=Path("output/motion_sprint23")
def main():
    pose=json.loads((ROOT/"pose.json").read_text());side=pose["tracked_arm"]
    raw=pose["landmarks"];frames=sorted((ROOT/"decoded").glob("frame_*.png"))
    if len(frames)!=len(raw):raise RuntimeError(f"Source/video alignment mismatch {len(frames)} vs {len(raw)}")
    rig=Image.open("output/motion_sprint22/motion.gif")
    OUT.mkdir(parents=True,exist_ok=True)
    images=[];displacements=[];flags=[];last=None
    for i,(path,landmarks) in enumerate(zip(frames,raw)):
        src=Image.open(path).convert("RGB").resize((480,270))
        d=ImageDraw.Draw(src)
        if landmarks:
            for prefix in ("left","right"):
                pts=[]
                for name in ("shoulder","elbow","wrist"):
                    p=landmarks[prefix+"_"+name];pts.append((round(p["x"]*480),round(p["y"]*270)))
                d.line(pts,fill=(255,50,70) if prefix==side else (68,220,246),width=5)
                for x,y in pts:d.ellipse((x-4,y-4,x+4,y+4),fill=(255,245,125))
            wrist=landmarks[side+"_wrist"]
            xy=(wrist["x"]*480,wrist["y"]*270)
            if last:
                step=math.dist(xy,last);displacements.append(step)
                if step>45:flags.append({"frame":i,"reason":"large source wrist jump","step_px":round(step,2)})
            last=xy
        else:
            flags.append({"frame":i,"reason":"pose missing"});last=None
        rig.seek(min(i,rig.n_frames-1))
        sheet=Image.new("RGB",(960,270));sheet.paste(src,(0,0));sheet.paste(rig.convert("RGB"),(480,0))
        dd=ImageDraw.Draw(sheet)
        dd.rectangle((0,0,480,21),fill=(10,10,25));dd.text((8,4),"LICENSED SOURCE + TRACKED MEDIAPIPE JOINTS",fill=(250,250,250))
        dd.rectangle((480,0,960,21),fill=(10,10,25));dd.text((488,4),"SPRINT 2.2 RIG (EXISTING VERIFIED RENDER)",fill=(250,250,250))
        images.append(sheet)
    assert len(images)>=6
    images[0].save(OUT/"diagnostic.gif",save_all=True,append_images=images[1:],duration=125,loop=0,disposal=2)
    folder=OUT/"frames";folder.mkdir(exist_ok=True)
    for i,img in enumerate(images):img.save(folder/f"frame_{i:04d}.png")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","8","-i",str(folder/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(OUT/"diagnostic.mp4")],check=True)
    images[0].save(OUT/"comparison_first.png");images[len(images)//2].save(OUT/"comparison_middle.png")
    report={"source_page":pose["source_page"],"creator":pose["creator"],"license":pose["license"],"license_url":pose["license_url"],"single_person_reference_verified":False,"identity_verified":False,"reason":"Source contains multiple performers; PoseLandmarker num_poses=1 is not identity verification.","frames":len(raw),"detected":sum(f is not None for f in raw),"coverage":round(sum(f is not None for f in raw)/len(raw),4),"mean_source_wrist_step_px":round(statistics.mean(displacements),3) if displacements else None,"max_source_wrist_step_px":round(max(displacements),3) if displacements else None,"threshold_px":45,"flagged_frames":flags,"flag_count":len(flags),"identity_switch_detected":None,"warning":"Large displacement is not proof of identity switching or tracking error; camera/real motion can cause jumps. This diagnostic compares source joint overlays with previously rendered character, not new motion retargeting.","reference_candidates":[{"page":"https://commons.wikimedia.org/wiki/File:Head_Shake.webm","license":"CC BY-SA 4.0","decision":"Not accepted: head-shake action does not establish a single-person arm-gesture benchmark"},{"page":"https://commons.wikimedia.org/wiki/File:Hand_Animation.webm","license":"CC0","decision":"Not accepted: animation, not real-person full-body gesture"}]}
    (OUT/"metrics.json").write_text(json.dumps(report,indent=2))
    print("PASS side-by-side diagnostic; identity NOT verified",json.dumps({k:v for k,v in report.items() if k not in ("flagged_frames","reference_candidates")}))
if __name__=="__main__":main()
