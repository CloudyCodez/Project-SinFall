"""Port Black/Rosé's downloaded motion, portraits and transformation particles."""
import json,zlib
from copy import deepcopy
import build_db_legends_animations as a
import build_db_legends_models as c
from retime_generic_clip import stretch_clip
from trim_streamed_generic_clip import trim_clip_start
from UnityPy.helpers.TypeTreeHelper import write_typetree
from UnityPy.streams import EndianBinaryWriter

FORMS=[('goku_black','e8e1bacac103bbedc48433e91743e89ae3ffb3b5','GokuBlack_02','246d2fb1351a7cff8b49f7d894af8a1c8c5504d1','GokuBlack_02_SPA_BKPowerball'),('goku_black_rose','cecc9fd198d52e02ce042c9fcaf7f257fcf04481','GokuBKR_02','87c79a0dd94d3e82e798646fe2c3e901eb201007','GokuBKR_02_SPA_Slashing_ATC')]
for form in FORMS:a.build(*form,effect_base=198500040 if form[0]=='goku_black' else 198500050)

def save_clip(o,t):
 writer=EndianBinaryWriter(endian=o.reader.endian)
 node=next(n for n in o._get_typetree_node().m_Children if n.m_Name=='m_MuscleClip')
 write_typetree(t['m_MuscleClip'],node,writer,o.assets_file);t['m_MuscleClipSize']=len(writer.bytes);o.save_typetree(t)

def port_clip(source,donor,model,name,camera=False):
 def merge(dst,src):
  if isinstance(dst,dict) and isinstance(src,dict):return {k:merge(v,src[k]) if k in src else v for k,v in dst.items()}
  return deepcopy(src)
 t=merge(donor.read_typetree(),source.read_typetree());actual=json.loads((c.ROOT/'Research/DBLegends'/f'{model}-rig.json').read_text())['paths']
 suffixes={zlib.crc32('/'.join(p.split('/')[i:]).encode()):p for p in actual for i in range(len(p.split('/')))}
 for b in t['m_ClipBindingConstant']['genericBindings']:
  if camera:continue
  if b['typeID']!=4:continue
  assert b['path'] in suffixes,(model,name,b['path'])
  path=suffixes[b['path']];b['path']=zlib.crc32(path.encode())
  if b['attribute']==1 and path=='VisualRoot/b_C_Base':b['path']=zlib.crc32(b'LegendsRootMotion')
 t['m_Name']=name;t['m_MuscleClip']['m_LoopTime']=False;t['m_Events']=[]
 return t

