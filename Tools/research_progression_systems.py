from pathlib import Path
import json,sys,io,contextlib
root=Path(__file__).resolve().parents[1]
s=(root/'Research/Il2CppDumper/dump.cs').read_text(encoding='utf8')
meta=json.loads((root/'Research/Il2CppDumper/script.json').read_text())['ScriptMethod']
names=['CG_RequestMissionProgress','CG_RequestMissionClear','CG_RequestMissionGetAchievePointReward','CG_RequestQuestChapterClear','CG_RequestQuestGuideListAllClearReward','CG_RequestQuestGuideListStepStart','CG_RequestQuestGuideListStepClear']
for r in meta:
 if any(n in r['Name'] for n in names) and (('Proxy' in r['Name'] and '$$CG_' in r['Name']) or 'Delegate$$Invoke' in r['Name']):print(hex(r['Address']),r['Name'],r['Signature'])
for name in ['DBMissionRow','DBMissionAchievepointRow','DBChapterRow','DBChapterGroupRow','DBGuidelistRewardRow','ClientSendMissionInfo','MissionClearRequestInfo','MissionClearResultInfo','QuestChapterClearInfo','MissionResult']:
 marker='public class '+name+' '
 if marker in s:
  a=s.index(marker);b=s.index('// Methods',a);print(s[a:b][:4500])
with contextlib.redirect_stdout(io.StringIO()):import map_login_read_schema as schemas
schemas.primitive['uint32_t']='i'
for r in meta:
 if 'Marshaler$$Read' in r['Name'] and any(n+'_o**' in r['Signature'] for n in ['MissionResult','ClientSendMissionInfo','MissionClearRequestInfo','MissionClearResultInfo','QuestChapterClearInfo']):print(hex(r['Address']),r['Signature'],schemas.schema(r['Address']))
import re
print('TABLES',re.findall(r'public class (DB\w*(?:Mission|QuestChapter|QuestGuide|Achieve)\w*Row) ',s))
