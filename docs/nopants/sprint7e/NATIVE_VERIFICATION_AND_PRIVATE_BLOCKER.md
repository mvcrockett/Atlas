# No Pants Studio — Sprint 7E Native-Rig Evidence and Private-Art Blocker

Date: 2026-11-06. Status: **NATIVE STRETCHY 5-SECOND CONTROL VERIFIED — PRIVATE CANONICAL RENDER NOT VERIFIED**.

## Branch and preservation
- Isolated branch: `no-pants-sprint7e-native-private-ingress`; forked from Sprint 7D `be0a7c03d2ad891781b2de297f46b2c2fd24aa1f`.
- `main` observed at `8e4e21b556c62b9d28b93e9c4471b02b246950b1` before sprint; no merges or main mutations made.
- No private image pixels, private asset URLs, private audio, private ZIPs, secrets or unencrypted private render artifacts were committed to this PUBLIC repository.

## User-supplied original image recovery and private kit
- Original portrait SHA256: `df39186b3d96856062167417d5f1f02f9a9e65a419b31a88b5ab46c01ee1b5e1` (1179×2010 JPEG).
- Full reference sheet SHA256: `aaa50428100bb549bcb350e3ccf11df276809c4e1308e0a8e79d9a41ea63a1cc` (1536×1024 JPEG).
- Private working crop: 650×650 from exact portrait, not regenerated.
- Local non-public artifact `NoPants_Sprint7E_Private_Artwork.zip` contains: independent SVG-authored five viseme PNG sprites; separate eye_open source pixels, half and closed painted eyelid overlays; provisional inpainted facial underpaint; source-aligned hair/neck/shoulder reference crops; private art manifest, 120-frame Rhubarb schedule, original synthetic demonstration audio, visual preview and quantitative image-difference report.
- The design remains Victoria-selected; the *art pack is NOT production-ready*. Closed-lid skin transitions are visibly imperfect; mouth sprites are hand-authored but stylized; independently riggable hair, neck and shoulders, and genuine occlusion underpaint do not exist yet. Skin fill is inferred, not recovered behind hair. Test mouth shapes may snap with no in-betweens.
- Outside the facial eye/mouth edit masks, composited previews match source crop exactly. Full frame reconstruction per-mouth MAE ranges roughly 1.28–1.68 RGB levels on 0–255. This only demonstrates original pixels largely retained, not artistic performance quality.
- Private bundle is available as a *conversation file*, not hosted as an authenticated private URL that GitHub Actions can consume.

## Native upstream engine code
- `benchmarks/native7e/bridge7e.js`: imports native upstream Stretchy `ScenePass` and `computePoseOverrides`, loads an art manifest + 120-frame schedule, switches mouth and eyelid layer opacity at distinct frames, and animates gentle native head translation.
- `benchmarks/native7e/capture7e.mjs`: headless Chromium real 120-frame capture, H.264/AAC MP4 generation, decoded-frame checks and motion telemetry.
- `benchmarks/native7e/make_public_fixture.py`: explicitly *synthetic calibration artwork* only, NOT user's heroine; no private art generation or transfer.
- `.github/workflows/no-pants-7e-native-calibration.yml`: real upstream pinned Stretchy clone, Rhubarb 1.14.0 CPU, PocketSphinx mouth cues, Python 120-frame schedule, native WebGL headless renderer, FFmpeg/FFprobe, and upload PUBLIC SYNTHETIC output only.

## Exact CI and two-attempt circuit breaker
1. https://github.com/mvcrockett/Atlas/actions/runs/42269420096 — failed when GitHub `ubuntu-latest` resolved to Ubuntu 26.04, unsupported by Playwright 1.55 Chromium browser installer. Prior steps including real Rhubarb, 120-frame cue mapping and upstream Stretchy clone PASSED; render not attempted.
2. https://github.com/mvcrockett/Atlas/actions/runs/42269637429 — **SUCCESS**, after pinning runner to `ubuntu-24.04`, with native page rendering and 5-second video successfully validated and uploaded.
   
   Metrics from downloaded and independently FFprobed artifact `nopants-7e-public-synthetic-native-control`, artifact ID `13529530124`:
   - Native renderer: pinned Stretchy `ScenePass + computePoseOverrides`
   - 120 captured and 120 decoded frames; 24/1 fps, 480×480, 5.000 seconds
   - H.264 video and AAC audio, both 5.000 seconds
   - 51 unique PNG frame hashes; 10 blink frames; selected automatic mouth states include rest/rounded/small/medium
   - Six downloaded image samples independently inspected; drawn synthetic face shows mouth-change and blink visibility
   - Note: unique hashes prove frame variation, NOT visual professional quality
   - All 7E uploaded video/screens are generic synthetic artwork, *not the lavender heroine*.

## The native PRIVATE heroine blocker
- Existing Sprint 3E encrypted input/output architecture depends on securely hosted private ZIP + GitHub Action encrypted repository secrets: `NOPANTS_ART_BUNDLE_URL`, `NOPANTS_ART_BUNDLE_SHA256`, `NOPANTS_EVIDENCE_KEY_HEX`.
- No verified private HTTPS transport/URL, repository-secret provisioning, AES-256-GCM egress/decrypt and visual review path was available. The user has not authorized public sharing of private art. We **did not attempt to use public source-asset commits or public Pages as a workaround**.
- The new 7E native bridge accepts private manifest/schedule geometry and shapes, but the ZIP has **not been exercised in native Stretchy**; no user heroine native render exists and no such success is claimed.
- This is a security/asset-delivery blocker, not evidence that native engine rejects the private layers.
- A production-quality eye, lip, neck/shoulder/hair art completion remains an independent creative blocker.

## Next single milestone
**Sprint 7F — Secure Private Native Art Runner and Puppet Repair**:
1. First audit the private asset transport and consent; choose a low-cost authenticated, ephemeral upload/download path rather than sharing private URLs or keys in chat. Keep public repo source-only.
2. Reuse native 7E five-second adapter and Sprint 3E crypto; DO NOT re-run an engine tournament or build a new renderer.
3. Improve blink underpainting and artist-drawn mouth/eye expression transitions, no diffuse ghost interpolation. Hair/neck remain static until actual occluded backfill is authored.
4. Execute one genuinely native 120-frame PRIVATE heroine render, encrypt outputs before upload, decrypt privately and compare decoded samples against canonical source. If credentials or secure transport aren't available, report exact blocker rather than publishing artwork.
5. Preserve zero additional paid spending, phone-first approach, two materially distinct attempts per new blocker, and Victoria's explicit final visual approval.

**Visual quality remains unapproved.**
