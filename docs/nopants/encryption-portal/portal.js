'use strict';
// Public, source-only browser encryption. No fetch, XHR, WebSocket, sendBeacon,
// service worker, analytics, external libraries, remote URLs, or file uploads.
const SOURCE_SHA256='6ebab335357134baefb2c64ae6c01edf0427943703beab2c252300a06f54229b';
const MAGIC=new TextEncoder().encode('NPS7I1');
const PBKDF2_ITERATIONS=600000;
const MAX_ZIP_BYTES=40*1024*1024;
const OUTPUT='NoPants_Sprint7H_ENCRYPTED_INPUT.bin';
const source=document.getElementById('source');
const password=document.getElementById('password');
const confirm=document.getElementById('confirm');
const button=document.getElementById('encrypt');
const status=document.getElementById('status');
const fileInfo=document.getElementById('file-info');

function setStatus(message,kind=''){
 status.textContent=message;
 status.className='status'+(kind?' '+kind:'');
}
function hasWebCrypto(){
 return window.isSecureContext===true &&
   !!window.crypto?.subtle &&
   typeof window.crypto.getRandomValues==='function';
}
function bytesToHex(buffer){
 return Array.from(new Uint8Array(buffer),x=>x.toString(16).padStart(2,'0')).join('');
}
function checkContext(){
 const ok=hasWebCrypto();
 button.disabled=!ok;
 if(!ok){
   setStatus('⚠️ This browser cannot use secure Web Crypto here. Open this same audited page via HTTPS in Safari. Nothing was sent or encrypted.','error');
 } else {
   setStatus('🔒 Secure Web Crypto is ready. No file has been processed.');
 }
 return ok;
}
source.addEventListener('change',()=>{
 const f=source.files?.[0];
 fileInfo.textContent=f ? 'Selected: '+f.name+' ('+f.size.toLocaleString()+' bytes)' : 'No file selected.';
});
button.addEventListener('click',async()=>{
 button.disabled=true;
 try{
  if(!hasWebCrypto())throw new Error('Secure Web Crypto unavailable; nothing encrypted.');
  const file=source.files?.[0];
  if(!file||!file.name.toLowerCase().endsWith('.zip'))throw new Error('Choose the original heroine ZIP first.');
  if(file.size>MAX_ZIP_BYTES)throw new Error('ZIP exceeds the 40 MiB safety limit.');
  const pass=password.value;
  if(pass.length<24)throw new Error('Create and save a unique password of at least 24 characters first.');
  if(pass!==confirm.value)throw new Error('Password confirmation does not match.');
  setStatus('🔍 Checking the original heroine ZIP identity locally…');
  const plaintext=await file.arrayBuffer();
  if(bytesToHex(await crypto.subtle.digest('SHA-256',plaintext))!==SOURCE_SHA256){
    throw new Error('This is not the exact verified original Sprint 7F ZIP. No output created.');
  }
  setStatus('🔐 Encrypting privately on this device…');
  const salt=crypto.getRandomValues(new Uint8Array(16));
  const nonce=crypto.getRandomValues(new Uint8Array(12));
  const rawPassword=new TextEncoder().encode(pass);
  const material=await crypto.subtle.importKey('raw',rawPassword,'PBKDF2',false,['deriveKey']);
  rawPassword.fill(0);
  const key=await crypto.subtle.deriveKey(
   {name:'PBKDF2',salt,iterations:PBKDF2_ITERATIONS,hash:'SHA-256'},
   material,{name:'AES-GCM',length:256},false,['encrypt']);
  const cipher=await crypto.subtle.encrypt({name:'AES-GCM',iv:nonce,tagLength:128},key,plaintext);
  const envelope=new Blob([MAGIC,salt,nonce,cipher],{type:'application/octet-stream'});
  const objectURL=URL.createObjectURL(envelope);
  const link=document.createElement('a');
  link.href=objectURL;link.download=OUTPUT;link.rel='noopener';
  document.body.appendChild(link);link.click();link.remove();
  window.setTimeout(()=>URL.revokeObjectURL(objectURL),60000);
  setStatus('✅ Encrypted file created locally ('+envelope.size.toLocaleString()+' bytes). Save '+OUTPUT+' to Files. Keep your recovery password in Apple Passwords. Nothing was uploaded.','ok');
 }catch(error){
  setStatus('⚠️ '+String(error?.message||'Unable to encrypt')+' Nothing was uploaded.','error');
 }finally{
  password.value='';confirm.value='';
  button.disabled=!hasWebCrypto();
 }
});
checkContext();
