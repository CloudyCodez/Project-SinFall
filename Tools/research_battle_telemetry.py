from pathlib import Path
import json,re,io,contextlib
root=Path(__file__).resolve().parents[1]
s=(root/'Research/Il2CppDumper/dump.cs').read_text(encoding='utf8')
for m in re.finditer(r'public bool isWin;',s):
 a=s.rfind('public class ',0,m.start());b=s.find('// Methods',m.end())
 block=s[a:b]
 if 'stage' in block.lower() and len(block)<9000:print(block)
with contextlib.redirect_stdout(io.StringIO()):import map_login_read_schema as schemas
schemas.primitive['uint32_t']='i'
for r in schemas.n.metadata['ScriptMethod']:
 if 'Marshaler$$Read' in r['Name'] and '__________81_o**' in r['Signature']:
  print(hex(r['Address']),r['Signature'],schemas.schema(r['Address']))
