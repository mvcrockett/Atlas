# Operation No Pants 6.0 — Sprint 6A Tournament Evidence
Date 2026-11-06. Status **completed bounded tournament**; successful Japanese original-art repair, other candidates screened per their roles. Do not confuse smoke tests with anime render verification.

## A. Real tested animation: Anime2.5DRig occlusion corrected
- Branch: `no-pants-6a-international-engine-tournament`, based on `no-pants-4d-public-domain-research`. Old branches and unapproved heroine not modified.
- GitHub Actions: https://github.com/mvcrockett/Atlas/actions/runs/42242553202 **passed**. Native Japanese app `852wa/Anime2.5DRig`, unchanged original WebGL renderer/rigging, test-only compatibility patch `benchmarks/international/patch4d_japanese.py`.
- Actual root cause: input PSD sequence topmost-first, `Rigger.buildRig` enumerates layers in input order, browser `app.js::render` sends `layers` in that same order and renderer draws the list sequentially. The existing semantic slots mark `back hair` at depth 0.55, `face` at 1.00 and `front hair` at 1.28 but the renderer does **not** sort by that depth. The input `back hair` was last and occluded face.
- Correction in ephemeral upstream runner: `rig.layers.sort((a,b)=>(a.depth-b.depth)||(a.z-b.z));` before `prepareLayers(rig)`. No invented sorting subsystem or rewritten renderer. Preserve stable tiebreaker and existing slot values. This is only verified on our particular 12-layer artwork; it may not generalize to other PSDs with carefully authored painter order.
- Repaired sample: original NoPants lavender 768x768 illustration, 72 frames/3s/24fps, **72 unique encoded source-frame hashes** (all intervals changed in source raster test), 0 browser page errors, native face, iris, eyebrows, mouth, hair and clothing now visible. Visual inspection of six representative decoded frames confirms facial visibility and a mouth-open state; blink states appear but are still stylized and rudimentary.
- Artifact id 13515811906 `nopants-6a-japanese-depth-order-repair` includes sample video, montage, metrics and telemetry. No third-party art; no private heroine.

## B. Comparison to prior verified Stretchy original-art benchmark
- Prior unmodified baseline: https://github.com/mvcrockett/Atlas/actions/runs/42239864407, Stretchy 72 frames/24fps/3s; measured 54 unique hashes in previous run, eye/mouth states.
- Side-by-side decoded clips from 6A Japanese vs 4D Stretchy, 768x768, same original character. The Japanese implementation has 72 unique source hashes and more fine-grained mesh motion. Stretchy baseline has 54 unique hashes and a cleaner static match.
- Local decoded frame comparisons (RGB pixel differences include encoder/transforms):
  - Japanese repaired: source MAE 3.476; face ROI source MAE 7.660; frame-to-frame MAE 0.354.
  - Stretchy baseline: source MAE 3.369; face ROI source MAE 8.192; frame-to-frame MAE 0.497.
  - NOT normalized for different engines' postprocessing or deformation. These do not prove absolute aesthetic superiority. Both images visibly retain the face, eyes and clothing. Neither is production-quality anime; artwork itself remains schematic.
- Direct source comparisons and visual review are available in locally generated `nopants_6a_actual_engine_comparison.png` and `nopants_6a_real_engines_side_by_side.mp4`; these were created from allowed original art and both verified GitHub test artifacts.

