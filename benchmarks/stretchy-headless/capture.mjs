import { chromium } from 'playwright';
import { mkdir, writeFile, readFile, readdir } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { spawnSync } from 'node:child_process';
import path from 'node:path';

const url=process.argv[2] || 'http://127.0.0.1:5173/benchmark.html';
const out=process.argv[3] || 'output/stretchy-headless';
const frames=path.join(out,'frames');
await mkdir(frames,{recursive:true});

const browser=await chromium.launch({
  headless:true,
  args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']
});
const page=await browser.newPage({viewport:{width:480,height:270}});
page.on('console',m=>console.log('[browser]',m.type(),m.text()));
await page.goto(url,{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.__benchmarkReady===true);

const telemetry=[];
for(let i=0;i<48;i++){
  const result=await page.evaluate(i=>window.__renderBenchmarkFrame(i),i);
  const b64=result.dataUrl.replace(/^data:image\/png;base64,/,'');
  await writeFile(path.join(frames,`frame_${String(i).padStart(4,'0')}.png`),Buffer.from(b64,'base64'));
  telemetry.push(result.telemetry);
}
await browser.close();

const pngs=(await readdir(frames)).filter(x=>x.endsWith('.png')).sort();
if(pngs.length!==48) throw new Error(`Expected 48 frames, got ${pngs.length}`);

const hashes=[];
for(const f of pngs){
  hashes.push(createHash('sha256').update(await readFile(path.join(frames,f))).digest('hex'));
}
const uniqueFrames=new Set(hashes).size;

const ff=spawnSync('ffmpeg',['-y','-loglevel','error','-framerate','24','-i',path.join(frames,'frame_%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p',path.join(out,'stretchy-headless.mp4')],{encoding:'utf8'});
if(ff.status!==0) throw new Error(ff.stderr || 'ffmpeg failed');
const probe=spawnSync('ffprobe',['-v','error','-count_frames','-select_streams','v:0','-show_entries','stream=r_frame_rate,nb_read_frames,duration','-of','json',path.join(out,'stretchy-headless.mp4')],{encoding:'utf8'});
if(probe.status!==0) throw new Error(probe.stderr || 'ffprobe failed');
const ffprobe=JSON.parse(probe.stdout);
const stream=ffprobe.streams[0];

const ys=telemetry.map(t=>t.elbowTip.y);
const blinkMin=Math.min(...telemetry.map(t=>t.eyeScaleY));
const smileMax=Math.max(...telemetry.map(t=>t.mouthScaleX));
const elbowRange=Math.max(...ys)-Math.min(...ys);
const headRange=Math.max(...telemetry.map(t=>t.headY))-Math.min(...telemetry.map(t=>t.headY));
const bodyRange=Math.max(...telemetry.map(t=>t.bodyScaleY))-Math.min(...telemetry.map(t=>t.bodyScaleY));

const metrics={
  engine:'Stretchy Studio ScenePass + animationEngine',
  upstream_commit:'24a83a27ba43e43e9d2e3de5e33994594e6199c2',
  fps:24,
  expected_frames:48,
  actual_frames:pngs.length,
  unique_frame_hashes:uniqueFrames,
  ffprobe:stream,
  blink_min_scale_y:blinkMin,
  smile_max_scale_x:smileMax,
  elbow_tip_y_range_px:elbowRange,
  head_y_range_px:headRange,
  body_scale_y_range:bodyRange,
  paid_api_usd:0,
  generative_ai_used:false,
  placeholder_art:true,
};
await writeFile(path.join(out,'telemetry.json'),JSON.stringify(telemetry,null,2));
await writeFile(path.join(out,'metrics.json'),JSON.stringify(metrics,null,2));

if(stream.r_frame_rate!=='24/1') throw new Error(`Wrong fps ${stream.r_frame_rate}`);
if(Number(stream.nb_read_frames)!==48) throw new Error(`Wrong video frame count ${stream.nb_read_frames}`);
if(uniqueFrames<12) throw new Error(`Insufficient motion; unique frames=${uniqueFrames}`);
if(blinkMin>.2) throw new Error(`Blink failed: min scaleY=${blinkMin}`);
if(smileMax<1.2) throw new Error(`Smile failed: max scaleX=${smileMax}`);
if(elbowRange<30) throw new Error(`Elbow mesh deformation too small: ${elbowRange}px`);
if(headRange<3) throw new Error(`Head motion too small: ${headRange}px`);
if(bodyRange<.015) throw new Error(`Breathing motion too small: ${bodyRange}`);
console.log(JSON.stringify(metrics,null,2));
