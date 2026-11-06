// Japanese Anime2.5DRig CPU/WebGL1 headless motion benchmark.
// Same ephemeral third-party sample2.psd used by Stretchy 4B.
import {chromium} from 'playwright';
import {mkdir,writeFile,readdir,readFile,rm} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import path from 'node:path';

const url='http://127.0.0.1:8000/';
const out='output/4c-japanese';
const privateDir=path.join(out,'private-frames');
await mkdir(privateDir,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
let metrics={engine:'852wa/Anime2.5DRig native auto-rigger, WebGL1',source:'upstream public sample2.psd',rights:'third-party sample artwork; no media redistribution or public image artifacts',visual_inspection:false};
try{
 const page=await browser.newPage({viewport:{width:1280,height:900}});
 let errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 await page.goto(url,{waitUntil:'domcontentloaded'});
 await page.locator('[data-sample="A"]').first().click();
 await page.waitForFunction(()=>{const m=document.getElementById('modelName');return m&&m.textContent.includes('sample2.psd');},{timeout:90000});
 await page.waitForTimeout(400);
 const canvas=page.locator('#cv');
 const sizes=await canvas.evaluate(el=>[el.width,el.height]);
 const bytes=[];
 let started=Date.now();
 for(let i=0;i<72;i++){
   // Browser's own animation timeline advances via requestAnimationFrame.
   // Capture pacing is approximate, not guaranteed exactly 24Hz.
   await page.waitForTimeout(42);
   const png=await canvas.screenshot({type:'png'});
   bytes.push(png);
   await writeFile(path.join(privateDir,'frame_'+String(i).padStart(4,'0')+'.png'),png);
 }
 const durationMillis=Date.now()-started;
 const unique=new Set(bytes.map(b=>createHash('sha256').update(b).digest('hex'))).size;
 const ff=spawnSync('ffmpeg',['-y','-loglevel','error','-framerate','24','-i',path.join(privateDir,'frame_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p',path.join(privateDir,'japan_rig.mp4')],{encoding:'utf8'});
 if(ff.status!==0)throw new Error('ffmpeg: '+ff.stderr+' '+ff.error);
 const prob=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=r_frame_rate,nb_read_frames,duration','-of','json',path.join(privateDir,'japan_rig.mp4')],{encoding:'utf8'});
 if(prob.status!==0)throw new Error('ffprobe: '+prob.stderr);
 const stream=JSON.parse(prob.stdout).streams[0];
 metrics={...metrics,loaded_model:'sample2.psd',canvas_dimensions:sizes,captured_frames:bytes.length,unique_frame_hashes:unique,capture_elapsed_seconds:durationMillis/1000,capture_mode:'non-deterministic live rAF sampled by browser screenshots; encoded at 24fps',encoded_frames:Number(stream.nb_read_frames),output_fps:stream.r_frame_rate,output_duration:Number(stream.duration),page_errors:errors,actual_look_verified:false,autorig_fired:true,video_kept_private:false};
 await writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2));
 if(metrics.captured_frames!==72||metrics.encoded_frames!==72||metrics.output_fps!=='24/1'||unique<15)throw new Error('Auto-rig animation fails basic movement verification: '+JSON.stringify(metrics));
 console.log('Japanese auto-rig nonvisual metrics:',JSON.stringify({unique,frames:72,encoded_fps:metrics.output_fps,elapsed:metrics.capture_elapsed_seconds}));
}finally{await browser.close();await rm(privateDir,{recursive:true,force:true});}
