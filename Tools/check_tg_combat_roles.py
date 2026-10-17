"""Check native TG faction/target/stat contracts against saved runtime tables."""
import json,struct
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def table(n):return json.loads((root/f'Research/DecodedCache/{n}.tg.offline.json').read_text())
decode=lambda x,mask:(x^mask)&0xffffffff
value=lambda x:struct.unpack('<f',struct.pack('<I',decode(x,0x4c4c4c4c)))[0]
units=json.loads((root/'Research/TokyoGhoul/roster-port-inventory.json').read_text())
roles=json.loads((root/'Research/TokyoGhoul/combat-role-refinement.json').read_text())
by_source={u['source']:u for u in units}
heroes={decode(r['id'],0x92929292):r for r in table('DB_hero_base')}
groups={r['id']:r for r in table('DB_hero_job_group')}
assert groups[12]['hero_job_group_name']==1400900, 'Dragon Ball membership must survive'
passives={decode(r['id'],0x4c4c4c4c):r for r in table('DB_skill_passive')}
exclusive={r['hero_id']:r for r in table('DB_skin_exclusive_passive')}
skins={r['id']:r for r in table('DB_skin_base')}
cards={decode(r['id'],0x65656565):r for r in table('DB_skill_card_base')}
options={decode(r['id'],0xbdbdbdbd):r for r in table('DB_skill_card_option')}
assert len(roles)==52
for role in roles:
    u=by_source[role['source']];group=role['faction_bonus']
    if group:
        assert group in heroes[u['hero']]['list_array_hero_job_group']
        assert u['hero'] in groups[group]['list_array_hero_id']
        p=passives[exclusive[u['hero']]['exclusive_passive_id_1']]
        assert p['effect_keyword']=='pass_one_array_apply_hero_job_group_atk_def_hp_inc_per_ally'
        assert p['list_array_apply_hero_job_group']==[group] and decode(p['kind_target'],0x4c4c4c4c)==0
        assert p['target']=='self' and p['sub_invoke_passive']==1 and value(p['effect_value']) in (8,10)
    for offset in (1,2,3,11,12,13,90):
        c=cards[u['skill_base']+offset]
        assert c['target']==(4 if c['range_type']==2 else 2), (u['source'],offset)
    for sid in (u['ssr'],u['ur']):
        assert all(skins[sid][k]>0 for k in ('atk','def','hp','atk_add','def_add','hp_add'))
    if role['role']=='support':
        for rank in (1,2,3):
            c=cards[u['skill_base']+10+rank]
            assert any(options[id]['effect_keyword']=='skill_dmg_per_heal_ally_all' for id in c['list_array_option_id_list'])
# Roles must differ numerically, rather than only their names/descriptions.
samples={role['role']:skins[by_source[role['source']]['ur']] for role in roles if role['source']!='1065'}
assert set(samples)=={'support','tank','elite damage','damage'}
assert samples['support']['hp']>samples['damage']['hp']
assert samples['elite damage']['atk']>samples['support']['atk']
assert samples['tank']['def']>samples['damage']['def']
print('PASS: 52 roles, CCG/Anteiku native formation filters, distinct stats, all TG AoE damage targets')
