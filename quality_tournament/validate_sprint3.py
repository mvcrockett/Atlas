"""CPU-only readiness validation; does not claim GPU/model execution."""
import json,pathlib,re
root=pathlib.Path(__file__).resolve().parent
bench=json.loads((root/"wan_benchmark.json").read_text())
assert bench["target"]["seconds"]==5
assert bench["target"]["frames"]==120
assert bench["execution"]["video_generated"] is False
ps=(root/"launch_wan_windows.ps1").read_text()
for needle in ("nvidia-smi","AvailableFreeSpace","torch.cuda.is_available","127.0.0.1","diffusion_models","text_encoders","vae","-CheckOnly","-SkipInstall"):
 assert needle in ps,needle
assert "0.0.0.0" not in ps
assert (root/"START_WAN_WINDOWS.cmd").exists()
print("PASS static Windows launcher + benchmark checks. NO GPU execution or video generation.")
