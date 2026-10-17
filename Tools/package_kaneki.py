"""Register a separate SSR/UR Centipede Kaneki test unit and native cards."""
import json,struct,zlib,runpy,re,sqlite3
from pathlib import Path
from copy import deepcopy
import UnityPy
import read_plain_table as reader
from read_plain_table import root,read_table,write_table
from gc_bundle_manifest import read,write

HERO,SSR,UR,GROUP=2995001,399501,399502,204
BODY,HEAD,WEAPON,COIN=3399501,4999501,899501,499905
classes={'DB_skin_base':'DBSkinBaseRow','DB_hero_base':'DBHeroBaseRow','DB_skin_skill':'DBSkinSkillRow','DB_item_info':'DBItemInfoRow','DB_costume_base':'DBCostumeBaseRow','DB_skin_costume_resource':'DBSkinCostumeResourceRow','DB_head_costume_resource':'DBHeadCostumeResourceRow','DB_weapon_costume_resource':'DBWeaponCostumeResourceRow','DB_skin_evolution':'DBSkinEvolutionRow','DB_skin_awaken_resource':'DBSkinAwakenResourceRow','DB_skin_skill_levelup':'DBSkinSkillLevelupRow','DB_skin_transcend':'DBSkinTranscendRow','DB_skin_exceed':'DBSkinExceedRow','DB_skill_card_base':'DBSkillCardBaseRow','DB_skill_card_resource':'DBSkillCardResourceRow'}
target=root/'dist/cache/b/30FF13B981773B83827E17DB9C456368';env=UnityPy.load(str(target))
scratch=root/'dist/kaneki-table-read';(scratch/'Research/DecodedCache').mkdir(parents=True,exist_ok=True)
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:(scratch/'Research/DecodedCache'/f'{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
oldroot=reader.root;reader.root=scratch;tables={n:read_table(n,c) for n,c in classes.items()};reader.root=oldroot
def signed(n):return n-0x100000000 if n>=0x80000000 else n
def enc(n,xor=0x92929292):return signed((n^xor)&0xffffffff)
def fenc(n):return enc(struct.unpack('<I',struct.pack('<f',n))[0],0x65656565)
def put(n,row,key='id'):
 a=tables[n];a[:]=[x for x in a if x[key]!=row[key]];a.append(row)
def source(n,id,key='id'):return deepcopy(next(x for x in tables[n] if x[key]==id))
def rules(n,key,old,new):
 a=tables[n];a[:]=[x for x in a if x[key]!=new];rows=[deepcopy(x) for x in a if x[key]==old];assert rows,n
 start=max(x['id'] for x in a)+1
 for i,x in enumerate(rows):x.update(id=start+i);x[key]=new;a.append(x)
for sid,old,rating in [(SSR,399401,5),(UR,399402,6)]:
 x=source('DB_skin_base',old);x.update(id=sid,base_skin_costume_id=BODY,base_head_costume_id=HEAD,base_weapon_costume_id=WEAPON,skin_portrait_base='kaneki_centipede_0001',sort=9904,category_group=HERO,matching_hero_id=HERO,hero_coin=COIN,rating=rating);put('DB_skin_base',x)
 x=source('DB_item_info',old,'item_id');x.update(item_id=sid,item_icon='icon_skin_kaneki_centipede_0001_s',item_name=990001,item_nickname=990002,item_description=990003);put('DB_item_info',x,'item_id')
 x=source('DB_skin_skill',old);x['id']=sid
 for rank in range(1,4):x[f'skill_a_{rank}_id']=990100+rank;x[f'skill_b_{rank}_id']=990110+rank
 for rank in range(1,7):x[f'special_id_{rank}']=990190
 put('DB_skin_skill',x)
hero=source('DB_hero_base',enc(2994001));hero.update(id=enc(HERO),hero_list=enc(504),hero_group=enc(GROUP),base_skin=enc(SSR),hero_category='Normal',hero_special=990001,hero_height='169cm',hero_weight='55kg',hero_age=-1,hero_birth=-1,hero_voice=-1);put('DB_hero_base',hero)
for id,old in [(HERO,2994001),(COIN,499904)]:
 x=source('DB_item_info',old,'item_id');x.update(item_id=id,item_icon='icon_hero_kaneki_centipede_0001_s',item_name=990001,item_nickname=990002,item_description=990003);put('DB_item_info',x,'item_id')
for n,new,old,typ in [('DB_skin_costume_resource',BODY,3399401,1),('DB_head_costume_resource',HEAD,4999401,3),('DB_weapon_costume_resource',WEAPON,899401,2)]:
 x=source(n,old);x.update(id=new,character_base='kaneki_centipede')
 if typ==1:x.update(resource_body='hero_kaneki_centipede_body_0001',resource_base_head='hero_kaneki_centipede_head_0001',portrait_base='kaneki_centipede_0001',model_scale=1.0,gacha_model_scale=1.0)
 if typ==3:x.update(resource_head='hero_kaneki_centipede_head_0001',error_check_head_resource='hero_kaneki_centipede_head_0001')
 put(n,x)
 x=source('DB_costume_base',old);x.update(id=new,costume_name=990002,hero_group=GROUP,costume_group=typ*10000000+GROUP*10000+100,list_array_matching_hero_id=[HERO],list_array_costume_hide_hero_id=[HERO]);put('DB_costume_base',x)
 x=source('DB_item_info',old,'item_id');x.update(item_id=new,item_name=990002,item_icon='icon_hero_kaneki_centipede_0001_s');put('DB_item_info',x,'item_id')
for n,key in [('DB_skin_evolution','matching_hero_id'),('DB_skin_awaken_resource','hero_id'),('DB_skin_skill_levelup','hero_id'),('DB_skin_transcend','hero_id'),('DB_skin_exceed','hero_id')]:rules(n,key,2994001,HERO)
# Basic test kit: source active skill rank multipliers; a second ranked strike
# and a non-cinematic ultimate. Advanced BTC Collapse passives are not ported.
for old,new,mult,title,folder in [(202101,990101,170,990011,'skill_01'),(202102,990102,240,990011,'skill_01'),(202103,990103,420,990011,'skill_01'),(202111,990111,180,990012,'skill_02'),(202112,990112,270,990012,'skill_02'),(202113,990113,400,990012,'skill_02'),(202190,990190,600,990013,'skill_02')]:
 x=source('DB_skill_card_base',enc(old,0x65656565));x.update(id=enc(new,0x65656565),skill_name=title,skill_explain=title+10,attack_type=1,range_type=1,atk_per=fenc(mult),atk_per_add=fenc(0),list_array_buff_id_list=[],list_array_option_id_list=[]);put('DB_skill_card_base',x)
 x=source('DB_skill_card_resource',enc(old,0x11111111));x.update(id=enc(new,0x11111111),skill_folder=folder,icon='icon_hero_kaneki_centipede_0001_card',cut_in_special='',list_array_special_end_sfx_id=[],special_end_ani=0,special_end_ui_sfx='',special_end_sound_id=enc(0,0x11111111),skill_final_end_sound_id=enc(0,0x11111111),skill_final_end_sfx_id=enc(0,0x11111111),last_hit_sfx_id=enc(0,0x11111111),post_effect_type=enc(0,0x11111111));put('DB_skill_card_resource',x)
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));manifest=root/'dist/cache/br-b.bin';b=bytearray(manifest.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));manifest.write_bytes(b)
for n,c in classes.items():(root/f'Research/DecodedCache/{n}.kaneki.offline.json').write_text(json.dumps(tables[n],indent=2))
(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2));(root/'Research/DecodedCache/items.json').write_text(json.dumps(tables['DB_item_info'],indent=2))
f=root/'Server/Protocol/LocalGachaCatalog.h';s=f.read_text();start=s.index('inline const Skin Skins[] = {');end=s.index('\n};',start);s=s[:start]+'inline const Skin Skins[] = {\n'+''.join('{%d,%d,%d},\n'%(r['id'],r['matching_hero_id'],r['rating']) for r in tables['DB_skin_base'])+s[end:];f.write_text(s)
runpy.run_path(str(root/'Tools/build_development_catalog.py'),run_name='__main__');runpy.run_path(str(root/'Tools/build_material_catalog.py'),run_name='__main__')
for filename,names in [('LocalEconomyCatalog.h',['EconomyCosts','SuperAwakeningCosts']),('LocalSystemsCatalog.h',['TrueAwakeningRecipeRows'])]:
 f=root/'Server/Protocol'/filename;s=f.read_text()
 for name in names:
  a=s.index(name+'[]');b=s.index('\n};',a);section=s[a:b];pos=1 if name=='EconomyCosts' else 0
  section='\n'.join(l for l in section.splitlines() if not(l.startswith('{') and int(l[1:].split(',')[pos])==HERO))
  for l in list(section.splitlines()):
   if l.startswith('{'):
    p=l[1:].split(',')
    if int(p[pos])==2994001:p[pos]=str(HERO);section+='\n{'+','.join(p)
  s=s[:a]+section+s[b:]
 f.write_text(s)
