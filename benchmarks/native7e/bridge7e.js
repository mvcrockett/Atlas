// Stretchy ScenePass + computePoseOverrides; Rhubarb-shaped mouth cues; 5 sec/24fps.
// This bridge contains no character artwork. Never publish private art to public Git.
import {ScenePass} from '/src/renderer/scenePass.js';
import {computePoseOverrides} from '/src/renderer/animationEngine.js';
const canvas=document.querySelector('#canvas');
const gl=canvas.getContext('webgl2',{alpha:true,premultipliedAlpha:false,preserveDrawingBuffer:true,stencil:true});
if(!gl)throw Error('WebGL2 unavailable');
const [mr,sr]=await Promise.all([fetch('/art/manifest.json'),fetch('/art/schedule.json')]);
if(!mr.ok||!sr.ok)throw Error('Expected art manifest and Rhubarb frame schedule');
const manifest=await mr.json(),schedule=await sr.json();
if(!Array.isArray(manifest.layers)||!manifest.layers.length||schedule.frame_count!==120||schedule.frames?.length!==120)throw Error('Invalid 5s art/schedule contract');
const W=manifest.canvas.width,H=manifest.canvas.height;
const scale=Math.min(460/W,450/H),ox=(480-W*scale)/2,oy=(480-H*scale)/2;
const transform=(x=0,y=0,pivot=[0,0])=>({x,y,rotation:0,scaleX:1,scaleY:1,pivotX:pivot[0],pivotY:pivot[1]});
const quad=(w,h)=>({vertices:[{x:0,y:0},{x:w,y:0},{x:w,y:h},{x:0,y:h}],uvs:new Float32Array([0,0,1,0,1,1,0,1]),triangles:[[0,1,2],[0,2,3]],edgeIndices:[0,1,2,3]});
const scene=new ScenePass(gl);
const nodes=[{id:'root',type:'group',parent:null,name:'root',visible:true,opacity:1,transform:transform()},
{id:'head',type:'group',parent:'root',name:'head',visible:true,opacity:1,transform:transform()}];
const parts=new Set();
for(const [i,l] of manifest.layers.entries()){
 if(!l.id||!l.path||parts.has(l.id))throw Error('Invalid/duplicate art part');
 const image=new Image();image.src='/art/'+l.path;await image.decode();parts.add(l.id);
 const q=quad(image.width,image.height);
 nodes.push({id:l.id,type:'part',parent:'head',name:l.id,visible:true,opacity:1,draw_order:l.order??i,transform:transform(l.x??0,l.y??0,l.pivot??[0,0]),mesh:q});
 scene.parts.uploadMesh(l.id,q);scene.parts.uploadTexture(l.id,image);
}
for(const k of ['face_base','eyes_open','eyes_closed','mouth_rest','mouth_small','mouth_medium','mouth_wide','mouth_rounded'])if(!parts.has(k))throw Error('Missing rig part '+k);
const animation={id:'nopants7e',name:'five_second_speech',duration:5000,fps:24,tracks:[
 {nodeId:'head',property:'y',keyframes:[[0,0],[1250,-1.6],[2500,0],[3750,1.6],[5000,0]].map(([time,value])=>({time,value,easing:'ease-both'}))}
]};
const project={version:'7e',canvas:{width:W,height:H},nodes,animations:[animation]};
const editor={view:{zoom:scale,panX:ox,panY:oy},overlays:{showImage:true,showWireframe:false,showVertices:false,showEdgeOutline:false,irisClipping:false},selection:[],meshEditMode:false};
window.__s7eReady=true;window.__s7eManifestStatus=manifest.status;
window.__renderS7EFrame=(i)=>{
 if(!Number.isInteger(i)||i<0||i>=120)throw Error('Frame out of bounds');
 const state=schedule.frames[i];
 const name=String(state.mouth_asset||'mouth_rest.png').replace('.png','');
 if(!parts.has(name))throw Error('Unknown cue art '+name);
 const blink=[39,89].some(mid=>Math.abs(mid-i)<=2);
 const pose=computePoseOverrides(animation,i*1000/24);
 for(const id of parts){
  let visible=1;
  if(id.startsWith('mouth_'))visible=id===name?1:0;
  if(id==='eyes_open')visible=blink?0:1;
  if(id==='eyes_closed')visible=blink?1:0;
  pose.set(id,{...(pose.get(id)||{}),opacity:visible});
 }
 scene.draw(project,editor,false,pose,{skipResize:true,exportMode:true});
 return {dataUrl:canvas.toDataURL('image/png'),telemetry:{frame:i,blink,mouth:name,headY:pose.get('head')?.y||0}};
};
window.__renderS7EFrame(0);
