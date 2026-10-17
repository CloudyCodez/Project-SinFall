"""Execute fusion ARM64 hooks with native call contracts and realistic unit fields."""
import struct
from unicorn import Uc,UC_ARCH_ARM64,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm64_const import *
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
from patch_db_legends_fusion import programs,GATE,CLEANUP,TRIGGER,PLAY,BLACK_EFFECT,BLACK_CAMERA
ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
RET=0x11000000;UNIT=0x10001000;VEGETA=0x10002000;NEW=0x10003000;MANAGER=0x10004000;MAIN=0x10005000;CO=0x10006000

def run(which,skin=399903,partner=399913,dead=False,excluded=False,missing=False,state=74,newskin=399921,actor_dead=False,actor_excluded=False,effect_id=198500063,camera_flags=(1<<28)|1572864):
 u=Uc(UC_ARCH_ARM64,UC_MODE_ARM);pages=set();calls=[]
 def mapat(a,size=4096):
  for p in range(a&~4095,(a+size+4095)&~4095,4096):
   if p not in pages:u.mem_map(p,4096);pages.add(p)
 def put(a,v,fmt='<Q'):mapat(a);u.mem_write(a,struct.pack(fmt,v))
 mapat(0x10000000,0x20000);mapat(RET);mapat(0x20000000,0x10000)
 for entry,cave,code,_ in programs():
  mapat(cave,len(code));u.mem_write(cave,code)
  if entry:mapat(entry);u.mem_write(entry,bytes(ks.asm(f'b #{cave}',addr=entry)[0]))
 for a in [0x479f048,0x51bf19c,0x4785d54,0x51ea028,0x4770fa0,0x47951bc,0x475df5c,0x3c3ede8,0x55656c0,0x51f27a8,0x813b41c,0x3c3ec90,0x51fafcc,0x59a0000,0x521e7dc]:mapat(a)
 for a in [0x3c3f3cc,0x4842d8c,0x485f190,0x4861a7c,0x556e684,0x555f9fc,0x3c496ec,0x5561c64,0x4858f98,0x555d430]:mapat(a)
 for unit,sid in [(UNIT,skin),(VEGETA,partner),(NEW,newskin)]:
  # Battle UnitModel.SkinID stays zero. The actual form is exposed through
  # the TeamUnitData virtual method, matching the native loader's contract.
  put(unit+0x128,unit+0x300);put(unit+0x328,0,'<I');put(unit+0x170,1,'<I')
  put(unit+0x160,unit+0x500);put(unit+0x500,0x10010000);put(unit+0x520,sid,'<I')
 put(0x10010458,0x10011000);put(0x10010460,0x10012000)
 put(VEGETA+0x1a8,int(excluded),'<B')
 put(UNIT+0x1a8,int(actor_excluded),'<B')
 put(CO+0x20,UNIT);put(CO+0x30,NEW);put(CO+0x38,MANAGER)
 put(0x8725ab0,0x10007000);put(0x10007000,0x10008000);put(0x100080b8,0x10009000);put(0x10009000,MAIN)
 put(0x1000c028,UNIT)
 put(0x1000a000,0x10014000);put(0x10014478,0x10013000);put(0x10014480,0x10015000)
 put(0x10016018,7,'<I');put(0x1001601c,2,'<I')
 for a in [0x5ca066c,0x5ca3f60,0x80f7d00,0x3c3f000,0x3e8d660]:mapat(a)
 for a in [0x33ee200,0x810bf1c,0x4e6a56c,0x4e68b50]:mapat(a)
 def hook(uc,a,size,data):
  if a in [RET,0x59a0000,0x521e7dc,0x51ea028]:
   if a==0x51ea028:calls.append(('fallback',uc.reg_read(UC_ARM64_REG_X0),uc.reg_read(UC_ARM64_REG_X1)))
   uc.emu_stop();return
  if a in [0x5ca066c,0x5ca3f60]:
   calls.append(('original_effect' if a==0x5ca066c else 'original_camera',))
   sp=uc.reg_read(UC_ARM64_REG_SP)
   if a==0x5ca066c:uc.reg_write(UC_ARM64_REG_SP,sp+0x70);lr=uc.reg_read(UC_ARM64_REG_LR)
   else:lr=struct.unpack('<Q',uc.mem_read(sp,8))[0];uc.reg_write(UC_ARM64_REG_SP,sp+0x30)
   uc.reg_write(UC_ARM64_REG_PC,lr);return
  if a==0x80f7d00:
   uc.reg_write(UC_ARM64_REG_X0,effect_id if which=='effect' else camera_flags);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return
  if a==0x3c3f000:
   assert uc.reg_read(UC_ARM64_REG_X0)==MAIN
   uc.reg_write(UC_ARM64_REG_X0,0x1000e800);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return
  if a==0x3e8d660:
   assert [uc.reg_read(UC_ARM64_REG_X0+i) for i in range(3)]==[0x1000e800,UNIT,0x1000f000]
   calls.append(('camera',));uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return
  if a==0x4e68b50:
   assert uc.reg_read(UC_ARM64_REG_X0)==0x1000c000
   assert uc.reg_read(UC_ARM64_REG_X1)==state
   calls.append(('play',state))
   sp=uc.reg_read(UC_ARM64_REG_SP);lr=struct.unpack('<Q',uc.mem_read(sp,8))[0]
   uc.reg_write(UC_ARM64_REG_SP,sp+0x50);uc.reg_write(UC_ARM64_REG_PC,lr);return
  if a in [0x33ee200,0x810bf1c,0x4e6a56c]:
   uc.reg_write(UC_ARM64_REG_X0,0x1000d000);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return
  if a==0x10011000:
   assert uc.reg_read(UC_ARM64_REG_X1)==0x10012000
   sid=struct.unpack('<I',uc.mem_read(uc.reg_read(UC_ARM64_REG_X0)+0x20,4))[0]
   uc.reg_write(UC_ARM64_REG_X0,sid);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return
  if a==0x10013000:
   assert uc.reg_read(UC_ARM64_REG_X0)==0x1000a000 and uc.reg_read(UC_ARM64_REG_X1)==1
   calls.append(('clear_deck',));uc.reg_write(UC_ARM64_REG_X0,0x10016000);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR));return
  stubs={0x479f048:'dead',0x51bf19c:'partner',0x4785d54:'condition',0x4770fa0:'exclude',0x47951bc:'return',0x475df5c:'visible',0x3c3ede8:'cards',0x55656c0:'remove_cards',0x51f27a8:'withdraw',0x813b41c:'start',0x3c3ec90:'manager',0x51fafcc:'transform',0x3c3f3cc:'ui',0x4842d8c:'delete_hp',0x485f190:'release_hand',0x556e684:'clear_hand',0x555f9fc:'rebuild_deck',0x3c496ec:'reset_cost',0x5561c64:'draw',0x4858f98:'direct_hand',0x555d430:'ability_complete'}
  stubs[0x4861a7c]='clear_hand_ui'
  if a not in stubs:return
  args=[uc.reg_read(UC_ARM64_REG_X0+i) for i in range(6)];name=stubs[a];calls.append((name,*args[:3]));result=0
  if name=='dead':result=int((dead and args[0]==VEGETA) or (actor_dead and args[0]==UNIT))
  elif name=='partner':assert args[1]==2997002 and args[2]==1;result=0 if missing else VEGETA
  elif name=='condition':put(args[0]+0x1b2,args[1],'<B')
  elif name=='exclude':put(args[0]+0x1a8,args[1],'<B')
  elif name=='cards':result=0x1000a000
  elif name=='ui':result=0x1000e000
  elif name=='manager':result=MANAGER
  elif name in ['withdraw','transform']:result=0x1000b000
  if name=='transform':assert args[:5]==[MANAGER,UNIT,0,0,1]
  if name=='delete_hp':assert args[:2]==[0x1000e000,UNIT if newskin==399933 else VEGETA]
  if name=='rebuild_deck':assert struct.unpack('<II',uc.mem_read(0x10016018,8))==(0,3),'Deck must be empty before native CreateDeckCard'
  if name in ['release_hand','clear_hand','rebuild_deck','reset_cost','direct_hand']:assert args[1]==1
  if name=='draw':assert args[:5]==[0x1000a000,1,0,0,0xffffffff]
  if name=='ability_complete':assert args[:2]==[0x1000a000,NEW]
  uc.reg_write(UC_ARM64_REG_X0,result);uc.reg_write(UC_ARM64_REG_PC,uc.reg_read(UC_ARM64_REG_LR))
 u.hook_add(UC_HOOK_CODE,hook);u.reg_write(UC_ARM64_REG_SP,0x20008000);u.reg_write(UC_ARM64_REG_LR,RET)
 if which=='gate':entry=GATE;u.reg_write(UC_ARM64_REG_X0,MANAGER);u.reg_write(UC_ARM64_REG_X1,UNIT)
 elif which in ['trigger','callback']:
  entry=TRIGGER;u.reg_write(UC_ARM64_REG_X0,CO);u.reg_write(UC_ARM64_REG_X1,UNIT);u.reg_write(UC_ARM64_REG_X3,0x475 if which=='trigger' else 0)
 elif which in ['effect','camera']:
  put(0x1000c020,UNIT);entry=BLACK_EFFECT if which=='effect' else BLACK_CAMERA;u.reg_write(UC_ARM64_REG_X0,0x1000c000);u.reg_write(UC_ARM64_REG_X1,0x1000f000)
 elif which=='play':entry=PLAY;u.reg_write(UC_ARM64_REG_X0,0x1000c000);u.reg_write(UC_ARM64_REG_X1,state)
 else:entry=CLEANUP;u.reg_write(UC_ARM64_REG_X19,CO)
 u.emu_start(entry,RET,count=1000)
 return calls,bytes(u.mem_read(UNIT+0x1b2,1))[0]

