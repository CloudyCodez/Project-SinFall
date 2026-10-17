"""Convert cached Legends Kamehameha particles to native GC effect prefabs."""
from copy import deepcopy
import json
import build_db_legends_models as c
from UnityPy.export import Texture2DConverter
from UnityPy.helpers.ResourceReader import get_resource_data

SOURCE_FILE='2f0b197f06f2a4ed790c80f452331e2c962f42ec'
EFFECTS=[('charge','kame_gokuuis_ult_crg01',198500001),('beam','kame_gokuuis_ult_beam',198500002),('impact','kame_gokuuis_ult_fireend',198500003),('release','kame_gokuuis_ult_fire',198500004)]

def merge(dst,src):
    if isinstance(dst,dict) and isinstance(src,dict):return {k:merge(v,src[k]) if k in src else v for k,v in dst.items()}
    return deepcopy(src)

def build(label,source_name,sfx,source_file=SOURCE_FILE,namespace='goku'):
    src=c.UnityPy.load(str(c.SOURCE/source_file));donor=c.gc('33F5ED49715B39003618C1986933CDD1');asset=donor.assets[0]
    templates={typ:next(o for o in donor.objects if o.type.name==typ) for typ in ['GameObject','Transform','ParticleSystem','ParticleSystemRenderer','Material','Mesh']}
    model=c.gc('253AD473855C32C7DC4EC70CA51D9A7D');templates['Texture2D']=next(o for o in model.objects if o.type.name=='Texture2D')
    shaders=c.gc('848ECA5317DD03D78753BB38EEA703D5');shader=next(o for o in shaders.objects if o.type.name=='Shader' and o.read().m_ParsedForm.m_Name=='Mobile/Particles/Alpha Blended')
    ab=next(o for o in donor.objects if o.type.name=='AssetBundle');asset.objects={ab.path_id:ab};mapping={};counter=8200000000000000000
    def resolve(o,p):
        if not p['m_PathID']:return None
        a=o.assets_file
        if p['m_FileID']:
            cab=a.externals[p['m_FileID']-1].path.rsplit('/',1)[-1]
            # Unity's builtin white texture/billboard resources are supplied
            # by the target engine when the corresponding reference is null.
            if cab.lower() in ['unity default resources','unity_builtin_extra']:return None
            if cab not in c.LOADED:c.LOADED[cab]=c.UnityPy.load(str(c.SOURCE/c.CAB_FILES[cab]))
            a=next(a for a in c.LOADED[cab].assets if a.name==cab)
        return a.objects[p['m_PathID']]
    def allocate(o,typ=None):
        nonlocal counter
        key=(o.assets_file.name,o.path_id)
        if key in mapping:return mapping[key]
        counter+=1;typ=typ or o.type.name
        n=c.clone(templates.get(typ,o),asset,counter);mapping[key]=n
        return n
    ns=allocate(shader);ns.save_typetree(shader.read_typetree())
    # Use additive blending for luminous source particles.
    st=ns.read_typetree()
    for sub in st['m_ParsedForm']['m_SubShaders']:
        for p in sub['m_Passes']:
            for key in ['destBlend','destBlendAlpha']:p['m_State']['rtBlend0'][key]['val']=1.0
    ns.save_typetree(st)
    def convert(o):
        if not o:return c.ptr()
        key=(o.assets_file.name,o.path_id)
        if key in mapping:return c.ptr(mapping[key].path_id)
        typ=o.type.name
        if typ not in ['Material','Texture2D','Mesh']:return c.ptr()
        n=allocate(o);t=o.read_typetree()
        if typ=='Texture2D':
            nt=templates[typ].read();nt.m_Name=t['m_Name'];nt.set_image(o.read().image,target_format=4);nt.save();t=nt.object_reader.read_typetree();n.save_typetree(t)
        elif typ=='Mesh':
            stream=t.get('m_StreamData',{})
            if stream.get('size'):t['m_VertexData']['m_DataSize']=get_resource_data(stream['path'],o.assets_file,stream['offset'],stream['size']);t['m_StreamData']=dict(path='',offset=0,size=0)
            n.save_typetree(merge(templates[typ].read_typetree(),t))
        else:
            t['m_Shader']=c.ptr(ns.path_id)
            props=t['m_SavedProperties'];props['m_TexEnvs']=[(name,dict(v,m_Texture=convert(resolve(o,v['m_Texture'])))) for name,v in props['m_TexEnvs'] if name=='_MainTex']
            t['m_CustomRenderQueue']=3000;t['m_ValidKeywords']=[];t['m_InvalidKeywords']=[]
            props['m_Colors']=[('_TintColor',dict(r=1.0,g=1.0,b=1.0,a=1.0))];n.save_typetree(merge(templates[typ].read_typetree(),t))
        return c.ptr(n.path_id)
    rootid=next(v.asset.m_PathID for p,v in next(o.read() for o in src.objects if o.type.name=='AssetBundle').m_Container if p.endswith('/'+source_name+'.prefab'))
    gos={o.path_id:o for o in src.objects if o.type.name=='GameObject'};trs={o.path_id:o for o in src.objects if o.type.name=='Transform'};selected=[]
    def visit(goid):
        go=gos[goid];selected.append(go)
        for cp in go.read_typetree()['m_Component']:
            o=resolve(go,cp['component'])
            if o.type.name in ['Transform','ParticleSystem','ParticleSystemRenderer']:selected.append(o)
            if o.type.name=='Transform':
                for p in o.read_typetree()['m_Children']:visit(trs[p['m_PathID']].read_typetree()['m_GameObject']['m_PathID'])
    visit(rootid)
    for o in selected:allocate(o)
    def remap(o,v):
        if isinstance(v,dict):
            if set(v)=={'m_FileID','m_PathID'}:
                target=resolve(o,v)
                if not target:return c.ptr()
                k=(target.assets_file.name,target.path_id)
                return c.ptr(mapping[k].path_id) if k in mapping else convert(target)
            return {k:remap(o,x) for k,x in v.items()}
        if isinstance(v,list):return [remap(o,x) for x in v]
        if isinstance(v,tuple):return tuple(remap(o,x) for x in v)
        return v
    for o in selected:
        t=remap(o,o.read_typetree());n=mapping[(o.assets_file.name,o.path_id)]
        if o.type.name=='GameObject':
            t['m_Component']=[x for x in t['m_Component'] if x['component']['m_PathID']];t['m_Layer']=9
            # GC's prefab pool registers Transform.name, then spawns using
            # DB_sfx.file_name. These must match, not the source Legends name.
            if o.path_id==rootid:t['m_Name']='fx_'+namespace+'_'+label
        if o.type.name=='ParticleSystem':
            t['playOnAwake']=True;t['looping']=False;t['stopAction']=2
            if namespace=='goku_black' and label.startswith('transform_'):
                t['simulationSpeed']/=3.0;t['useUnscaledTime']=False
        if o.type.name=='Transform' and o.read_typetree()['m_GameObject']['m_PathID']==rootid:
            t['m_Father']=c.ptr();t['m_LocalPosition']=dict(x=0.0,y=0.0,z=0.0)
        n.save_typetree(merge(templates[o.type.name].read_typetree(),t))
    logical=('phoenix_dbl_vfx_' if namespace=='goku' else 'phoenix_dbl_'+namespace+'_vfx_')+label;c.report[:]=[r for r in c.report if r['logical']!=logical]
    path='assets/sevensins/patchresources/effect/dragonball/'+namespace+'/fx_'+namespace+'_'+label+'.prefab'
    c.emit(donor,logical,[(path,mapping[(src.assets[0].name,rootid)].path_id)],[])
    print(label,len(selected),'native components',flush=True)

if __name__=='__main__':
    for args in EFFECTS:build(*args)
    (c.OUT/'br-m.bin').write_bytes(c.write(*c.manifest));(c.OUT/'assets.json').write_text(json.dumps(c.report,indent=2))
    (c.ROOT/'Research/DBLegends/vfx-registration.json').write_text(json.dumps([dict(id=id,path='DragonBall/goku',filename='fx_goku_'+label) for label,name,id in EFFECTS],indent=2))
