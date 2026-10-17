from pathlib import Path
import subprocess,shutil,zipfile,secrets,os
import lief
ROOT=Path(__file__).resolve().parents[1];hub=ROOT/'AndroidHub';build=hub/'build';dist=ROOT/'dist';dist.mkdir(exist_ok=True)
java=Path('C:/Program Files/Eclipse Adoptium/jdk-25.0.3.9-hotspot/bin')
sdk=Path('C:/Program Files (x86)/Android/android-sdk');tools=sdk/'build-tools/36.0.0';jar=sdk/'platforms/android-35/android.jar'
native=lief.parse(str(hub/'native/libgcserver.so'))
if 'libc++_shared.so' in native.libraries:
 raise RuntimeError('Phone server requires an unpackaged C++ runtime. Run Tools/build_phone_native.py first.')
def run(*args):
 print('Running',Path(str(args[0])).name,flush=True);subprocess.run([str(a) for a in args],check=True)
for directory in ('classes','dex','assets','lib/arm64-v8a'): (build/directory).mkdir(parents=True,exist_ok=True)
shutil.copytree(ROOT/'Research/RuntimeConfig',build/'assets/content',dirs_exist_ok=True)
shutil.copy2(hub/'native/libgcserver.so',build/'lib/arm64-v8a/libgcserver.so')
run(java/'javac.exe','-source','8','-target','8','-encoding','UTF-8','-classpath',jar,'-d',build/'classes',*hub.glob('src/**/*.java'),ROOT/'AndroidSetup/src/com/phoenix/offline/ReleaseFiles.java')
os.environ['JAVA_HOME']=str(java.parent)
run(tools/'d8.bat','--lib',jar,'--min-api','26','--output',build/'dex',*build.glob('classes/**/*.class'))
run(tools/'aapt2.exe','link','-o',build/'base.apk','-I',jar,'--manifest',hub/'AndroidManifest.xml','-A',build/'assets')
with zipfile.ZipFile(build/'base.apk','a') as z:
 z.write(build/'dex/classes.dex','classes.dex')
 z.write(build/'lib/arm64-v8a/libgcserver.so','lib/arm64-v8a/libgcserver.so',compress_type=zipfile.ZIP_STORED)
keys=ROOT/'.keys';keys.mkdir(exist_ok=True);key=keys/'7ds-local.jks';password=keys/'signing-password.txt'
if not key.exists():
 password.write_text(secrets.token_hex(32))
 run(java/'keytool.exe','-genkeypair','-keystore',key,'-storepass:file',password,'-keypass:file',password,'-alias','7ds-local','-keyalg','RSA','-keysize','3072','-validity','10000','-dname','CN=7DS Offline, O=Phoenix')
run(tools/'zipalign.exe','-f','-p','4',build/'base.apk',build/'aligned.apk')
apk=dist/'7DS-Offline-Hub.apk'
run(tools/'apksigner.bat','sign','--ks',key,'--ks-key-alias','7ds-local','--ks-pass','file:'+str(password),'--out',apk,build/'aligned.apk')
run(tools/'apksigner.bat','verify',apk)
print('Built',apk)
