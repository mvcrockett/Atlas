# 🌏 NoPants 4.0 — Public-Domain International Animation Research Checkpoint
**Date:** November 6, 2026. **Scope:** metadata/rights research only. **No art downloaded, rendered, or integrated.**

**Policy:** select only artworks expressly marked *Public Domain* by their holding institution or Wikimedia Commons with appropriate age and jurisdiction evidence; distinguish metadata-only PD from actual downloadable media. A portal's copyright badge is not a substitute for item-level clearance. Do not include music, live-action film fragments, film restorations, recent edits, or modern animations with unclear multiple contributor rights. Protect private unapproved heroine.

## Five shortlisted items: 5 source/rights ledger entries

| ID | Jurisdiction/artist | Source, stable object URL | Date | Host rights representation | Use for NoPants | Clearance confidence and caveats |
|---|---|---|---|---|---|---|
| PD-01 | United Kingdom/United States: Eadweard Muybridge (1830–1904) | National Gallery of Art, `Plate Number 626. "Annie G." galloping`, https://www.nga.gov/artworks/167044-plate-number-626-annie-g-galloping | 1887 | **Public domain and free media**, NGA open access; original 1887 work. See also Wikimedia Commons Public Domain Mark https://commons.wikimedia.org/wiki/File:Muybridge_race_horse_gallop.jpg | Sequential locomotion frames; test gait contact positions, cadence, motion/foot acceleration and optical-flow continuity | **CLEAR for U.S. and artist's life+100 countries as historical work**, subject to exact digital asset's terms; recommend NGA file rather than 2006 reedited derivative for benchmark |
| PD-02 | France: Étienne-Jules Marey (1830–1904) | Wikimedia Commons `Image chronophotographique d'un coureur.pdf`, https://commons.wikimedia.org/wiki/File:Image_chronophotographique_d%27un_coureur.pdf | 1891 | Wikimedia Commons **Public domain** for historical Marey chronophotograph; original source named in Commons file summary | Human-run motion trajectories: extract joint paths, foot contact and gait tempo; no generative model required | **CLEAR as historic work in U.S. and France/EU life+70**. Local recent PDF packaging/scan can carry terms under some jurisdictions; use unaltered Commons historical image and preserve metadata, no new editorial material |
| PD-03 | Japan: Katsushika Hokusai (1760–1849) | Wikimedia Commons `Hokusai manga - hokusaimanga07kats.pdf`, https://commons.wikimedia.org/wiki/File:Hokusai_manga_-_hokusaimanga07kats.pdf | Before 1850 | Wikimedia Commons public domain in origin/life+70 countries and U.S. (published well before 1931), Public Domain Mark; scan sourced from Internet Archive | Pose vocabulary, silhouette clarity, expressive gestures, line economy. Not a sequence of film frames | **CLEAR historical sketches** under long-expired terms; individual frames/pages should be checked for scans/editorial marks before redistribution |
| PD-04 | China: Shitao/Zhu Ruoji (1642–1707) | Metropolitan Museum of Art `Landscapes`, object `1989.363.154a–h`, https://www.metmuseum.org/art/collection/search/49179 | ca.1690 | The Met item marked **Public Domain** and **Download Image**; Met Open Access permits unrestricted commercial and noncommercial uses | Authentic atmospheric background, compositional depth, scrolling camera/pan/parallax benchmarks; cultural source reference | **CLEAR** institution-verified open access, U.S. + historical Chinese/other life+70 territory expiration |
| PD-05 | Korea: Kim Su-gyu (active late 18th–early 19th century) | Metropolitan Museum of Art `Rainy Landscape`, object 2006.104, https://www.metmuseum.org/art/collection/search/73188 | late 18th century | The Met item marked **Public Domain** and **Download Image**; Met Open Access permits unrestricted commercial and noncommercial uses | Atmospheric rain/fog layers, river/bridge parallax and slow camera motion | **CLEAR** institutional designation; historical work firmly before modern terms; avoid misrepresenting it as anime-style character art |

