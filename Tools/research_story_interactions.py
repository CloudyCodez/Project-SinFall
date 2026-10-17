from pathlib import Path
import json,sys,contextlib,io
root=Path(__file__).resolve().parents[1]
s=(root/'Research/Il2CppDumper/dump.cs').read_text(encoding='utf8')
for name in ['DropInteractiveResult','DropInteractiveInfo','UniqueInteractiveResult','UserRecipeInfo','UserNpcResult','DBCookingRecipeRow','DBCookingListRow','DBCookingMaterialRow','ShopBuyInfo','ShopBuyRequestInfo','ShopInfo']:
 marker='public class '+name+' '
 if marker in s:
  a=s.index(marker);b=min(s.index('// Methods',a),s.index('// Properties',a)) if '// Properties' in s[a:s.index('// Methods',a)] else s.index('// Methods',a)
  print(s[a:b][:6000])
meta=json.loads((root/'Research/Il2CppDumper/script.json').read_text())['ScriptMethod']
for r in meta:
 if any(x in r['Name']+' '+r['Signature'] for x in ['CG_RequestCookingStart','CG_RequestBasePointShopInfo','CG_RequestBasePointShopBuy','CookingResult_o','UserRecipeInfo_o','UserNpcResult_o','ShopBuyInfo_o','ShopBuyRequestInfo_o','ShopInfo_o','ShopProduct_o','CG_RequestBasePointDropInteractiveOpen','CG_RequestLobbyDropInteractiveOpen','CG_RequestBasePointUniqueInteractiveOpen','DropInteractiveResult_o']):
  if ('Marshaler' in r['Name'] and '$$Read' in r['Name']) or ('Proxy' in r['Name'] and '$$CG_' in r['Name']):print(hex(r['Address']),r['Name'],r['Signature'])
with contextlib.redirect_stdout(io.StringIO()):import map_login_read_schema as schemas
for addr in [0x36df06c,0x36d7534,0x36c44cc,0x36c3f58]:print(hex(addr),schemas.schema(addr))
for r in meta:
 if any(x in r['Name'] for x in ['CG_RequestBasePointDropInteractiveOpenOK','CG_RequestLobbyDropInteractiveOpenOK','CG_RequestBasePointUniqueInteractiveOpenOK']) and 'Delegate$$Invoke' in r['Name']:print(hex(r['Address']),r['Name'],r['Signature'])
