# Operation No Pants 4.0 — Sprint 4D verified outcome and PD movement decision
Date: 2026-11-06. Latest tested source branch: `no-pants-4d-public-domain-research`. Report-only branch: `no-pants-4d-verified-results-and-marey-plan`.

## GitHub CI proof and circuit breaker
- First run [#42238959340](https://github.com/mvcrockett/Atlas/actions/runs/42238959340) failed in **both** jobs during `ag-psd` Node canvas initialization.
- One final materially different attempt installed `canvas@3.1.2` and explicitly required `ag-psd/initialize-canvas`.
- Second run [#42239864407](https://github.com/mvcrockett/Atlas/actions/runs/42239864407) passed **both** native renderer jobs. No further animation CI attempts are authorized in this sprint under the two-attempt rule. The report is on a different branch to avoid automatically triggering a third run.
- Artwork: original 768×768 lavender-haired anime-style portrait programmatically drawn with Pillow as independently transparent PNG layers; legitimate layered PSD serialized and roundtrip-tested using upstream `ag-psd@30.2.0`. **Not** the private unapproved heroine and not sourced from unclear-rights sample files.
- Both engines ran on GitHub-hosted CPU runners with Chromium/SwiftShader; no local computer, GPU inference, external paid API or large models.
- Output artifacts: `nopants-4d-japanese-original-anime` artifact id **13514941430**, `nopants-4d-stretchy-original-anime` artifact id **13513516927**. Both include original-art three-second 24fps MP4, montage PNG, JSON metrics and telemetry.

## CI metrics (verified against downloaded artifacts and decoded videos)
| | Japanese Anime2.5DRig | Stretchy Studio |
|---|---:|---:|
| Encoded frames | 72 | 72 |
| Frame rate | 24 fps | 24 fps |
| Duration | 3.0 s | 3.0 s |
| Unique PNG frame hashes | 72/72 | 54/72 |
| Mean RGB change between sequential decoded frames | 0.110 | 0.497 |
| Max decoded frame change | 0.938 | 0.798 |
| Raw full-image RGB difference from original static source (MAE) | 9.89 | 3.37 |
| Raw face region RGB difference (approx. ROI, MAE) | 43.20 | 8.84 |
| Logged page errors | 0 | 0 |
| Empty frames flagged by benchmark | 0 | 0 |
| PSD layer count reported | 17 auto-rig layer parts | 12 imported PSD layers |

**Metrics caution:** Source reconstruction error is an unregistered image difference after alpha/background handling, not a psychometric identity or aesthetic score. Frame hashes do not measure smoothness. Japanese auto-rig creates extra derived parts; count 17 is not PSD source count.

## Crucial manual visual inspection
Downloaded both Actions artifacts, decoded both MP4s and inspected montage and exact frame samples 0,18,43,51,71.
- **Japanese output is visibly broken:** large opaque purple hair layer occludes face/eyes/mouth through the entire clip. Distinct motion is real, but expression and identity cannot be evaluated or credited. This is a PSD layer-order/depth/occlusion incompatibility, not proof the Japanese algorithm is intrinsically inferior.
- **Stretchy output is visibly intact:** lavender-haired face, eye positions, blush, clothing preserved; closed eyelids at sample frames 18 and 51 and mouth-open variant near frame 43 visibly work. Neck and shoulders remain simple 2D art; hair motion modest; character illustration is stylized, vector-like calibration anime rather than professional production anime.
- The engines are matched on source file, 768px canvas, output duration, frame times and scheduled expression events but NOT entirely identical in control semantics: Japanese uses angle/pseudo-3D transform and spring physics; Stretchy is keyframed. This is a compatibility/determinism benchmark, not a validated artistic head-to-head winner.
**Decision:** Keep Stretchy primary for present production pipeline. Retain Anime2.5DRig as separate MIT-licensed *candidate* after a **single targeted layer-order correction** in a later sprint, not an engine replacement today.

## Rights and privacy
Original benchmark images were generated independently and may be published in this repo's run artifacts. The user's separate original heroine is never loaded/committed. Third-party Anime2.5DRig application software is MIT-licensed; third-party sample illustration is not assumed free for commercial reuse. The runtime was used intact except for a test-only deterministic stepping hook.

## Marey 1891 motion study research (NO integration performed)
Verified public-domain file item:
- *Image chronophotographique d'un coureur.jpg* by Étienne-Jules Marey, dated November 15, 1891, original published in `Revue générale des sciences pures et appliquées` 1891.
- Commons item URL: https://commons.wikimedia.org/wiki/File:Image_chronophotographique_d%27un_coureur.jpg
- Direct original linked on Commons: https://upload.wikimedia.org/wikipedia/commons/e/ee/Image_chronophotographique_d%27un_coureur.jpg
- Commons marks source Public Domain and Creative Commons Public Domain Mark 1.0. Author died 1904; published 1891, very likely PD in US under pre-1931 publication rule and in French/EU author's-life+70 regimes. Commons warns a separate US PD tag is missing, so **archive rights metadata requires additional review before commercial release**; do not claim unconditional global legal clearance.
- Source metadata: 432 × 323px; 132,143 bytes; upstream Wikimedia Commons SHA-1 `90f3519a7e731076a51d300a6b5f92d8269d4c8b` (repository metadata, NOT locally verified).
- Download into model container was attempted **once** and failed due environment access. No file was ingested or processed, and no local SHA-256 can truthfully be reported.
- **Explicit exclusion:** Science Museum Group Marey running photographs tagged CC BY-NC-SA 4.0 are NOT commercially cleared; their museum catalogue's CC0 metadata license does not grant rights to noncommercial-only photos. See https://collection.sciencemuseumgroup.org.uk/objects/co8247285/series-of-photographs-showing-phases-of-movement-of-a-running-man

### CPU-only A/B benchmark design (future)
1. Once a byte copy of the Commons JPG is safely fetched and SHA-256 computed, record exact revision/license screenshot, original SHA-1 verification and chain of custody in the rights ledger. Work on the historical science diagram, not museum NC reproductions.
2. Apply Pillow/OpenCV grayscale thresholding to the high-contrast runner strokes, crop only the 1891 chronophotographic portion (exclude printed caption), and **manually validate** foot/hip/head sampling because overlaid multiexposure lines cross and naïve silhouette segmentation may misassign positions.
3. Generate a CSV of up to 6–12 measured poses or root positions, with confidence flags. Normalize source times only after validating exposure cadence; do not infer frame rate from spacing without documentation.
4. Compare (A) existing sinusoidal root trajectory vs (B) cadence/trajectory estimated from verified Marey positions on a **separate CPU motion-control test** using 72 deterministic frame samples at 24fps, same original artwork and camera. Gait requires a proper original full-body rig: **present 768×768 art is head-and-shoulders only, so no footfall/gait quality claim is permitted.** Until full body exists, demonstrate extraction and trajectory continuity only (CSV/plots, not re-enacted running).
5. Track derivatives (velocity/acceleration), hold-frame percent, joint continuity and drift. Do not adopt a motion pattern unless human visual review shows actual improvement. Do not integrate Marey imagery into finished character scenes without rights audit.

## Next sprint decision and stop condition
Next should fix **Japanese depth/occlusion on this original layered PSD** without rewriting Anime2.5DRig, then visually compare blinking, mouth and hair under fixed timeline with Stretchy. Separately implement public-domain motion data ingestion only after actual asset rights and checksum are documented. Preserve branches and the per-blocker two-attempt stop rule.
