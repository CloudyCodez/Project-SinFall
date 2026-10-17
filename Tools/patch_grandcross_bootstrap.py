"""Build r3: finish the local startup prerequisites before normal game login.

Targets only the preserved 2.113.1 ARM64 client. Never modifies the original.
"""
from pathlib import Path
import hashlib
from keystone import Ks, KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = Path(r"E:\7DS-Offline")
BASE = ROOT / "Original-APK/libil2cpp.cloud-local-r2.so"
ORIGINAL = ROOT / "Original-APK/libil2cpp.original.so"
OUTPUT = ROOT / "Original-APK/libil2cpp.cloud-local-r12.so"
image = bytearray(BASE.read_bytes())
pristine = ORIGINAL.read_bytes()
assembler = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)

def emit(va, assembly, expected=None):
    encoded, _ = assembler.asm(assembly, addr=va)
    data = bytes(encoded)
    offset = va - 0x4000
    reference = pristine[offset:offset + len(data)] if expected is None else expected
    if image[offset:offset + len(data)] != reference:
        raise RuntimeError(f"Unexpected source at {va:#x}")
    image[offset:offset + len(data)] = data
    for ins in Cs(CS_ARCH_ARM64, CS_MODE_ARM).disasm(data, va):
        print(f"{ins.address:#x}: {ins.mnemonic} {ins.op_str}")

# This guard means patch complete AND tutorial complete. The local asset tree
# is already installed; the r2 stage redirect never set these status bits, so
# it reached the normal patch-failure dialog rather than starting the scene.
# Keep the native scene coroutine and all table/resource initialization.
emit(0x4FC2284, "nop", bytes.fromhex("E0190036"))

# WorldInfoManager's original constructor still initializes its collections.
# Its tail call to the GC write barrier is moved into this small trampoline.
# We then add and select one local world using the client's own methods.
# WorldInfo.ToString is already repurposed as the r2 loopback getter; the rest
# of that method is available without overwriting any adjacent method.
cave = 0x3C22EC0
emit(0x3C21E64, f"b {cave}")
emit(cave, """
    stp x29, x30, [sp, #-32]!
    stp x20, x19, [sp, #16]
    mov x19, x0
    bl 0x3450A90
    sub x19, x19, #32
    adrp x0, 0x8B49000
    add x0, x0, #0x400
    bl 0x3450AE4
    adrp x20, 0x8B49000
    ldr x20, [x20, #0x400]
    mov x0, x19
    mov x1, x20
    mov x2, x20
    mov x3, x20
    mov x4, x20
    mov w5, #5001
    mov x6, xzr
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
    ldp x29, x30, [sp], #32
    ret
""")
# Initialize the installed BM root before the scene reads downloaded tables.
# This diagnostic build also exports the encrypted cached database archive
# through the client's own decoder, allowing its index to be inspected locally.
bootstrap = 0x4FC5B50
text_start = bootstrap + 0x200
root_text = b"/sdcard/Android/data/com.netmarble.nanagb/files/bm\0"
input_text = b"".join(root_text[:-1] + ("/br-"+section+".bin\0").encode() for section in ["b","c","enl","enu","jas","kr","m","s","w"]) + b"\0"
output_text = b"/sdcard/gc-decoded-database.bin\0"
input_va = text_start + len(root_text)
output_va = input_va + len(input_text)
emit(0x4FC6900, f"b {bootstrap}")
emit(bootstrap, f"""
    stp x29, x30, [sp, #-64]!
    stp x20, x19, [sp, #16]
    stp x22, x21, [sp, #32]
    mov x19, x0
    mov w0, #1
    mov x1, xzr
    bl 0x3E48B64
    adrp x0, {text_start & ~0xFFF}
    add x0, x0, #{text_start & 0xFFF}
    bl 0x33EE200
    mov x20, x0
    mov x1, xzr
    bl 0x5734600
    mov x0, xzr
    bl 0x4823CE8
    mov x1, x20
    mov x2, xzr
    bl 0x4823D74
    mov x0, x20
    mov x1, xzr
    bl 0x5734600
    adrp x22, {input_va & ~0xFFF}
    add x22, x22, #{input_va & 0xFFF}
load_index:
    mov x0, x22
    bl 0x33EE200
    mov x1, xzr
    bl 0x7839DE0
    mov x20, x0
    mov x0, xzr
    bl 0x4823CE8
    mov x1, x20
    mov x2, xzr
    bl 0x48252D8
    mov w21, w0
    mov x0, x22
    bl 0x33EE200
    mov x1, xzr
    cbnz w21, index_ok
    mov x0, xzr
index_ok:
    bl 0x5734600
next_character:
    ldrb w8, [x22], #1
    cbnz w8, next_character
    ldrb w8, [x22]
    cbnz w8, load_index
    mov x0, xzr
    bl 0x4823CE8
    mov w1, #1
    mov x2, xzr
    bl 0x4824D4C
done:
    mov x0, x19
    ldp x22, x21, [sp, #32]
    ldp x20, x19, [sp, #16]
    ldp x29, x30, [sp], #64
    stp x30, x21, [sp, #-32]!
    b 0x4FC6904
""")
# Local, pre-decoded Unity bundles can pass through the cache decoder.
# Non-Unity data continues through the original decryption implementation.
emit(0x4FF1C5C, "b 0x4FC5C80")
emit(0x4FC5C80, """
    cbz x1, encrypted
    ldr x8, [x1, #24]
    cmp x8, #8
    b.lt encrypted
    ldr x8, [x1, #32]
    movz x9, #0x6e55
    movk x9, #0x7469, lsl #16
    movk x9, #0x4679, lsl #32
    movk x9, #0x0053, lsl #48
    cmp x8, x9
    b.ne encrypted
    str x1, [x2]
    mov w0, #1
    ret
encrypted:
    sub sp, sp, #0x40
    b 0x4FF1C60
""")
strings = root_text + input_text + output_text
assert text_start + len(strings) < 0x4FC6040
image[text_start - 0x4000:text_start - 0x4000 + len(strings)] = strings
OUTPUT.write_bytes(image)
print(f"OUTPUT={OUTPUT}\nSHA256={hashlib.sha256(image).hexdigest()}")
