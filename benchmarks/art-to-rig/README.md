# Sprint 3A — Anime Art-to-Rig Bridge

This is a generic **textured layer adapter**, not an anime quality generator.

## Real source candidate
The unapproved original reference image **Anime Woman Character Reference Sheet.png** was recovered from the user's Library. A front view was decomposed locally into two PNGs, and placed in a downloadable candidate ZIP. This copyrighted/user-provided image is **not** committed to this repository or silently declared approved.

## Admitting artwork
Put a directory containing manifest.json and its relative PNG layers under `art/` of the pinned upstream Stretchy checkout. Required manifest fields:
- `canvas: {width,height}`
- `layers: [{id,path,parent,order,x,y,pivot:[x,y]}]`
- `controls: {head_y:{node}, breathing:{node}}`
- `status: UNAPPROVED_CANDIDATE | APPROVED`
- `approval: boolean`

The adapter imports Stretchy's actual `ScenePass` and `computePoseOverrides`; textured quads and pivot controls map each provided layer into its renderer. It does not solve eyelid separation, mouth interior, articulated arm redraws or missing anatomy.

## CI
GitHub Actions uses a clearly labeled **calibration-only layered fixture**, made from two independently textured tiles. It establishes the app/build/render/FFmpeg transport without asserting anime-quality. Actual approved anime-art CI validation requires explicit user-approved asset admission.

Sprint 3A gate: mechanics may pass; visual fidelity remains UNVERIFIED until an approved, genuinely layer-separated anime character is rendered and examined.
