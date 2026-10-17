"""Adapt the extracted BTC 1065 model to Grand Cross's native bone container.

Uses original meshes, skin weights, avatar and clips. No publisher scripts or
controllers are carried into the GC prefab. Native GC materials/controllers are
retained, with source textures and animation curves substituted.
"""
from pathlib import Path
from copy import copy,deepcopy
import re,json,hashlib,zlib
import UnityPy
from UnityPy.files.ObjectReader import ObjectReader
from UnityPy.streams import EndianBinaryReader
from UnityPy.helpers.UnityVersion import UnityVersion
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
from gc_bundle_manifest import read,write,hash_name,bundle_key

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'Research/TokyoGhoul/Kaneki'
OUT=ROOT/'dist/kaneki-assets';OUT.mkdir(exist_ok=True)
orig=UnityVersion.from_str.__func__
UnityVersion.from_str=classmethod(lambda cls,v:orig(cls,re.match(r'\d+\.\d+\.\d+[abfp]\d+',v).group(0)))
# UnityPy queues edits for saving but ordinarily rereads the original bytes.
# This builder revisits the root after attaching bones and splitting the head;
# make those later reads see the edited component list and render layer.
_set_raw_data=ObjectReader.set_raw_data
def set_live_data(obj,data):
    endian=obj.reader.endian
    _set_raw_data(obj,data)
    obj.reader=EndianBinaryReader(data,endian=endian)
    obj.byte_start=0;obj.byte_size=len(data)
ObjectReader.set_raw_data=set_live_data
def load(path,tg=False):
    b=path.read_bytes();offset=b.find(b'UnityFS',8 if tg else 30)
    assert offset>=0,path
    return UnityPy.load(b[offset:])
def gc(name):return load(ROOT/'Research/PhoneAssets/bm/m'/name)
def ptr(n=0,file=0):return dict(m_FileID=file,m_PathID=n)
def clone(o,target,newid=None):
    n=copy(o);n.data=o.get_raw_data();n.assets_file=target
    if newid is not None:n.path_id=newid
    typ=copy(o.serialized_type);typ.node=o._get_typetree_node();target.types.append(typ)
    n.serialized_type=typ;n.type_id=len(target.types)-1
    target.objects[n.path_id]=n;return n

manifest=read((ROOT/'Research/PhoneAssets/bm/br-m.bin').read_bytes())
bundles,aliases,dirs=manifest
report=[]
def emit(env,logical,paths,deps=()):
    from tg_bundle_identity import unique_files
    unique_files(env,'m/'+logical)
    bundle=next(o for o in env.objects if o.type.name=='AssetBundle')
    bt=bundle.read_typetree();bt['m_Name']='m/'+logical
    # Paths point to explicit top-level objects. Every internal object is a
    # preload dependency, ensuring textures/meshes remain alive with the prefab.
    ids=[i for i in env.assets[0].objects if i!=bundle.path_id]
    bt['m_PreloadTable']=[ptr(i) for i in ids]
    bt['m_Container']=[(p,dict(preloadIndex=0,preloadSize=len(ids),asset=ptr(i))) for p,i in paths]
    bundle.save_typetree(bt)
    # Retain the native bone-container schema. Stripping it made the rebuilt
    # MonoBehaviour impossible to deserialize independently of the player.
    a=env.assets[0];types=[]
    for obj in a.objects.values():
        typ=copy(obj.serialized_type)
        rows=obj._get_typetree_node().to_dict_list()
        for idx,row in enumerate(rows):
            row.pop('m_Children',None)
            for key in ('m_TypeFlags','m_MetaFlag','m_RefTypeHash'):
                if row.get(key) is None:row[key]=0
            if row.get('m_Index') is None:row['m_Index']=idx
        typ.node=TypeTreeNode.from_list(rows)
        if typ.type_dependencies is None:typ.type_dependencies=[]
        obj.serialized_type=typ;obj.type_id=len(types);types.append(typ)
    a.types=types;a._enable_type_tree=True
    data=env.file.save(packer='lz4');name=hashlib.md5(('phoenix/'+logical).encode()).hexdigest().upper();(OUT/name).write_bytes(data)
    key=bundle_key(name)
    crc=zlib.crc32(b''.join(f.bytes if hasattr(f,'bytes') else f.save() for f in env.file.files.values()))
    bundles[key]=dict(crc=crc,flags=0,size=3,section=2,name=name,deps=list(deps),extra=[])
    for p,i in paths:
        base='assets/sevensins/patchresources/';assert p.startswith(base)
        directory,filename=p[len(base):].rsplit('/',1)
        dirs.setdefault(base,{}).setdefault(hash_name(directory+'/'),{})[hash_name(filename)]=key
    report.append(dict(logical=logical,file=name,paths=[p for p,i in paths],objects=len(ids),crc=crc))