# Original transformation is five seconds. Retiming all curves by three keeps
# that presentation readable when the battle is running at triple speed.
src=c.UnityPy.load(str(c.SOURCE/'26ca68052ea118a87a47a0437a7e6da20f9cfe46'))
motion=max((o for o in src.objects if o.type.name=='AnimationClip'),key=lambda o:len(o.read_typetree()['m_ClipBindingConstant']['genericBindings']))
camera_motion=min((o for o in src.objects if o.type.name=='AnimationClip'),key=lambda o:len(o.read_typetree()['m_ClipBindingConstant']['genericBindings']))
assert len(camera_motion.read_typetree()['m_ClipBindingConstant']['genericBindings'])==3
for model in ['goku_black','goku_black_rose']:
 r=next(r for r in c.report if r['logical']==f'phoenix_dbl_{model}_animations_0');e=c.UnityPy.load(str(c.OUT/r['file']))
 donor=next(o for o in e.objects if o.type.name=='AnimationClip' and o.read().m_Name=='idle_battle');paths=[]
 camera=c.clone(donor,e.assets[0],8500000000000000010)
 camera_tree=port_clip(camera_motion,donor,model,'ability_transform_cam',camera=True)
 stretch_clip(camera_tree,3.0)
 if model=='goku_black_rose':trim_clip_start(camera_tree,camera_tree['m_MuscleClip']['m_StopTime']*.53)
 save_clip(camera,camera_tree)
 paths.append((f'assets/sevensins/patchresources/character/hero_{model}/ani/weapon_glove/_common/ability_transform_cam.anim',camera.path_id))
 for i,name in enumerate(['ability','ability_01','ability_01_atk','ability_01_ready','ability_01_idle','tag_change_return','tag_change','idle_change']):
  obj=c.clone(donor,e.assets[0],8500000000000000000+i)
  t=port_clip(motion,donor,model,name);stretch_clip(t,3.0)
  if model=='goku_black_rose':
   # Continue the original source motion after impact instead of restarting it.
   trim_clip_start(t,t['m_MuscleClip']['m_StopTime']*.53)
   if name in ['idle_change','tag_change']:
    t['m_Events'].append(dict(time=.01,functionName='OnAnimationCamera',data='',objectReferenceParameter=c.ptr(camera.path_id),floatParameter=.2,intParameter=(1<<28)|524288|1048576,messageOptions=0))
    t['m_Events'].append(dict(time=.10,functionName='OnAnimationSound',data='',objectReferenceParameter=c.ptr(),floatParameter=1.0,intParameter=198510001,messageOptions=0))
    t['m_Events'].append(dict(time=.20,functionName='OnAnimationEffect',data='',objectReferenceParameter=c.ptr(),floatParameter=0.0,intParameter=198500065,messageOptions=0))
    t['m_Events'].append(dict(time=.05,functionName='OnAnimationEffect',data='',objectReferenceParameter=c.ptr(),floatParameter=0.0,intParameter=198500064,messageOptions=0))
  elif name=='tag_change_return':
   trim_clip_start(t,t['m_MuscleClip']['m_StopTime']-.30)
  else:
   # The native ability plays ability_01, not the tag/appearance aliases.
   t['m_Events'].append(dict(time=.01,functionName='OnAnimationCamera',data='',objectReferenceParameter=c.ptr(camera.path_id),floatParameter=.2,intParameter=(1<<28)|524288|1048576,messageOptions=0))
   t['m_Events'].append(dict(time=.15,functionName='OnAnimationSound',data='',objectReferenceParameter=c.ptr(),floatParameter=1.0,intParameter=198510002,messageOptions=0))
   for fraction,sfx in [(.04,198500061),(.30,198500062),(.53,198500063)]:
    t['m_Events'].append(dict(time=t['m_MuscleClip']['m_StopTime']*fraction,functionName='OnAnimationEffect',data='',objectReferenceParameter=c.ptr(),floatParameter=0.0,intParameter=sfx,messageOptions=0))
  save_clip(obj,t)
  for folder in ['_common','ability','ability_01']:paths.append((f'assets/sevensins/patchresources/character/hero_{model}/ani/weapon_glove/{folder}/{name}.anim',obj.path_id))
 logical=f'phoenix_dbl_{model}_transformation';c.report[:]=[x for x in c.report if x['logical']!=logical];c.emit(e,logical,paths,[])
 # Readable attack timing and contact events use the same time multiplier.
 for r in list(c.report):
  if not r['logical'].startswith(f'phoenix_dbl_{model}_animations_'):continue
  e=c.UnityPy.load(str(c.OUT/r['file']))
  for o in e.objects:
   if o.type.name!='AnimationClip':continue
   t=o.read_typetree()
   if t['m_Name'].startswith(('skill_','special_')) and not any(k in t['m_Name'] for k in ['dash','return']):stretch_clip(t,2.0);save_clip(o,t)
  paths=[(p,v.asset.m_PathID) for o in e.objects if o.type.name=='AssetBundle' for p,v in o.read().m_Container]
  c.report.remove(r);c.emit(e,r['logical'],paths,c.bundles[c.bundle_key(r['file'])]['deps'])
 # Native battle socket component schema, with requested prefab name.
 e=c.gc('FE97C080DD9E32B91ED4480F09F1F997');bt=next(o.read() for o in e.objects if o.type.name=='AssetBundle')
 path,entry=next((p,v) for p,v in bt.m_Container if 'socket_hero_meliodas_berserker' in p);go=e.assets[0].objects[entry.asset.m_PathID];t=go.read_typetree();t['m_Name']='socket_hero_'+model;go.save_typetree(t)
 logical=f'phoenix_dbl_{model}_sockets';c.report[:]=[x for x in c.report if x['logical']!=logical];c.emit(e,logical,[(f'assets/sevensins/patchresources/character/hero_{model}/socket_hero_{model}.prefab',go.path_id)],next(x['deps'] for x in c.bundles.values() if x['name']=='FE97C080DD9E32B91ED4480F09F1F997'))

