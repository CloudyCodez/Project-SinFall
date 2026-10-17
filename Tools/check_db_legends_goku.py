"""Check Goku's runtime asset references and native evolution registration."""
from pathlib import Path
import json,zlib
import UnityPy
from gc_bundle_manifest import read,bundle_key,hash_name
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/kaneki-assets'
bundles,_,dirs=read((OUT/'br-m.bin').read_bytes());rows=json.loads((OUT/'assets.json').read_text());selected=[r for r in rows if r['logical'].startswith(('phoenix_dbl_goku_','phoenix_dbl_vfx_'))]
assert len(selected)==28,len(selected)
identities=set();effects=set()
for r in selected:
    e=UnityPy.load((OUT/r['file']).read_bytes());objects=e.assets[0].objects
    for filename in e.file.files:assert filename not in identities;identities.add(filename)
    for path in r['paths']:
        base='assets/sevensins/patchresources/';d,f=path[len(base):].rsplit('/',1);assert dirs[base][hash_name(d+'/')][hash_name(f)]==bundle_key(r['file'])
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
            if parent_go['m_Name']=='g_C_Head' and ('face' in child_go['m_Name'].lower() or 'hair' in child_go['m_Name'].lower()):
                assert all(abs(v)<1e-6 for v in t['m_LocalPosition'].values()),(r['logical'],'duplicate head rest offset')
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
            effects.update(x['intParameter'] for x in t['m_Events'] if x['functionName']=='OnAnimationEffect' and 198500001<=x['intParameter']<=198500004)
        if o.type.name=='ParticleSystem':assert t['playOnAwake'] and not t['looping']
        if o.type.name=='MonoScript':assert o.read().m_ClassName=='container_of_using_bones'
assert effects=={198500001,198500002,198500004},effects
def table(n):return json.loads((ROOT/'Research/DecodedCache'/f'{n}.tg.offline.json').read_text())
skins=[x for x in table('DB_skin_base') if x['matching_hero_id']==2997001]
cards={(x['id']^0x65656565)&0xffffffff:x for x in table('DB_skill_card_base')}
resources={(x['id']^0x11111111)&0xffffffff:x for x in table('DB_skill_card_resource')}
for form in range(3):
    base=14000100+form*100
    for rank in range(1,4):
        assert cards[base+rank]['target']==2
        assert cards[base+10+rank]['target']==4
    assert cards[base+90]['target']==4
    assert resources[base+90]['skill_folder']=='skill_03'
assert {x['skin_awaken_count'] for x in table('DB_skin_awaken_stat') if x['hero_id']==2997001}==set(range(1,7))
assert [(x['id'],x['rating']) for x in skins]==[(399901,5),(399902,6),(399903,7)]
assert all(x['hero_coin']==498999 for x in skins)
assert {x['id'] for x in table('DB_skin_ani') if x['id'] in [399901,399902,399903]}=={399901,399902,399903}
for model in ['goku_base','goku_blue','goku_ui']:
    for directory,name in [('ani/weapon_glove/_common','evolution_cam'),('ani/weapon_glove/_common','idle_start'),('ani/weapon_glove/_common','idle_start_02'),('ani/story','story_idle')]:
        folder=f'character/hero_{model}/{directory}/'
        assert hash_name(name+'.anim') in dirs['assets/sevensins/patchresources/'][hash_name(folder)],(model,name)
assert {x['evolution_rating'] for x in table('DB_skin_evolution') if x['matching_hero_id']==2997001}>={5,6}
assert {x['id'] for x in table('DB_sfx') if x['path']=='DragonBall/goku'}=={198500001,198500002,198500003,198500004}
assert '{1,2997001,6,0,' in (ROOT/'Server/Protocol/LocalEconomyCatalog.h').read_text()
print('PASS: 28 Goku bundles, awakening stats, AoE targets, four-hit combo, growth/evolution presentation, local object references, native effect events, SSR/UR/LR progression and LR server costs')
