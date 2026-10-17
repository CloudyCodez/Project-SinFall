from pathlib import Path
import json,re,contextlib,io
root=Path(__file__).resolve().parents[1]
meta=json.loads((root/'Research/Il2CppDumper/script.json').read_text())['ScriptMethod']
need=['CookingUseCookingBuff','FoodBuffAutoUse','RecipeActive','Basepoint','Npc','Donation','WeaponOption','WeaponBase','ArtifactUnionUpgrade','CostumeUpgrade','Destroy_Stage','DestroyStage','FinalBoss_Stage','FinalBossStage','SubdueBoss','Tower_Stage','TowerStage']
for m in meta:
 if 'SevenDSGameC2S.Proxy$$CG_' in m['Name'] and 'int32_t remote,' in m['Signature'] and any(n.lower() in m['Name'].lower() for n in need):print(hex(m['Address']),m['Name'],m['Signature'])
dump=(root/'Research/Il2CppDumper/dump.cs').read_text(encoding='utf8')
for name in ['FoodBuffInfo','DBCookingListRow','DBCookingRecipeRow','DBCookingBuffRow','DBBasepointNpcRow','DBBasepointRow','DBBasepointFellowshipRow','DBWeaponOptionChangeRow','DBArtifactUnionRow','UserArtifactUnionInfo']:
 marker='public class '+name+' '
 if marker in dump:
  a=dump.index(marker);b=dump.index('// Methods',a);print(dump[a:b])
with contextlib.redirect_stdout(io.StringIO()):import map_login_read_schema as native
for m in meta:
 if m['Name'].endswith('$$Read') and any(', '+n+'_o** ' in m['Signature'] for n in ['FoodBuffInfo','UserArtifactUnionInfo','UserRecipeInfo','UserBasepointInfo','UserNpcInfo','BasepointDonationResult']):print(hex(m['Address']),m['Signature'],native.schema(m['Address']))
