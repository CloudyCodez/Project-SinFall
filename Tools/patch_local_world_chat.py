"""Complete the local world record with the native default ChatkitSetting.

Builds from stable r12, without the temporary login-field tracing patches.
"""
from pathlib import Path
import hashlib
from keystone import Ks, KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN

root = Path('E:/7DS-Offline/Original-APK')
data = bytearray((root / 'libil2cpp.cloud-local-r12.so').read_bytes())
ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)
code = '''
stp x29, x30, [sp, #-48]!
stp x20, x19, [sp, #16]
mov x19, x0
bl 0x3450A90
sub x19, x19, #32
adrp x0, 0x8B49000
add x0, x0, #0x400
bl 0x3450AE4
adrp x20, 0x8B49000
ldr x20, [x20, #0x400]
adrp x0, 0x8A87000
add x0, x0, #0x420
bl 0x3450AE4
adrp x8, 0x8A87000
ldr x0, [x8, #0x420]
bl 0x3450D6C
str x0, [sp, #32]
mov x1, xzr
bl 0x3E51968
mov x0, x19
mov x1, x20
mov x2, x20
mov x3, x20
mov x4, x20
mov w5, #5001
ldr x6, [sp, #32]
mov x7, xzr
bl 0x3C22220
mov x0, x19
mov w1, wzr
mov x2, xzr
bl 0x3C221A0
mov x1, x0
mov x0, x19
mov x2, xzr
bl 0x3C22C1C
ldp x20, x19, [sp, #16]
ldp x29, x30, [sp], #48
ret
'''
va = 0x3C22EC0
encoded = bytes(ks.asm(code, addr=va)[0])
assert va + len(encoded) < 0x3C230F0
data[va - 0x4000:va - 0x4000 + len(encoded)] = encoded
# The official notice webview waits for a remote SDK close callback, which is
# unavailable locally. Complete this notice coroutine; retain login processing.
notice_va = 0x4FCAE18
notice = bytes(ks.asm('mov w0, wzr; ret', addr=notice_va)[0])
data[notice_va - 0x4000:notice_va - 0x4000 + len(notice)] = notice
output = root / 'libil2cpp.cloud-local-r21.so'
output.write_bytes(data)
print(output, hashlib.sha256(data).hexdigest())
