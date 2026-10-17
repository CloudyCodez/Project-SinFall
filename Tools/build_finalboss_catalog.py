from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
def rows(n):return json.loads((root/f'Research/DecodedCache/{n}.json').read_text())
stages=rows('DB_stage_final_boss')
out=['#pragma once','#include "LocalEconomyCatalog.h"','namespace GcLocal {','struct FinalBossStage{int id,group,monsters[9];};','inline const FinalBossStage FinalBossStages[]={']
for r in stages:
 monsters=[r.get(f'phase{phase}_boss_id_{i}',r.get(f'Phase{phase}_boss_id_{i}',0)) for phase in range(1,4) for i in range(1,4)]
 assert any(monsters);out.append('{%d,%d,{%s}},'%(r['id'],r['group_id'],','.join(map(str,monsters))))
out+=['};','inline const FinalBossStage* FindFinalBoss(int id){for(const auto& r:FinalBossStages)if(r.id==id)return &r;return nullptr;}','inline const EconomyStage FinalBossEconomy[]={']
for r in stages:
 drops=[(r[f'drop_item_id_{i}'],r[f'drop_item_value_{i}'],r[f'drop_item_per_{i}']) for i in range(1,6)]+[(0,0,0)]*10
 out.append('{5,%d,%d,%d,%d,%d,%d,%d,%d,%d,{%s}},'%(r['id'],r['need_stamina_item_id'],r['need_stamina_count'],r['gold_value'],r['hero_exp'],r['first_reward_id'],r['first_reward_value'],r['area'],r['user_exp'],','.join('{%d,%d,%d}'%p for p in drops)))
out+=['};','struct FinalBossSetting{int id,group,season;};','inline const FinalBossSetting FinalBossSettings[]={']
valid={r['group_id'] for r in stages};settings={}
for r in rows('DB_final_boss_setting'):
 if r['group_id'] in valid and r['group_active']:settings[r['group_id']]=r
for r in settings.values():out.append('{%d,%d,%d},'%(r['id'],r['group_id'],r['season_id']))
out+=['};','}']
(root/'Server/Protocol/LocalFinalBossCatalog.h').write_text('\n'.join(out)+'\n')
print('Final Boss:',len(stages),'stages',len(settings),'permanent native boss groups')
