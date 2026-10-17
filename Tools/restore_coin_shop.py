"""Keep the offline Coin Shop products matched to the preserved client tables."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'Server/Protocol'
items={r['item_id']:r for r in json.loads((ROOT/'Research/DecodedCache/items.json').read_text())}
lines=['#pragma once','namespace GcLocal {','struct CoinProduct { int id,item,count,type; bool event; int price,payType,payRating; };','inline const CoinProduct CoinProducts[] = {']
for event,table in [(False,'DB_coin_shop'),(True,'DB_coin_shop_event')]:
 file=ROOT/f'Research/DecodedCache/{table}.json'
 offline=ROOT/f'Research/DecodedCache/{table}.offline.json'
 if offline.exists():file=offline
 for row in json.loads(file.read_text()):
  item=items[row['product_id']]
  lines.append('{%d,%d,%d,%d,%s,%d,%d,%d},'%(row['id'],row['product_id'],row['product_count'],item['item_type'],str(event).lower(),row['price_count'],{'herocoin':26,'eventcoin':27,'fesherocoin':28,'friend':6}[row['price_coin_item_type']],row['price_coin_type']))
lines+=['};','struct PaymentCoin {int id,rating;};','inline const PaymentCoin PaymentCoins[]={']
lines+=['{%d,%d},'%(r['item_id'],r['item_rating']) for r in items.values() if r['item_type'] in (26,27,28)]
lines+=['};','inline const CoinProduct* FindCoinProduct(int id,bool event) { for (const auto& p:CoinProducts) if(p.id==id && p.event==event) return &p; return nullptr; }','}']
(p/'LocalCoinCatalog.h').write_text('\n'.join(lines)+'\n')
contracts={
 'SevenDSCoinShopC2S':(10664,'CG_RequestCoinShopInfo();\n CG_RequestCoinShopBuy([in] LocalCoinBuyRequest request);\n CG_RequestEventCoinShopBuy([in] LocalCoinBuyRequest request);'),
 'SevenDSCoinShopS2C':(18517,'CG_RequestCoinShopInfoOK([in] LocalCoinShopInfo info);\n CG_RequestCoinShopBuyOK([in] LocalCoinBuyResult result);'),
 'SevenDSEventCoinS2C':(18573,'CG_RequestEventCoinShopBuyOK([in] LocalCoinBuyResult result);')}
for ns,(base,methods) in contracts.items(): (p/(ns+'.PIDL')).write_text('#include "GrandCrossRmiTypes.h"\nglobal %s %d\n{\n %s\n}\n'%(ns,base,methods))
print('Generated',len(lines)-7,'native Coin Shop products')
