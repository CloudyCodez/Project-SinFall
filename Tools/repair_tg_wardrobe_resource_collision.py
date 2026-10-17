"""Restore three legacy TG outfit rows overwritten by provisional Black IDs."""
from pathlib import Path
helper=Path(__file__).with_name('package_tg_roster.py')
exec(compile(helper.read_text(encoding='utf-8').split('# Fixed bonuses')[0],str(helper),'exec'))
affected=[u for u in units if u['body'] in [3399701,3399702,3399703,3399711,3399712,3399713,3399721,3399731,3399732,3399733]]
for u in affected:
 for n,field,donor,typ in [('DB_skin_costume_resource','body',3399401,1),('DB_head_costume_resource','head',4999401,3),('DB_weapon_costume_resource','weapon',899401,2)]:
  new=u[field];model=u['model'];x=source(n,donor);x.update(id=new,character_base=model)
  if typ==1:x.update(resource_body=f'hero_{model}_body_0001',resource_base_head=f'hero_{model}_head_0001',portrait_base=model+'_0001',model_scale=1.0,gacha_model_scale=1.0)
  if typ==3:x.update(resource_head=f'hero_{model}_head_0001',error_check_head_resource=f'hero_{model}_head_0001')
  put(n,x)
  x=source('DB_costume_base',donor);x.update(id=new,costume_name=u['text_base']+1,hero_group=u['group'],costume_group=typ*10000000+u['group']*10000+100,list_array_matching_hero_id=[u['hero']],list_array_costume_hide_hero_id=[u['hero']]);put('DB_costume_base',x)
  x=source('DB_item_info',donor,'item_id');x.update(item_id=new,item_name=u['text_base']+1,item_icon=f'icon_hero_{model}_0001_s');put('DB_item_info',x,'item_id')
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));mf=root/'dist/cache/br-b.bin';b=bytearray(mf.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));mf.write_bytes(b)
for name in ['DB_skin_costume_resource','DB_head_costume_resource','DB_weapon_costume_resource']:
 (root/f'Research/DecodedCache/{name}.tg.offline.json').write_text(json.dumps(tables[name],indent=2))
print('Restored outfit resources:',[u['source'] for u in affected])
