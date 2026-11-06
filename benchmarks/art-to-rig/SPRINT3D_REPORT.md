# Operation No Pants: Sprint 3D evidence checkpoint

Date: 2026-11-06. Status: **PARTIAL SUCCESS / REAL-ART STRETCHY CI NOT VERIFIED**.

## Branch safety
Created only `no-pants-sprint3d-stretchy-resync` from `no-pants-sprint3a-art-to-rig-bridge`. No merges or modifications to `main`, `operation-no-pants-3-phase2b`, the two Sprint 2 experiment branches, or the Sprint 3A original branch.

## Native engine
GitHub Actions run: https://github.com/mvcrockett/Atlas/actions/runs/42206065500

- **Passed** actual pinned upstream Stretchy `ScenePass` and `computePoseOverrides`, called through headless Chromium.
- 72 decoded frames, 24fps, 3 seconds; 68 unique image hashes.
- Hierarchical head and torso, eyelid opacity tracks, mouth-state transitions and slight hair motion exercised.
- Captured representative frames and video verified in artifact.
- Artwork in CI is explicitly `CALIBRATION_ONLY_NOT_ANIME` (synthetic eight-layer fixture), *not* the user's detailed anime character.

## Actual anime art
- Recovered original candidate from user Library and old Sprint 3B/3C artifacts.
- Candidate remains `UNAPPROVED_TECHNICAL_FIXTURE`, not canonical.
- Local refined 72-frame, 24fps, 3s video used **OpenCV/Pillow as a proxy**, not Stretchy.
- Corrected prior blink/mouth coordinate misalignment: older lids targeted the eyebrow region.
- Rebuilt head/side-hair masks, feathered edges, restrained motion, mouth redraws, and closed-lid overlays.
- Saved the local art-pack, script, montage, side-by-side comparison, MP4 and metrics outside the public repo.
- **No user art is published to the public repo in this sprint**. This intentionally prevents unauthorized publication of unapproved art.

## Source / temporal metrics (local proxy, NOT Stretchy)
| Metric | Sprint 3C proxy | Sprint 3D local proxy |
| --- | ---: | ---: |
| Frames | 72 | 72 |
| FPS | 24 | 24 |
| Duration | 3s | 3s |
| Mean frame-to-frame absolute RGB difference | 2.209 | 0.515 |
| 95th percentile frame difference | 5.321 | 0.683 |
| Mean RGB difference vs original across clip | 12.643 | 5.655 |
| Initial frame RGB error vs original | 5.552 | 0.000 * |
* Initial frame intentionally replaced with exact original art; not an automatic reconstruction achievement.

**Warning**: Reduced interframe difference does *not* by itself prove improved temporal quality; we also deliberately reduced the motion amplitude. Identity preservation is observed within a small-motion range, not quantified with an identity model. The blink still requires proper production redraws; arms/hands and occluded anatomy remain unverified.

## Remaining hard blocker
Actual user-art layer bytes are in the conversation's working container, while the user's GitHub repository is **public**. The connected GitHub write interface accepts text, not arbitrary local raster assets. Publishing the unapproved art to the public repo solely to make CI work was avoided.

**Therefore no claim is made that the user's refined anime artwork successfully rendered in Stretchy via GitHub Actions.** The native-engine control and local detailed-raster proxy are independently verified, but the last connection remains unproven.

## Next Sprint 3E (narrow, secure)
1. Arrange a **nonpublic asset ingress** for the approved fixture, keeping original art out of public branch history.
2. Run exactly this `bridge3d.js` on the fixture and verify one 72-frame MP4, compare to local proxy, and measure face/eye/mouth, seam and texture fidelity.
3. If deformation gaps persist, evaluate See-through (SIGGRAPH 2026 anime layer decomposition) as a future optional art-reconstruction tool; no heavy model install yet.
4. Preserve two-attempt circuit breaker and branch isolation; no Wan, OpenToonz or full studio.
