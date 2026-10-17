"""Add playable BTC variants, native finite passives and an original summon pool.

Reads the current restored DB, so rerunning never resets restored content.
"""
import json,struct,zlib,runpy,re,sqlite3,math
from pathlib import Path
from copy import deepcopy
import UnityPy
import read_plain_table as reader
from read_plain_table import root,read_table,write_table
from gc_bundle_manifest import read,write
from tg_native_kits import profile,card

units=json.loads((root/'Research/TokyoGhoul/roster-port-inventory.json').read_text())
classes={'DB_skin_base':'DBSkinBaseRow','DB_hero_base':'DBHeroBaseRow','DB_skin_skill':'DBSkinSkillRow','DB_item_info':'DBItemInfoRow','DB_costume_base':'DBCostumeBaseRow','DB_skin_costume_resource':'DBSkinCostumeResourceRow','DB_head_costume_resource':'DBHeadCostumeResourceRow','DB_weapon_costume_resource':'DBWeaponCostumeResourceRow','DB_skin_evolution':'DBSkinEvolutionRow','DB_skin_awaken_resource':'DBSkinAwakenResourceRow','DB_skin_skill_levelup':'DBSkinSkillLevelupRow','DB_skin_transcend':'DBSkinTranscendRow','DB_skin_exceed':'DBSkinExceedRow','DB_skill_card_base':'DBSkillCardBaseRow','DB_skill_card_resource':'DBSkillCardResourceRow','DB_skill_passive':'DBSkillPassiveRow','DB_skin_exclusive_passive':'DBSkinExclusivePassiveRow','DB_gamble_display':'DBGambleDisplayRow','DB_gamble_group':'DBGambleGroupRow','DB_gamble_rating_per':'DBGambleRatingPerRow'}
classes.update(DB_hero_job_group='DBHeroJobGroupRow',DB_skill_card_option='DBSkillCardOptionRow')
target=root/'dist/cache/b/30FF13B981773B83827E17DB9C456368';env=UnityPy.load(str(target))
scratch=root/'dist/tg-table-read';(scratch/'Research/DecodedCache').mkdir(parents=True,exist_ok=True)
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:(scratch/'Research/DecodedCache'/f'{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
oldroot=reader.root;reader.root=scratch;tables={n:read_table(n,c) for n,c in classes.items()};reader.root=oldroot
for n,c in classes.items():assert write_table(tables[n],c)==(scratch/f'Research/DecodedCache/{n}.bin').read_bytes(),n
def signed(n):return n-0x100000000 if n>=0x80000000 else n
def enc(n,xor=0x92929292):return signed((n^xor)&0xffffffff)
def fenc(n,xor=0x65656565):return enc(struct.unpack('<I',struct.pack('<f',n))[0],xor)
def put(n,row,key='id'):
 a=tables[n];a[:]=[x for x in a if x[key]!=row[key]];a.append(row)
def source(n,id,key='id'):return deepcopy(next(x for x in tables[n] if x[key]==id))
def rules(n,key,old,new):
 a=tables[n];a[:]=[x for x in a if x[key]!=new];rows=[deepcopy(x) for x in a if x[key]==old];assert rows,n
 start=max(x['id'] for x in a)+1
 for i,x in enumerate(rows):x.update(id=start+i);x[key]=new;a.append(x)

# Fixed bonuses are limited to self or living allies. Turn ramping uses the
# native end-turn mechanism, with at most three increments (never unlimited).
effects={
 'basic':('pass_atk_def_hp_inc_per','basic stats'),
 'atk':('pass_atk_inc_per','Attack'), 'hp':('pass_hp_inc_per','HP'),
 'def':('pass_def_inc_per','Defense'), 'crit':('pass_crit_add_per','Critical Chance'),
 'critdmg':('pass_crit_atk_add_per','Critical Damage'),
 'steal':('pass_hp_steal_add_per','Lifesteal'), 'regen':('pass_hp_regen_add_per','Regeneration Rate'),
 'reduce':('pass_get_dmg_dec_per','damage reduction'),
 'ramp':('pass_endturn_atk_inc_per','Attack'),
 'rampdef':('pass_endturn_def_inc_per','Defense'),
}
# Values are percentages; one stack for permanent bonuses, three for ramping.
profiles={u['source']:profile(u) for u in units}
assert set(profiles)=={u['source'] for u in units}
strings={1300100:'Tokyo Ghoul',1300101:'Ghoul'};passive_report=[];card_report=[]
job=deepcopy(tables['DB_hero_job_group'][0]);job.update(id=11,hero_job_group_name=1300100,sorting_number=11,list_array_hero_id=[u['hero'] for u in units],list_array_union_id=[]);put('DB_hero_job_group',job)
templates=deepcopy(tables['DB_skill_passive'])
exclusive_template=deepcopy(tables['DB_skin_exclusive_passive'][0])
for u in units:
 HERO,SSR,UR,GROUP=u['hero'],u['ssr'],u['ur'],u['group'];BODY,HEAD,WEAPON,COIN=u['body'],u['head'],u['weapon'],u['coin']
 model=u['model'];tid=u['text_base'];skill=u['skill_base']
 strings.update({tid:u['name'],tid+1:u['title'],tid+2:'Tokyo Ghoul: Break the Chains crossover.',tid+10:'Kagune Strike' if GROUP in [204,205] else 'Quinque Strike',tid+11:'Flamewing Assault' if GROUP==205 else 'Quinque Assault' if GROUP==206 else 'Kagune Assault',tid+12:u['title']+' — Unleashed',tid+20:'Inflicts damage equal to {melee_val} of Attack on one enemy.',tid+21:'Inflicts damage equal to {melee_val} of Attack on one enemy.',tid+22:'Inflicts damage equal to {melee_val} of Attack on one enemy.'})
 for sid,old,rating in [(SSR,399401,5),(UR,399402,6)]:
  x=source('DB_skin_base',old);x.update(id=sid,base_skin_costume_id=BODY,base_head_costume_id=HEAD,base_weapon_costume_id=WEAPON,skin_portrait_base=model+'_0001',sort=9904+u['index'],category_group=HERO,matching_hero_id=HERO,hero_coin=COIN,rating=rating,attribute=u['attribute']);put('DB_skin_base',x)
  x=source('DB_item_info',old,'item_id');x.update(item_id=sid,item_icon=f'icon_skin_{model}_0001_s',item_name=tid,item_nickname=tid+1,item_description=tid+2);put('DB_item_info',x,'item_id')
  x=source('DB_skin_skill',old);x['id']=sid
  for rank in range(1,4):x[f'skill_a_{rank}_id']=skill+rank;x[f'skill_b_{rank}_id']=skill+10+rank
  for rank in range(1,7):x[f'special_id_{rank}']=skill+90
  put('DB_skin_skill',x)
 hero=source('DB_hero_base',enc(2994001));hero.update(id=enc(HERO),hero_list=enc(504+u['index']),hero_group=enc(GROUP),base_skin=enc(SSR),hero_category='Normal',hero_special=tid,hero_voice=-1,kind=enc(7 if u['race']=='Ghoul' else 3),sub_kind_check=0,sub_kind=enc(0),list_array_hero_job_group=[3,11],list_array_sub_hero_group=[],list_array_hero_group_check=[],collaboration_name=1300100,collaboration_kind=1300101 if u['race']=='Ghoul' else -1);put('DB_hero_base',hero)
 for id,old in [(HERO,2994001),(COIN,499904)]:
  x=source('DB_item_info',old,'item_id');x.update(item_id=id,item_icon=f'icon_hero_{model}_0001_s',item_name=tid,item_nickname=tid+1,item_description=tid+2);put('DB_item_info',x,'item_id')
 for n,new,old,typ in [('DB_skin_costume_resource',BODY,3399401,1),('DB_head_costume_resource',HEAD,4999401,3),('DB_weapon_costume_resource',WEAPON,899401,2)]:
  x=source(n,old);x.update(id=new,character_base=model)
  if typ==1:x.update(resource_body=f'hero_{model}_body_0001',resource_base_head=f'hero_{model}_head_0001',portrait_base=model+'_0001',model_scale=1.0,gacha_model_scale=1.0)
  if typ==3:x.update(resource_head=f'hero_{model}_head_0001',error_check_head_resource=f'hero_{model}_head_0001')
  put(n,x)
  x=source('DB_costume_base',old);x.update(id=new,costume_name=tid+1,hero_group=GROUP,costume_group=typ*10000000+GROUP*10000+100,list_array_matching_hero_id=[HERO],list_array_costume_hide_hero_id=[HERO]);put('DB_costume_base',x)
  x=source('DB_item_info',old,'item_id');x.update(item_id=new,item_name=tid+1,item_icon=f'icon_hero_{model}_0001_s');put('DB_item_info',x,'item_id')
 for n,key in [('DB_skin_evolution','matching_hero_id'),('DB_skin_awaken_resource','hero_id'),('DB_skin_skill_levelup','hero_id'),('DB_skin_transcend','hero_id'),('DB_skin_exceed','hero_id')]:rules(n,key,2994001,HERO)
 for old,new,mult,title,folder in [(202101,skill+1,170,tid+10,'skill_01'),(202102,skill+2,240,tid+10,'skill_01'),(202103,skill+3,420,tid+10,'skill_01'),(202111,skill+11,180,tid+11,'skill_02'),(202112,skill+12,270,tid+11,'skill_02'),(202113,skill+13,400,tid+11,'skill_02'),(202190,skill+90,600,tid+12,'skill_02')]:
  phase=1 if new in [skill+1,skill+2,skill+3] else 2 if new in [skill+11,skill+12,skill+13] else 3
  rank=new-skill if phase==1 else new-skill-10 if phase==2 else 1
  kitcard=card(u,phase,rank,tables['DB_skill_card_option']);strings[title]=kitcard['name'];strings[title+10]=kitcard['description'];mult=kitcard['multiplier']
  card_report.append(dict(source=u['source'],id=new,phase=phase,rank=rank,**kitcard))
  x=source('DB_skill_card_base',enc(old,0x65656565));x.update(id=enc(new,0x65656565),skill_name=title,skill_explain=title+10,attack_type=1,range_type=kitcard['range'],atk_per=fenc(mult),atk_per_add=fenc(0),list_array_buff_id_list=[],list_array_option_id_list=[kitcard['option']]);put('DB_skill_card_base',x)
  x=source('DB_skill_card_resource',enc(old,0x11111111));x.update(id=enc(new,0x11111111),skill_folder=folder,icon='icon_monster_special' if phase==3 else 'icon_monster_special' if kitcard['range']==2 else 'icon_monster_single_attack',cut_in_special='',list_array_special_end_sfx_id=[],special_end_ani=0,special_end_ui_sfx='',special_end_sound_id=enc(0,0x11111111),skill_final_end_sound_id=enc(0,0x11111111),skill_final_end_sfx_id=enc(0,0x11111111),last_hit_sfx_id=enc(0,0x11111111),post_effect_type=enc(0,0x11111111));put('DB_skill_card_resource',x)
 name,kit=profiles[u['source']];descriptions=[];ids=[]
 for j,entry in enumerate(kit):
  effect,value=entry[:2];targetkind=entry[2] if len(entry)>2 else 'self';keyword,label=effects[effect];pid=980000+u['index']*10+j
  template=next(x for x in templates if x['effect_keyword']==keyword and x['target']=='self' and x['exclusive_type']=='normal' and x['list_array_apply_contents']==[1])
  # Use native ally templates where available (same targeting as base race supports).
  if targetkind!='self':
   template=next((x for x in templates if x['effect_keyword']==keyword and x['target']=='global_ally' and x['exclusive_type']=='normal' and x['list_array_apply_contents']==[1]),template)
  x=deepcopy(template);ramping=effect.startswith('ramp');cap=3 if ramping else 1
  subject={"ally":"all allies", "ghoul":"all Ghoul allies", "human":"all Human allies"}.get(targetkind,"own")
  desc=(f'Increases own {label} by {value}% at the end of each turn (up to {cap} times; maximum {value*cap}%).' if ramping else f'Reduces damage taken by '+({'ally':'all allies','ghoul':'all Ghoul allies','human':'all Human allies'}.get(targetkind,'self'))+f' by {value}%.' if effect=='reduce' else f'Increases {subject} {label} by {value}%.')
  x.update(id=enc(pid,0x4c4c4c4c),name=tid+40,explain=tid+41+j,explain_simple=-1,first_stack=enc(0 if ramping else 1,0x4c4c4c4c),max_stack=enc(cap,0x4c4c4c4c),effect_value=fenc(value,0x4c4c4c4c),effect_value_add=fenc(0,0x4c4c4c4c),target='global_ally' if targetkind!='self' else 'self',sub_invoke_passive=0 if targetkind!='self' else 1,active_text=-1,active_sfx_id=enc(0,0x4c4c4c4c),passive_sfx_id=enc(0,0x4c4c4c4c),exclusive_ani=enc(0,0x4c4c4c4c),exclusive_invisible=0,list_array_hero_target=[],list_array_kind_target=[],kind_target=enc({'ghoul':7,'human':3}.get(targetkind,0),0x4c4c4c4c),attribute_target=enc(0,0x4c4c4c4c),list_array_apply_hero_category=[],list_array_apply_hero_job_group=[],list_array_exclusive_condition_icon=[1,7])
  put('DB_skill_passive',x);strings[tid+41+j]=desc;ids.append(pid);descriptions.append(desc)
 strings[tid+40]=name
 x=deepcopy(exclusive_template);x.update(hero_id=HERO,special_level_passive=0,exclusive_passive_id_1=ids[0],exclusive_passive_id_2=ids[1],exclusive_passive_id_3=ids[2]);put('DB_skin_exclusive_passive',x,'hero_id')
 passive_report.append(dict(source=u['source'],hero=HERO,name=u['name'],form=u['title'],passive=name,effects=descriptions,ids=ids))

# Add a fourth banner, retaining the three restored banners and their pools.
BANNER,GACHA=990,9900
b=deepcopy(next(x for x in tables['DB_gamble_display'] if x['id']==20));b.update(id=BANNER,gamble_group=GACHA,gamble_BG_name='bg_banner_gacha_tg_original',event_gacha_start='2020-01-01 00:00:00',event_gacha_end='9999-12-31 23:59:59',gamble_desc=1300102)
put('DB_gamble_display',b);strings[1300102]='Tokyo Ghoul — Break the Chains: Original Crossover'
pool=[x for x in tables['DB_skin_base'] if x['id'] in {u['ssr'] for u in units}]
pool += [x for x in tables['DB_skin_base'] if x['rating'] in [3,4] and x['matching_hero_id']>0 and x['id'] in {p['skin_id'] for p in tables['DB_gamble_group'] if p['gamble_group']==120}]
counts={r:sum(x['rating']==r for x in pool) for r in [3,4,5]};assert all(counts.values())
percent={3:55,4:37,5:8};denominator=math.lcm(*(counts[r] for r in counts))*100
tables['DB_gamble_group'][:]=[x for x in tables['DB_gamble_group'] if x['gamble_group']!=GACHA]
serverpool=[]
for i,x in enumerate(pool):
 tables['DB_gamble_group'].append(dict(id=990000+i,gamble_group=GACHA,skin_id=x['id'],gamble_rate=1000,pick_up_check=0,skin_level=1,skin_awaken=0))
 serverpool.append((GACHA,x['id'],denominator*percent[x['rating']]//100//counts[x['rating']],1,0))
put('DB_gamble_rating_per',dict(id=BANNER,gamble_group=GACHA,rating_1=0,rating_2=0,rating_3=55,rating_4=37,rating_5=8))
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));manifest=root/'dist/cache/br-b.bin';b=bytearray(manifest.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));manifest.write_bytes(b)
for n,c in classes.items():(root/f'Research/DecodedCache/{n}.tg.offline.json').write_text(json.dumps(tables[n],indent=2))
(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2));(root/'Research/DecodedCache/items.json').write_text(json.dumps(tables['DB_item_info'],indent=2))
f=root/'Server/Protocol/LocalGachaCatalog.h';s=f.read_text();start=s.index('inline const Skin Skins[] = {');end=s.index('\n};',start);s=s[:start]+'inline const Skin Skins[] = {\n'+''.join('{%d,%d,%d},\n'%(r['id'],r['matching_hero_id'],r['rating']) for r in tables['DB_skin_base'])+s[end:]
start=s.index('inline const Banner Banners[]');end=s.index('\n};',start)
section='\n'.join(l for l in s[start:end].splitlines() if not l.startswith('{990,'));s=s[:start]+section+'\n{990,9900,1,11},'+s[end:]
start=s.index('inline const PoolEntry Pool[]');end=s.index('\n};',start);section='\n'.join(l for l in s[start:end].splitlines() if not l.startswith('{9900,'));s=s[:start]+section+'\n'+''.join('{%d,%d,%d,%d,%d},\n'%r for r in serverpool)+s[end:];f.write_text(s)
runpy.run_path(str(root/'Tools/build_development_catalog.py'),run_name='__main__');runpy.run_path(str(root/'Tools/build_material_catalog.py'),run_name='__main__')
for filename,names in [('LocalEconomyCatalog.h',['EconomyCosts','SuperAwakeningCosts']),('LocalSystemsCatalog.h',['TrueAwakeningRecipeRows'])]:
 f=root/'Server/Protocol'/filename;s=f.read_text()
 for name in names:
  a=s.index(name+'[]');b=s.index('\n};',a);section=s[a:b];pos=1 if name=='EconomyCosts' else 0
  section='\n'.join(l for l in section.splitlines() if not(l.startswith('{') and int(l[1:].split(',')[pos]) in {u['hero'] for u in units}))
  donors=[l for l in section.splitlines() if l.startswith('{') and int(l[1:].split(',')[pos])==2994001]
  assert donors,(filename,name)
  for u in units:
   for l in donors:
    p=l[1:].split(',');p[pos]=str(u['hero']);section+='\n{'+','.join(p)
  s=s[:a]+section+s[b:]
 f.write_text(s)
