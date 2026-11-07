"""Decrypt NPS7I1 input from a trusted owner-configured HTTPS link, then validate the
7F canonical experimental ZIP in-memory. Never log art, URL or passphrase."""
import hashlib, hmac, os, pathlib, sys, urllib.request, urllib.parse
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'nopants7f'))
from private_transport import verify_bundle
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/"nopants7g"))
from https_download import fetch_https
MAGIC=b'NPS7I1'
MAX_CIPHERTEXT=45*1024*1024
ITERATIONS=600000

def decrypt_blob(blob,password,expected_plain_sha256):
    if not isinstance(blob,bytes) or len(blob)<50 or len(blob)>MAX_CIPHERTEXT:
        raise ValueError('invalid encrypted size')
    if not blob.startswith(MAGIC):raise ValueError('unknown private envelope')
    if not password or len(expected_plain_sha256)!=64:
        raise ValueError('missing private input credentials')
    try:bytes.fromhex(expected_plain_sha256)
    except ValueError as exc:raise ValueError('invalid expected SHA256') from exc
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key=hashlib.pbkdf2_hmac('sha256',password.encode('utf-8'),blob[6:22],ITERATIONS,32)
    try:plain=AESGCM(key).decrypt(blob[22:34],blob[34:],None)
    except Exception as exc:raise ValueError('input authentication failed') from exc
    if not hmac.compare_digest(hashlib.sha256(plain).hexdigest(),expected_plain_sha256.lower()):
        raise ValueError('plaintext bundle digest mismatch')
    return plain

def fetch_ciphertext(url):
    return fetch_https(url,MAX_CIPHERTEXT,"NoPants-Private-Runner-7I")

def ingest(url,password,expected_plain_sha256,dest):
    raw=decrypt_blob(fetch_ciphertext(url),password,expected_plain_sha256)
    return verify_bundle(raw,expected_plain_sha256,dest)

def main():
    url=os.environ.get('NOPANTS_ART_BUNDLE_URL','')
    pwd=os.environ.get('NOPANTS_INPUT_PASSPHRASE','')
    digest=os.environ.get('NOPANTS_ART_BUNDLE_SHA256','')
    dest=os.environ.get('NOPANTS_ASSET_DIR','')
    if not all((url,pwd,digest,dest,os.environ.get('NOPANTS_EVIDENCE_KEY_HEX'))):
        raise SystemExit('Private input secrets not configured. No art was downloaded.')
    try:
        result=ingest(url,pwd,digest,dest)
    except Exception:
        raise SystemExit('Private encrypted ingress failed closed. No secrets or art logged.') from None
    print('PASS: owner-encrypted input authenticated and validated in private runner; no art publicly uploaded.')

if __name__=='__main__':main()
