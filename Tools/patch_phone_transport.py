from pathlib import Path
import lief, struct
p=Path('Original-APK/libProudNetClientPlugin.phone-simple.so')
b=bytearray(p.read_bytes()); elf=lief.parse(str(p))
s=next(s for s in elf.exported_symbols if s.name=='_ZN5Proud10CNetConfig16MessageMaxLengthE')
o=elf.virtual_address_to_offset(s.value)
print('Original message limit:',struct.unpack_from('<I',b,o)[0])
struct.pack_into('<I',b,o,1073741824)
for va in (0x12ee80,0x12ee88):
 off=elf.virtual_address_to_offset(va)
 b[off:off+8]=struct.pack('<II',0x52a00200,0xd65f03c0)
p.write_bytes(b)
print('Phone transport limit set to 1 MiB')
