from types import SimpleNamespace
"""No secrets or real art: bounded HTTPS ingress and encrypted egress contract tests."""
import hashlib, io, json, os, pathlib, sys, tempfile, zipfile
from PIL import Image
sys.path.insert(0,str(pathlib.Path(__file__).parent))
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1] / "nopants7f"))
import private_bridge as bridge
from private_transport import open_evidence, REQUIRED

def fake_bundle():
    im=Image.new("RGBA",(128,128),(20,33,44,255))
    png=io.BytesIO();im.save(png,format="PNG")
    parts=sorted(REQUIRED-{"reference_source.png","manifest.json","schedule.json","dialogue.wav"})
    manifest={"status":"PRIVATE_CANONICAL_EXPERIMENTAL","production_art_ready":False,
      "native_render_verified":False,"canvas":{"width":128,"height":128},
      "layers":[{"id":n[:-4],"path":n,"order":i} for i,n in enumerate(parts)]}
    schedule={"fps":24,"frame_count":120,"frames":[{"frame":i,"mouth_asset":"mouth_rest.png"} for i in range(120)]}
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w") as z:
        for n in REQUIRED:
            payload=png.getvalue() if n.endswith(".png") else json.dumps(manifest if n=="manifest.json" else schedule).encode() if n.endswith(".json") else b"RIFF....WAVE"
            z.writestr(n,payload)
    return b.getvalue()

class FakeResponse:
    def __init__(self,data,uri):self.data=io.BytesIO(data);self.uri=uri
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def read(self,n):return self.data.read(n)
    def geturl(self):return self.uri

raw=fake_bundle()
expected=hashlib.sha256(raw).hexdigest()
old=bridge.urllib.request.build_opener
bridge.urllib.request.build_opener=lambda *handlers:SimpleNamespace(open=lambda req,timeout=60:FakeResponse(raw,"https://approved.example.org/one-time"))
try:
    with tempfile.TemporaryDirectory() as tmp:
        target=pathlib.Path(tmp)
        assert bridge.receive_private_bundle("https://approved.example.org/token",expected,target/"art")["frames"]==120
        try:bridge.receive_private_bundle("http://approved.example.org/unsafe",expected,target/"unsafe")
        except ValueError:pass
        else:raise AssertionError("HTTP allowed")
        try:bridge.receive_private_bundle("https://approved.example.org/token","0"*64,target/"bad")
        except ValueError:pass
        else:raise AssertionError("Incorrect digest allowed")
        p=target/"output";p.mkdir()
        for name in bridge.EVIDENCE_NAMES:(p/name).write_bytes(b"synthetic evidence, not user artwork: "+name.encode())
        key=os.urandom(32)
        envelope=target/"sealed.aesgcm"
        assert bridge.seal_native_output(p,key.hex(),envelope)==len(bridge.EVIDENCE_NAMES)
        sealed=envelope.read_bytes()
        assert b"synthetic evidence" not in sealed
        with zipfile.ZipFile(io.BytesIO(open_evidence(sealed,key))) as z:
            assert set(z.namelist())==set(bridge.EVIDENCE_NAMES)
        (p/"native7e.mp4").unlink()
        try:bridge.seal_native_output(p,key.hex(),target/"missing.aesgcm")
        except FileNotFoundError:pass
        else:raise AssertionError("Incomplete output accepted")
    print("PASS: 7G HTTPS-only, digest validation, 120-frame contract, sealed evidence, missing-output rejection; synthetic files only")
finally:
    bridge.urllib.request.build_opener=old
