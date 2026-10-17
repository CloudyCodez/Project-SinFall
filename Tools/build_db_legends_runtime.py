"""Supply imported fighters' native battle sockets and event-bearing fusion clip."""
import json
from copy import deepcopy
import build_db_legends_models as c
MODELS=['goku_base','goku_blue','goku_ui','vegeta_base','vegeta_super','vegeta_blue','gogeta_blue']
for model in MODELS:
 logical='phoenix_dbl_runtime_'+model+'_sockets';c.report[:]=[r for r in c.report if r['logical']!=logical]
 e=c.gc('FE97C080DD9E32B91ED4480F09F1F997')
 bt=next(o.read() for o in e.objects if o.type.name=='AssetBundle')
 path,entry=next((p,v) for p,v in bt.m_Container if 'socket_hero_meliodas_berserker' in p)
 root=entry.asset.m_PathID
 go=e.assets[0].objects[root];t=go.read_typetree();t['m_Name']='socket_hero_'+model;go.save_typetree(t)
 deps=next(x['deps'] for x in c.bundles.values() if x['name']=='FE97C080DD9E32B91ED4480F09F1F997')
 c.emit(e,logical,[(f'assets/sevensins/patchresources/character/hero_{model}/socket_hero_{model}.prefab',root)],deps)
# Ability attacks require an animation hit event before PlayAbilitySkill fires.
logical='phoenix_dbl_runtime_goku_ui_fusion';c.report[:]=[r for r in c.report if r['logical']!=logical]
e=None
for r in c.report:
 if r['logical'].startswith('phoenix_dbl_goku_ui_animations_'):
  candidate=c.UnityPy.load(str(c.OUT/r['file']))
  found=next((o for o in candidate.objects if o.type.name=='AnimationClip' and o.read().m_Name=='skill_01_ready'),None)
  if found:e=candidate;idle=found;break
assert e is not None
# Use the already retargeted model's pose and native action events. Keep the
# generic schema intact; missing camera/ability clips no longer short circuit.
paths=[]
for i,name in enumerate(['ability','ability_01','ability_01_atk','ability_01_ready','ability_01_idle']):
 obj=c.clone(idle,e.assets[0],8200000000000000000+i);t=obj.read_typetree();t['m_Name']=name;t['m_MuscleClip']['m_LoopTime']=name.endswith('_idle')
 length=t['m_MuscleClip']['m_StopTime']
 t['m_Events']=[] if name.endswith(('_idle','_ready')) else [dict(time=length*.1,functionName='OnAnimationEffect',data='',objectReferenceParameter=c.ptr(),floatParameter=0.0,intParameter=198500001,messageOptions=0),dict(time=length*.65,functionName='OnAnimationEvent',data='{"state":"dmg","speed":"0.01","height":"0","distance":"0","finishblend":"False","reactionoff":"True"}',objectReferenceParameter=c.ptr(),floatParameter=0.0,intParameter=131331,messageOptions=0)]
 obj.save_typetree(t)
 for folder in ['ability','ability_01','_common']:paths.append((f'assets/sevensins/patchresources/character/hero_goku_ui/ani/weapon_glove/{folder}/{name}.anim',obj.path_id))
c.emit(e,logical,paths,[])
# Keep Blue Vegeta's head on the same animated bone as the neck mesh.
r=next(r for r in c.report if r['logical']=='phoenix_dbl_vegeta_blue_model');e=c.UnityPy.load(str(c.OUT/r['file']));objects=e.assets[0].objects
for o in e.objects:
 if o.type.name=='Transform':
  t=o.read_typetree();p=t['m_Father']['m_PathID']
  if p and objects[p].type.name=='Transform':
   pg=objects[objects[p].read_typetree()['m_GameObject']['m_PathID']].read_typetree()['m_Name']
   cg=objects[t['m_GameObject']['m_PathID']].read_typetree()['m_Name']
   if pg=='b_C_Head' and ('face' in cg.lower() or 'hair' in cg.lower()):
    t['m_LocalPosition']=dict(x=0.0,y=0.0,z=0.0);o.save_typetree(t)
