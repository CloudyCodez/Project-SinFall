"""Preserve native quest dependencies, objective types and campaign stage rules."""
import json
from pathlib import Path
from read_plain_table import read_table
root=Path(__file__).resolve().parents[1]
quests=json.loads((root/'Research/DecodedCache/DB_quest.json').read_text())
main=json.loads((root/'Research/DecodedCache/DB_stage.json').read_text())
town=read_table('DB_stage_quest','DBStageQuestRow')
areas=read_table('DB_area','DBAreaRow')
area_by_position={(r['region'],r['area']):r for r in areas}
(root/'Research/DecodedCache/DB_stage_quest.json').write_text(json.dumps(town),encoding='utf8')
def ints(values):return '{'+','.join(map(str,values))+'}'
lines=['#pragma once','namespace GcLocal {',
 'struct QuestRule {int id,parent;bool story;const char* type;std::vector<int> needs;int stageMode;};',
 'inline const QuestRule QuestRules[]={']
for q in quests:
 parent=q['open_value_1'] if q['open_class_1']=='quest_end' else 0
 mode={'main':0,'week':1,'boss':2,'quest':3,'free':4}.get(q['play_stage_type'],-1)
 if q['quest_type']=='battle_quest_count':mode=3
 lines.append('{%d,%d,%s,%s,%s,%d},'%(q['id'],parent,str(q['quest_class']=='story').lower(),json.dumps(q['quest_type']),ints(q['list_array_need_id']),mode))
lines+=['};','inline const QuestRule* FindQuestRule(int id){for(const auto& r:QuestRules)if(r.id==id)return &r;return nullptr;}',
 'struct CampaignStage {int mode,id,needStage,needQuest,startQuest;bool main;int monsters[10];int region=0,side=-1;bool mainRoute=false;};',
 'inline const CampaignStage CampaignStages[]={']
for mode,rows in [(0,main),(3,town)]:
 for r in rows:
  monsters=[r.get(f'monster_id_{i}',0) for i in range(1,7)]+[r.get(f'boss_id_{i}',0) for i in range(1,5)]
  area=area_by_position.get((r.get('region',0),r.get('area',0)),{})
  side=area.get('side',-1)
  route=mode==0 and side==0 and r.get('type') in ['main','sub_enemy','sub_reward']
  lines.append('{%d,%d,%d,%d,%d,%s,%s,%d,%d,%s},'%(mode,r['id'],r.get('need_stage_id',0),r.get('need_quest_id',0),r['start_quest_id'],str(mode==0 and r['type']=='main').lower(),ints(monsters),r.get('region',0),side,str(route).lower()))
lines+=['};','inline const CampaignStage* FindCampaignStage(int mode,int id){for(const auto& r:CampaignStages)if(r.mode==mode&&r.id==id)return &r;return nullptr;}','}']
(root/'Server/Protocol/LocalStoryRules.h').write_text('\n'.join(lines)+'\n',encoding='utf8')
assert len(quests)==2350
print('Preserved',sum(q['quest_class']=='story' for q in quests),'story quest rules and',len(town),'town quest battles')
