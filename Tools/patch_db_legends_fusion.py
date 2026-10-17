"""LR-pair ability gating and second-fighter withdrawal for native tag fusion.

Only Sign Goku's ability and the Sign-to-Blue-Gogeta tag completion are changed.
Executable storage uses unused TAS automation methods, as the race patch does.
"""
from pathlib import Path
import json, struct
from keystone import Ks, KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN
ROOT=Path(__file__).resolve().parents[1]
GATE=0x4063ff0
CLEANUP=0x40640e4
TRIGGER=0x406482c
LOGGER=0x4064920
MESSAGES=0x4064a14
PLAY=0x4064dd8
SKIN=0x4064ad4
REFRESH=0x4064314
BLACK_GATE=0x4063704
BLACK_TRIGGER=0x40635d0
BLACK_EFFECT=0x40632e8
BLACK_CAMERA=0x406396c
ROSE_PREVIEW_NAME=0x4063a20
ROSE_PREVIEW_NICK=0x4063a60
def programs():
 gate='''
 stp x30,x19,[sp,#-48]!
 stp x20,x21,[sp,#16]
 str x2,[sp,#32]
 mov x19,x0
 mov x20,x1
 cbz x20,fallback
 mov x0,x20
 bl #0x4064ad4
 mov w8,w0
 mov w9,#0x1a1f
 movk w9,#6,lsl #16
 cmp w8,w9
 b.ne #0x4063704
 mov x0,x20
 mov x1,xzr
 bl #0x479f048
 cbnz w0,disabled
 ldrb w8,[x20,#0x1a8]
 cbnz w8,disabled
 mov x0,x19
 mov w1,#0xbb2a
 movk w1,#0x2d,lsl #16
 ldr w2,[x20,#0x170]
 mov x3,xzr
 bl #0x51bf19c
 cbz x0,disabled
 mov x21,x0
 mov x0,x21
 bl #0x4064ad4
 mov w8,w0
 mov w9,#0x1a29
 movk w9,#6,lsl #16
 cmp w8,w9
 b.ne disabled
 ldrb w8,[x21,#0x1a8]
 cbnz w8,disabled
 mov x0,x21
 mov x1,xzr
 bl #0x479f048
 cbnz w0,disabled
 mov w1,#1
 b set_condition
 disabled: mov w1,wzr
 set_condition: mov x0,x20
 mov x2,xzr
 bl #0x4785d54
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#48
 ret
 fallback: mov x0,x20
 mov w1,#0x6f2
 ldr x2,[sp,#32]
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#48
 b #0x51ea028
 '''
 cleanup='''
 stp x30,x20,[sp,#-48]!
 stp x21,x22,[sp,#16]
 str x23,[sp,#32]
 ldr x8,[x19,#0x20]
 cbz x8,done
 mov x0,x8
 bl #0x4064ad4
 mov w8,w0
 mov w9,#0x1a1f
 movk w9,#6,lsl #16
 cmp w8,w9
 b.ne done
 ldr x8,[x19,#0x30]
 cbz x8,done
 mov x0,x8
 bl #0x4064ad4
 mov w8,w0
 mov w9,#0x1a31
 movk w9,#6,lsl #16
 cmp w8,w9
 b.ne done
 ldr x20,[x19,#0x38]
 cbz x20,done
 ldr x8,[x19,#0x30]
 ldr w23,[x8,#0x170]
 mov x0,x20
 mov w1,#0xbb2a
 movk w1,#0x2d,lsl #16
 mov w2,w23
 mov x3,xzr
 bl #0x51bf19c
 cbz x0,done
 mov x21,x0
 ldrb w8,[x21,#0x1a8]
 cbnz w8,done
 mov w1,#1
 mov x2,xzr
 bl #0x4770fa0
 mov x0,x21
 mov w1,wzr
 mov x2,xzr
 bl #0x47951bc
 mov x0,x21
 mov w1,wzr
 mov w2,#1
 mov x3,xzr
 bl #0x475df5c
 adrp x8,#0x8725000
 ldr x8,[x8,#0xab0]
 ldr x8,[x8]
 ldr x8,[x8,#0xb8]
 ldr x22,[x8]
 cbz x22,done
 mov x0,x22
 mov x1,xzr
 bl #0x3c3ede8
 cbz x0,withdraw
 mov x1,x21
 mov x2,xzr
 bl #0x55656c0
 withdraw: mov x0,x22
 mov x1,x21
 ldr x2,[x19,#0x30]
 mov w3,w23
 bl #0x4064314
 done: ldr x23,[sp,#32]
 ldp x21,x22,[sp,#16]
 ldp x30,x20,[sp],#48
 mov w0,wzr
 b #0x521e7dc
 '''
 trigger='''
 stp x30,x19,[sp,#-80]!
 stp x20,x21,[sp,#16]
 stp x0,x1,[sp,#32]
 stp x2,x3,[sp,#48]
 str x4,[sp,#64]
 cbz x1,fallback_trigger
 mov x19,x1
 mov x0,x19
 bl #0x4064ad4
 mov w8,w0
 mov w9,#0x1a1f
 movk w9,#6,lsl #16
 cmp w8,w9
 b.ne #0x40635d0
 ldr w3,[sp,#56]
 cmp w3,#0x475
 b.ne trigger_done
 mov w0,#0
 bl #0x4064920
 adrp x8,#0x8725000
 ldr x8,[x8,#0xab0]
 ldr x8,[x8]
 ldr x8,[x8,#0xb8]
 ldr x20,[x8]
 cbz x20,trigger_done
 mov x0,x20
 mov x1,xzr
 bl #0x3c3ec90
 cbz x0,trigger_done
 mov x21,x0
 mov x1,x19
 mov x2,xzr
 bl #0x51cb300
 ldrb w8,[x19,#0x1b2]
 cbz w8,trigger_done
 mov w0,#1
 bl #0x4064920
 mov x0,x21
 mov x1,x19
 mov x2,xzr
 mov w3,wzr
 mov w4,#1
 mov x5,xzr
 bl #0x51fafcc
 cbz x0,trigger_done
 mov x1,x0
 mov x0,x20
 mov x2,xzr
 bl #0x813b41c
 mov w0,#2
 bl #0x4064920
 trigger_done:
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#80
 ret
 fallback_trigger:
 ldp x0,x1,[sp,#32]
 ldp x2,x3,[sp,#48]
 ldr x4,[sp,#64]
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#80
 sub sp,sp,#0x110
 b #0x59a0000
 '''
 trigger=trigger.replace('#0x1a1f',f'#{399903&65535}')
 # Decimal IDs are verified here to prevent silent immediate transcription bugs.
 gate=gate.replace('#0x1a1f',f'#{399903&65535}').replace('#0x1a29',f'#{399913&65535}').replace('#0xbb2a',f'#{2997002&65535}').replace('#0x2d',f'#{2997002>>16}')
 cleanup=cleanup.replace('#0x1a1f',f'#{399903&65535}').replace('#0x1a31',f'#{399921&65535}').replace('#0xbb2a',f'#{2997002&65535}').replace('#0x2d',f'#{2997002>>16}')
 # Black transforms alone. Never run the fusion partner-withdrawal path.
 cleanup=cleanup.replace(' cmp w8,w9\n b.ne done', ''' cmp w8,w9
 b.eq fusion_cleanup
 mov w9,#6715
 movk w9,#6,lsl #16
 cmp w8,w9
 b.eq black_cleanup
 add w9,w9,#1
 cmp w8,w9
 b.ne done
 black_cleanup:
 ldr x21,[x19,#0x30]
 cbz x21,done
 mov x0,x21
 bl #0x4064ad4
 mov w9,#6717
 movk w9,#6,lsl #16
 cmp w0,w9
 b.ne done
 ldr w23,[x21,#0x170]
 adrp x8,#0x8725000
 ldr x8,[x8,#0xab0]
 ldr x8,[x8]
 ldr x8,[x8,#0xb8]
 ldr x0,[x8]
 cbz x0,done
 ldr x1,[x19,#0x20]
 mov x2,x21
 mov w3,w23
 bl #0x4064314
 b done
 fusion_cleanup:''',1)
 black_gate='''
 mov w9,#6715
 movk w9,#6,lsl #16
 cmp w8,w9
 b.eq check_black
 add w9,w9,#1
 cmp w8,w9
 b.ne black_fallback
 check_black:
 mov x0,x20
 mov x1,xzr
 bl #0x479f048
 cbnz w0,black_disabled
 ldrb w8,[x20,#0x1a8]
 cbnz w8,black_disabled
 mov w1,#1
 b black_condition
 black_disabled: mov w1,wzr
 black_condition: mov x0,x20
 mov x2,xzr
 bl #0x4785d54
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#48
 ret
 black_fallback: mov x0,x20
 mov w1,#0x6f2
 ldr x2,[sp,#32]
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#48
 b #0x51ea028
 '''
 # Reuse the well-tested native swap sequence, with no partner requirement.
 black_trigger=trigger[trigger.index(' ldr w3,[sp,#56]'):trigger.index(' trigger_done:')]
 black_trigger='''
 mov w9,#6715
 movk w9,#6,lsl #16
 cmp w8,w9
 b.eq black_dispatch
 add w9,w9,#1
 cmp w8,w9
 b.ne black_trigger_fallback
 black_dispatch:
 '''+black_trigger+'''
 trigger_done:
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#80
 ret
 black_trigger_fallback:
 ldp x0,x1,[sp,#32]
 ldp x2,x3,[sp,#48]
 ldr x4,[sp,#64]
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#80
 sub sp,sp,#0x110
 b #0x59a0000
 '''
 black_effect='''
 stp x30,x19,[sp,#-48]!
 stp x20,x21,[sp,#16]
 mov x19,x0
 mov x20,x1
 mov x21,x2
 bl effect_original
 cbz x20,effect_done
 mov x0,x20
 mov x1,xzr
 bl #0x80f7d00
 mov w8,#57055
 movk w8,#3028,lsl #16
 cmp w0,w8
 b.ne effect_done
 ldr x0,[x19,#0x20]
 cbz x0,effect_done
 bl #0x4064ad4
 mov w8,#6715
 movk w8,#6,lsl #16
 cmp w0,w8
 b.eq effect_swap
 add w8,w8,#1
 cmp w0,w8
 b.ne effect_done
 effect_swap:
 ldr x1,[x19,#0x20]
 mov x0,xzr
 mov x2,xzr
 mov w3,#0x475
 mov x4,xzr
 bl #0x406482c
 effect_done:
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#48
 ret
 effect_original:
 sub sp,sp,#0x70
 b #0x5ca066c
 '''
 # Camera events marked as our transformation use the existing native
 # camera player even while the ability lifecycle selects a logic camera.
 black_camera='''
 stp x30,x19,[sp,#-48]!
 stp x20,x21,[sp,#16]
 mov x19,x0
 mov x20,x1
 mov x21,x2
 cbz x20,camera_fallback
 mov x0,x20
 mov x1,xzr
 bl #0x80f7d00
 tbz w0,#28,camera_fallback
 ldr x0,[x19,#0x20]
 cbz x0,camera_fallback
 bl #0x4064ad4
 mov w8,#6715
 movk w8,#6,lsl #16
 cmp w0,w8
 b.lt camera_fallback
 add w8,w8,#2
 cmp w0,w8
 b.gt camera_fallback
 adrp x8,#0x8725000
 ldr x8,[x8,#0xab0]
 ldr x8,[x8]
 ldr x8,[x8,#0xb8]
 ldr x0,[x8]
 cbz x0,camera_fallback
 mov x1,xzr
 bl #0x3c3f000
 cbz x0,camera_fallback
 ldr x1,[x19,#0x20]
 mov x2,x20
 mov x3,xzr
 bl #0x3e8d660
 b camera_done
 camera_fallback:
 mov x0,x19
 mov x1,x20
 mov x2,x21
 bl camera_original
 camera_done:
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#48
 ret
 camera_original:
 str x30,[sp,#-0x30]!
 b #0x5ca3f60
 '''
 ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
 # Play is the actual native ability state transition, independent of an
 # imported hit-event callback. Preserve the complete original Play call.
 play='''
 stp x30,x19,[sp,#-80]!
 stp x20,x21,[sp,#16]
 stp x0,x1,[sp,#32]
 stp x2,x3,[sp,#48]
 str x4,[sp,#64]
 mov x19,x0
 mov w20,w1
 mov x21,xzr
 cbz x19,original_call
 ldr x21,[x19,#0x28]
 cbz x21,original_call
 mov x0,x21
 bl #0x4064ad4
 mov w8,w0
 mov w9,#6685
 movk w9,#6,lsl #16
 cmp w8,w9
 b.lt original_call
 mov w9,#6705
 movk w9,#6,lsl #16
 cmp w8,w9
 b.gt original_call
 mov x0,x19
 mov w1,w20
 mov x2,xzr
 bl #0x4e6a56c
 mov x1,xzr
 bl #0x810bf1c
 original_call:
 ldp x0,x1,[sp,#32]
 ldp x2,x3,[sp,#48]
 ldr x4,[sp,#64]
 bl original_play
 cmp w20,#74
 b.eq dispatch
 cmp w20,#78
 b.eq play_swap
 b play_done
 play_swap:
 dispatch:
 cbz x21,play_done
 mov x0,x21
 bl #0x4064ad4
 mov w8,w0
 mov w9,#6687
 movk w9,#6,lsl #16
 cmp w8,w9
 b.eq dispatch_swap
 mov w9,#6715
 movk w9,#6,lsl #16
 cmp w8,w9
 b.eq play_done
 add w9,w9,#1
 cmp w8,w9
 b.eq play_done
 b play_done
 dispatch_swap:
 mov x0,xzr
 mov x1,x21
 mov x2,xzr
 mov w3,#0x475
 mov x4,xzr
 bl #0x406482c
 play_done:
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#80
 ret
 original_play:
 str x30,[sp,#-0x50]!
 b #0x4e68b50
 '''
 logger='''
 str x30,[sp,#-16]!
 adrp x8,#0x4064000
 add x8,x8,#0xa14
 add x0,x8,x0,lsl #6
 bl #0x33ee200
 mov x1,xzr
 bl #0x810bf1c
 ldr x30,[sp],#16
 ret
 '''
 messages=b''.join(x.encode().ljust(64,b'\0') for x in ['[Phoenix Fusion] ability animation started','[Phoenix Fusion] LR pair valid; starting native swap','[Phoenix Fusion] native swap coroutine scheduled'])
 # UnitModel.SkinID is a presentation field and is not initialized by the
 # battle model loader. TeamUnitData.GetSkinID (virtual slot50) is authoritative.
 skin='''
 cbz x0,no_skin
 ldr x0,[x0,#0x160]
 cbz x0,no_skin
 ldr x8,[x0]
 ldr x9,[x8,#0x458]
 ldr x1,[x8,#0x460]
 br x9
 no_skin: mov w0,wzr
 ret
 '''
 # Complete the same native ability lifecycle as OnAfterPlayAbilitySkill,
 # then rebuild this camp's hand/deck from the post-fusion active roster.
 # ClearCardList alone leaves the visible UI and the ability input lock alive.
 refresh='''
 stp x30,x19,[sp,#-64]!
 stp x20,x21,[sp,#16]
 stp x22,x23,[sp,#32]
 mov x19,x0
 mov x20,x1
 mov x21,x2
 mov w22,w3
 mov x1,xzr
 bl #0x3c3f3cc
 cbz x0,refresh_done
 mov x23,x0
 mov x1,x20
 mov x2,xzr
 bl #0x4842d8c
 mov x0,x23
 mov w1,w22
 mov x2,xzr
 bl #0x485f190
 mov x0,x23
 mov w1,w22
 mov x2,xzr
 bl #0x4861a7c
 mov x0,x19
 mov x1,xzr
 bl #0x3c3ede8
 cbz x0,refresh_done
 mov x20,x0
 mov w1,w22
 mov x2,xzr
 bl #0x556e684
 // CreateDeckCard skips rebuilding a nonempty native deck. Clear that deck
 // through its virtual accessor, independently of the visible hand.
 mov x0,x20
 mov w1,w22
 ldr x8,[x20]
 ldr x9,[x8,#0x478]
 ldr x2,[x8,#0x480]
 blr x9
 cbz x0,deck_cleared
 str wzr,[x0,#0x18]
 ldr w8,[x0,#0x1c]
 add w8,w8,#1
 str w8,[x0,#0x1c]
 deck_cleared:
 mov x0,x20
 mov w1,w22
 mov x2,xzr
 bl #0x555f9fc
 mov x0,x19
 mov w1,w22
 mov x2,xzr
 bl #0x3c496ec
 mov x0,x20
 mov w1,w22
 mov w2,wzr
 mov w3,wzr
 mov w4,#-1
 mov x5,xzr
 bl #0x5561c64
 mov x0,x23
 mov w1,w22
 mov x2,xzr
 bl #0x4858f98
 mov x0,x20
 mov x1,x21
 mov x2,xzr
 bl #0x555d430
 adrp x0,#0x4064000
 add x0,x0,#0x514
 bl #0x33ee200
 mov x1,xzr
 bl #0x810bf1c
 refresh_done:
 ldp x22,x23,[sp,#32]
 ldp x20,x21,[sp,#16]
 ldp x30,x19,[sp],#64
 ret
 '''
 result=[(0x51cb300,GATE,bytes(ks.asm(gate,addr=GATE)[0]),244),(0x521e6d0,CLEANUP,bytes(ks.asm(cleanup,addr=CLEANUP)[0]),560),(0x599fffc,TRIGGER,bytes(ks.asm(trigger,addr=TRIGGER)[0]),244),(0,LOGGER,bytes(ks.asm(logger,addr=LOGGER)[0]),244),(0,MESSAGES,messages,192),(0x4e68b4c,PLAY,bytes(ks.asm(play,addr=PLAY)[0]),700),(0,SKIN,bytes(ks.asm(skin,addr=SKIN)[0]),208)]
 refresh_code=bytes(ks.asm(refresh,addr=REFRESH)[0])
 assert len(refresh_code)<=0x200
 refresh_code=refresh_code.ljust(0x200,b'\0')+b'[Phoenix Fusion] roster, health bars and hand rebuilt\0'
 result.append((0,REFRESH,refresh_code,708))
 result.extend([(0,BLACK_GATE,bytes(ks.asm(black_gate,addr=BLACK_GATE)[0]),424),(0,BLACK_TRIGGER,bytes(ks.asm(black_trigger,addr=BLACK_TRIGGER)[0]),308)])
 result.extend([(0x5ca0668,BLACK_EFFECT,bytes(ks.asm(black_effect,addr=BLACK_EFFECT)[0]),320),(0x5ca3f5c,BLACK_CAMERA,bytes(ks.asm(black_camera,addr=BLACK_CAMERA)[0]),472)])
 # The hidden transformed hero is not an owned HeroData. Its inventory
 # preview must use the selected SkinData rather than GetHero's donor fallback.
 for entry,cave,skin_field,hero_field in [(0x47e3c2c,ROSE_PREVIEW_NAME,0x1b0,0x40),(0x47e3c48,ROSE_PREVIEW_NICK,0x1b8,0x48)]:
  code=f'''
  ldr x9,[x19,#0x70]
  cbz x9,original_name
  ldr w10,[x9,#0x18c]
  mov w11,#{2997005&65535}
  movk w11,#{2997005>>16},lsl #16
  cmp w10,w11
  b.ne original_name
  ldr x1,[x9,#{skin_field}]
  b #{entry+4}
  original_name: ldr x1,[x8,#{hero_field}]
  b #{entry+4}
  '''
  result.append((entry,cave,bytes(ks.asm(code,addr=cave)[0]),64))
 for _,_,code,limit in result:assert len(code)<=limit,(len(code),limit)
 return result
