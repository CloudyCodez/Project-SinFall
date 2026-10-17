import json
from read_plain_table import root,read_table
q=read_table('DB_quest','DBQuestRow');st=json.loads((root/'Research/DecodedCache/DB_stage.json').read_text());rows=read_table('DB_quest_skip_info','DBQuestSkipInfoRow')
fmt=lambda x:'{'+','.join(map(str,x))+'}'
out=['#pragma once','namespace GcLocal {','struct ChapterSkipRule {int id,previous,cost;std::vector<int> quests,stages;};','inline const ChapterSkipRule ChapterSkipRules[]={']
for r in rows:
 if r['chapter_type_name']!='UI_chapter_type_001':continue
 quests=[x['id'] for x in q if x['region'] in r['list_array_quest_region'] and x['quest_class'] in r['list_array_quest_class'] and x['quest_group'] in r['list_array_quest_group']]
 stages=[x['id'] for x in st if x['id'] and ((x['region'] in r['list_array_quest_region'] and x['type'] in r['list_array_stage_type']) or (x['type']=='extra' and x['extra_group_id'] in r['list_array_event_stage_extra_group_id']))]
 out.append('{%d,%d,%d,%s,%s},'%(r['id'],r['active_condition_skip_id'],r['price_count'] if r['chapter_skip_enable'] else 0,fmt(quests),fmt(stages)))
out+=['};','inline const ChapterSkipRule* FindChapterSkip(int id){for(const auto& r:ChapterSkipRules)if(r.id==id)return &r;return nullptr;}','}']
(root/'Server/Protocol/LocalChapterSkipCatalog.h').write_text('\n'.join(out)+'\n')
print('Native story skip rules',len(out)-8)
