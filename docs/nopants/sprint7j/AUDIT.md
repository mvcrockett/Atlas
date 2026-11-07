# Sprint 7J — Actual private native rendering and source-resolution export

Date: 2026-11-06 (America/Chicago). Branch: `no-pants-sprint7j-native-fidelity`.
Engineering commit: `69ed6cc5e028d47ad38ad5ed461532923ffe0503`.
Exact tested source tree: `45968d5a0aa18ef1e5ed20e5e42a98a4689e9661`.
Base: Sprint 7I `44fec0372c679e7b6dcc0702b81f3bfb693ef13b`, descendant of requested 7H `0b35e676ec947827585fff1efb7cf360c0e6ddd7`.
Main observed: `8e4e21b556c62b9d28b93e9c4471b02b246950b1`. Main and prior remote branches were not modified.

## Outcome and scope
**VERIFIED:** actual private 7F heroine layers rendered with native upstream Stretchy ScenePass and computePoseOverrides; 120 decoded frames, 24 fps, 5 seconds, audio 5 seconds. Code runs in this Work workspace on CPU/SwiftShader, without a user desktop or external private-art transfer. No public private-art artifacts. The private MP4 was returned to the owner in ChatGPT.
**PARTIALLY VERIFIED:** facial expression fidelity. All 120 decoded frames inspected as a contact sheet and six larger decoded samples inspected. This is frame inspection, not a claim of real-time playback/listening or owner acceptance.
**EXPERIMENTAL:** blink and lip artwork; rigid portrait motion only. No walking, turning, independent hair/clothing deformation or body acting.
**BLOCKED:** unattended iPhone-to-protected-GitHub private production, iPhone execution/key-retention verification and supported ciphertext upload routing. The connector cannot configure secrets. No Dropbox upload, share, key generation, environment provisioning or private workflow dispatch occurred.

Mission: remove the native private-render blocker and preserve original pixel detail. One renderer, existing assets, zero paid spend; bounded dependency fallback and targeted export/security repairs. This replaces the previous assumption that third-party hosting is always prerequisite to native private rendering: it is unnecessary when the current authorized workspace can run headless Chromium itself. It does not solve encrypted phone-to-GitHub transfer.

## Recovered history: evidence levels
The repository's historical reports were read; historical videos were not independently downloaded/re-reviewed this session. Their findings remain attributed prior evidence rather than new test passes.

| Stage | Recovered finding | Present interpretation |
|---|---|---|
| Early Sprint 1 / phase work | Blender geometric output; Synfig format repairs; mocked 16-test execution bridge; GPU demo status without actual GPU video | Preserve; no production anime proof |
| Continuous engine | CPU Farneback 120-frame interpolation on synthetic keyframes | Existing experiment; cannot repair missing anatomy or create genuine acting |
| Sprint 2 | Native headless Stretchy control, separate Synfig CLI fallback | Reusable native renderer and CPU compositor |
| Sprint 3A–3E | Art-to-rig bridge, native synthetic control, local detailed-art proxies, secure ingress design | Synthetic native and private proxy outputs were distinct |
| Sprint 4A–4C | PSD interface/parser/import tests; Japanese Anime2.5DRig benchmark; timing/rights limitations | PSD path usable; mismatched sampling invalidates simplistic engine rankings |
| Sprint 4D / 6A | Original benchmark art rendered in two native engines; Japanese depth-sort repair; Synfig invocation; Inochi launch only; OpenToonz packaging screen | Prior original-art render exists, but not this private heroine; no new tournament needed |
| Sprint 5 | No separately named Sprint 5 branch/report found in inspected history | Do not invent a milestone |
| 7A–7D | Readiness, real Rhubarb cues, 120-frame schedule, source-locked local nonnative puppet | Timing and source fidelity available; native private connection absent |
| 7E | Reported native synthetic 120-frame control at run 42269637429 | Baseline renderer reused here |
| 7F | Private 12-entry bundle + integrity/AES-GCM contracts | Exact bundle recovered and validated here |
| 7G | HTTPS ingestion + encrypted evidence; staged private workflow | Contracts pass locally; private remote execution not established |
| 7H | Exact encrypted Dropbox destination approval; key custody/upload/secret blockers | Approval remains limited to that destination and ciphertext |
| 7I | Password-derived AES-256-GCM input adapter and staged workflow | No browser encryption UI exists in this branch; synthetic tests alone do not establish iPhone interoperability |
| 7J | Native private render, full-resolution export, path/audio repairs, redirect protection | Actual increment in this session |

