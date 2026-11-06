"""Private asset ingress. Never print URLs, secrets or decoded artwork into CI logs."""
import os
import pathlib
import hashlib
import json
import urllib.request
import urllib.parse
import zipfile
import io

MAX_DOWNLOAD = 40 * 1024 * 1024
MAX_UNCOMPRESSED = 100 * 1024 * 1024
REQUIRED = ["manifest.json", "reference_source.png"]

def validate_and_extract(raw, destination, expected_sha):
    digest = hashlib.sha256(raw).hexdigest()
    if len(expected_sha) != 64 or not hashlib.compare_digest(digest, expected_sha.lower()):
        raise ValueError("Bundle SHA256 mismatch")
    dst = pathlib.Path(destination)
    dst.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names = z.namelist()
        if len(names) > 150:
            raise ValueError("Too many bundle members")
        if len(names) != len(set(names)):
            raise ValueError("Duplicate filenames")
        total = 0
        for info in z.infolist():
            name = info.filename
            p = pathlib.PurePosixPath(name)
            if p.is_absolute() or ".." in p.parts or "\\" in name or name.startswith("."):
                raise ValueError("Unsafe asset path")
            if not (name.endswith(".png") or name.endswith(".json") or name.endswith("/")):
                raise ValueError("Unexpected file format")
            total += info.file_size
        if total > MAX_UNCOMPRESSED:
            raise ValueError("Uncompressed bundle too large")
        for req in REQUIRED:
            if req not in names:
                raise ValueError("Missing required bundle content")
        z.extractall(dst)
    manifest = json.loads((dst / "manifest.json").read_text())
    if manifest.get("status") != "UNAPPROVED_TECHNICAL_FIXTURE" or manifest.get("approval") is not False:
        raise ValueError("Fixture approval status does not match unapproved test")
    layers = manifest.get("layers") or []
    if not (2 <= len(layers) <= 60):
        raise ValueError("Unexpected layer count")
    from PIL import Image
    w, h = manifest["canvas"]["width"], manifest["canvas"]["height"]
    if not (100 <= w <= 4096 and 100 <= h <= 4096):
        raise ValueError("Unsupported canvas size")
    for layer in layers:
        p = pathlib.PurePosixPath(layer["path"])
        if p.is_absolute() or ".." in p.parts or not p.as_posix().endswith(".png"):
            raise ValueError("Invalid layer path")
        full = dst / p
        if not full.is_file():
            raise ValueError("Missing layer PNG")
        with Image.open(full) as im:
            if im.size != (w, h):
                raise ValueError("Layer dimensions mismatch")
            im.verify()
    print("Private art bundle validated: size, hash, file paths, layers and approval label.")

def main():
    url = os.environ.get("NOPANTS_ART_BUNDLE_URL", "").strip()
    expected = os.environ.get("NOPANTS_ART_BUNDLE_SHA256", "").strip()
    if not url or not expected or not os.environ.get("NOPANTS_EVIDENCE_KEY_HEX"):
        raise RuntimeError("Secure input secrets missing; no art was fetched.")
    if urllib.parse.urlparse(url).scheme != "https":
        raise RuntimeError("Asset URL must use HTTPS.")
    req = urllib.request.Request(url, headers={"User-Agent":"NoPants-Private-Asset-Runner/1.0"})
    with urllib.request.urlopen(req, timeout=55) as resp:
        if urllib.parse.urlparse(resp.geturl()).scheme != "https":
            raise RuntimeError("Asset redirect was not HTTPS.")
        data = resp.read(MAX_DOWNLOAD + 1)
    if len(data) > MAX_DOWNLOAD:
        raise RuntimeError("Asset bundle exceeds transfer limit")
    validate_and_extract(data, os.environ["NOPANTS_ASSET_DIR"], expected)

if __name__ == "__main__":
    main()
