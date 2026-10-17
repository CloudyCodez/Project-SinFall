"""Move Legends resources out of the TG allocation while retaining costume groups."""
from pathlib import Path
helper=Path(__file__).with_name('package_tg_roster.py')
exec(compile(helper.read_text(encoding='utf-8').split('# Fixed bonuses')[0],str(helper),'exec'))
mapping={}
for start,new,count in [(701,851,3),(711,861,3),(721,871,1)]:
 for i in range(count):
  for prefix in [3399000,4999000,899000]:mapping[prefix+start+i]=prefix+new+i
for old,new in mapping.items():
 for table in ['DB_skin_costume_resource','DB_head_costume_resource','DB_weapon_costume_resource','DB_costume_base']:
  original=next((r for r in tables[table] if r['id']==old),None)
  if original is not None:
   if table!='DB_costume_base':assert original['character_base'].startswith(('goku','vegeta','gogeta')),(old,table)
   row=deepcopy(original);row['id']=new;put(table,row)
 original=next(r for r in tables['DB_item_info'] if r['item_id']==old);row=deepcopy(original);row['item_id']=new;put('DB_item_info',row,'item_id')
for skin in tables['DB_skin_base']:
 if skin['id'] in [399901,399902,399903,399911,399912,399913,399921]:
  for field in ['base_skin_costume_id','base_head_costume_id','base_weapon_costume_id']:skin[field]=mapping.get(skin[field],skin[field])
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));mf=root/'dist/cache/br-b.bin';b=bytearray(mf.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));mf.write_bytes(b)
for f in [root/'Tools'/n for n in ['package_db_legends_goku.py','package_db_legends_vegeta.py','package_db_legends_gogeta.py','package_db_legends_goku_black.py']]+[root/'Server/Protocol/LocalCosmeticCatalog.h']:
 s=f.read_text(encoding='utf-8')
 for old,new in mapping.items():s=re.sub(r'\b'+str(old)+r'\b',str(new),s)
 f.write_text(s,encoding='utf-8')
print('Moved seven Legends models to reserved costume IDs, preserving equipped groups')
