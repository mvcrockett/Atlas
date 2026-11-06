"""Source-only private native-art transport contracts for NoPants Studio.

Never print URLs, keys, private pixels, or decrypted artifacts. No network side effects.
"""
import hashlib, hmac, io, json, pathlib, zipfile, secrets
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

REQUIRED = {"manifest.json", "schedule.json", "reference_source.png", "dialogue.wav",
            "face_base.png", "eyes_open.png", "eyes_closed.png", "mouth_rest.png",
            "mouth_small.png", "mouth_medium.png", "mouth_wide.png", "mouth_rounded.png"}
MAX_COMPRESSED = 40*1024*1024
MAX_EXPANDED = 100*1024*1024
MAGIC=b'NPS7F1'; AAD=b'NoPantsSprint7F-EncryptedEvidence-v1'

def verify_bundle(raw, expected_sha256, private_destination):
    if not isinstance(raw,bytes) or len(raw)>MAX_COMPRESSED:
        raise ValueError('bundle absent or too large')
    digest=hashlib.sha256(raw).hexdigest()
    if len(expected_sha256)!=64 or not hmac.compare_digest(digest,expected_sha256.lower()):
        raise ValueError('bundle digest mismatch')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        infos=archive.infolist()
        names=[x.filename for x in infos]
        if len(names)>80 or len(names)!=len(set(names)) or not REQUIRED.issubset(names):
            raise ValueError('unexpected archive members')
        if sum(x.file_size for x in infos)>MAX_EXPANDED:
            raise ValueError('bundle decompressed size exceeded')
        for info in infos:
            p=pathlib.PurePosixPath(info.filename)
            if p.is_absolute() or '..' in p.parts or '\\' in info.filename or info.is_dir() or p.name!=info.filename:
                raise ValueError('unsafe archive member')
            if p.suffix not in ('.png','.json','.wav'):
                raise ValueError('disallowed archive member')
        manifest=json.loads(archive.read('manifest.json'))
        schedule=json.loads(archive.read('schedule.json'))
        if manifest.get('status')!='PRIVATE_CANONICAL_EXPERIMENTAL' or manifest.get('production_art_ready') is not False or manifest.get('native_render_verified') is not False:
            raise ValueError('invalid private production status')
        wh=manifest.get('canvas') or {}
        w,h=wh.get('width'),wh.get('height')
        if not isinstance(w,int) or not isinstance(h,int) or not (100<=w<=4096 and 100<=h<=4096):
            raise ValueError('invalid canvas')
        layers=manifest.get('layers') or []
        if not isinstance(layers,list) or len(layers)<8 or len(layers)>60:
            raise ValueError('invalid layer count')
        ids=set()
        for layer in layers:
            if layer.get('path') not in names or layer.get('id') in ids:
                raise ValueError('invalid layer')
            ids.add(layer['id'])
        if schedule.get('fps')!=24 or schedule.get('frame_count')!=120 or len(schedule.get('frames',[]))!=120:
            raise ValueError('invalid timing schedule')
        for i,frame in enumerate(schedule['frames']):
            if frame.get('frame')!=i or frame.get('mouth_asset') not in REQUIRED:
                raise ValueError('unexpected mouth schedule')
        from PIL import Image
        for layer in layers:
            with Image.open(io.BytesIO(archive.read(layer['path']))) as im:
                if im.size!=(w,h) or im.mode not in ('RGB','RGBA'):
                    raise ValueError('invalid image dimensions or mode')
                im.verify()
        target=pathlib.Path(private_destination)
        if target.exists() and any(target.iterdir()):
            raise ValueError('destination must be empty')
        target.mkdir(parents=True,exist_ok=True,mode=0o700)
        for info in infos:
            p=target/info.filename
            with p.open('xb') as f:f.write(archive.read(info.filename))
            p.chmod(0o600)
    return {'members':len(names),'layers':len(layers),'frames':120}

def seal_evidence(private_files,key):
    if not isinstance(key,bytes) or len(key)!=32:
        raise ValueError('AES-256 key must be 32 bytes')
    if not private_files:raise ValueError('missing render evidence')
    contents=io.BytesIO()
    with zipfile.ZipFile(contents,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for name,raw in private_files.items():
            if '/' in name or '\\' in name or name.startswith('.') or not isinstance(raw,bytes):
                raise ValueError('invalid evidence entry')
            archive.writestr(name,raw)
    nonce=secrets.token_bytes(12)
    return MAGIC+nonce+AESGCM(key).encrypt(nonce,contents.getvalue(),AAD)

def open_evidence(ciphertext,key):
    if not ciphertext.startswith(MAGIC) or len(key)!=32:
        raise ValueError('invalid envelope')
    nonce=ciphertext[len(MAGIC):len(MAGIC)+12]
    return AESGCM(key).decrypt(nonce,ciphertext[len(MAGIC)+12:],AAD)
