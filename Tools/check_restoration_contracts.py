"""Check local response layouts against independently recovered native client readers."""
import contextlib, io, json, re
from pathlib import Path
with contextlib.redirect_stdout(io.StringIO()):
    import map_login_read_schema as native
ROOT = Path(__file__).resolve().parents[1]
def schema(name):
    matches=[x for x in native.n.metadata['ScriptMethod'] if ', '+name+'_o** ty,' in x.get('Signature','') and x['Name'].endswith('$$Read')]
    assert len(matches)==1, (name,len(matches))
    return native.schema(matches[0]['Address'])
skin=schema('UserSkin')
checks={'SkinOneStepEvolutionResult':'ii'+skin+'c'*9,
        'SkinEvolutionResult':'i'+skin+'c'*9,
        'SkinEvolutionBreakResult':skin+'c'*9,
        'SkinSkillLevelUpResult':skin+'c'*9,
        'QuestProgressInfo':'ibcb',
        'QuestClearResultInfo':'ii'+'c'*10+'i'*8+'ccb',
        'UserCostumeSkin':'iibbid', 'UserCostumeWeapon':'iibbid','UserCostumeHead':'iibbid'}
for name,expected in checks.items(): assert schema(name)==expected,(name,schema(name),expected)
# Resolve the exact package tokens/settings from the preserved native configuration.
from read_plain_table import read_table
import struct
configs={r['contents']:r for r in read_table('DB_config_game','DBConfigGameRow')}
for key,item in [('one_step_evolution_item_lite',912089),('one_step_evolution_item_package',911424)]:
    r=configs[key];assert r['value_int_1']^0x3b3b3b3b==item
    assert r['value_int_2']^0x3b3b3b3b==1
for key in ['one_step_evolution_lite','one_step_evolution_package']:
    r=configs[key];assert [r[k]^0x3b3b3b3b for k in ['value_int_1','value_int_2']]==[6,6]
    assert struct.unpack('<f',struct.pack('<I',r['value_float_1']^0x3b3b3b3b))[0]==90
quests=json.loads((ROOT/'Research/DecodedCache/DB_quest.json').read_text())
ids={q['id'] for q in quests}
assert len(ids)==len(quests)
assert all(q['next_story_quest']==0 or q['next_story_quest'] in ids for q in quests if q['quest_class']=='story')
material_header=(ROOT/'Server/Protocol/LocalMaterialCatalog.h').read_text()
materials=list(map(int,re.findall(r'\d+',re.search(r'MaterialIds\[\] = \{(.*?)\}',material_header,re.S)[1])))
assert len(materials)==len(set(materials)), 'Duplicate inventory IDs'
assert {500019,5301001,5301002,5301101,5301102,540001,542701}.issubset(materials),'Missing awakening/growth materials'
for filename in ['local-test-account-skins.txt','local-test-development.txt','local-test-passives.txt','local-test-cosmetics.txt']:
    assert (ROOT/'Server'/filename).exists(), filename
print('PASS: 9 native wire contracts, story chain references, unique inventory IDs, preserved account files')
