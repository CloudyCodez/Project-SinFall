from pathlib import Path
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

path = Path(r"E:\7DS-Offline\Original-APK\libil2cpp.original.so")
data = path.read_bytes()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
for name, off, size in [
    ("NextProcess", 0x4FBEA94, 0x140),
    ("ExecuteProcess", 0x4FBCF04, 0x180),
    ("SetExecuteProcess", 0x4FBCC68, 0x100),
    ("GameServerConnect", 0x4FC2AA0, 0x140),
    ("PacketConnect", 0x5468198, 0x140),
]:
    print(f"\n== {name} file+0x{off:X} ==")
    for ins in md.disasm(data[off:off+size], off):
        print(f"0x{ins.address:08x}: {ins.mnemonic:8} {ins.op_str}")
