"""Continuous Anime Engine v0.1: honest CPU optical-flow inbetweening.
Inputs: continuous_engine/keyframes/*.png (ordered) or original synthetic fixture.
No generative anatomy, no RIFE, no claim of approved character artwork.
"""
import argparse,json,math,time
from pathlib import Path
import cv2,numpy as np
from PIL import Image,ImageDraw
ROOT=Path("output/continuous_engine")
def fixture(out):
 out.mkdir(parents=True,exist_ok=True)
 for i in range(9):
  t=i/8; im=Image.new("RGB",(480,270),(26,25,45)); d=ImageDraw.Draw(im)
  # Original procedural stylized lavender heroine TEST ASSET, not approved anime reference
  d.ellipse((167,67,313,266),fill=(112,79,158))
  d.ellipse((202,33,278,119),fill=(231,175,155))
  d.pieslice((196,23,283,88),180,360,fill=(61,35,76))
  for x in (222,257): d.ellipse((x-4,75,x+4,83),fill=(36,85,69))
  d.arc((224,85,257,101),0,180,fill=(110,49,67),width=2)
  # A deliberately moving forearm/hand: useful optical-flow stress test
  angle=math.radians(-60+105*math.sin(math.pi*t))
  sx,sy=296,157; ex=sx+int(74*math.cos(angle));ey=sy-int(74*math.sin(angle))
  d.line((sx,sy,ex,ey),fill=(231,175,155),width=17)
  d.ellipse((ex-13,ey-13,ex+13,ey+13),fill=(231,175,155))
  im.save(out/f"key_{i:03d}.png")
def flow_interpolate(a,b,t):
 # Farneback is CPU optical flow, NOT learned RIFE. Blend warped endpoints.
 gray_a=cv2.cvtColor(a,cv2.COLOR_RGB2GRAY);gray_b=cv2.cvtColor(b,cv2.COLOR_RGB2GRAY)
 fa=cv2.calcOpticalFlowFarneback(gray_a,gray_b,None,.5,4,21,4,7,1.5,0)
 fb=cv2.calcOpticalFlowFarneback(gray_b,gray_a,None,.5,4,21,4,7,1.5,0)
 h,w=gray_a.shape;xx,yy=np.meshgrid(np.arange(w,dtype=np.float32),np.arange(h,dtype=np.float32))
 wa=cv2.remap(a,xx-fa[:,:,0]*t,yy-fa[:,:,1]*t,cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
 wb=cv2.remap(b,xx-fb[:,:,0]*(1-t),yy-fb[:,:,1]*(1-t),cv2.INTER_LINEAR,borderMode=cv2.BORDER_REFLECT)
 return cv2.addWeighted(wa,1-t,wb,t,0)
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--keyframes",default="continuous_engine/keyframes");ap.add_argument("--method",choices=["flow","blend"],default="flow");args=ap.parse_args()
 ROOT.mkdir(parents=True,exist_ok=True);source=Path(args.keyframes)
 files=sorted(source.glob("*.png"))
 fixture_used=False
 if len(files)<2:
  fixture(ROOT/"fixture");files=sorted((ROOT/"fixture").glob("*.png"));fixture_used=True
 assert len(files)>=2
 images=[np.array(Image.open(p).convert("RGB").resize((480,270))) for p in files]
 assert len({a.shape for a in images})==1
 frame_dir=ROOT/"frames";frame_dir.mkdir(exist_ok=True)
 start=time.monotonic();out=[];total=120
 for n in range(total):
  pos=n*(len(images)-1)/(total-1);i=min(int(pos),len(images)-2);t=pos-i
  if t<=1e-8:frame=images[i].copy()
  elif t>=1-1e-8:frame=images[i+1].copy()
  elif args.method=="flow":frame=flow_interpolate(images[i],images[i+1],t)
  else:frame=cv2.addWeighted(images[i],1-t,images[i+1],t,0)
  out.append(frame)
  Image.fromarray(frame).save(frame_dir/f"frame_{n:04d}.png")
 import imageio.v2 as imageio
 import imageio_ffmpeg
 writer=imageio.get_writer(str(ROOT/"continuous.mp4"),fps=24,codec="libx264",quality=7,macro_block_size=1,ffmpeg_log_level="error")
 for frame in out:writer.append_data(frame)
 writer.close()
 Image.fromarray(out[0]).save(ROOT/"continuous.gif",save_all=True,append_images=[Image.fromarray(x) for x in out[1:]],duration=42,loop=0,optimize=False)
 diffs=[float(np.mean(np.abs(out[i].astype(np.float32)-out[i-1].astype(np.float32)))) for i in range(1,total)]
 jumps=[i for i,x in enumerate(diffs,1) if x>18]
 metrics={"method":args.method,"optical_flow":"Farneback CPU (not RIFE, not generative AI)","frame_count":total,"fps":24,"seconds":5,"keyframe_count":len(files),"fixture_used":fixture_used,"candidate_art_approved":False,"real_ai_keyframes_used":not fixture_used,"frame_resolution":[480,270],"mean_frame_difference":float(np.mean(diffs)),"max_frame_difference":max(diffs),"large_pixel_change_frame_indices":jumps,"render_seconds":round(time.monotonic()-start,2),"anatomy_verified":False,"identity_consistency_verified":False,"limitations":"Optical flow warps and blends pixels; cannot draw missing fingers or unseen anatomy. Pixel difference alone does not measure perceptual flicker. Manual visual inspection required.","paid_api_usd":0}
 (ROOT/"metrics.json").write_text(json.dumps(metrics,indent=2))
 assert len(out)==120 and (ROOT/"continuous.mp4").stat().st_size>10000
 print(json.dumps(metrics,indent=2))
if __name__=="__main__":main()
