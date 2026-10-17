from pathlib import Path
import json,re,contextlib,io
root=Path(__file__).resolve().parents[1]
with contextlib.redirect_stdout(io.StringIO()):import map_login_read_schema as n
meta=n.meta
for m in meta.values():
 name=m['Name'];sig=m['Signature']
 if any(x in name for x in ['FoodBuffData','CookingData','RecipeActive','CookingUseCookingBuffOK','FoodBuffAutoUseOnOffOK']) and not '<' in name:print(hex(m['Address']),name,sig)
dump=(root/'Research/Il2CppDumper/dump.cs').read_text(encoding='utf8')
for cls in ['FoodBuffData','CookingData','MissionType','DBPvpShopRow','DBArtifactCardUnionRow']:
 match=re.search(r'public (?:class|enum) '+cls+r'\b.*?(?=// Methods|\n})',dump,re.S)
 if match:print(match[0])
for name in ['DB_cooking_recipe','DB_mission','DB_quest']:
 rows=json.loads((root/f'Research/DecodedCache/{name}.json').read_text())
 if name=='DB_cooking_recipe':print(name,rows[:3])
 else:
  rows=[r for r in rows if any('pvp' in str(v).lower() or 'arena' in str(v).lower() for k,v in r.items() if k in ['mission_type','quest_type','contents_menu','type'])]
  print(name,len(rows),rows[:4])
