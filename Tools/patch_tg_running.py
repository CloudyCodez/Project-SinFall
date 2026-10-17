"""Update only the imported roster's common movement bundles."""
from pathlib import Path
import json
from tg_run_retarget import retarget_run
from UnityPy.helpers.TypeTreeHelper import write_typetree
from UnityPy.streams import EndianBinaryWriter

helper = Path(__file__).with_name('build_kaneki_assets.py')
exec(compile(helper.read_text().split("donor='253")[0], str(helper), 'exec'))
manifest = read((OUT/'br-m.bin').read_bytes()); bundles, aliases, dirs = manifest
report = json.loads((OUT/'assets.json').read_text())
native_model = gc('253AD473855C32C7DC4EC70CA51D9A7D')
native_run = next(o.read_typetree() for o in gc('514C2E68A63B9423FA2FAB1B3515207F').objects if o.type.name == 'AnimationClip' and o.read().m_Name == 'run')
checks = []
for unit in json.loads((ROOT/'Research/TokyoGhoul/roster-port-inventory.json').read_text()):
    prefix = 'phoenix_kaneki' if unit['index'] == 0 else 'phoenix_tg_' + unit['source']
    model_row = next(r for r in report if r['logical'] == prefix + '_model')
    row = next(r for r in report if r['logical'] == prefix + '_animations_0')
    model = UnityPy.load((OUT/model_row['file']).read_bytes())
    env = UnityPy.load((OUT/row['file']).read_bytes())
    idle = next(o.read_typetree() for o in env.objects if o.type.name == 'AnimationClip' and o.read().m_Name == 'idle_battle')
    obj = next(o for o in env.objects if o.type.name == 'AnimationClip' and o.read().m_Name == 'run')
    tree, check = retarget_run(native_run, native_model, model, idle)
    node = next(n for n in obj._get_typetree_node().m_Children if n.m_Name == 'm_MuscleClip')
    writer = EndianBinaryWriter(endian=obj.reader.endian)
    write_typetree(tree['m_MuscleClip'], node, writer, obj.assets_file)
    tree['m_MuscleClipSize'] = len(writer.bytes)
    obj.save_typetree(tree)
    def save_bundle(env,row):
        global report
        bt=next(o.read() for o in env.objects if o.type.name=='AssetBundle')
        paths=[(p,v.asset.m_PathID) for p,v in bt.m_Container]
        report=[r for r in report if r['logical']!=row['logical']]
        emit(env,row['logical'],paths,bundles[bundle_key(row['file'])]['deps'])
    save_bundle(env,row)
    # Battle uses per-skill dash/return states, not the common run state.
    # Install both phases for both skills, including the donor skill_01
    # bundle which never supplied a dash/return clip in the first place.
    check['skill_movement_clips']=[]
    for index in [1,2]:
        arow=next(r for r in report if r['logical']==prefix+f'_animations_{index}')
        aenv=UnityPy.load((OUT/arow['file']).read_bytes());asset=aenv.assets[0]
        template=next(o for o in aenv.objects if o.type.name=='AnimationClip')
        bundle=next(o for o in aenv.objects if o.type.name=='AssetBundle');bt=bundle.read_typetree()
        directory=bt['m_Container'][0][0].rsplit('/',1)[0]
        for phase in ['dash','return']:
            name=f'skill_0{index}_{phase}'
            clip=next((o for o in aenv.objects if o.type.name=='AnimationClip' and o.read().m_Name==name),None)
            if clip is None:
                clip=clone(template,asset,8100000000000000000+index*10+(phase=='return'))
                bt['m_Container'].append((directory+'/'+name+'.anim',dict(preloadIndex=0,preloadSize=0,asset=ptr(clip.path_id))))
            gait=deepcopy(tree);gait['m_Name']=name
            clip.save_typetree(gait);check['skill_movement_clips'].append(name)
        bundle.save_typetree(bt);save_bundle(aenv,arow)
    check.update(source=unit['source'],model=unit['model']); checks.append(check)
    print(unit['source'], 'looping run:', len(check['animated_bones']), 'moving bones', flush=True)
(OUT/'br-m.bin').write_bytes(write(*manifest))
(OUT/'assets.json').write_text(json.dumps(report,indent=2))
(ROOT/'Research/TokyoGhoul/running-validation.json').write_text(json.dumps(checks,indent=2))
print('Updated',len(checks),'movement bundles; other animations and models preserved')
