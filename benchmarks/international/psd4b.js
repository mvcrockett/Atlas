// NoPants 4B: actual PSD bytes -> existing Stretchy importPsd + organizer + ScenePass.
// Third-party public PSD sample stays inside ephemeral GitHub runner, never committed or artifacted.
import {importPsd} from '/src/io/psd.js';
import {matchTag,detectCharacterFormat,organizeCharacterLayers} from '/src/io/psdOrganizer.js';
import {ScenePass} from '/src/renderer/scenePass.js';
import {computePoseOverrides} from '/src/renderer/animationEngine.js';
const c=document.getElementById('screen');
const gl=c.getContext('webgl2',{alpha:true,stencil:true,preserveDrawingBuffer:true});
if(!gl) throw new Error('WebGL2 unavailable');
const res=await fetch('/fixture.psd');
if(!res.ok)throw new Error('Public PSD fixture HTTP '+res.status);
const buffer=await res.arrayBuffer();
const imported=importPsd(buffer);
if(!imported.layers.length) throw new Error('Native importPsd returned zero pixel layers');
const W=imported.width,H=imported.height;
const layers=imported.layers;
const tagCount=layers.filter(l=>matchTag(l.name)).length;
const opaqueStats=[], info=[];
const scene=new ScenePass(gl);
const nodes=[{id:'root',type:'group',parent:null,name:'root',visible:true,opacity:1,transform:{x:0,y:0,rotation:0,scaleX:1,scaleY:1,pivotX:0,pivotY:0}}];
const mkGroup=(id,parent,pivot)=>({id,name:id,type:'group',parent,visible:true,opacity:1,transform:{x:0,y:0,rotation:0,scaleX:1,scaleY:1,pivotX:pivot[0],pivotY:pivot[1]}});
nodes.push(mkGroup('body','root',[W/2,H*.65]),mkGroup('head','body',[W/2,H*.34]));
const normalized=(name)=>matchTag(name)||'unknown';
for(let i=0;i<layers.length;i++){
 const l=layers[i], id='psdpart_'+i, tag=normalized(l.name);
 const p=tag==='front hair'||tag==='back hair'||tag==='face'||tag==='mouth'||tag==='nose'||tag==='eyebrow'||tag==='eyelash'||tag==='eyewhite'||tag==='irides'||tag==='ears'||tag==='headwear'||tag==='earwear'?'head':'body';
 const img=l.imageData;
 const texture=document.createElement('canvas');texture.width=W;texture.height=H;
 const tx=texture.getContext('2d');
 if(img.width===W&&img.height===H) tx.putImageData(img,0,0);
 else tx.putImageData(img,l.x,l.y);
 let nonempty=0;
 const pixels=img.data;
 for(let j=3;j<pixels.length;j+=4)if(pixels[j]!==0)nonempty++;
 const total=img.width*img.height;
 const textured=nonempty>0;
 opaqueStats.push(nonempty);
 info.push({name:l.name,tag,offset:[l.x,l.y],dims:[img.width,img.height],nonempty_pixels:nonempty,alpha_coverage_ratio:nonempty/Math.max(1,total),opacity:l.opacity,visible:l.visible});
 if(!textured)continue;
 const node={id,type:'part',name:l.name,parent:p,visible:l.visible!==false,opacity:l.opacity??1,draw_order:i,transform:{x:0,y:0,rotation:0,scaleX:1,scaleY:1,pivotX:0,pivotY:0}};
 nodes.push(node);
 scene.parts.uploadQuadFallback(id,W,H);
 scene.parts.uploadTexture(id,texture);
}
const header={source:'third-party public sample2.psd from 852wa/Anime2.5DRig; not verified See-through-produced, no distribution rights implied',format:'PSD',importer:'Stretchy src/io/psd.js importPsd, ag-psd',organizer:'Stretchy src/io/psdOrganizer.js',width:W,height:H,parsed_layers:layers.length,nonempty_layers:opaqueStats.filter(n=>n>0).length,tagged_layers:tagCount,character_format_detected:detectCharacterFormat(layers),layer_properties:info};
const hierarchy=organizeCharacterLayers(layers,()=>('o'+Math.random().toString(36).slice(2)));
header.organizer_groups=hierarchy.groupDefs.map(x=>x.name);
const animation={id:'psd4b',name:'minimal_head_motion',duration:2000,fps:24,tracks:[{nodeId:'head',property:'y',keyframes:[{time:0,value:0},{time:500,value:-4},{time:1000,value:0},{time:1500,value:4},{time:2000,value:0}]}]};
const project={canvas:{width:W,height:H},nodes,animations:[animation]};
const scale=Math.min(460/W,450/H);
const editor={view:{zoom:scale,panX:(480-W*scale)/2,panY:(480-H*scale)/2},overlays:{showImage:true,showWireframe:false,showVertices:false,showEdgeOutline:false,irisClipping:false},selection:[],meshEditMode:false};
window.__psdHeader=header;
window.__psdReady=true;
window.__renderPSDFrame=(n)=>{
 const pose=computePoseOverrides(animation,n/24*1000);
 scene.draw(project,editor,false,pose,{skipResize:true,exportMode:true});
 return {frame:n,head_y:pose.get('head')?.y??0,dataUrl:c.toDataURL('image/png')};
};
window.__renderPSDFrame(0);
