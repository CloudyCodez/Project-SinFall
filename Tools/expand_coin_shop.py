"""Add the same non-festival/non-collab base variants as the normal banner."""
import json
from copy import deepcopy
from read_plain_table import read_table,root
def normal_shop(units,festival=(),collab=()):
 rows=read_table('DB_coin_shop','DBCoinShopRow')
 template=next(r for r in rows if r['product_id']==304001)
 ids={r['id'] for r in rows};normal={u['id'] for u in units}
 skins={r['id']:r for r in json.loads((root/'Research/DecodedCache/skins.json').read_text())}
 for index,skin in enumerate(sorted(normal)):
  existing=next((r for r in rows if r['product_id']==skin),None)
  if existing is None:
   existing=deepcopy(template);existing['id']=20000+index
   assert existing['id'] not in ids;ids.add(existing['id']);rows.append(existing)
  rating=skins[skin]['start_rating'];price=10 if rating<=3 else 20 if rating==4 else 30
  existing.update(product_id=skin,product_count=1,product_free_count=0,
                  price_coin_item_type='herocoin',price_coin_type=4,price_count=price,
                  skin_discount=price,buy_limited_count=0,period_buy_limited_count=0,
                  period_buy_limited_type=0,buy_limited_start='',buy_limited_end='',ad_info=0,event_product=0)
 assert {r['product_id'] for r in rows if r['price_coin_type']==4 and r['price_count'] in (10,20,30)}>=normal
 for offset,pool,currency in [(30000,festival,'fesherocoin'),(40000,collab,'eventcoin')]:
  for index,skin in enumerate(sorted({u['id'] for u in pool})):
   existing=next((r for r in rows if r['product_id']==skin),None)
   if existing is None:
    existing=deepcopy(template);existing['id']=offset+index;assert existing['id'] not in ids;ids.add(existing['id']);rows.append(existing)
   existing.update(product_id=skin,product_count=1,product_free_count=0,price_coin_item_type=currency,price_coin_type=5,price_count=3,skin_discount=3,
    price_coin_item_sub_type=0,buy_limited_count=0,period_buy_limited_count=0,period_buy_limited_type=0,buy_limited_start='',buy_limited_end='',ad_info=0,event_product=0)
 (root/'Research/DecodedCache/DB_coin_shop.offline.json').write_text(json.dumps(rows,indent=2))
 (root/'dist/normal-unit-coin-shop.json').write_text(json.dumps({'price':30,'coin_rating':4,'count':len(normal),'units':sorted(normal)},indent=2))
 return rows
