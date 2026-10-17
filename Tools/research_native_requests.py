from pathlib import Path
import contextlib,io,json
with contextlib.redirect_stdout(io.StringIO()):import map_login_read_schema as n
n.primitive.update({'uint16_t':'h','uint32_t':'i'})
terms=['CookingUseCookingBuff','FoodBuffAutoUse','RecipeActive','BasePointInfo','BasePointGoldDonation','BasePointDropInteractiveOpen','BasePointUniqueInteractiveOpen','BasePointDailyReward','ArtifactUnionUpgrade','FinalBoss','Tower','CreatureNest','Destroy','Descent','Subdue','CostumeUpgrade','WeaponChange','WeaponUpgradeReset']
for m in n.meta.values():
 if 'S2C' in m['Name'] and 'Stub$$ProcessReceivedMessage_' in m['Name'] and any(t in m['Name'] for t in terms):
  a=m['Address'];end=n.addresses[n.addresses.index(a)+1];ids=set();reads=[]
  for ins in n.n.decoder.disasm(n.n.data[n.n.offset(a):n.n.offset(a)+end-a],a):
   if ins.mnemonic=='mov' and ins.op_str.startswith(('w1, #','w8, #')):
    value=int(ins.op_str.split('#')[1],0)
    if 14000<=value<20000:ids.add(value)
   if ins.mnemonic=='bl':
    target=int(ins.op_str[1:],0)
    if target in n.meta and '$$Read' in n.meta[target]['Name']:reads.append(n.schema(target))
  print('RESPONSE',ids,m['Name'],''.join(reads))
for m in n.meta.values():
 if '.Proxy$$CG_' not in m['Name'] or not any(t in m['Name'] for t in terms) or 'int32_t remote,' not in m['Signature']:continue
 a=m['Address'];end=n.addresses[n.addresses.index(a)+1];value=None;rid=None
 for ins in n.n.decoder.disasm(n.n.data[n.n.offset(a):n.n.offset(a)+end-a],a):
  if ins.mnemonic=='mov' and ins.op_str.startswith('w1, #'):value=int(ins.op_str.split('#')[1],0)
  if ins.mnemonic=='bl' and ins.op_str=='#0x79e83bc':rid=value;break
 print(hex(a),rid,m['Name'],m['Signature'])
for m in n.meta.values():
 if m['Name'].endswith('$$Read') and any(', '+t+'_o** ' in m['Signature'] for t in ['BasePointInfo','BasePointRefreshInfo','UserNpc','UserNpcResultInfo','UserBasePointContentsInfo','UserBuffInfo','FinalBossInfo','DisasterTowerInfo']):
  print('READ',hex(m['Address']),n.schema(m['Address']),m['Signature'])
