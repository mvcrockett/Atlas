import {chromium} from 'playwright';
import {mkdir,writeFile,readFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
const out='output/sprint3d';
const dir=path.join(out,'frames');await mkdir(dir,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
try{
 const page=await browser.newPage({viewport:{width:480,height:480}});
 page.on('pageerror',e=>console.error('[PAGE ERROR]',e.message));
 await page.goto('http://127.0.0.1:5173/bridge3d.html',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>window.__sprint3dReady===true);
 const telemetry=[];
 for(let i=0;i<72;i++){
  const v=await page.evaluate(i=>window.__renderS3DFrame(i),i);
  await writeFile(path.join(dir,'frame_'+String(i).padStart(4,'0')+'.png'),Buffer.from(v.dataUrl.split(',')[1],'base64'));
  telemetry.push(v.telemetry);
 }
 const manifest=await page.evaluate(()=>window.__artManifest);
 const files=(await readdir(dir)).filter(f=>f.endsWith('.png')).sort();
 const hashes=await Promise.all(files.map(async f=>createHash('sha256').update(await readFile(path.join(dir,f))).digest('hex')));
 const ff=spawnSync('ffmpeg',['-y','-loglevel','error','-framerate','24','-i',path.join(dir,'frame_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p',path.join(out,'sprint3d.mp4')],{encoding:'utf8'});
 if(ff.status!==0)throw new Error('FFmpeg: '+ff.stderr);
 const probe=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=r_frame_rate,nb_read_frames,duration','-of','json',path.join(out,'sprint3d.mp4')],{encoding:'utf8'});
 if(probe.status!==0)throw new Error('ffprobe: '+probe.stderr);
 const stream=JSON.parse(probe.stdout).streams[0];
 const max=a=>Math.max(...a),min=a=>Math.min(...a);
 const metrics={engine:'upstream Stretchy ScenePass + computePoseOverrides',art_status:manifest.status,approved:manifest.approval,
  num_layers:manifest.layers.length,frames:files.length,unique_frames:new Set(hashes).size,
  fps:stream.r_frame_rate,decoded_frames:Number(stream.nb_read_frames),duration:Number(stream.duration),
  head_y_range:max(telemetry.map(x=>x.head_y))-min(telemetry.map(x=>x.head_y)),
  blink_peak:max(telemetry.map(x=>x.blink_opacity??0)),smile_peak:max(telemetry.map(x=>x.smile_opacity??0)),
  visual_anime_quality_verified:false,paid_api_usd:0};
 await writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2));
 await writeFile(path.join(out,'telemetry.json'),JSON.stringify(telemetry,null,2));
 for(const i of [0,18,24,45,51,71]){
   await writeFile(path.join(out,'inspect_'+String(i).padStart(4,'0')+'.png'),await readFile(path.join(dir,'frame_'+String(i).padStart(4,'0')+'.png')));
 }
 if(files.length!==72||metrics.unique_frames<20||metrics.fps!=='24/1'||metrics.decoded_frames!==72||Math.abs(metrics.duration-3)>.02||metrics.head_y_range<3.5||metrics.blink_peak<.9||metrics.smile_peak<.9)
   throw new Error('Failed required motion/encoding assertions: '+JSON.stringify(metrics));
 console.log(JSON.stringify(metrics,null,2));
}finally{await browser.close();}
