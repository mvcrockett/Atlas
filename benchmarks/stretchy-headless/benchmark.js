import { ScenePass } from '/src/renderer/scenePass.js';
import { computePoseOverrides } from '/src/renderer/animationEngine.js';

const canvas = document.getElementById('stage');
const gl = canvas.getContext('webgl2', {
  alpha: true,
  premultipliedAlpha: false,
  stencil: true,
  preserveDrawingBuffer: true,
});
if (!gl) throw new Error('WebGL2 unavailable');

const scene = new ScenePass(gl);

function quad(w,h){
  return {
    vertices:[{x:0,y:0},{x:w,y:0},{x:w,y:h},{x:0,y:h}],
    uvs:new Float32Array([0,0,1,0,1,1,0,1]),
    triangles:[[0,1,2],[0,2,3]],
    edgeIndices:[0,1,2,3],
  };
}
function stripMesh(){
  const vertices=[
    {x:0,y:0},{x:35,y:0},{x:70,y:0},
    {x:0,y:18},{x:35,y:18},{x:70,y:18},
  ];
  return {
    vertices,
    uvs:new Float32Array([0,0, .5,0, 1,0, 0,1, .5,1, 1,1]),
    triangles:[[0,1,3],[3,1,4],[1,2,4],[4,2,5]],
    edgeIndices:[0,1,2,5,4,3],
  };
}
function makeTex(w,h,draw){
  const c=document.createElement('canvas'); c.width=w; c.height=h;
  const x=c.getContext('2d'); x.clearRect(0,0,w,h); draw(x,w,h); return c;
}
const tex={
  bg:makeTex(480,270,(x,w,h)=>{x.fillStyle='#f4f0f7';x.fillRect(0,0,w,h)}),
  body:makeTex(105,110,(x,w,h)=>{x.fillStyle='#8e6bb8';x.beginPath();x.roundRect(0,0,w,h,18);x.fill()}),
  head:makeTex(86,100,(x,w,h)=>{x.fillStyle='#efc4ae';x.beginPath();x.ellipse(w/2,h/2,w*.48,h*.49,0,0,Math.PI*2);x.fill()}),
  hair:makeTex(98,112,(x,w,h)=>{x.fillStyle='#4a2e55';x.beginPath();x.ellipse(w/2,42,w*.5,42,0,Math.PI,Math.PI*2);x.fill();x.fillRect(1,40,15,60);x.fillRect(w-16,40,15,60)}),
  eye:makeTex(15,7,(x,w,h)=>{x.fillStyle='#294f45';x.beginPath();x.ellipse(w/2,h/2,w*.45,h*.45,0,0,Math.PI*2);x.fill()}),
  mouth:makeTex(28,12,(x,w,h)=>{x.strokeStyle='#9f4e65';x.lineWidth=3;x.beginPath();x.arc(w/2,2,10,8,.15*Math.PI,.85*Math.PI);x.stroke()}),
  arm:makeTex(70,18,(x,w,h)=>{x.fillStyle='#efc4ae';x.beginPath();x.roundRect(0,0,w,h,8);x.fill()}),
};

const armRest=stripMesh().vertices.map(v=>({...v}));
function bentArm(angleDeg){
  const a=angleDeg*Math.PI/180, pivot={x:35,y:9};
  return armRest.map(v=>{
    if(v.x<=35) return {...v};
    const dx=v.x-pivot.x, dy=v.y-pivot.y;
    return {
      x:pivot.x + dx*Math.cos(a)-dy*Math.sin(a),
      y:pivot.y + dx*Math.sin(a)+dy*Math.cos(a)
    };
  });
}

