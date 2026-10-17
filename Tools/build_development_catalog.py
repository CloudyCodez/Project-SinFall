"""Build local development limits from the matching client tables."""
import json
from pathlib import Path
from read_plain_table import read_table

root = Path(__file__).resolve().parents[1]
rows = read_table('DB_exp', 'DBExpRow')
# DBExpRow.XOROperand is 0x234; ToXORByteArray truncates it per byte.
exp = {r['level'] ^ 0x34343434: {k: v ^ 0x34343434 for k, v in r.items() if k.startswith('rank_exp_')} for r in rows}
skins = json.loads((root / 'Research/DecodedCache/skins.json').read_text())
items = json.loads((root / 'Research/DecodedCache/items.json').read_text())
out = ['#pragma once', 'namespace GcLocal {', 'struct DevelopmentSkin { int id, maxExp, rating, maxLevel; };', 'inline constexpr DevelopmentSkin DevelopmentSkins[] = {']
for s in skins:
    level = s['max_level']
    limit = exp.get(level - 1, {}).get(s['select_rank_exp'], 0)
    assert 0 <= limit < 1000000000
    out.append(f'{{{s["id"]},{limit},{s["rating"]},{s["max_level"]}}},')
out += ['};', 'struct ExperienceMaterial { int id, exp; };', 'inline constexpr ExperienceMaterial ExperienceMaterials[] = {']
for i in items:
    if i['item_type'] == 31 and i['item_param_4'] > 0:
        out.append(f'{{{i["item_id"]},{i["item_param_4"]}}},')
out += ['};', 'struct ExperienceLevel { int level, rank2, rank3, rank4; };', 'inline constexpr ExperienceLevel ExperienceLevels[] = {']
for level, row in sorted(exp.items()):
    out.append('{%d,%d,%d,%d},' % (level, row.get('rank_exp_2', 0), row.get('rank_exp_3', 0), row.get('rank_exp_4', 0)))
out += ['};', '}']
(root / 'Server/Protocol/LocalDevelopmentCatalog.h').write_text('\n'.join(out) + '\n')
print(f'Generated development limits for {len(skins)} skins.')