f=root/'Server/Protocol/LocalEconomyCatalog.h';s=f.read_text();a=s.index('inline const HeroCoin HeroCoins[]');b=s.index('\n};',a)
for sid in [SSR,UR]:
 if '{%d,'%sid not in s[a:b]:s=s[:b]+'\n{%d,%d},'%(sid,COIN)+s[b:];b=s.index('\n};',a)
f.write_text(s)
f=root/'Server/Protocol/LocalCosmeticCatalog.h';s=f.read_text();a=s.index('\n};')
for new,typ in [(BODY,1),(HEAD,3),(WEAPON,2)]:
 if '{%d,'%new not in s:s=s[:a]+'\n{%d,%d,%d,%d},'%(new,typ,GROUP,typ*10000000+GROUP*10000+100)+s[a:];a=s.index('\n};')
f.write_text(s)
# English names are encrypted with the exact native localization transform.
path=root/'Research/PhoneAssets/bm/enl/ED820E4A95A79685C0E32459145857D3';raw=path.read_bytes();lang=UnityPy.load(raw[raw.find(b'UnityFS',30):]);obj=next(o for o in lang.objects if o.type.name=='TextAsset');text=obj.read();db=root/'dist/kaneki-assets/English.sqlite';db.write_bytes(text.m_Script.encode('utf8','surrogateescape'));con=sqlite3.connect(db)
strings={990001:'Ken Kaneki',990002:'Centipede',990003:'Tokyo Ghoul: Break the Chains crossover test unit.',990011:'Kagune Strike',990012:'Centipede Assault',990013:'Centipede Rampage',990021:'Inflicts damage equal to {melee_val} of Attack on one enemy.',990022:'Inflicts damage equal to {melee_val} of Attack on one enemy.',990023:'Inflicts damage equal to {melee_val} of Attack on one enemy.'}
def encrypt(s):
 key='NetmarbleFun&Cherry';n=len(s);s=''.join(chr(ord(c)^ord(key[(i+1)*n%len(key)])) for i,c in enumerate(s));return s.replace('\\','\\\\').replace('\0','\\0').replace('\n','\\n')
for id,value in strings.items():con.execute('delete from TRANSLATION where si=?',(id,));con.execute('insert into TRANSLATION values(?,?,?)',(f'Phoenix_Kaneki_{id}',id,encrypt(value)))
con.commit();con.close();text.m_Script=db.read_bytes().decode('utf8','surrogateescape');text.save();out=root/'dist/kaneki-assets/enl';out.mkdir(exist_ok=True);(out/path.name).write_bytes(lang.file.save(packer='lz4'));v=read((root/'Research/PhoneAssets/bm/br-enl.bin').read_bytes());r=next(r for r in v[0].values() if r['name']==path.name);r['crc']=zlib.crc32(b''.join(f.save() for f in lang.file.files.values()));r['flags']=0;r['size']=3;(out/'br-enl.bin').write_bytes(write(*v))
(root/'dist/kaneki-unit.json').write_text(json.dumps(dict(hero=HERO,ssr=SSR,ur=UR,model='kaneki_centipede',cards=[990101,990111,990190],status='awaiting_client_runtime_test'),indent=2))
print('Registered Centipede Kaneki SSR/UR, separate cards, growth, costumes and English text')
