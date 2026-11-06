# Quality Tournament Sprint 2 — quality and hardware audit

## Original anime character brief (NOT approved finished art)
Original adult heroine "Lavender": shoulder-length dark plum hair, green eyes, lavender jacket, cream shirt, five-fingered hands, crisp cel shading. No copyrighted franchise likeness. Fixed waist-up camera, neutral background, one performer.

## Shared 5-second benchmark
24 fps at 768x432, 120 frames. Raise right hand, wave once, lower hand. No cuts or dialogue. Evaluate face identity, hair/clothing consistency, fingers, acting, flicker, runtime and licensing. An engine gets a score only after its own actual output is rendered and visually inspected.

## Blender quality audit
Previous actual Blender render was 40 frames at 8 fps, 480x270. Basic geometry, hair cap, minimal face, tube limbs, simple background and insufficient acting. Real engine execution verified; professional anime quality NOT achieved.

## ComfyUI + Wan 2.2 5B local installation
Official tutorial: https://docs.comfy.org/tutorials/video/wan/wan2_2
Model source: https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged
Official template: https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/video_wan2_2_5B_ti2v.json
ComfyUI repository: https://github.com/comfyanonymous/ComfyUI (GPL-3.0)
Wan2.2 repository: https://github.com/Wan-Video/Wan2.2 (Apache-2.0; verify checkpoint, text encoder and VAE terms separately)

Three required files:
1. diffusion_models/wan2.2_ti2v_5B_fp16.safetensors (~10.0 GB)
2. text_encoders/umt5_xxl_fp8_e4m3fn_scaled.safetensors (~6.7 GB)
3. vae/wan2.2_vae.safetensors (~1.4 GB)

Total checkpoint storage ~18.1 GB decimal. Budget at least 35-50 GB free disk for environment, weights, cache and outputs. DO NOT commit weights to Git.

ComfyUI's official native-offloading guide says 5B should fit 8GB VRAM. This is **not verified on user's RTX 4060 8GB**; full model does not fit GPU at once. RAM/CPU offloading, smaller resolution and fewer frames may be necessary. A full 120-frame run may OOM or be slow. No paid APIs.

Windows launcher: quality_tournament/launch_wan_windows.ps1. Checks prerequisites, NVIDIA GPU, Python/Git, free disk; installs ComfyUI and CUDA PyTorch in a venv, starts local UI. Requires Windows RTX machine, does not run on Mac M2. Models downloaded through official ComfyUI template workflow, not automatically by untrusted URL. The launcher is an installation/startup convenience, **not** a proven one-button completed render.

Once UI opens, Workflow > Browse Templates > Video > Wan2.2 5B video generation. Install three files, enable Load Image for approved character art, begin with short low-res smoke test. Log seed, frame count, generation time, peak VRAM and inspect MP4 before quality scoring.

## Other engines
OpenToonz https://opentoonz.github.io/e/ — free/open-source traditional 2D; authored drawings required; not yet rendered.
Inochi2D https://github.com/Inochi2D/inochi-creator — open-source facial puppetry; needs original segmented art and rig; not yet rendered.
Synfig https://www.synfig.org/ — previous native SIF failed with "Can't find linked file #project.sif". One bounded format repair attempt; park if unsuccessful.
Video-to-video stylization — needs working licensed base animation and verified model; not rendered.

New paid API/software cost $0. Electricity, GitHub Actions usage and disk may incur real costs. No six-way comparison gallery yet.
