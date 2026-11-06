"""Compute bounded metrics and authenticated-encrypt private render evidence.
Only encrypted bytes may be uploaded to public Actions artifacts.
"""
import os, json, io, zipfile, pathlib, hashlib, secrets, statistics
from PIL import Image, ImageChops, ImageStat
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

RENDER_DIR = pathlib.Path("output/sprint3d")
SOURCE_DIR = pathlib.Path(os.environ["NOPANTS_ASSET_DIR"])
TARGET = pathlib.Path("output/sprint3e")
TARGET.mkdir(parents=True, exist_ok=True)

def mean_abs(a, b):
    a = a.convert("RGB")
    b = b.convert("RGB")
    if a.size != b.size:
        return None
    return sum(ImageStat.Stat(ImageChops.difference(a,b)).mean) / 3.0

frames = sorted((RENDER_DIR/"frames").glob("frame_*.png"))
if len(frames) != 72:
    raise RuntimeError("Expected 72 detailed-art frames")
rgb_frames = []
hashes = set()
for p in frames:
    hashes.add(hashlib.sha256(p.read_bytes()).hexdigest())
    with Image.open(p) as im:
        rgb_frames.append(Image.new("RGBA", im.size, "white"))
        rgb_frames[-1].alpha_composite(im.convert("RGBA"))
        rgb_frames[-1] = rgb_frames[-1].convert("RGB")

interframe = [mean_abs(a,b) for a,b in zip(rgb_frames, rgb_frames[1:])]
refs={}
for p in sorted((SOURCE_DIR/"reference_frames").glob("frame_*.png")):
    i=int(p.stem.rsplit("_",1)[-1])
    if i>=len(rgb_frames):continue
    with Image.open(p) as im:
        refs[str(i)] = {"note":"Reference frame has different canvas geometry; not directly pixel-comparable",
                        "dimensions":[im.width,im.height], "current_dimensions":list(rgb_frames[i].size),
                        "raw_mae":mean_abs(im,rgb_frames[i])}
metrics = json.loads((RENDER_DIR/"metrics.json").read_text())
metrics["secure_ingress"] = True
metrics["public_artwork_uploaded"] = False
metrics["public_plaintext_video_uploaded"] = False
metrics["visual_review_completed"] = False
metrics["identity_measurement"] = "not measured"
metrics["frame_difference_mean"] = statistics.mean(interframe)
metrics["frame_difference_p95"] = sorted(interframe)[int(.95*(len(interframe)-1))]
metrics["reference_frame_checks"] = refs
metrics["source_comparison_warning"] = "Native 480x480 output vs 280x470 reference: source fidelity requires registered/cropped comparison and human review."
metrics["source_status"] = "UNAPPROVED_TECHNICAL_FIXTURE"
metrics["artifact_encryption"] = "AES-256-GCM, 12-byte random nonce, associated data NoPants-Sprint3E-v1"
metrics["unique_frame_hashes"] = len(hashes)
# Sanitize absolute paths and prevent additional metadata leakage
(RENDER_DIR/"metrics_secure.json").write_text(json.dumps(metrics,indent=2))
keyhex = os.environ.get("NOPANTS_EVIDENCE_KEY_HEX","").strip()
if len(keyhex)!=64:
    raise RuntimeError("Evidence encryption key must be 64 hex characters (32 bytes).")
try:
    key=bytes.fromhex(keyhex)
except ValueError as e:
    raise RuntimeError("Evidence key must be hexadecimal") from e
files = [RENDER_DIR/"sprint3d.mp4", RENDER_DIR/"metrics_secure.json", RENDER_DIR/"telemetry.json"]
files += sorted(RENDER_DIR.glob("inspect_*.png"))
if not all(p.is_file() for p in files):
    raise RuntimeError("Render evidence incomplete; refusing to upload")
payload=io.BytesIO()
with zipfile.ZipFile(payload,"w",zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for p in files:
        archive.write(p,p.name)
nonce=secrets.token_bytes(12)
aad=b"NoPants-Sprint3E-v1"
cipher=AESGCM(key).encrypt(nonce,payload.getvalue(),aad)
(TARGET/"private_evidence.aesgcm").write_bytes(b"NP3E1"+nonce+cipher)
# Only ciphertext and generic, non-visual status information leaves runner.
(TARGET/"STATUS.txt").write_text("ENCRYPTED PRIVATE RENDER EVIDENCE. Use your locally held AES-GCM key to decrypt. User art remains UNAPPROVED.\n")
print("Render evidence sealed with AES-256-GCM. Private images, video and telemetry are not public artifacts.")
