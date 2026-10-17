"""Preserve chapter, Hero's Way and standard mission rules."""
from pathlib import Path
import UnityPy,json,re
from read_plain_table import read_table
root=Path(__file__).resolve().parents[1]
names={'DB_mission':'DBMissionRow','DB_mission_achievepoint':'DBMissionAchievepointRow','DB_chapter':'DBChapterRow','DB_guidelist_reward':'DBGuidelistRewardRow'}
env=UnityPy.load(str(root/'Research/DecodedCache/30FF13B981773B83827E17DB9C456368'))
for obj in env.objects:
 if obj.type.name=='TextAsset':
  a=obj.read()
  if a.m_Name in names:(root/f'Research/DecodedCache/{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
rows={}
for name,cls in names.items():
 rows[name]=read_table(name,cls)
 (root/f'Research/DecodedCache/{name}.json').write_text(json.dumps(rows[name]),encoding='utf8')
 print(name,len(rows[name]),rows[name][:2])

dump=(root/'Research/Il2CppDumper/dump.cs').read_text(encoding='utf8')
enum=dump.split('public enum MissionType ')[1].split('\n}')[0]
types={n.lower():int(v) for n,v in re.findall(r'public const MissionType (\w+) = (\d+);',enum)}
out=['#pragma once','namespace GcLocal {',
 'struct MissionRule{int chain,index,type,value,target,item,count,points;};',
 'inline const MissionRule MissionRules[]={']
for r in rows['DB_mission']:
 assert r['mission_type'].lower() in types and 0<r['chain_index']<256
 out.append('{%d,%d,%d,%d,%d,%d,%d,%d},'%(r['chain_id'],r['chain_index'],types[r['mission_type'].lower()],r['mission_type_value'],r['mission_target_value'],r['reward_item_id_1'],r['reward_item_count_1'],r['reward_achievepoint_Value']))
out+=['};','struct AchievementRule{int order,target,item,count;};','inline const AchievementRule AchievementRules[]={']
for r in rows['DB_mission_achievepoint']:out.append('{%d,%d,%d,%d},'%(r['reward_order'],r['mission_target_value'],r['reward_item_id_1'],r['reward_item_count_1']))
out+=['};','struct GuideReward{int step,skin;};','inline const GuideReward GuideRewards[]={']
for r in rows['DB_guidelist_reward']:
 assert r['skin_level']==90 and r['skin_awaken']==6
 out.append('{%d,%d},'%(r['quest_phase'],r['reward_item_id']))
quests=json.loads((root/'Research/DecodedCache/DB_quest.json').read_text())
out+=['};','struct GuideQuest{int quest,step;};','inline const GuideQuest GuideQuests[]={']
for r in quests:
 if r['quest_class']=='guide_list':out.append('{%d,%d},'%(r['id'],(r['quest_group']-2000)//10))
out+=['};','struct ChapterRule{int region,index,item,count;std::vector<int> quests;};','inline const ChapterRule ChapterRules[]={']
# Native AllClearQuestCheckInfo first finds Story/Side, then removes Side/Loop.
for r in rows['DB_chapter']:
 if r['chapter_type']=='region_story' and r['chapter_clear_index']>0:
  need=[q['id'] for q in quests if q['region']==r['matching_region'] and q['quest_class']=='story']
  out.append('{%d,%d,%d,%d,{%s}},'%(r['matching_region'],r['chapter_clear_index'],r['reward_item_id'],r['reward_item_count'],','.join(map(str,need))))
out+=['};','struct AccountLevel{int level,exp;};','inline const AccountLevel AccountLevels[]={']
for r in read_table('DB_exp','DBExpRow'):
 level=r['level']^0x34343434;exp=r['user_exp']^0x34343434
 if level>0 and 0<=exp<2147483647:out.append('{%d,%d},'%(level,exp))
out+=['};','}']
(root/'Server/Protocol/LocalProgressionCatalog.h').write_text('\n'.join(out)+'\n',encoding='utf8')
print('Generated native progression catalog')
