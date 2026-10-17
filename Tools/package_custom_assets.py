"""Install additive custom bundles before Unity reads its cache manifests."""
from pathlib import Path
import re,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];decoded=ROOT/'Research/PhoneClientDecoded'
source=ROOT/'dist/kaneki-assets'
if not (source/'assets.json').exists():raise SystemExit('No custom assets built')
template=(decoded/'smali/com/phoenix/offline/SummonCatalog.smali').read_text().split('.method public static installManifest',1)[0].split('.method',1)[1]
template='.method'+template
methods=[];entries=[]
for file in source.iterdir():
 if file.is_file() and (re.fullmatch('[A-F0-9]{32}',file.name) or file.name=='br-m.bin'):
  entries.append((file,'bm' if file.name.startswith('br-') else 'bm/m'))
for module in ('enl','enu','s'):
 if (source/module).exists():
  for file in (source/module).iterdir():entries.append((file,'bm' if file.name.startswith('br-') else 'bm/'+module))
for index,(file,destination) in enumerate(entries):
 asset=f'offline-custom/{index}/{file.name}';out=decoded/'assets'/asset;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(file,out)
 text=template.replace('install(','copy%d('%index).replace('"offline_catalog"',f'"offline_custom_{index}"').replace('"bm/b"',f'"{destination}"').replace('offline-db/30FF13B981773B83827E17DB9C456368',asset).replace('30FF13B981773B83827E17DB9C456368',file.name)
 text=re.sub(r'"[a-f0-9]{64}"','"'+hashlib.sha256(file.read_bytes()).hexdigest()+'"',text)
 text=text.replace('Installed three-banner summon catalog','Installed custom asset '+file.name)
 methods.append(text)
# Keep the additive installer in its own DEX: the original primary DEX is
# already close to the 65,536 method-reference limit.
legacy=decoded/'smali/com/phoenix/offline/CustomAssets.smali'
if legacy.exists():legacy.unlink()
helper=decoded/'smali_classes5/com/phoenix/offline/CustomAssets.smali'
helper.parent.mkdir(parents=True,exist_ok=True)
header='.class public final Lcom/phoenix/offline/CustomAssets;\n.super Ljava/lang/Object;\n.method public static install(Landroid/content/Context;)V\n.locals 0\n'
header+=''.join(f'invoke-static {{p0}}, Lcom/phoenix/offline/CustomAssets;->copy{i}(Landroid/content/Context;)V\n' for i in range(len(entries)))+'return-void\n.end method\n'
helper.write_text(header+'\n'.join(methods))
activity=decoded/'smali_classes3/com/netmarble/fpplugin/FPActivity.smali';text=activity.read_text();call='    invoke-static {p0}, Lcom/phoenix/offline/CustomAssets;->install(Landroid/content/Context;)V\n\n';marker='    invoke-super {p0, p1}, Lcom/netmarble/unity/NMGUnityPlayerActivity;->onCreate(Landroid/os/Bundle;)V'
if call.strip() not in text:text=text.replace(marker,call+marker)
activity.write_text(text);print('Packaged',len(entries),'custom assets/manifests')
