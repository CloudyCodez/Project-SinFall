"""Verify actual saved wardrobe links, LR recipe and non-obtainable legacy rows."""
import json, re, struct
from pathlib import Path
root=Path(__file__).resolve().parents[1]
def table(name):return json.loads((root/f'Research/DecodedCache/{name}.tg.offline.json').read_text())
units=json.loads((root/'Research/TokyoGhoul/roster-port-inventory.json').read_text())
migration=json.loads((root/'Research/TokyoGhoul/wardrobe-migration.json').read_text())
assert len(migration['kept'])==52 and len(migration['migrations'])==69
kept=[u for u in units if u['source'] in migration['kept']]
assert {u['source'] for u in kept if u['name']=='Ken Kaneki'}=={'1007','1065'}
costumes={r['id']:r for r in table('DB_costume_base')}
resource_tables={name:{r['id']:r for r in table(name)} for name in ['DB_skin_costume_resource','DB_head_costume_resource','DB_weapon_costume_resource']}
for u in units:
    for field,name in [('body','DB_skin_costume_resource'),('head','DB_head_costume_resource'),('weapon','DB_weapon_costume_resource')]:
        assert resource_tables[name][u[field]]['character_base']==u['model'], (u['source'],field,'Outfit must retain its own original model')
by_source={u['source']:u for u in units}
header=(root/'Server/Protocol/LocalTgWardrobe.h').read_text()
cosmetic_catalog=(root/'Server/Protocol/LocalCosmeticCatalog.h').read_text()
for u in units:
    for field,typ in [('body',1),('head',3),('weapon',2)]:
        row=costumes[u[field]]
        assert '{%d,%d,%d,%d},'%(u[field],typ,row['hero_group'],row['costume_group']) in cosmetic_catalog, 'Login ownership packet must include every outfit part'
for mapping in migration['migrations']:
    old=by_source[mapping['source']];new=by_source[mapping['canonical']]
    for field in ['body','head','weapon']:
        c=costumes[old[field]]
        assert c['hero_group']==mapping['group'] and c['list_array_matching_hero_id']==[new['hero']]
        assert c['list_array_costume_hide_hero_id']==[new['hero']], 'Empty display-hero list hides the costume'
    for old_field,new_field in [('old_ssr','ssr'),('old_ur','ur')]:
        assert '{%d,%d,%d,%d,%d},'%(mapping[old_field],mapping[new_field],mapping['old_hero'],mapping['hero'],mapping['group']) in header
old_skins={m[k] for m in migration['migrations'] for k in ['old_ssr','old_ur']}
heroes={(r['id']^0x92929292)&0xffffffff:r for r in table('DB_hero_base')}
groups={(heroes[u['hero']]['hero_group']^0x92929292)&0xffffffff for u in kept}
assert len(groups)==len(kept) and max(groups)<=255
assert len({costumes[u[field]]['costume_group'] for u in units for field in ['body','head','weapon']})==len(units)*3
assert not any(r['skin_id'] in old_skins for r in table('DB_gamble_group'))
skins={r['id']:r for r in table('DB_skin_base')}
for mapping in migration['migrations']:
    assert ((heroes[mapping['old_hero']]['hero_display']^0x92929292)&0xffffffff)==0, 'Legacy variant must not remain a locked roster hero'
    assert ((heroes[mapping['hero']]['hero_display']^0x92929292)&0xffffffff)==1
    old=by_source[mapping['source']]
    for sid in [mapping['old_ssr'],mapping['old_ur']]:
        assert skins[sid]['matching_hero_id']==mapping['hero'], 'Native base-costume owner must be the retained hero'
        assert skins[sid]['category_group']==mapping['hero']
    for field in ['body','head','weapon']:
        assert '{%d,%d},'%(old[field],mapping['hero']) in header, 'Login must grant the outfit to its retained owner'
lr=skins[399950];ur=skins[399502]
assert lr['rating']==7 and lr['matching_hero_id']==2995001
assert all(lr[k]==ur[k]*2 for k in ['atk','def','hp','atk_add','def_add','hp_add'])
assert lr['skin_portrait_base']==ur['skin_portrait_base']
assert any(r['matching_hero_id']==2995001 and r['evolution_rating']==6 for r in table('DB_skin_evolution'))
assert '{1,2995001,6,0,' in (root/'Server/Protocol/LocalEconomyCatalog.h').read_text()
skill=next(r for r in table('DB_skin_skill') if r['id']==399950)
cards={(r['id']^0x65656565)&0xffffffff:r for r in table('DB_skill_card_base')}
options={(r['id']^0xbdbdbdbd)&0xffffffff:r for r in table('DB_skill_card_option')}
for key in ['skill_a_1_id','skill_b_1_id','special_id_1']:
    card=cards[skill[key]]
    assert all(i in options for i in card['list_array_option_id_list'])
assert cards[skill['special_id_1']]['target']==4
assert {options[i]['effect_keyword'] for i in cards[skill['special_id_1']]['list_array_option_id_list']}=={'skill_hp_steal_add_per','skill_stamina_dec'}
assert 'BackupTgWardrobeSaves' in header and '.tg-wardrobe-v1.bak' in header
print('PASS: 69 wardrobe mappings, 52 obtainable heroes, preserved legacy rows, save backups, Centipede LR recipe/stats/cards')
