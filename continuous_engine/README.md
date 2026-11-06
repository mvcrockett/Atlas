# Continuous Anime Engine Sprint 1

## What is actually implemented
A phone-triggerable GitHub Actions workflow at `.github/workflows/continuous-anime.yml`, with a 5-second, 24-fps, 120-frame 480x270 CPU renderer. Accepts ordered PNGs in `continuous_engine/keyframes/key_000.png`, `key_001.png`, etc. With no supplied frames it uses an original procedural lavender-themed *test fixture* generated in Python, NOT the previously generated/approved anime heroine art and NOT AI-generated art. The user can trigger the workflow using GitHub mobile/browser Actions > Phone-First Continuous Anime Engine > Run workflow. The repository must have the input PNGs committed for the workflow to use them.

## Technology
CPU Farneback bidirectional optical flow via OpenCV; warps and blends images. If optical flow is unstable, dispatch workflow with `interpolation=blend` to test a simple crossfade baseline. Neither is RIFE. RIFE inference requires downloading weights, PyTorch setup and performance evaluation; not yet implemented. The engine creates all 120 frames, exports MP4 and GIF, and records basic pixel-change diagnostics. It does not invent unseen hands, maintain identity under occlusion or certify professional animation quality.

## Benchmark and quality gates
- Verify 120 numbered PNGs, MP4 and GIF in Actions.
- Inspect first/middle/last and ideally the whole MP4.
- Metrics: mean/max consecutive-frame pixel difference, frame indices exceeding 18 mean absolute pixel values. These are coarse diagnostics, not perceptual quality scores.
- Keyframe consistency, anatomy and user approval require human review. Failure of continuity should be flagged, not silently declared fixed.
- Full anime reference candidate is **not yet committed**; approval pending.

## GPU generative repair (future, not executed)
1. Find a failed segment (e.g. hand rotates through unseen surface) using flow diagnostics and visual review.
2. Generate a new intermediate *pose-conditioned* keyframe using the original approved character sheet plus skeleton/segmentation guides and consistent seed/style. This requires a suitable generative GPU and rights-cleared model. The iPhone is only the control interface.
3. Insert corrected keyframe and rerun CPU interpolation; repeat with capped retries. Record seed, source, license, frame index and identity check. Do not claim this stage is operational.
4. For larger scene changes, use multiple authored keyframes or a GPU video model, rather than stretching optical flow.

## Limitations and cost
No local desktop/RTX setup required. Standard GitHub runners have no GPU. Public/open-source tooling and no paid APIs, but GitHub Actions quotas, network, storage and electricity may apply. A five-second movie can be technically continuous and still look visually bad; quality must be judged from actual output.
