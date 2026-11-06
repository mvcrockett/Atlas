"""Decrypt Sprint 3E evidence locally. Never commit your secret key."""
import argparse, pathlib, os, zipfile, io
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
parser=argparse.ArgumentParser()
parser.add_argument("encrypted_file",help="private_evidence.aesgcm from the Actions artifact")
parser.add_argument("--out",default="nopants_sprint3e_decoded")
args=parser.parse_args()
raw=pathlib.Path(args.encrypted_file).read_bytes()
if not raw.startswith(b"NP3E1") or len(raw)<34:
    raise SystemExit("Invalid evidence envelope")
secret=os.environ.get("NOPANTS_EVIDENCE_KEY_HEX","").strip()
if len(secret)!=64:
    raise SystemExit("Set NOPANTS_EVIDENCE_KEY_HEX privately in your environment; do not paste it into chat")
try:
    clear=AESGCM(bytes.fromhex(secret)).decrypt(raw[5:17],raw[17:],b"NoPants-Sprint3E-v1")
except Exception:
    raise SystemExit("Evidence authentication failed; incorrect key or corrupt data")
dst=pathlib.Path(args.out)
dst.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(io.BytesIO(clear)) as z:
    for info in z.infolist():
        p=pathlib.PurePosixPath(info.filename)
        if p.is_absolute() or ".." in p.parts:
            raise SystemExit("Refusing unsafe evidence path")
    z.extractall(dst)
print("Private evidence decrypted locally into",dst,"(never publish these files)")
