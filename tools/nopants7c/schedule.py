#!/usr/bin/env python3
"""Asset-free and deterministic Rhubarb frame schedule validator for No Pants Studio.
Pure standard library; public repository safe. NO private character imagery.
"""
import argparse
import json
from pathlib import Path

SHAPES = {"X": "rest", "A": "rest", "B": "small", "C": "medium", "D": "wide",
          "E": "rounded", "F": "rounded", "G": "medium", "H": "medium"}

def schedule(data, fps=24, duration=5):
    cues = data.get("mouthCues")
    if not cues or fps <= 0 or duration <= 0:
        raise ValueError("Missing cues or nonpositive fps/duration")
    last = 0.0
    for cue in cues:
        start, end, value = float(cue["start"]), float(cue["end"]), cue["value"]
        if start < last - 1e-7 or end < start or value not in SHAPES:
            raise ValueError("Invalid or unsorted Rhubarb cues")
        last = end
    frames = []
    for index in range(round(fps * duration)):
        t = index / fps
        active = next((c["value"] for c in cues if c["start"] <= t < c["end"]), "X")
        frames.append({"frame": index, "time": round(t, 6), "cue": active,
                       "mouth_asset": "mouth_" + SHAPES[active] + ".png"})
    return frames

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input", type=Path)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--fps", type=int, default=24)
    p.add_argument("--duration", type=float, default=5)
    a = p.parse_args()
    output = {"fps": a.fps, "frame_count": round(a.fps*a.duration),
              "frames": schedule(json.loads(a.input.read_text()), a.fps, a.duration)}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(output, indent=2))
    print(f"PASS: {len(output['frames'])} ordered frames. No art accessed.")

if __name__ == "__main__":
    main()
