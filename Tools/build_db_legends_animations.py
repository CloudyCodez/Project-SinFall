"""Retarget original Legends combat clips to Goku's GC generic rigs."""
from pathlib import Path
from copy import deepcopy
import json,zlib
import build_db_legends_models as ctx
from build_db_legends_models import ROOT,OUT,SOURCE,INDEX,gc,ptr,UnityPy,emit,read,write

COMMON='d3d90e390527b41da661af1f4437c01cd84bc909'
FORMS=[('goku_base','1c009494efb3cd5ae534dd3410b222fff248c6d1','Goku','fd5cf158be1c682164e792d03a5feef5898caec5','GokuUIS_03_ULA_Kamehameha'),('goku_blue','f38e460879464d47f610005870f5dc598d1e0894','GokuSSGSS_02','fd5cf158be1c682164e792d03a5feef5898caec5','GokuUIS_03_ULA_Kamehameha'),('goku_ui','ed53d47ad0583aa7e1abf1b1775938f2883f76b5','GokuUIS_03','fd5cf158be1c682164e792d03a5feef5898caec5','GokuUIS_03_ULA_Kamehameha')]

def build(model,common,prefix,ultimate,ultname,effect_base=198500000):
    envs=[UnityPy.load(str(SOURCE/file)) for file in dict.fromkeys([common,COMMON,ultimate,'ed53d47ad0583aa7e1abf1b1775938f2883f76b5'])]
    clips={}
    for env in envs:
        for o in env.objects:
            if o.type.name=='AnimationClip':
                name=o.read().m_Name
                if name not in clips or len(o.read_typetree()['m_ClipBindingConstant']['genericBindings'])>len(clips[name].read_typetree()['m_ClipBindingConstant']['genericBindings']):clips[name]=o
    rig=json.loads((ROOT/'Research/DBLegends'/f'{model}-rig.json').read_text());actual=rig['paths'];hashes={zlib.crc32(p.encode()):p for p in actual}
    sourcepaths={h:p for e in envs for o in e.objects if o.type.name=='Avatar' for h,p in o.read_typetree()['m_TOS']}
    if model in ['goku_black','goku_black_rose']:
        for path in actual:
            parts=path.split('/')
            for start in range(len(parts)):
                suffix='/'.join(parts[start:]);sourcepaths.setdefault(zlib.crc32(suffix.encode()),suffix)
    def choose(names):
        return next(clips[name] for name in names if name in clips)
    stand=choose([prefix+'_BAS_STAND','Goku_BAS_STAND'])
    run=choose([prefix+'_BAS_BOOST_F_01',prefix+'_BAS_BOOST_F_00',prefix+'_BAS_BUKUU_F','Goku_BAS_BOOST_F_01'])
    punch=choose([prefix+'_ATC_BLOW',prefix+'_COMBO_BLOW'])
    blast=choose([prefix+'_ATC_SHOT_Alternate',prefix+'_ATC_SHOT_BothHand',prefix+'_ATC_SHOT','GokuUIS_03_ATC_SHOT_Alternate'])
    charge=choose(['Common_ATC_SKILL_START',prefix+'_BAS_STAND','Goku_BAS_STAND'])
    hit=choose(['Common_DMG_BLOW_F','Common_DMG_Fastest_Heavy'])
    die=choose(['Common_DMG_FinishKO_G_01','Common_DMG_FinishKO_01'])
    ult=choose([ultname])
    logical='phoenix_dbl_'+model
    ctx.report[:]=[r for r in ctx.report if not r['logical'].startswith(logical+'_animations_')]
    for index,filename in enumerate(['514C2E68A63B9423FA2FAB1B3515207F','7D61CD01C99CE8E69E27EFC2B2420436','356E0C6D42B92E7C1767DE3B5883B86D','0AE6A657E32FAB7D18EE97D170CB92B7','E28BAE6D20B219BB7E0B49407425F577','356E0C6D42B92E7C1767DE3B5883B86D']):
        e=gc(filename)
        extra_paths=[]
        if index==1:
            # GC selects per-card dash/return states for melee approach. The
            # punch donor lacks these; a common run clip is not a substitute.
            travel=gc('356E0C6D42B92E7C1767DE3B5883B86D')
            for number,name in enumerate(['skill_02_dash','skill_02_return']):
                source=next(o for o in travel.objects if o.type.name=='AnimationClip' and o.read().m_Name==name)
                obj=ctx.clone(source,e.assets[0],8400000000000000000+number)
                tree=obj.read_typetree();tree['m_Name']=name.replace('skill_02','skill_01');tree['m_Events']=[];obj.save_typetree(tree)
                extra_paths.append((f'assets/sevensins/patchresources/character/hero_{model}/ani/weapon_glove/skill_01/{tree["m_Name"]}.anim',obj.path_id))
        if index==0:
            # Combat-only donors omit the UI evolution and growth clips.
            ui=gc('5FC491B0AB8C95967A37E3CD2AC301D0')
            existing={o.read().m_Name for o in e.objects if o.type.name=='AnimationClip'}
            ui_paths={v.asset.m_PathID:p for o in ui.objects if o.type.name=='AssetBundle' for p,v in o.read().m_Container}
            for o in ui.objects:
                if o.type.name=='AnimationClip' and o.read().m_Name not in existing:
                    assert o.path_id not in e.assets[0].objects
                    ctx.clone(o,e.assets[0])
                    extra_paths.append((ui_paths[o.path_id].replace('hero_slime_rimuruhuman','hero_'+model).replace('weapon_ssr_type01','weapon_glove'),o.path_id))
        for o in e.objects:
            if o.type.name!='AnimationClip':continue
            old=o.read_typetree();name=old['m_Name']
            if 'cam' in name.lower():continue
            chosen=charge if name=='skill_01_ready' else stand if index==4 or name in ['idle','idle_battle','stun','wakeup','appear_drop','skill_02_end','appear','awaken_lookup','evolution','idle_start','idle_start_02','special_ready','victory'] else run if name=='run' or 'dash' in name or 'return' in name else hit if name.startswith('dmg') else die if name=='die' else punch if name.startswith('skill_01') else blast if name.startswith('skill_02') else ult
            if index==5:chosen=ult if name=='skill_02_atk' else run if 'dash' in name or 'return' in name else stand
            tree=chosen.read_typetree();tree['m_Name']=name;tree['m_Events']=deepcopy(old['m_Events'])
            tree['m_MuscleClip']['m_LoopTime']=name in ['idle','idle_battle','run']
            mapped=0;total=0
            for binding in tree['m_ClipBindingConstant']['genericBindings']:
                if binding['typeID']!=4:continue
                total+=1
                if binding['path'] in hashes:mapped+=1;continue
                path=sourcepaths.get(binding['path'],'')
                matches=[p for p in actual if p and path and (path==p or path.endswith('/'+p) or p.endswith('/'+path))]
                if matches:
                    candidate=max(matches,key=len);binding['path']=zlib.crc32(candidate.encode());mapped+=1
            # Convert Unity 6 serialized fields to the donor clip schema.
            def merge(dst,src):
                if isinstance(dst,dict) and isinstance(src,dict):return {k:merge(v,src[k]) if k in src else v for k,v in dst.items()}
                return deepcopy(src)
            tree=merge(old,tree)
            if model in ['gogeta_blue','goku_black','goku_black_rose']:
                root_hash=zlib.crc32(b'VisualRoot/b_C_Base')
                for binding in tree['m_ClipBindingConstant']['genericBindings']:
                    if binding['typeID']==4 and binding['attribute']==1 and binding['path']==root_hash:
                        binding['path']=zlib.crc32(b'LegendsRootMotion')
            if name=='run' or 'dash' in name or 'return' in name:
                tree['m_MuscleClip']['m_AverageSpeed']=dict(x=0.0,y=0.0,z=6.0)
            before=old['m_MuscleClip']['m_StopTime'];after=tree['m_MuscleClip']['m_StopTime']
            for event in tree['m_Events']:event['time']=min(after,event['time']*after/before) if before else 0
            # Native events resolve our converted effect prefabs through DB_sfx.
            if name=='special_01' or (index==5 and name=='skill_02_atk'):
                def event(t,fn,id,data=''):
                    return dict(time=t,functionName=fn,data=data,objectReferenceParameter=ptr(),floatParameter=0.0,intParameter=id,messageOptions=0)
                tree['m_Events']=[event(after*.32,'OnAnimationEffect',effect_base+1),event(after*.57,'OnAnimationEffect',effect_base+4),event(after*.60,'OnAnimationEffect',effect_base+2),event(after*.68,'OnAnimationEvent',131330,'{"state":"dmg","speed":"0.01","height":"0","distance":"0","finishblend":"False"}')]
            elif name.startswith('skill_02'):
                for event in tree['m_Events']:
                    if event['functionName']=='OnAnimationEffect' and event['intParameter']!=900003:event['intParameter']=198500004
                if name!='skill_02_atk':tree['m_Events']=[event for event in tree['m_Events'] if event['functionName'] not in ['OnAnimationEffect','OnAnimationFacial']]
            elif name.startswith('skill_01'):
                # Remove inherited demon sword trails from the martial arts kit.
                tree['m_Events']=[event for event in tree['m_Events'] if event['functionName']!='OnAnimationEffect' or event['intParameter']==900003]
                if name=='skill_01_ready':
                    tree['m_Events']=[dict(time=after*.15,functionName='OnAnimationEffect',data='',objectReferenceParameter=ptr(),floatParameter=0.0,intParameter=effect_base+1,messageOptions=0)]
                if name=='skill_01_atk':
                    # Native hit events divide the card's total across contacts.
                    tree['m_Events']=[event for event in tree['m_Events'] if event['functionName']!='OnAnimationEvent']
                    for fraction,hit in [(.24,65794),(.40,65794),(.57,65794),(.76,131330)]:
                        tree['m_Events'].append(dict(time=after*fraction,functionName='OnAnimationEvent',data='{"state":"dmg","speed":"0.01","height":"0","distance":"0","finishblend":"False"}',objectReferenceParameter=ptr(),floatParameter=0.0,intParameter=hit,messageOptions=0))
                    tree['m_Events'].sort(key=lambda event:event['time'])
            if index==5:tree['m_Name']=name.replace('skill_02','skill_03')
            from UnityPy.helpers.TypeTreeHelper import write_typetree
            from UnityPy.streams import EndianBinaryWriter
            writer=EndianBinaryWriter(endian=o.reader.endian)
            node=next(n for n in o._get_typetree_node().m_Children if n.m_Name=='m_MuscleClip')
            write_typetree(tree['m_MuscleClip'],node,writer,o.assets_file)
            tree['m_MuscleClipSize']=len(writer.bytes)
            o.save_typetree(tree)
            assert mapped>0,(model,name,'no rig bindings')
            print(model,name,chosen.read().m_Name,'mapped',mapped,'/',total,flush=True)
        bt=next(o.read() for o in e.objects if o.type.name=='AssetBundle')
        paths=[(p.replace('hero_meliodas_berserker','hero_'+model).replace('hero_nor_tir','hero_'+model),v.asset.m_PathID) for p,v in bt.m_Container]+extra_paths
        if index==5:paths=[(p.replace('skill_02','skill_03'),id) for p,id in paths]
        emit(e,logical+f'_animations_{index}',paths,next(r['deps'] for r in ctx.bundles.values() if r['name']==filename))

if __name__=='__main__':
    for form in FORMS:build(*form)
    (OUT/'br-m.bin').write_bytes(write(*ctx.manifest));(OUT/'assets.json').write_text(json.dumps(ctx.report,indent=2))
