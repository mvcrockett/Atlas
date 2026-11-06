# Operation No Pants Studio — Blueprint v2.0
Approved by project owner: 2026-11-06. This is an additive plan. Preserve NO_PANTS_CHARTER.md (v1.2), quality_guardian/QUALITY_GATES.json, prior handoffs, and verified code.

## Mission
Build a phone-operated personal studio for professional-looking original Japanese anime, by integrating proven open-source video engines rather than inventing a new renderer. First output target: 3–5 seconds of the approved lavender heroine blinking/smiling, genuinely generated as MP4. Artistic approval is mandatory and separate from technical success.

## Proposed architecture
iPhone thin UI -> No Pants job controller -> ComfyUI workflow API on a reachable GPU host -> pluggable I2V engine (AnimeGen first, Wan2.2 Animate for controlled motion, AniSora experimental) -> reuse existing video assembly/finishing -> MP4 and review. Initial hosted AnimeGen proof-of-concept may bypass ComfyUI; do not demand ComfyUI before first video. No local desktop required for owner.

## Six phases and evidence gates
1. Foundation Audit: verify official code/workflows/licenses, resource needs, and an actual $0 execution path. Exit: reproducible specification with honest blockers.
2. First Real Anime: approved single-character portrait -> genuinely generated 3–5-second MP4 -> inspect frames and human approve. Exit: actual playable output, not procedural/interpolated fixture.
3. Character Acting: motion-driving reference with Wan Animate; verify face, hair, hands, gestures, consistency and anatomy. Exit: controlled movement verified in actual footage.
4. Phone-First Studio: minimal controller for submitting workflow, tracking jobs and retrieving MP4 on iPhone. Exit: real phone-to-video round trip.
5. Quality and Finishing: reuse existing assembly; introduce interpolation/restoration only after generated motion exists. Exit: repeatable 85/100 quality, subscores per v1.2 gates, human approval.
6. Personal Production Studio: shot sequencing, reusable character assets, dialogue/audio, episode assembly. Exit: practical repeatable short-scene-to-episode workflow.

## Engine selection and licenses — provisional, verify before distribution
- ComfyUI: official https://github.com/Comfy-Org/ComfyUI ; GPL-3.0; existing workflow JSON/API/queue; cloud managed API is paid, NOT an authorized $0 GPU.
- Wan2.2 Animate: existing official Comfy workflow https://comfy.org/hub/workflows/wan2-2-animate-character-animation-and-replacement-c2c4b45b7df5/ ; 14B fp8 checkpoint, video-driving, optional segmentation/pose/CLIP components; memory substantial and depends on precision/offloading. Verify specific checkpoint and dependency licenses separately.
- AnimeGen I2V: official https://huggingface.co/aidealab/AnimeGen-I2V ; Apache-2.0 model based on Wan2.2 I2V A14B; recommends RTX 4090+ locally; ~114GB repo; Diffusers example. Official hosted Space https://huggingface.co/spaces/aidealab/AnimeGen-I2V shows Running on Zero, but NO GPU job submitted or MP4 verified. This is FIRST EXECUTION CANDIDATE, bypassing ComfyUI until output exists.
- Bilibili Index-AniSora: https://github.com/bilibili/Index-anisora ; anime-focused alternative, publishes a 12GB VRAM V3.1 option and V3.2 Wan2.2-derived weights. Version-specific license/dependencies, performance and actual hosting must be validated; not first path.
- Finishing: existing repository assembly retained. The Anime Scripter and LTX are optional later research, not Phase 1 dependencies.

## Phase 1 audit result and selected minimal path
(1) Obtain clean single portrait crop from already approved heroine sheet without requiring GitHub PNG upload. (2) Submit to official AIdeaLab AnimeGen I2V hosted demo on a genuinely free quota, if available. (3) Ask for static-camera blink and subtle smile, 3–5 sec; save MP4. (4) Inspect real frames, identity and temporal stability. (5) Only if demo fails with observed error, try one materially distinct free fallback (AniSora hosted demo if verified, or Wan-based available free host). If no callable browser/GPU tool, user can run Space from phone or use ChatGPT Work cloud browser where available; do not misrepresent a hosted landing page as completed inference.

## Governance and stop rules
$0 paid GPU/API without explicit approval; no user desktop; one mission/session; at most two materially distinct attempts per blocker; no missing-GitHub-PNG polling; no new renderer, dashboard or full studio implementation before real video. Preserve verified code. No GPU inference, MP4, quality score, or free quota should be claimed without evidence. Keep infrastructure, generative execution and artistic acceptance separate. Original v1.2 Quality Guardian score 85/100 and minimum subscores remain binding. Never count procedural cartoons as anime. Update handoff with evidence and readback.

## Phase 2 activation condition
Real generated MP4 or actual demo failure details. If no evidence, stop and request only the concrete input needed; do not loop through status checks.
