from pathlib import Path
import UnityPy,json
from read_plain_table import read_table
root=Path(__file__).resolve().parents[1]
names={'DB_food_buff':'DBFoodBuffRow','DB_basepoint_fellow_reward':'DBBasepointFellowRewardRow','DB_town_donation_value_config':'DBTownDonationValueConfigRow','DB_artifact_card_union':'DBArtifactCardUnionRow','DB_pvp_shop':'DBPvpShopRow'}
env=UnityPy.load(str(root/'Research/DecodedCache/30FF13B981773B83827E17DB9C456368'))
for obj in env.objects:
 if obj.type.name!='TextAsset':continue
 a=obj.read()
 if any(x in a.m_Name for x in ['pvp','food_buff','artifact','donation','fellow','stage_final','stage_disaster']):print(a.m_Name)
 if a.m_Name in names:(root/f'Research/DecodedCache/{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
for name,cls in names.items():
 if not (root/f'Research/DecodedCache/{name}.bin').exists():continue
 try:
  rows=read_table(name,cls)
  (root/f'Research/DecodedCache/{name}.json').write_text(json.dumps(rows),encoding='utf8')
  print(name,len(rows),rows[:2])
 except Exception as e:print(name,type(e).__name__,str(e))
