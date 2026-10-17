"""Validate the saved native DB and server pool against each source identity."""
from pathlib import Path
import json,re,struct,zlib
import UnityPy
import read_plain_table as reader
from read_plain_table import write_table,read_table
from gc_bundle_manifest import read,bundle_key,hash_name
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist/kaneki-assets'
units=json.loads((ROOT/'Research/TokyoGhoul/roster-port-inventory.json').read_text())
wardrobe=json.loads((ROOT/'Research/TokyoGhoul/wardrobe-migration.json').read_text())
owners={m['old_hero']:m['hero'] for m in wardrobe['migrations']}
classes={'DB_skin_base':'DBSkinBaseRow','DB_hero_base':'DBHeroBaseRow','DB_hero_job_group':'DBHeroJobGroupRow','DB_skin_skill':'DBSkinSkillRow','DB_skill_passive':'DBSkillPassiveRow','DB_skin_exclusive_passive':'DBSkinExclusivePassiveRow','DB_skill_card_base':'DBSkillCardBaseRow','DB_skill_card_resource':'DBSkillCardResourceRow','DB_skill_card_option':'DBSkillCardOptionRow','DB_gamble_display':'DBGambleDisplayRow','DB_gamble_group':'DBGambleGroupRow','DB_gamble_rating_per':'DBGambleRatingPerRow'}
env=UnityPy.load(str(ROOT/'dist/cache/b/30FF13B981773B83827E17DB9C456368'))
scratch=ROOT/'dist/tg-check';(scratch/'Research/DecodedCache').mkdir(parents=True,exist_ok=True)
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:(scratch/'Research/DecodedCache'/f'{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
old=reader.root;reader.root=scratch;tables={n:read_table(n,c) for n,c in classes.items()};reader.root=old
for n,c in classes.items():assert write_table(tables[n],c)==(scratch/f'Research/DecodedCache/{n}.bin').read_bytes()
skins={r['id']:r for r in tables['DB_skin_base']};skills={r['id']:r for r in tables['DB_skin_skill']}
dec=lambda v,key:(v^key)&0xffffffff
heroes={dec(r['id'],0x92929292):r for r in tables['DB_hero_base']}
for field in ['hero','ssr','ur','model','text','skill']:
 if all(field in u for u in units):assert len({u[field] for u in units})==len(units),field
for u in units:
 h=heroes[u['hero']]
 assert dec(h['kind'],0x92929292)==(7 if u['race']=='Ghoul' else 3),(u['source'],u['race'])
 assert 11 in h['list_array_hero_job_group']
 assert h['collaboration_name']==1300100
cards={dec(r['id'],0x65656565):r for r in tables['DB_skill_card_base']}
resources={dec(r['id'],0x11111111):r for r in tables['DB_skill_card_resource']}
passives={dec(r['id'],0x4c4c4c4c):r for r in tables['DB_skill_passive']}
exclusive={r['hero_id']:r for r in tables['DB_skin_exclusive_passive']}
manifest,_,dirs=read((OUT/'br-m.bin').read_bytes());base='assets/sevensins/patchresources/'
for u in units:
 for sid in [u['ssr'],u['ur']]:
  assert skins[sid]['matching_hero_id']==owners.get(u['hero'],u['hero']) and skins[sid]['skin_portrait_base']==u['model']+'_0001'
  ids=[skills[sid][k] for k in ['skill_a_1_id','skill_a_2_id','skill_a_3_id','skill_b_1_id','skill_b_2_id','skill_b_3_id','special_id_1']]
  assert len(set(ids))==7
  for id in ids:
   assert id in cards and id in resources
   assert resources[id]['icon']==('icon_monster_special' if id==u['skill_base']+90 else 'icon_monster_special' if cards[id]['range_type']==2 else 'icon_monster_single_attack')
  for suffix in ['_s','_l','_card']:
   folder='costume' if suffix!='_card' else 'skillactive/hero'
   name=f'icon_hero_{u["model"]}_0001{suffix}.png'
   assert hash_name(name) in dirs[base][hash_name('ui/image/icon/'+folder+'/')]
 for j in [1,2,3]:
  pid=exclusive[u['hero']][f'exclusive_passive_id_{j}'];p=passives[pid]
  assert p['exclusive_type']=='normal' and p['list_array_apply_contents']==[1]
  assert dec(p['max_stack'],0x4c4c4c4c) in [1,3]
  value=struct.unpack('<f',struct.pack('<I',dec(p['effect_value'],0x4c4c4c4c)))[0]
  assert 0<value<=40 and value*dec(p['max_stack'],0x4c4c4c4c)<=40
centipede=passives[exclusive[2995001]['exclusive_passive_id_1']]
assert centipede['target']=='global_ally' and dec(centipede['kind_target'],0x4c4c4c4c)==7
assert struct.unpack('<f',struct.pack('<I',dec(centipede['effect_value'],0x4c4c4c4c)))[0]==40
banners={r['id']:r for r in tables['DB_gamble_display']};assert {20,65,109,990}.issubset(banners)
assert banners[990]['event_gacha_end'].startswith('9999')
pool=[r for r in tables['DB_gamble_group'] if r['gamble_group']==9900]
wardrobe=ROOT/'Research/TokyoGhoul/wardrobe-migration.json'
kept=set(json.loads(wardrobe.read_text())['kept']) if wardrobe.exists() else {u['source'] for u in units}
assert {r['skin_id'] for r in pool if skins[r['skin_id']]['rating']==5}=={u['ssr'] for u in units if u['source'] in kept}
assert {skins[r['skin_id']]['rating'] for r in pool}=={3,4,5}
header=(ROOT/'Server/Protocol/LocalGachaCatalog.h').read_text();rows=[tuple(map(int,m)) for m in re.findall(r'\{(9900),(\d+),(\d+),(\d+),(\d+)\}',header)]
assert {r[1] for r in rows}=={r['skin_id'] for r in pool}
total=sum(r[2] for r in rows);rate=sum(r[2] for r in rows if skins[r[1]]['rating']==5)/total
assert abs(rate-.08)<1e-10
crc=zlib.crc32(b''.join(f.save() for f in env.file.files.values()));assert struct.unpack_from('<I',(ROOT/'dist/cache/br-b.bin').read_bytes(),12)[0]==crc
for key,module in [('br-enu.bin','enu')]:
 m,_,ds=read((OUT/module/key).read_bytes());dirhash=hash_name('ui/image/gachabackground/gachabackground_en/');filehash=hash_name('bg_banner_gacha_tg_original.png')
 entry=m[ds[base][dirhash][filehash]];assert (OUT/module/entry['name']).exists() and entry['flags']==0
print(f'PASS: {len(units)} source forms, {len(units)*2} SSR/UR registrations, {len(units)*7} cards, {len(units)*3} capped passive effects, distinct races/Tokyo Ghoul characteristic, native icon lookups, fourth banner with 8% SSR and preserved original banners')
