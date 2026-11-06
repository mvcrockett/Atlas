# Stretchy Studio Headless Benchmark

Bounded Operation No Pants Sprint 2 experiment.

This benchmark does **not** claim production anime quality. It tests whether Stretchy Studio's actual browser renderer and animation engine can be automated unattended in GitHub Actions.

It reuses upstream Stretchy Studio at pinned commit `24a83a27ba43e43e9d2e3de5e33994594e6199c2` and directly imports:

- `src/renderer/scenePass.js`
- `src/renderer/animationEngine.js`
- their renderer dependencies

The synthetic fixture exercises:
- transform keyframes
- blink
- smile
- breathing/head motion
- direct mesh-vertex interpolation for a bending elbow
- WebGL2 frame rendering
- Playwright headless Chromium capture
- FFmpeg assembly to 48-frame / 24fps / 2-second MP4

Farnebäck remains untouched as the existing control in `continuous_engine`.
