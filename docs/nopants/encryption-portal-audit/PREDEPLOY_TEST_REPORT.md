# No Pants Studio — Mobile Encryption Portal: PREDEPLOY Evidence

Date: 2026-11-06
Status: **WORKING CHROMIUM MOBILE BROWSER PROOF, NOT DEPLOYED, SAFARI NOT YET TESTED ON IPHONE**.

## Consent boundary
Victoria approved creating **public source code only** on a new isolated experimental branch, with a future GitHub Pages deployment **only after separate specific approval**. No plaintext/private art, no passwords, no merge to main, no GitHub Pages publication.

## Source
- `docs/nopants/encryption-portal/index.html`: HTML5 responsive form and restrictive Content Security Policy.
- `docs/nopants/encryption-portal/portal.css`: mobile-first visual accessibility and keyboard/focus contrast.
- `docs/nopants/encryption-portal/portal.js`: all encryption local in secure WebCrypto context, strict original Sprint 7F ZIP SHA256 match, 24+-character password, PBKDF2-HMAC-SHA256/600000 iterations, random 16-byte salt and 12-byte IV, AES-256-GCM ciphertext and tag, `NPS7I1` envelope and owner-download `NoPants_Sprint7H_ENCRYPTED_INPUT.bin`.
- `docs/nopants/encryption-portal/test-portal.cjs`: Chromium Playwright synthetic fixture, in-memory substitution of SHA256 expected hash ONLY in test route, 390×844 mobile viewport, live plaintext-to-ciphertext output download, Node crypto decryption & wrong-passphrase rejection, network request audit.
- `.github/workflows/no-pants-encryption-portal-tests.yml`: Actions test. **NO deploy step**, and no art/secrets.

## Verified GitHub Actions evidence
- First Actions attempt `42329314501`: configuration failed before job launch, due to YAML step-name quoting. Fixed.
- Second Actions attempt `42329349107`: **SUCCESS**, tested **actual browser page** in Chromium secure localhost context. Emitted metrics:
  `{"result":"PASS","test_art":"synthetic_only","viewport":"390x844","secure_context":true,"encrypted_file_bytes":107,"cipher_format":"NPS7I1","aes_gcm":true,"wrong_password_rejected":true,"external_requests":0,"non_get_requests":0,"private_heroine_used":false,"actual_iphone_safari_verified":false}`.
- Latest preview screenshot run `42329463396`: **SUCCESS**. Artifact `nopants-encryption-portal-preview` (public-safe screenshot of unfilled form), no artwork inside.

## Privacy and limitations
- Code has no fetch, XMLHttpRequest, WebSocket, sendBeacon, analytics, external script/style or file-upload requests. CSP disallows connect requests and forms. Unit and browser tests check this but future hosting compromise or source changes are distinct threats.
- Browser source zip stays on owner device; password entered only locally into WebCrypto. User must retain password independently in trusted password manager. Browser's JavaScript memory cannot guarantee hardware-grade secret zeroization.
- Web Crypto is available in secure contexts, such as HTTPS and localhost. This confirms behavior in **Chromium/localhost only**; actual Safari iPhone file-picking, memory, download behavior and keyboard need device verification after owner-approved live hosting.
- GitHub Pages is not zero-knowledge hosting: provider controls served public JS; owner should confirm deployed source before uploading any ZIP.
- The exact original 7F source SHA256 is a content hash and does not reveal private pixels, but publishing it allows offline comparisons to independently obtained input bytes. It is acceptable for this public-only work by prior design.
- The browser preview is a SCREENSHOT, not a clickable live portal. A live URL would require a separately approved GitHub Pages deployment; **do not invent one**.
- This is client-side input encryption only. The staged protected GitHub runner still requires owner-controlled secrets and separate user approval before merge or native rendering. **No private heroine render, upload or key-sharing happened**.

## Next owner approval
Request exact approval for deploying these audited public-only files via GitHub Pages, with intended branch/path and published URL reviewed before use. If approved, check safe Pages configuration and publish without touching artwork. Open resulting HTTPS page in iPhone Safari and test with harmless synthetic fixture first. Only then use the original ZIP locally and store password independently; never send plaintext to web.