paths=[(p,v.asset.m_PathID) for o in e.objects if o.type.name=='AssetBundle' for p,v in o.read().m_Container];deps=c.bundles[c.bundle_key(r['file'])]['deps'];c.report.remove(r);c.emit(e,r['logical'],paths,deps)
# GC computes travel timing from AnimationClip.averageSpeed, while Legends'
# flight clips have zero root displacement. Supply the native movement hint.
for r in list(c.report):
 if r['logical'].startswith('phoenix_dbl_') and '_animations_' in r['logical']:
  e=c.UnityPy.load(str(c.OUT/r['file']));changed=False
  for o in e.objects:
   if o.type.name=='AnimationClip' and (o.read().m_Name=='run' or 'dash' in o.read().m_Name or 'return' in o.read().m_Name):
    t=o.read_typetree();t['m_MuscleClip']['m_AverageSpeed']=dict(x=0.0,y=0.0,z=6.0);o.save_typetree(t);changed=True
  if changed:
   paths=[(p,v.asset.m_PathID) for o in e.objects if o.type.name=='AssetBundle' for p,v in o.read().m_Container];deps=c.bundles[c.bundle_key(r['file'])]['deps'];c.report.remove(r);c.emit(e,r['logical'],paths,deps)
# Slow Gogeta's combat motion and its actual damage/VFX events together.
# The timing marker makes repeated runtime builds idempotent.
from retime_generic_clip import stretch_clip
for r in list(c.report):
 if r['logical'].startswith('phoenix_dbl_gogeta_blue_animations_'):
  e=c.UnityPy.load(str(c.OUT/r['file']));changed=False
  for o in e.objects:
   if o.type.name!='AnimationClip':continue
   t=o.read_typetree();name=t['m_Name']
   if name=='skill_01_atk':
    # All six damage contacts start with the first punch, after approach.
    t['m_Events']=[x for x in t['m_Events'] if x['functionName']!='OnAnimationEvent']
    duration=t['m_MuscleClip']['m_StopTime']
    for fraction,hit in [(0.03,65794),(.18,65794),(.33,65794),(.48,65794),(.63,65794),(.78,131330)]:
     t['m_Events'].append(dict(time=duration*fraction,functionName='OnAnimationEvent',data='{"state":"dmg","speed":"0.01","height":"0","distance":"0","finishblend":"False"}',objectReferenceParameter=c.ptr(),floatParameter=0.0,intParameter=hit,messageOptions=0))
    t['m_Events'].sort(key=lambda x:x['time']);o.save_typetree(t);changed=True
   if not (name.startswith('skill_') or name.startswith('special_')):continue
   marker=next((x for x in t['m_Events'] if x['functionName']=='PhoenixTimingMarker'),None)
   previous=(marker['floatParameter'] or 1.7) if marker else 1.0
   target=3.0
   if previous>=target:continue
   t['m_Events']=[x for x in t['m_Events'] if x['functionName']!='PhoenixTimingMarker']
   stretch_clip(t,target/previous)
   t['m_Events'].append(dict(time=t['m_MuscleClip']['m_StopTime'],functionName='PhoenixTimingMarker',data='',objectReferenceParameter=c.ptr(),floatParameter=target,intParameter=0,messageOptions=1))
   from UnityPy.helpers.TypeTreeHelper import write_typetree
   from UnityPy.streams import EndianBinaryWriter
   writer=EndianBinaryWriter(endian=o.reader.endian);node=next(n for n in o._get_typetree_node().m_Children if n.m_Name=='m_MuscleClip');write_typetree(t['m_MuscleClip'],node,writer,o.assets_file);t['m_MuscleClipSize']=len(writer.bytes)
   o.save_typetree(t);changed=True
  if changed:
   paths=[(p,v.asset.m_PathID) for o in e.objects if o.type.name=='AssetBundle' for p,v in o.read().m_Container];deps=c.bundles[c.bundle_key(r['file'])]['deps'];c.report.remove(r);c.emit(e,r['logical'],paths,deps)
