"""Check resources requested by the actual phone's fusion/battle errors."""
import json,UnityPy
from pathlib import Path
from gc_bundle_manifest import read,hash_name,bundle_key
root=Path(__file__).resolve().parents[1];out=root/'dist/kaneki-assets';rows=json.loads((out/'assets.json').read_text());bundles,_,dirs=read((out/'br-m.bin').read_bytes());base='assets/sevensins/patchresources/'
def resolve(folder,name):
 key=dirs[base][hash_name(folder+'/')][hash_name(name)];return next(r for r in rows if bundle_key(r['file'])==key)
for model in ['goku_base','goku_blue','goku_ui','vegeta_base','vegeta_super','vegeta_blue','gogeta_blue']:
 row=resolve('character/hero_'+model,'socket_hero_'+model+'.prefab');e=UnityPy.load(str(out/row['file']));assert any(o.type.name=='GameObject' and o.read().m_Name=='socket_hero_'+model for o in e.objects)
 for name in ['skill_01_dash','skill_01_return']:
  row=resolve(f'character/hero_{model}/ani/weapon_glove/skill_01',name+'.anim')
  e=UnityPy.load(str(out/row['file']));t=next(o.read_typetree() for o in e.objects if o.type.name=='AnimationClip' and o.read().m_Name==name)
  assert t['m_MuscleClip']['m_AverageSpeed']['z']>0
  assert t['m_ClipBindingConstant']['genericBindings']
row=resolve('character/hero_goku_ui/ani/weapon_glove/ability','ability_01_atk.anim');e=UnityPy.load(str(out/row['file']));clip=next(o.read_typetree() for o in e.objects if o.type.name=='AnimationClip' and o.read().m_Name=='ability_01_atk');assert any(x['functionName']=='OnAnimationEvent' and x['intParameter']==131331 for x in clip['m_Events'])
for event in clip['m_Events']:
 if event['functionName']=='OnAnimationEvent':
  data=json.loads(event['data']);assert all(k in data for k in ['state','speed','height','distance','finishblend']),data
row=resolve('character/hero_gogeta_blue/ani/weapon_glove/_common','idle_change.anim');e=UnityPy.load(str(out/row['file']));clip=next(o.read_typetree() for o in e.objects if o.type.name=='AnimationClip' and o.read().m_Name=='idle_change');assert not clip['m_MuscleClip']['m_LoopTime']
for o in e.objects:
 if o.type.name=='AssetBundle':
  for path,entry in o.read().m_Container:
   if path.endswith(('/idle_change.anim','/appear.anim','/appear_drop.anim','/tag_change_return.anim')):
    t=entry.asset.read_typetree()
    assert abs(t['m_MuscleClip']['m_StopTime']-2.5)<1e-5
    assert abs(t['m_MuscleClip']['m_Clip']['data']['m_DenseClip']['m_SampleRate']-10.0)<1e-5
    assert abs(t['m_Events'][0]['time']-.3)<1e-5
resolve('character/hero_gogeta_blue/ani/weapon_glove/_common','tag_change_return.anim')
resolve('ui/image/icon/ability','icon_ability_2997001.png')
checked=0
for row in rows:
 if row['logical'].startswith('phoenix_dbl_') and '_vfx_' in row['logical']:
  from pathlib import PurePosixPath
  e=UnityPy.load(str(out/row['file']))
  for o in e.objects:
   if o.type.name=='AssetBundle':
    for path,v in o.read().m_Container:
     if path.endswith('.prefab'):assert v.asset.read().m_Name==PurePosixPath(path).stem,(row['logical'],path)
 if row['logical'].startswith('phoenix_dbl_') and '_animations_' in row['logical']:
  e=UnityPy.load(str(out/row['file']))
  for o in e.objects:
   if o.type.name=='AnimationClip':
    t=o.read_typetree();name=t['m_Name']
    if name=='skill_01_ready':assert not any(x['functionName']=='OnAnimationEvent' for x in t['m_Events']);checked+=1
    if name=='run' or 'dash' in name or 'return' in name:assert t['m_MuscleClip']['m_AverageSpeed']['z']>0