const nodes=[
  {id:'bg',type:'part',name:'Background',parent:null,draw_order:0,opacity:1,visible:true,transform:{x:0,y:0,rotation:0,scaleX:1,scaleY:1,pivotX:0,pivotY:0},mesh:quad(480,270)},
  {id:'bodyG',type:'group',name:'BodyRig',parent:null,opacity:1,visible:true,transform:{x:0,y:0,rotation:0,scaleX:1,scaleY:1,pivotX:240,pivotY:190}},
  {id:'body',type:'part',name:'LavenderBody',parent:'bodyG',draw_order:10,opacity:1,visible:true,transform:{x:188,y:145,rotation:0,scaleX:1,scaleY:1,pivotX:52,yPivot:55,pivotY:55},mesh:quad(105,110)},
  {id:'headG',type:'group',name:'HeadRig',parent:'bodyG',opacity:1,visible:true,transform:{x:0,y:0,rotation:0,scaleX:1,scaleY:1,pivotX:240,pivotY:105}},
  {id:'hair',type:'part',name:'Hair',parent:'headG',draw_order:20,opacity:1,visible:true,transform:{x:191,y:47,rotation:0,scaleX:1,scaleY:1,pivotX:49,pivotY:56},mesh:quad(98,112)},
  {id:'head',type:'part',name:'Face',parent:'headG',draw_order:21,opacity:1,visible:true,transform:{x:197,y:58,rotation:0,scaleX:1,scaleY:1,pivotX:43,pivotY:50},mesh:quad(86,100)},
  {id:'eyeL',type:'part',name:'EyeL',parent:'headG',draw_order:22,opacity:1,visible:true,transform:{x:218,y:98,rotation:0,scaleX:1,scaleY:1,pivotX:7.5,pivotY:3.5},mesh:quad(15,7)},
  {id:'eyeR',type:'part',name:'EyeR',parent:'headG',draw_order:22,opacity:1,visible:true,transform:{x:248,y:98,rotation:0,scaleX:1,scaleY:1,pivotX:7.5,pivotY:3.5},mesh:quad(15,7)},
  {id:'mouth',type:'part',name:'Mouth',parent:'headG',draw_order:23,opacity:1,visible:true,transform:{x:226,y:124,rotation:0,scaleX:.78,scaleY:1,pivotX:14,pivotY:6},mesh:quad(28,12)},
  {id:'arm',type:'part',name:'LeftArmMesh',parent:'bodyG',draw_order:30,opacity:1,visible:true,transform:{x:274,y:155,rotation:0,scaleX:1,scaleY:1,pivotX:0,pivotY:9},mesh:stripMesh()},
];

const animation={
  id:'bench',name:'NoPantsRigBenchmark',duration:2000,fps:24,
  tracks:[
    {nodeId:'eyeL',property:'scaleY',keyframes:[{time:0,value:1,easing:'linear'},{time:420,value:1,easing:'ease-both'},{time:500,value:.08,easing:'ease-both'},{time:610,value:1,easing:'ease-both'},{time:2000,value:1,easing:'linear'}]},
    {nodeId:'eyeR',property:'scaleY',keyframes:[{time:0,value:1,easing:'linear'},{time:420,value:1,easing:'ease-both'},{time:500,value:.08,easing:'ease-both'},{time:610,value:1,easing:'ease-both'},{time:2000,value:1,easing:'linear'}]},
    {nodeId:'mouth',property:'scaleX',keyframes:[{time:0,value:.78,easing:'ease-both'},{time:900,value:1.32,easing:'ease-both'},{time:1600,value:1.12,easing:'ease-both'},{time:2000,value:.9,easing:'linear'}]},
    {nodeId:'headG',property:'y',keyframes:[{time:0,value:0,easing:'ease-both'},{time:1000,value:-5,easing:'ease-both'},{time:2000,value:0,easing:'ease-both'}]},
    {nodeId:'bodyG',property:'scaleY',keyframes:[{time:0,value:1,easing:'ease-both'},{time:1000,value:1.025,easing:'ease-both'},{time:2000,value:1,easing:'ease-both'}]},
    {nodeId:'arm',property:'mesh_verts',keyframes:[{time:0,value:armRest,easing:'ease-both'},{time:1000,value:bentArm(62),easing:'ease-both'},{time:2000,value:armRest,easing:'ease-both'}]},
  ],
};

const project={version:'benchmark',canvas:{width:480,height:270},textures:[],nodes,animations:[animation]};
const editor={view:{zoom:1,panX:0,panY:0},overlays:{showImage:true,showWireframe:false,showVertices:false,showEdgeOutline:false,irisClipping:false},selection:[],meshEditMode:false};

const textures={bg:tex.bg,body:tex.body,hair:tex.hair,head:tex.head,eyeL:tex.eye,eyeR:tex.eye,mouth:tex.mouth,arm:tex.arm};
for(const p of nodes.filter(n=>n.type==='part')){
  scene.parts.uploadMesh(p.id,p.mesh);
  scene.parts.uploadTexture(p.id,textures[p.id]);
}

function renderFrame(frameIndex){
  const timeMs=(frameIndex/24)*1000;
  const pose=computePoseOverrides(animation,timeMs,false,2000);
  for(const p of nodes.filter(n=>n.type==='part')){
    const ov=pose.get(p.id);
    scene.parts.uploadPositions(p.id,ov?.mesh_verts ?? p.mesh.vertices,p.mesh.uvs);
  }
  scene.draw(project,editor,false,pose,{skipResize:true,exportMode:true});
  const armPose=pose.get('arm')?.mesh_verts ?? armRest;
  return {
    dataUrl:canvas.toDataURL('image/png'),
    telemetry:{
      frameIndex,timeMs,
      elbowTip:{x:armPose[2].x,y:armPose[2].y},
      eyeScaleY:pose.get('eyeL')?.scaleY ?? 1,
      mouthScaleX:pose.get('mouth')?.scaleX ?? .78,
      headY:pose.get('headG')?.y ?? 0,
      bodyScaleY:pose.get('bodyG')?.scaleY ?? 1,
    }
  };
}
window.__renderBenchmarkFrame=renderFrame;
window.__benchmarkReady=true;
renderFrame(0);
