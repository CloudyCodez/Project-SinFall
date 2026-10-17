from pathlib import Path
import UnityPy,json
from read_plain_table import read_table,write_table
root=Path(__file__).resolve().parents[1]
names={'DB_final_boss_season':'DBFinalBossSeasonRow','DB_final_boss_setting':'DBFinalBossSettingRow','DB_stage_final_boss':'DBStageFinalBossRow','DB_stage_final_boss_event':'DBStageFinalBossEventRow','DB_stage_final_boss_group':'DBStageFinalBossGroupRow','DB_stage_tower':'DBStageTowerRow','DB_stage_tower_season':'DBStageTowerSeasonRow','DB_stage_creaturenest':'DBStageCreaturenestRow','DB_stage_creaturenest_info':'DBStageCreaturenestInfoRow'}
env=UnityPy.load(str(root/'Research/DecodedCache/30FF13B981773B83827E17DB9C456368'))
for obj in env.objects:
 if obj.type.name=='TextAsset':
  a=obj.read()
  if a.m_Name in names:(root/f'Research/DecodedCache/{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
for name,cls in names.items():
 try:
  rows=read_table(name,cls);assert write_table(rows,cls)==(root/f'Research/DecodedCache/{name}.bin').read_bytes()
  (root/f'Research/DecodedCache/{name}.json').write_text(json.dumps(rows),encoding='utf8')
  print(name,len(rows),{k:v for k,v in rows[0].items() if k in ['id','group_id','monster_id_1','boss_id_1','phase1_boss_id_1','season_id','event_id','reward_id','reward_count']})
 except Exception as e:print(name,type(e).__name__,str(e))
