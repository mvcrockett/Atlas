# Sprint 7F — Private Native Art Ingress Readiness (Evidence)
Date: 2026-11-06
Status: **PRIVATE ORIGINAL-ART KIT BUILT / SECURE TRANSPORT CONTRACT TESTED / NATIVE PRIVATE HEROINE RENDER BLOCKED.**

## Branch history and exact verification
- Started from 7E `5e54bc513a14f698367347b22c774dc9983c958c`.
- Created independent branch `no-pants-sprint7f-secure-native-puppet`. No merge to `main`; prior branch histories preserved.
- 7E genuine native Stretchy **synthetic-only** 5s pipeline succeeded: https://github.com/mvcrockett/Atlas/actions/runs/42269637429 .
- 7F source-only security CI: https://github.com/mvcrockett/Atlas/actions/runs/42272780276 **passed**, using only synthetic generated 128x128 PNGs and fake MP4 bytes; no private art on GitHub.
- Public source: `tools/nopants7f/private_transport.py` verifies flat ZIP integrity, digest, filenames, bounded size, eight private rig layer names, 120-frame schedule, PNG sizes and private status. It also provides AES-256-GCM evidence sealing/opening with independent 12-byte random nonce and authenticated AAD. `test_private_transport.py` covers corrupt hash, synthetic valid input, ciphertext round-trip and wrong-key rejection.

## Private input prepared OFF-GITHUB
- Actual owner-approved portrait, SHA256 `df39186b3d96856062167417d5f1f02f9a9e65a419b31a88b5ab46c01ee1b5e1`. Reference sheet SHA256 `aaa50428100bb549bcb350e3ccf11df276809c4e1308e0a8e79d9a41ea63a1cc`.
- Private native input ZIP: `NoPants_Sprint7F_NATIVE_INPUT_PRIVATE.zip`, 12 entries, 1,949,790 bytes, SHA256 `6ebab335357134baefb2c64ae6c01edf0427943703beab2c252300a06f54229b`. Contains manifest, schedule, dialogue audio, source crop and eight RGBA 650x650 native art slots. Local source-only validator passed against its actual ZIP contents. A ZIP is **not encrypted at rest** and must be handled privately.
- Private 7F art preview includes feathered experimental eye and five mouth shapes. Original pixels outside edits preserved. Pixel-change fraction relative to source (threshold any RGB channel difference >8) approximately: rest 2.03%, small 2.09%, medium 2.19%, wide 2.36%, rounded 2.07%, closed-eye blink 4.89%. These are diagnostic locality numbers, not quality scores.
- Facial preview still exhibits skin fill seams especially on closed-eye blink. Face underpaint still estimated, not genuinely recovered hidden artwork. No full independently rigged hair, neck, or shoulder art.
- `NoPants_Sprint7F_Private_Production_Kit.zip` and `VISUAL_REVIEW_7F.jpg` delivered privately to the conversation; **neither uploaded to public repo or CI**.

## Native private rendering BLOCKER
Sprint 3E private-art ingress design still needs (a) safe, owner-consented authentication / ephemeral art hosting and (b) encrypted repository secrets `NOPANTS_ART_BUNDLE_URL`, `NOPANTS_ART_BUNDLE_SHA256`, `NOPANTS_EVIDENCE_KEY_HEX`. GitHub connector does not expose repository-secret configuration, and no trusted, approved hosted URL for the private art was established. Therefore **no GitHub Actions private native heroine run was started**; there is no encrypted private MP4 nor video inspection from the native engine.

The pre-existing Sprint 3E ingress validator also only accepts an `UNAPPROVED_TECHNICAL_FIXTURE`/PNG-only ZIP. It cannot consume this 7F canonical artwork bundle without a guarded, scoped update for the new status, WAV audio, five-second schedule and exact source manifest, which remains to be implemented in the next private run workflow. Do not repurpose it without that explicit contract update.

## Secure-next-step design
1. User approves a specific authenticated temporary storage destination that can provide an HTTPS expiring URL, and uses GitHub Settings to provision secrets. Never transmit keys in chat, logs or code.
2. A separate fail-closed 7G workflow checks secret presence WITHOUT revealing values, calls 7F ZIP contract validator on a securely downloaded private ZIP, runs the previously verified 7E Stretchy native WebGL adapter, encrypts only private MP4, metrics and inspected samples, then uploads ciphertext only.
3. Decrypt and review privately; stop if any secret or secure art transport is missing. Never use GitHub Pages or public commits for private art.
4. Once private render is inspectable, have Victoria make the visual decision. Do not claim production readiness based on pipeline tests.
5. Art cleanup: reduce blink skin-patch edges; redraw rig-ready phoneme mouths with consistent geometry and proper occluded underpaint. Hair/neck separate geometry remains deferred.

**Milestone: 7G Secure Private Native Proof + Quality Gate. No production acceptance in 7F.**
