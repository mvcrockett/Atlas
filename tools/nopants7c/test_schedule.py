#!/usr/bin/env python3
"""CPU-only synthetic and source-free timing tests. No art uploaded."""
import json
import tempfile
import subprocess
import sys
from pathlib import Path
from runpy import run_path
m=run_path(str(Path(__file__).with_name('schedule.py')))
f=m['schedule']
sample={"mouthCues":[{"start":0,"end":0.5,"value":"A"},{"start":0.5,"end":1.0,"value":"C"},{"start":1.0,"end":2.0,"value":"E"},{"start":2,"end":3,"value":"X"}]}
frames=f(sample)
assert len(frames)==120
assert frames[0]["mouth_asset"]=="mouth_rest.png"
assert frames[12]["mouth_asset"]=="mouth_medium.png"
assert frames[24]["mouth_asset"]=="mouth_rounded.png"
assert frames[48]["mouth_asset"]=="mouth_rest.png"
assert frames[119]["mouth_asset"]=="mouth_rest.png"
assert [x["frame"] for x in frames]==list(range(120))
try:f({"mouthCues":[{"start":1,"end":0,"value":"B"}]})
except ValueError:pass
else:raise AssertionError("invalid cues accepted")
try:f({"mouthCues":[{"start":0,"end":1,"value":"??"}]})
except ValueError:pass
else:raise AssertionError("unknown cue accepted")
with tempfile.TemporaryDirectory() as d:
    d=Path(d);(d/'cues.json').write_text(json.dumps(sample))
    subprocess.run([sys.executable,str(Path(__file__).with_name('schedule.py')),str(d/'cues.json'),'--output',str(d/'map.json')],check=True)
    assert json.loads((d/'map.json').read_text())["frame_count"]==120
print("PASS: 7C cue frame scheduling + bounds + CLI. Private artwork not accessed.")
