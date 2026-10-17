"""Seed every preserved common-item kind, including modern growth currencies."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
rows=sorted((r for r in json.loads((root/'Research/DecodedCache/items.json').read_text()) if 0<r['item_type']<200 and r['item_id']>0),key=lambda r:r['item_id'])
assert len(rows)==len({r['item_id'] for r in rows})
assert {543301,543302,543303,543304,543305,500021,5301001,500019,912089,911424,542701,542702}.issubset({r['item_id'] for r in rows})
header='#pragma once\nnamespace GcLocal {\ninline constexpr int MaterialIds[] = {'+','.join(str(r['item_id']) for r in rows)+'};\n'
header+='struct MaterialType { int id,type; };\ninline constexpr MaterialType MaterialTypes[] = {\n'
header+='\n'.join('{%d,%d},'%(r['item_id'],r['item_type']) for r in rows)
header+='\n};\ninline int FindMaterialType(int id) { for(const auto& r:MaterialTypes)if(r.id==id)return r.type;return 0; }\n}\n'
(root/'Server/Protocol/LocalMaterialCatalog.h').write_text(header)
print('Generated',len(rows),'common inventory entries and native item types')
