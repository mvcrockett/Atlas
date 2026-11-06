#!/usr/bin/env python3
"""Patch temporary upstream Anime2.5DRig in CI, without editing our public fork.
Add deterministic 24Hz frame stepper while reusing original animate/render and rigger.
"""
import pathlib,sys
p=pathlib.Path(sys.argv[1])
code=p.read_text()
anchor="requestAnimationFrame(tick);"
pos=code.rfind(anchor)
if pos<0:raise SystemExit('Upstream app.js tick anchor missing')
injection=r"""
// BEGIN NoPants test-only frame stepper (upstream animate/render retained)
window.__nopants4dStep=(frame)=>{
 if(!layers.length||!currentRig)throw Error('Model not loaded');
 paused=true;
 for(const key of ['idle','blink','rand','talk','cam','mouse','mic'])auto[key]=false;
 auto.phys=true;
 const t=frame/24;
 const pi=Math.PI;
 const headSway=Math.sin(t*2*pi/3);
 // Same scheduled blink and mouth targets as Stretchy control.
 const triangle=(c,w)=>Math.max(0,1-Math.abs(t-c)/w);
 const blink=Math.max(triangle(.75,.125),triangle(2.125,.125));
 T.angleX=0;T.angleY=.045*headSway;T.angleZ=.028*headSway;
 T.body=.015*Math.sin(t*2*pi/3);
 T.eyeOpenL=1-blink;T.eyeOpenR=1-blink;
 T.mouthOpen=Math.max(0,triangle(1.8,.35));
 T.mouthForm=.15*Math.sin(t*2*pi/3);
 T.bangL=.015*Math.sin(t*2*pi/3);T.bangC=.015*Math.sin(t*2*pi/3);T.bangR=.015*Math.sin(t*2*pi/3);
 lastFrame=animate(t*1000,1/24);render(lastFrame);
 const pixels=new Uint8Array(CW*CH*4);gl.readPixels(0,0,CW,CH,gl.RGBA,gl.UNSIGNED_BYTE,pixels);
 const ctx=document.createElement('canvas');ctx.width=CW;ctx.height=CH;
 const c2=ctx.getContext('2d');const im=c2.createImageData(CW,CH);
 for(let y=0;y<CH;y++){const src=(CH-1-y)*CW*4,dst=y*CW*4;im.data.set(pixels.subarray(src,src+CW*4),dst);}
 c2.putImageData(im,0,0);
 return {frame,blink,mouthOpen:T.mouthOpen,headSway,dataUrl:ctx.toDataURL('image/png')};
};
window.__nopants4dReady=true;
// END NoPants test-only frame stepper
"""
code=code[:pos]+injection+'\n'+code[pos:]
p.write_text(code)
print('Deterministic Anime2.5DRig test hook installed (no replacement of upstream engine)')