def patch(path=None):
 path=Path(path or ROOT/'Original-APK/libil2cpp.phone-local.so')
 data=bytearray(path.read_bytes());original=(ROOT/'Original-APK/libil2cpp.original.so').read_bytes()
 phoff=struct.unpack_from('<Q',data,32)[0];size,count=struct.unpack_from('<HH',data,54)
 segments=[struct.unpack_from('<IIQQQQQQ',data,phoff+i*size) for i in range(count)]
 def offset(a):
  s=next(s for s in segments if s[0]==1 and s[3]<=a<s[3]+s[5]);return s[2]+a-s[3]
 names={r['Address']:r['Name'] for r in json.loads((ROOT/'Research/Il2CppDumper/script.json').read_text(encoding='utf8'))['ScriptMethod']}
 assert names[TRIGGER]=='TasMessageHandler$$RegistWeaponSet'
 assert names[GATE]=='TasMessageHandler$$RegistFoodAll'
 assert names[CLEANUP]=='TasMessageHandler$$RegistFoodMaterialAll'
 assert names[REFRESH]=='TasMessageHandler$$ReadyToBuyForItemStore'
 assert names[0x51cb300]=='IngameUnitManager$$EvaluateAbilitySkillActivation'
 assert names[0x521dcd8].endswith('PostProcessTagSystemUnit>d__277$$MoveNext')
 ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN);records=[]
 previous_path=ROOT/'dist/db-legends-fusion-hooks.json'
 previous=json.loads(previous_path.read_text()) if previous_path.exists() else []
 for entry,cave,code,limit in programs():
  if entry:
   branch=bytes(ks.asm(f'b #{cave}',addr=entry)[0]);pos=offset(entry)
   assert bytes(data[pos:pos+4]) in [original[pos:pos+4],branch],hex(entry)
   data[pos:pos+4]=branch
  cpos=offset(cave)
  prior=next((bytes.fromhex(r['code']) for r in previous if int(r['cave'],16)==cave),None)
  current=bytes(data[cpos:cpos+len(code)])
  allowed=[original[cpos:cpos+len(code)],code]
  if prior:
   allowed.append(prior[:len(code)]+original[cpos+len(prior):cpos+len(code)])
   # Older builds left a longer revision's tail in this reserved TAS cave.
   # Accept it only after verifying the entire recorded active hook prefix.
   if len(prior)<len(code) and bytes(data[cpos:cpos+len(prior)])==prior:
    data[cpos+len(prior):cpos+len(code)]=original[cpos+len(prior):cpos+len(code)]
    current=bytes(data[cpos:cpos+len(code)])
  assert current in allowed,hex(cave)
  data[cpos:cpos+len(code)]=code
  records.append(dict(entry=hex(entry),cave=hex(cave),code=code.hex()))
 path.write_bytes(data);(ROOT/'dist/db-legends-fusion-hooks.json').write_text(json.dumps(records,indent=2))
 print('Installed LR-pair gating and native tag-completion fusion withdrawal hooks')
if __name__=='__main__':
 import sys
 if '--check-only' in sys.argv:print([(hex(entry),len(code)) for entry,_,code,_ in programs()])
 else:patch()
