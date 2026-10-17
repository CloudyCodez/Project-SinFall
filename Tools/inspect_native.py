"""Disassemble preserved ARM64 code with matching Il2CppDumper method names.

Cpp2IL's textual Disassembly sections used incorrect ELF file translation;
this utility reads the actual PT_LOAD segments instead of trusting that text.
"""
import json
import struct
import sys
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = Path(r"E:\7DS-Offline")
data = (ROOT / "Original-APK/libil2cpp.original.so").read_bytes()
phoff = struct.unpack_from("<Q", data, 32)[0]
phsize, phcount = struct.unpack_from("<HH", data, 54)
segments = []
for index in range(phcount):
    record = struct.unpack_from("<IIQQQQQQ", data, phoff + index * phsize)
    if record[0] == 1:
        segments.append((record[3], record[2], record[5]))
def offset(va):
    for start, file_start, size in segments:
        if start <= va < start + size:
            return file_start + va - start
    raise ValueError(f"Address outside file-backed PT_LOAD: {va:#x}")

metadata = json.loads((ROOT / "Research/Il2CppDumper/script.json").read_text())
methods = {x["Address"]: x["Name"] for x in metadata["ScriptMethod"]}
decoder = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
for argument in sys.argv[1:]:
    addr, sep, length = argument.partition(":")
    va = int(addr, 0)
    count = int(length, 0) if sep else 256
    print(f"\n{va:#x} {methods.get(va, '')}")
    file_offset = offset(va)
    for instruction in decoder.disasm(data[file_offset:file_offset + count], va):
        annotation = ""
        if instruction.mnemonic in ("bl", "b") and instruction.op_str.startswith("#"):
            annotation = methods.get(int(instruction.op_str[1:], 0), "")
        print(f"{instruction.address:#x} {instruction.mnemonic:7} {instruction.op_str:35} {annotation}")
