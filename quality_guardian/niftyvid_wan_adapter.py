"""Wan 2.2 Gradio API contract adapter. DRY RUN ONLY by default.
Source: https://github.com/IgorCSIS/nifty-vid/blob/main/worker/src/index.ts
No network requests, paid services, or GPU jobs are made by this module.
"""
import json

SPACE = "https://cbensimon-wan2-2-fp8da-aoti-preview2.hf.space"
PROMPT = ("Professional 2D Japanese anime. Auburn-haired green-eyed woman in lavender "
          "blinks once, then smiles subtly. Static medium shot, preserve identity. "
          "No zoom, no cuts, no morphing.")
NEGATIVE = ("色调艳丽, 过曝, 静态, 细节模糊不清, 字幕, 风格, 作品, 画作, 画面, 静止, "
            "整体发灰, 最差质量, 低质量, JPEG压缩残留, 丑陋的, 残缺的, 多余的手指, "
            "画得不好的手部, 画得不好的脸部, 畸形的, 毁容的, 形态畸形的肢体, "
            "手指融合, 静止不动的画面, 杂乱的背景, 三条腿, 背景人很多, 倒着走")

def make_payload(uploaded_path, filename="heroine.png", prompt=PROMPT, duration=3.5, steps=6):
    """Contract from upstream NiftyVid; requires upload to Gradio first."""
    if not 0.5 <= duration <= 4.5 or not 1 <= steps <= 12:
        raise ValueError("Outside public free Space limits")
    filedata = {
        "path": uploaded_path,
        "url": SPACE + "/gradio_api/file=" + uploaded_path,
        "orig_name": filename, "size": None, "mime_type": None,
        "meta": {"_type": "gradio.FileData"}
    }
    return {"data": [filedata, None, prompt, steps, NEGATIVE, duration,
                     1, 1, 42, True, 6, "UniPCMultistep", 3.0, 16, False, True]}

def parse_complete_sse(lines):
    """Extract HTTPS MP4 URL from a Gradio completion event; no download."""
    event = None
    data = []
    for raw in lines:
        line = raw.decode("utf-8").rstrip("\r\n") if isinstance(raw, bytes) else raw.rstrip("\r\n")
        if not line:
            if event == "complete":
                value = json.loads("\n".join(data))
                video = value[0] if isinstance(value, list) and value else None
                url = video.get("url") if isinstance(video, dict) else None
                if isinstance(url, str) and url.startswith("https://"):
                    return url
                raise ValueError("No HTTPS video URL")
            if event == "error":
                raise RuntimeError("Upstream error: " + "\n".join(data)[:500])
            event, data = None, []
        elif line.startswith("event:"):
            event = line[6:].strip()
        elif line.startswith("data:"):
            data.append(line[5:].strip())
    raise RuntimeError("No completion event")

if __name__ == "__main__":
    print(json.dumps({"mode": "DRY_RUN_NO_NETWORK", "upload_endpoint": SPACE + "/gradio_api/upload",
        "submit_endpoint": SPACE + "/gradio_api/call/generate_video",
        "payload": make_payload("/tmp/gradio/example.png"),
        "gpu_job_submitted": False, "mp4_generated": False}, ensure_ascii=False, indent=2))
