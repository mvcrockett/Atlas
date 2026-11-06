# Sprint 7D — Canonical Pixel-Locked Puppet: Evidence and Handoff
**Date:** 2026-11-06  
**Status:** Source-locked PRIVATE art kit prepared; local video verified; native Stretchy proof **BLOCKED / NOT EXECUTED**.  
**Privacy:** The PUBLIC GitHub branch contains only original source-free code/tests/this text. No user's source images, derived layers, unencrypted outputs, private URLs or keys committed.

## Verifiable baseline
- Inspected `main` SHA: `8e4e21b556c62b9d28b93e9c4471b02b246950b1`
- Inspected 7C SHA: `9a2c037c910f24abe586fefa62480eded354e476`
- Branch `no-pants-sprint7d-pixel-locked-native-proof` forked directly from 7C.
- 7C public synthetic scheduler CI: https://github.com/mvcrockett/Atlas/actions/runs/42265706016 (success).
- 7B real Rhubarb CPU mouth-cue generation: https://github.com/mvcrockett/Atlas/actions/runs/42264477159 (success; exactly 10 detected cues).
- Sprint 3E secure-art ingress design and its 3 secrets: `NOPANTS_ART_BUNDLE_URL`, `NOPANTS_ART_BUNDLE_SHA256`, `NOPANTS_EVIDENCE_KEY_HEX` at https://github.com/mvcrockett/Atlas/blob/no-pants-sprint3e-private-art-ingress/benchmarks/art-to-rig/SPRINT3E_PRIVATE_INGRESS.md — design **not verified end-to-end**.

## Private original and geometry (no pixels included here)
- Owner's ORIGINAL heroine portrait supplied in chat: 1179×2010, SHA256 `df39186b3d96856062167417d5f1f02f9a9e65a419b31a88b5ab46c01ee1b5e1`.
- Owner's ORIGINAL multi-view reference sheet: 1536×1024, SHA256 `aaa50428100bb549bcb350e3ccf11df276809c4e1308e0a8e79d9a41ea63a1cc`.
- Private kit crop: (0,0) to (1179,1180) resampled to 650×650, with mouth center (388,430), left eye (271,313), right eye (448,270).
- Geometry, private underpaint hypotheses, eye patches, five viseme variants, rough color-segmented hair locks, neck/shoulder reference crops, and full build script packaged in the **private conversation attachment**, not this repository.
- Masked round-trip static reconstruction of original mouth source patches: average absolute RGB error **0.02665 on 0–255 scale**, fraction of pixels with >18 max-channel difference **0.00035**. About **95.872%** of static crop lies outside the edited mouth mask. This is **static pixel fidelity only**, NOT animation quality and NOT proof of full-layer decomposition.
- Hidden skin was estimated by OpenCV inpainting; the true hidden hair/neck/shoulder art is **not actually recovered**.
- Closed lids were provisional painted lines; mouth variants were source-pixel warps, **not professionally authored phoneme sprites**. Side hair was roughly color-segmented but not animated or verified as independent watertight layers.

## Private local render evidence
- File: `heroine_7d_pixel_locked_LOCAL_NONNATIVE.mp4` in private downloadable kit.
- Engine: PRIVATE local Pillow / OpenCV / FFmpeg compositing. **NOT native Stretchy ScenePass / computePoseOverrides and NOT Anime2.5DRig.**
- FFprobe: 650×650 H.264, 24/1fps, **120 decoded frames**, exactly 5.000 seconds, AAC audio 5.000 seconds.
- Input: actual 7B Rhubarb-generated JSON (10 cues) and its original synthetic dialogue recording.
- Output: 116 unique PNG SHA256 frame hashes out of 120, mean adjacent frame RGB MAE 0.36198, highest per-pair RGB MAE 1.30652 (0–255).
- Privately exported `inspected_frames.jpg` contains 6 decoded frame samples.
- **Art-attempt circuit breaker adhered to:** (1) source-pixel warp visemes gave a faithful but too-subtle mouth; (2) extraction from the owner's full reference-sheet open-mouth expressions generated a displaced lip patch / mismatched skin and was **rejected** after visual review. Retain first solely as nonnative diagnostic proof.
- Human approval: **NOT REQUESTED AS A PRODUCTION PASS**; Victoria must view and evaluate actual clip. No claim of production-ready blinking, visually faithful speech or a completed puppet.

## Native Stretchy blocker
1. The container could not resolve public GitHub for local git clone of Stretchy, so no upstream local native WebGL renderer was available for the private art (local git failed DNS).
2. Existing Sprint 3E remote secure workflow requires an externally hosted time-limited private art ZIP and corresponding GitHub encrypted secret configuration, SHA256, and AES-GCM key; these inputs were not verified or provisioned. The PUBLIC repo must not accept private art bytes as a work-around.
3. Existing Sprint 3D bridge is visibly hardcoded to a 3-second mouth timeline; 5-second Rhubarb cue adapter integration remains engineering work, not verified by the source-free preflight.
4. No native rendered private-art MP4 / decrypted and inspected private-output GitHub artifact exists for Sprint 7D. **The native proof exit gate remains unmet.**

## Public safe code and CI
- `tools/nopants7d/validate_private_asset_manifest.py`: stdlib-only offline private-kit manifest preflight, checks source hashes, geometry, layer slots and explicitly rejects false native VERIFIED flags. No file bytes uploaded.
- `tools/nopants7d/test_manifest.py`: source-free synthetic, malformed and missing asset tests.
- `.github/workflows/no-pants-7d-asset-preflight.yml`: source-free GitHub Actions validator on isolated 7D branch (cannot itself be a persistent default-branch UI button until reviewed/merged).
- GitHub Actions run: https://github.com/mvcrockett/Atlas/actions/runs/42267824635 — **success**. This tests manifest validity, **NOT native image rendering**.

## Proposed quantitative gates for subsequent proof
- Actual native Stretchy or Anime2.5DRig `ScenePass`/mesh/bones run, with source-hash recorded and private art not exposed.
- 120 frames, 24fps, 5s, consistent resolution and valid synced audio.
- Source-pixel / identity ROI comparisons use aligned frames; exclude dynamic features from strict pixel-equality tests.
- No duplicated mouth, floating eyelids, seams, missing underpaint, hair/neck overlap inversion, or unwanted face drift.
- Victoria's explicit visual review and acceptance is required.

## Only next milestone: Sprint 7E
**Secure Native Rig Ingress & Artist-Finished Facial Layers.**
1. Securely provision real private asset ingress outside public git with owner-approved hosting, correct hash, encrypted evidence key; do not request secrets in chat.
2. Redraw actual closed eyelids and distinct mouth shapes and complete hidden face/hair/neck/shoulder fill while keeping portrait identity.
3. Adapt proven Stretchy bridge from 3000ms to 5000ms, using archived Rhubarb frame schedule and transparent textures.
4. Run first **authentic native private 120-frame render**, decrypt privately, inspect against original; hard stop after 2 different blocker attempts.
5. Do not start a new engine tournament, big downloads or new renderer; keep $0 added paid spending.
