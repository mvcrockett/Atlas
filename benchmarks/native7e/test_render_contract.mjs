import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {renderGeometry,privacyClass,validateStreams} from './render_contract.mjs';

test('native export keeps one source texel per pixel with even padded dimensions',()=>{
 assert.deepEqual(renderGeometry(650,650,'native'),{width:682,height:682,scale:1,x:16,y:16});
 assert.deepEqual(renderGeometry(651,701,'native'),{width:684,height:734,scale:1,x:16,y:16});
});
test('legacy framing remains compatible',()=>{
 const g=renderGeometry(650,650);assert.equal(g.width,480);assert.equal(g.height,480);assert.equal(g.scale,450/650);
});
test('bad dimensions and export modes fail',()=>{
 for(const n of [NaN,0,-1,650.1,4097,'650'])assert.throws(()=>renderGeometry(n,650,'native'));
 assert.throws(()=>renderGeometry(650,650,'other'));
});
test('private artwork can never report synthetic privacy',()=>{
 assert.equal(privacyClass('PRIVATE_CANONICAL_EXPERIMENTAL'),'PRIVATE_ARTWORK');
 assert.equal(privacyClass('SYNTHETIC_CALIBRATION_ONLY'),'SYNTHETIC_CALIBRATION_ONLY');
 assert.throws(()=>privacyClass(undefined));assert.throws(()=>privacyClass('public'));
});
const geometry=renderGeometry(650,650,'native');
const streams=[{codec_type:'video',nb_read_frames:'120',r_frame_rate:'24/1',width:682,height:682,duration:'5.000'},
 {codec_type:'audio',duration:'5.000'}];
test('decoder validation requires frame count, resolution, fps AND audio duration',()=>{
 assert.equal(validateStreams(streams,geometry).audio.duration,'5.000');
 for(const change of [{nb_read_frames:119},{r_frame_rate:'30/1'},{width:480},{duration:4.5},{duration:'NaN'}])
  assert.throws(()=>validateStreams([{...streams[0],...change},streams[1]],geometry));
 assert.throws(()=>validateStreams([streams[0]],geometry));
 assert.throws(()=>validateStreams([streams[0],{codec_type:'audio',duration:'4'}],geometry));
});
test('staged encrypted runner consumes exactly its extraction destination and audio',()=>{
 const s=readFileSync(new URL('../../.github/workflows/no-pants-7i-private-staged.yml',import.meta.url),'utf8');
 assert.match(s,/NOPANTS_ASSET_DIR: \$\{\{ runner.temp \}\}\/nopants7i-private-art/);
 assert.match(s,/cp -a "\$RUNNER_TEMP\/nopants7i-private-art\/\."/);
 assert.doesNotMatch(s,/nopants7g-private-art/);
 assert.match(s,/NOPANTS_AUDIO_PATH: \$\{\{ runner.temp \}\}\/stretchystudio\/art\/dialogue.wav/);
 assert.match(s,/render_contract.mjs/);
 assert.doesNotMatch(s,/\n  push:/);
});
