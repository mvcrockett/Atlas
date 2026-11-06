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

## Phase 4 — reusable characters, expressive poses and wrapped dialogue
Run `python phase4.py --config phase4.json` to render `output/phase4_story/phase4_story.gif` and `.mp4`. Named character profiles in `phase4.json` control outfit color (lavender, coral, mint, blue), hair (dark, brown, gold) and horizontal position. Each shot chooses a character, background (garden, studio, night), pose (idle, wave, jump, walk), expression (happy, surprised, sad, sleepy, neutral), duration, caption, and optional `transition: fade` (otherwise cut). Eased jumping and crossfade transitions improve movement; captions automatically wrap to up to three lines.

The Phase 4 workflow also renders the original fish and every Phase 2–3 example. This is a simple procedural 2D animation engine; it does not yet provide sprite import, audio, a GUI, or lip synchronization. Phase 5 voice/music/sound effects/FFmpeg mixing remains **planned only**.

## Phase 4.1 — GIF timing and caption polish
Phase 4's GIF export now distributes 10-millisecond GIF delay quantization across frames instead of rounding every frame to the same delay. For the default 12 fps, 72 frames total exactly 6.00 seconds. Scene crossfades now blend **caption-free scene frames** and render only the incoming shot's caption afterward, avoiding overlapping dialogue. The Phase 1–3 engines are unchanged. GIF players may still vary in their interpretation of frame delays. Phase 5 audio remains future work.
