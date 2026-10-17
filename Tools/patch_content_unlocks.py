"""Remove content entry gates without changing recorded story/quest progress."""
import json,struct
from pathlib import Path
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
ROOT=Path(__file__).resolve().parents[1]
UNLOCKS={
 'Util$$IsOpenConditionCheck': [0x4342fc8,0x43430ec],
 'Util$$IsTrainingContentsOpen':[0x4346318],
 'SupremeDeityData$$IsContentsOpenQuest':[0x44d04e0],
 'DemonLordData$$IsContentsOpenQuest':[0x4d898fc],
 'ArtifactData$$IsArtifactOpenCondition':[0x4e4ff18],
 'ArtifactData$$IsOpenContents':[0x4e50ab0],
 'Util$$IsOpenBattleMenu':[0x434555c],
 'GameDataContainer$$IsActiveCheckArea':[0x4f3326c],
 'GameDataContainer$$IsWeekTutorialClearArea':[0x4f38794],
 'Util$$IsUnlockItemInventory':[0x4342ef4],
 'AccountDependentStateVariableCollection$$get_IsWeekOpen':[0x463e3ac],
}
def patch(path):
 data=bytearray(path.read_bytes());phoff=struct.unpack_from('<Q',data,32)[0];size,count=struct.unpack_from('<HH',data,54)
 segments=[struct.unpack_from('<IIQQQQQQ',data,phoff+i*size) for i in range(count)]
 metadata={m['Address']:m for m in json.loads((ROOT/'Research/Il2CppDumper/script.json').read_text())['ScriptMethod']}
 assembler=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN);records=[]
 # Only the progression check that opens limit breaking is bypassed. The
 # surrounding native code still calculates each hero's actual cap and checks
 # level, upgrade step and materials.
 address=0x5425190
 assert metadata[0x5425098]['Name']=='SkinData$$UpdatePublicEvolutionBreakMaxID'
 assert metadata[0x520b584]['Name']=='UserStageData$$IsStageClear'
 segment=next(s for s in segments if s[0]==1 and s[3]<=address<s[3]+s[5]);offset=segment[2]+address-segment[3]
 original=bytes(assembler.asm('bl #0x520b584',addr=address)[0]);code=bytes(assembler.asm('mov w0,#1',addr=address)[0])
 assert bytes(data[offset:offset+4]) in (original,code),'Unexpected limit-break gate instruction'
 data[offset:offset+4]=code
 records.append({'name':'Limit break access from login','address':hex(address),'bytes':code.hex()})
 # The battle-menu Solgres shortcut first checks its lock overlay and then
 # invokes ContentsLinkHelper in condition-check-only mode. Its native
 # selection/GoRegionUI path follows these checks; keep that navigation.
 assert metadata[0x41555d4]['Name']=='PageLobbyBattleMenu$$OnClickMoveWeekStage'
 for address,label,original_instruction,instruction in [
  (0x41556a8,'Solgres shortcut lock overlay','bl #0x813a1a0','mov w0,#0'),
  (0x41557dc,'Solgres shortcut content condition','bl #0x408dcb8','mov w0,#1')]:
  segment=next(s for s in segments if s[0]==1 and s[3]<=address<s[3]+s[5]);offset=segment[2]+address-segment[3]
  original=bytes(assembler.asm(original_instruction,addr=address)[0]);code=bytes(assembler.asm(instruction,addr=address)[0])
  assert bytes(data[offset:offset+4]) in (original,code),label
  data[offset:offset+4]=code;records.append({'name':label,'address':hex(address),'bytes':code.hex()})
 for name,addresses in UNLOCKS.items():
  for address in addresses:
   assert metadata[address]['Name']==name and metadata[address]['Signature'].startswith('bool ')
   segment=next(s for s in segments if s[0]==1 and s[3]<=address<s[3]+s[5]);offset=segment[2]+address-segment[3]
   code=bytes(assembler.asm('mov w0,#1; ret',addr=address)[0]);data[offset:offset+len(code)]=code
   records.append({'name':name,'address':hex(address),'bytes':code.hex()})
 # The native client materializes a distinct ItemData per inventory stack.
 # Testing balances must fit in one stack, otherwise login creates millions
 # of objects before the tavern can load. Keep the native stack builder and
 # actual item amounts; only enlarge its positive per-slot capacity.
 address=0x5753950;name='ItemInventoryData$$GetInventoryMaxItemCountPerSlot'
 assert metadata[address]['Name']==name and metadata[address]['Signature'].startswith('int32_t ')
 segment=next(s for s in segments if s[0]==1 and s[3]<=address<s[3]+s[5]);offset=segment[2]+address-segment[3]
 code=bytes(assembler.asm('mov w0,#0x7fffffff; ret',addr=address)[0]);data[offset:offset+len(code)]=code
 records.append({'name':name,'address':hex(address),'bytes':code.hex(),'capacity':2147483647})
 # Offline accounts have no Netmarble channel session. Preserve the native
 # callback invocation with false, rather than querying the unavailable SDK.
 for address,name,instruction,original_instruction in [
  (0x5721ca8,'FPAuthManager$$IsConnectedChannel','mov w0,#0; ret','stp x30,x21,[sp,#-0x20]!; stp x20,x19,[sp,#0x10]'),
  (0x57217c4,'FPAuthManager$$IsConnectedAnyChannel offline callback','b #0x5721860','bl #0x571eb64')]:
  if address==0x5721ca8:assert metadata[address]['Name']==name
  else:assert metadata[0x57216d8]['Name']=='FPAuthManager$$IsConnectedAnyChannel'
  segment=next(s for s in segments if s[0]==1 and s[3]<=address<s[3]+s[5]);offset=segment[2]+address-segment[3]
  code=bytes(assembler.asm(instruction,addr=address)[0]);original=bytes(assembler.asm(original_instruction,addr=address)[0])
  assert bytes(data[offset:offset+len(code)]) in (original,code),name
  data[offset:offset+len(code)]=code
  records.append({'name':name,'address':hex(address),'bytes':code.hex()})
 path.write_bytes(data);(ROOT/'dist/content-unlocks.json').write_text(json.dumps(records,indent=2));print('Patched',len(records),'content entry checks; story/quest data unchanged')
if __name__=='__main__':patch(ROOT/'Original-APK/libil2cpp.phone-local.so')
