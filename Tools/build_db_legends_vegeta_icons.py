"""Use the three source Legends battle portraits for native GC icon lookups."""
import json
import build_db_legends_models as ctx
from build_db_legends_models import ROOT,OUT,SOURCE,UnityPy,gc,clone,emit,write
from PIL import Image

for model,file,name in [('vegeta_base', '6fc4483c14088ae7fab17a029b101d5cfa1df4a0', 'BChaIco_0257_Vegeta_257'), ('vegeta_super', 'b8efb9acbf967da24bb0f51fe779eaeea9400540', 'BChaIco_0257_VegetaSS1_257'), ('vegeta_blue', '88ee58811656d02183e1bfbb04aefc39aa9158b0', 'BChaIco_0217_VegetaSSGSS_217'), ('gogeta_blue', '02e4bd794a3cd4a8c925216f7230128b94671f4f', 'BChaIco_0729_GogetaSSGSS_729')]:
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
