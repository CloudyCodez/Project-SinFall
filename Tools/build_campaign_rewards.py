"""Preserve native campaign rewards and their item union types."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
items={r['item_id']:r['item_type'] for r in json.loads((root/'Research/DecodedCache/items.json').read_text())}
lines=['#pragma once','namespace GcLocal {','struct CampaignReward {int mode,stage,item,count,type;bool first;};','inline const CampaignReward CampaignRewards[]={']
for mode,table in [(0,'DB_stage'),(3,'DB_stage_quest')]:
 for r in json.loads((root/f'Research/DecodedCache/{table}.json').read_text()):
  for first,prefix in [(False,'reward'),(True,'first_reward')]:
   item=r.get(prefix+'_id_1' if not first else prefix+'_id',0)
   count=r.get(prefix+'_value_1' if not first else prefix+'_value',0)
   if item in items and count>0:
    lines.append('{%d,%d,%d,%d,%d,%s},'%(mode,r['id'],item,count,items[item],str(first).lower()))
lines+=['};','}']
(root/'Server/Protocol/LocalCampaignRewards.h').write_text('\n'.join(lines)+'\n',encoding='utf8')
print('Preserved native campaign reward types')
