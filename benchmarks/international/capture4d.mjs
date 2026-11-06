// Sprint 4D: real 768px original anime art, two native engines, 72 deterministic frames.
import {chromium} from 'playwright';
import {PNG} from 'pngjs';
import {mkdir,writeFile,readFile} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
const kind=process.argv[2];
if(!['japanese','stretchy'].includes(kind))throw Error('Usage: node capture4d.mjs japanese|stretchy');
const out=path.join('output','4d-'+kind);
const framesDir=path.join(out,'frames');
await mkdir(framesDir,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
const errors=[];
try {
 const page=await browser.newPage({viewport:{width:1000,height:950}});
 page.on('pageerror',e=>errors.push(e.message));
 if(kind==='japanese'){
   await page.goto('http://127.0.0.1:8000/',{waitUntil:'domcontentloaded'});
   await page.locator('[data-sample="A"]').first().click();
   await page.waitForFunction(()=>window.__nopants4dReady && window.Anime25D?.state?.().layers>2,{timeout:120000});
 } else {
   await page.goto('http://127.0.0.1:5173/psd4d.html',{waitUntil:'domcontentloaded'});
   await page.waitForFunction(()=>window.__psdReady===true,{timeout:120000});
 }
 const source = kind==='stretchy' ? await page.evaluate(()=>window.__psdHeader) : await page.evaluate(()=>window.Anime25D.state());
 const frames=[],telemetry=[],hashes=[];
 let prior=null, sumdiff=0, maxdiff=0, changes=0, allzero=0;
 for(let i=0;i<72;i++){
   const result=await page.evaluate(([k,i])=>k==='japanese'?window.__nopants4dStep(i):window.__renderPSDFrame(i),[kind,i]);
   const buf=Buffer.from(result.dataUrl.split(',')[1],'base64');
   const frame=PNG.sync.read(buf);
   if(frame.width!==768||frame.height!==768)throw Error('Expected 768x768 frame: '+frame.width+'x'+frame.height);
   if(prior){
     let d=0;for(let j=0;j<frame.data.length;j+=4){d+=Math.abs(frame.data[j]-prior.data[j])+Math.abs(frame.data[j+1]-prior.data[j+1])+Math.abs(frame.data[j+2]-prior.data[j+2]);}
     d/=frame.width*frame.height*3;sumdiff+=d;maxdiff=Math.max(maxdiff,d);if(d>0.015)changes++;
   }
   // White/transparent all-empty rendering is not a successful anime benchmark.
   let nonwhite=0;
   for(let j=0;j<frame.data.length;j+=4)if(frame.data[j]<235||frame.data[j+1]<235||frame.data[j+2]<235)nonwhite++;
   if(nonwhite/(frame.width*frame.height)<.1)allzero++;
   const dest=path.join(framesDir,'frame_'+String(i).padStart(4,'0')+'.png');
   await writeFile(dest,buf);
   hashes.push(createHash('sha256').update(buf).digest('hex'));
   telemetry.push({frame:i,blink:result.blink??null,mouth:result.mouth??result.mouthOpen??null,head:result.head_y??result.headSway??null});
   prior=frame;
 }
 const ff=spawnSync('ffmpeg',['-y','-loglevel','error','-framerate','24','-i',path.join(framesDir,'frame_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p',path.join(out,kind+'.mp4')],{encoding:'utf8'});
 if(ff.status!==0)throw Error('ffmpeg failure '+ff.stderr);
 const probe=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,r_frame_rate,duration','-of','json',path.join(out,kind+'.mp4')],{encoding:'utf8'});
 if(probe.status!==0)throw Error('ffprobe failure '+probe.stderr);
 const stream=JSON.parse(probe.stdout).streams[0];
 const montage=spawnSync('ffmpeg',['-y','-loglevel','error','-i',path.join(out,kind+'.mp4'),'-vf','select=not(mod(n\\,12)),scale=384:384,tile=3x2','-frames:v','1',path.join(out,kind+'_montage.png')],{encoding:'utf8'});
 if(montage.status!==0)throw Error('montage failure '+montage.stderr);
 const metrics={engine:kind,asset:'original 768x768 lavender-hair layered anime portrait, not private heroine',origin:'original authored in Sprint 4D',psd_was_created_by_ag_psd:true,frames:72,encoded_fps:stream.r_frame_rate,encoded_frames:Number(stream.nb_read_frames),duration_s:Number(stream.duration),unique_frames:new Set(hashes).size,changed_intervals_above_rgb_threshold:changes,mean_absolute_frame_rgb_change:sumdiff/71,max_absolute_frame_rgb_change:maxdiff,empty_frames:allzero,driver:'sequential fixed frame index /24; original animation and render engines',control_timing:'3 seconds with blink at .75 and 2.125 and mouth change ~1.8',source_layer_count:source.parsed_layers??source.layers,source_nonempty_layers:source.nonempty_layers??null,page_errors:errors,visual_inspection_pending:true};
 await writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2));
 await writeFile(path.join(out,'telemetry.json'),JSON.stringify(telemetry,null,2));
 console.log('Sprint 4D',kind,JSON.stringify(metrics));
 if(metrics.encoded_fps!=='24/1'||metrics.encoded_frames!==72||metrics.unique_frames<20||metrics.empty_frames>0)throw Error('Not enough valid animation frames');
}finally{await browser.close();}
