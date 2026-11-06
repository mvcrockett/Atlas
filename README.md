# Operation No Pants Animation Studio 🎬

A free, open-source 2D animation pipeline using Python, Pillow, FFmpeg, and GitHub Actions. No paid APIs.

## Phase 1 — original fish (preserved)
`python animate.py` generates `output/fish.gif` and `output/fish.mp4`. Its original source remains untouched.

## Phase 2 — configuration-driven scenes (preserved)
`python studio.py --config scenes.json` generates fish, ball, and star animations with configurable backgrounds, movement, duration, size, and frame rate. Its source and scenes remain untouched.

## Phase 3 — layered characters and multi-shot storyboards
`python characters.py --config storyboard.json` creates GIF/MP4 short stories from a JSON storyboard. Characters use separately composed background, limbs, body, head/hair, face and caption layers. Supported actor `color`: lavender, coral, mint; `pose`: wave, idle, jump; `expression`: happy, surprised, sleepy. Supported backgrounds: studio, garden, stage.

Each story contains ordered `shots`, with independent `duration` (0.5–10 seconds), `background`, `actor` and optional `caption` (up to 90 characters, must fit frame). Story `fps` 1–24, `size` 320×240 through 1280×720, up to 12 shots. The included `hello_lavender` example demonstrates three sequential shots and expressions.

Run locally after installing Python, FFmpeg and `pip install -r requirements.txt`. On GitHub, open **Actions → Render free animation → Run workflow**. The workflow renders all three phases and uploads one ZIP artifact.

## Scope and limitations
These are simple procedurally drawn cartoon characters, not generative AI, imported sprite rigs, lip-sync, sound, or a graphical editor. The JSON file is the scene editor. For now, captions are single-line, and animated GIF timing may vary slightly from MP4 due to centisecond timing.

## Roadmap — future work (not implemented yet)
- **Phase 4:** richer layered sprite/character assets, pose transitions, caption wrapping, and scene editing.
- **Phase 5: open-source audio integration:** optional locally generated character voices (evaluate Piper TTS voice/model licenses and runtime requirements), user-recorded dialogue, original or appropriately licensed music and sound effects, and FFmpeg mixing with timeline synchronization, volume balancing, and MP4 audio muxing.
- Preserve silent GIF exports (GIF does not support audio). MP4 will carry synchronized sound once Phase 5 is implemented.
- No paid services, no assumed commercial-use rights, and no heavyweight speech model installation until benchmarked.
