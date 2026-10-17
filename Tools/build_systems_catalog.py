"""Native equipment, relic, box and True Awakening definitions."""
import json,struct
from pathlib import Path
from read_plain_table import read_table
root=Path(__file__).resolve().parents[1]
def decrypt(rows,mask):
 for r in rows:
  for k,v in r.items():
   if isinstance(v,int):
    x=(v&0xffffffff)^mask;r[k]=x if x<0x80000000 else x-0x100000000
 return rows
out=['#pragma once','namespace GcLocal {']
def emit(name,fields,rows):
 out.append('struct '+name+' { '+','.join([])+'int '+','.join(fields)+'; };')
 out.append('inline const '+name+' '+name+'Rows[] = {')
 for r in rows:out.append('{'+','.join(str(r[f]) for f in fields)+'},')
 out.append('};')
base=decrypt(read_table('DB_weapon_base','DBWeaponBaseRow'),0x14141414)
emit('EquipmentBase',['id','set_id','weapon_rating','weapon_parts','status_value_min','status_value_max','random_option_id'],base)
emit('EquipmentUpgrade',['weapon_rating','upgrade_level','upgrade_per','upgrade_material_id','upgrade_material_count','upgrade_price_id','upgrade_price_count','upgrade_fail_gauge'],decrypt(read_table('DB_weapon_upgrade','DBWeaponUpgradeRow'),0x6b6b6b6b))
emit('EquipmentEvolution',['weapon_rating','evolution_count','evolution_material_id','evolution_material_count','evolution_price_id','evolution_price_count'],read_table('DB_weapon_evolution','DBWeaponEvolutionRow'))
grind=decrypt(read_table('DB_weapon_grind','DBWeaponGrindRow'),0x58585858)
for r in grind:
 for i in range(1,7):
  k=f'evolution_item_rate_{i}'
  r[k]=round(struct.unpack('<f',struct.pack('<I',r[k]&0xffffffff))[0]*100)
emit('EquipmentGrind',['weapon_rating','weapon_enchant','fellowship_level','grind_item_id']+sum(([f'bonus_rate_{i}',f'grind_item_count_{i}',f'evolution_item_count_{i}'] for i in range(1,4)),[])+[f'evolution_item_rate_{i}' for i in range(1,7)],grind)
emit('EquipmentBaseChange',['weapon_rating','need_material_id_1','need_material_count_1','need_material_id_2','need_material_count_2','need_material_id_3','need_material_count_3'],read_table('DB_weapon_base_change','DBWeaponBaseChangeRow'))
changes=read_table('DB_weapon_option_change','DBWeaponOptionChangeRow')
for r in changes:r['reroll']=int(r['change_type']=='change')
emit('EquipmentOptionChange',['weapon_rating','evolution_count','reroll','change_material_id','change_material_count','change_price_id','change_price_count','option_change_min_1','option_rate_1','option_change_min_2','option_rate_2'],changes)
opts=decrypt(read_table('DB_weapon_option','DBWeaponOptionRow'),0xb8b8b8b8)
for r in opts:
 for k in ('option_effect_min','option_effect_max'):
  r[k]=round(struct.unpack('<f',struct.pack('<I',r[k]&0xffffffff))[0]*10)
emit('EquipmentOption',['id','random_option_group','option_effect_id','option_effect_min','option_effect_max'],opts)
emit('EquipmentCarve',['weapon_rating','weapon_parts','carve_item_id_1','carve_item_count_1','carve_item_id_2','carve_item_count_2','carve_price_id','carve_price_count','carve_clear_price_id','carve_clear_price_count'],read_table('DB_weapon_carve_base','DBWeaponCarveBaseRow'))
growth=read_table('DB_weapon_growth','DBWeaponGrowthRow')
for r in growth:r['fixed_option_tenths']=round(r['evolution_option_amount_set']*10)
emit('EquipmentGrowth',['id','item_id','weapon_evolution_count','weapon_upgrade_count','is_carve','weapon_status_amount','evolution_option_amount','fixed_option_tenths']+[f'evolution_option_{i}' for i in range(1,6)],growth)
items=json.loads((root/'Research/DecodedCache/items.json').read_text())
emit('EquipmentSale',['item_id','sell_on','sell_id','sell_cost'],[r for r in items if r['item_type']==212])
emit('EquipmentTicket',['item_id','item_param_1'],[r for r in items if r['item_type']==103])
selection=read_table('DB_selected_exchange_info','DBSelectedExchangeInfoRow')
for r in selection:
 r['weapon_upgrade_count']=r['Weapon_upgrade_count']
 r['fixed_option_tenths']=round(r['evolution_option_amount_set']*10)
emit('EquipmentSelection',['id','select_group','item_id','weapon_evolution_count','weapon_upgrade_count','weapon_status_amount','evolution_option_amount','fixed_option_tenths']+[f'evolution_option_{i}' for i in range(1,6)],selection)
emit('EquipmentSelectionTicket',['item_id','item_param_1'],[r for r in items if r['item_type']==77])
craft=read_table('DB_costume_craft','DBCostumeCraftRow')
for r in craft:r['quick_token']=543200+r['list_array_creaturenest_boss_group'][0]+0 if r['list_array_creaturenest_boss_group'] else 0
# Boss groups 101..105 correspond to quick-craft tokens 543301..543305.
fields=['costume_id','quick_token','collabo_type','need_gold_id','need_gold']+sum(([f'need_item_{i}',f'need_item_count_{i}'] for i in range(1,5)),[])
emit('RelicRecipe',fields,craft)
fields=['hero_id','exceed_type','exceed_price_id','exceed_price_count']+sum(([f'exceed_material_id_{i}',f'exceed_material_count_{i}'] for i in range(1,5)),[])
emit('TrueAwakeningRecipe',fields,read_table('DB_skin_exceed','DBSkinExceedRow'))
boxrows=read_table('DB_box_item_info','DBBoxItemInfoRow')
fields=['item_id','box_type']+sum(([f'item_id_{i}',f'item_count_{i}',f'item_rate_{i}'] for i in range(1,21)),[])
emit('ItemBox',fields,boxrows)
out+=['}'];(root/'Server/Protocol/LocalSystemsCatalog.h').write_text('\n'.join(out)+'\n')
print('Generated',len(base),'equipment bases,',len(craft),'relics and',len(boxrows),'boxes')
