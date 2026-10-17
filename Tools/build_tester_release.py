"""Build the phone-only installer and split release payload without touching recovery APKs.

Requires Java, Android SDK build-tools 36, apktool 3 and the preserved local client.
Large output goes to --output (use a drive with at least 22 GB free).
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[1]
VERSION = 'v0.1.0-tester.1'
ASSET_VERSION = 'assets-v0.1.0-tester.1'
REPO = 'CloudyCodez/Project-SinFall'
JAVA = Path(os.environ.get('SINFALL_JAVA', 'C:/Program Files/Eclipse Adoptium/jdk-25.0.3.9-hotspot/bin'))
SDK = Path(os.environ.get('ANDROID_HOME', 'C:/Program Files (x86)/Android/android-sdk'))
BT = SDK / 'build-tools/36.0.0'
JAR = SDK / 'platforms/android-35/android.jar'
APKTOOL = Path(os.environ.get('SINFALL_APKTOOL', 'E:/Games/Blazing-Rebirth/tools/apktool/apktool.clean.jar'))
os.environ['JAVA_HOME'] = str(JAVA.parent)


def run(*args):
    print('Running', Path(str(args[0])).name, flush=True)
    subprocess.run([str(a) for a in args], check=True)


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def spec(path, tag):
    return dict(name=path.name, size=path.stat().st_size, sha256=sha(path),
                url=f'https://github.com/{REPO}/releases/download/{tag}/{path.name}')


def compile_java(sources, work):
    classes = work / 'classes'
    dex = work / 'dex'
    classes.mkdir(parents=True, exist_ok=True)
    dex.mkdir(exist_ok=True)
    run(JAVA/'javac.exe', '-source', '8', '-target', '8', '-encoding', 'UTF-8',
        '-classpath', JAR, '-d', classes, *sources)
    run(BT/'d8.bat', '--lib', JAR, '--min-api', '26', '--output', dex, *classes.rglob('*.class'))
    return dex / 'classes.dex'


def sign(unsigned, destination, work):
    aligned = work / 'aligned.apk'
    run(BT/'zipalign.exe', '-f', '-p', '4', unsigned, aligned)
    run(BT/'apksigner.bat', 'sign', '--ks', ROOT/'.keys/7ds-local.jks',
        '--ks-key-alias', '7ds-local', '--ks-pass', 'file:'+str(ROOT/'.keys/signing-password.txt'),
        '--out', destination, aligned)
    run(BT/'apksigner.bat', 'verify', '--verbose', destination)
    aligned.unlink()


def hub(output, work):
    work.mkdir(parents=True, exist_ok=True)
    sources = list((ROOT/'AndroidHub/src').rglob('*.java')) + [ROOT/'AndroidSetup/src/com/phoenix/offline/ReleaseFiles.java']
    dex = compile_java(sources, work)
    assets = work/'assets'
    shutil.copytree(ROOT/'Research/RuntimeConfig', assets/'content', dirs_exist_ok=True)
    unsigned = work/'unsigned.apk'
    run(BT/'aapt2.exe', 'link', '-o', unsigned, '-I', JAR,
        '--manifest', ROOT/'AndroidHub/AndroidManifest.xml', '-A', assets)
    with zipfile.ZipFile(unsigned, 'a') as z:
        z.write(dex, 'classes.dex')
        z.write(ROOT/'AndroidHub/native/libgcserver.so', 'lib/arm64-v8a/libgcserver.so')
    sign(unsigned, output/'7DS-Offline-Hub.apk', work)
    unsigned.unlink()


def client(output, work):
    work.mkdir(parents=True, exist_ok=True)
    dex = compile_java(list((ROOT/'AndroidSetup/src').rglob('*.java')), work)
    decoded = ROOT/'Research/PhoneClientDecoded'
    resource_project = work/'resources'
    resource_project.mkdir(exist_ok=True)
    shutil.copytree(decoded/'res', resource_project/'res', dirs_exist_ok=True)
    shutil.copy2(decoded/'apktool.yml', resource_project/'apktool.yml')
    android = '{http://schemas.android.com/apk/res/android}'
    ET.register_namespace('android', 'http://schemas.android.com/apk/res/android')
    manifest = ET.parse(decoded/'AndroidManifest.xml')
    application = manifest.getroot().find('application')
    activity = ET.SubElement(application, 'activity', {
        android+'name': 'com.phoenix.offline.AssetSetupActivity', android+'exported': 'true',
        android+'configChanges': 'orientation|screenSize|keyboardHidden',
        android+'theme': '@android:style/Theme.Material.NoActionBar'})
    for original in list(application.findall('activity')):
        if original is activity:
            continue
        for intent in list(original.findall('intent-filter')):
            if any(c.get(android+'name') == 'android.intent.category.LAUNCHER' for c in intent.findall('category')):
                original.remove(intent)
                activity.append(intent)
    manifest.write(resource_project/'AndroidManifest.xml', encoding='utf-8', xml_declaration=True)
    resources_apk = work/'resources.apk'
    run(JAVA/'java.exe', '-jar', APKTOOL, 'b', resource_project, '-o', resources_apk)
    unsigned = work/'unsigned.apk'
    # Keep the exact tested game code, native libraries and custom content from the existing APK.
    # Only replace compiled resources/manifest and add a separate setup DEX.
    with zipfile.ZipFile(ROOT/'dist/7DS-Offline-Client.apk') as original, \
         zipfile.ZipFile(resources_apk) as resources, zipfile.ZipFile(unsigned, 'w', allowZip64=True) as dest:
        for entry in original.infolist():
            if entry.filename in ('AndroidManifest.xml', 'resources.arsc') or entry.filename.startswith(('res/', 'META-INF/')):
                continue
            with original.open(entry) as src, dest.open(entry, 'w', force_zip64=entry.file_size >= 2**31) as target:
                shutil.copyfileobj(src, target, 1024*1024)
        for entry in resources.infolist():
            if entry.filename in ('AndroidManifest.xml', 'resources.arsc') or entry.filename.startswith('res/'):
                dest.writestr(entry, resources.read(entry))
        dest.write(dex, 'classes6.dex', compress_type=zipfile.ZIP_STORED)
    sign(unsigned, output/'7DS-Offline-Client.apk', work)
    unsigned.unlink()


def package(output):
    main = output/'main'
    side = output/'assets'
    main.mkdir(exist_ok=True)
    side.mkdir(exist_ok=True)
    apk = output/'7DS-Offline-Client.apk'
    parts = []
    with apk.open('rb') as source:
        index = 1
        while True:
            chunk = source.read(1024*1024)
            if not chunk:
                break
            part = main/f'7DS-Offline-Client.apk.part{index:03}'
            with part.open('wb') as target:
                target.write(chunk)
                remaining = 900*1024*1024-len(chunk)
                while remaining:
                    chunk = source.read(min(1024*1024, remaining))
                    if not chunk:
                        break
                    target.write(chunk)
                    remaining -= len(chunk)
            parts.append(spec(part, VERSION))
            index += 1
    packs = []
    files = sorted(p for p in (ROOT/'PhoneVanillaData/files/bm').rglob('*') if p.is_file())
    batch, size = [], 0

    def flush():
        path = side/f'7DS-assets-{len(packs)+1:03}.zip'
        print('Packing', path.name, len(batch), 'files', flush=True)
        with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_STORED) as z:
            for f in batch:
                z.write(f, f.relative_to(ROOT/'PhoneVanillaData/files').as_posix())
        item = spec(path, ASSET_VERSION)
        item.update(unpacked_size=size, files=len(batch))
        packs.append(item)

    for f in files:
        n = f.stat().st_size
        if batch and size+n > 900*1024*1024:
            flush()
            batch, size = [], 0
        batch.append(f)
        size += n
    if batch:
        flush()
    manifest = dict(schema=1, version=VERSION, asset_version=ASSET_VERSION,
                    client=dict(size=apk.stat().st_size, sha256=sha(apk), parts=parts), assets=packs)
    (main/'release.json').write_text(json.dumps(manifest, indent=2)+'\n')
    shutil.copy2(output/'7DS-Offline-Hub.apk', main/'7DS-Offline-Hub.apk')
    (side/'assets.json').write_text(json.dumps(dict(version=ASSET_VERSION, assets=packs), indent=2)+'\n')
    for folder in (main, side):
        checksums = '\n'.join(f'{sha(p)}  {p.name}' for p in sorted(folder.iterdir()) if p.is_file() and p.name != 'SHA256SUMS.txt')
        (folder/'SHA256SUMS.txt').write_text(checksums+'\n')
    print('Release payload ready at', output, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--step', choices=['hub', 'client', 'package', 'all'], default='all')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    if args.step in ('hub', 'all'):
        hub(args.output, args.output/'build-hub')
    if args.step in ('client', 'all'):
        client(args.output, args.output/'build-client')
    if args.step in ('package', 'all'):
        package(args.output)
