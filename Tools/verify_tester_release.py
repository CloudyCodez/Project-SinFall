"""Verify the distributable client segments and every asset before publication."""
from pathlib import Path
import argparse
import hashlib
import json
import zipfile
from build_tester_release import ROOT, VERSION, ASSET_VERSION, REPO, sha


def verify(output):
    manifest = json.loads((output/'main/release.json').read_text())
    assert manifest['schema'] == 1 and manifest['version'] == VERSION
    assert manifest['asset_version'] == ASSET_VERSION
    digest = hashlib.sha256()
    length = 0
    names = set()
    for item in manifest['client']['parts']:
        path = output/'main'/item['name']
        assert item['url'] == f'https://github.com/{REPO}/releases/download/{VERSION}/{path.name}'
        assert path.stat().st_size == item['size'] < 2**31
        assert sha(path) == item['sha256'], path
        with path.open('rb') as source:
            while chunk := source.read(1024*1024):
                digest.update(chunk)
                length += len(chunk)
    assert digest.hexdigest() == manifest['client']['sha256']
    assert length == manifest['client']['size']
    assert sha(output/'7DS-Offline-Client.apk') == manifest['client']['sha256']
    for item in manifest['assets']:
        path = output/'assets'/item['name']
        print('Verifying', path.name, flush=True)
        assert item['url'] == f'https://github.com/{REPO}/releases/download/{ASSET_VERSION}/{path.name}'
        assert path.stat().st_size == item['size'] < 2**31
        assert sha(path) == item['sha256'], path
        with zipfile.ZipFile(path) as z:
            assert z.testzip() is None, path
            entries = z.infolist()
            assert len(entries) == item['files']
            assert sum(e.file_size for e in entries) == item['unpacked_size']
            for entry in entries:
                assert entry.filename.startswith('bm/')
                assert '..' not in Path(entry.filename).parts and '\\' not in entry.filename
                assert entry.filename not in names, entry.filename
                names.add(entry.filename)
    source_names = {p.relative_to(ROOT/'PhoneVanillaData/files').as_posix()
                    for p in (ROOT/'PhoneVanillaData/files/bm').rglob('*') if p.is_file()}
    assert names == source_names, 'Asset inventory differs from preserved cache'
    with zipfile.ZipFile(ROOT/'dist/7DS-Offline-Client.apk') as original, \
         zipfile.ZipFile(output/'7DS-Offline-Client.apk') as released:
        assert released.testzip() is None
        for entry in original.infolist():
            if (entry.filename.startswith('lib/') or entry.filename.startswith('assets/') or
                (entry.filename.startswith('classes') and entry.filename.endswith('.dex'))):
                with original.open(entry) as a, released.open(entry.filename) as b:
                    assert hashlib.file_digest(a, 'sha256').digest() == hashlib.file_digest(b, 'sha256').digest(), entry.filename
        assert 'classes6.dex' in released.namelist()
    assert sha(output/'main/7DS-Offline-Hub.apk') == sha(output/'7DS-Offline-Hub.apk')
    receipt = dict(version=VERSION, client_sha256=manifest['client']['sha256'],
                   manifest_sha256=sha(output/'main/release.json'), asset_files=len(names),
                   asset_packs=len(manifest['assets']), asset_bytes=sum(i['unpacked_size'] for i in manifest['assets']),
                   checks='SHA-256, part reconstruction, ZIP CRC, asset inventory, preserved game code/content',
                   device_tested=False)
    (output/'main/verification.json').write_text(json.dumps(receipt, indent=2)+'\n')
    # Include the verification receipt in the final checksums.
    for folder in (output/'main', output/'assets'):
        (folder/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.name}\n' for p in sorted(folder.iterdir())
                                                   if p.is_file() and p.name != 'SHA256SUMS.txt'))
    print(json.dumps(receipt, indent=2), flush=True)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    verify(parser.parse_args().output)
