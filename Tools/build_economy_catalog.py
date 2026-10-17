"""Preserved development recipes and farming rewards for finite accounts."""
import json
from pathlib import Path
from read_plain_table import read_table

root = Path(__file__).resolve().parents[1]
out = ['#pragma once', 'namespace GcLocal {',
       'struct EconomyCost { int kind,hero,level,rating; int items[5],counts[5]; };',
       'inline const EconomyCost EconomyCosts[] = {']

def cost(kind, hero, level, rating, pairs):
    pairs = [(i, n) for i, n in pairs if i > 0 and n > 0]
    assert len(pairs) <= 5
    pairs += [(0, 0)] * (5 - len(pairs))
    out.append('{%d,%d,%d,%d,{%s},{%s}},' %
               (kind, hero, level, rating, ','.join(str(i) for i, _ in pairs),
                ','.join(str(n) for _, n in pairs)))

for r in read_table('DB_skin_evolution', 'DBSkinEvolutionRow'):
    pairs = [(r['evolution_key_id'], r['evolution_key_count'])]
    pairs += [(r[f'evolution_material_id_{i}'], r[f'evolution_material_count_{i}']) for i in range(1, 4)]
    pairs += [(r['evolution_price_id'], r['evolution_price_count'])]
    cost(2 if r['evolution_break_check'] else 1, r['matching_hero_id'], r['evolution_rating'], 0, pairs)
for r in read_table('DB_skin_awaken_resource', 'DBSkinAwakenResourceRow'):
    pairs = [(r[f'awaken_material_id_{i}'], r[f'awaken_material_count_{i}']) for i in range(1, 5)]
    pairs += [(r['awaken_price_id'], r['awaken_price_count'])]
    cost(3, r['hero_id'], r['skin_awaken_count'], r['skin_rating'], pairs)
skins = json.loads((root/'Research/DecodedCache/skins.json').read_text())
breaks=read_table('DB_evolution_break_base','DBEvolutionBreakBaseRow')
hero_bases={r['matching_hero_id']:(r['start_rating'],r['attribute']) for r in skins}
for hero,(rating,attribute) in hero_bases.items():
    for r in breaks:
        if r['start_rating']!=rating or r['evolution_break_attribute']!=attribute:continue
        pairs=[(r['evolution_break_key_id'],r['evolution_break_key_count'])]
        pairs += [(r[f'evolution_break_material_id_{i}'],r[f'evolution_break_material_count_{i}']) for i in range(1,4)]
        pairs += [(r['evolution_break_price_id'],r['evolution_break_price_count'])]
        cost(2,hero,r['evolution_break_step'],0,pairs)
coins = {r['matching_hero_id']: r['hero_coin'] for r in skins}
for r in read_table('DB_skin_skill_levelup', 'DBSkinSkillLevelupRow'):
    if r['hero_id'] not in coins:
        continue  # No preserved playable skin: do not invent a duplicate currency.
    for level in range(2, 7):
        cost(4, r['hero_id'], level, 0,
             [(coins[r['hero_id']], r[f'special_material_count_{level}']),
              (r[f'special_price_id_{level}'], r[f'special_price_count_{level}'])])
for r in read_table('DB_skin_transcend', 'DBSkinTranscendRow'):
    cost(5, r['hero_id'], r['transcend_level'], 0,
         [(r['transcend_price_id'], r['transcend_price_count'])])
out += ['};','struct SuperAwakeningCost { int hero,level,gauge,refundItem,refundCount,addGauge; };','inline const SuperAwakeningCost SuperAwakeningCosts[]={']
out += ['{%d,%d,%d,%d,%d,%d},'%(r['hero_id'],r['transcend_level'],r['transcend_gauge'],r['reset_return_item_id'],r['reset_return_item_count'],r['add_transcend_gauge']) for r in read_table('DB_skin_transcend','DBSkinTranscendRow')]
out += ['};','struct SuperAwakeningCoin {int item,points;};','inline const SuperAwakeningCoin SuperAwakeningCoins[]={']
itemrows=json.loads((root/'Research/DecodedCache/items.json').read_text())
config={r['contents']:r['value_int_1']^0x3b3b3b3b for r in read_table('DB_config_game','DBConfigGameRow')}
resetconfig={r['contents']:(r['value_int_1']^0x3b3b3b3b,r['value_int_2']^0x3b3b3b3b) for r in read_table('DB_config_game','DBConfigGameRow')}
for r in itemrows:
    key=''
    if r['item_id']==config['item_transcend_coin_id']:key='transcend_transcend_coin_point'
    elif r['item_type']==26:key={3:'transcend_r_coin_point',4:'transcend_sr_coin_point',5:'transcend_ssr_coin_point'}.get(r['item_rating'],'')
    elif r['item_type']==28:key={4:'transcend_sr_eventcoin_point',5:'transcend_ssr_eventcoin_point'}.get(r['item_rating'],'')
    if key:out.append('{%d,%d},'%(r['item_id'],config[key]))
out += ['};','struct SuperAwakeningReset {int item,count;};','inline const SuperAwakeningReset SuperAwakeningResetCosts[]={']
out += ['{%d,%d},'%resetconfig[f'transcend_reset_use_item_{i}'] for i in (1,2)]
out += ['};', 'struct FarmingDrop { int item,count,weight; };',
        'struct EconomyStage { int mode,id,staminaItem,stamina,gold,heroExp,firstItem,firstCount,area,userExp; FarmingDrop drops[15]; };',
        'inline const EconomyStage EconomyStages[] = {']
for mode, table in [(0, 'DB_stage'), (1, 'DB_stage_week'), (2, 'DB_stage_boss'), (3, 'DB_stage_quest')]:
    rows = json.loads((root/f'Research/DecodedCache/{table}.json').read_text())
    for r in rows:
        drops = [(r.get(f'drop_item_id_{i}', 0), r.get(f'drop_item_value_{i}', 0), r.get(f'drop_item_per_{i}', 0)) for i in range(1, 16)]
        fields = [mode, r['id'], r.get('need_stamina_item_id', 0), r.get('need_stamina_count', 0),
                  r.get('gold_value', 0), r.get('hero_exp', 0), r.get('first_reward_id', 0), r.get('first_reward_value', 0), r.get('area', 0), r.get('user_exp', 0)]
        out.append('{%s,{%s}},' % (','.join(map(str, fields)), ','.join('{%d,%d,%d}' % d for d in drops)))
out += ['};', 'struct HeroCoin { int skin,coin; };', 'inline const HeroCoin HeroCoins[] = {']
out += ['{%d,%d},' % (r['id'], r['hero_coin']) for r in skins if r['hero_coin'] > 0]
out += ['};','struct QuestReward {int quest,item,count,type;};','inline const QuestReward QuestRewards[]={']
items={r['item_id']:r for r in json.loads((root/'Research/DecodedCache/items.json').read_text())}
for r in json.loads((root/'Research/DecodedCache/DB_quest.json').read_text()):
    for n in range(1,5):
        item=r.get(f'reward_item_id_{n}',0);count=r.get(f'reward_item_count_{n}',0)
        if item in items and count>0:out.append('{%d,%d,%d,%d},'%(r['id'],item,count,items[item]['item_type']))
out += ['};', '}']
(root/'Server/Protocol/LocalEconomyCatalog.h').write_text('\n'.join(out)+'\n')
print('Generated preserved finite-economy recipes, stage costs/rewards and duplicate coins')