for model,file,fragment in [('goku_black','b39059c512f133c9cf1de1ec9b16dcc1dd7d4910','GokuBlack_350'),('goku_black_rose','05ca1553ead3af5889cbb573ed1fdb78d699c0ed','GokuBlackRose_350')]:
 src=c.UnityPy.load(str(c.SOURCE/file));image=next(o.read().image for o in src.objects if o.type.name=='Texture2D' and fragment.lower() in o.read().m_Name.lower())
 e=c.gc('253AD473855C32C7DC4EC70CA51D9A7D');asset=e.assets[0];ab=next(o for o in e.objects if o.type.name=='AssetBundle');template=next(o for o in e.objects if o.type.name=='Texture2D');asset.objects={ab.path_id:ab}
 tex=c.clone(template,asset,8500000000000000020);t=tex.read();t.m_Name=model+'_portrait';t.set_image(image.convert('RGBA'),target_format=4);t.save()
 paths=[(f'assets/sevensins/patchresources/ui/image/icon/{folder}/{prefix}{model}_0001{suffix}.png',tex.path_id) for prefix in ['icon_hero_','icon_skin_'] for suffix in ['_s','_l','_card'] for folder in ['hero','costume','Hero_Coin','skillactive/hero']]
 paths.append((f'assets/sevensins/patchresources/ui/image/icon/hero/{model}_0001.png',tex.path_id))
 if model=='goku_black':paths.append(('assets/sevensins/patchresources/ui/image/icon/ability/icon_ability_2997004.png',tex.path_id))
 logical=f'phoenix_dbl_{model}_icon';c.report[:]=[x for x in c.report if x['logical']!=logical];c.emit(e,logical,paths,[])

# Original Legends particle hierarchies, converted to native GC components.
import build_db_legends_vfx as v
effects=[('charge','gokublack_cc_return_crg',198500041,'5633a1cde662ff530b9e12b6f1d6c1dd5cbd1d28'),('beam','gokublack_cc_return_fire',198500042,'5633a1cde662ff530b9e12b6f1d6c1dd5cbd1d28'),('impact','slash_blackrose_hit',198500043,'178a362dc0abe7ef2d9184f6e8f2e1f5f2028c81'),('release','gokublack_cc_return_burst',198500044,'5633a1cde662ff530b9e12b6f1d6c1dd5cbd1d28'),('rose_charge','gokublackrose_intro_handaura',198500051,'5633a1cde662ff530b9e12b6f1d6c1dd5cbd1d28'),('rose_slash','slash_blackrose_handsword',198500052,'178a362dc0abe7ef2d9184f6e8f2e1f5f2028c81'),('rose_hit','slash_blackrose_hit',198500053,'178a362dc0abe7ef2d9184f6e8f2e1f5f2028c81'),('rose_trail','slash_blackrose_swordtrail01',198500054,'178a362dc0abe7ef2d9184f6e8f2e1f5f2028c81'),('transform_charge','gokublack_change_start',198500061,'5633a1cde662ff530b9e12b6f1d6c1dd5cbd1d28'),('transform_spark','gokublack_change01',198500062,'5633a1cde662ff530b9e12b6f1d6c1dd5cbd1d28'),('transform_burst','gokublack_change02',198500063,'5633a1cde662ff530b9e12b6f1d6c1dd5cbd1d28'),('transform_aura','aura_ssrose',198500064,'2feb5dec130fc59260280973a648f890faa7f755'),('transform_end','gokublack_change_end',198500065,'5633a1cde662ff530b9e12b6f1d6c1dd5cbd1d28')]
for label,name,sfx,file in effects:v.build(label,name,sfx,file,'goku_black')
(c.OUT/'br-m.bin').write_bytes(c.write(*c.manifest));(c.OUT/'assets.json').write_text(json.dumps(c.report,indent=2))
(c.ROOT/'Research/DBLegends/black-vfx-registration.json').write_text(json.dumps([dict(id=sfx,path='DragonBall/goku_black',filename='fx_goku_black_'+label) for label,name,sfx,file in effects],indent=2))
print('Built Black/Rosé combat, original transformation motion, portraits, sockets and effects')
