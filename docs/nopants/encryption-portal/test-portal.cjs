// Automated browser contract using synthetic file only.
// The hash constant is overridden ONLY in Playwright's test HTTP response;
// production portal.js is never modified or provided private input.
const {chromium}=require('playwright');
const crypto=require('node:crypto');
const fs=require('node:fs');
const path=require('node:path');
(async()=>{
 const data=Buffer.from('SYNTHETIC NO-PANTS PORTAL TEST FIXTURE - NO USER ART 2026');
 const sha=crypto.createHash('sha256').update(data).digest('hex');
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const port=process.env.NOPANTS_TEST_PORT||'8765';
 const url='http://127.0.0.1:'+port+'/docs/nopants/encryption-portal/index.html';
 let errors=[];
 try{
  const page=await browser.newPage({viewport:{width:390,height:844},acceptDownloads:true});
  page.on('request',req=>{
    const target=new URL(req.url());
    if(!['127.0.0.1','localhost'].includes(target.hostname) || req.method()!=='GET'){
      errors.push('Forbidden request: '+req.method()+' '+target.hostname);
    }
  });
  page.on('pageerror',e=>errors.push('Browser JS: '+e.message));
  await page.route('**/portal.js',async route=>{
    const original=fs.readFileSync(path.join(__dirname,'portal.js'),'utf8');
    if(!original.includes('const SOURCE_SHA256='))throw Error('Hash override target missing');
    const patched=original.replace(/const SOURCE_SHA256='[a-f0-9]{64}';/, "const SOURCE_SHA256='"+sha+"';");
    await route.fulfill({status:200,contentType:'application/javascript',body:patched});
  });
  await page.goto(url,{waitUntil:'networkidle'});
  if(!await page.evaluate(()=>window.isSecureContext&&!!crypto.subtle))throw Error('Localhost secure context lacks WebCrypto');
  if(!await page.locator('#encrypt').isEnabled())throw Error('Encryption control unavailable');
  await page.screenshot({path:path.join(process.cwd(),'portal-preview.png'),fullPage:true});
  await page.locator('#source').setInputFiles({name:'synthetic-fixture.zip',mimeType:'application/zip',buffer:data});
  const password='SYNTHETIC-STRONG-TEST-PASSPHRASE-ONLY-1234';
  await page.locator('#password').fill(password);
  await page.locator('#confirm').fill(password);
  const dl=page.waitForEvent('download');
  await page.locator('#encrypt').click();
  const download=await dl;
  if(download.suggestedFilename()!=='NoPants_Sprint7H_ENCRYPTED_INPUT.bin')throw Error('Unexpected output name');
  const dest=path.join(process.cwd(),'portal-synthetic-output.bin');
  await download.saveAs(dest);
  const encrypted=fs.readFileSync(dest);
  if(encrypted.subarray(0,6).toString()!=='NPS7I1')throw Error('Wrong header');
  const salt=encrypted.subarray(6,22),iv=encrypted.subarray(22,34);
  const key=crypto.pbkdf2Sync(password,salt,600000,32,'sha256');
  const payload=encrypted.subarray(34);
  const decipher=crypto.createDecipheriv('aes-256-gcm',key,iv);
  decipher.setAuthTag(payload.subarray(payload.length-16));
  const decoded=Buffer.concat([decipher.update(payload.subarray(0,-16)),decipher.final()]);
  if(!decoded.equals(data))throw Error('Browser output could not be decrypted');
  let wrongRejected=false;
  try{
    const bad=crypto.createDecipheriv('aes-256-gcm',crypto.pbkdf2Sync('wrong',salt,600000,32,'sha256'),iv);
    bad.setAuthTag(payload.subarray(payload.length-16));bad.update(payload.subarray(0,-16));bad.final();
  }catch(e){wrongRejected=true}
  if(!wrongRejected)throw Error('Wrong password accepted');
  if(errors.length)throw Error(errors.join(' | '));
  if(!await page.locator('#status').innerText().then(t=>t.includes('Nothing was uploaded')))throw Error('Wrong success status');
  fs.rmSync(dest);
  console.log(JSON.stringify({result:'PASS',test_art:'synthetic_only',viewport:'390x844',secure_context:true,encrypted_file_bytes:encrypted.length,cipher_format:'NPS7I1',aes_gcm:true,wrong_password_rejected:true,external_requests:0,non_get_requests:0,private_heroine_used:false,actual_iphone_safari_verified:false}));
 }finally{await browser.close()}
})().catch(e=>{console.error('FAIL: '+e.message);process.exitCode=1});
