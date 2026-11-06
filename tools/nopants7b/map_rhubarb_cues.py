#!/usr/bin/env python3
"""Map Rhubarb JSON mouth cues to frame-indexed 2D character rig instructions.

No artwork is loaded or published. Works with standard Rhubarb v1 JSON.
"""
import argparse
import json
from pathlib import Path

SHAPE_MAP = {
    "X": "mouth_rest",
    "A": "mouth_rest",
    "B": "mouth_small",
    "C": "mouth_medium",
    "D": "mouth_wide",
    "E": "mouth_rounded",
    "F": "mouth_rounded",
    "G": "mouth_medium",
    "H": "mouth_medium",
}

def map_cues(data, fps=24, duration=5.0):
    if fps <= 0 or duration <= 0:
        raise ValueError("positive fps and duration required")
    cues = data.get("mouthCues")
    if not isinstance(cues, list) or not cues:
        raise ValueError("Rhubarb mouthCues must be a nonempty list")
    total = round(duration * fps)
    frames = []
    previous_end = -1.0
    for cue in cues:
        start, end = float(cue["start"]), float(cue["end"])
        value = str(cue["value"])
        if end < start or start < previous_end - 1e-6:
            raise ValueError("nonmonotonic or invalid mouth cues")
        if value not in SHAPE_MAP:
            raise ValueError(f"unsupported Rhubarb shape {value!r}")
        previous_end = end
    for frame in range(total):
        t = frame / fps
        active = next((cue["value"] for cue in cues if float(cue["start"]) <= t < float(cue["end"])), "X")
        frames.append({"frame": frame, "time": round(t, 6), "rhubarb": active,
                       "asset": SHAPE_MAP[active] + ".png"})
    return {"fps": fps, "duration": duration, "frame_count": total, "frames": frames}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cues", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--duration", type=float, default=5.0)
    args = parser.parse_args()
    result = map_cues(json.loads(args.cues.read_text()), args.fps, args.duration)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2))
    print(f"Mapped {result['frame_count']} mouth frames")

if __name__ == "__main__":
    main()
