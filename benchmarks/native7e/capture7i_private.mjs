import {chromium} from 'playwright';
import {mkdir,writeFile,readFile,readdir} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
// Private 7I capture: encrypted evidence follows. No public output files.
const out='output/nopants7e',frameDir=path.join(out,'frames');
await mkdir(frameDir,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
try{
 const page=await browser.newPage({viewport:{width:480,height:480}});
 let pageErrors=[];page.on('pageerror',e=>pageErrors.push(e.message));
 await page.goto('http://127.0.0.1:5173/bridge7e.html',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>window.__s7eReady===true);
 const telemetry=[];
 for(let i=0;i<120;i++){
  const v=await page.evaluate(i=>window.__renderS7EFrame(i),i);
  await writeFile(path.join(frameDir,'frame_'+String(i).padStart(4,'0')+'.png'),Buffer.from(v.dataUrl.split(',')[1],'base64'));
  telemetry.push(v.telemetry);
 }
 if(pageErrors.length)throw Error('WebGL page errors: '+pageErrors.join(' | '));
 const files=(await readdir(frameDir)).filter(x=>x.endsWith('.png')).sort();
 const hashes=await Promise.all(files.map(async f=>createHash('sha256').update(await readFile(path.join(frameDir,f))).digest('hex')));
 const audio='art/dialogue.wav';
 let cmd=['-y','-loglevel','error','-framerate','24','-i',path.join(frameDir,'frame_%04d.png')];
 cmd.push('-i',audio,'-t','5','-c:v','libx264','-pix_fmt','yuv420p','-crf','22','-c:a','aac','-af','apad=whole_dur=5','-movflags','+faststart',path.join(out,'native7e.mp4'));
 const ff=spawnSync('ffmpeg',cmd,{encoding:'utf8'});if(ff.status!==0)throw Error('FFmpeg failed: '+ff.stderr);
 const probe=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=r_frame_rate,nb_read_frames,duration','-of','json',path.join(out,'native7e.mp4')],{encoding:'utf8'});
 if(probe.status!==0)throw Error('ffprobe failed');
 const s=JSON.parse(probe.stdout).streams[0];
 const metrics={engine:'native Stretchy ScenePass + computePoseOverrides',art_status:await page.evaluate(()=>window.__s7eManifestStatus),
  frames:files.length,decoded_frames:Number(s.nb_read_frames),fps:s.r_frame_rate,duration:Number(s.duration),
  unique_frames:new Set(hashes).size,mouth_states:[...new Set(telemetry.map(t=>t.mouth))],blink_frames:telemetry.filter(t=>t.blink).length,
  privacy_class:'PRIVATE_CANONICAL_EXPERIMENTAL',private_heroine_native_verified:false};
 if(files.length!==120||metrics.decoded_frames!==120||metrics.fps!=='24/1'||Math.abs(metrics.duration-5)>0.05||metrics.unique_frames<15||metrics.mouth_states.length<2||metrics.blink_frames<2)throw Error('Failed required tests: '+JSON.stringify(metrics));
 await writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2));
 for(const n of [0,18,39,62,89,119])await writeFile(path.join(out,'inspect_'+String(n).padStart(4,'0')+'.png'),await readFile(path.join(frameDir,'frame_'+String(n).padStart(4,'0')+'.png')));
 console.log(JSON.stringify(metrics));
}finally{await browser.close();}
