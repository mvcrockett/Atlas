"""Phase 5: optional, licensed WAV audio mixed into an existing silent MP4.

No external services. Only local user-provided audio; no assumed music licenses.
"""
import argparse
import json
import math
import shutil
import subprocess
import wave
from pathlib import Path


def demo_tone(path, seconds=0.35, rate=24000):
    """Original synthesized test tone, NOT a generated voice or licensed music."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        frames = bytearray()
        for i in range(round(seconds * rate)):
            envelope = min(1.0, i / (rate * .02), (seconds * rate - i) / (rate * .05))
            sample = int(5500 * max(0.0, envelope) * math.sin(2 * math.pi * 440 * i / rate))
            frames.extend(sample.to_bytes(2, "little", signed=True))
        wav.writeframes(frames)
    return path


def mux(config):
    source = Path(config["video"])
    destination = Path(config["output"])
    if not source.is_file() or source.suffix.lower() != ".mp4":
        raise ValueError("Existing silent MP4 required")
    if source.resolve() == destination.resolve():
        raise ValueError("Output must not overwrite source video")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("FFmpeg and FFprobe must be on PATH")
    probe = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
                            str(source)], capture_output=True, text=True, check=True)
    duration = float(probe.stdout.strip())
    if duration <= 0:
        raise ValueError("Invalid video duration")
    tracks = config.get("tracks", [])
    if not tracks:
        raise ValueError("Supply at least one WAV track")
    if len(tracks) > 12:
        raise ValueError("At most 12 WAV tracks")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(source)]
    filters = []
    for index, track in enumerate(tracks):
        path = Path(track["path"])
        if path.suffix.lower() != ".wav" or not path.is_file():
            raise ValueError(f"Missing WAV: {path}")
        with wave.open(str(path), "rb") as wav:
            if wav.getcomptype() != "NONE":
                raise ValueError("WAV must be uncompressed PCM")
        offset = float(track.get("start", 0))
        volume = float(track.get("volume", 1))
        if not (0 <= offset < duration and 0 <= volume <= 2):
            raise ValueError("Track start or volume outside permitted range")
        cmd += ["-i", str(path)]
        milliseconds = round(offset * 1000)
        filters.append(f"[{index+1}:a]aresample=48000,aformat=channel_layouts=stereo,"
                       f"volume={volume},adelay={milliseconds}|{milliseconds}[a{index}]")
    inputs = "".join(f"[a{i}]" for i in range(len(tracks)))
    filters.append(f"{inputs}amix=inputs={len(tracks)}:duration=longest:normalize=0,"
                   f"apad,atrim=duration={duration:.6f},asetpts=N/SR/TB[mix]")
    destination.parent.mkdir(parents=True, exist_ok=True)
    cmd += ["-filter_complex", ";".join(filters), "-map", "0:v:0", "-map", "[mix]",
            "-c:v", "libx264", "-profile:v", "baseline", "-level", "3.1",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            "-ar", "48000", "-movflags", "+faststart", "-t", f"{duration:.6f}",
            str(destination)]
    subprocess.run(cmd, check=True)
    print(f"Phase 5 audio: {destination} ({len(tracks)} track(s), {duration:.2f}s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="audio.json")
    parser.add_argument("--make-demo-tone", metavar="WAV")
    args = parser.parse_args()
    if args.make_demo_tone:
        demo_tone(args.make_demo_tone)
    else:
        mux(json.loads(Path(args.config).read_text()))
