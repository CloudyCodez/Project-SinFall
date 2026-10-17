from pathlib import Path
import json,re
root=Path(__file__).resolve().parents[1]
def rows(n):return json.loads((root/f'Research/DecodedCache/{n}.json').read_text())
out=['#pragma once','namespace GcLocal {','struct FoodRule {int id,uses,minutes,passive;bool combat;};','inline const FoodRule FoodRules[]={']
for r in rows('DB_food_buff'):out.append('{%d,%d,%d,%d,%s},'%(r['id'],r['use_count'],r['use_time_min'],r['passive_id'],str(r['passive_type']!='contents').lower()))
out+=['};','struct FoodRewardRule{int id,gold,experience;};','inline const FoodRewardRule FoodRewardRules[]={']
for x in rows('DB_contents_passive'):
 if x['effect_keyword'] in ('stage_gold_inc_per','hero_exp_inc_per'):out.append('{%d,%d,%d},'%(x['id'],x['effect_per'] if x['effect_keyword']=='stage_gold_inc_per' else 0,x['effect_per'] if x['effect_keyword']=='hero_exp_inc_per' else 0))
out+=['};','struct RecipeBook{int recipe,item;};','inline const RecipeBook RecipeBooks[]={']
for r in rows('DB_cooking_recipe'):out.append('{%d,%d},'%(r['id'],r['material_id']))
dump=(root/'Research/Il2CppDumper/dump.cs').read_text(encoding='utf8')
enum=dump.split('public enum MissionType ')[1].split('\n}')[0]
pvp_types=[int(v) for n,v in re.findall(r'public const MissionType (\w+) = (\d+);',enum) if 'pvp' in n.lower() or 'arena' in n.lower()]
out+=['};','inline bool PvpMissionType(int type){switch(type){'+''.join('case %d:'%v for v in pvp_types)+'return true;default:return false;}}','inline const int PvpQuestIds[]={']
quests=[r for r in rows('DB_quest') if any('pvp' in str(r[k]).lower() or 'arena' in str(r[k]).lower() for k in ['quest_type','play_stage_type'])]
out.append(','.join(str(r['id']) for r in quests))
items={i['item_id']:i for i in rows('items')}
out+=['};','struct PvpUnlockItem{int source,item,count,type;};','inline const PvpUnlockItem PvpUnlockItems[]={']
# Each native shop product is granted once; purchase limits do not inflate the grant.
for r in rows('DB_pvp_shop'):out.append('{%d,%d,%d,%d},'%(r['id'],r['shop_item_id'],r['product_count'],items[r['shop_item_id']]['item_type']))
out+=['};','}']
(root/'Server/Protocol/LocalFoodPvpCatalog.h').write_text('\n'.join(out)+'\n')
print('Food rules',len(rows('DB_food_buff')),'PvP quests',len(quests),'PvP mission types',pvp_types,'PvP shop products',len(rows('DB_pvp_shop')))
