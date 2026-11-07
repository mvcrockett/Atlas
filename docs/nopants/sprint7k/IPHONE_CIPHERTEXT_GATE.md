# Sprint 7K — Owner ciphertext prerequisite and iPhone test gate
Date: 2026-11-06

## Current verified state
- `main` at `8e4e21b556c62b9d28b93e9c4471b02b246950b1`, unchanged.
- `no-pants-sprint7j-encrypted-owner-handoff` at `e4dd1f86d99f03cfb8f3cbbafbd00c29470f911b`, unchanged.
- Sprint 7I Actions synthetic encryption/decryption test https://github.com/mvcrockett/Atlas/actions/runs/42318811918 SUCCESS.
- Inspected actual mounted local files; `NoPants_Sprint7F_NATIVE_INPUT_PRIVATE.zip` present, size 1,949,790 bytes, 12 members, ZIP CRC check passes, SHA256 `6ebab335357134baefb2c64ae6c01edf0427943703beab2c252300a06f54229b`.
- Inspected `NoPants_7I_Encrypt_Offline.html` (6,998 bytes) locally: runs WebCrypto SHA256 check, derives PBKDF2-SHA256 AES-256-GCM encryption key from owner-entered password, 600,000 iterations, random salt and nonce, downloads a local .bin via Blob/object URL. Page makes no network requests. **This is code inspection, not iPhone Safari validation.**
- Search of mounted files found **no** `NoPants_Sprint7H_ENCRYPTED_INPUT.bin` file and the current user message contains no new encrypted attachment.
- Dropbox destination `/NoPants_Sprint7H_ENCRYPTED_INPUT.bin` was specifically approved for **ciphertext only**. Do not upload any plaintext ZIP or invent a connector fileParam.

## Actual blocker: a real owner-generated ciphertext file
The GitHub runner cannot access Victoria's original private image zip until:
1. Victoria saves a unique, strong recovery password in Apple Passwords before starting.
2. She locally executes the standalone HTML encryptor in a **working secure WebCrypto context** (iPhone Safari's handling of downloaded `file://` HTML is unverified). Select the exact original 7F ZIP. A strict SHA256 check prevents using a different ZIP.
3. She confirms a new file `NoPants_Sprint7H_ENCRYPTED_INPUT.bin` exists in Files. Expected size for exact ZIP + 6-byte magic + 16-byte salt + 12-byte nonce + 16-byte authentication tag is **1,949,840 bytes**.
4. She uploads **only ciphertext** to the ChatGPT conversation. We must retrieve an actual injected source_file reference before attempting a connected Dropbox upload.
If Files preview or Safari cannot execute `crypto.subtle`/Blob download, stop and get her actual error symptoms; a random online HTML editor/encryptor is not an authorized replacement. An authenticated, owner-approved secure-hosted static HTML page *might* be needed, but must be separately authorized and reviewed before deploying.

## GitHub protected deployment handoff
The staged manual workflow `.github/workflows/no-pants-7i-private-staged.yml` is isolated, not merged, not run with private art.
Its `nopants-private` protected environment must be owner configured in GitHub UI, including:
- `NOPANTS_ART_BUNDLE_URL`: temporary single-use HTTPS Dropbox download link to encrypted .bin. Dropbox connector link TTL 60–900 seconds, consumed by first HTTP request (even HEAD); do not generate until a run is imminent.
- `NOPANTS_INPUT_PASSPHRASE`: password entered **by owner in GitHub secret UI only**, never chat.
- `NOPANTS_ART_BUNDLE_SHA256`: plaintext ZIP hash above.
- `NOPANTS_EVIDENCE_KEY_HEX`: separately retained 32-byte random key for AES-256-GCM output evidence. User must retain a secure copy outside GitHub.
Do NOT merge workflow to default branch or dispatch without separate owner consent. GitHub Actions will temporarily hold decrypted art in its trusted ephemeral worker; input/output encryption does not protect it from compromised runner code.

## This sprint's actual changes
Created a new isolated branch `no-pants-sprint7k-owner-ciphertext-gate`. No private art uploaded, no Dropbox mutation, no workflow secret change, no default-branch merge, no native heroine video and no production-quality approval.
**Single next action:** run the offline encryption page on owner's iPhone, attach the produced .bin, or report exact Safari error. Stop adding new engine architecture or synthetic animation tests until this prerequisite changes.