`BRANCH_BASELINES.txt` records the inspected remote branch heads. Reports also inspected include `quality_tournament/SPRINT2.md`, `quality_guardian/SESSION_HANDOFF.md`, `benchmarks/art-to-rig/SPRINT3D_REPORT.md`, international 4A/4B/4C/6A reports and 7C–7H handoffs. Historical handoff instructions to publish artwork are superseded by current explicit privacy restrictions.

## Bottlenecks and fixes
1. **Wrong asset path:** staged 7I extracts to `nopants7i-private-art` but copied from `nopants7g-private-art`. Fixed exact source path.
2. **Wrong audio path:** staged art/audio lives under the upstream checkout; capture assumed repository-relative `art/dialogue.wav`. Added explicit `NOPANTS_AUDIO_PATH` and set it in 7G/7I staged workflows.
3. **Detail loss:** fixed 480x480 capture shrank 650x650 layers to 450x450. Added native mode with 1:1 source pixels, integer placement and 16-pixel motion margin. Legacy framing remains available. Output 682x682, even dimensions for H.264.
4. **Black overscan / privacy labeling:** explicitly matte transparent export on white; classify private source as `PRIVATE_ARTWORK`, not the former hardcoded synthetic label. Fail on unknown status.
5. **Weak evidence:** verify audio duration plus video dimensions/count/fps; refuse nonempty output directories rather than mixing stale frames. Record unique hashes, adjacent holds, temporal method and duration. No inferred artistic pass.
6. **Reproducibility:** `run_local.py` verifies the pinned, clean renderer source; validates the ZIP; runs a loopback-only static server and removes temporary input staging. Native ScenePass dependencies do not need the entire Vite UI or pnpm installation for this local path. Browser blocks third-party requests.
7. **Redirect integrity:** former 7G/7I checked final URL only, after an insecure intermediate request could already occur. Shared HTTPS redirect handler rejects downgrade/userinfo before following. AES-GCM formats unchanged.

No original image, generated layer, model weight, video, private URL or key was committed. Native source pin: `MangoLion/stretchystudio@24a83a27ba43e43e9d2e3de5e33994594e6199c2` (MIT).

## Actual rendered evidence
Source ZIP `NoPants_Sprint7F_NATIVE_INPUT_PRIVATE.zip`: 1,949,790 bytes, SHA256 `6ebab335357134baefb2c64ae6c01edf0427943703beab2c252300a06f54229b`; 12 files, 8 RGBA layers 650x650, validated schedule. Source readiness flags intentionally remain false.

| Metric | Legacy framing control | Native detail mode |
|---|---:|---:|
| Frame canvas | 480x480 | 682x682 |
| Actual art area | 450x450 | 650x650 |
| Decoded frames / fps / duration | 120 / 24 / 5 sec | 120 / 24 / 5 sec |
| Audio stream duration | 5 sec | 5 sec |
| Unique source PNG hashes | 59 | 70 |
| Adjacent identical source PNGs | 41 | 28 |
| Sampled timeline poses | 120 | 120 |
| Pixel-flow/generated interpolated frames | 0 | 0 |
| Mouth drawings exercised | rest, rounded, small, medium | same |
| Blink frames | 10 | 10 |
| Capture + encoding wall time | 5.353 sec | 8.939 sec (repeat) |

70 unique image hashes are NOT 70 independently authored drawings. Transform keyframes are interpolated by native easing at 120 times, while eye/mouth drawings switch discretely. Repeated image hashes arise from subtle movement/quantization and repeated poses. No RIFE generation or invented body motion.

Measured frame-zero RGB MAE against the same alpha-composited layer reference: native **0.00353/255**, maximum channel error 1. Legacy reconstruction, after cropping its 450px art and Lanczos resizing to 650px: **1.23704/255**. Native avoids destructive downsampling (650²/450² = 2.086x art pixels). This compares renderer fidelity to prepared layers, NOT anatomical correctness or fidelity of inferred underpaint to original hidden anatomy. Video compression differs from these uncompressed PNG measurements.

Native MP4: 536,499 bytes; SHA256 `a49122ff5673b499cf538e39e473b877a7cbf2d4ac747faa251c0f7822b55523`.
Aggregate SHA256 of concatenated per-frame SHA256 digests in order: `d75de35ee38473b733718a43ecb65709efea984ea2cc59f39aae14e73ea2840d`.
Independent run via the new launcher reproduced the exact MP4 and all PNG bytes. Same runtime only; no cross-browser determinism claim.

Visual assessment: source hair, jewelry, face and clothing detail preserved; no gross identity replacement or missing face. Eye closure exposes broad skin-colored patch edges and abrupt state changes. Mouth changes are visible but stylized; exact heard phoneme alignment has not been judged. Head movement is tiny and moves the whole rectangular portrait including its background; this is not separated head/body anatomy. No optical-flow ghosting added; small sampling shimmer is not excluded by contact-sheet review. Owner artistic acceptance pending.

