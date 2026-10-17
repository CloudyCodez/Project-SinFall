"""Validate the port against the native bundle cache and prefab contracts."""
import json
from pathlib import Path
import UnityPy
from gc_bundle_manifest import read, hash_name, bundle_key

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist/kaneki-assets'
official,_,_=read((ROOT/'Research/PhoneAssets/bm/br-m.bin').read_bytes())
assert all(key==bundle_key(row['name']) for key,row in official.items())
bundles,_,directories=read((OUT/'br-m.bin').read_bytes())
identities=set()
for row in json.loads((OUT/'assets.json').read_text()):
    key=bundle_key(row['file']);assert key in bundles
    env=UnityPy.load((OUT/row['file']).read_bytes())
    for filename in env.file.files:
        assert filename not in identities,(row['logical'],'duplicate Unity internal file',filename)
        identities.add(filename)
    objects=env.assets[0].objects
    for obj in env.objects:
        tree=obj.read_typetree()
        if obj.type.name=='GameObject':
            assert tree['m_Layer']==9
            assert all(p['component']['m_PathID'] in objects for p in tree['m_Component'])
        if obj.type.name=='SkinnedMeshRenderer':
            assert tree['m_Mesh']['m_FileID']==0
            assert tree['m_Mesh']['m_PathID'] in objects
            assert all(p['m_PathID'] in objects for p in tree['m_Bones'])
        if obj.type.name=='AnimationClip':
            stop=tree['m_MuscleClip']['m_StopTime']
            assert all(e['time']<=stop+0.001 for e in tree['m_Events'])
        if obj.type.name=='AssetBundle' and row['logical']=='phoenix_kaneki_model':
            for path,entry in tree['m_Container']:
                go=objects[entry['asset']['m_PathID']].read_typetree()
                assert go['m_Name']==Path(path).stem
    for path in row['paths']:
        base='assets/sevensins/patchresources/'
        directory,filename=path[len(base):].rsplit('/',1)
        assert directories[base][hash_name(directory+'/')][hash_name(filename)]==key
for file in (OUT/'enu').iterdir():
    if file.name.startswith('br-'):continue
    env=UnityPy.load(file.read_bytes())
    for filename in env.file.files:
        assert filename not in identities,('enu',filename)
        identities.add(filename)
print('PASS: unique Unity internal file identities, native filename hashes, prefab names/layers/components, mesh bones, animation events and asset paths')