### Verification references
- National Gallery of Art artwork record calls Muybridge plate's media free/public domain: https://www.nga.gov/artworks/167044-plate-number-626-annie-g-galloping
- Wikimedia Commons original Marey file page with author/date/licensing: https://commons.wikimedia.org/wiki/File:Image_chronophotographique_d%27un_coureur.pdf
- Wikimedia Commons original Hokusai scanned sketchbook metadata and Public Domain Mark: https://commons.wikimedia.org/wiki/File:Hokusai_manga_-_hokusaimanga07kats.pdf
- Met Shitao public-domain item and Download Image: https://www.metmuseum.org/art/collection/search/49179
- Met Kim Su-gyu public-domain item and Download Image: https://www.metmuseum.org/art/collection/search/73188
- Met Open Access policy covers unrestricted commercial/noncommercial use of art identified as PD: https://www.metmuseum.org/about-the-met/policies-and-documents/open-access

### Exclusions: why other archives were not selected yet
- Early film and animation archives: year of production alone does not establish rights to modern film restorations, scores, titles, performer rights or country-specific copyright; excluded.
- Europeana: aggregator items have **different item-level rights labels**, including In Copyright and CC-BY-NC; the portal as a whole is not public domain. Review actual object labels before adding future entries.
- National Korean/Chinese/Taiwanese film archives: a cultural institution's public web access is not proof of public-domain, commercial-reuse rights. No Taiwan-specific item met this review's proof threshold; do not invent one.
- Do not treat Wikimedia Commons "unknown photographer" + U.S.-only tag as cleared worldwide (e.g., some Shanghai 1920s street photos).
- A repository's code license has **no authority over sample artwork copyright**.

### Rights and commercial reuse rule
These five are **strong institutional/Commons public-domain candidates**, with U.S. and relevant source-country age or institutional rights evidence. Actual project commercial release must retain exact-item source page, capture date, downloaded-file checksum, attributed author/title, rights statement snapshot and check distribution target's laws (e.g. moral rights and modern photograph reproductions may require review). **No blanket assertion of universal worldwide legal certainty.** Nothing is authorized for publication by a bare search result.

## Candidate benchmark: PD-02 Marey running, 72 frames / 3 seconds / CPU only
Objective: learn whether historical motion *reference* improves our existing anime rig while keeping **our own original anime character art** as the visual subject.

1. Download only the Commons 1891 Marey PDF image (< 300KB) after capture/verify the original item's PD license and SHA-256; crop/threshold 2–6 runner/foot silhouette positions manually or algorithmically into sparse joint/foot trajectories.
2. Use deterministic Python/OpenCV or Pillow CPU preprocessing, no model weights and no major downloads. Do **not** copy the historical photograph into the produced anime render: only export numerical foot-contact and root-sway timing controls.
3. A/B against a matched 3-second anime idle or walk-pose rig: **A** existing sine timing, **B** the Marey-derived timing. Same character art, resolution, 24fps, 72 sampled frames, camera and renderer. Only timing/pose trajectories differ.
4. Measure contact drift, root displacement smoothness, limb trajectory plausibility, 72-frame hashes, frame-to-frame change and seam/flicker; visually inspect outputs after the original legal anime benchmark renders correctly.
5. Stop if no usable skeletal limbs exist in the current asset; our Sprint 4D lavender portrait is head-and-shoulders only, so **a footfall/run study is not technically applicable yet**. In that case run a smaller **head oscillation vs chronophoto-derived torso displacement** test and mark it a proxy, or defer Marey gait until a full-body original rig exists.
6. Success gate: demonstrate measurable improved motion in a CPU runner and human-auditable montage, without degrading identity or creating fictitious anatomy. **No asset ingested or code integrated during this research checkpoint.**

## Sprint 4D current status
Branch `no-pants-4d-original-art-matched-benchmark` exists and original legal 768px layered artwork recreation, ag-psd builder, test-only Anime2.5DRig fixed-time injector and dual-engine GitHub workflow were committed. Initial run https://github.com/mvcrockett/Atlas/actions/runs/42238959340 failed in BOTH jobs before rendering because ag-psd required `initializeCanvas` in the Node PSD writer. **Do not claim either engine completed an original-art benchmark.** One material attempt has been used; a second distinct attempt must fix ag-psd's Node Canvas initialization or switch to a browser ag-psd PSD build, then rerun and verify output. Preserve main and other branches.
