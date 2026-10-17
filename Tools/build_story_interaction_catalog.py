"""Extract preserved native cooking and town shop rules."""
from pathlib import Path
import UnityPy,json,re
from read_plain_table import read_table
root=Path(__file__).resolve().parents[1]
names={'DB_cooking_list':'DBCookingListRow','DB_cooking_recipe':'DBCookingRecipeRow','DB_cooking_material':'DBCookingMaterialRow','DB_basepoint_shop':'DBBasepointShopRow','DB_basepoint_npc':'DBBasepointNpcRow'}
env=UnityPy.load(str(root/'Research/DecodedCache/30FF13B981773B83827E17DB9C456368'))
for obj in env.objects:
 if obj.type.name=='TextAsset':
  a=obj.read()
  if a.m_Name in names:(root/f'Research/DecodedCache/{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
rows={}
for name,cls in names.items():
 rows[name]=read_table(name,cls)
 (root/f'Research/DecodedCache/{name}.json').write_text(json.dumps(rows[name]),encoding='utf8')
 print(name,len(rows[name]))
lines=['#pragma once','namespace GcLocal {',
 'struct CookingRule {int id,materials[3],food,minCount,maxCount,quest;};',
 'inline const CookingRule CookingRules[]={']
for r in rows['DB_cooking_list']:
 lines.append('{%d,{%d,%d,%d},%d,%d,%d,%d},'%(r['id'],r['material_id_1'],r['material_id_2'],r['material_id_3'],r['reward_id_1'],r['reward_count_min_1'],r['reward_count_max_1'],r['quest_index']))
lines+=['};','struct RecipeRule {int id,cooking,maxExp,experience;};','inline const RecipeRule RecipeRules[]={']
for r in rows['DB_cooking_recipe']:
 exp=next((m['recipe_exp'] for m in rows['DB_cooking_material'] if m['recipe_link']==r['id']),0)
 lines.append('{%d,%d,%d,%d},'%(r['id'],r['cooking_list_link'],r['max_exp'],exp))
lines+=['};','struct TownShopRule {int id,town,item,count,currency,price,limit,level;};','inline const TownShopRule TownShopRules[]={']
for r in rows['DB_basepoint_shop']:
 lines.append('{%d,%d,%d,%d,%d,%d,%d,%d},'%(r['id'],r['basepoint_id'],r['product_id'],r['product_count'],r['price_id'],r['price_count'],r['buy_limited_count'],r['need_fellow_level']))
lines+=['};','struct QuestItemRule {int quest,item,count;bool keep;};','inline const QuestItemRule QuestItemRules[]={']
for r in json.loads((root/'Research/DecodedCache/DB_quest.json').read_text()):
 lines.append('{%d,%d,%d,%s},'%(r['id'],r['give_quest_item_id'],r['give_quest_item_count'],str(bool(r['need_item_keep'])).lower()))
lines+=['};','}']
(root/'Server/Protocol/LocalStoryInteractionsCatalog.h').write_text('\n'.join(lines)+'\n',encoding='utf8')
