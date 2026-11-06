#!/usr/bin/env python3
"""Source-free synthetic validation: no original heroine files or private data."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
sys.path.insert(0,str(Path(__file__).parent))
from validate_private_asset_manifest import validate,REQUIRED
m={"asset_classification":"PRIVATE_DO_NOT_PUBLISH",
   "native_rig_status":"NOT_VERIFIED",
   "cropping":{"source_bbox":[0,0,40,40],"output_size":[24,24]},
   "source_portrait_sha256":"a"*64,"reference_sheet_sha256":"b"*64,
   "layer_status":{x:"synthetic" for x in REQUIRED}}
assert validate(m,None)==len(REQUIRED)
with TemporaryDirectory() as x:
 p=Path(x)
 for n in REQUIRED:(p/n).write_bytes(b"synthetic-content")
 assert validate(m,p)==len(REQUIRED)
 (p/"mouth_medium.png").unlink()
 try:validate(m,p)
 except FileNotFoundError:pass
 else:raise AssertionError("missing asset not rejected")
for bad in [{"asset_classification":"PUBLIC"},{'native_rig_status':'VERIFIED'},{'cropping':{'source_bbox':[0,0,20,20],'output_size':[0,0]}}]:
 broken=dict(m);broken.update(bad)
 try:validate(broken,None)
 except ValueError:pass
 else:raise AssertionError("unsafe manifest accepted")
print("PASS: synthetic manifest, missing assets, unsafe status and bad dimensions checks.")
