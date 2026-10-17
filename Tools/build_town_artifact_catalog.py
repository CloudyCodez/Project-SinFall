from pathlib import Path
import json
from read_plain_table import read_table,write_table
root=Path(__file__).resolve().parents[1]
def rows(n):return json.loads((root/f'Research/DecodedCache/{n}.json').read_text())
out=['#pragma once','namespace GcLocal {','struct TownQuestReward{int quest,town,exp;};','inline const TownQuestReward TownQuestRewards[]={']
for q in rows('DB_quest'):
 if q['base_fellow_id'] and q['base_fellow_exp']>0:out.append('{%d,%d,%d},'%(q['id'],q['base_fellow_id'],q['base_fellow_exp']))
out+=['};','struct TownRule{int id,level,exp;};','inline const TownRule TownRules[]={']
for r in rows('DB_basepoint_fellow_reward'):out.append('{%d,%d,%d},'%(r['basepoint_id'],r['fellow_level'],r['fellow_exp']))
out+=['};','struct TownChest{int npc,town,index,quest,item,count;};','inline const TownChest TownChests[]={']
for r in rows('DB_basepoint_npc'):
 if r['reward_id_1']:out.append('{%d,%d,%d,%d,%d,%d},'%(r['id'],r['basepoint_id'],r['basepoint_index'],r['open_value'] if r['open_type']=='quest_end' else 0,r['reward_id_1'],r['reward_count_1']))
out+=['};','struct ArtifactUnionRule{int id,cap,cards[5];};','inline const ArtifactUnionRule ArtifactUnionRules[]={']
exp=read_table('DB_exp','DBExpRow')
for r in rows('DB_artifact_card_union'):
 candidates=[e[f"union_class_{r['reinforce_class']}"]^0x34343434 for e in exp if 0<(e['level']^0x34343434)<r['reinforce_max_level']]
 cap=max(candidates,default=0);assert 0<=cap<2147483647
 out.append('{%d,%d,{%s}},'%(r['union_id'],cap,','.join(str(r[f'union_card_{i}']) for i in range(1,6))))
out+=['};','struct UnionMaterial{int id,exp;};','inline const UnionMaterial UnionMaterials[]={']
for r in rows('items'):
 if r['item_type']==106:
  assert r['item_param_4']>0;out.append('{%d,%d},'%(r['item_id'],r['item_param_4']))
out+=['};','}']
(root/'Server/Protocol/LocalTownArtifactCatalog.h').write_text('\n'.join(out)+'\n')
assert write_table(read_table('DB_artifact_card_union','DBArtifactCardUnionRow'),'DBArtifactCardUnionRow')==(root/'Research/DecodedCache/DB_artifact_card_union.bin').read_bytes()
print('Verified native artifact table roundtrip; emitted town/chest rewards, 78 artifact sets and EXP caps')
