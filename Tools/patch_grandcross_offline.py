"""Build the persistent, Frida-free Grand Cross local client library."""
from pathlib import Path
import hashlib
import struct

from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = Path(r"E:\7DS-Offline")
SOURCE = ROOT / "Original-APK" / "libil2cpp.original.so"
OUTPUT = ROOT / "Original-APK" / "libil2cpp.cloud-local-r2.so"


def words(*values: int) -> bytes:
    return b"".join(struct.pack("<I", value) for value in values)


def encode_adrp(rd: int, instruction_va: int, target_va: int) -> int:
    delta_pages = ((target_va & ~0xFFF) - (instruction_va & ~0xFFF)) >> 12
    if not -(1 << 20) <= delta_pages < (1 << 20):
        raise ValueError("ADRP target is out of range")
    immediate = delta_pages & ((1 << 21) - 1)
    immlo = immediate & 3
    immhi = immediate >> 2
    return 0x90000000 | (immlo << 29) | (immhi << 5) | rd


def expect_and_write(image: bytearray, offset: int, expected: bytes, replacement: bytes):
    actual = bytes(image[offset:offset + len(expected)])
    if actual != expected:
        raise RuntimeError(
            f"unexpected bytes at 0x{offset:X}: {actual.hex()} != {expected.hex()}"
        )
    if len(replacement) != len(expected):
        raise ValueError("replacement must preserve file layout")
    image[offset:offset + len(replacement)] = replacement


image = bytearray(SOURCE.read_bytes())

# PageLogin.NextProcess: retain the proven state-aware redirect. Stages 0-2
# advance normally so PageLogin initializes and verifies local connectivity.
# Once that completes, redirect to the normal NextScene path (26). The local
# build pins its game endpoint below, so publisher configuration, sessions,
# web views, and the patch chain are neither needed nor safe offline; the
# signed base configuration itself raises title-screen "Support Code 2" when
# consumed outside its retired live environment. Jumping directly to
# stage 26 from the function entry corrupts the calling convention on this
# build and crashes before the local connection is attempted.
next_process_offset = 0x4FBEA94
next_process_va = 0x4FC2A94
next_process_original_prefix = bytes.fromhex(
    "FE0F1CF8 F85F01A9 F65702A9 F44F03A9 34F001F0 883A5C39"
    " F30300AA 68030037 60BA0190"
)
# This exact sequence is the previously verified r1 patch.
next_process_patch = bytes.fromhex(
    "084440B9 1F090071 AB000054 1F690071 6A000054 41038052"
    " 6FF8FF17 01050011 6DF8FF17"
)
# Only replace the function prefix covered by the compact redirect.
existing_prefix = bytes(image[next_process_offset:next_process_offset + len(next_process_patch)])
if existing_prefix != next_process_patch:
    # Source is pristine, so validate its first instruction sequence before patching.
    if existing_prefix != next_process_original_prefix:
        raise RuntimeError("PageLogin.NextProcess source does not match this client build")
    image[next_process_offset:next_process_offset + len(next_process_patch)] = next_process_patch

# PageLogin.OnCheckFailed is the retired publisher patch/integrity failure
# callback. Offline, route it through NextProcess instead of presenting
# "Support Code 2" and stopping. x0 is already the PageLogin instance, so a
# tail branch preserves the correct calling convention and stack state.
on_check_failed_va = 0x4FC5B48
on_check_failed_offset = 0x4FC1B48
check_failed_delta = (next_process_va - on_check_failed_va) >> 2
expect_and_write(
    image,
    on_check_failed_offset,
    bytes.fromhex("FF0302D1"),  # sub sp,sp,#0x80
    words(0x14000000 | (check_failed_delta & 0x03FFFFFF)),
)

# PatchManager's failure callback is separate from the app-control callback
# above and is what displays the title-screen "Patch failed / Support Code 2"
# dialog. Treat the already-present phone asset set as complete and advance
# through the same state-safe transition used by successful bootstrap stages.
on_failed_patch_va = 0x4FC38F4
on_failed_patch_offset = 0x4FBF8F4
failed_patch_delta = (next_process_va - on_failed_patch_va) >> 2
expect_and_write(
    image,
    on_failed_patch_offset,
    bytes.fromhex("FE0F1FF8"),  # str x30,[sp,#-0x10]!
    words(0x14000000 | (failed_patch_delta & 0x03FFFFFF)),
)

