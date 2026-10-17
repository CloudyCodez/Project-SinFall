"""Validate Black's impact swap, camera aliases and original pose continuation."""
import sys,json,struct,math
from copy import deepcopy
import build_db_legends_models as c
from retime_generic_clip import stretch_clip
from trim_streamed_generic_clip import trim_clip_start

def evaluate(tree,time):
 s=tree['m_MuscleClip']['m_Clip']['data']['m_StreamedClip'];raw=struct.pack('<'+'I'*len(s['data']),*s['data']);off=0;values={}
 while off<len(raw):
  at,n=struct.unpack_from('<fi',raw,off);off+=8
  for i in range(n):
   index,a,b,rate,value=struct.unpack_from('<i4f',raw,off);off+=20
   if at<=time:
    dt=time-at if abs(at)<1e30 else 0;values[index]=((a*dt+b)*dt+rate)*dt+value
 return values
src=c.UnityPy.load(str(c.SOURCE/'26ca68052ea118a87a47a0437a7e6da20f9cfe46'))
for obj in src.objects:
 if obj.type.name!='AnimationClip':continue
 full=obj.read_typetree();stretch_clip(full,3.0);cut=full['m_MuscleClip']['m_StopTime']*.53;trim=deepcopy(full);trim_clip_start(trim,cut)
 for dt in [0,.01,.2,1,3,6.9]:
  old=evaluate(full,cut+dt);new=evaluate(trim,dt);assert old.keys()==new.keys()
  assert all(math.isclose(old[k],new[k],rel_tol=2e-4,abs_tol=2e-4) for k in old),('Pose discontinuity',dt)
for model in ['goku_black','goku_black_rose']:
 r=next(r for r in c.report if r['logical']==f'phoenix_dbl_{model}_transformation');e=c.UnityPy.load(str(c.OUT/r['file']));clips={o.read().m_Name:o.read_typetree() for o in e.objects if o.type.name=='AnimationClip'}
 if model=='goku_black':
  t=clips['ability_01'];cam=next(x for x in t['m_Events'] if x['functionName']=='OnAnimationCamera');assert cam['intParameter']&(1<<28)
  target=e.assets[0].objects[cam['objectReferenceParameter']['m_PathID']].read_typetree();assert target['m_Name']=='ability_transform_cam'
  event=next(x for x in t['m_Events'] if x['intParameter']==198500063);assert math.isclose(event['time'],t['m_MuscleClip']['m_StopTime']*.53,abs_tol=1e-5)
  assert clips['tag_change_return']['m_MuscleClip']['m_StopTime']<.31
 else:
  assert 7<clips['idle_change']['m_MuscleClip']['m_StopTime']<7.1
  assert all(x['intParameter']!=198500063 for x in clips['idle_change']['m_Events'])
for r in c.report:
 if not r['logical'].startswith('phoenix_dbl_goku_black_vfx_transform_'):continue
 e=c.UnityPy.load(str(c.OUT/r['file']))
 for o in e.objects:
  if o.type.name=='ParticleSystem':assert math.isclose(o.read_typetree()['simulationSpeed'],1/3,rel_tol=1e-6)
rows=json.loads((c.ROOT/'Research/DecodedCache/DB_sfx.tg.offline.json').read_text())
assert all(next(x for x in rows if x['id']==id)['create_socket']=='fx_spawn_center' for id in [198500061,198500062,198500063,198500064])
print('PASS: source motion/camera continuation preserves sampled poses, active ability carries camera/beam events, Rosé avoids repeated transformation, VFX use supported sockets and x3 timing')
