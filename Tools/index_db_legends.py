"""Index the user's copied Legends cache without touching account data."""
from pathlib import Path
import collections
import json
import UnityPy

ROOT = Path(__file__).resolve().parents[1] / 'Research/DBLegends'
SOURCE = ROOT / 'PhoneFiles/streamingassetbundles'
TARGET = ROOT / 'bundle-index.json'
rows = json.loads(TARGET.read_text(encoding='utf-8')) if TARGET.exists() else []
done = {row['file'] for row in rows}
for path in SOURCE.iterdir():
    if path.name in done or not path.is_file():
        continue
    env = UnityPy.load(str(path))
    row = dict(file=path.name, objects=dict(collections.Counter(o.type.name for o in env.objects)), names=[], paths=[], externals=[])
    for obj in env.objects:
        if obj.type.name == 'AssetBundle':
            row['paths'] = [entry[0] for entry in obj.read().m_Container]
        elif obj.type.name in ['GameObject', 'AnimationClip', 'Mesh', 'Avatar', 'Texture2D', 'TextAsset']:
            row['names'].append(obj.read().m_Name)
    for asset in env.assets:
        row['externals'] += [external.path for external in asset.externals]
    rows.append(row)
    if any('/goku/' in path or 'gokuui' in path for path in row['paths']):
        print(path.name, row['paths'][:4])
TARGET.write_text(json.dumps(rows, indent=2), encoding='utf-8')
print('Indexed', len(rows), 'Legends bundles')