f=root/'Server/Protocol/LocalEconomyCatalog.h';s=f.read_text();a=s.index('inline const HeroCoin HeroCoins[]');b=s.index('\n};',a)
for u in units:
 for sid in [u['ssr'],u['ur']]:
  if '{%d,'%sid not in s[a:b]:s=s[:b]+'\n{%d,%d},'%(sid,u['coin'])+s[b:];b=s.index('\n};',a)
f.write_text(s)
f=root/'Server/Protocol/LocalCosmeticCatalog.h';s=f.read_text();a=s.index('\n};')
for u in units:
 for new,typ in [(u['body'],1),(u['head'],3),(u['weapon'],2)]:
  if '{%d,'%new not in s:s=s[:a]+'\n{%d,%d,%d,%d},'%(new,typ,u['group'],typ*10000000+u['group']*10000+100)+s[a:];a=s.index('\n};')
f.write_text(s)
path=root/'dist/kaneki-assets/enl/ED820E4A95A79685C0E32459145857D3';lang=UnityPy.load(str(path));obj=next(o for o in lang.objects if o.type.name=='TextAsset');text=obj.read();db=root/'dist/kaneki-assets/English.sqlite';db.write_bytes(text.m_Script.encode('utf8','surrogateescape'));con=sqlite3.connect(db)
def encrypt(s):
 key='NetmarbleFun&Cherry';n=len(s);s=''.join(chr(ord(c)^ord(key[(i+1)*n%len(key)])) for i,c in enumerate(s));return s.replace('\\','\\\\').replace('\0','\\0').replace('\n','\\n')
for id,value in strings.items():con.execute('delete from TRANSLATION where si=?',(id,));con.execute('insert into TRANSLATION values(?,?,?)',(f'Phoenix_TG_{id}',id,encrypt(value)))
con.commit();con.close();text.m_Script=db.read_bytes().decode('utf8','surrogateescape');text.save();path.write_bytes(lang.file.save(packer='lz4'));v=read((path.parent/'br-enl.bin').read_bytes());r=next(r for r in v[0].values() if r['name']==path.name);r['crc']=zlib.crc32(b''.join(f.save() for f in lang.file.files.values()));r['flags']=0;r['size']=3;(path.parent/'br-enl.bin').write_bytes(write(*v))
(root/'dist/tg-roster-cards.json').write_text(json.dumps(card_report,indent=2))
(root/'dist/tg-roster-passives.json').write_text(json.dumps(passive_report,indent=2))
(root/'dist/tg-banner.json').write_text(json.dumps(dict(banner=BANNER,group=GACHA,rarity_rates=percent,units=units),indent=2))
print('Registered',len(units),'SSR/UR forms,',len(passive_report)*3,'finite native passive effects and TG original banner')