# ExecuteProcess has completed its one-time metadata/status initialization by
# this point and is about to dispatch m_currentProcess through its jump table.
# Select the native NextScene case (26) here. This is intentionally *inside*
# the initialized function body: redirecting from the function entry skipped
# required setup and crashed this client build.
execute_dispatch_offset = 0x4FBD2F8
execute_dispatch_original = bytes.fromhex(
    "684640B9 08050051 1F650071 08BB0054"
)
str_state_26 = 0xB9000000 | ((0x44 // 4) << 10) | (19 << 5) | 8
execute_dispatch_patch = words(
    0x52800348,   # mov w8,#26
    str_state_26, # str w8,[x19,#0x44]
    0x52800328,   # mov w8,#25 (zero-based jump-table index)
    0xD503201F,   # nop (bounds check is unnecessary for constant 25)
)
expect_and_write(
    image,
    execute_dispatch_offset,
    execute_dispatch_original,
    execute_dispatch_patch,
)

# The actual Support Code 2 dialog originates in Patch's IPatchDelegate
# failure handler, before PageLogin's own failure callbacks. The offline build
# already ships the complete phone asset tree, so map that failure to Patch's
# normal completion callback. Both methods are instance methods on Patch and
# x0 is therefore already the correct receiver.
patch_on_failed_va = 0x5880AA8
patch_on_failed_offset = 0x587CAA8
patch_completed_va = 0x5882998
patch_completed_delta = (patch_completed_va - patch_on_failed_va) >> 2
expect_and_write(
    image,
    patch_on_failed_offset,
    bytes.fromhex("FF8301D1"),  # sub sp,sp,#0x60
    words(0x14000000 | (patch_completed_delta & 0x03FFFFFF)),
)

# Force the normal WorldInfo accessors to the loopback endpoint. This avoids
# Frida, DNS overrides, and dependency on publisher configuration responses.
port_offset = 0x3C1EE80
expect_and_write(
    image,
    port_offset,
    bytes.fromhex("003040B9 C0035FD6"),
    words(0x52800000 | (5001 << 5), 0xD65F03C0),  # mov w0,#5001; ret
)

ip_offset = 0x3C1EE88
to_string_offset = 0x3C1EEB0
ip_va = 0x3C22E88
to_string_va = 0x3C22EB0
literal_pointer_va = 0x8B49400  # managed string literal "127.0.0.1"
branch_delta = (to_string_va - ip_va) >> 2
ip_patch = words(0x14000000 | (branch_delta & 0x03FFFFFF), 0xD503201F)
expect_and_write(image, ip_offset, bytes.fromhex("001440F9 C0035FD6"), ip_patch)

# Reuse WorldInfo.ToString as a tiny shared local-IP getter. Its debug output
# remains useful (it now prints 127.0.0.1), while get_IP gains enough room for
# an ADRP/LDR/RET sequence without disturbing adjacent accessors.
to_string_patch = words(
    encode_adrp(0, to_string_va, literal_pointer_va),
    0xF9400000 | ((0x400 // 8) << 10),  # ldr x0,[x0,#0x400]
    0xD65F03C0,
)
expect_and_write(
    image,
    to_string_offset,
    bytes.fromhex("FE0F1DF8 F65701A9 F44F02A9"),
    to_string_patch,
)

OUTPUT.write_bytes(image)

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
for offset, va, size, label in (
    (port_offset, 0x3C22E80, 8, "get_Port"),
    (ip_offset, ip_va, 8, "get_IP"),
    (to_string_offset, to_string_va, 12, "local IP trampoline"),
):
    decoded = "; ".join(f"{i.mnemonic} {i.op_str}" for i in md.disasm(bytes(image[offset:offset+size]), va))
    print(f"{label}: {decoded}")
print(f"{OUTPUT}\nSHA256={hashlib.sha256(image).hexdigest().upper()}")
