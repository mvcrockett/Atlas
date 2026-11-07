#!/usr/bin/env python3
"""Render the verified private 7F kit locally without publishing or hosting it.
Requires pinned Stretchy source, Playwright Chromium and FFmpeg. No network install.
"""
import argparse, functools, http.server, os, pathlib, shutil, subprocess, sys, tempfile, threading
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'tools/nopants7f'))
from private_transport import verify_bundle
PIN='24a83a27ba43e43e9d2e3de5e33994594e6199c2'
class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--stretchy',type=pathlib.Path,required=True)
    p.add_argument('--bundle',type=pathlib.Path,required=True)
    p.add_argument('--sha256',required=True)
    p.add_argument('--output',type=pathlib.Path,required=True)
    p.add_argument('--mode',choices=['native','legacy'],default='native')
    a=p.parse_args()
    head=subprocess.check_output(['git','-C',str(a.stretchy),'rev-parse','HEAD'],text=True).strip()
    if head!=PIN:raise ValueError('Unexpected upstream revision')
    # Refuse local source modifications: HEAD alone is insufficient provenance.
    changed=subprocess.check_output(['git','-C',str(a.stretchy),'status','--porcelain','--','src'],text=True)
    if changed:raise ValueError('Upstream renderer source must be clean')
    with tempfile.TemporaryDirectory(prefix='nopants-private-') as d:
        stage=pathlib.Path(d)
        verify_bundle(a.bundle.read_bytes(),a.sha256,stage/'art')
        shutil.copytree(a.stretchy/'src',stage/'src')
        for name in ['bridge7e.html','bridge7e.js','render_contract.mjs']:
            shutil.copyfile(pathlib.Path(__file__).parent/name,stage/name)
        server=http.server.ThreadingHTTPServer(('127.0.0.1',5173),functools.partial(QuietHandler,directory=str(stage)))
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        env={**os.environ,'NOPANTS_AUDIO_PATH':str(stage/'art/dialogue.wav'),
             'NOPANTS_OUTPUT_DIR':str(a.output.resolve()),'NOPANTS_RENDER_MODE':a.mode}
        try:
            subprocess.run(['node',str(pathlib.Path(__file__).parent/'capture7e.mjs')],env=env,check=True)
        finally:
            server.shutdown();server.server_close();thread.join()
    print('PASS: local native export finished; ephemeral input staging removed.')
if __name__=='__main__':main()
