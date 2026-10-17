import sys,re
sys.path.insert(0,r'E:/7DS-Offline/Tools')
import inspect_native as n
meta={x['Address']:x for x in n.metadata['ScriptMethod']}; addresses=sorted(meta)
from bisect import bisect_right
primitive={'int32_t':'i','int64_t':'l','uint8_t':'b','int16_t':'h','bool':'o','float':'f','double':'q','System_String_o*':'s'}
def schema(a):
 m=meta[a]; sig=m['Signature']
 if 'System_Collections_Generic_List' in sig:return 'i'
 if 'System_DateTime' in sig:return 'd'
 if m['Name'].startswith(('Nettention.Proud.Marshaler','Nettention.Proud.Message')):
  arg=sig.split(',')[1].strip().rsplit(' ',1)[0]
  if arg not in primitive:raise Exception((hex(a),sig,arg))
  return primitive[arg]
 out=''
 end=addresses[bisect_right(addresses,a)]
 for ins in n.decoder.disasm(n.data[n.offset(a):n.offset(a)+end-a],a):
  if ins.mnemonic in ('bl','b') and ins.op_str.startswith('#'):
   target=int(ins.op_str[1:],0)
   if target in meta and '$$Write' in meta[target]['Name']:out+=schema(target)
 return out
root=0x36b2514; out=''; field=''
for ins in n.decoder.disasm(n.data[n.offset(root):n.offset(root)+0x628],root):
 if ins.mnemonic.startswith('ldr') and ('w1,' in ins.op_str or 'x1,' in ins.op_str):field=ins.op_str
 if ins.mnemonic in ('bl','b'):
  a=int(ins.op_str[1:],0)
  if a in meta and '$$Write' in meta[a]['Name']:
   s=schema(a);print(len(out),field,s,meta[a]['Signature']);out+=s
print('FULL',out)