## Executed tests and failure log
- `node --test benchmarks/native7e/test_render_contract.mjs`: **6/6 passed** (geometry, legacy compatibility, invalid geometry, privacy, decoded streams, staged path/audio regression).
- `python tools/nopants7g/test_https_download.py`: **4/4 passed**, including simulated insecure redirect refusal before follow-up network access.
- Existing 7C schedule, 7D manifest, 7F ZIP/AES-GCM, 7G ingress/output and 7I encrypted input scripts: **all executed and passed**. These are assertion scripts; do not invent a unittest case count.
- Actual native render and decoder validation: passed in native and legacy modes; native repeated through local launcher with identical output hashes.
- `git diff --check`: passed.
- No new GPU job or remote private render executed. GitHub source-only CI status must be checked separately; it does not establish a private remote render.

Failures honestly recorded: Playwright's standard browser CDN returned invalid/truncated ZIPs and its internal downloader auto-retried before being stopped. Switched once to npm-distributed `@sparticuz/chromium@143.0.4`; archive automatic extraction hit unsupported chown in this filesystem, resolved by decompressing supplied Brotli files and extracting with `tar --no-same-owner`. Initial browser probe found no reachable server across process sessions; a same-process server lifecycle solved it. `/usr/bin/time` absent; Python resource measurement used instead. First redirect-test harness allowed the environment proxy ahead of its fake handler and produced two HTTP 503 errors against synthetic `.example` targets; corrected by disabling proxies in that test-only opener and replacing the HTTPS handler, then 4/4 passed. No private bytes were sent by those tests. Shell git push lacked credentials; connector tree/commit publication used instead. Remote source tree matched the locally tested tree exactly.

## Cost and reproducibility
Additional cash spending initiated: **$0**. No subscriptions, paid APIs, rented GPUs, billing changes or user computer setup.
Measured native launcher: 9.634 sec elapsed; child user CPU 5.872 sec, system CPU 0.758 sec; `ru_maxrss` 275,332 KiB (~269 MiB maximum child RSS, not summed process-tree peak). SwiftShader software rasterization. MP4 ~524 KiB; private full-frame scratch evidence ~100 MB. Browser compressed payload ~64 MiB; browser runtime directory including compressed/extracted copies 398 MiB, upstream source directory 6.9 MiB; pinned upstream source clone and existing Node/Python/FFmpeg dependencies. Shared platform resource costs are not a cash invoice or free-tier guarantee.

Reproduction: install Playwright in `benchmarks/native7e`, provide its Chromium (or set `NOPANTS_CHROMIUM_PATH` to a compatible executable), FFmpeg/FFprobe, Python Pillow/cryptography; clone pinned upstream source. Then:

```sh
python benchmarks/native7e/run_local.py \
  --stretchy /absolute/path/to/stretchystudio \
  --bundle /private/path/NoPants_Sprint7F_NATIVE_INPUT_PRIVATE.zip \
  --sha256 6ebab335357134baefb2c64ae6c01edf0427943703beab2c252300a06f54229b \
  --output /private/path/new-empty-render-directory
```

Do not place private inputs/outputs in public git. `--mode legacy` is the matched framing control. No encrypted input required for local-only authorized workspace processing; remote ingress continues requiring authenticated encryption. The current proof uses Playwright 1.62.1 runtime package with Chromium 143 fallback; staged workflows still specify Playwright 1.55 and have not been rerun with private data.

## Next sprint, in order
1. **Visible quality:** author source-aligned closed/half-closed eyes with appropriate skin/occlusion masks, preserving canonical identity. Two distinct art approaches maximum; inspect the full blink sequence. Do not warp the full portrait to fake a nod.
2. **Real movement:** build independently underpainted face/hair/neck/shoulder layers, then small pivot-based head motion and one hair strand. Keep baseline for matched A/B review; fail on revealed gaps and depth inversions.
3. **Phone security:** recover the existing conversation-only 7I browser encryptor reported by the concurrently updated 7I branch, inspect its exact source and prior interoperability harness, then verify actual iPhone execution, off-chat owner key custody and the injected ciphertext upload handle. Only approved Dropbox path `/NoPants_Sprint7H_ENCRYPTED_INPUT.bin`. No invented upload handles or secret capture in chat.
4. **Remote production:** verify protected environment and owner-configured secrets, exact input-copy/audio path tests, then obtain any still-required merge/dispatch approval. No default-branch merge in this session. Private outputs remain ciphertext-only on GitHub.
5. **Scene production:** only after usable character layers, extend shots to composition, independent body gestures and audio-directed timing. Evaluate GPU repair only when an authorized genuinely free compute path exists.

