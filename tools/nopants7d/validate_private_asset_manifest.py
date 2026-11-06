#!/usr/bin/env python3
"""Private artwork manifest preflight; NO image uploads, network access, or logging assets."""
import argparse
import hashlib
import json
from pathlib import Path

REQUIRED = {
    "canonical_original_crop.png", "mouth_original.png", "eyes_original.png",
    "eyelids_closed_provisional.png", "mouth_rest.png", "mouth_small.png",
    "mouth_medium.png", "mouth_wide.png", "mouth_rounded.png"
}
def validate(data, asset_dir):
    if data.get("asset_classification") != "PRIVATE_DO_NOT_PUBLISH":
        raise ValueError("private classification missing")
    if data.get("native_rig_status") == "VERIFIED":
        raise ValueError("do not claim native proof from preparation manifest")
    bbox=data.get("cropping",{}).get("source_bbox")
    size=data.get("cropping",{}).get("output_size")
    if not isinstance(bbox,list) or len(bbox)!=4 or not isinstance(size,list) or len(size)!=2:
        raise ValueError("invalid source crop geometry")
    if any(not isinstance(n,int) for n in bbox+size) or size[0]<1 or size[1]<1:
        raise ValueError("non-integer or nonpositive geometry")
    layers=data.get("layer_status",{})
    if not REQUIRED.issubset(layers):
        raise ValueError("required provisional layer names missing")
    if asset_dir:
        missing=sorted(n for n in REQUIRED if not (asset_dir/n).is_file())
        if missing:raise FileNotFoundError("required private art missing (names only): "+", ".join(missing))
    for k in ("source_portrait_sha256","reference_sheet_sha256"):
        v=data.get(k,"")
        if len(v)!=64 or any(c not in '0123456789abcdef' for c in v):
            raise ValueError("missing or invalid sha256")
    return len(REQUIRED)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("manifest",type=Path)
    p.add_argument("--asset-dir",type=Path)
    a=p.parse_args()
    n=validate(json.loads(a.manifest.read_text()),a.asset_dir)
    print(f"PASS: private manifest geometry and {n} provisional layer slots validated; no image bytes sent anywhere.")

if __name__=="__main__":main()
