"""Register generated artwork in native common and English UI modules."""
from pathlib import Path
import json,shutil
from PIL import Image
helper=Path(__file__).with_name('build_kaneki_assets.py')
exec(compile(helper.read_text().split("donor='253")[0],str(helper),'exec'))
manifest=read((OUT/'br-m.bin').read_bytes());bundles,aliases,dirs=manifest
report=json.loads((OUT/'assets.json').read_text());logical='phoenix_tg_original_banner'
report=[r for r in report if r['logical']!=logical]
e=load(ROOT/'Research/PhoneAssets/bm/enu/F9FC829D52731A9344505F5117EA199A')
tex=next(o for o in e.objects if o.type.name=='Texture2D');data=tex.read();data.m_Name='bg_banner_gacha_tg_original'
# Match native power-of-two card textures and keep the art's aspect ratio.
art=Image.open(ROOT/'Research/TokyoGhoul/original-banner.png').convert('RGBA')
canvas=Image.new('RGBA',(1024,1024),(12,9,20,255));art.thumbnail((1024,1024));canvas.alpha_composite(art,((1024-art.width)//2,(1024-art.height)//2))
data.set_image(canvas,target_format=4);data.save()
paths=[(f'assets/sevensins/patchresources/ui/image/gachabackground/{folder}bg_banner_gacha_tg_original.png',tex.path_id) for folder in ['','gachabackground_en/']]
emit(e,logical,paths);(OUT/'br-m.bin').write_bytes(write(*manifest));(OUT/'assets.json').write_text(json.dumps(report,indent=2))
english=read((ROOT/'Research/PhoneAssets/bm/br-enu.bin').read_bytes());key=bundle_key(report[-1]['file'])
# English assets must carry the enu module in the serialized bundle name.
# Reusing the common bundle with m/name leaves the localized load mismatched.
bundle=next(o for o in e.objects if o.type.name=='AssetBundle');bt=bundle.read_typetree();bt['m_Name']='enu/phoenix_tg_original_banner';bundle.save_typetree(bt)
from tg_bundle_identity import unique_files
unique_files(e,'enu/phoenix_tg_original_banner')
english_data=e.file.save(packer='lz4')
english_crc=zlib.crc32(b''.join(f.bytes if hasattr(f,'bytes') else f.save() for f in e.file.files.values()))
english[0][key]=dict(bundles[key],section=1002,crc=english_crc)
for path,_ in paths:
 base='assets/sevensins/patchresources/';directory,filename=path[len(base):].rsplit('/',1)
 english[2].setdefault(base,{}).setdefault(hash_name(directory+'/'),{})[hash_name(filename)]=key
out=OUT/'enu';out.mkdir(exist_ok=True);(out/report[-1]['file']).write_bytes(english_data);(out/'br-enu.bin').write_bytes(write(*english))
print('Registered original banner in common and English GachaBackground paths')
