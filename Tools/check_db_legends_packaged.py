"""Verify the active installer entries in the signed phone APK."""
import hashlib,json,re,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
apk=ROOT/'dist/7DS-Offline-Client.apk'
with zipfile.ZipFile(apk) as z:
 assert z.read('lib/arm64-v8a/libil2cpp.so')==(ROOT/'Original-APK/libil2cpp.phone-local.so').read_bytes()
 smali=(ROOT/'Research/PhoneClientDecoded/smali_classes5/com/phoenix/offline/CustomAssets.smali').read_text()
 rows=json.loads((ROOT/'dist/kaneki-assets/assets.json').read_text())
 count=0
 for row in rows:
  if not row['logical'].startswith('phoenix_dbl_'):continue
  paths=re.findall(r'offline-custom/\d+/'+re.escape(row['file']),smali)
  assert paths,row['logical']
  assert z.read('assets/'+paths[0])==(ROOT/'dist/kaneki-assets'/row['file']).read_bytes(),row['logical']
  count+=1
 print('PASS: active native library and',count,'DB Legends bundles match validated source')
with apk.open('rb') as f:print('SHA256',hashlib.file_digest(f,'sha256').hexdigest())
