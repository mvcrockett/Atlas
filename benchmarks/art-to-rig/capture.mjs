import {chromium} from 'playwright';
import {mkdir,writeFile,readFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
const url=process.argv[2]||'http://127.0.0.1:5173/bridge.html';
const out=process.argv[3]||'output/art-to-rig';
const dir=path.join(out,'frames');await mkdir(dir,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
try{
 const page=await browser.newPage({viewport:{width:480,height:480}});
 page.on('pageerror',e=>console.error('[PAGE ERROR]',e.message));
 await page.goto(url,{waitUntil:'networkidle'});
 await page.waitForFunction(()=>window.__bridgeReady===true);
 const telemetry=[];
 for(let i=0;i<48;i++){
  const value=await page.evaluate(i=>window.__renderBridgeFrame(i),i);
  await writeFile(path.join(dir,`frame_${String(i).padStart(4,'0')}.png`),Buffer.from(value.dataUrl.split(',')[1],'base64'));
  telemetry.push(value.telemetry);
 }
 const manifest=await page.evaluate(()=>window.__artManifest);
 const files=(await readdir(dir)).filter(f=>f.endsWith('.png')).sort();
 const hashes=await Promise.all(files.map(async f=>createHash('sha256').update(await readFile(path.join(dir,f))).digest('hex')));
 const ff=spawnSync('ffmpeg',['-y','-loglevel','error','-framerate','24','-i',path.join(dir,'frame_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p',path.join(out,'art-to-rig.mp4')],{encoding:'utf8'});
 if(ff.status!==0)throw new Error('FFmpeg: '+ff.stderr);
 const probe=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=r_frame_rate,nb_read_frames,duration','-of','json',path.join(out,'art-to-rig.mp4')],{encoding:'utf8'});
 if(probe.status!==0)throw new Error('ffprobe: '+probe.stderr);
 const stream=JSON.parse(probe.stdout).streams[0];
 const distinct=new Set(hashes).size;
 const metrics={engine:'Stretchy Studio ScenePass + computePoseOverrides',bridge:'textured layer manifest',art_status:manifest.status,art_approval:manifest.approval,frames:files.length,unique_frames:distinct,fps:stream.r_frame_rate,decoded_frames:stream.nb_read_frames,duration:stream.duration,head_motion_range:Math.max(...telemetry.map(x=>x.headY))-Math.min(...telemetry.map(x=>x.headY)),breathing_range:Math.max(...telemetry.map(x=>x.torsoScaleY))-Math.min(...telemetry.map(x=>x.torsoScaleY)),eye_mouth_arm_anatomy_verified:false,anime_visual_quality_verified:false,paid_api_usd:0};
 await writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2));
 for(const i of [0,12,24,36,47]) await writeFile(path.join(out,`inspect_${String(i).padStart(4,'0')}.png`),await readFile(path.join(dir,`frame_${String(i).padStart(4,'0')}.png`)));
 if(files.length!==48||stream.r_frame_rate!=='24/1'||Number(stream.nb_read_frames)!==48||distinct<10||metrics.head_motion_range<5)throw new Error('Verification failed: '+JSON.stringify(metrics));
 console.log(JSON.stringify(metrics,null,2));
}finally{await browser.close();}
