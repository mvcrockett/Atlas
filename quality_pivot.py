"""Operation No Pants: honest multi-engine quality benchmark readiness.
This is NOT a generated anime comparison. No model downloads, no paid services.
"""
import json, shutil, platform, os
from pathlib import Path

ROOT=Path("output/quality_pivot")
ENGINES={
 "comfyui_wan22":{"family":"AI video","license":"ComfyUI GPL-3.0; Wan2.2 Apache-2.0 (verify each asset)","requires":"Local GPU, ComfyUI, Wan2.2 5B model, text encoder and VAE","runner":"GPU-local","entry":"ComfyUI Wan2.2 5B TI2V official template","official":"https://docs.comfy.org/tutorials/video/wan/wan2_2","executable":None},
 "blender":{"family":"3D anime / Grease Pencil","license":"GPL","requires":"Blender and authored reusable character model","runner":"local CPU/GPU","entry":"blender -b scene.blend -a","official":"https://docs.blender.org/manual/en/latest/advanced/command_line/render.html","executable":"blender"},
 "opentoonz":{"family":"traditional 2D","license":"BSD-style open source; check bundled assets","requires":"OpenToonz and authored scene","runner":"local","entry":"OpenToonz batch render","official":"https://opentoonz.github.io/e/","executable":"OpenToonz"},
 "synfig":{"family":"2D vector rig","license":"GPL","requires":"Synfig CLI and authored scene","runner":"local","entry":"synfig -t png scene.sif","official":"https://wiki.synfig.org/Render_options","executable":"synfig"},
 "vtuber_rig":{"family":"face rig / puppetry","license":"Check selected engine and character asset","requires":"An authored deformable character rig","runner":"local","entry":"Research Inochi2D/Sakura2D compatibility and automation before integration","official":"https://github.com/Inochi2D/inochi-creator","executable":None},
 "video_stylization":{"family":"AI postproduction","license":"Model-specific; verify","requires":"Video-to-video model, local GPU and stable input","runner":"GPU-local","entry":"Evaluate only after stable base character animation","official":"https://docs.comfy.org/","executable":None},
}
def main():
 ROOT.mkdir(parents=True,exist_ok=True)
 rows=[]
 for name,spec in ENGINES.items():
  installed=shutil.which(spec["executable"]) if spec["executable"] else None
  rows.append({"engine":name,**spec,"installed_executable":installed,"rendered":False,"quality_score":None,"status":"not_rendered","reason":"No authored common benchmark character and no verified engine-specific output in this CPU workflow"})
 benchmark={"version":"1.0","scene":{"duration_seconds":5,"target_fps":24,"target_resolution":[768,432],"shot":"Original adult anime-style woman in lavender jacket, waist-up, raises right hand and waves once, neutral camera and background, one subject, no copyrighted character","character_art":"Not yet supplied or approved; do not substitute placeholder art and claim high quality","evaluation":["character identity and facial consistency","anatomy and hands","motion and acting","flicker","render time and hardware use","commercial asset rights"],"score_policy":"No quality scores until comparable outputs exist","environment":{"system":platform.platform(),"cuda_probe":"not performed in CPU CI","github_actions_gpu":"not available on ubuntu-latest standard runner"},"engines":rows,"new_paid_api_spend_usd":0}
 (ROOT/"readiness.json").write_text(json.dumps(benchmark,indent=2))
 assert len(rows)==6
 assert all(r["rendered"] is False and r["quality_score"] is None for r in rows)
 print("PASS: six-engine readiness manifest; NO false anime render claims")
if __name__=="__main__":main()
