# Operation No Pants 4.0 — Sprint 4A International integration audit
Date: 2026-11-06. Status: **INTERFACE-READINESS ONLY; NO NEW ANIME RENDER**.

## Primary discovery
See-through ALREADY exports semantic multilayer PSD and Stretchy ALREADY has PSD import, semantic tag organization, mesh controls and rigging support. No custom PSD parser or heavyweight bridge should be invented until their existing native import is tested. [Stretchy's docs](https://github.com/MangoLion/stretchystudio/blob/master/docs/README_internal.md) explicitly call out **See-Through PSD** as a preferred upstream workflow. This shortens the roadmap: use the supported PSD import wizard, then automate the smallest necessary wrapper.

## International candidates / licensing / I/O / costs
| Component | Geographic evidence | License (verify model assets separately) | In → Out | CPU/GPU | Decision |
|---|---|---|---|---|---|
| See-through | Saint Francis University Hong Kong + U Pennsylvania + Spellbrush/Shitagaki Lab | Apache-2.0 source, confirm checkpoints/dependencies | original anime PNG/JPG → layered PSD (up to 23 semantic/depth layers) | GPU, 12–16 GB default; NF4 ~8 GB; first-time multi-GB model download | **NEXT PRIORITY: native PSD compatibility and permission-safe test** |
| Stretchy Studio | Maintainer Nguyen Phan; do not infer a country | MIT | PSD/PNG → meshes, rig + spritesheet/sequence/Spine | CPU + WebGL2 headless SwiftShader demonstrated in NoPants CI | **RETAIN PRIMARY** |
| OpenToonz | Italy/Japan (Toonz/Ghibli) | Modified BSD main code, thirdparty terms vary | scene levels/sequences → composited scenes, CLI tcomposer / ToonzScript | CPU mostly; Linux installation complexity | **Defer to post-rig camera/composition validation** |
| The Anime Scripter | international maintainers; no country attribution without evidence | AGPL-3.0 software plus model-specific terms | video/images → restoration/RIFE/dedup/interpolation | GPU expected for fast processing, NCNN Vulkan alternatives | **Optional independent postprocessing; commercial compliance review first** |
| Wan 2.2 Animate | China / Alibaba | Apache-2.0 code, model assets separately | driving video + character image → posed animated video | high VRAM; quantized third-party workflows vary | **DEFER GPU** |
| Synfig | global community | GPL-3.0 | .sif/.sifz → CPU frames/video | CPU runner verified earlier | **KEEP fallback** |

### Existing evidence / branch isolation
- Existing Farnebäck control and 24fps MP4 workflows untouched.
- Real detailed artwork from prior Sprint 3D was processed only by local proxy. Stretchy native anime-art execution remains **unverified**.
- Sprint 3E branch has fail-closed secure asset/artifact workflow. Public repository; art approval = false.
- New 4A branch is based on Sprint 3E, keeping prior branch heads unchanged.
- 4A GitHub smoke test downloads ONLY three public small source files (not user artwork or any model weights), checks current interface markers, and uploads no visuals.

### Compatibility contracts and potential gaps
1. See-through CLI: `inference/scripts/inference_psd.py --srcp <image> --save_to_psd` → layered `.psd`.
2. Stretchy: `src/io/psd.js::importPsd(buffer)` uses `ag-psd` to read rasterized layers; `src/io/psdOrganizer.js` groups recognized names (hair, face, eyes, neck, mouth, topwear etc.).
3. Possible **PSD naming/order and image metadata mismatch**; native import may render yet need explicit joint/pivot cleanup. Layer transparency/occlusion quality requires actual visual inspection.
4. 4A smoke test checks source surface contracts **only**. No PSD is converted or imported in this sprint.

### Next constrained sprint: 4B
- Start with the **public See-through sample illustration** or a separately authorized image. Do not silently upload user art to public inference services.
- Obtain one layered See-through PSD via demo or suitable GPU hardware; if blocked, use an already published nonprivate See-through sample PSD or construct a small synthetic PSD purely for **byte-level parser compatibility**, clearly not an anime-quality test.
- Import the PSD using Stretchy's existing PSD parser and organizer on a sandboxed environment, not a new parser.
- Verify correct layer count/order, transparent masks, face/hair overlap and correct named groups; animate one modest motion and inspect 48 actual frames only if the native import succeeds.
- Preserve model license review and private asset boundaries; do not download large checkpoint or spend money. Two-attempt circuit breaker.
- **Phone-first:** The user pushes a conversational action. If private login or consent is unavoidable, request just the single necessary user approval, not a long manual technical setup.
