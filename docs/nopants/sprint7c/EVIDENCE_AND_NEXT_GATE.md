# Operation No Pants Studio Sprint 7C — Evidence Report
Date: 2026-11-06
Branch: `no-pants-sprint7c-living-heroine`
Status: **bounded technical progress; NOT production-quality or native-rig validated.**
Privacy: Original user-supplied heroine artwork, all derivative PNGs and MP4 stay OUTSIDE this PUBLIC repository.

## Verified incoming baseline
- `main`: `8e4e21b556c62b9d28b93e9c4471b02b246950b1` at initial inspection.
- 7B: `a7e50d4a65569b9c36e41a51eb71c6bf090b3915`; branched from this SHA.
- Prior Rhubarb release 1.14.0 actually ran on GitHub CPU in https://github.com/mvcrockett/Atlas/actions/runs/42264477159 and generated **10 timed cues**, validated by its passing job and recorded artifact.
- Original owner reference: portrait 1179×2010 and full 1536×1024 sheet; pixel files remained in private session.
- Local 7B six-expression source was **ImageGen-derived**, not exactly original canonical pixels; previous private portrait and cue file recoverable in local session.

## Verified 7C public/code work
- `tools/nopants7c/schedule.py`: pure Python Rhubarb cue-to-mouth scheduling, 120 frames at 24fps, strict sorted-cue checks; no artwork operations.
- `tools/nopants7c/test_schedule.py`: source-free synthetic timing tests; normal, malformed and CLI cases.
- `.github/workflows/no-pants-7c-cue-schedule.yml`: safe branch-only push CI, manual-dispatch stanza. Manual dispatch in GitHub's ordinary UI generally requires YAML on the default branch; no merge performed.
- CI: **passed** https://github.com/mvcrockett/Atlas/actions/runs/42265706016 (tested scheduling, NOT an anime render).
- All preexisting branches left unchanged by Sprint 7C operations.

## Real LOCAL PRIVATE video inspection
- Local rendered file: `heroine_7c_audio_driven_private.mp4` (provided privately in conversation, not in public GitHub).
- Decoder probe: MP4 H.264 + AAC, 512×512, 24/1fps, **exactly 120 frames**, 5.000 seconds.
- 10 source Rhubarb cues select mouth states; blinking separately triggered; small rigid portrait drift.
- 112 unique PNG hashes among 120 frames, which is NOT a measure of aesthetic quality.
- Measured mean absolute full-frame neighbor difference 0.357; maximum 1.321 (pixel 0-255 units, RGB). Mouth ROI neighbor mean 0.753, max 11.944. Metrics are diagnostic only and cannot establish perceptual smoothness.
- Attempt 1 interpolated between dissimilar expression sprites: observed doubled/ghost mouths. **Rejected**.
- Attempt 2 switches mouth visemes discretely at Rhubarb cue boundaries: inspected six samples show no doubled-mouth fade; rapid sprite jumps and slight mouth/skin inconsistency remain. **Keep as honest experimental baseline**.
- Provisional alpha mouth/eye region texture patches were exported privately as evaluation aids; they are not separately underpainted rig-ready features, no clean independent face underpaint and no true hair articulation.
- This private test uses Pillow/OpenCV/FFmpeg compositing from existing artwork fixtures, **not Stretchy's or Anime2.5DRig's native rig**. They remain previously verified alternatives; using them with private heroine pixels requires secured ingress and proper independently authored layers.
- No native 7C Stretchy render, no GPU inference, no public private-art artifact, no completed private review gallery.

## Visual gate / blockers
- Character design is selected as reference, but test portrait differs subtly from original canonical illustration, because it was generated as an expression sheet.
- Face generally remains coherent, but transitions still lack true deformation and lip timing is bounded by sparse automatic cue data. Exact phoneme synchronization and performance aesthetics are NOT yet verified by Victoria.
- Layers for rear hair / face / neck / blouse not cleanly extracted and independently underpainted. No actual full-body movement or hand motion.
- Mobile review of private artwork currently uses conversation file link; a stable authenticated delivery system is not yet operational.
- The private-art Sprint 3E workflow is staged but unverified end to end with proper secrets and original assets; public GitHub Pages is unsuitable for private imagery.

## Exact next milestone
**Sprint 7D — Canonical Pixel-Locked Puppet Construction & Native Rig Proof.**
Privately reconstruct feature layers from original approved portrait/reference sheet; align eye/mouth pivots; redraw hidden fill; run one encrypted private native Stretchy or Anime2.5DRig portrait test; compare exact decoded frames to canonical design. Keep $0 spend, two-attempt breaker, no public art. Victoria must decide visual acceptance after actually watching the output.

No production-quality claim. No source art committed.
