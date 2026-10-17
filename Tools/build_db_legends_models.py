"""Convert modular Legends Goku meshes to native GC prefabs and schemas.

The source is Unity 6; every runtime component is serialized with a GC donor
type tree. Source scripts and shaders never enter the playable prefab.
"""
from pathlib import Path
from copy import deepcopy
import json, zlib
import numpy as np
from PIL import Image

helper = Path(__file__).with_name('build_kaneki_assets.py')
exec(compile(helper.read_text(encoding='utf-8').split("donor='253")[0], str(helper), 'exec'))
manifest = read((OUT/'br-m.bin').read_bytes())
bundles, aliases, dirs = manifest
report = json.loads((OUT/'assets.json').read_text())
SOURCE = ROOT/'Research/DBLegends/PhoneFiles/streamingassetbundles'
INDEX = json.loads((ROOT/'Research/DBLegends/bundle-index.json').read_text())
CAB_CACHE=ROOT/'Research/DBLegends/cab-index.json'
if CAB_CACHE.exists():CAB_FILES=json.loads(CAB_CACHE.read_text())
else:
    CAB_FILES={}
    for row in INDEX:
        e=UnityPy.load(str(SOURCE/row['file']))
        for a in e.assets:CAB_FILES[a.name]=row['file']
    CAB_CACHE.write_text(json.dumps(CAB_FILES))
LOADED={}

def source_for(fragment):
    row = next(r for r in INDEX if any(fragment in path for path in r['paths']))
    return UnityPy.load(str(SOURCE/row['file']))

FORMS = [
    dict(name='goku_base', body='body_01', face='face_01', hair='hair_01'),
    dict(name='goku_blue', body='ssgss_body_02', face='ssgss_face_01', hair='ssgss_hair_01'),
    dict(name='goku_ui', body='uis_body_03', face='uis_face_03', hair='uis_hair_01'),
]

