"""Keep coin-shop tabs and rarity prices synchronized in client and server catalogs."""
import json,struct,zlib
from pathlib import Path
from copy import deepcopy
import UnityPy
from read_plain_table import root,write_table,read_table
skins={r['id']:r for r in json.loads((root/'Research/DecodedCache/skins.json').read_text())}
normal=json.loads((root/'Research/DecodedCache/DB_coin_shop.offline.json').read_text())
event_path=root/'Research/DecodedCache/DB_coin_shop_event.offline.json'
events=json.loads((event_path if event_path.exists() else root/'Research/DecodedCache/DB_coin_shop_event.json').read_text())
template=read_table('DB_coin_shop_event','DBCoinShopEventRow')[0]
collab=[r for r in normal if r['product_id'] in skins and r['price_coin_item_type']=='eventcoin']
normal=[r for r in normal if r not in collab]
for r in collab:
 e=next((x for x in events if x['product_id']==r['product_id']),None)
 if e is None:
  e=deepcopy(template);e['id']=r['id'];assert e['id'] not in {x['id'] for x in events};events.append(e)
 for key in e:
  if key in r:e[key]=r[key]
 e.update(product_category=1,product_sale=1,price_coin_item_type='eventcoin',price_coin_type=5,price_count=3,skin_discount=3,buy_limited_start='',buy_limited_end='')
for r in normal:
 if r['product_id'] in skins and r['price_coin_item_type']=='herocoin':
  rating=skins[r['product_id']]['start_rating'];price=10 if rating<=3 else 20 if rating==4 else 30
  r.update(price_coin_type=4,price_count=price,skin_discount=price)
assert all(r['price_coin_item_type']!='eventcoin' for r in normal if r['product_id'] in skins)
modified={'DB_coin_shop':('DBCoinShopRow',normal),'DB_coin_shop_event':('DBCoinShopEventRow',events)}
for name,(cls,rows) in modified.items():
 (root/f'Research/DecodedCache/{name}.offline.json').write_text(json.dumps(rows,indent=2))
 assert write_table(read_table(name,cls),cls)==(root/f'Research/DecodedCache/{name}.bin').read_bytes()
name='30FF13B981773B83827E17DB9C456368';target=root/'dist/cache/b'/name
env=UnityPy.load(str(target));changed=set()
for o in env.objects:
 if o.type.name!='TextAsset':continue
 a=o.read()
 if a.m_Name in modified:
  cls,rows=modified[a.m_Name];a.m_Script=write_table(rows,cls).decode('utf8','surrogateescape');a.save();changed.add(a.m_Name)
assert changed==set(modified);target.write_bytes(env.file.save(packer='lz4'))
checked=UnityPy.load(str(target));saved={o.read().m_Name:o.read().m_Script for o in checked.objects if o.type.name=='TextAsset'}
for table,(cls,rows) in modified.items():assert saved[table].encode('utf8','surrogateescape')==write_table(rows,cls)
manifest_path=root/'dist/cache/br-b.bin';manifest=bytearray(manifest_path.read_bytes());assert manifest.find(name.encode())==27
struct.pack_into('<I',manifest,12,zlib.crc32(b''.join(f.save() for f in checked.file.files.values())));manifest_path.write_bytes(manifest)
report={'regular_prices_gold':{'R':10,'SR':20,'SSR_and_above':30},'collab_event_units':sum(x['product_id'] in skins and x['price_coin_item_type']=='eventcoin' for x in events),'regular_products':len(normal),'event_products':len(events)}
(root/'dist/normal-unit-coin-shop.json').write_text(json.dumps(report,indent=2));print(report)