donor='253AD473855C32C7DC4EC70CA51D9A7D'
target=gc(donor);asset=target.assets[0]
nativebone=next(o for o in target.objects if o.type.name=='MonoBehaviour')
nativescript=next(o for o in target.objects if o.type.name=='MonoScript')
nativemat=next(o for o in target.objects if o.type.name=='Material')
nativetex=next(o for o in target.objects if o.type.name=='Texture2D')
bundle=next(o for o in target.objects if o.type.name=='AssetBundle')
native_layer=next(o.read_typetree()['m_Layer'] for o in target.objects if o.type.name=='GameObject')
mbtree=nativebone.read_typetree();mattree=nativemat.read_typetree()
asset.objects={bundle.path_id:bundle}
model=load(SRC/'1065',True);models=model.assets[0].objects
transforms={o.path_id:o.read_typetree() for o in model.objects if o.type.name=='Transform'}
names={o.path_id:o.read().m_Name for o in model.objects if o.type.name=='GameObject'}
root=next(i for i,t in transforms.items() if t['m_Father']['m_PathID']==0 and names[t['m_GameObject']['m_PathID']]=='1065')
keep=set()
def descend(i):
    keep.add(i);t=transforms[i];keep.add(t['m_GameObject']['m_PathID'])
    for p in t['m_Children']:descend(p['m_PathID'])
descend(root)
allowed={'GameObject','Transform','Animator','SkinnedMeshRenderer'}
for o in model.objects:
    if o.type.name in allowed:
        go=o.read_typetree().get('m_GameObject',{}).get('m_PathID')
        if o.path_id in keep or go in keep:clone(o,asset);keep.add(o.path_id)
rootgo=transforms[root]['m_GameObject']['m_PathID']
byname={names[t['m_GameObject']['m_PathID']]:i for i,t in transforms.items() if i in keep}
for o in list(asset.objects.values()):
    if o.type.name=='GameObject':
        t=o.read_typetree();t['m_Component']=[c for c in t['m_Component'] if c['component']['m_PathID'] in asset.objects]
        t['m_Layer']=native_layer
        if o.path_id==rootgo:t['m_Name']='hero_kaneki_centipede_body_0001'
        o.save_typetree(t)
    elif o.type.name=='Transform':
        t=o.read_typetree();t['m_Children']=[p for p in t['m_Children'] if p['m_PathID'] in asset.objects];o.save_typetree(t)

mesh=load(SRC/'res_mid_1065',True)
for o in mesh.objects:
    if o.type.name=='Mesh':clone(o,asset)
ani=load(SRC/'character_1065_ani',True)
avatar=next(o for o in ani.objects if o.type.name=='Avatar');clone(avatar,asset)
animator=next(o for o in asset.objects.values() if o.type.name=='Animator')
t=animator.read_typetree();t['m_Avatar']=ptr(avatar.path_id);t['m_Controller']=ptr();t['m_ApplyRootMotion']=False;animator.save_typetree(t)
materials=load(SRC/'character_1064_mat',True)
materialmap={o.path_id:o for o in materials.objects if o.type.name=='Material'}
texturemap={o.path_id:o for o in materials.objects if o.type.name=='Texture2D'}
texids={};nextid=8000000000000000000
for mid,o in materialmap.items():
    old=o.read_typetree();tree=deepcopy(mattree);tree['m_Name']='kaneki_'+old['m_Name']
    oldtex=dict(old['m_SavedProperties']['m_TexEnvs'])
    p=oldtex.get('_MainTex',oldtex.get('_BaseMap',oldtex.get('_BaseTex')))
    assert p and p['m_Texture']['m_PathID'] in texturemap,(old['m_Name'],oldtex)
    tid=p['m_Texture']['m_PathID']
    if tid not in texids:
        nextid+=1;texture=clone(nativetex,asset,nextid);data=texture.read();data.m_Name='kaneki_'+texturemap[tid].read().m_Name;data.set_image(texturemap[tid].read().image);data.save();texids[tid]=nextid
    for name,entry in tree['m_SavedProperties']['m_TexEnvs']:
        if name=='_MainTex':entry['m_Texture']=ptr(texids[tid])
    clone(nativemat,asset,mid).save_typetree(tree)
for o in asset.objects.values():
    if o.type.name=='SkinnedMeshRenderer':
        t=o.read_typetree();t['m_Mesh']['m_FileID']=0
        for p in t['m_Materials']:p['m_FileID']=0;assert p['m_PathID'] in asset.objects
        o.save_typetree(t)
# Grand Cross's native bone accessor points directly at the BTC skeleton.
clone(nativescript,asset)
clone(nativebone,asset)
mbtree['m_GameObject']=ptr(rootgo)
bone_names={'m_bip':'Bip001','m_bip_neck':'Bip001 Neck','m_bip_spine':'Bip001 Spine','m_bip_spine1':'Bip001 Spine1','m_bip_head':'Bip001 Head','m_neck_dmy':'Bip001 Neck','m_weapon_left':'Bip001 L Hand','m_weapon_right':'Bip001 R Hand','m_move001':'Bip001','m_spawn_head':'Bip001 Head','m_spawn_center':'Bip001 Pelvis','m_spawn_body':'Bip001 Spine1','m_spawn_follow':'Bip001','m_spawn_lefthand':'Bip001 L Hand','m_spawn_righthand':'Bip001 R Hand'}
for key in list(mbtree):
    if key.startswith('m_') and key not in ['m_GameObject','m_Enabled','m_Script','m_Name']:
        mbtree[key]=ptr(byname.get(bone_names.get(key,''),0))
