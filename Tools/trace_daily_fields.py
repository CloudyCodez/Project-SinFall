from pathlib import Path
import sys
sys.path.insert(0,r'E:/7DS-Offline/Tools');import inspect_native as n
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
r=Path(r'E:/7DS-Offline/Original-APK');d=bytearray((r/'libil2cpp.cloud-local-r12.so').read_bytes());k=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
def emit(a,s):
 b=bytes(k.asm(s,addr=a)[0]);d[a-0x4000:a-0x4000+len(b)]=b
emit(0x4fc3e00,'''stp x29,x30,[sp,#-64]!
stp x0,x1,[sp,#16]
stp x2,x16,[sp,#32]
ldr x8,[x20]
sub x8,x1,x8
str w8,[sp,#48]
add x0,sp,#48
mov x1,xzr
bl 0x78d9988
mov x1,xzr
bl 0x5734600
ldr x0,[sp,#16]
ldr w8,[x0,#16]
str w8,[sp,#48]
add x0,sp,#48
mov x1,xzr
bl 0x78d9988
mov x1,xzr
bl 0x5734600
ldp x0,x1,[sp,#16]
ldp x2,x16,[sp,#32]
blr x16
ldp x29,x30,[sp],#64
ret''')
field=None;j=0
for ins in n.decoder.disasm(n.data[n.offset(0x36b7c44):n.offset(0x36b7c44)+1500],0x36b7c44):
 if ins.mnemonic=='add' and ins.op_str.startswith('x1, x8, #'):field=int(ins.op_str.split('#')[1],0)
 if ins.mnemonic=='bl' and field is not None:
  target=int(ins.op_str[1:],0);cave=0x4fc4000+j*32;j+=1
  emit(ins.address,f'bl {cave}')
  emit(cave,f'''stp x16,x30,[sp,#-16]!
adrp x16,{target&~4095}
add x16,x16,#{target&4095}
bl 0x4fc3e00
ldp x16,x30,[sp],#16
ret''');field=None
(r/'libil2cpp.cloud-local-r19.so').write_bytes(d)
print(j,'root field traces')
