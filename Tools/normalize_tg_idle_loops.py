"""Ensure native idle states continue even when source showcase clips are one-shot."""
from pathlib import Path
import json,zlib
import UnityPy
from gc_bundle_manifest import read,write,bundle_key
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/kaneki-assets'
manifest=read((OUT/'br-m.bin').read_bytes());rows=json.loads((OUT/'assets.json').read_text())
for row in rows:
 if not row['logical'].startswith('phoenix_tg_') or not row['logical'].endswith('_animations_0'):continue
 env=UnityPy.load((OUT/row['file']).read_bytes());changed=False
 for o in env.objects:
  if o.type.name=='AnimationClip' and o.read().m_Name in ['idle','idle_battle']:
   t=o.read_typetree()
   if not t['m_MuscleClip']['m_LoopTime']:t['m_MuscleClip']['m_LoopTime']=True;o.save_typetree(t);changed=True
 if changed:
  (OUT/row['file']).write_bytes(env.file.save(packer='lz4'));crc=zlib.crc32(b''.join(f.save() for f in env.file.files.values()));manifest[0][bundle_key(row['file'])]['crc']=crc;row['crc']=crc
  print('Fixed looping:',row['logical'])
(OUT/'br-m.bin').write_bytes(write(*manifest));(OUT/'assets.json').write_text(json.dumps(rows,indent=2))
