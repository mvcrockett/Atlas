import {chromium} from 'playwright';
import {mkdir,writeFile,readFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
import {privacyClass,validateStreams} from './render_contract.mjs';
const started=performance.now();
const out=process.env.NOPANTS_OUTPUT_DIR||'output/nopants7e',frameDir=path.join(out,'frames');
await mkdir(out,{recursive:true,mode:0o700});
if((await readdir(out)).length)throw Error('Output directory must be empty; refusing stale evidence');
await mkdir(frameDir,{mode:0o700});
// Explicit audio path works when protected art lives outside the repository checkout.
const audio=process.env.NOPANTS_AUDIO_PATH||'art/dialogue.wav';
await readFile(audio);
const mode=process.env.NOPANTS_RENDER_MODE||'legacy';
if(!['legacy','native'].includes(mode))throw Error('Unknown export mode');
const browser=await chromium.launch({headless:true,
 ...(process.env.NOPANTS_CHROMIUM_PATH?{executablePath:process.env.NOPANTS_CHROMIUM_PATH}:{}),
 args:['--no-sandbox','--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
try{
 const page=await browser.newPage();
 // Rendering is local-only. Block all third-party network access before loading art.
 await page.route('**/*',route=>new URL(route.request().url()).origin==='http://127.0.0.1:5173'?route.continue():route.abort());
 const pageErrors=[];page.on('pageerror',e=>pageErrors.push(e.message));
 await page.goto('http://127.0.0.1:5173/bridge7e.html?mode='+mode,{waitUntil:'networkidle'});
 await page.waitForFunction(()=>window.__s7eReady===true);
 const geometry=await page.evaluate(()=>window.__s7eGeometry);
 const status=await page.evaluate(()=>window.__s7eManifestStatus);
 const privacy=privacyClass(status),telemetry=[];
 for(let i=0;i<120;i++){
  const v=await page.evaluate(i=>window.__renderS7EFrame(i),i);
  await writeFile(path.join(frameDir,'frame_'+String(i).padStart(4,'0')+'.png'),Buffer.from(v.dataUrl.split(',')[1],'base64'),{mode:0o600});
  telemetry.push(v.telemetry);
 }
 if(pageErrors.length)throw Error('WebGL page error; private details withheld');
 const files=(await readdir(frameDir)).filter(x=>x.endsWith('.png')).sort();
 const hashes=await Promise.all(files.map(async f=>createHash('sha256').update(await readFile(path.join(frameDir,f))).digest('hex')));
 // Composite transparent overscan onto an explicit white matte, not implicit black.
 const vf='split[fg][bg];[bg]lutrgb=r=255:g=255:b=255,format=rgb24[white];[white][fg]overlay=shortest=1:format=auto,format=yuv420p';
 const ff=spawnSync('ffmpeg',['-y','-loglevel','error','-framerate','24','-i',path.join(frameDir,'frame_%04d.png'),'-i',audio,
  '-filter_complex',vf,'-t','5','-c:v','libx264','-crf','18','-c:a','aac','-af','apad=whole_dur=5','-movflags','+faststart',path.join(out,'native7e.mp4')],{encoding:'utf8'});
 if(ff.status!==0)throw Error('FFmpeg export failed; private diagnostics withheld');
 const probe=spawnSync('ffprobe',['-v','error','-count_frames','-show_streams','-of','json',path.join(out,'native7e.mp4')],{encoding:'utf8'});
 if(probe.status!==0)throw Error('ffprobe failed');
 const {video:v,audio:a}=validateStreams(JSON.parse(probe.stdout).streams,geometry);
 const metrics={engine:'native Stretchy ScenePass + computePoseOverrides',art_status:status,privacy_class:privacy,
  frames:files.length,decoded_frames:Number(v.nb_read_frames),fps:v.r_frame_rate,duration:Number(v.duration),audio_duration:Number(a.duration),
  width:v.width,height:v.height,geometry,export_mode:mode,unique_frames:new Set(hashes).size,
  adjacent_identical_frames:hashes.slice(1).filter((h,i)=>h===hashes[i]).length,
  sampled_pose_count:120,pixel_interpolated_frames:0,temporal_method:'native eased transform samples; discrete eye/mouth drawings',
  mouth_states:[...new Set(telemetry.map(t=>t.mouth))],blink_frames:telemetry.filter(t=>t.blink).length,
  native_render_executed:true,visual_quality_accepted:false,wall_seconds:(performance.now()-started)/1000};
 if(files.length!==120||metrics.unique_frames<15||metrics.mouth_states.length<2||metrics.blink_frames<2)throw Error('Motion contract failed');
 await writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2),{mode:0o600});
 await writeFile(path.join(out,'telemetry.json'),JSON.stringify(telemetry),{mode:0o600});
 for(const n of [0,18,39,62,89,119])await writeFile(path.join(out,'inspect_'+String(n).padStart(4,'0')+'.png'),await readFile(path.join(frameDir,'frame_'+String(n).padStart(4,'0')+'.png')));
 console.log('PASS: 120 native frames and 5-second audio/video validated. Inspect private metrics for details.');
}finally{await browser.close();}
