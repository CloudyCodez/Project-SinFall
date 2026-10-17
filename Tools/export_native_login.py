from pathlib import Path
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
r=Path(r'E:/7DS-Offline/Original-APK');d=bytearray((r/'libil2cpp.cloud-local-r12.so').read_bytes());k=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
def emit(a,s):
 b=bytes(k.asm(s,addr=a)[0]);d[a-0x4000:a-0x4000+len(b)]=b
emit(0x36b68a8,'b 0x4fc3e00')
emit(0x4fc3e00,'''stp x29,x30,[sp,#-64]!
stp x19,x20,[sp,#16]
stp x21,x22,[sp,#32]
mov x19,x0
mov x20,x1
mov x2,xzr
bl 0x369e428
sub x21,x20,#0x328
ldr x0,[x19]
bl 0x3450d6c
mov x22,x0
mov x1,xzr
bl 0x79e8018
mov x0,x22
mov x1,x21
mov x2,xzr
bl 0x36b2514
ldr x8,[x22,#24]
ldr w9,[x8,#24]
ldr x21,[x8,#16]
str x9,[x21,#24]
adrp x0,0x4fc4000
add x0,x0,#16
bl 0x33ee200
mov x1,x21
mov x2,xzr
bl 0x783a4ec
mov x0,x19
mov x1,x20
mov x2,xzr
nop
ldp x21,x22,[sp,#32]
ldp x19,x20,[sp,#16]
ldp x29,x30,[sp],#64
ret''')
for a,s in [(0x4fc4000,b'Cloud\0'),(0x4fc4010,b'/sdcard/gc-native-login.bin\0')]:d[a-0x4000:a-0x4000+len(s)]=s
(r/'libil2cpp.cloud-local-r17.so').write_bytes(d)

