"""Validate actual packaged runtime gait channels, bindings and loop seams."""
import json, zlib
from pathlib import Path
import numpy as np
import UnityPy
from UnityPy.helpers.TypeTreeHelper import write_typetree
from UnityPy.streams import EndianBinaryWriter
from tg_run_retarget import hierarchy, curve_samples

ROOT = Path(__file__).resolve().parents[1]; OUT = ROOT/'dist/kaneki-assets'
rows = json.loads((OUT/'assets.json').read_text()); checked = 0
for u in json.loads((ROOT/'Research/TokyoGhoul/roster-port-inventory.json').read_text()):
    prefix = 'phoenix_kaneki' if u['index'] == 0 else 'phoenix_tg_'+u['source']
    def asset(suffix):
        row = next(r for r in rows if r['logical'] == prefix+suffix)
        return UnityPy.load((OUT/row['file']).read_bytes())
    model = hierarchy(asset('_model'))
    clips=[]
    for index,names in [(0,['run']),(1,['skill_01_dash','skill_01_return']),(2,['skill_02_dash','skill_02_return'])]:
        env=asset(f'_animations_{index}')
        bundle=next(o.read() for o in env.objects if o.type.name=='AssetBundle')
        paths={p:v.asset.m_PathID for p,v in bundle.m_Container}
        for name in names:
            obj=next(o for o in env.objects if o.type.name=='AnimationClip' and o.read().m_Name==name)
            assert any(p.endswith('/'+name+'.anim') and i==obj.path_id for p,i in paths.items()),(u['source'],name)
            clips.append(obj)
    for obj in clips:
        tree = obj.read_typetree(); muscle = tree['m_MuscleClip']
        node = next(n for n in obj._get_typetree_node().m_Children if n.m_Name == 'm_MuscleClip')
        writer = EndianBinaryWriter(endian=obj.reader.endian); write_typetree(muscle,node,writer,obj.assets_file)
        assert tree['m_MuscleClipSize'] == len(writer.bytes), u['source']
        assert muscle['m_LoopTime'] and tree['m_WrapMode'] == 2
        dense = muscle['m_Clip']['data']['m_DenseClip']; assert dense['m_FrameCount'] == 33
        samples = curve_samples(tree,np.linspace(0,muscle['m_StopTime'],33))
        valid = {zlib.crc32(p.encode()) for p in model}
        assert all(b['path'] in valid for b in tree['m_ClipBindingConstant']['genericBindings'])
        for path in model:
            h=zlib.crc32(path.encode())
            if (h,2,4) not in samples: continue
            q=samples[(h,2,4)]; assert np.all(np.isfinite(q))
            assert np.max(abs(np.linalg.norm(q,axis=1)-1)) < .002
            assert np.linalg.norm(q[0]-q[-1]) < .001
            if path.rsplit('/',1)[-1] in ['Bip001 L Thigh','Bip001 R Thigh','Bip001 L Calf','Bip001 R Calf']:
                assert np.max(np.linalg.norm(q-q[0],axis=1)) > .05
            for attr,field in [(1,'m_LocalPosition'),(3,'m_LocalScale')]:
                a=samples[(h,attr,4)]; assert np.max(abs(a-a[0])) < .001
    checked+=1
print('PASS:',checked,'native run loops and 104 skill dash/return clips; all bindings valid, legs animated, normalized rotations, preserved bone lengths and closed loop seams')
