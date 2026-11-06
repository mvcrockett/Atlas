// Generic textured-layer adapter for Stretchy Studio. No raster art is redrawn.
import { ScenePass } from '/src/renderer/scenePass.js';
import { computePoseOverrides } from '/src/renderer/animationEngine.js';
const canvas=document.getElementById('canvas');
const gl=canvas.getContext('webgl2',{alpha:true,stencil:true,preserveDrawingBuffer:true});
if(!gl) throw new Error('WebGL2 not available');
const scene=new ScenePass(gl);
const manifest=await (await fetch('/art/manifest.json')).json();
if(!Array.isArray(manifest.layers)||manifest.layers.length<2)throw new Error('Need at least two layers');
const cw=manifest.canvas.width,ch=manifest.canvas.height;
const scale=Math.min(460/cw,450/ch);
const originX=(480-cw*scale)/2,originY=(480-ch*scale)/2;
function mesh(w,h){return {vertices:[{x:0,y:0},{x:w,y:0},{x:w,y:h},{x:0,y:h}],uvs:new Float32Array([0,0,1,0,1,1,0,1]),triangles:[[0,1,2],[0,2,3]],edgeIndices:[0,1,2,3]};}
function group(id,parent=null){return {id,type:'group',name:id,parent,visible:true,opacity:1,transform:{x:0,y:0,rotation:0,scaleX:1,scaleY:1,pivotX:0,pivotY:0}};}
const nodes=[group('root')];
const animTracks=[];
for(const [i,part] of manifest.layers.entries()){
 const im=new Image();im.src='/art/'+part.path;await im.decode();
 const id=part.id,parent=part.parent||'root';
 const pivot=part.pivot||[0,0];
 const node={id,type:'part',name:id,parent,draw_order:part.order??i,visible:true,opacity:1,imageWidth:im.width,imageHeight:im.height,transform:{x:part.x||0,y:part.y||0,rotation:0,scaleX:1,scaleY:1,pivotX:pivot[0],pivotY:pivot[1]},mesh:mesh(im.width,im.height)};
 nodes.push(node);
 scene.parts.uploadMesh(id,node.mesh);
 scene.parts.uploadTexture(id,im);
}
const layerIds=new Set(manifest.layers.map(x=>x.id));
for(const control of Object.values(manifest.controls||{})){
 if(!layerIds.has(control.node))throw new Error('Invalid control node: '+control.node);
}
const head=manifest.controls?.head_y?.node||manifest.layers[manifest.layers.length-1].id;
const torso=manifest.controls?.breathing?.node||manifest.layers[0].id;
animTracks.push(
 {nodeId:head,property:'y',keyframes:[{time:0,value:0},{time:500,value:-4},{time:1000,value:0},{time:1500,value:4},{time:2000,value:0}]},
 {nodeId:torso,property:'scaleY',keyframes:[{time:0,value:1},{time:1000,value:1.015},{time:2000,value:1}]},
);
const anim={id:'bridge',name:'art_to_rig_head_breathe',fps:24,duration:2000,tracks:animTracks};
const project={version:'benchmark',canvas:{width:cw,height:ch},nodes,animations:[anim]};
const editor={view:{zoom:scale,panX:originX,panY:originY},overlays:{showImage:true,showWireframe:false,showVertices:false,showEdgeOutline:false,irisClipping:false},selection:[],meshEditMode:false};
window.__artManifest=manifest;
window.__renderBridgeFrame=(i)=>{
 const pose=computePoseOverrides(anim,i/24*1000);
 gl.viewport(0,0,480,480);
 gl.clearColor(1,1,1,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.STENCIL_BUFFER_BIT);
 scene.draw(project,editor,false,pose,{skipResize:true,exportMode:true});
 return {dataUrl:canvas.toDataURL('image/png'),telemetry:{frame:i,headY:pose.get(head)?.y??0,torsoScaleY:pose.get(torso)?.scaleY??1}};
};
window.__bridgeReady=true;
window.__renderBridgeFrame(0);
