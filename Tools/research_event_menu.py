"""Resolve native event JSON literals through ELF relocations."""
import inspect_native as n,struct,re
shoff=struct.unpack_from('<Q',n.data,40)[0];size,count=struct.unpack_from('<HH',n.data,58);rel={}
for index in range(count):
 h=struct.unpack_from('<IIQQQQIIQQ',n.data,shoff+index*size)
 if h[1]==4:
  for off in range(h[4],h[4]+h[5],h[9]):
   addr,info,addend=struct.unpack_from('<QQq',n.data,off);rel[addr]=addend
strings={s['Address']:s['Value'] for s in n.metadata['ScriptString']}
def literals(start,size):
 regs={};seen=set()
 for i in n.decoder.disasm(n.data[n.offset(start):n.offset(start)+size],start):
  a=re.fullmatch(r'(x\d+), #(0x[0-9a-f]+)',i.op_str)
  if i.mnemonic=='adrp' and a:regs[a[1]]=int(a[2],16)
  a=re.fullmatch(r'(x\d+), \[(x\d+)(?:, #(0x[0-9a-f]+|[0-9]+))?\]',i.op_str)
  if i.mnemonic=='ldr' and a:
   addr=regs.get(a[2],0)+int(a[3] or '0',0)
   v=rel.get(addr,0)
   if v in strings and (v,strings[v]) not in seen:print(hex(i.address),strings[v]);seen.add((v,strings[v]))
   regs[a[1]]=v
if __name__=='__main__':
 for start,size in [(0x504640c,0x2d00),(0x55bae04,0x258),(0x55bb1c0,0x4a0)]:
  print('LITERALS',hex(start));literals(start,size)
