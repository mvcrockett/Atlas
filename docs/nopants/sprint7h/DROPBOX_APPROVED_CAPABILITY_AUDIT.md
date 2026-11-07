# Sprint 7H — Approved Dropbox destination: capability audit and safe stop
Date: 2026-11-06

## Exact authorization
Victoria explicitly approved storing an **encrypted-only** version of the private heroine ZIP in **her connected Dropbox** at exactly:
`/NoPants_Sprint7H_ENCRYPTED_INPUT.bin`
She expressly forbade plaintext upload, sharing secrets in chat/logs, uploading to public GitHub, or merging `main` without separate approval.

## Verified
- Source file was present locally at `/mnt/data/nopants_sprint7f_private/NoPants_Sprint7F_NATIVE_INPUT_PRIVATE.zip` at inspection: **1,949,790 bytes**, SHA-256 `6ebab335357134baefb2c64ae6c01edf0427943703beab2c252300a06f54229b`, 12 ZIP entries, `testzip() is None`.
- Dropbox connection supports `upload_file` with a **ChatGPT-injected fileParam** `source_file`, not an arbitrary local container file path. No new ciphertext source_file was injected; do not fabricate the parameter.
- Dropbox `download_link` supports temporary single-use bearer HTTPS URLs with lifetime 60–900 seconds. Any first HEAD/Range/GET consumes them. They are **not** durable or login-gated runner integration. They could serve a time-coordinated runner after an owner sets the URL as an encrypted secret, provided it remains unused and unexpired.
- `create_shared_link` for this connector only creates/reuses account-restricted (`no_one`) links; an unattended GitHub Actions runner cannot automatically use an account-only link without supported Dropbox authentication. Do not swap to an anyone-with-link share automatically.
- Dropbox root listing (nonrecursive) displayed no file with the target filename. This is not a write test.
- The GitHub connector cannot create/update Action environment secrets; user must configure these in GitHub directly.
- Previous 7G staged native private workflow is source-only and fail-closed. Its HTTPS ingress currently expects a **plaintext 7F ZIP** after download and SHA validation. It **cannot directly consume a client-encrypted .bin** without a new decryption adapter and additional separately held key.
- The current chat environment cannot deliver an encryption key to the owner through an independent verified secret channel without putting it in chat/attachments. Creating a fresh key and keeping it only in an ephemeral assistant sandbox risks permanent data loss after reset.

## Result / stop
**NO FILE UPLOADED TO DROPBOX. NO NEW ZIP ENCRYPTED. NO FILE/SHARED LINK CREATED. NO GITHUB SECRETS CONFIGURED. NO WORKFLOW DISPATCHED. NO NATIVE PRIVATE RENDER.**
Exact blockers:
1. Need an owner-controlled way to generate and retain the input-decryption key off chat (e.g., a trusted iPhone encryption app, or a secure local browser-only client with verifiable code), then produce ciphertext with a conversation fileParam the Dropbox connector can receive.
2. Need a decryption adapter on the protected GitHub runner to support input ciphertext, distinct from 7G's encrypted *output* envelope.
3. Need owner action to set protected environment secrets; a one-use Dropbox URL expiring in 60–900 seconds is operationally brittle with human-reviewed GitHub workflows. A longer-lived authenticated Dropbox API credential would require additional scopes/secret provisioning, not available via this connector.
4. Need explicit user approval for any merge to default branch and any workflow dispatch.

## Smallest safe next deliverable
Build an auditable **browser-only input encryption/decryption tool and runner adapter** with synthetic test vector, no private artwork, and a clear iPhone key-retention mechanism. Owner uses that locally to encrypt the 7F ZIP and saves the recovery key in their own password manager. Only after validating ciphertext and owner key custody should the assistant attempt `upload_file` to exactly `/NoPants_Sprint7H_ENCRYPTED_INPUT.bin`. Use Dropbox short-lived single-use link only when ready to launch, and treat URL as secret. If fileParam routing is unavailable, report rather than bypassing.

## Notes
- Authenticated encryption protects stored bytes but not the decrypted artwork while it is being rendered on GitHub's ephemeral worker.
- No paid spend or new engine tournament. Prior native synthetic Stretchy proof remains at Actions run 42269637429; prior security contract run 42314859236.