asset.objects[nativebone.path_id].save_typetree(mbtree)
t=asset.objects[rootgo].read_typetree();t['m_Component'].append(dict(component=ptr(nativebone.path_id)));asset.objects[rootgo].save_typetree(t)
# Self-contained empty head prefab: BTC already includes its skinned face/hair.
nextid+=1;headgo=clone(asset.objects[rootgo],asset,nextid);nextid+=1;headtr=clone(asset.objects[root],asset,nextid)
ht=headtr.read_typetree();ht.update(m_GameObject=ptr(headgo.path_id),m_Father=ptr(),m_Children=[]);headtr.save_typetree(ht)
ht=headgo.read_typetree();ht.update(m_Name='hero_kaneki_centipede_head_0001',m_Component=[dict(component=ptr(headtr.path_id))]);headgo.save_typetree(ht)
deps=next(r['deps'] for r in bundles.values() if r['name']==donor)
emit(target,'phoenix_kaneki_model',[(f'assets/sevensins/patchresources/character/hero_kaneki_centipede/prefabs/{n}.prefab',i) for n,i in [('hero_kaneki_centipede_body_0001',rootgo),('hero_kaneki_centipede_head_0001',headgo.path_id)]],deps)

clips={o.read().m_Name:o for o in ani.objects if o.type.name=='AnimationClip'}
clipmap={'idle':'1065@casual_ani','idle_battle':'1065@stand_ani','run':'1065@skill_forward_ani','die':'1065@die_ani','stun':'1065@dizzy_ani','wakeup':'1065@stand_ani','appear_drop':'1065@stand_ani'}
for index,filename in enumerate(['514C2E68A63B9423FA2FAB1B3515207F','7D61CD01C99CE8E69E27EFC2B2420436','356E0C6D42B92E7C1767DE3B5883B86D','0AE6A657E32FAB7D18EE97D170CB92B7']):
    e=gc(filename)
    for o in e.objects:
        if o.type.name=='AnimationClip':
            old=o.read_typetree();name=old['m_Name']
            if 'cam' in name.lower():continue
            srcname=clipmap.get(name,'1065@hit_ani' if name.startswith('dmg') else '1065@skill_1_ani' if name.startswith('skill_01') else '1065@skill_2_ani' if name.startswith('skill_02') else '1065@skill_3_ani')
            tree=clips[srcname].read_typetree();tree['m_Name']=name;tree['m_Events']=old['m_Events']
            before=old['m_MuscleClip']['m_StopTime'];after=tree['m_MuscleClip']['m_StopTime']
            for event in tree['m_Events']:
                event['time']=min(after,event['time']*after/before) if before else 0
            o.save_typetree(tree)
    bt=next(o.read() for o in e.objects if o.type.name=='AssetBundle')
    paths=[(p.replace('hero_meliodas_berserker','hero_kaneki_centipede'),v.asset.m_PathID) for p,v in bt.m_Container]
    olddeps=next(r['deps'] for r in bundles.values() if r['name']==filename)
    emit(e,f'phoenix_kaneki_animations_{index}',paths,olddeps)

# Portraits use original BTC images, exposed under all native small/large/card
# icon filenames. Their source bundle remains a Texture2D, as NGUI expects.
for label,source,names_ in [('icon','1065_head',['icon_hero_kaneki_centipede_0001_s','icon_hero_kaneki_centipede_0001_l','icon_skin_kaneki_centipede_0001_s','icon_skin_kaneki_centipede_0001_l','icon_hero_kaneki_centipede_0001_card']),('portrait','1065_full',['kaneki_centipede_0001'])]:
    e=load(SRC/source,True);a=e.assets[0];a.unity_version='2022.3.27f1'
    tex=next(o for o in e.objects if o.type.name=='Texture2D')
    paths=[(f'assets/sevensins/patchresources/ui/image/icon/hero/{n}.png',tex.path_id) for n in names_]
    paths += [(f'assets/sevensins/patchresources/ui/image/icon/hero/kaneki/{n}.png',tex.path_id) for n in names_]
    if label=='icon':
        paths.append(('assets/sevensins/patchresources/ui/image/icon/skillactive/hero/icon_hero_kaneki_centipede_0001_card.png',tex.path_id))
        paths += [(f'assets/sevensins/patchresources/ui/image/icon/costume/{n}.png',tex.path_id) for n in names_]
        paths += [(f'assets/sevensins/patchresources/ui/image/icon/costume/kaneki/{n}.png',tex.path_id) for n in names_]
    emit(e,'phoenix_kaneki_'+label,paths)
data=write(*manifest);assert write(*read(data))==data
(OUT/'br-m.bin').write_bytes(data)
(OUT/'assets.json').write_text(json.dumps(report,indent=2))
print('Built Kaneki native prefab, four animation bundles and BTC portraits:',len(report),'bundles')





