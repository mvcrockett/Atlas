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

## Phase 5 — offline audio MVP (WAV to synchronized MP4)
`audio.py` takes an existing silent MP4 and one or more **user-provided, uncompressed PCM WAV** recordings, with per-track start time in seconds and volume, and creates a separate iPhone-friendly H.264/AAC MP4. It never alters the original MP4 or silent GIF. Edit `audio.json` with your own local WAV file paths; **only use music/sound effects you created or have rights to use**. Tracks beyond the video duration are trimmed; gaps are silent. No voice cloning, TTS, paid APIs, or music downloads are part of this MVP.

Usage after rendering Phase 4: `python audio.py --config audio.json`. For CI only, `python audio.py --make-demo-tone assets/audio/demo_tone.wav` creates an original, short 440 Hz test beep, **not a voice performance**. Replace it with a recording to hear real speech. GitHub Actions runs the synthetic test and uploads the audio MP4 alongside the preserved 12 silent exports. FFmpeg is provided by the open-source `imageio-ffmpeg` wheel in the workflow. This is the first step toward the preserved roadmap of user voices, licensed SFX/music, optional vetted open-source TTS, and more advanced timeline mixing.

**Playback note:** The existing Phase 4.1 MP4 was validated as H.264 and converted to a compatible baseline variant; whether the ChatGPT iOS app opens a particular sandbox link still depends on the client. GitHub Actions artifacts provide a second download route.

## Anime-inspired layered visual proof of concept
Run `python anime_layers.py` to generate `output/anime_layers/anime_layers.mp4` and `.gif` using original Pillow-drawn artwork: independent gradient sky/stars, distant illuminated city, illustrated character, foreground drifting petals, blurred glow, cinematic letterboxing and camera parallax. This is a 4-second 640x360 12fps demonstration of **layered compositing and cinematic motion**, not production-quality frame-by-frame anime, lip sync, or imported AI art. It preserves the Phase 1–5 scripts and their outputs. All artwork is created in code, with no paid APIs or outside assets.
