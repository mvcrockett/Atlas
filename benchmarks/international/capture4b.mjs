import {chromium} from 'playwright';
import {mkdir,writeFile,readFile,readdir,rm} from 'node:fs/promises';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
const out='output/sprint4b',temp=path.join(out,'PRIVATE_FRAMES_NOT_FOR_UPLOAD');
await mkdir(temp,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
try {
 const page=await browser.newPage({viewport:{width:480,height:480}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:5173/psd4b.html',{waitUntil:'domcontentloaded'});
 await page.waitForFunction(()=>window.__psdReady===true,{timeout:120000});
 const header=await page.evaluate(()=>window.__psdHeader);
 if(header.parsed_layers<3||header.nonempty_layers<3)throw new Error('Insufficient real PSD layers '+header.parsed_layers);
 const hashes=[], head=[];
 for(let i=0;i<48;i++){
   const r=await page.evaluate(i=>window.__renderPSDFrame(i),i);
   const bytes=Buffer.from(r.dataUrl.split(',')[1],'base64');
   await writeFile(path.join(temp,'frame_'+String(i).padStart(4,'0')+'.png'),bytes);
   hashes.push(createHash('sha256').update(bytes).digest('hex'));
   head.push(r.head_y);
 }
 const ff=spawnSync('ffmpeg',['-y','-loglevel','error','-framerate','24','-i',path.join(temp,'frame_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p',path.join(temp,'internal-only.mp4')],{encoding:'utf8'});
 if(ff.status!==0)throw new Error('FFmpeg failed '+ff.stderr+' '+ff.error);
 const prob=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=nb_read_frames,r_frame_rate,duration','-of','json',path.join(temp,'internal-only.mp4')],{encoding:'utf8'});
 if(prob.status!==0)throw new Error('ffprobe failed '+prob.stderr);
 const s=JSON.parse(prob.stdout).streams[0];
 const metrics={purpose:'4B ephemeral third-party sample PSD import, not See-through-output provenance',native_stretchy:true,art_is_not_user_art:true,visual_review_completed:false,rights:'source artist rights not established; no media published',parsed_layers:header.parsed_layers,nonempty_layers:header.nonempty_layers,tagged_layers:header.tagged_layers,character_format_detected:header.character_format_detected,organizer_groups:header.organizer_groups,layer_tags:header.layer_properties.map(x=>({tag:x.tag,coverage_ratio:+x.alpha_coverage_ratio.toFixed(4),nonempty_pixels:x.nonempty_pixels})),frames:48,unique_hashes:new Set(hashes).size,fps:s.r_frame_rate,decoded_frames:Number(s.nb_read_frames),duration:Number(s.duration),head_motion_range:Math.max(...head)-Math.min(...head),js_errors:errors,frame_images_stored_publicly:false,video_stored_publicly:false};
 await writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2));
 console.log('Nonvisual metadata only:',JSON.stringify({layers:metrics.parsed_layers,nonempty:metrics.nonempty_layers,tags:metrics.tagged_layers,frames:48,unique:metrics.unique_hashes,fps:metrics.fps,head_motion_range:metrics.head_motion_range}));
 if(s.r_frame_rate!=='24/1'||Number(s.nb_read_frames)!==48||metrics.unique_hashes<12||metrics.head_motion_range<5)throw new Error('Motion or encode assertions failed');
} finally {await browser.close();await rm(temp,{recursive:true,force:true});}
