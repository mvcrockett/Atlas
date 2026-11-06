import io,zipfile,hashlib,tempfile,json,os
from pathlib import Path
from PIL import Image
from private_transport import verify_bundle,seal_evidence,open_evidence,REQUIRED

def synth_bundle():
    im=Image.new('RGBA',(128,128),(13,22,31,255)); p=io.BytesIO();im.save(p,format='PNG')
    layers=[{'id':n[:-4],'path':n,'order':i} for i,n in enumerate(sorted(REQUIRED)) if n.endswith('.png') and n!='reference_source.png']
    m={'status':'PRIVATE_CANONICAL_EXPERIMENTAL','production_art_ready':False,'native_render_verified':False,'canvas':{'width':128,'height':128},'layers':layers}
    s={'fps':24,'frame_count':120,'frames':[{'frame':i,'mouth_asset':'mouth_rest.png'} for i in range(120)]}
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:
        for name in REQUIRED:
            raw=p.getvalue() if name.endswith('.png') else json.dumps(m if name=='manifest.json' else s).encode() if name.endswith('.json') else b'RIFF....WAVE'
            z.writestr(name,raw)
    return b.getvalue()
raw=synth_bundle()
with tempfile.TemporaryDirectory() as t:
    assert verify_bundle(raw,hashlib.sha256(raw).hexdigest(),Path(t)/'private')=={'members':12,'layers':8,'frames':120}
    try:verify_bundle(raw,'0'*64,Path(t)/'other')
    except ValueError:pass
    else:raise AssertionError('wrong hash accepted')
key=os.urandom(32)
c=seal_evidence({'native7f.mp4':b'FAKE-SYNTHETIC-VID','metrics.json':b'{}'},key)
assert c.startswith(b'NPS7F1') and b'FAKE-SYNTHETIC-VID' not in c
with zipfile.ZipFile(io.BytesIO(open_evidence(c,key))) as z:
    assert z.read('native7f.mp4')==b'FAKE-SYNTHETIC-VID'
try:open_evidence(c,os.urandom(32))
except Exception:pass
else:raise AssertionError('wrong key accepted')
print('PASS source-free private ZIP integrity, schedule contract, AES-GCM roundtrip and wrong-key rejection')
