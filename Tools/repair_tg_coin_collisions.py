"""Move TG hero coins away from native 500xxx resources; preserve the current DB."""
from pathlib import Path
import json,re,struct,zlib,runpy
from copy import deepcopy
import UnityPy
import read_plain_table as reader
from read_plain_table import root,read_table,write_table
classes={'DB_item_info':'DBItemInfoRow','DB_skin_base':'DBSkinBaseRow'}
original=read_table('DB_item_info','DBItemInfoRow')
target=root/'dist/cache/b/30FF13B981773B83827E17DB9C456368';env=UnityPy.load(str(target))
scratch=root/'dist/coin-repair-read';(scratch/'Research/DecodedCache').mkdir(parents=True,exist_ok=True)
for o in env.objects:
 if o.type.name=='TextAsset' and o.read().m_Name in classes:
  a=o.read();(scratch/'Research/DecodedCache'/f'{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
oldroot=reader.root;reader.root=scratch;tables={n:read_table(n,c) for n,c in classes.items()};reader.root=oldroot
units=json.loads((root/'Research/TokyoGhoul/roster-port-inventory.json').read_text())
items={r['item_id']:r for r in tables['DB_item_info']};mapping={}
for u in units:
 old=u['coin'];new=498500+u['index'];assert new!=498999
 if old!=new:
  assert new not in items,(new,'already occupied')
  row=deepcopy(items[old]);row['item_id']=new;items[new]=row;mapping[old]=new;u['coin']=new
for row in original:
 if row['item_id'] in mapping:items[row['item_id']]=row
for row in tables['DB_skin_base']:
 if 2995001<=row['matching_hero_id']<=2995121:row['hero_coin']=next(u['coin'] for u in units if u['hero']==row['matching_hero_id'])
tables['DB_item_info']=list(items.values())
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));mf=root/'dist/cache/br-b.bin';b=bytearray(mf.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));mf.write_bytes(b)
for n in classes:(root/f'Research/DecodedCache/{n}.tg.offline.json').write_text(json.dumps(tables[n],indent=2))
(root/'Research/DecodedCache/items.json').write_text(json.dumps(tables['DB_item_info'],indent=2));(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2))
(root/'Research/TokyoGhoul/roster-port-inventory.json').write_text(json.dumps(units,indent=2))
f=root/'Server/Protocol/LocalEconomyCatalog.h';s=f.read_text();a=s.index('HeroCoins[]');b=s.index('\n};',a);part=s[a:b]
for u in units:
 for sid in [u['ssr'],u['ur']]:part=re.sub(r'\{%d,\d+\},'%sid,'{%d,%d},'%(sid,u['coin']),part)
s=s[:a]+part+s[b:];f.write_text(s)
runpy.run_path(str(root/'Tools/build_material_catalog.py'),run_name='__main__')
assert items[500019]['item_type']==82 and items[500012]['item_type']==3 and items[500021]['item_type']==55
assert not ({u['coin'] for u in units}&{r['item_id'] for r in original})
print('Restored native resource definitions; moved 121 TG duplicate coins to reserved IDs')
