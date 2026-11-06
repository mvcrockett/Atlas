# Sprint 7G — Secure Private Native Heroine Proof: Evidence and Owner Handoff

Date: 2026-11-06. **Status: security contract verified with SYNTHETIC data; real native PRIVATE HEROINE render BLOCKED at owner-controlled hosting/secrets.** Do not conflate the synthetic test with any private art/render accomplishment.

## Baseline and branch safety
- Branch `no-pants-sprint7g-secure-heroine-bridge` created from confirmed 7F commit `685d7672612d44382c47e7dbf990add27d17b6fc`.
- `main` observed at `8e4e21b556c62b9d28b93e9c4471b02b246950b1` before sprint, left alone.
- 7F AES-GCM / ZIP test: https://github.com/mvcrockett/Atlas/actions/runs/42272780276 (previous passing control).
- Native upstream Stretchy with synthetic art: https://github.com/mvcrockett/Atlas/actions/runs/42269637429 (previous passing 120-frame control, **not the heroine**).

## Private input independently inspected locally
- Exact local source `NoPants_Sprint7F_NATIVE_INPUT_PRIVATE.zip` present, integrity check `testzip()==None`, 12 ZIP members, 8 full-canvas RGBA layers 650×650, a 5-second/120-frame schedule, and original synthetic dialogue WAV. ZIP SHA-256 `6ebab335357134baefb2c64ae6c01edf0427943703beab2c252300a06f54229b`.
- Manifest status `PRIVATE_CANONICAL_EXPERIMENTAL`; production_art_ready false; native_render_verified false. The approved original portrait source hash is `df39186b3d96856062167417d5f1f02f9a9e65a419b31a88b5ab46c01ee1b5e1`.
- Source image bytes and derivative art remain in the chat's working/private artifact locations; **none committed or transmitted to hosting**.
- Face base opaque, eye and mouth sprites alpha-isolated; art still has eyelid/underpaint seams, imperfect mouth alignments and no true independent hair/neck/shoulder rig. No artist quality gate passed in this sprint.

## Code delivered (public safe)
1. `tools/nopants7g/private_bridge.py`: HTTPS-only input and redirect checking, bounded private download, SHA-256 + 7F bundle validation before extraction, authenticated AES-256-GCM output sealing; no URL, key or private pixels in logs.
2. `tools/nopants7g/test_private_bridge.py`: exercises synthetic 12-file artwork only, digest rejection, HTTP rejection, exactly 120 schedule entries, encryption/decryption, wrong/missing data refusal. Does not access the user's heroine.
3. `.github/workflows/no-pants-7g-safe-contract.yml`: branch-safe synthetic test, no secrets, no private images.
4. `.github/workflows/no-pants-7g-private-staged.yml`: **not activated**; manual-only, protected `nopants-private` environment required, upstream Stretchy pinned at `24a83a27ba43e43e9d2e3de5e33994594e6199c2`, Ubuntu 24.04, render via existing 7E adapter, ciphertext-only upload (1-day retention). No input art ever publicly uploaded.

## Test evidence
- https://github.com/mvcrockett/Atlas/actions/runs/42314859236 — **success**, synthetic secure-ingress and AES-256-GCM contract test only.
- No 7G native private heroine video, no private render frames, no decrypted private output, and **no visual approval**. The private workflow was not dispatched because owner-approved hosting and encrypted secrets are absent/unverified.
- No paid services purchased or user desktop setup requested.

## Exact block
This GitHub connector can create branches/files and inspect workflow runs but cannot configure repository/environment encrypted secrets or guarantee owner-approved authenticated private hosting. A private art upload to any third party was not authorized. **Do not use public GitHub history, Pages, public workflow artifacts, issue comments, or logs as a shortcut.** No default-branch merge was done; a workflow_dispatch file on an isolated branch may not appear in GitHub's regular Run Workflow UI until reviewed and merged to default branch.

## Phone-first OWNER actions, only when the owner explicitly chooses to proceed
1. Select/approve an authenticated file host/destination for the private ZIP. Do not assume Dropbox/Drive/other third-party upload is approved merely because it is connected. Prefer short-lived HTTPS links with strict expiry and restricted access. Any signed download URL is a secret.
2. In GitHub `mvcrockett/Atlas` Settings → Environments, create `nopants-private` with approval/reviewer protection if supported. Configure **environment secrets**, never paste their values into chat/issues:
   - `NOPANTS_ART_BUNDLE_URL`: privately hosted, time-limited, direct HTTPS ZIP download link.
   - `NOPANTS_ART_BUNDLE_SHA256`: SHA-256 of the **exact ZIP bytes**; current local 7F ZIP digest above is valid only if this exact package is hosted unchanged.
   - `NOPANTS_EVIDENCE_KEY_HEX`: randomly generated 32-byte AES key expressed as 64 lowercase hex characters, retained separately and securely by the owner for later decryption; losing it makes ciphertext unrecoverable.
3. Before any run, review the staged workflow and protected environment permissions, then explicitly authorize a carefully reviewed merge of that workflow into `main` (otherwise regular manual Run Workflow UI may not show it). This sprint did NOT merge.
4. Use GitHub Actions → staged private workflow → Run workflow, approve protected environment, monitor result without exposing credentials. Only AES-GCM ciphertext may be downloaded.
5. A phone-only local decryption/review interface is NOT yet implemented; do not claim that the ciphertext is viewable on iPhone without secure client-side tooling.

## Single next milestone
**Sprint 7H — Owner-Approved Private Transport Provisioning & Authentic Native Render.**
First collect the owner's explicit destination choice and access configuration. Then, and ONLY then, run the verified native 7E adapter through 7G protected ingress, inspect real decrypted 120 frames and the exact heroine video, and request Victoria's visual sign-off. If protected secrets are unavailable, fail closed and produce setup diagnostics without touching private art.
