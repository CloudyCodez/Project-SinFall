"""Native bookmark product and standalone hidden heroes; preserve transformation-only forms."""
import json
from copy import deepcopy
from read_plain_table import read_table,root,write_table
skins=read_table('DB_skin_base','DBSkinBaseRow');heroes=read_table('DB_hero_base','DBHeroBaseRow')
dec=lambda value:(value^0x92929292)&0xffffffff
hero_by_id={dec(h['id']):h for h in heroes};skills={r['id']:r for r in read_table('DB_skin_skill','DBSkinSkillRow')}
normal_path=root/'Research/DecodedCache/DB_coin_shop.offline.json';event_path=root/'Research/DecodedCache/DB_coin_shop_event.offline.json'
normal=json.loads(normal_path.read_text());events=json.loads(event_path.read_text());template=read_table('DB_coin_shop_event','DBCoinShopEventRow')[0]
base={}
for s in skins:
 h=s['matching_hero_id']
 if h not in base or (s['rating'],s['id'])<(base[h]['rating'],base[h]['id']):base[h]=s
selected=[]
for hid,s in base.items():
 h=hero_by_id[hid];cards=skills.get(s['id'],{})
 if dec(h['hero_display'])!=0 or 'dummy' in s['skin_portrait_base'] or s['before_change_hero_skin_id'] or s['change_hero_skin_id'] or h['hero_category'].startswith('Collabo_'):continue
 if not all(cards.get(key,0)>0 for key in ['skill_a_1_id','skill_b_1_id','special_id_1']):continue
 selected.append(s['id'])
 existing=next((r for r in events if r['product_id']==s['id']),None)
 original=next((r for r in normal if r['product_id']==s['id']),None)
 if existing is None:
  existing=deepcopy(template);existing['id']=original['id'] if original else 51000+len(selected);events.append(existing)
 if original:
  for key in existing:
   if key in original:existing[key]=original[key]
 existing.update(product_id=s['id'],product_count=1,product_free_count=0,product_category=1,product_sale=1,price_coin_item_type='herocoin',price_coin_type=4,price_count=30,skin_discount=30,buy_limited_count=0,period_buy_limited_count=0,period_buy_limited_type=0,buy_limited_start='',buy_limited_end='')
 normal=[r for r in normal if r['product_id']!=s['id']]
 h['hero_display']=1^0x92929292
 if h['hero_display']>=0x80000000:h['hero_display']-=0x100000000
 for x in skins:
  if x['matching_hero_id']==hid:x['skin_display']=1
bookmark=next((r for r in normal if r['product_id']==500035),None)
if bookmark is None:
 bookmark=deepcopy(next(r for r in normal if r['product_type']==1));bookmark['id']=50035;assert not any(r['id']==50035 for r in normal);normal.append(bookmark)
bookmark.update(product_type=1,product_sale=1,product_id=500035,product_count=1,product_free_count=0,price_coin_item_type='herocoin',price_coin_type=4,price_count=10,skin_discount=10,buy_limited_count=0,ad_info=0,event_product=0,price_coin_item_sub_type=0,period_buy_limited_type=0,period_buy_limited_count=0,buy_limited_start='',buy_limited_end='')
normal_path.write_text(json.dumps(normal,indent=2));event_path.write_text(json.dumps(events,indent=2))
# Refinement packages shop tables without resetting other current DB modifications.
import runpy
runpy.run_path(str(root/'Tools/refine_coin_shop.py'),run_name='__main__')
import UnityPy,struct,zlib
target=root/'dist/cache/b/30FF13B981773B83827E17DB9C456368';env=UnityPy.load(str(target));tables={'DB_skin_base':('DBSkinBaseRow',skins),'DB_hero_base':('DBHeroBaseRow',heroes)}
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in tables:
   cls,rows=tables[a.m_Name];a.m_Script=write_table(rows,cls).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));env=UnityPy.load(str(target));manifest=root/'dist/cache/br-b.bin';b=bytearray(manifest.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));manifest.write_bytes(b)
runpy.run_path(str(root/'Tools/restore_coin_shop.py'),run_name='__main__')
(root/'dist/hidden-story-heroes.json').write_text(json.dumps({'native_hero_records':selected,'price_sr_coins':30,'bookmark_item':500035,'bookmark_gold_coins':10,'boss_only_conversion_pending':['Demon King (Meliodas)','Indura Monspeet','Indura Derieri']},indent=2))
print('Enabled standalone hidden hero records:',selected)