# Retarget Gogeta's own Legends entry motion for the native tag appearance.
logical='phoenix_dbl_runtime_gogeta_entrance';c.report[:]=[r for r in c.report if r['logical']!=logical]
e=c.UnityPy.load(str(c.OUT/next(r['file'] for r in c.report if r['logical']=='phoenix_dbl_gogeta_blue_animations_0')))
donor=next(o for o in e.objects if o.type.name=='AnimationClip' and o.read().m_Name=='idle_battle')
source=c.UnityPy.load(str(c.SOURCE/'0078d08dd86329535d70b2ee86e03e38d82b4df5'))
entry=next((o for o in source.objects if o.type.name=='AnimationClip' and o.read().m_Name=='GTB_05_BAS_CHANGE_IN'),None)
if entry:
 import zlib
 actual=json.loads((c.ROOT/'Research/DBLegends/gogeta_blue-rig.json').read_text())['paths']
 sourcepaths={h:p for o in source.objects if o.type.name=='Avatar' for h,p in o.read_typetree()['m_TOS']}
 # This common bundle has no Avatar. Resolve source-relative skeleton hashes
 # from every suffix of our actual rig rather than silently leaving them unbound.
 for path in actual:
  segments=path.split('/')
  for start in range(len(segments)):
   suffix='/'.join(segments[start:]);sourcepaths.setdefault(zlib.crc32(suffix.encode()),suffix)
 def merge(dst,src):
  if isinstance(dst,dict) and isinstance(src,dict):return {k:merge(v,src[k]) if k in src else v for k,v in dst.items()}
  return deepcopy(src)
 tree=merge(donor.read_typetree(),entry.read_typetree())
 mapped=0
 for b in tree['m_ClipBindingConstant']['genericBindings']:
  if b['typeID']==4:
   path=sourcepaths.get(b['path'],'');matches=[p for p in actual if path and p and (path==p or p.endswith('/'+path) or path.endswith('/'+p))]
   if matches:b['path']=zlib.crc32(max(matches,key=len).encode());mapped+=1
   if b['attribute']==1 and b['path']==zlib.crc32(b'VisualRoot/b_C_Base'):b['path']=zlib.crc32(b'LegendsRootMotion')
 assert mapped==sum(b['typeID']==4 for b in tree['m_ClipBindingConstant']['genericBindings']),('Unbound entrance bones',mapped)
 tree['m_MuscleClip']['m_LoopTime']=False;tree['m_Events']=[dict(time=.05,functionName='OnAnimationEffect',data='',objectReferenceParameter=c.ptr(),floatParameter=0.0,intParameter=198500001,messageOptions=0)]
 # Legends' battle entry is only 0.417s (0.139s at GC x3). Stretch the
 # actual curves, including cubic tangents, so x3 presents it over 0.833s.
 # This is confined to appearance aliases; combat/game speed stays native.
 from retime_generic_clip import stretch_clip
 stretch_clip(tree,6.0)
 paths=[]
 for i,name in enumerate(['idle_change','appear','appear_drop','tag_change_return']):
  obj=c.clone(donor,e.assets[0],8300000000000000000+i);tree['m_Name']=name
  from UnityPy.helpers.TypeTreeHelper import write_typetree
  from UnityPy.streams import EndianBinaryWriter
  writer=EndianBinaryWriter(endian=obj.reader.endian);node=next(n for n in obj._get_typetree_node().m_Children if n.m_Name=='m_MuscleClip');write_typetree(tree['m_MuscleClip'],node,writer,obj.assets_file);tree['m_MuscleClipSize']=len(writer.bytes)
  obj.save_typetree(tree);paths.append((f'assets/sevensins/patchresources/character/hero_gogeta_blue/ani/weapon_glove/_common/{name}.anim',obj.path_id))
 c.emit(e,logical,paths,[])
else:raise ValueError('Downloaded Gogeta entry clip missing')
# The active ability uses a dedicated hero-keyed icon lookup.
r=next(r for r in c.report if r['logical'].startswith('phoenix_dbl_gogeta_blue_icon'))
e=c.UnityPy.load(str(c.OUT/r['file']));tex=next(o for o in e.objects if o.type.name=='Texture2D')
logical='phoenix_dbl_runtime_fusion_icon';c.report[:]=[r for r in c.report if r['logical']!=logical]
c.emit(e,logical,[(f'assets/sevensins/patchresources/ui/image/icon/ability/icon_ability_2997001.png',tex.path_id)],[])
(c.OUT/'br-m.bin').write_bytes(c.write(*c.manifest));(c.OUT/'assets.json').write_text(json.dumps(c.report,indent=2))
print('Registered seven native socket prefabs, event-bearing fusion clips, Blue Vegeta neck correction')
