# Operation No Pants Animation Studio 🎬

Free, open-source, cloud-rendered GIF and MP4 animation using Python, Pillow, FFmpeg, and GitHub Actions. No paid AI services.

## Phase 1 — preserved
`animate.py` still produces the original 4-second fish animation at `output/fish.gif` and `output/fish.mp4`. Its source is unchanged.

## Phase 2 — reusable scene engine
Edit `scenes.json` to define scenes. Run `python studio.py --config scenes.json` to export a GIF and MP4 per scene to `output/<scene-name>/`.

Scene properties:
- `name`: unique letters, numbers, underscores or hyphens
- `character`: `fish`, `ball`, `star`
- `background`: `ocean`, `sky`, `night`
- `motion`: `swim`, `bounce`, `orbit`, `still`
- `duration`: seconds from 0.5 to 15
- `fps`: 1 to 30
- `size`: optional `[640, 360]` (maximum 1920 × 1080)

The default scenes demonstrate three combinations. The pipeline renders the legacy fish first, then all configured scenes. GitHub Actions uploads an artifact named `no-pants-studio-animations`.

## Run on GitHub from iPhone
Open **Actions → Render free animation → Run workflow**. After the job completes, open the run and download the artifact ZIP.

## Run locally (optional)
Install Python 3, FFmpeg, and `pip install -r requirements.txt`. Then run `python animate.py` and `python studio.py`.

All graphics are drawn procedurally. This is a simple reusable 2D engine, not generative AI video or a character-rigging editor.
