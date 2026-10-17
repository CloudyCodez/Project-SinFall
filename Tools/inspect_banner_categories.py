import json
from collections import Counter
from read_plain_table import read_table,root,dump
b=json.loads((root/'Research/DecodedCache/banners.json').read_text())
for x in b:print({k:x[k] for k in ('id','gamble_type','gamble_group','gamble_BG_name','list_array_pickup_skin_id')})
s=json.loads((root/'Research/DecodedCache/skins.json').read_text());print('Skin keys',list(s[0]))
for name,cls in [('DB_hero_base','DBHeroBaseRow'),('DB_hero_list','DBHeroListRow')]:
 try:
  rows=read_table(name,cls);print(name,len(rows),rows[:2]);(root/f'Research/DecodedCache/{name}.json').write_text(json.dumps(rows,indent=2))
 except Exception as e:print(name,e)
