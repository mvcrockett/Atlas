"""Source-free test for NPS7I1 encrypted Dropbox input and 7F verified contract."""
import io, hashlib, os, pathlib, sys, tempfile, zipfile, json
from PIL import Image
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
sys.path.insert(0,str(pathlib.Path(__file__).parent))
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'nopants7f'))
from ingress_encrypted import decrypt_blob, ingest, MAGIC, ITERATIONS
from private_transport import REQUIRED

PASSWORD='SYNTHETIC-TEST-PASSWORD-NOT-REAL-123456789'
def make_zip():
    img=Image.new('RGBA',(128,128),(20,30,40,255));p=io.BytesIO();img.save(p,format='PNG')
    layers=[{'id':n[:-4],'path':n,'order':i} for i,n in enumerate(sorted(REQUIRED)) if n.endswith('.png') and n!='reference_source.png']
    m={'status':'PRIVATE_CANONICAL_EXPERIMENTAL','production_art_ready':False,'native_render_verified':False,
       'canvas':{'width':128,'height':128},'layers':layers}
    s={'fps':24,'frame_count':120,'frames':[{'frame':i,'mouth_asset':'mouth_rest.png'} for i in range(120)]}
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w') as z:
        for name in REQUIRED:
            raw=p.getvalue() if name.endswith('.png') else json.dumps(m if name=='manifest.json' else s).encode() if name.endswith('.json') else b'RIFF-DUMMY-WAVE'
            z.writestr(name,raw)
    return out.getvalue()

def encrypt(b,password=PASSWORD):
    salt=os.urandom(16);nonce=os.urandom(12)
    key=hashlib.pbkdf2_hmac('sha256',password.encode(),salt,ITERATIONS,32)
    return MAGIC+salt+nonce+AESGCM(key).encrypt(nonce,b,None)

raw=make_zip();digest=hashlib.sha256(raw).hexdigest();cipher=encrypt(raw)
assert cipher.startswith(MAGIC)
assert decrypt_blob(cipher,PASSWORD,digest)==raw
for broken,passwd,sha in [(cipher,'wrong-password',digest),(cipher[:-1]+bytes([cipher[-1]^1]),PASSWORD,digest),(cipher,PASSWORD,'0'*64)]:
    try:decrypt_blob(broken,passwd,sha)
    except ValueError:pass
    else:raise AssertionError('bad encrypted input accepted')
class Response:
    def __init__(self,data):self._data=io.BytesIO(data)
    def __enter__(self):return self
    def __exit__(self,*a):pass
    def geturl(self):return 'https://approved.example.org/temporary-download'
    def read(self,n):return self._data.read(n)
import ingress_encrypted
original=ingress_encrypted.urllib.request.urlopen
ingress_encrypted.urllib.request.urlopen=lambda request,timeout=60:Response(cipher)
try:
    with tempfile.TemporaryDirectory() as t:
        result=ingest('https://approved.example.org/temporary-download',PASSWORD,digest,pathlib.Path(t)/'private')
        assert result['frames']==120 and result['layers']==8
    with tempfile.TemporaryDirectory() as t:
        try:ingest('http://approved.example.org/plaintext',PASSWORD,digest,pathlib.Path(t)/'private')
        except ValueError:pass
        else:raise AssertionError('HTTP accepted')
finally:
    ingress_encrypted.urllib.request.urlopen=original
print('PASS: password-derived AES-GCM decrypt, digest, 12-file bundle, HTTPS-only, wrong password, tamper and wrong SHA rejected; SYNTHETIC ONLY')