for args,enabled in [({},1),({'partner':399912},0),({'dead':True},0),({'excluded':True},0),({'missing':True},0)]:
 c,v=run('gate',**args);assert v==enabled,(args,c)
 assert any(x[0]=='transform' for x in run('trigger',**args)[0])==bool(enabled)
assert run('gate',skin=399902)[0][0][0]=='fallback'
assert not run('trigger',skin=399902)[0]
assert not run('callback')[0], 'Imported hit events must not dispatch a second swap'
for state in [74,78]:assert any(x[0]=='transform' for x in run('play',state=state)[0])
for state in [1,16,75,76]:assert not any(x[0]=='transform' for x in run('play',state=state)[0])
for skin in [344002,399902,399913,399921]:
 assert run('play',skin=skin)[0]==[('play',74)], 'Only Sign Goku may enter the custom fusion dispatcher'
c,_=run('cleanup');assert [x[0] for x in c]==['partner','exclude','return','visible','cards','remove_cards','ui','delete_hp','release_hand','clear_hand_ui','cards','clear_hand','clear_deck','rebuild_deck','reset_cost','draw','direct_hand','ability_complete'],c
assert not run('cleanup',skin=399902)[0]
assert [x[0] for x in run('cleanup',excluded=True)[0]]==['partner']
print('PASS: LR-only gate, missing/dead/excluded partner rejection, native tag dispatch, idempotent withdrawal, original-unit fallback')
for skin in [399931,399932]:
 c,v=run('gate',skin=skin,missing=True);assert v==1 and not any(x[0]=='partner' for x in c)
 assert any(x[0]=='transform' for x in run('trigger',skin=skin,missing=True)[0])
 for state in [74,78]:assert not any(x[0]=='transform' for x in run('play',skin=skin,state=state,missing=True)[0]), 'Black must wait for beam impact'
 for flags in [dict(actor_dead=True),dict(actor_excluded=True)]:
  assert run('gate',skin=skin,**flags)[1]==0
  assert not any(x[0]=='transform' for x in run('trigger',skin=skin,**flags)[0])
 c,_=run('cleanup',skin=skin,newskin=399933)
 assert [x[0] for x in c]==['ui','delete_hp','release_hand','clear_hand_ui','cards','clear_hand','clear_deck','rebuild_deck','reset_cost','draw','direct_hand','ability_complete'],c
 assert not run('cleanup',skin=skin,newskin=399921)[0]
assert run('gate',skin=399933)[0][0][0]=='fallback'
print('PASS: Black SSR/UR solo transformation, dead/excluded rejection, Rosé-only completion and clean card refresh without partner removal')

for skin in [399931,399932]:
 c,_=run('effect',skin=skin);assert c[0][0]=='original_effect' and any(x[0]=='transform' for x in c),c
 for effect_id in [198500061,198500062,198500064]:assert run('effect',skin=skin,effect_id=effect_id)[0]==[('original_effect',)]
 assert run('camera',skin=skin)[0]==[('camera',)]
 assert run('camera',skin=skin,camera_flags=1572864)[0]==[('original_camera',)]
for skin in [399903,399921,399933,344002]:assert run('effect',skin=skin)[0]==[('original_effect',)]
for skin in [399903,399921,344002]:assert run('camera',skin=skin)[0]==[('original_camera',)]
assert run('camera',skin=399933)[0]==[('camera',)]
print('PASS: Black swaps only on final beam event; transformation camera forwards to native camera player; unrelated effects/cameras preserve original behavior')
