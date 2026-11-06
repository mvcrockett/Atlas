# Sprint 7A — Evidence, Security, Phone Workflow & Quality Gates
**Date**: 2026-11-06
**Status**: recovery documentation only; NO canonical heroine selected; NO new anime performance rendered.
**Isolated branch baseline**: b4927c7180ebeea2963f3f48473c3ce4f55f3643 (6A). Main observed: 8e4e21b556c62b9d28b93e9c4471b02b246950b1.

## Live repository inspection
- Repo: https://github.com/mvcrockett/Atlas (PUBLIC). Any branch added to this repository is also publicly visible.
- Existing separate branches: main, phase2b, Sprint2 Stretchy/Synfig, Sprint3A, Sprint3D, Sprint3E, 4A–4D, 6A, FATLAS performance POC. Do not replace or merge them for this sprint.
- Main branch contains .github/workflows/continuous-anime.yml with workflow_dispatch, plus render and other workflow files; no proof it can render the unapproved heroine.
- Experimental Sprint 3E private ingress: https://github.com/mvcrockett/Atlas/blob/no-pants-sprint3e-private-art-ingress/benchmarks/art-to-rig/SPRINT3E_PRIVATE_INGRESS.md . Input URL, SHA256, and AES-GCM key are supplied through encrypted repository secrets; raw frames/video not uploaded. It was staged; private heroine video render NOT established.
- Existing 6A evidence: https://github.com/mvcrockett/Atlas/actions/runs/42242553202 original schematic character and Japanese depth-order repair; https://github.com/mvcrockett/Atlas/actions/runs/42243336566 CPU probes successful. These DO NOT confirm production-quality lavender heroine.
- Original heroine reference pixels, separate layer ZIPs and Sprint 3B local package NOT FOUND in inspected GitHub branch trees. A description and historic metrics are not recoverable image files.

## Phone-only production control
- The durable GitHub Actions manual button requires a workflow_dispatch YAML present on the DEFAULT branch. Existing main workflow_dispatch can already be manually launched. Branch-only workflow dispatch may not appear in GitHub UI until a safe dispatch shim is reviewed and merged to main; that merge requires explicit user authorization.
- SAFETY: GitHub Pages sites are public even when published from a private repository. NEVER deploy private art, dialogue recordings, full videos or encrypted secrets to Pages.
- Minimal near-term approach: (1) use existing main Actions tab to run NONPRIVATE calibration jobs and view artifacts; (2) design a private-art review path using encrypted job artifacts with owner-side decryption or an authenticated private host; (3) do not publish a public gallery until owner explicitly approves sanitized showcase media.
- $0 paid API spend; public GitHub Actions usage and retention still subject to platform quotas and current terms.

## Five-second, 24fps talking portrait — proposed GATES (NOT YET TESTED)
Technical reproducibility:
- MP4 duration: 5.00s +/- 1/24s, exactly 120 decoded frames, playback 24 fps, all frames same 768x768 target output size (or explicitly approved alternative).
- No missing frame files, corrupted decode, sequence-order faults, or unexpected alpha-background holes.
- Audio present and readable; audio/video drift <= 80 ms for a short reference clip; deterministic inputs and hashes recorded; no network secret or private art in public logs.
- Each timed mouth cue must map to an authored matching mouth texture; no placeholder mouth-shape drawn over an unsuitable base source without review.

Human visual gates (must all be explicitly approved by Victoria):
- Canonical character design is explicitly approved from the ORIGINAL recovered source.
- Face and hairstyle look like locked source throughout; no significant identity drift or schematic substitute.
- Blink closes and reopens naturally; eyelid layers do not tear or float.
- Mouth moves in plausible correspondence with audible syllables; no detached mouth.
- No distracting seams, holes, alpha halos, broken clothing overlap, hair occlusion inversion or unwanted flicker in playback.
- Acting and style feel like anime, not a procedural/geometric cartoon.
Metrics alone CANNOT automatically pass these gates.

## Rhubarb lip synchronization
Official upstream: https://github.com/DanielSWolf/rhubarb-lip-sync . Project says MIT for core and permissive licenses for dependencies; command-line, available desktop release assets (including Linux) and output timed 2D mouth cues. It may be used to create commercial animation; keep notices if distributing its code. NO binary installed, command executed, audio processed, or validated 5-second lip-sync test in this sprint. Benchmark only after mouth-shape artwork exists.
License reference: https://github.com/DanielSWolf/rhubarb-lip-sync/blob/master/LICENSE.md

## Next sprint candidate (ONLY after owner confirms source status and selects design)
Sprint 7B — Character Art Completion, PRIVATE fixture track. Recover original source bytes, collect explicit design approval, paint/verify closed lids and mouth variants, clean hair/neck seams, perform side-by-side static/short rig inspection. Preserve public/noncanonical calibration track. Do not promise a feature-length film from a talking portrait.
