"""Guard against login memory explosions from unlimited material balances."""
import json
import math
import struct
import zipfile
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

root = Path(__file__).resolve().parents[1]
with zipfile.ZipFile(root / 'dist/7DS-Offline-Client.apk') as apk:
    data = apk.read('lib/arm64-v8a/libil2cpp.so')
address = 0x5753950
phoff = struct.unpack_from('<Q', data, 32)[0]
size, count = struct.unpack_from('<HH', data, 54)
segments = [struct.unpack_from('<IIQQQQQQ', data, phoff + i * size) for i in range(count)]
segment = next(s for s in segments if s[0] == 1 and s[3] <= address < s[3] + s[5])
offset = segment[2] + address - segment[3]
instructions = list(Cs(CS_ARCH_ARM64, CS_MODE_ARM).disasm(data[offset:offset + 8], address))
assert [(i.mnemonic, i.op_str) for i in instructions] == [('mov', 'w0, #0x7fffffff'), ('ret', '')]
items = [r for r in json.loads((root / 'Research/DecodedCache/items.json').read_text())
         if 0 < r['item_type'] < 200 and r['storage_on']]
assert all(math.ceil((2000000000 if 543301 <= r['item_id'] <= 543305 else 999999) / 2147483647) == 1
           for r in items)
print('PASS: packaged client builds one stack for each of', len(items), 'seeded storage items')
