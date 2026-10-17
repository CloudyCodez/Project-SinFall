"""Extend native race name lookups for Ghoul without changing existing races.

Uses the unused automation-only GetFortSolgresKey method as executable space.
No gameplay methods are removed; the debug automation entry is unavailable in
the offline client. Original non-Ghoul getter paths are retained verbatim.
"""
import json,struct
from pathlib import Path
from keystone import Ks,KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN
ROOT=Path(__file__).resolve().parents[1]
def patch():
    path=ROOT/'Original-APK/libil2cpp.phone-local.so';data=bytearray(path.read_bytes())
    original=(ROOT/'Original-APK/libil2cpp.original.so').read_bytes()
    phoff=struct.unpack_from('<Q',data,32)[0];size,count=struct.unpack_from('<HH',data,54)
    segments=[struct.unpack_from('<IIQQQQQQ',data,phoff+i*size) for i in range(count)]
    def offset(a):
        s=next(s for s in segments if s[0]==1 and s[3]<=a<s[3]+s[5]);return s[2]+a-s[3]
    meta={r['Address']:r['Name'] for r in json.loads((ROOT/'Research/Il2CppDumper/script.json').read_text())['ScriptMethod']}
    cave=0x4063c38;assert meta[cave]=='TasMessageHandler$$GetFortSolgresKey'
    ks=Ks(KS_ARCH_ARM64,KS_MODE_LITTLE_ENDIAN)
    for index,(address,name) in enumerate([(0x4366cc4,'Util$$GetKindName'),(0x4366f18,'Util$$GetKindTypeLocalizeName'),(0x435c820,'Util$$GetKindIconSpriteName')]):
        assert meta[address]==name
        slot=cave+index*64;off=offset(address)
        branch=bytes(ks.asm(f'b #{slot}',addr=address)[0])
        assert bytes(data[off:off+4]) in [original[off:off+4],branch],name
        # Both language names use our translation ID. Reuse a valid native
        # race icon for the additional enum while preserving its race value.
        custom='mov w0,#6; b #'+str(slot+24) if index==2 else 'mov w0,#'+str(1300101&65535)+'; movk w0,#'+str(1300101>>16)+',lsl #16; mov x1,xzr; b #0x436435c'
        code=bytes(ks.asm(f'cmp w0,#7; b.ne #{slot+24}; '+custom,addr=slot)[0])
        data[offset(slot):offset(slot)+len(code)]=code
        data[offset(slot+24):offset(slot+28)]=original[off:off+4]
        jump=bytes(ks.asm(f'b #{address+4}',addr=slot+28)[0]);data[offset(slot+28):offset(slot+32)]=jump
        data[off:off+4]=branch
    # The default inventory filter enumerates only the shipped six races.
    # Append Ghoul to that list so existing Kaneki/Haise entries stay visible.
    address=0x5434f40;slot=cave+192;off=offset(address)
    assert meta[0x5434dfc]=='SkinData$$GetAllValidKindFilterList'
    branch=bytes(ks.asm(f'b #{slot}',addr=address)[0])
    assert bytes(data[off:off+4]) in [original[off:off+4],branch]
    code=bytes(ks.asm('mov w1,#7; mov x0,x19; ldr x8,[x21]; ldr x8,[x8,#0x20]; ldr x8,[x8,#0xc0]; ldr x2,[x8,#0x70]; bl #0x637233c; mov x0,x19; b #0x5434f44',addr=slot)[0])
    assert len(code)<=84
    data[offset(slot):offset(slot)+len(code)]=code;data[off:off+4]=branch
    # The ordinary hero screen builds its default list independently instead
    # of calling GetAllValidKindFilterList. Extend that path too. Explicit
    # race selections keep their original behavior.
    address=0x5a0f1d8;slot=0x4063d4c;off=offset(address)
    assert meta[slot]=='TasMessageHandler$$RegistStamina'
    assert meta[0x5a0eed4]=='ViewHeroInventory.<GetKindFilteredSkinData>d__252$$MoveNext'
    branch=bytes(ks.asm(f'b #{slot}; nop',addr=address)[0])
    assert bytes(data[off:off+8]) in [original[off:off+8],branch]
    code=bytes(ks.asm(f'cmp w20,w0; b.ge #{slot+12}; b #0x5a0f1e0; ldr x8,[sp,#0x18]; ldr x0,[x8,#0x40]; mov w1,#7; ldr x8,[x28]; ldr x8,[x8,#0x20]; ldr x8,[x8,#0xc0]; ldr x2,[x8,#0x70]; bl #0x637233c; b #0x5a0f2fc',addr=slot)[0])
    assert len(code)<244
    data[offset(slot):offset(slot)+len(code)]=code;data[off:off+8]=branch
    # Inventory setup also filters the DB hero rows before creating HeroData.
    # Extend its all-races selection before the later view filter runs.
    address=0x5424bc0;slot=0x4063e40;off=offset(address)
    assert meta[slot]=='TasMessageHandler$$RegistQuestSide'
    branch=bytes(ks.asm(f'b #{slot}',addr=address)[0])
    assert bytes(data[off:off+4]) in [original[off:off+4],branch]
    code=bytes(ks.asm(f'mov x0,x22; mov w1,#7; mov x2,xzr; bl #0x4c7ab48; cbnz w0,#{slot+36}; mov x0,x22; mov x1,xzr; bl #0x4c7ac40; cbz w0,#{slot+68}; mov x0,x20; mov w1,#7; ldr x8,[x29]; ldr x8,[x8,#0x20]; ldr x8,[x8,#0xc0]; ldr x2,[x8,#0x70]; bl #0x637233c; nop; adrp x8,#0x8743000; b #0x5424bc4',addr=slot)[0])
    assert len(code)<244
    data[offset(slot):offset(slot)+len(code)]=code;data[off:off+4]=branch
    path.write_bytes(data);print('Patched distinct Ghoul race names and safe native race icon')
if __name__=='__main__':patch()
