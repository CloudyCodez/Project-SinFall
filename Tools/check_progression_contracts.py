"""Validate progression wire layouts against preserved native readers."""
import contextlib,io,re,json
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):import map_login_read_schema as native
native.primitive['uint32_t']='i'
root=Path(__file__).resolve().parents[1]
def schema(name):
 matches=[m for m in native.n.metadata['ScriptMethod'] if m['Name'].endswith('$$Read') and (', '+name+'_o** ') in m['Signature'] and 'System_Collections_Generic_List_' not in m['Signature']]
 assert len(matches)==1,(name,len(matches))
 return native.schema(matches[0]['Address'])
for name,expected in {'MissionResult':'ccccccc','ClientSendMissionInfo':'ibi','MissionClearRequestInfo':'ib','MissionClearResultInfo':'cicccccccccii','QuestChapterClearInfo':'lllll','UpgradeUserSkin':'i'+schema('UserSkin'),'UserRecipeInfo':'iio','UserArtifactTeamInfo':'bic'}.items():
 assert schema(name)==expected,(name,schema(name),expected)
s=(root/'Server/Protocol/GrandCrossRmiTypes.h').read_text().split('inline const char* LoginUserZeroSchema()')[1].split('}')[0]
declared=''.join(re.findall(r'"([a-z]+)"',s));assert declared==native.schema(0x36b5ebc)[3:]
for index,token in {427:'c',432:'i',481:'l',542:'o',543:'b',583:'c',584:'c'}.items():assert declared[index]==token
quests=json.loads((root/'Research/DecodedCache/DB_quest.json').read_text())
guide=[q for q in quests if q['quest_class']=='guide_list'];assert len(guide)==60
assert all(sum((q['quest_group']-2000)//10==phase for q in guide)==3 for phase in range(1,21))
print('PASS: 8 native progression record layouts, full login schema, recipe/artifact/progression field widths and 20 native Hero\'s Way groups')
