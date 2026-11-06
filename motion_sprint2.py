"""Sprint 2: rights-documented real-person footage -> MediaPipe Pose -> original gesture animation.
Fail closed: no synthetic fallback, no fabricated landmark data.
"""
import json,math,subprocess,urllib.request
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path("output/motion_sprint2")
SOURCE="https://commons.wikimedia.org/wiki/Special:Redirect/file/HandWaveExample.webm"
MODEL="https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
def download(url,path):
    req=urllib.request.Request(url,headers={"User-Agent":"OperationNoPantsResearch/0.1 (noncommercial test; contact via GitHub mvcrockett/Atlas)"})
    with urllib.request.urlopen(req,timeout=45) as response:
        data=response.read(15_000_000)
    if len(data)<10000:raise RuntimeError("Downloaded source unexpectedly small")
    path.write_bytes(data)
def main():
    import mediapipe as mp
    ROOT.mkdir(parents=True,exist_ok=True)
    video=ROOT/"source.webm";model=ROOT/"pose_landmarker.task"
    download(SOURCE,video);download(MODEL,model)
    frames=ROOT/"decoded";frames.mkdir(exist_ok=True)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(video),"-vf","fps=8,scale=480:-2","-frames:v","40",str(frames/"frame_%04d.png")],check=True)
    from mediapipe.tasks import python
    from mediapipe.tasks.python import vision
    opts=vision.PoseLandmarkerOptions(base_options=python.BaseOptions(model_asset_path=str(model)),running_mode=vision.RunningMode.VIDEO,num_poses=1,min_pose_detection_confidence=.3,min_pose_presence_confidence=.3,min_tracking_confidence=.3)
    found=[];files=sorted(frames.glob("*.png"))
    with vision.PoseLandmarker.create_from_options(opts) as landmarker:
        for i,path in enumerate(files):
            frame=mp.Image.create_from_file(str(path))
            result=landmarker.detect_for_video(frame,i*125)
            if not result.pose_landmarks:found.append(None);continue
            marks=result.pose_landmarks[0]
            found.append({n:{"x":round(marks[j].x,5),"y":round(marks[j].y,5),"visibility":round(marks[j].visibility or 0,4)} for n,j in (("left_shoulder",11),("left_elbow",13),("left_wrist",15),("right_shoulder",12),("right_elbow",14),("right_wrist",16))})
    coverage=sum(x is not None for x in found)/len(found)
    if coverage<.35:raise RuntimeError(f"Human pose detection coverage insufficient: {coverage:.1%}")
    side=max(("left","right"),key=lambda s:sum(x is not None and min(x[s+"_shoulder"]["visibility"],x[s+"_elbow"]["visibility"],x[s+"_wrist"]["visibility"])>.35 for x in found))
    usable=[(i,x) for i,x in enumerate(found) if x and min(x[side+"_shoulder"]["visibility"],x[side+"_elbow"]["visibility"],x[side+"_wrist"]["visibility"])>.35]
    if len(usable)<6:raise RuntimeError(f"Insufficient visible {side} arm landmarks: {len(usable)}")
    jitter=[]
    for (i,a),(j,b) in zip(usable,usable[1:]):
        if j==i+1:
            jitter.append(math.dist((a[side+"_wrist"]["x"],a[side+"_wrist"]["y"]),(b[side+"_wrist"]["x"],b[side+"_wrist"]["y"])))
    summary={"source":SOURCE,"source_page":"https://commons.wikimedia.org/wiki/File:HandWaveExample.webm","creator":"NMu11er","license":"CC BY-SA 4.0","license_url":"https://creativecommons.org/licenses/by-sa/4.0/","changes":"downsampled for pose tracking; landmark retargeting into original figure","model":MODEL,"engine":"MediaPipe Pose Landmarker lite","frames":len(found),"detected_frames":sum(x is not None for x in found),"detection_coverage":round(coverage,4),"tracked_arm":side,"visible_arm_frames":len(usable),"consecutive_wrist_displacement_mean_normalized":round(sum(jitter)/len(jitter),5) if jitter else None,"landmarks":found}
    (ROOT/"pose.json").write_text(json.dumps(summary,indent=2))
    out=ROOT/"render_frames";out.mkdir(exist_ok=True)
    pictures=[]
    for k,(i,x) in enumerate(usable):
        im=Image.new("RGB",(480,270),(22,24,45));d=ImageDraw.Draw(im)
        # Retarget relative arm angles from tracked joints to a different original cartoon character.
        pts=[x[side+"_"+part] for part in ("shoulder","elbow","wrist")]
        anchor=(238,122);scale=280
        coords=[anchor]+[(round(anchor[0]+(p["x"]-pts[0]["x"])*scale),round(anchor[1]+(p["y"]-pts[0]["y"])*scale)) for p in pts[1:]]
        d.ellipse((205,52,265,112),fill=(235,178,157),outline=(85,53,99),width=3)
        d.polygon([(207,113),(268,113),(287,266),(188,266)],fill=(105,76,156))
        d.line(coords,fill=(241,191,169),width=19,joint="curve")
        for xx,yy in coords:d.ellipse((xx-5,yy-5,xx+5,yy+5),fill=(253,214,191))
        d.text((15,15),"REAL HUMAN POSE / ORIGINAL CARTOON RETARGET",fill=(240,219,244))
        im.save(out/f"frame_{k:04d}.png");pictures.append(im)
    pictures[0].save(ROOT/"motion.gif",save_all=True,append_images=pictures[1:],duration=125,loop=0,disposal=2)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","8","-i",str(out/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(ROOT/"motion.mp4")],check=True)
    print(f"PASS real-person MediaPipe: {len(files)} frames; coverage {coverage:.1%}; visible {side} arm {len(usable)}; mean wrist step {summary['consecutive_wrist_displacement_mean_normalized']}")
if __name__=="__main__":main()
