# No Pants Studio — GitHub Pages publication decision packet (NOT DEPLOYED)

Prepared: November 6, 2026 (America/Chicago). **Owner approval required for every publishing step.**

## Verified GitHub repository state
- Public repo: `mvcrockett/Atlas`. GitHub REST repository metadata reported `default_branch=main`, `private=false`, **`has_pages=false`**, `homepage=null`.
- `main` remained `8e4e21b556c62b9d28b93e9c4471b02b246950b1`.
- Experimental source branch `no-pants-encryption-portal-predeploy` at prior tested source commit `57c0bb03dfcf7490af1b9e198cac7b3ad3573fd7`.
- Last real browser screenshot test GitHub Actions run `42329463396`: SUCCESS. Tested mobile-size Chromium (390×844) and a synthetic fixture; encryption/digest/wrong-password tests passed; no external/non-GET requests; **NOT Safari or private heroine tested**.
- Main recursive tree (53 entries) contained **no Pages deployment workflow, root index.html or CNAME**.
- GitHub Pages settings REST endpoint and deployment listing endpoint were *not exposed by the active GitHub connector*, so cannot inspect the owner account's exact Pages source, custom domain, access controls or complete deployment history. Repo `has_pages=false` corroborates no enabled Pages site. An attempted public Pages URL could not be independently opened, so no live site claimed.

## Critical folder selection trap
GitHub Pages' branch source supports ONLY the branch root `/` or top-level `/docs`. It CANNOT directly select `/docs/nopants/encryption-portal`. Choosing `/docs` in the existing source branch would publish a much larger documentation tree. Choosing `/` would publish repository files. Either violates the user's explicit intention to publish only three audited static files.

## Recommended exact deployment: GitHub Actions artifact, separate owner approval
1. Leave experimental source branch unchanged for the approved audit; pin source SHA to `57c0bb03dfcf7490af1b9e198cac7b3ad3573fd7`. Do not include test harness, report, original image or any GitHub workflows in the public site artifact.
2. After explicit separate owner approval, add one **manual-only** Pages deployment workflow `.github/workflows/nopants-portal-pages.yml` on `main`. Its exact proposed content is recorded *only as non-executable documentation* in `docs/nopants/encryption-portal-audit/PROPOSED_PAGES_DEPLOY.yml.example`. It checks out the pinned source SHA, copies ONLY `index.html`, `portal.css`, `portal.js` plus `.nojekyll` into isolated artifact staging, and uses configure/upload/deploy Pages actions. Permissions limited to contents read, pages write, id-token write. Never automatically trigger on pushes.
3. Owner uses repo Settings → Pages → Build and deployment → Source → **GitHub Actions**, not “Deploy from branch”. A repository administrator/maintainer must configure this. Any `github-pages` environment protection rules should be reviewed. Never claim existing Pages configuration changed.
4. Owner manually triggers the reviewed workflow from Actions on `main`, and confirms artifact file list and green deployment.
5. Expected site URL only AFTER successful Pages build: **`https://mvcrockett.github.io/Atlas/`**. This is a derived standard GitHub Pages project URL, NOT a currently live or verified URL. No custom domain confirmed. If the URL redirects, use the actual address verified by GitHub Pages Settings → Visit site.
6. Before using heroine art, user opens *live HTTPS page* in iPhone Safari and performs a harmless local test (see below). The web-host provider controls served code and can technically alter it; owner should check the deployed source is the audited pinned version and secure HTTPS.
7. Owner separately authorizes actual private-art encryption, and later encrypted-only Dropbox upload and GitHub protected runner. Do not bundle these authorizations with publication.

## Source-only privacy contract
- Portal CSP `default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'none'; form-action 'none'; object-src 'none'`; uses relative same-origin files and no upload or analytics code.
- Real Chromium test validates no external requests and no non-GET requests for its synthetic fixture. This is useful evidence, not a universal guarantee against malicious future script or compromised GitHub Pages host.
- Web Crypto AES-256-GCM, PBKDF2-SHA256 600,000 iterations, cryptographic salts/nonces. Expected exact source ZIP SHA256. Key stays user-controlled; password must be saved securely BEFORE input.
- Meta CSP `frame-ancestors` is ignored by browsers; this is not framed-clickjacking defense. Static app contains no external forms and no network posting.
- Original heroine, passphrase, generated ciphertext and private video DO NOT belong in GitHub repository history, Pages artifacts, browser telemetry or logs.

## iPhone Safari verification after separate authorized deployment
1. On iPhone, in **Safari**, visit deployed HTTPS URL from repo Pages settings. Check padlock/HTTPS and exact expected path; do not use an unrelated mirror.
2. Confirm the colored page and purple title load, file selector and password fields work, button is enabled, and no Web Crypto unavailable warning appears.
3. Before touching heroine ZIP, choose a **small harmless throwaway ZIP** and see whether SHA-256 identity mismatch is displayed without download—this is the expected safe behavior, NOT full successful encryption.
4. To validate full encryption with a harmless file, the reviewer must serve a *test-only version* of the page with a SHA256 appropriate for a harmless fixture through a separate audited environment (as CI does), not modify the live production source or use a real password in demo. Actual full save path on physical iPhone remains unverified.
5. In a separate, deliberately owner-authorized step, save a unique 24+ character password in Apple Passwords, pick exact original private 7F ZIP from Files, encrypt on Safari webpage, save the `NoPants_Sprint7H_ENCRYPTED_INPUT.bin` to Files and verify downloaded size (1,949,840 bytes for the exact source ZIP). Do not share the password.
6. If iOS file picker fails, browser content reloads due to memory or download does not save, stop and report exact symptom; do not switch to random online encryption sites.
7. Only AFTER owner confirms success, attach ciphertext only in chat to allow approved Dropbox destination `/NoPants_Sprint7H_ENCRYPTED_INPUT.bin`. The attached file can be checked for envelope header/size, not decrypted without owner-held secret.

## No-op statement
The publication plan itself makes no Pages configuration change, no main merge, no workflow dispatch, no private art upload, no password handling, no native heroine render, no cash spend.

## Official docs
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
