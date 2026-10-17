"""Replace forward dash reused on return with each fighter's Legends retreat."""
import json,zlib
from copy import deepcopy
import build_db_legends_models as c
from build_db_legends_animations import FORMS,COMMON
from build_db_legends_vegeta_animations import FORMS as VEGETA
from UnityPy.helpers.TypeTreeHelper import write_typetree
from UnityPy.streams import EndianBinaryWriter

changes=[]
for model,file,prefix,*_ in [*FORMS,*VEGETA]:
    env=c.UnityPy.load(str(c.SOURCE/file))
    source=next(o for o in env.objects if o.type.name=='AnimationClip' and o.read().m_Name==prefix+'_BAS_BUKUU_B')
    actual=json.loads((c.ROOT/'Research/DBLegends'/f'{model}-rig.json').read_text())['paths']
    hashes={}
    for path in actual:
        segments=path.split('/')
        for i in range(len(segments)):
            hashes.setdefault(zlib.crc32('/'.join(segments[i:]).encode()),path)
    for row in list(c.report):
        if not row['logical'].startswith('phoenix_dbl_'+model+'_animations_'):continue
        target=c.UnityPy.load(str(c.OUT/row['file']));count=0
        for o in target.objects:
            if o.type.name!='AnimationClip' or 'return' not in o.read().m_Name:continue
            old=o.read_typetree();t=deepcopy(source.read_typetree())
            for b in t['m_ClipBindingConstant']['genericBindings']:
                if b['typeID']!=4:continue
                assert b['path'] in hashes,(model,b['path'])
                b['path']=zlib.crc32(hashes[b['path']].encode())
                if model=='gogeta_blue' and b['attribute']==1 and b['path']==zlib.crc32(b'VisualRoot/b_C_Base'):
                    b['path']=zlib.crc32(b'LegendsRootMotion')
            def merge(dst,src):
                if isinstance(dst,dict) and isinstance(src,dict):return {k:merge(v,src[k]) if k in src else v for k,v in dst.items()}
                return deepcopy(src)
            t=merge(old,t);t['m_Name']=old['m_Name'];t['m_Events']=[]
            t['m_MuscleClip']['m_LoopTime']=False
            t['m_MuscleClip']['m_AverageSpeed']=dict(x=0.0,y=0.0,z=6.0)
            w=EndianBinaryWriter(endian=o.reader.endian)
            node=next(n for n in o._get_typetree_node().m_Children if n.m_Name=='m_MuscleClip')
            write_typetree(t['m_MuscleClip'],node,w,o.assets_file);t['m_MuscleClipSize']=len(w.bytes)
            o.save_typetree(t);count+=1
            changes.append(dict(model=model,clip=t['m_Name'],source=source.read().m_Name))
        if count:
            paths=[(p,v.asset.m_PathID) for o in target.objects if o.type.name=='AssetBundle' for p,v in o.read().m_Container]
            deps=c.bundles[c.bundle_key(row['file'])]['deps'];c.report.remove(row);c.emit(target,row['logical'],paths,deps)
(c.OUT/'br-m.bin').write_bytes(c.write(*c.manifest))
(c.OUT/'assets.json').write_text(json.dumps(c.report,indent=2))
(c.ROOT/'Research/DBLegends/retreat-registration.json').write_text(json.dumps(changes,indent=2))
print('Retargeted',len(changes),'return states to original backward flight')
