from pathlib import Path
import sys
import zipfile,shutil,lzma,json,re,subprocess,os,lief
ROOT=Path(__file__).resolve().parents[1];decoded=ROOT/'Research/PhoneClientDecoded';lib=decoded/'lib/arm64-v8a';lib.mkdir(parents=True,exist_ok=True)
from patch_content_unlocks import patch
patch(ROOT/'Original-APK/libil2cpp.phone-local.so')
from patch_tg_race import patch as patch_race
patch_race()
from patch_db_legends_fusion import patch as patch_fusion
patch_fusion()
java=Path('C:/Program Files/Eclipse Adoptium/jdk-25.0.3.9-hotspot/bin');tools=Path('C:/Program Files (x86)/Android/android-sdk/build-tools/36.0.0');os.environ['JAVA_HOME']=str(java.parent)
with zipfile.ZipFile(ROOT/'Original-APK/split_config.arm64_v8a.apk') as z:
 for name in z.namelist():
  if name.startswith('lib/arm64-v8a/') and not name.endswith('/'):(lib/Path(name).name).write_bytes(z.read(name))
shutil.copy2(ROOT/'Original-APK/libil2cpp.phone-local.so',lib/'libil2cpp.so')
shutil.copy2(ROOT/'Original-APK/libProudNetClientPlugin.phone-simple.so',lib/'libProudNetClientPlugin.so')
for name in ('libgadget.so','libgadget.config.so','liblocal-script.so'):
 if (lib/name).exists():(lib/name).unlink()
manifest=decoded/'AndroidManifest.xml';text=manifest.read_text()
text=re.sub(r' android:requiredSplitTypes="[^"]*"','',text)
text=re.sub(r'\s*<meta-data[^>]+android:name="com.android.vending.splits(?:.required)?"[^>]*/>','',text)
manifest.write_text(text)
subprocess.run([__import__('sys').executable, str(ROOT/'Tools/package_summon_catalog.py')], check=True)
if (ROOT/'dist/kaneki-assets/assets.json').exists() and '--skip-assets' not in sys.argv:
 subprocess.run([__import__('sys').executable, str(ROOT/'Tools/patch_tg_running.py')], check=True)
 subprocess.run([__import__('sys').executable, str(ROOT/'Tools/repair_tg_bundle_identities.py')], check=True)
 subprocess.run([__import__('sys').executable, str(ROOT/'Tools/package_custom_assets.py')], check=True)
def run(*args):print('Running',Path(str(args[0])).name,flush=True);subprocess.run([str(a) for a in args],check=True)
unsigned=ROOT/'Research/phone-client-unsigned.apk';aligned=ROOT/'Research/phone-client-aligned.apk';apk=ROOT/'dist/7DS-Offline-Client.apk'
run(java/'java.exe','-jar','E:/Games/Blazing-Rebirth/tools/apktool/apktool.clean.jar','b',decoded,'-o',unsigned)
run(tools/'zipalign.exe','-f','-p','4',unsigned,aligned)
run(tools/'apksigner.bat','sign','--ks',ROOT/'.keys/7ds-local.jks','--ks-key-alias','7ds-local','--ks-pass','file:'+str(ROOT/'.keys/signing-password.txt'),'--out',apk,aligned)
run(tools/'apksigner.bat','verify',apk)
print('Built',apk)
