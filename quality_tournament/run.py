"""Same original 5-second character scene: Blender render and Synfig render attempts.
Never report success for an engine unless its own executable created output.
"""
import json,subprocess,shutil,math,os
from pathlib import Path
from PIL import Image
OUT=Path("output/quality_tournament");OUT.mkdir(parents=True,exist_ok=True)
DURATION=5;FPS=8
def run(cmd,timeout=180):
 try:
  p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=timeout)
  return {"exit":p.returncode,"tail":p.stdout[-2200:]}
 except Exception as e:return {"exit":None,"error":str(e)}
def encode(folder,name):
 files=sorted(folder.glob("*.png"))
 if len(files)<10:return False
 mp4=OUT/(name+".mp4")
 p=run(["ffmpeg","-y","-loglevel","error","-framerate",str(FPS),"-i",str(folder/"frame_%04d.png"),"-c:v","libx264","-pix_fmt","yuv420p",str(mp4)],60)
 if p["exit"]!=0:return False
 images=[Image.open(f).convert("RGB") for f in files]
 images[0].save(OUT/(name+".gif"),save_all=True,append_images=images[1:],duration=125,loop=0)
 return True
def main():
 status={}
 for engine in ("blender","synfig"):
  status[engine]={"installed":bool(shutil.which(engine)),"rendered":False,"reason":"not attempted"}
 if status["blender"]["installed"]:
  cmd=["blender","-b","-t","2","--python","quality_tournament/blender_scene.py"]
  res=run(cmd,220)
  status["blender"].update({"render_log":res,"rendered":encode(OUT/"blender_frames","blender") if res["exit"]==0 else False})
  status["blender"]["reason"]="render verified" if status["blender"]["rendered"] else "Blender scene failed or no decoded frames"
 if status["synfig"]["installed"]:
  res=run(["synfig","quality_tournament/character.sif","-t","png","-w","480","-h","270","-o",str(OUT/"synfig_test.png")],90)
  png=OUT/"synfig_test.png"
  status["synfig"].update({"render_log":res,"rendered":res["exit"]==0 and png.exists() and png.stat().st_size>1000})
  status["synfig"]["reason"]="Synfig actual still-frame render (not five-second animation)" if status["synfig"]["rendered"] else "Synfig file/render unsupported; no success claimed"
 status.update({"comfyui_wan22":{"rendered":False,"reason":"No GPU in standard GitHub Actions runner; local RTX 4060 not connected"},"opentoonz":{"rendered":False,"reason":"Not installed/tested in this CPU job"},"vtuber_rig":{"rendered":False,"reason":"No authored face rig or tested runtime"},"video_stylization":{"rendered":False,"reason":"No GPU model installed or licensed input pipeline"}})
 (OUT/"results.json").write_text(json.dumps(status,indent=2))
 print(json.dumps({k:{"rendered":v["rendered"],"reason":v["reason"]} for k,v in status.items()},indent=2))
 if not status["blender"]["rendered"]:raise RuntimeError("Blender must produce actual MP4/GIF or job fails")
if __name__=="__main__":main()
