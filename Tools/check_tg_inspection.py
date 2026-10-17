"""Check actual prefab paths against generic idle bindings and kagune shaders."""
from pathlib import Path
import json,zlib
import UnityPy
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/kaneki-assets'
rows=json.loads((OUT/'assets.json').read_text());report=[]
for row in rows:
 if not row['logical'].startswith('phoenix_tg_') or not row['logical'].endswith('_model'):continue
 e=UnityPy.load((OUT/row['file']).read_bytes());objects=e.assets[0].objects
 transforms={o.path_id:o.read_typetree() for o in e.objects if o.type.name=='Transform'}
 names={o.path_id:o.read().m_Name for o in e.objects if o.type.name=='GameObject'}
 root=next(i for i,t in transforms.items() if t['m_Father']['m_PathID']==0 and names[t['m_GameObject']['m_PathID']].endswith('_body_0001'))
 def path(i):
  if i==root:return ''
  t=transforms[i];prefix=path(t['m_Father']['m_PathID']);return (prefix+'/' if prefix else '')+names[t['m_GameObject']['m_PathID']]
 paths={path(i) for i,t in transforms.items() if i==root or t['m_Father']['m_PathID']}
 avatar=next(o.read_typetree() for o in e.objects if o.type.name=='Avatar')
 assert {s for _,s in avatar['m_TOS']}==paths,row['logical']
 assert all(h==zlib.crc32(s.encode()) for h,s in avatar['m_TOS'])
 driver=[o.read_typetree() for o in e.objects if o.type.name=='Animator'];assert len(driver)==1 and driver[0]['m_GameObject']['m_PathID']==transforms[root]['m_GameObject']['m_PathID']
 arow=next(r for r in rows if r['logical']==row['logical'].replace('_model','_animations_0'))
 a=UnityPy.load((OUT/arow['file']).read_bytes());valid={h for h,s in avatar['m_TOS']}
 results={}
 for o in a.objects:
  if o.type.name=='AnimationClip' and o.read().m_Name in ['idle','idle_battle']:
   t=o.read_typetree();bindings=[b['path'] for b in t['m_ClipBindingConstant']['genericBindings'] if b['typeID']==4]
   ratio=sum(h in valid for h in bindings)/len(bindings)
   assert ratio>.9,(row['logical'],t['m_Name'],ratio)
   assert t['m_MuscleClip']['m_LoopTime'],(row['logical'],t['m_Name'],'not looping')
   results[t['m_Name']]=round(ratio,4)
 materials=[o.read_typetree() for o in e.objects if o.type.name=='Material']
 fx=[t for t in materials if t['m_CustomRenderQueue']==3000]
 for material in fx:
  shader=objects[material['m_Shader']['m_PathID']].read_typetree()['m_ParsedForm']
  assert shader['m_Name']=='Phoenix/Kagune Additive'
  for sub in shader['m_SubShaders']:
   for p in sub['m_Passes']:assert p['m_State']['rtBlend0']['destBlend']['val']==1.0
 report.append(dict(model=row['logical'],idle_binding_coverage=results,effect_materials=len(fx)))
(ROOT/'Research/TokyoGhoul/inspection-validation.json').write_text(json.dumps(report,indent=2))
print('PASS:',len(report),'rebuilt hierarchies and looping inspection/battle idles; kagune additive materials checked')
