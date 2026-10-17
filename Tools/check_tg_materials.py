"""Verify kagune native shader/texture bindings after asset serialization."""
from pathlib import Path
import json
import UnityPy
from PIL import ImageChops
root=Path(__file__).resolve().parents[1];out=root/'dist/kaneki-assets'
units=json.loads((root/'Research/TokyoGhoul/roster-port-inventory.json').read_text())
assets={r['logical']:r for r in json.loads((out/'assets.json').read_text())}
animated=0;ghouls=0
for u in units:
    if u['race']!='Ghoul':continue
    logical='phoenix_kaneki_model' if u['source']=='1065' else 'phoenix_tg_'+u['source']+'_model'
    env=UnityPy.load(str(out/assets[logical]['file']));a=env.assets[0]
    assert any(o.type.name=='Material' and o.read().m_Name=='PhoenixTGVisualsV3' for o in env.objects)
    for o in env.objects:
        if o.type.name!='SkinnedMeshRenderer':continue
        for p in o.read_typetree()['m_Materials']:
            m=a.objects[p['m_PathID']].read_typetree();sp=m['m_Shader']
            if sp['m_FileID']:continue
            shader=a.objects[sp['m_PathID']].read_typetree()['m_ParsedForm']['m_Name']
            if shader!='SevenDeadlySins/SpriteSheet':continue
            floats=dict(m['m_SavedProperties']['m_Floats']);tex=dict(m['m_SavedProperties']['m_TexEnvs'])['_MainTex']['m_Texture']
            assert not tex['m_FileID']
            t=a.objects[tex['m_PathID']].read();im=t.image.convert('RGBA')
            assert im.size==(1024,1024) and floats['_Cols']==4 and floats['_Rows']==4 and floats['_Speed']>0
            assert ImageChops.difference(im.crop((0,0,256,256)),im.crop((256,0,512,256))).getbbox() is not None,'Static effect atlas'
            assert im.getchannel('A').getextrema()[0]<255,'Opaque effect backing'
            animated+=1
    ghouls+=1
assert animated>0
print(f'PASS: {ghouls} ghoul prefabs; {animated} animated kagune material bindings, non-static frames and transparent backing')
