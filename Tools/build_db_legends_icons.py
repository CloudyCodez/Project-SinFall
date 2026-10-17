"""Use the three source Legends battle portraits for native GC icon lookups."""
import json
import build_db_legends_models as ctx
from build_db_legends_models import ROOT,OUT,SOURCE,UnityPy,gc,clone,emit,write
from PIL import Image

for model,file,name in [('goku_base','708645ff7a44c93a9ac52af9263699c60017d431','BChaIco_0401_Goku_401'),('goku_blue','95a51e38981bc3a12a0009307d4c6e9ac5a54eb3','BChaIco_0517_GokuSSGSS_517'),('goku_ui','f0397e97fb13b8006d61886dfcb5a92fb18bb5dc','BChaIco_0586_GokuUIS_586')]:
    source=UnityPy.load(str(SOURCE/file));image=next(o.read().image for o in source.objects if o.type.name=='Texture2D' and o.read().m_Name==name)
    image.save(str(ROOT/'Research/DBLegends'/f'{model}-source-icon.png'))
    env=gc('253AD473855C32C7DC4EC70CA51D9A7D');asset=env.assets[0];bundle=next(o for o in env.objects if o.type.name=='AssetBundle');template=next(o for o in env.objects if o.type.name=='Texture2D');asset.objects={bundle.path_id:bundle}
    texture=clone(template,asset,8200000000000000001);data=texture.read();data.m_Name=model+'_portrait';data.set_image(image.convert('RGBA'),target_format=4);data.save()
    paths=[]
    for prefix in ['icon_hero_','icon_skin_']:
        for suffix in ['_s','_l','_card']:
            name=prefix+model+'_0001'+suffix
            for folder in ['costume','hero','Hero_Coin','skillactive/hero']:
                paths.append((f'assets/sevensins/patchresources/ui/image/icon/{folder}/{name}.png',texture.path_id))
    paths.append((f'assets/sevensins/patchresources/ui/image/icon/hero/{model}_0001.png',texture.path_id))
    logical='phoenix_dbl_'+model+'_icon';ctx.report[:]=[r for r in ctx.report if r['logical']!=logical];emit(env,logical,paths)
    print(model,'source portrait',image.size)
(OUT/'br-m.bin').write_bytes(write(*ctx.manifest));(OUT/'assets.json').write_text(json.dumps(ctx.report,indent=2))
