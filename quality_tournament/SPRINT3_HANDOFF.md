# Quality Tournament Sprint 3 handoff — 2026-11-05

## Preserved baseline
Blender: real 40-frame 5-second MP4/GIF, visually primitive. Synfig: native 40 frames, static image, not a waving animation. All prior MediaPipe, audio, storyboard, GIF/MP4 workflows preserved.

## New
- Candidate heroine image generated in chat (not uploaded into GitHub; user approval pending). Do not imply repo contains approved PNG.
- START_WAN_WINDOWS.cmd: double-click launcher for a Windows PC with NVIDIA RTX GPU, after downloading/cloning the repository.
- launch_wan_windows.ps1: explicit Windows-only checks, VRAM threshold, disk threshold, minimum model-file sizes, CUDA probe, localhost-only server. The size checks are not SHA-256 verification. It does not auto-download model weights or auto-render.
- wan_benchmark.json: reproducible 5s 24fps 768x432 target and lower-resolution shorter smoke test. Fixed seed, prompt and negative prompt. Exact Wan template node parameters still need verification on a GPU-capable system.
- validate_sprint3.py / wan-readiness.yml: CPU CI checks of manifest and launcher safety strings. **Static tests do not prove PowerShell runtime or GPU compatibility.**

## Installation caveats
PowerShell 5.1+ and Python 3.11 launcher, Git, NVIDIA drivers, sufficient disk, CUDA PyTorch, internet for installation. Script is designed for Windows only; no direct access to the user's computer. Model checkpoints must be obtained from the official ComfyUI/Wan 2.2 workflow and exact per-file licenses checked. At least 45 GB free at preflight; ~18GB models. 8GB VRAM is a plausible *offload* configuration, not guaranteed to succeed. User must place approved character image in local ComfyUI input directory, select official Wan 2.2 5B image-to-video template, set prompt and seed and generate. Do not claim one-click final video yet.

## OpenToonz and VTuber paths
OpenToonz (https://opentoonz.github.io/e/) is relevant for hand-drawn animation, cleanup, palette control and compositing. It cannot produce high-quality anime without high-quality original drawings; no OpenToonz binary or rendered scene verified in this sprint.
Inochi Creator (https://github.com/Inochi2D/inochi-creator) is relevant to expressive face puppetry; requires original segmented eyes, eyebrows, hair, mouth and body parts, plus manual rigging. No tested rig or output yet. OpenToonz and Inochi2D are **readiness/research**, not verified engines.
Video-to-video model stylization remains untested. No paid APIs were used. New software/API cash: $0, not accounting for storage/electricity/CI usage.

## Next action
1. Confirm static CI run and correct any failures within two attempts.
2. User approves/revises original candidate heroine reference.
3. On user's Windows RTX PC, download repo and double-click START_WAN_WINDOWS.cmd. Inspect preflight and CUDA checks; record VRAM and errors.
4. Install official 5B model files; run short smoke test and inspect actual video. If successful, attempt full 5-second target. Do not claim success before artifact exists.
5. Build fair visual comparison against Blender and Synfig; only score genuinely rendered outputs.
