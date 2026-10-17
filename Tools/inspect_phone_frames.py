from pathlib import Path
import struct
for p in sorted(Path('Research/PhoneProtocol').glob('*server.bin'))[-2:]:
 b=p.read_bytes(); print(p,len(b)); i=b.find(b'\x09\x09')
 while i+6<=len(b):
  n=struct.unpack_from('<I',b,i+2)[0]
  print(i,n,b[i+6:i+26].hex()); i+=6+n
