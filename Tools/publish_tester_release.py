"""Upload verified payloads as drafts, then publish the side assets and main tester."""
from pathlib import Path
import argparse
import json
import subprocess
from build_tester_release import ROOT, REPO, VERSION, ASSET_VERSION, sha


def gh(*args):
    return subprocess.check_output(['gh', *map(str, args)], text=True, encoding='utf-8')


def remote_release(tag):
    # Draft tags are not available through /releases/tags until publication.
    url = json.loads(gh('release', 'view', tag, '--repo', REPO, '--json', 'apiUrl'))['apiUrl']
    return json.loads(gh('api', url))


def verify_remote(tag, folder):
    remote = remote_release(tag)
    for file in folder.iterdir():
        if file.is_file():
            asset = next(a for a in remote['assets'] if a['name'] == file.name)
            assert asset['size'] == file.stat().st_size and asset['digest'] == 'sha256:'+sha(file), file.name


def publish(output):
    receipt = json.loads((output/'main/verification.json').read_text())
    assert receipt['manifest_sha256'] == sha(output/'main/release.json'), 'Re-run payload verification'
    for folder in (output/'assets', output/'main'):
        for line in (folder/'SHA256SUMS.txt').read_text().splitlines():
            digest, name = line.split('  ', 1)
            assert sha(folder/name) == digest, f'Payload changed: {name}'
    for tag, title, notes, folder in (
        (ASSET_VERSION, 'Tester 1 — separate game assets', 'ASSET-NOTES.md', output/'assets'),
        (VERSION, 'Project SinFall — First tester', 'TESTER-NOTES.md', output/'main'),
    ):
        existing = subprocess.run(['gh', 'release', 'view', tag, '--repo', REPO, '--json', 'isDraft'], capture_output=True, text=True, encoding='utf-8')
        if existing.returncode:
            print(gh('release', 'create', tag, '--repo', REPO, '--target', 'main', '--draft', '--prerelease',
                     '--title', title, '--notes-file', ROOT/'Release'/notes), flush=True)
        else:
            if not json.loads(existing.stdout)['isDraft']:
                verify_remote(tag, folder)
                print('Published release already matches:', tag, flush=True)
                continue
        remote = remote_release(tag)['assets']
        complete = {a['name']: a for a in remote}
        for file in sorted(folder.iterdir()):
            if not file.is_file():
                continue
            asset = complete.get(file.name)
            if asset and asset.get('digest') == 'sha256:'+sha(file) and asset['size'] == file.stat().st_size:
                print('Already uploaded:', file.name, flush=True)
                continue
            print('Uploading', file.name, flush=True)
            # One file at a time limits peak memory and permits rerunning failed uploads.
            for attempt in range(3):
                try:
                    print(gh('release', 'upload', tag, file, '--repo', REPO, '--clobber'), flush=True)
                    break
                except subprocess.CalledProcessError:
                    if attempt == 2:
                        raise
                    print('Retrying upload:', file.name, flush=True)
        verify_remote(tag, folder)
        print(gh('release', 'edit', tag, '--repo', REPO, '--draft=false', '--prerelease', '--latest=false'), flush=True)
    print(f'https://github.com/{REPO}/releases/tag/{VERSION}', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    publish(parser.parse_args().output)
