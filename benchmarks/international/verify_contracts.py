#!/usr/bin/env python3
"""NoPants 4A: zero-art, zero-model-download interface compatibility probe.

Verifies current upstream source contracts. This is NOT an AI inference,
PSD conversion, GPU benchmark, or native anime rendering test.
"""
import hashlib
import json
import pathlib
import re
import sys
import urllib.request

SOURCES = {
 "see_through_cli": "https://raw.githubusercontent.com/shitagaki-lab/see-through/main/inference/scripts/inference_psd.py",
 "stretchy_psd_reader": "https://raw.githubusercontent.com/MangoLion/stretchystudio/24a83a27ba43e43e9d2e3de5e33994594e6199c2/src/io/psd.js",
 "stretchy_organizer": "https://raw.githubusercontent.com/MangoLion/stretchystudio/24a83a27ba43e43e9d2e3de5e33994594e6199c2/src/io/psdOrganizer.js",
}
EXPECT = {
 "see_through_cli": ["--srcp", "--save_to_psd", "further_extr", "apply_layerdiff", "apply_marigold"],
 "stretchy_psd_reader": ["importPsd(buffer)", "readPsd(buffer", "imageData", "layers.reverse()"],
 "stretchy_organizer": ["KNOWN_TAGS", "organizeCharacterLayers", "'back hair'", "'front hair'", "'face'", "'mouth'", "'neck'", "'topwear'"],
}

def fetch(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent":"NoPants-readiness-probe/1.0"}), timeout=30) as response:
        if response.status != 200:
            raise RuntimeError(f"Unexpected HTTP status {response.status}")
        content = response.read(500_001)
        if len(content) > 500_000:
            raise RuntimeError("Source file exceeds bounds")
        return content.decode("utf-8")

def analyze(sources):
    findings = {}
    for name, content in sources.items():
        missing = [term for term in EXPECT[name] if term not in content]
        findings[name] = {
            "url": SOURCES[name],
            "sha256": hashlib.sha256(content.encode()).hexdigest(),
            "checks": len(EXPECT[name]),
            "passed": not missing,
            "missing": missing
        }
    findings["static_contract"] = {
        "passed": all(f["passed"] for f in findings.values()),
        "meaning": "See-through exports layered PSD; Stretchy parses layered PSD and has compatible semantic tag families",
        "limitations": [
            "No PSD byte-level interoperability was executed",
            "No See-through model or weights downloaded",
            "No user artwork processed",
            "Naming conventions and blend modes may still require adaptation",
            "Semantic layers alone do not guarantee usable skeletal pivots"
        ],
    }
    return findings

def main():
    payload = {name: fetch(url) for name,url in SOURCES.items()}
    report = analyze(payload)
    output = pathlib.Path("output/4a")
    output.mkdir(parents=True, exist_ok=True)
    (output/"interface_readiness.json").write_text(json.dumps(report, indent=2))
    print("4A public upstream static contract probe:", "PASS" if report["static_contract"]["passed"] else "FAIL")
    for name, item in report.items():
        if name == "static_contract": continue
        print(f"  {name}: {'PASS' if item['passed'] else 'FAIL'} ({item['checks']} markers)")
    if not report["static_contract"]["passed"]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
