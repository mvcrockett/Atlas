# Operation No Pants Studio — Sprint 7H owner approval gate

Date: 2026-11-06
Status: **STOPPED AT EXPLICIT DESTINATION CONSENT**. No private imagery or source bytes uploaded or used for a new native render.

## Verified inputs and baseline
- `main` confirmed at `8e4e21b556c62b9d28b93e9c4471b02b246950b1`.
- `no-pants-sprint7g-secure-heroine-bridge` confirmed at `803dc76afa16d8bc8877340650fbd01510318fe9`.
- Synthetic contract run 42314859236 is complete/successful (NOT a heroine render).
- 7F private native input at private local working path: ZIP is readable, 12 members, zip integrity check clear. SHA-256: `6ebab335357134baefb2c64ae6c01edf0427943703beab2c252300a06f54229b`.
- Manifest checked locally: `PRIVATE_CANONICAL_EXPERIMENTAL`, 650x650, eight named sprite layers, 120 frames at 24 fps. Not production-ready.
- No third-party transfer authorization has yet been granted by the owner. A connected cloud storage account is NOT permission to upload this asset.

## Current architecture
- Native Stretchy + Rhubarb 120-frame SYNTHETIC control verified previously at run 42269637429, separate from user art.
- 7G HTTPS ingress / SHA256 validation / AES-GCM evidence encryption synthetically verified at 42314859236.
- 7G staged private workflow is manual-only, targets `nopants-private` GitHub environment, requires three owner-managed secrets: `NOPANTS_ART_BUNDLE_URL`, `NOPANTS_ART_BUNDLE_SHA256`, `NOPANTS_EVIDENCE_KEY_HEX`.
- Workflow dispatch generally requires a reviewed default-branch workflow; do NOT merge to main without owner approval.
- Current connector cannot create GitHub Actions environment secrets or guarantee private user approval controls.

## Recommended consent choice (not executed)
**Dropbox private storage and time-limited bearer-link workflow, only if owner explicitly approves this destination and its exposure tradeoff.** A typical shared link usable by an unauthenticated GitHub Actions runner acts as a bearer credential: anyone possessing it could fetch the ZIP until it expires or is revoked. An account-only Dropbox invite cannot be consumed automatically by an unauthenticated GitHub runner. Some Dropbox accounts/settings may not support password or link expiry. No actual link capability has been verified for this user's account. Never place raw signed links in chat, issue comments, logs, public repository files, or workflow inputs visible outside trusted secrets.

**Stronger alternative:** client-side encrypt the 7F ZIP before uploading to an approved file host, then separately configure a decryption key as an encrypted GitHub environment secret. This requires an auditable decryption adaptation and key handling, so do not claim current staged workflow implements it.

## Phone-first owner actions once a destination is approved
1. Approve a specific host and exact storage path. Only then upload ZIP (or ciphertext if using the stronger design).
2. Use host UI to create a short-lived direct-download HTTPS link; check that a headless server can download it and does not require interactive browser login. Treat link itself as a secret.
3. In Safari → github.com/mvcrockett/Atlas → Settings → Environments, create/review protected `nopants-private` with required reviewer and branch restrictions if available on this repo/plan. Do not assume controls are active; GitHub may auto-create an unprotected environment if referenced but absent.
4. Add environment secrets directly in GitHub: `NOPANTS_ART_BUNDLE_URL`, `NOPANTS_ART_BUNDLE_SHA256`, `NOPANTS_EVIDENCE_KEY_HEX`. The SHA above only matches the existing unmodified ZIP.
5. Retain independent copy of AES key outside GitHub for decryption. Do NOT transmit secrets in chat.
6. Review native workflow security and request explicit authorization for merging safe workflow to main before launching an actual private production run.
7. Trigger workflow under required environment approval, confirm encrypted-only output; decrypt privately using a trusted viewer, inspect continuous 5-sec clip and 6+ frames.
8. Revoke hosted link and delete remote asset when no longer required.

## Security caveats
- GitHub repository is PUBLIC. No plaintext private art/video/URL/key in Git history, Pages, plaintext artifacts, logs, untrusted PR contexts or console output.
- GitHub-hosted Actions runners receive decrypted art in ephemeral workspace during the render. AES-GCM protects artifact at rest and download, not plaintext while a trusted runner processes it.
- Secrets are not automatically safe from malicious workflow changes. A protected environment and careful code review are important.
- iPhone-only decryption of returned encrypted artifacts is NOT implemented yet.
- Private art still has seams, immature blink and mouth textures, and incomplete hair/neck/shoulder underpainting. Even successful native rendering will not establish production quality.

## Exit result
- 7H branch created only for this consent and exact-owner-action handoff.
- No host selected, no upload, no secret changes, no workflow dispatch, no new 7H render, no visual approval.
- **Next single milestone: obtain Victoria's explicit approval of the specific host/destination and transfer mode, then resume protected provisioning and attempt the authentic native heroine render.**