## C. CPU / cloud feasibility tournament results
- https://github.com/mvcrockett/Atlas/actions/runs/42243137733 (first independent smoketest)
- https://github.com/mvcrockett/Atlas/actions/runs/42243336566 (second smoketest, **successful jobs**)
- Japanese Anime2.5DRig — **actual original-art native anime motion passed** after one focused repair attempt. MIT source license, sample art separate. Strong candidate for expression/hair backend.
- Stretchy Studio — **actual original-art native animation passed previously**. MIT. Best-controlled deterministic scene/pipeline baseline. Keep primary renderer until an end-to-end scene gate says otherwise.
- Synfig — **CPU CLI installation and invocation passed** in 6A Ubuntu 24.04. Previous Sprint 2 produced a 24fps geometric render. Licensed GPL family (not suitable for casually copy-pasting into a proprietary codebase); standalone use remains possible. No new anime-art render in this sprint; preserve as CPU fallback.
- Inochi Creator v0.8.6 — **official 22 MB Linux binary downloaded; first attempt failed due missing SDL2**. After installing Ubuntu SDL2 in second attempt, native process **ran under Xvfb/Mesa software rendering for the full 20-second bounded smoke test**; process exited under intentional timeout with XIO report. This supports launch feasibility, NOT verified PSD import, puppet file, render quality or native automation. Source BSD-2-Clause. Further full-model tests are a separate 6B work item with a fresh scoped limit; don't claim pass beyond launch.
- OpenToonz — **distribution screen only**. Ubuntu 24.04 runner apt policy had no `opentoonz` candidate and official GitHub v1.8.0 releases list .pkg macOS and .exe Windows but no Linux prebuilt. No native headless test because compiling/installing the full application would breach the sprint's no-large-build constraint. BSD-3-Clause main software, bundled thirdparty terms. Continue as future scene-composition candidate, but don't block us on it.
- The Anime Scripter (NevermindNilas/TheAnimeScripter) — source **AGPL-3.0**, AI models primarily GPU. Supports CPU dedup and scene-change analysis but not an adequate CPU RIFE inference replacement. Use existing FFmpeg/OpenCV CPU diagnostics rather than copying AGPL code into NoPants. No new TAS code execution or weights in this sprint. Commercial use requires license compliance review.
- See-through — previous 4A upstream PSD source-contract test passed; native model inference not attempted (GPU/model checkpoint costs, hardware not set up). Reuse existing PSD-compatible importer, hold automatic decomposition to later.
- OpenToonz and Inochi are NOT disqualified for needing graphical display; they are gated for future practical tests.

## D. Weighted preselection scorecard (provisional, NOT scientific benchmark)
Rubric: visual identity 30%, usable rigging/expressions 25%, free cloud feasibility 20%, phone automation 15%, permissive/compliant commercial licensing 10%. Scores are deliberately incomplete:
| Candidate | Visual /30 | Rigging /25 | CPU /20 | Automation /15 | License /10 | Evidence confidence |
|---|---:|---:|---:|---:|---:|---|
| Stretchy | 21 | 15 | 19 | 14 | 10 | Actual original 72-frame MP4 and visual inspection |
| Anime2.5DRig repaired | 21 | 20 | 18 | 12 | 10 | Actual original 72-frame MP4 and visual inspection, experimental depth ordering |
| Synfig | unscored | unscored | 18 | 11 | conditional | CPU CLI; prior simple fixture render only |
| Inochi Creator | unscored | unscored | preliminary 10 | unscored | 10 | Startup smoke only; not yet imported benchmark PSD |
| OpenToonz | unscored | unscored | not established | not established | conditional | No native Linux package tested |
| The Anime Scripter | unscored | unscored | GPU-dependent | conditional | AGPL review | Source inspection only |
| See-through | unscored | unscored | GPU-dependent | interface verified | check model terms | PSD source interface only |

The two numerical scores are proposal/engineering estimates based on observed sample and feature coverage, not repeatable perceptual measurements. Never use a score to override demonstrable unusable draw order or licensing incompatibility.

## E. Architecture decision and 6B phase gates
1. **Stretchy remains deterministic main timeline/renderer** for now, because it is already phone-triggerable and has reproducible 24fps rendering.
2. **Anime2.5DRig becomes the favored dedicated portrait/face/hair animation backend**, running in isolation, not an immediate copy-paste hybrid; verify corrected depth ordering on different PSDs before production use.
3. **Inochi remains an R&D challenger**: one bounded PSD import and one real small rigged scene under Xvfb/LLVMPipe, no massive dependencies and no claims before actual outputs.
4. **Synfig remains a CLI fallback** for separate CPU 2D composition, not the anime character rig winner.
5. **OpenToonz moves to scene-compositing exploration once end-to-end character motion is clean**, not a gating dependency today.
6. **Public-domain rights ledger stays separate**. Don't confuse motion references with source-art repairs.

### Sprint 6B acceptance tests
- Repaired Japanese semantic-depth ordering must preserve face on at least two independently ordered original layered PSDs.
- One higher-detail legal anime portrait with at least 2 eye and 2 mouth expression drawings, hair with actual mask overlap.
- Same 24fps frame samples per engine; at least one dynamic 5-second expressive portrait with visually checked blink, mouth, hair and identity (not a frame-hash-only assertion).
- Quantitative seam/occlusion masks and held-frame diagnostics, plus side-by-side downloadable media for phone review.
- Original and all previous branches preserved; no public user heroine nor unlicensed art.
- No GPU/cloud setup work for user. Two materially different attempts per blocker.
