from pathlib import Path
import struct
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
ROOT=Path(__file__).resolve().parents[1]
root=ROOT/'Original-APK'; b=bytearray((root/'libil2cpp.cloud-local-r21.so').read_bytes())
ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
va=0x79e8338
code=bytes(ks.asm('strb wzr,[x0,#0x21]; ret',addr=va)[0])
phoff=struct.unpack_from('<Q',b,32)[0]; size,count=struct.unpack_from('<HH',b,54)
for i in range(count):
 s=struct.unpack_from('<IIQQQQQQ',b,phoff+i*size)
 if s[0]==1 and s[3]<=va<s[3]+s[5]:
  off=s[2]+va-s[3];b[off:off+len(code)]=code; break
(root/'libil2cpp.phone-local.so').write_bytes(b)
from patch_content_unlocks import patch
patch(root/'libil2cpp.phone-local.so')
for p in (ROOT/'Server/Protocol/Generated').glob('*.cpp'):
 text=p.read_text();text=text.replace('__msg.SetSimplePacketMode(m_core->IsSimplePacketMode());','__msg.SetSimplePacketMode(false);')
 p.write_text(text)
