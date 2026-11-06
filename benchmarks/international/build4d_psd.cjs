// Runs inside temporary pinned Stretchy workspace; builds legitimate layered PSD.
// Uses ag-psd's own writePsdBuffer, not a homegrown PSD serializer.
const fs=require('node:fs');
const path=require('node:path');
const {PNG}=require('pngjs');
require('ag-psd/initialize-canvas'); // upstream native Node canvas initialization
const {writePsdBuffer,readPsd}=require('ag-psd');
const src=process.argv[2]||'art4d';
const dest=process.argv[3]||'fixture.psd';
const names=['back hair','neck','topwear','face','eyewhite','irides','eyelash','eyebrow','mouth_close','mouth_open','eye_close','front hair'];
const visibleSet=new Set(names); // Keep eye/mouth alternatives available to Japanese parser; renderers determine active expression.
const images=names.map(name=>{
 const png=PNG.sync.read(fs.readFileSync(path.join(src,name+'.png')));
 if(png.width!==768||png.height!==768)throw Error('Unexpected PNG dimensions: '+name);
 return {name,top:0,left:0,hidden:!visibleSet.has(name),
     imageData:{width:768,height:768,data:new Uint8ClampedArray(png.data)}};
});
// ag-psd children are topmost first; keep all expression states as independently addressable layers
const psd={width:768,height:768,children:images.reverse(),colorMode:3,bitsPerChannel:8};
const bytes=writePsdBuffer(psd,{generateThumbnail:false});
fs.writeFileSync(dest,Buffer.from(bytes));
const parsed=readPsd(fs.readFileSync(dest),{useImageData:true,skipCompositeImageData:true});
const seen=parsed.children.map(x=>x.name);
for(const name of names)if(!seen.includes(name))throw Error('Missing PSD layer: '+name);
if(parsed.width!==768||parsed.height!==768||parsed.children.length!==12)throw Error('Roundtrip failed');
console.log('ag-psd 768px PSD roundtrip PASS:',parsed.children.length,'layers,',bytes.length,'bytes');