## Continuation prompt
Atlas, continue No Pants Studio from branch no-pants-sprint7j-native-fidelity, engineering commit 69ed6cc5e028d47ad38ad5ed461532923ffe0503. Read docs/nopants/sprint7j/AUDIT.md and the latest branch head first. Preserve main and all prior branches; create a new isolated branch. Sprint 7J rendered the exact private 7F heroine with pinned native Stretchy locally: 120 frames, 24 fps, 5 seconds, 682x682; MP4 SHA256 a49122ff5673b499cf538e39e473b877a7cbf2d4ac747faa251c0f7822b55523. Recover the private input and rendered MP4 from ChatGPT files, never public git. Prioritize repairing the visibly broad closed-eye skin patches and adding a properly authored half-blink layer, then render a matched before/after with the existing native launcher and inspect decoded frames. Keep real layer separation/underpaint as prerequisite to independent head/hair motion. Use $0 additional cash, two attempts per blocker, no background-work promises. Do not upload plaintext art, expose keys, merge main, or treat synthetic tests as artistic success. The encrypted phone-to-Dropbox path remains separately blocked on owner key custody, actual iPhone execution of the existing 7I client, supported upload handle and protected secrets; only the exact approved ciphertext destination is authorized. Deliver tested code, a privately returned clip, measured metrics, honest visual limitations and the next prompt.

## Files changed in engineering commit

- `.github/workflows/no-pants-7e-native-calibration.yml`
- `.github/workflows/no-pants-7g-private-staged.yml`
- `.github/workflows/no-pants-7i-private-staged.yml`
- `.github/workflows/no-pants-7j-contract.yml`
- `.gitignore`
- `benchmarks/native7e/bridge7e.js`
- `benchmarks/native7e/capture7e.mjs`
- `benchmarks/native7e/render_contract.mjs`
- `benchmarks/native7e/run_local.py`
- `benchmarks/native7e/test_render_contract.mjs`
- `tools/nopants7g/https_download.py`
- `tools/nopants7g/private_bridge.py`
- `tools/nopants7g/test_https_download.py`
- `tools/nopants7g/test_private_bridge.py`
- `tools/nopants7i/ingress_encrypted.py`
- `tools/nopants7i/test_ingress_encrypted.py`

See [RESEARCH.md](RESEARCH.md) for international licensing, CPU/GPU, fidelity, automation and maintenance screening. New documentation adds this audit, that research screen and the branch baseline inventory.

## Remote CI observation

The new source-only workflow is committed on the isolated branch. Connector workflow-run queries returned an empty list for engineering commit 69ed6cc5e028d47ad38ad5ed461532923ffe0503 during this session. **No GitHub CI pass is claimed.** All stated test passes above executed locally against the exact published source tree. Private staged workflows were not dispatched.

## Concurrent 7I update discovered at final preservation check

The 7I branch advanced independently during this Work session, from `44fec0372c679e7b6dcc0702b81f3bfb693ef13b` to `a842088dfcb98d6cf4893572d02039f0337ed860`. This session did NOT change it. Main and the other 20 previously recorded branches were unchanged at the final comparison. The requested baseline audit was correct when selected; this later work is recorded rather than silently overwritten.

Inspected new commits: `1084b71` (private-labelled duplicate capture), `5d82c8a` (staged workflow selects it), `a842088` (encryption evidence handoff). The new [7I handoff](https://github.com/mvcrockett/Atlas/blob/a842088dfcb98d6cf4893572d02039f0337ed860/docs/nopants/sprint7i/IPHONE_ENCRYPTION_EVIDENCE.md) reports a conversation-only `NoPants_7I_Encrypt_Offline.html` and Node WebCrypto/Python synthetic interoperability; Safari execution still unverified. Thus a client was produced elsewhere and should be recovered and audited, not rebuilt without checking. The HTML is not in the repository, so this session has NOT independently verified its bytes or browser behavior. Earlier table statements about absence apply to the repository branch at our initial baseline, not to all user files.

The new `capture7i_private.mjs` fixes privacy labeling but retains the old fixed 480px canvas and checkout-relative audio assumption. Its staged workflow still contains the 7g/7i input directory mismatch. 7J already fixes these issues using the shared privacy-aware capture and explicit audio path. Keep 7J's tested capture/workflow fixes when combining histories; do not blindly replace them with the late 7I duplicate. Both remote branches are preserved; no merge was done.
