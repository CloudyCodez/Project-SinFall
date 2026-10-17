"""Repair existing ports without regenerating models or resetting registrations."""
from pathlib import Path
import json,zlib
import UnityPy
from gc_bundle_manifest import read,write,bundle_key,hash_name
from tg_bundle_identity import unique_files
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/kaneki-assets'
report=json.loads((OUT/'assets.json').read_text())
for module in ['m','enu']:
    folder=OUT if module=='m' else OUT/module
    manifest=read((folder/('br-'+module+'.bin')).read_bytes())
    bundles,_,dirs=manifest
    rows=report if module=='m' else [r for r in report if (folder/r['file']).exists()]
    for row in rows:
        path=folder/row['file'];env=UnityPy.load(path.read_bytes())
        unique_files(env,module+'/'+row['logical'])
        # Duplicate coin portraits use the same native small-icon texture.
        if module=='m':
            bundle=next(o for o in env.objects if o.type.name=='AssetBundle');tree=bundle.read_typetree()
            aliases=[]
            for name,value in tree['m_Container']:
                if '/icon/costume/' in name and name.endswith('_s.png'):
                    aliases.append((name.replace('/icon/costume/','/icon/hero_coin/'),value))
            for name,value in aliases:
                if not any(p==name for p,_ in tree['m_Container']):tree['m_Container'].append((name,value))
                base='assets/sevensins/patchresources/';directory,filename=name[len(base):].rsplit('/',1)
                dirs.setdefault(base,{}).setdefault(hash_name(directory+'/'),{})[hash_name(filename)]=bundle_key(row['file'])
                if name not in row['paths']:row['paths'].append(name)
            bundle.save_typetree(tree)
        path.write_bytes(env.file.save(packer='lz4'))
        crc=zlib.crc32(b''.join(f.bytes if hasattr(f,'bytes') else f.save() for f in env.file.files.values()))
        bundles[bundle_key(row['file'])]['crc']=crc
        if module=='m':row['crc']=crc
    (folder/('br-'+module+'.bin')).write_bytes(write(*manifest))
    print('Repaired',len(rows),module,'bundles',flush=True)
(OUT/'assets.json').write_text(json.dumps(report,indent=2))
