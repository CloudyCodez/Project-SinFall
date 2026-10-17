"""Generate permanent cosmetic grants from the matching preserved client database."""
from pathlib import Path
from read_plain_table import read_table
ROOT = Path(__file__).resolve().parents[1]
rows = read_table('DB_costume_base', 'DBCostumeBaseRow')
assert all(r['costume_type'] in (1, 2, 3) and 0 < r['hero_group'] < 256 for r in rows)
assert len({r['id'] for r in rows}) == len(rows)
output = '#pragma once\nnamespace GcLocal {\nstruct CosmeticRow { int id, type, heroGroup, group; };\ninline constexpr CosmeticRow Cosmetics[] = {\n'
output += ''.join('    {%d,%d,%d,%d},\n' % (r['id'], r['costume_type'], r['hero_group'], r['costume_group']) for r in rows)
output += '};\ninline const CosmeticRow* FindCosmetic(int id) { for (const auto& c : Cosmetics) if (c.id == id) return &c; return nullptr; }\n}\n'
(ROOT / 'Server/Protocol/LocalCosmeticCatalog.h').write_text(output)
print('Generated', len(rows), 'cosmetics')
