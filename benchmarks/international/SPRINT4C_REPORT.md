# Operation NoPants 4.0 — Sprint 4C CPU-only international rig benchmark

Date: 2026-11-06. Result: **BOTH NATIVE ENGINES RAN ON GITHUB CPU RUNNERS; VISUAL-QUALITY DECISION NOT YET VERIFIED**.

## Verified run
https://github.com/mvcrockett/Atlas/actions/runs/42235294206
Both independent jobs passed on Ubuntu 24.04 using headless Chromium/SwiftShader and FFmpeg. No local RTX or private computer. No Wan or See-through inference. Paid API spending $0.

## Shared input
Both consumed the same upstream `sample2.psd` from https://github.com/852wa/Anime2.5DRig ; this is a real layered anime PSD supplied by a third party. Its author's sample illustration rights are reserved per README. Neither its PSD nor the resulting PNG/MP4 files were published in GitHub artifacts or this report. The samples are NOT established as See-through-generated assets and NOT the user's unapproved heroine.

## Direct evidence
- Japanese auto-rigger: `nopants4c-japanese-metrics` artifact. Native `852wa/Anime2.5DRig` WebGL1 loaded `sample2.psd` through its actual browser UI, ran its original automatic rigging and animation, and captured 72 canvas snapshots. All 72 hashes unique. 1280x1280 canvas. FFmpeg wrote and ffprobe confirmed **72 frames, 24fps encoded, 3.0 s output**. **Critical caveat:** browser's live rAF was sampled by slow screenshots over **101.43 seconds**, then compressed to a 3-second playback. This **is not** 24fps live-time capture; unique hashes cannot establish smooth 24fps motion or comparable fidelity.
- Stretchy control: `nopants4c-stretchy-metrics` artifact. Same public PSD imported with upstream `src/io/psd.js::importPsd`, native ScenePass and computePoseOverrides. 15 nonempty semantic layers, 14 recognized tags. Deterministic 72-frame 24fps 3.0 s encoded output. **29 unique frame hashes / 72**, indicating held/repeated frames with low-amplitude 3-second head-y oscillation and framebuffer quantization.
- Both pipelines had no browser page errors and produced verified FFmpeg clips inside runner, removed without public publishing. There are **no visual frames available in our conversation** for an honest artistic comparison.

## Fairness limitations
These tests are **not apples-to-apples**:
- Japan engine sampled actual live rAF across 101.43s (non-deterministic animation), then encoded at 24fps; Stretchy renders exact keyframed poses on a deterministic three-second timeline.
- Japan sampled full 1280x1280 character canvas; Stretchy rendered on a 480x480 benchmark canvas.
- Japanese rig includes its native idle/blink/hair/mouth physics; Stretchy control exercised just head motion, not comparable facial or hair animation.
- Unique hashes alone say *nothing* about identity, visual fidelity, seam quality, temporal flicker, eyes, mouth and hair aesthetics.
- Sample artwork redistribution rights are uncertain, so no plaintext visual artifact was uploaded to a public repo.

## Licensing and reuse
`852wa/Anime2.5DRig` code is MIT (verified root LICENSE); includes ag-psd under MIT and bundled MediaPipe FaceMesh under Apache-2.0 as documented. The sample illustration is **not** automatically MIT-licensed. Stretchy MIT. Respect upstream attribution and copyright requirements. Independent test is a legal/architectural evaluation, not a determination of product compliance.

## Engineering architecture decision
**Keep Stretchy as NoPants primary deterministic 24fps frame renderer.** It is already verified and repo-integrated.

**Adopt Anime2.5DRig as the *candidate* auto-rigging and expression system**, initially as a separate native renderer, not by copying its whole WebGL1 runtime into Stretchy's WebGL2 pipeline. Its `lib/rigger.js` performs PSD-based automatic anchors, layer aliases, spring strand settings, meshes, mouth/eye replacements. The WebGL1 runtime and WebGL2 mesh models are not plug-compatible. Do not swap primary engine or promise seamless merger without a controlled same-motion comparison.

## Recommended Sprint 4D
1. Create a **fully original, redistributable anime illustration with a real PSD layer kit** (not a geometric calibration puppet) OR secure explicit permission for reusing a third-party sample in private artifact review. Keep the user's unapproved fixture private.
2. On that legal asset, use matched canvas dimensions, motion paths, frame times and 72 deterministic samples for both engines. In Anime2.5DRig, expose an instrumented test-only stepper or stable frame clock rather than 101-second screenshot sampling.
3. Add in-run pixel metrics (registered source similarity, actual temporal changes, edge discontinuity and occlusion masks) plus user-visible permitted frame montage/video.
4. Test blink, mouth and hair with identical intended motion and inspect outputs; choose whether `lib/rigger.js` can be reused or Japanese native engine should remain a dedicated portrait-animation backend.
5. Keep prior branches, security, CPU/no-paid-API constraints; two materially distinct attempts per blocker.
