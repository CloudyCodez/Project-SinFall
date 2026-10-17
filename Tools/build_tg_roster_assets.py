"""Port the requested BTC roster through the verified Kaneki native pipeline."""
from pathlib import Path
from copy import deepcopy
import json,sys
import zlib

# Share the exact tested serialization, live-edit and manifest helpers.
helper=Path(__file__).with_name('build_kaneki_assets.py')
exec(compile(helper.read_text().split("donor='253")[0],str(helper),'exec'))
SRC=ROOT/'Research/TokyoGhoul/PortAssets'
manifest=read((OUT/'br-m.bin').read_bytes())
bundles,aliases,dirs=manifest
report=json.loads((OUT/'assets.json').read_text())
units=json.loads((ROOT/'Research/TokyoGhoul/roster-port-inventory.json').read_text())
donor='253AD473855C32C7DC4EC70CA51D9A7D'

def port(unit):
    global report
    sid=unit['source'];modelname=unit['model'];prefix='hero_'+modelname
    logical='phoenix_tg_'+sid
    if any(r['logical']==logical+'_model' for r in report) and '--force' not in sys.argv:
        print(sid,'already built',flush=True);return
    report=[r for r in report if not r['logical'].startswith(logical+'_')]
    sources={n:load(SRC/n,True) for n in unit['files'] if not n.endswith(('_head','_full'))}
    cab={a.name:a for env in sources.values() for a in env.assets}
    def resolve(owner,p):
        if not p['m_PathID']:return None
        a=owner.assets_file
        if p['m_FileID']:
            name=a.externals[p['m_FileID']-1].path.rsplit('/',1)[-1]
            assert name in cab,(sid,name,'dependency missing')
            a=cab[name]
        return a.objects[p['m_PathID']]
    target=gc(donor);asset=target.assets[0]
    nativebone=next(o for o in target.objects if o.type.name=='MonoBehaviour')
    nativescript=next(o for o in target.objects if o.type.name=='MonoScript')
    nativemat=next(o for o in target.objects if o.type.name=='Material')
    nativetex=next(o for o in target.objects if o.type.name=='Texture2D')
    bundle=next(o for o in target.objects if o.type.name=='AssetBundle')
    mbtree=nativebone.read_typetree();mattree=nativemat.read_typetree()
    asset.objects={bundle.path_id:bundle}
    model=sources[sid]
    transforms={o.path_id:o.read_typetree() for o in model.objects if o.type.name=='Transform'}
    names={o.path_id:o.read().m_Name for o in model.objects if o.type.name=='GameObject'}
    root=next(i for i,t in transforms.items() if t['m_Father']['m_PathID']==0 and names[t['m_GameObject']['m_PathID']]==sid)
    keep=set()
    def descend(i):
        keep.add(i);t=transforms[i];keep.add(t['m_GameObject']['m_PathID'])
        for p in t['m_Children']:descend(p['m_PathID'])
    descend(root)
    for o in model.objects:
        if o.type.name in {'GameObject','Transform','Animator','SkinnedMeshRenderer'}:
            go=o.read_typetree().get('m_GameObject',{}).get('m_PathID')
            if o.path_id in keep or go in keep:clone(o,asset);keep.add(o.path_id)
    rootgo=transforms[root]['m_GameObject']['m_PathID']
    byname={names[t['m_GameObject']['m_PathID']]:i for i,t in transforms.items() if i in keep}
    for o in list(asset.objects.values()):
        t=o.read_typetree()
        if o.type.name=='GameObject':
            t['m_Component']=[c for c in t['m_Component'] if c['component']['m_PathID'] in asset.objects]
            t['m_Layer']=9
            if o.path_id==rootgo:t['m_Name']=prefix+'_body_0001'
            o.save_typetree(t)
        elif o.type.name=='Transform':
            t['m_Children']=[p for p in t['m_Children'] if p['m_PathID'] in asset.objects];o.save_typetree(t)
    nextid=8000000000000000000;copied={}
    def copy_unique(obj):
        nonlocal nextid
        k=(obj.assets_file.name,obj.path_id)
        if k not in copied:
            nextid+=1;clone(obj,asset,nextid);copied[k]=nextid
        return copied[k]
    textureids={}
    particle_shader=next(o for o in gc('848ECA5317DD03D78753BB38EEA703D5').objects if o.type.name=='Shader' and o.read_typetree().get('m_ParsedForm',{}).get('m_Name')=='Mobile/Particles/Alpha Blended')
    particle_shader_id=copy_unique(particle_shader)
    additive=particle_shader.read_typetree()
    additive['m_ParsedForm']['m_Name']='Phoenix/Kagune Additive'
    for subshader in additive['m_ParsedForm']['m_SubShaders']:
        for shaderpass in subshader['m_Passes']:
            state=shaderpass['m_State'];state['rtBlend0']['destBlend']['val']=1.0;state['rtBlend0']['destBlendAlpha']['val']=1.0
    asset.objects[particle_shader_id].save_typetree(additive)
    def finish_material(tree,old,textureid):
        floats=dict(old['m_SavedProperties']['m_Floats'])
        # Kagune sheets use an unlit, double-sided transparent shader. An
        # opaque lit body shader turns their rectangular backing into a fan.
        if floats.get('_DstBlend',0)!=0 or floats.get('_ZWrite',1)==0:
            tree.update(m_Shader=ptr(particle_shader_id),m_CustomRenderQueue=3000,m_ValidKeywords=[],m_InvalidKeywords=[],stringTagMap=[('RenderType','Transparent')])
            tree['m_SavedProperties']['m_TexEnvs']=[('_MainTex',dict(m_Texture=ptr(textureid),m_Scale=dict(x=1,y=1),m_Offset=dict(x=0,y=0)))]
            tree['m_SavedProperties']['m_Colors']=[]
            tree['m_SavedProperties']['m_Floats']=[('_InvFade',1.0),('_ZWrite',0.0),('_Cull',0.0)]
        return tree
    def material(obj):
        nonlocal nextid
        k=(obj.assets_file.name,obj.path_id)
        if k in copied:return copied[k]
        old=obj.read_typetree();oldtex=dict(old['m_SavedProperties']['m_TexEnvs'])
        p=next((oldtex[n] for n in ['_MainTex','_BaseMap','_BaseTex'] if n in oldtex and oldtex[n]['m_Texture']['m_PathID']),None)
        if p is None:
            # Source kagune glow materials are solid emissive colors, with no
            # albedo texture. Bake that color into a tiny native albedo map.
            from PIL import Image
            colors=dict(old['m_SavedProperties']['m_Colors']);color=colors.get('_MainColor',colors.get('_BaseColor',dict(r=1,g=1,b=1,a=1)))
            nextid+=1;texture=clone(nativetex,asset,nextid);data=texture.read();data.m_Name=modelname+'_solid'
            data.set_image(Image.new('RGBA',(4,4),tuple(round(max(0,min(1,color[k]))*255) for k in ['r','g','b','a'])));data.save()
            tree=deepcopy(mattree);tree['m_Name']=modelname+'_'+old['m_Name']
            for name,entry in tree['m_SavedProperties']['m_TexEnvs']:
                if name=='_MainTex':entry['m_Texture']=ptr(nextid)
            tree=finish_material(tree,old,nextid)
            nextid+=1;new=clone(nativemat,asset,nextid);new.save_typetree(tree);copied[k]=nextid;return nextid
        assert p,(sid,old['m_Name'],list(oldtex))
        tex=resolve(obj,p['m_Texture']);assert tex is not None,(sid,old['m_Name'])
        tk=(tex.assets_file.name,tex.path_id)
        if tk not in textureids:
            nextid+=1;texture=clone(nativetex,asset,nextid);data=texture.read()
            data.m_Name=modelname+'_'+tex.read().m_Name
            image=tex.read().image
            floats=dict(old['m_SavedProperties']['m_Floats'])
            if floats.get('_DstBlend',0)!=0 or floats.get('_ZWrite',1)==0:
                # Preserve the source effect's color multiplier when moving
                # from its URP shader to GC's native particle GPU program.
                import numpy as np
                from PIL import Image
                color=dict(old['m_SavedProperties']['m_Colors']).get('_MainColor',dict(r=1,g=1,b=1,a=1))
                pixels=np.asarray(image.convert('RGBA')).astype('float32').copy()
                pixels[:,:,:3]*=np.array([min(4,color[k]) for k in ['r','g','b']])
                image=Image.fromarray(np.clip(pixels,0,255).astype('uint8'))
            data.set_image(image);data.save();textureids[tk]=nextid
        tree=deepcopy(mattree);tree['m_Name']=modelname+'_'+old['m_Name']
        for name,entry in tree['m_SavedProperties']['m_TexEnvs']:
            if name=='_MainTex':entry['m_Texture']=ptr(textureids[tk])
        tree=finish_material(tree,old,textureids[tk])
        nextid+=1;new=clone(nativemat,asset,nextid);new.save_typetree(tree);copied[k]=nextid
        return nextid
    for old in model.objects:
        if old.type.name=='SkinnedMeshRenderer' and old.path_id in asset.objects:
            t=old.read_typetree();t['m_Mesh']=ptr(copy_unique(resolve(old,t['m_Mesh'])))
            t['m_Materials']=[ptr(material(resolve(old,p))) for p in t['m_Materials']]
            asset.objects[old.path_id].save_typetree(t)
    ani=sources['character_'+sid+'_ani']
    root_animator=next((o for o in model.objects if o.type.name=='Animator' and o.read_typetree()['m_GameObject']['m_PathID']==rootgo),None)
    avatar=resolve(root_animator,root_animator.read_typetree()['m_Avatar']) if root_animator else None
    def hierarchy_path(i):
        if i==root:return ''
        parent=hierarchy_path(transforms[i]['m_Father']['m_PathID'])
        return (parent+'/' if parent else '')+names[transforms[i]['m_GameObject']['m_PathID']]
    actual_paths={hierarchy_path(i):i for i in transforms if i in keep}
    avatar_candidates=[o for source in sources.values() for o in source.objects if o.type.name=='Avatar']
    avatar=max(avatar_candidates,key=lambda o:sum(path in actual_paths for _,path in o.read_typetree()['m_TOS']))
    avatarid=copy_unique(avatar)
    # Generic avatars must describe this prefab's complete hierarchy. Several
    # BTC skins reuse 1001's controller but have no compatible bundled avatar.
    av=avatar.read_typetree();nodes=[]
    def ordered(i):
        nodes.append(i)
        for p in transforms[i]['m_Children']:
            if p['m_PathID'] in keep:ordered(p['m_PathID'])
    ordered(root);indices={i:j for j,i in enumerate(nodes)}
    hashes=[zlib.crc32(hierarchy_path(i).encode()) for i in nodes]
    skeleton=dict(m_Node=[dict(m_ParentId=indices.get(transforms[i]['m_Father']['m_PathID'],-1),m_AxesId=-1) for i in nodes],m_ID=hashes,m_AxesArray=[])
    poses=[dict(t=transforms[i]['m_LocalPosition'],q=transforms[i]['m_LocalRotation'],s=transforms[i]['m_LocalScale']) for i in nodes]
    av['m_Name']=modelname+'Avatar';av['m_TOS']=sorted((h,hierarchy_path(i)) for h,i in zip(hashes,nodes))
    data=av['m_Avatar'];data['m_AvatarSkeleton']={'data':skeleton};data['m_AvatarSkeletonPose']={'data':dict(m_X=poses)};data['m_DefaultPose']={'data':dict(m_X=deepcopy(poses))}
    data['m_SkeletonNameIDArray']=[0 if i==root else zlib.crc32(names[transforms[i]['m_GameObject']['m_PathID']].encode()) for i in nodes]
    motion=byname['Bip001'];chain=[];i=motion
    while i in indices:chain.insert(0,i);i=transforms[i]['m_Father']['m_PathID']
    data['m_RootMotionBoneIndex']=indices[motion]
    data['m_RootMotionSkeleton']={'data':dict(m_Node=[dict(m_ParentId=j-1,m_AxesId=-1) for j in range(len(chain))],m_ID=[zlib.crc32(hierarchy_path(i).encode()) for i in chain],m_AxesArray=[])}
    data['m_RootMotionSkeletonIndexArray']=[indices[i] for i in chain]
    from UnityPy.helpers.TypeTreeHelper import write_typetree
    from UnityPy.streams import EndianBinaryWriter
    writer=EndianBinaryWriter(endian=avatar.reader.endian)
    node=next(n for n in avatar._get_typetree_node().m_Children if n.m_Name=='m_Avatar')
    write_typetree(data,node,writer,asset);av['m_AvatarSize']=len(writer.bytes)
    asset.objects[avatarid].save_typetree(av)
    animators=[o for o in asset.objects.values() if o.type.name=='Animator']
    driver=next((o for o in animators if o.read_typetree()['m_GameObject']['m_PathID']==rootgo),animators[0])
    removed={o.path_id for o in animators if o.path_id!=driver.path_id}
    for i in removed:del asset.objects[i]
    for o in list(asset.objects.values()):
        if o.type.name=='GameObject':
            t=o.read_typetree();t['m_Component']=[p for p in t['m_Component'] if p['component']['m_PathID'] not in removed and p['component']['m_PathID']!=driver.path_id]
            if o.path_id==rootgo:t['m_Component'].append(dict(component=ptr(driver.path_id)))
            o.save_typetree(t)
    t=driver.read_typetree();t.update(m_GameObject=ptr(rootgo),m_Avatar=ptr(avatarid),m_Controller=ptr(),m_ApplyRootMotion=False);driver.save_typetree(t)
    clone(nativescript,asset);clone(nativebone,asset);mbtree['m_GameObject']=ptr(rootgo)
    bone_names={'m_bip':'Bip001','m_bip_neck':'Bip001 Neck','m_bip_spine':'Bip001 Spine','m_bip_spine1':'Bip001 Spine1','m_bip_head':'Bip001 Head','m_neck_dmy':'Bip001 Neck','m_weapon_left':'Bip001 L Hand','m_weapon_right':'Bip001 R Hand','m_move001':'Bip001','m_spawn_head':'Bip001 Head','m_spawn_center':'Bip001 Pelvis','m_spawn_body':'Bip001 Spine1','m_spawn_follow':'Bip001','m_spawn_lefthand':'Bip001 L Hand','m_spawn_righthand':'Bip001 R Hand'}
    for key in list(mbtree):
        if key.startswith('m_') and key not in ['m_GameObject','m_Enabled','m_Script','m_Name']:mbtree[key]=ptr(byname.get(bone_names.get(key,''),0))
    assert mbtree['m_bip']['m_PathID'] and mbtree['m_bip_head']['m_PathID'],sid
    asset.objects[nativebone.path_id].save_typetree(mbtree)
    t=asset.objects[rootgo].read_typetree();t['m_Component'].append(dict(component=ptr(nativebone.path_id)));asset.objects[rootgo].save_typetree(t)
    nextid+=1;headgo=clone(asset.objects[rootgo],asset,nextid);nextid+=1;headtr=clone(asset.objects[root],asset,nextid)
    ht=headtr.read_typetree();ht.update(m_GameObject=ptr(headgo.path_id),m_Father=ptr(),m_Children=[]);headtr.save_typetree(ht)
    ht=headgo.read_typetree();ht.update(m_Name=prefix+'_head_0001',m_Component=[dict(component=ptr(headtr.path_id))]);headgo.save_typetree(ht)
    deps=next(r['deps'] for r in bundles.values() if r['name']==donor)
    emit(target,logical+'_model',[(f'assets/sevensins/patchresources/character/{prefix}/prefabs/{n}.prefab',i) for n,i in [(prefix+'_body_0001',rootgo),(prefix+'_head_0001',headgo.path_id)]],deps)
    clips={o.read().m_Name:o for o in ani.objects if o.type.name=='AnimationClip'}
    for source in unit['animations']:
        if source!='character_'+sid+'_ani':
            for o in sources[source].objects:
                if o.type.name=='AnimationClip':clips.setdefault(o.read().m_Name,o)
    primary_clips={o.read().m_Name:o for o in ani.objects if o.type.name=='AnimationClip'}
    def find(suffixes):
        for pool in [primary_clips,clips]:
            for suffix in suffixes:
                for name,clip in pool.items():
                    normal=lambda s:s.lower().replace('@skil_','@skill_').replace('@skill1','@skill_1').replace('@skill2','@skill_2').replace('@skill3','@skill_3')
                    if normal(name).endswith(normal(suffix)):return clip
        raise ValueError((sid,suffixes,list(clips)))
    idle=find(['@casual_ani','@stand_ani']);stand=find(['@stand_ani','@casual_ani'])
    hit=find(['@hit_ani']);die=find(['@die_ani']);run=find(['@skill_forward_ani','@skill_2_forward_ani','@skill_1_forward_ani','@forward_ani','@run_ani'])
    skills=[find(['@skill_1_ani','@skill_1_all_ani','@skill_1_1_ani']),find(['@skill_2_ani','@skill_2_all_ani','@skill_2_1_ani','@skill_1_2_ani']),find(['@skill_3_ani','@skill_2_all_ani','@skill_2_ani','@skill_1_3_ani','@skill_1_ani'])]
    for index,filename in enumerate(['514C2E68A63B9423FA2FAB1B3515207F','7D61CD01C99CE8E69E27EFC2B2420436','356E0C6D42B92E7C1767DE3B5883B86D','0AE6A657E32FAB7D18EE97D170CB92B7']):
        e=gc(filename)
        for o in e.objects:
            if o.type.name=='AnimationClip':
                old=o.read_typetree();name=old['m_Name']
                if 'cam' in name.lower():continue
                chosen=idle if name=='idle' else stand if name in ['idle_battle','wakeup','appear_drop'] else run if name=='run' else hit if name.startswith('dmg') else die if name=='die' else stand if name=='stun' else skills[0] if name.startswith('skill_01') else skills[1] if name.startswith('skill_02') else skills[2]
                tree=chosen.read_typetree();tree['m_Name']=name;tree['m_Events']=old['m_Events']
                if name in ['idle','idle_battle']:
                    tree['m_MuscleClip']['m_LoopTime']=True
                source_paths={h:path for source in sources.values() for obj in source.objects if obj.type.name=='Avatar' for h,path in obj.read_typetree()['m_TOS']}
                actual_hashes={zlib.crc32(path.encode()) for path in actual_paths}
                # Shared controller clips may include or omit the Root wrapper.
                for binding in tree['m_ClipBindingConstant']['genericBindings']:
                    if binding['typeID']!=4 or binding['path'] in actual_hashes:continue
                    path=source_paths.get(binding['path'],'')
                    candidates=[path.removeprefix('Root/'),'Root/'+path]
                    for candidate in candidates:
                        if candidate in actual_paths:binding['path']=zlib.crc32(candidate.encode());break
                before=old['m_MuscleClip']['m_StopTime'];after=tree['m_MuscleClip']['m_StopTime']
                for event in tree['m_Events']:event['time']=min(after,event['time']*after/before) if before else 0
                o.save_typetree(tree)
        bt=next(o.read() for o in e.objects if o.type.name=='AssetBundle')
        paths=[(p.replace('hero_meliodas_berserker',prefix),v.asset.m_PathID) for p,v in bt.m_Container]
        emit(e,logical+f'_animations_{index}',paths,next(r['deps'] for r in bundles.values() if r['name']==filename))
    for label,source,names_ in [('icon',sid+'_head',[f'icon_hero_{modelname}_0001_s',f'icon_hero_{modelname}_0001_l',f'icon_skin_{modelname}_0001_s',f'icon_skin_{modelname}_0001_l',f'icon_hero_{modelname}_0001_card']),('portrait',sid+'_full',[modelname+'_0001'])]:
        e=load(SRC/source,True);e.assets[0].unity_version='2022.3.27f1';tex=next(o for o in e.objects if o.type.name=='Texture2D')
        paths=[(f'assets/sevensins/patchresources/ui/image/icon/hero/{n}.png',tex.path_id) for n in names_]
        paths += [(f'assets/sevensins/patchresources/ui/image/icon/hero/{modelname.split("_")[0]}/{n}.png',tex.path_id) for n in names_]
        if label=='icon':
            paths.append((f'assets/sevensins/patchresources/ui/image/icon/skillactive/hero/icon_hero_{modelname}_0001_card.png',tex.path_id))
            paths += [(f'assets/sevensins/patchresources/ui/image/icon/costume/{n}.png',tex.path_id) for n in names_]
            paths += [(f'assets/sevensins/patchresources/ui/image/icon/costume/{modelname.split("_")[0]}/{n}.png',tex.path_id) for n in names_]
        emit(e,logical+'_'+label,paths)
    (OUT/'br-m.bin').write_bytes(write(*manifest));(OUT/'assets.json').write_text(json.dumps(report,indent=2))
    print(sid,unit['name'],unit['title'],'built',flush=True)

for unit in units[1:]:port(unit)
print('Roster ready:',len(units),'forms;',len(report),'bundles')
