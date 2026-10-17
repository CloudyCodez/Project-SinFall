"""Check Goku's runtime asset references and native evolution registration."""
from pathlib import Path
import json,zlib
import UnityPy
from gc_bundle_manifest import read,bundle_key,hash_name
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/kaneki-assets'
bundles,_,dirs=read((OUT/'br-m.bin').read_bytes());rows=json.loads((OUT/'assets.json').read_text());selected=[r for r in rows if r['logical'].startswith(('phoenix_dbl_vegeta_','phoenix_dbl_gogeta_'))]
assert len(selected)==40,len(selected)
identities=set();effects=set()
for r in selected:
    e=UnityPy.load((OUT/r['file']).read_bytes());objects=e.assets[0].objects
    for filename in e.file.files:assert filename not in identities;identities.add(filename)
    for path in r['paths']:
        base='assets/sevensins/patchresources/';d,f=path[len(base):].rsplit('/',1)
        expected=r['file']
        if r['logical']=='phoenix_dbl_gogeta_blue_animations_0' and f in ['appear.anim','appear_drop.anim']:
            expected=next(x['file'] for x in rows if x['logical']=='phoenix_dbl_runtime_gogeta_entrance')
        assert dirs[base][hash_name(d+'/')][hash_name(f)]==bundle_key(expected),(r['logical'],path)
    def refs(v):
        if isinstance(v,dict):
            if set(v)=={'m_FileID','m_PathID'}:
                if v['m_FileID']==0 and v['m_PathID']:assert v['m_PathID'] in objects,(r['logical'],v)
            else:
                for x in v.values():refs(x)
        elif isinstance(v,(tuple,list)):
            for x in v:refs(x)
    for o in e.objects:
        t=o.read_typetree();refs(t)
        if r['logical'].endswith('_model') and o.type.name=='Transform' and t['m_Father']['m_PathID']:
            parent=objects[t['m_Father']['m_PathID']].read_typetree()
            parent_go=objects[parent['m_GameObject']['m_PathID']].read_typetree()
            child_go=objects[t['m_GameObject']['m_PathID']].read_typetree()
            if parent_go['m_Name'] in ['g_C_Head','b_C_Head'] and ('face' in child_go['m_Name'].lower() or 'hair' in child_go['m_Name'].lower()):
                if r['logical'] in ['phoenix_dbl_vegeta_blue_model','phoenix_dbl_gogeta_blue_model']:assert parent_go['m_Name']=='b_C_Head'
                expected=0.0
                assert abs(t['m_LocalPosition']['y']-expected)<1e-6 and abs(t['m_LocalPosition']['x'])<1e-6 and abs(t['m_LocalPosition']['z'])<1e-6,(r['logical'],'head socket offset')
        if o.type.name=='GameObject':assert t['m_Layer']==9
        if r['logical'].endswith('_model') and o.type.name=='Transform':
            go=objects[t['m_GameObject']['m_PathID']].read_typetree()
            if go['m_Name']=='VisualRoot':assert abs(t['m_LocalPosition']['y']-.90)<1e-6
        if o.type.name=='AnimationClip':
            assert all(x['time']<=t['m_MuscleClip']['m_StopTime'] for x in t['m_Events'])
            if t['m_Name']=='skill_01_atk':
                hits=[x for x in t['m_Events'] if x['functionName']=='OnAnimationEvent']
                assert [x['intParameter'] for x in hits]==[65794,65794,65794,131330]
                assert len({x['time'] for x in hits})==4
            effects.update(x['intParameter'] for x in t['m_Events'] if x['functionName']=='OnAnimationEffect' and 198500001<=x['intParameter']<=198500024)
        if o.type.name=='ParticleSystem':assert t['playOnAwake'] and not t['looping']
        if o.type.name=='MonoScript':assert o.read().m_ClassName=='container_of_using_bones'
assert effects=={198500001,198500002,198500004,198500011,198500012,198500014,198500021,198500022,198500024},effects

for r in selected:
 if '_vfx_' in r['logical']:
  e=UnityPy.load((OUT/r['file']).read_bytes())
  assert any(o.type.name=='ParticleSystem' for o in e.objects),r['logical']
def table(n):return json.loads((ROOT/'Research/DecodedCache'/f'{n}.tg.offline.json').read_text())
skins=[x for x in table('DB_skin_base') if x['matching_hero_id']==2997002]
assert sorted(x['id'] for x in skins)==[399911,399912,399913]
assert sorted(x['rating'] for x in skins)==[5,6,7]
cards={(x['id']^0x65656565)&0xffffffff:x for x in table('DB_skill_card_base')}
resources={(x['id']^0x11111111)&0xffffffff:x for x in table('DB_skill_card_resource')}
sfx={x['id'] for x in table('DB_sfx')}
for form in range(3):
 base=14100100+form*100
 assert cards[base+1]['target']==2
 assert cards[base+11]['target']==4
 assert cards[base+90]['target']==4
 assert resources[base+90]['skill_folder']=='skill_03'
 for rank in [11,12,13,90]:assert (resources[base+rank]['hit_sfx_id']^0x11111111)&0xffffffff in sfx
assert effects<=sfx
print('PASS: 40 Vegeta/Gogeta bundles, self-contained references, four-hit combos, nonempty beam particles, correct effect registrations, and Vegeta SSR/UR/LR evolution')
