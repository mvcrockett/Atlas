"""Secure, source-only bridge from owner-approved HTTPS private art ZIP to native Stretchy.
No private bytes are committed, printed, or put in plaintext Actions artifacts.
Requires explicit owner-approved host + separately set GitHub encrypted secrets.
"""
import hashlib
import os
import pathlib
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "nopants7f"))
from private_transport import verify_bundle, seal_evidence, MAX_COMPRESSED

EVIDENCE_NAMES = ("native7e.mp4", "metrics.json", "inspect_0000.png",
                  "inspect_0018.png", "inspect_0039.png", "inspect_0062.png",
                  "inspect_0089.png", "inspect_0119.png")

def receive_private_bundle(url, expected_digest, destination):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Private art host must be a valid HTTPS URL without userinfo")
    request=urllib.request.Request(url, headers={"User-Agent":"NoPants-Secure-Runner/7G"})
    with urllib.request.urlopen(request, timeout=60) as response:
        final=urllib.parse.urlparse(response.geturl())
        if final.scheme != "https" or final.username or final.password:
            raise ValueError("Private art redirect must remain HTTPS")
        raw=response.read(MAX_COMPRESSED+1)
    if len(raw)>MAX_COMPRESSED:
        raise ValueError("Private art ZIP exceeds size cap")
    return verify_bundle(raw, expected_digest, destination)

def seal_native_output(output_dir, key_hex, ciphertext_path):
    try:
        key=bytes.fromhex(key_hex)
    except ValueError as exc:
        raise ValueError("Invalid encryption key format") from exc
    if len(key)!=32:
        raise ValueError("Evidence key must be 32 bytes")
    folder=pathlib.Path(output_dir)
    evidence={}
    for name in EVIDENCE_NAMES:
        path=folder/name
        if not path.is_file() or path.stat().st_size==0:
            raise FileNotFoundError("Expected private evidence file missing")
        evidence[name]=path.read_bytes()
    output=pathlib.Path(ciphertext_path)
    output.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
    output.write_bytes(seal_evidence(evidence,key))
    output.chmod(0o600)
    return len(evidence)

def main():
    if len(sys.argv)!=2 or sys.argv[1] not in ("ingress","seal"):
        raise SystemExit("Usage: python private_bridge.py ingress|seal")
    # Do not print or echo secrets, asset URIs, private file names, or captured imagery.
    if sys.argv[1]=="ingress":
        url=os.environ.get("NOPANTS_ART_BUNDLE_URL","")
        digest=os.environ.get("NOPANTS_ART_BUNDLE_SHA256","")
        target=os.environ.get("NOPANTS_ASSET_DIR","")
        if not all((url,digest,target,os.environ.get("NOPANTS_EVIDENCE_KEY_HEX"))):
            raise SystemExit("Private runner unconfigured. No art retrieved.")
        receive_private_bundle(url,digest,target)
        print("Private input verified; asset bytes remain ephemeral.")
    else:
        k=os.environ.get("NOPANTS_EVIDENCE_KEY_HEX","")
        if not k:raise SystemExit("Private evidence key missing. No output uploaded.")
        seal_native_output("output/nopants7e",k,"output/nopants7g/sealed_evidence.aesgcm")
        print("Authenticated ciphertext prepared; no plaintext artifact publishing.")

if __name__=="__main__":
    main()