def build(form):
    model=form['name']; logical='phoenix_dbl_'+model
    global report
    report=[r for r in report if r['logical']!=logical+'_model']
    selected_roots={};palette_override=None
    if 'order' in form:
        order_env=UnityPy.load(str(SOURCE/form['order']))
        order_obj=next(o for o in order_env.objects if o.type.name=='MonoBehaviour' and 'formModelOrder' in o.read_typetree())
        order=order_obj.read_typetree()['formModelOrder'][form.get('form',0)]
        def order_ref(owner,p):
            if hasattr(p,'path_id'):return p.get_obj()
            a=owner.assets_file
            if p['m_FileID']:
                cab=a.externals[p['m_FileID']-1].path.rsplit('/',1)[-1]
                if cab not in LOADED:LOADED[cab]=UnityPy.load(str(SOURCE/CAB_FILES[cab]))
                a=next(a for a in LOADED[cab].assets if a.name==cab)
            return a.objects[p['m_PathID']]
        source={}
        for part in ['body','face','hair']:
            spec=order_ref(order_obj,order[part+'ModelList'])
            rootobj=order_ref(spec,spec.read_typetree()['models'][0])
            file=CAB_FILES[rootobj.assets_file.name];e=UnityPy.load(str(SOURCE/file));source[part]=e
            selected_roots[id(e)]=e.assets[0].objects[rootobj.path_id]
        color=order_ref(order_obj,order['colorTableList'])
        palette_override=order_ref(color,color.read_typetree()['colorTables'][0]).read()
        assert palette_override.m_Width==256 and palette_override.m_Height==1
    else:source={part:source_for('/goku/common/model/'+form[part]+'/') for part in ['body','face','hair']}
    env=gc('253AD473855C32C7DC4EC70CA51D9A7D');asset=env.assets[0]
    templates={typ:next(o for o in env.objects if o.type.name==typ) for typ in ['GameObject','Transform','Animator','SkinnedMeshRenderer','Mesh','Avatar','Material','Texture2D','MonoBehaviour','MonoScript']}
    bundle=next(o for o in env.objects if o.type.name=='AssetBundle');asset.objects={bundle.path_id:bundle}
    nextid=8100000000000000000
    def native(typ,tree):
        nonlocal nextid
        nextid+=1;obj=clone(templates[typ],asset,nextid);base=templates[typ].read_typetree()
        # Copy matching fields recursively; discard Unity 6-only properties.
        def merge(dst,src):
            if isinstance(dst,dict) and isinstance(src,dict):return {k:merge(v,src[k]) if k in src else v for k,v in dst.items()}
            return deepcopy(src)
        obj.save_typetree(merge(base,tree));return obj
    def resolve(owner,p):
        if not p['m_PathID']:return None
        a=owner.assets_file
        if p['m_FileID']:
            cab=a.externals[p['m_FileID']-1].path.rsplit('/',1)[-1]
            if cab not in LOADED:LOADED[cab]=UnityPy.load(str(SOURCE/CAB_FILES[cab]))
            a=next(a for a in LOADED[cab].assets if a.name==cab)
        return a.objects[p['m_PathID']]
    def part_root(e):
        if id(e) in selected_roots:return selected_roots[id(e)]
        data=next(o.read_typetree() for o in e.objects if o.type.name=='MonoBehaviour' and 'models' in o.read_typetree())
        return e.assets[0].objects[data['models'][0]['m_PathID']]
    mappings={};byname={};parents={};names={};poses={};renderers=[]
    def add_hierarchy(e,root,parent=0,reuse=False):
        gos={o.path_id:o for o in e.objects if o.type.name=='GameObject'}
        trs={o.path_id:o for o in e.objects if o.type.name=='Transform'}
        roottr=next(t for t in trs.values() if t.read_typetree()['m_GameObject']['m_PathID']==root.path_id)
        local={}
        def visit(tr,parentid):
            t=tr.read_typetree();go=gos[t['m_GameObject']['m_PathID']];g=go.read_typetree();name=g['m_Name']
            # Attach face/hair to the already animated body hierarchy. Reuse
            # matching skeleton nodes, retaining their body rest transforms.
            if reuse and name in byname and not ('Shape' in name or 'Face' in name or 'Hair' in name):
                newtr=byname[name];local[tr.path_id]=newtr
            else:
                ng=native('GameObject',dict(m_Name=name,m_Component=[],m_Layer=9,m_IsActive=True))
                # Modular head pieces are authored at the head's world rest
                # height. Legends resets that placement when attaching them
                # to attachNode 15; retaining it here adds the neck height twice.
                if reuse and tr.path_id==roottr.path_id:
                    t=deepcopy(t);t['m_LocalPosition']=dict(x=0.0,y=0.0,z=0.0)
                    t['m_LocalRotation']=dict(x=0.0,y=0.0,z=0.0,w=1.0)
                nt=native('Transform',dict(t,m_GameObject=ptr(ng.path_id),m_Father=ptr(parentid),m_Children=[]))
                newtr=nt.path_id;local[tr.path_id]=newtr
                ngt=ng.read_typetree();ngt['m_Component']=[dict(component=ptr(newtr))];ng.save_typetree(ngt)
                parents[newtr]=parentid;names[newtr]=name;poses[newtr]=t
                byname.setdefault(name,newtr)
                for c in g['m_Component']:
                    obj=resolve(go,c['component'])
                    if obj and obj.type.name in ['SkinnedMeshRenderer','MeshRenderer'] and not any('ghost' in resolve(obj,p).read_typetree()['m_Name'].lower() for p in obj.read_typetree()['m_Materials']):renderers.append((obj,ng.path_id,local,e))
            for p in t['m_Children']:visit(trs[p['m_PathID']],newtr)
            return newtr
        nr=visit(roottr,parent);mappings.update({(e.assets[0].name,k):v for k,v in local.items()});return nr
    root=add_hierarchy(source['body'],part_root(source['body']))
    # Blue Vegeta's neck vertices follow b_C_Head. Its g_C_Head locator has
    # independent animated translation/rotation and no weighted body vertices;
    # parenting here tears the face away from the neck throughout the idle.
    head=byname['b_C_Head'] if model in ['vegeta_blue','gogeta_blue','goku_black','goku_black_rose'] else byname.get('g_C_Head',byname['b_C_Head'])
    add_hierarchy(source['face'],part_root(source['face']),head,True)
    add_hierarchy(source['hair'],part_root(source['hair']),head,True)
    for i,parent in parents.items():
        if parent:
            t=asset.objects[parent].read_typetree();t['m_Children'].append(ptr(i));asset.objects[parent].save_typetree(t)
    rootgo=asset.objects[root].read_typetree()['m_GameObject']['m_PathID']
    # GC places the prefab root on the ground. Legends authors the skeleton
    # around the pelvis, with the soles about 0.85 m below its root. Keep that
    # correction on an unanimated visual parent so clips cannot erase it.
    g=asset.objects[rootgo].read_typetree();g['m_Name']='VisualRoot';asset.objects[rootgo].save_typetree(g)
    visual=root
    wrapper=native('GameObject',dict(m_Name='hero_'+model+'_body_0001',m_Component=[],m_Layer=9,m_IsActive=True))
    wt=native('Transform',dict(m_GameObject=ptr(wrapper.path_id),m_Father=ptr(),m_Children=[ptr(visual)],m_LocalPosition=dict(x=0.0,y=0.0,z=0.0),m_LocalRotation=dict(x=0.0,y=0.0,z=0.0,w=1.0),m_LocalScale=dict(x=1.0,y=1.0,z=1.0)))
    g=wrapper.read_typetree();g['m_Component']=[dict(component=ptr(wt.path_id))];wrapper.save_typetree(g)
    t=asset.objects[visual].read_typetree();t['m_Father']=ptr(wt.path_id);t['m_LocalPosition']['y']+=0.90;asset.objects[visual].save_typetree(t)
    parents[visual]=wt.path_id;names[visual]='VisualRoot';poses[visual]=t
    root=wt.path_id;rootgo=wrapper.path_id;parents[root]=0;names[root]='hero_'+model+'_body_0001';poses[root]=wt.read_typetree()
    if model in ['gogeta_blue','goku_black','goku_black_rose']:
        # GC already moves the fighter between battle waypoints. Preserve the
        # source clip's root track on an unweighted sibling, not the skeleton:
        # its flight displacement otherwise carries into the following attack.
        dg=native('GameObject',dict(m_Name='LegendsRootMotion',m_Component=[],m_Layer=9,m_IsActive=True))
        dt=native('Transform',dict(m_GameObject=ptr(dg.path_id),m_Father=ptr(root),m_Children=[],m_LocalPosition=dict(x=0.0,y=0.0,z=0.0),m_LocalRotation=dict(x=0.0,y=0.0,z=0.0,w=1.0),m_LocalScale=dict(x=1.0,y=1.0,z=1.0)))
        g=dg.read_typetree();g['m_Component']=[dict(component=ptr(dt.path_id))];dg.save_typetree(g)
        t=wt.read_typetree();t['m_Children'].append(ptr(dt.path_id));wt.save_typetree(t)
        parents[dt.path_id]=root;names[dt.path_id]='LegendsRootMotion';poses[dt.path_id]=dt.read_typetree()
    # Legends stores palette indices in the texture alpha channel. Bake the
    # original 1P color table into native RGBA albedo, rather than importing
    # its incompatible render-texture palette shader.
    texs=[o.read() for e in [source['body'],*LOADED.values()] for o in e.objects if o.type.name=='Texture2D']
    pal=palette_override or next(t for t in texs if t.m_Width==256 and t.m_Height==1 and ('1P' in t.m_Name))
    palette=np.asarray(pal.image.convert('RGB')).reshape(256,3)
    materials={};meshes={}
    def material(old):
        key=(old.assets_file.name,old.path_id)
        if key in materials:return materials[key]
        t=old.read_typetree();texenv=dict(t['m_SavedProperties']['m_TexEnvs']);image=resolve(old,texenv['_MainTex']['m_Texture']).read().image.convert('RGBA')
        pixels=np.array(image);color=palette[pixels[:,:,3]].copy()
        if '_MaskTex' in texenv:
            mask=resolve(old,texenv['_MaskTex']['m_Texture'])
            if mask:
                shade=np.array(mask.read().image.resize(image.size).convert('RGBA'))[:,:,0]/255
                color=np.clip(color.astype(float)*(0.65+0.35*shade[:,:,None]),0,255).astype('uint8')
        rgba=np.concatenate([color,np.full((*color.shape[:2],1),255,dtype='uint8')],axis=2)
        texture=native('Texture2D',{});data=texture.read();data.m_Name=model+'_'+t['m_Name'];data.set_image(Image.fromarray(rgba),target_format=4);data.save()
        mat=templates['Material'].read_typetree();mat['m_Name']=model+'_'+t['m_Name']
        for name,entry in mat['m_SavedProperties']['m_TexEnvs']:
            if name=='_MainTex':entry['m_Texture']=ptr(texture.path_id)
        obj=native('Material',mat);materials[key]=obj.path_id;return obj.path_id
    for old,goid,local,e in renderers:
        t=old.read_typetree()
        static=old.type.name=='MeshRenderer'
        mf=next((o for o in e.objects if o.type.name=='MeshFilter' and o.read_typetree()['m_GameObject']==t['m_GameObject']),None) if static else None
        mesh=resolve(mf,mf.read_typetree()['m_Mesh']) if static else resolve(old,t['m_Mesh']);key=(mesh.assets_file.name,mesh.path_id)
        if key not in meshes:
            mt=mesh.read_typetree()
            stream=mt['m_StreamData']
            if stream['size']:
                from UnityPy.helpers.ResourceReader import get_resource_data
                mt['m_VertexData']['m_DataSize']=get_resource_data(stream['path'],mesh.assets_file,stream['offset'],stream['size'])
                mt['m_StreamData']=dict(offset=0,size=0,path='')
            meshes[key]=native('Mesh',mt).path_id
        def mapped(p):
            if not p['m_PathID']:return ptr()
            return ptr(mappings[(old.assets_file.name,p['m_PathID'])])
        rt=dict(t,m_GameObject=ptr(goid),m_Materials=[ptr(material(resolve(old,p))) for p in t['m_Materials']],m_Enabled=True,m_UpdateWhenOffscreen=True)
        if static:
            nextid+=1;ro=clone(old,asset,nextid);ro.save_typetree(rt)
            ft=mf.read_typetree();ft.update(m_GameObject=ptr(goid),m_Mesh=ptr(meshes[key]));nextid+=1;fo=clone(mf,asset,nextid);fo.save_typetree(ft)
            g=asset.objects[goid].read_typetree();g['m_Component'].append(dict(component=ptr(fo.path_id)));asset.objects[goid].save_typetree(g)
        else:
            rt.update(m_Mesh=ptr(meshes[key]),m_Bones=[mapped(p) for p in t['m_Bones']],m_RootBone=mapped(t['m_RootBone']))
            ro=native('SkinnedMeshRenderer',rt)
        g=asset.objects[goid].read_typetree();g['m_Component'].append(dict(component=ptr(ro.path_id)));asset.objects[goid].save_typetree(g)
    # Build a complete generic avatar in GC's native schema.
    def path(i):
        if i==root:return ''
        p=path(parents[i]);return (p+'/' if p else '')+names[i]
    nodes=[]
    def order(i):
        nodes.append(i)
        for p in asset.objects[i].read_typetree()['m_Children']:order(p['m_PathID'])
    order(root);indices={i:j for j,i in enumerate(nodes)};actual={path(i):i for i in nodes}
    skeleton=dict(m_Node=[dict(m_ParentId=indices.get(parents[i],-1),m_AxesId=-1) for i in nodes],m_ID=[zlib.crc32(path(i).encode()) for i in nodes],m_AxesArray=[])
    pose=[dict(t=poses[i]['m_LocalPosition'],q=poses[i]['m_LocalRotation'],s=poses[i]['m_LocalScale']) for i in nodes]
    av=templates['Avatar'].read_typetree();av['m_Name']=model+'Avatar';av['m_TOS']=sorted((zlib.crc32(p.encode()),p) for p in actual)
    data=av['m_Avatar'];data['m_AvatarSkeleton']={'data':skeleton};data['m_AvatarSkeletonPose']={'data':dict(m_X=pose)};data['m_DefaultPose']={'data':dict(m_X=deepcopy(pose))};data['m_SkeletonNameIDArray']=[0 if i==root else zlib.crc32(names[i].encode()) for i in nodes]
    motion=byname['b_C_Base'];chain=[];i=motion
    while i in indices:chain.insert(0,i);i=parents[i]
    data['m_RootMotionBoneIndex']=indices[motion];data['m_RootMotionSkeleton']={'data':dict(m_Node=[dict(m_ParentId=j-1,m_AxesId=-1) for j in range(len(chain))],m_ID=[zlib.crc32(path(i).encode()) for i in chain],m_AxesArray=[])};data['m_RootMotionSkeletonIndexArray']=[indices[i] for i in chain]
    from UnityPy.helpers.TypeTreeHelper import write_typetree
    from UnityPy.streams import EndianBinaryWriter
    writer=EndianBinaryWriter(endian=templates['Avatar'].reader.endian);node=next(n for n in templates['Avatar']._get_typetree_node().m_Children if n.m_Name=='m_Avatar');write_typetree(data,node,writer,asset);av['m_AvatarSize']=len(writer.bytes)
    avatar=native('Avatar',av);anim=native('Animator',dict(m_GameObject=ptr(rootgo),m_Avatar=ptr(avatar.path_id),m_Controller=ptr(),m_ApplyRootMotion=False))
    script=clone(templates['MonoScript'],asset);mb=templates['MonoBehaviour'].read_typetree();mb['m_GameObject']=ptr(rootgo)
    bone_names={'m_bip':'b_C_Base','m_bip_head':'b_C_Head','m_bip_neck':'b_C_Neck1','m_bip_spine':'b_C_Spine1','m_bip_spine1':'b_C_Spine2','m_neck_dmy':'b_C_Neck1','m_weapon_left':'b_L_Hand','m_weapon_right':'b_R_Hand','m_move001':'b_C_Base','m_spawn_head':'b_C_Head','m_spawn_body':'b_C_Spine2','m_spawn_center':'b_C_Pelvis','m_spawn_follow':'b_C_Base','m_spawn_lefthand':'b_L_Hand','m_spawn_righthand':'b_R_Hand'}
    for key in mb:
        if key.startswith('m_') and key not in ['m_GameObject','m_Enabled','m_Script','m_Name']:mb[key]=ptr(byname.get(bone_names.get(key,''),0))
    mb['m_Script']=ptr(script.path_id);bone=native('MonoBehaviour',mb)
    g=asset.objects[rootgo].read_typetree();g['m_Component'] += [dict(component=ptr(anim.path_id)),dict(component=ptr(bone.path_id))];asset.objects[rootgo].save_typetree(g)
    # Empty cosmetic head wrapper: the face and hair remain on the body rig.
    hg=native('GameObject',dict(m_Name='hero_'+model+'_head_0001',m_Component=[],m_Layer=9));ht=native('Transform',dict(m_GameObject=ptr(hg.path_id),m_Father=ptr(),m_Children=[]));t=hg.read_typetree();t['m_Component']=[dict(component=ptr(ht.path_id))];hg.save_typetree(t)
    deps=next(r['deps'] for r in bundles.values() if r['name']=='253AD473855C32C7DC4EC70CA51D9A7D')
    emit(env,logical+'_model',[(f'assets/sevensins/patchresources/character/hero_{model}/prefabs/{n}.prefab',i) for n,i in [('hero_'+model+'_body_0001',rootgo),('hero_'+model+'_head_0001',hg.path_id)]],deps)
    (ROOT/'Research/DBLegends'/f'{model}-rig.json').write_text(json.dumps(dict(paths=actual,bones=byname,root=root,rootgo=rootgo,renderers=len(renderers)),indent=2))
    print(model,'native rig:',len(nodes),'bones;',len(renderers),'mesh renderers',flush=True)

if __name__=='__main__':
    for form in FORMS:build(form)
    (OUT/'br-m.bin').write_bytes(write(*manifest));(OUT/'assets.json').write_text(json.dumps(report,indent=2))
