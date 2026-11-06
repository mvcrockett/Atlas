// Sprint 3D: manifest-driven layered anime animation using upstream Stretchy WebGL.
import {ScenePass} from '/src/renderer/scenePass.js';
import {computePoseOverrides} from '/src/renderer/animationEngine.js';
const canvas=document.getElementById('canvas');
const gl=canvas.getContext('webgl2',{alpha:true,premultipliedAlpha:false,stencil:true,preserveDrawingBuffer:true});
if(!gl)throw new Error('WebGL2 unavailable');
const response=await fetch('/art/manifest.json');
if(!response.ok)throw new Error('Art manifest missing: '+response.status);
const manifest=await response.json();
if(!Array.isArray(manifest.layers)||!manifest.layers.length)throw new Error('Art layers missing');
const scene=new ScenePass(gl), W=manifest.canvas.width,H=manifest.canvas.height;
const scale=Math.min(460/W,450/H);
const ox=(480-W*scale)/2,oy=(480-H*scale)/2;
const transform=(x=0,y=0,pivot=[0,0])=>({x,y,rotation:0,scaleX:1,scaleY:1,pivotX:pivot[0],pivotY:pivot[1]});
function quad(w,h){return {vertices:[{x:0,y:0},{x:w,y:0},{x:w,y:h},{x:0,y:h}],uvs:new Float32Array([0,0,1,0,1,1,0,1]),triangles:[[0,1,2],[0,2,3]],edgeIndices:[0,1,2,3]};}
const nodes=[{id:'root',type:'group',parent:null,name:'root',visible:true,opacity:1,transform:transform()}];
for(const g of manifest.groups||[]){
  if(!g.id||g.id==='root')throw new Error('Invalid group id');
  nodes.push({id:g.id,type:'group',parent:g.parent||'root',name:g.id,visible:true,opacity:1,transform:transform(g.x||0,g.y||0,g.pivot||[0,0])});
}
for(const [i,p] of manifest.layers.entries()){
  if(!p.path||!p.id)throw new Error('Layer missing path/id');
  const image=new Image();
  image.src='/art/'+p.path; await image.decode();
  nodes.push({id:p.id,type:'part',parent:p.parent||'root',name:p.id,visible:true,opacity:p.opacity??1,draw_order:p.order??i,transform:transform(p.x||0,p.y||0,p.pivot||[0,0]),mesh:quad(image.width,image.height)});
  scene.parts.uploadMesh(p.id,quad(image.width,image.height));
  scene.parts.uploadTexture(p.id,image);
}
const idset=new Set(nodes.map(x=>x.id));
if(idset.size!==nodes.length)throw new Error('Duplicate node IDs');
for(const node of nodes){if(node.parent&&!idset.has(node.parent))throw new Error('Missing parent '+node.parent);}
const controls=manifest.controls||{};
const tracks=[];
const add=(id,prop,keys)=>{if(id&&!idset.has(id))throw new Error('Unknown control node '+id);if(id)tracks.push({nodeId:id,property:prop,keyframes:keys.map(([time,value])=>({time,value,easing:'ease-both'}))});};
const head=controls.head_y?.node;
const torso=controls.breathing?.node;
const hair=controls.hair_drift?.node;
add(head,'y',[[0,0],[750,-2],[1500,0],[2250,2],[3000,0]]);
add(torso,'scaleY',[[0,1],[750,1.008],[1500,1],[2250,.998],[3000,1]]);
add(hair,'x',[[0,0],[750,.8],[1500,0],[2250,-.8],[3000,0]]);
add(hair,'rotation',[[0,0],[750,.4],[1500,0],[2250,-.4],[3000,0]]);
const blinkNodes=controls.blink||{};
for(const id of blinkNodes.eyes||[]) add(id,'opacity',[[0,1],[710,1],[750,0],[800,1],[2090,1],[2130,0],[2190,1],[3000,1]]);
for(const id of blinkNodes.closed_lids||[]) add(id,'opacity',[[0,0],[710,0],[750,1],[800,0],[2090,0],[2130,1],[2190,0],[3000,0]]);
const mouths=controls.mouth_swap||{};
add(mouths.neutral,'opacity',[[0,1],[600,1],[1000,0],[1650,0],[1850,0],[2300,0],[2800,1],[3000,1]]);
add(mouths.smile,'opacity',[[0,0],[600,0],[1000,1],[1650,1],[1850,0],[2300,.8],[2800,0],[3000,0]]);
add(mouths.open,'opacity',[[0,0],[1650,0],[1850,1],[2150,1],[2300,0],[3000,0]]);
const animation={id:'s3d',name:'anime_art_micro_motion',duration:3000,fps:24,tracks};
const project={version:'s3d',canvas:{width:W,height:H},nodes,animations:[animation]};
const editor={view:{zoom:scale,panX:ox,panY:oy},overlays:{showImage:true,showWireframe:false,showVertices:false,showEdgeOutline:false,irisClipping:false},selection:[],meshEditMode:false};
window.__sprint3dReady=true;
window.__artManifest=manifest;
window.__renderS3DFrame=i=>{
 const pose=computePoseOverrides(animation,i/24*1000);
 scene.draw(project,editor,false,pose,{skipResize:true,exportMode:true});
 return {dataUrl:canvas.toDataURL('image/png'),telemetry:{frame:i,head_y:pose.get(head)?.y??0,blink_opacity:blinkNodes.closed_lids?.length?(pose.get(blinkNodes.closed_lids[0])?.opacity??0):null,smile_opacity:mouths.smile?(pose.get(mouths.smile)?.opacity??0):null}};
};
window.__renderS3DFrame(0);