assert checked>=7
def table(name):return json.loads((root/'Research/DecodedCache'/f'{name}.tg.offline.json').read_text())
skins={r['id']:r for r in table('DB_skin_base')}
for field in ['atk','def','hp','atk_add','def_add','hp_add']:
 assert skins[399921][field]==1.5*(skins[399903][field]+skins[399913][field]),field
for level in [1,50,100]:
 for stat in ['atk','def','hp']:
  values=[skins[s][stat]+(level-1)*skins[s][stat+'_add'] for s in [399903,399913,399921]]
  assert abs(values[2]-1.5*(values[0]+values[1]))<1e-6,(stat,level)
# Root displacement goes to an unweighted sibling; GC owns battlefield travel.
import zlib
rig_paths=json.loads((root/'Research/DBLegends/gogeta_blue-rig.json').read_text())['paths']
entrance_paths={zlib.crc32(p.encode()) for p in rig_paths}|{zlib.crc32(b'LegendsRootMotion')}
for row in rows:
 if row['logical'].startswith('phoenix_dbl_gogeta_blue_animations_') or row['logical']=='phoenix_dbl_runtime_gogeta_entrance':
  e=UnityPy.load(str(out/row['file']))
  for o in e.objects:
   if o.type.name=='AnimationClip':
    t=o.read_typetree()
    if row['logical'].startswith('phoenix_dbl_gogeta_blue_animations_') and t['m_Name'].startswith(('skill_', 'special_')):
     marker=next(x for x in t['m_Events'] if x['functionName']=='PhoenixTimingMarker')
     assert marker['floatParameter']==3.0, 'Gogeta combat timing must compensate for x3 speed'
    if row['logical'].startswith('phoenix_dbl_gogeta_blue_animations_') and t['m_Name']=='skill_01_atk':
     hits=[x for x in t['m_Events'] if x['functionName']=='OnAnimationEvent']
     assert len(hits)==6 and [x['intParameter'] for x in hits]==[65794]*5+[131330]
     assert hits[0]['time']<.1*t['m_MuscleClip']['m_StopTime']
    for b in t['m_ClipBindingConstant']['genericBindings']:
     assert not (b['typeID']==4 and b['attribute']==1 and b['path']==zlib.crc32(b'VisualRoot/b_C_Base')),(row['logical'],o.read().m_Name)
     if row['logical']=='phoenix_dbl_runtime_gogeta_entrance' and t['m_Name'] in ['idle_change','appear','appear_drop','tag_change_return'] and b['typeID']==4:assert b['path'] in entrance_paths,('Unbound entrance bone',b)
heroes={(r['id']^0x92929292)&0xffffffff:r for r in table('DB_hero_base')}
# The engine indexes dormant tag units by the same group as the active unit.
# Compare the full relationship with the shipped Camilla transformation pair.
for main,sub in [(344002,344902),(399903,399921)]:
 a,b=skins[main],skins[sub]
 assert a['change_hero_skin_id']==sub and b['before_change_hero_skin_id']==main
 assert a['category_group']==b['category_group']
 assert heroes[a['matching_hero_id']]['hero_group']==heroes[b['matching_hero_id']]['hero_group']
 assert a['after_change_hero_model']==0 and b['after_change_hero_model']==1
passive=next(r for r in table('DB_skin_exclusive_passive') if r['hero_id']==2997003)
assert passive['list_array_ability_exclusive_passive_id']==[]
assert not any(r['skin_id']==399921 for r in table('DB_gamble_group'))
print('PASS: seven native socket resources, fusion animation hit event, active ability icon, Gogeta entry clip, charge-only ready events and nonzero flight speed')
