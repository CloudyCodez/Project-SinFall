import lief
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
p=lief.parse('Original-APK/libProudNetClientPlugin.phone-simple.so')
cs=Cs(CS_ARCH_ARM64,CS_MODE_ARM)
for s in p.exported_symbols:
 if 'MessageMaxLength' in s.name:
  print(hex(s.value),s.name)
  if s.type.name=='FUNC':
   for ins in cs.disasm(bytes(p.get_content_from_virtual_address(s.value,80)),s.value): print(hex(ins.address),ins.mnemonic,ins.op_str)
