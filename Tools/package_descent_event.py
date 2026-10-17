"""Add an offline Crocshell point track while preserving all other client DB edits."""
import json,struct,zlib
from copy import deepcopy
import UnityPy
from read_plain_table import read_table,write_table,root
name='30FF13B981773B83827E17DB9C456368';table='DB_event_mission_score';cls='DBEventMissionScoreRow'
original=read_table(table,cls);assert write_table(original,cls)==(root/f'Research/DecodedCache/{table}.bin').read_bytes()
rows=[r for r in original if r['event_sub_index']!=1000001];used={r['id'] for r in rows}
source=[r for r in original if r['event_sub_index']==1001];assert len(source)==5
for r in source:
 e=deepcopy(r);e['id']=max(used)+1;used.add(e['id']);e.update(event_sub_index=1000001,event_point_id=912305);rows.append(e)
(root/f'Research/DecodedCache/{table}.offline.json').write_text(json.dumps(rows,indent=2))
target=root/'dist/cache/b'/name;env=UnityPy.load(str(target));changed=False
for o in env.objects:
 if o.type.name!='TextAsset':continue
 a=o.read()
 if a.m_Name==table:a.m_Script=write_table(rows,cls).decode('utf8','surrogateescape');a.save();changed=True
assert changed;target.write_bytes(env.file.save(packer='lz4'));checked=UnityPy.load(str(target))
saved=next(o.read().m_Script for o in checked.objects if o.type.name=='TextAsset' and o.read().m_Name==table);assert saved.encode('utf8','surrogateescape')==write_table(rows,cls)
manifest_path=root/'dist/cache/br-b.bin';manifest=bytearray(manifest_path.read_bytes());assert manifest.find(name.encode())==27;struct.pack_into('<I',manifest,12,zlib.crc32(b''.join(f.save() for f in checked.file.files.values())));manifest_path.write_bytes(manifest)
print('PASS: preserved original point tracks; added five-tier Crocshell adapter; verified bundle and manifest CRC')
