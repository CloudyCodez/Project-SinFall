"""Player adapters for native Demon King Meliodas and Indura boss models/cards."""
import json,struct,zlib,re,runpy
from copy import deepcopy
from read_plain_table import root,read_table,write_table
import UnityPy
specs=[('demon_king_meliodas',3089019,315501,315502,2991001,399101,200),('monspeet_indura',3030067,315001,315002,2992001,399201,201),('derieri_indura',3030068,320001,320002,2993001,399301,202),('meliodas_berserker',2040101,300102,300103,2994001,399401,203)]
classes={'DB_skin_base':'DBSkinBaseRow','DB_hero_base':'DBHeroBaseRow','DB_skin_skill':'DBSkinSkillRow','DB_item_info':'DBItemInfoRow','DB_costume_base':'DBCostumeBaseRow','DB_skin_costume_resource':'DBSkinCostumeResourceRow','DB_head_costume_resource':'DBHeadCostumeResourceRow','DB_weapon_costume_resource':'DBWeaponCostumeResourceRow','DB_skin_evolution':'DBSkinEvolutionRow','DB_skin_awaken_resource':'DBSkinAwakenResourceRow','DB_skin_skill_levelup':'DBSkinSkillLevelupRow','DB_skin_transcend':'DBSkinTranscendRow','DB_skin_exceed':'DBSkinExceedRow'}
tables={n:read_table(n,c) for n,c in classes.items()}
# Read existing packaged tables without altering the preserved originals.
import read_plain_table as reader
saved_root=reader.root
scratch=root/'dist/boss-table-read';(scratch/'Research/DecodedCache').mkdir(parents=True,exist_ok=True)
target=root/'dist/cache/b/30FF13B981773B83827E17DB9C456368';env=UnityPy.load(str(target))
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:(scratch/'Research/DecodedCache'/f'{a.m_Name}.bin').write_bytes(a.m_Script.encode('utf8','surrogateescape'))
reader.root=scratch
for n,c in classes.items():tables[n]=read_table(n,c)
reader.root=saved_root
base_items={x['item_id']:x for x in tables['DB_item_info']};resources={((x['id']^0x50505050)&0xffffffff):x for x in read_table('DB_monster_resource','DBMonsterResourceRow')};mcards={((x['id']^0x66666666)&0xffffffff):x for x in read_table('DB_monster_skill','DBMonsterSkillRow')}
enc=lambda n: ((n^0x92929292)&0xffffffff)-(0x100000000 if ((n^0x92929292)&0xffffffff)>=0x80000000 else 0)
flt=lambda n:struct.unpack('<f',struct.pack('<I',(n^0x50505050)&0xffffffff))[0]
def put(name,row,key='id'):
 rows=tables[name];existing=next((x for x in rows if x[key]==row[key]),None)
 if existing:existing.clear();existing.update(row)
 else:rows.append(row)
def clone_hero_rules(name,key,old,new):
 rows=tables[name];sources=[deepcopy(x) for x in rows if x[key]==old];assert sources,(name,old)
 rows[:]=[x for x in rows if x[key]!=new];nextid=max(x['id'] for x in rows)+1
 for i,x in enumerate(sources):x['id']=nextid+i;x[key]=new;rows.append(x)
normal=json.loads((root/'Research/DecodedCache/DB_coin_shop.offline.json').read_text());events=json.loads((root/'Research/DecodedCache/DB_coin_shop_event.offline.json').read_text());shop_template=deepcopy(next(x for x in events if x['price_coin_item_type']=='herocoin'))
report=[]
for index,(model,mid,ssr,ur,hid,sid,group) in enumerate(specs):
 src=next(x for x in tables['DB_skin_base'] if x['id']==ssr);sourcehero=src['matching_hero_id'];monster=resources[mid];card=mcards[mid];bossitem=base_items[mid]
 bodyid=3399101+index*100;headid=4999101+index*100;weaponid=899101+index*100;coinid=499901+index
 for old,newsid,rating in [(ssr,sid,5),(ur,sid+1,6)]:
  x=deepcopy(next(x for x in tables['DB_skin_base'] if x['id']==old));x.update(id=newsid,base_skin_costume_id=bodyid,base_head_costume_id=headid,base_weapon_costume_id=weaponid,skin_portrait_base=src['skin_portrait_base'],skin_category=1,skin_display=1,sort=9900+index,category_group=hid,matching_hero_id=hid,hero_coin=coinid,hero_coin_count=1,start_rating=5,rating=rating,change_hero_skin_id=0,before_change_hero_skin_id=0,change_effect_id=0,after_change_hero_model=0,costume_combination=0,weapon_hide_display=1,costume_set_count='1/1/1/1');put('DB_skin_base',x)
  skills=deepcopy(next(x for x in tables['DB_skin_skill'] if x['id']==old));skills['id']=newsid
  for key in ['skill_a_1_id','skill_a_2_id','skill_a_3_id','skill_b_1_id','skill_b_2_id','skill_b_3_id']:skills[key]=(card[key]^0x66666666)&0xffffffff;assert skills[key]>0
  skills.update(skill_a_draw_per=50,skill_b_draw_per=50,ability_id=0,skill_etc_id=0,counter_attack_1_id=0,counter_attack_2_id=0,counter_attack_3_id=0)
  for i in range(1,7):skills[f'special_id_{i}']=(card['special_id']^0x66666666)&0xffffffff
  put('DB_skin_skill',skills)
  item=deepcopy(base_items[old]);item.update(item_id=newsid,item_name=bossitem['item_name'],item_nickname=bossitem['item_nickname'],item_description=bossitem['item_description'],item_icon=base_items[ssr]['item_icon'],item_rating=rating);put('DB_item_info',item,'item_id')
 hero=deepcopy(next(x for x in tables['DB_hero_base'] if ((x['id']^0x92929292)&0xffffffff)==sourcehero));hero.update(id=enc(hid),hero_list=enc(500+index),hero_group=enc(group),hero_display=enc(1),hero_wanted_display=1,base_skin=enc(sid),npc_type=enc(0),weapon_idle_start=enc(0),weapon_hide_active=1,list_array_hero_group_check=[],list_array_sub_hero_group=[],hero_category='Normal',main_hero_type='main',hero_special=bossitem['item_name'],hero_coop_main=-1,hero_coop_sub=-1)
 for i in range(1,11):hero[f'hero_action_{i}']=enc(0)
 put('DB_hero_base',hero)
 heroitem=deepcopy(base_items[sourcehero]);heroitem.update(item_id=hid,item_name=bossitem['item_name'],item_nickname=bossitem['item_nickname'],item_description=bossitem['item_description'],item_icon=base_items[sourcehero]['item_icon']);put('DB_item_info',heroitem,'item_id')
 coin=deepcopy(base_items[src['hero_coin']]);coin.update(item_id=coinid,item_name=bossitem['item_name'],item_nickname=-1,item_rating=5,item_icon=base_items[src['hero_coin']]['item_icon']);put('DB_item_info',coin,'item_id')
 costume=deepcopy(next(x for x in tables['DB_skin_costume_resource'] if x['id']==src['base_skin_costume_id']));costume.update(id=bodyid,character_base=model,resource_body=monster['resource_body'],replace_resource_body='',change_head=0,resource_base_head=monster['resource_head'],base_head_helm_mixer_name='',list_array_weapon_attach_dummy=[],list_array_weapon_combi_attach_dummy=[],ani_directory_name=monster['ani_directory_name'],enable_special_sfx=0,model_scale=1.0,gacha_model_scale=1.0,sfx_scale=1.0,portrait_base=src['skin_portrait_base'],check_size='normal',victory_prop='');put('DB_skin_costume_resource',costume)
 head=deepcopy(tables['DB_head_costume_resource'][0]);head.update(id=headid,character_base=model,resource_head=monster['resource_head'],error_check_head_resource=monster['resource_head'],head_mixer_name='',head_attach_dummy=0);put('DB_head_costume_resource',head)
 weapon=deepcopy(tables['DB_weapon_costume_resource'][0]);weapon.update(id=weaponid,character_base=model,resource_weapon='0',weapon_model_type=0);put('DB_weapon_costume_resource',weapon)
 for old,new,typ in [(src['base_skin_costume_id'],bodyid,1),(src['base_weapon_costume_id'],weaponid,2),(src['base_head_costume_id'],headid,3)]:
  x=deepcopy(next(x for x in tables['DB_costume_base'] if x['id']==old));x.update(id=new,costume_name=bossitem['item_name'],list_array_costume_hide_hero_id=[hid],list_array_matching_hero_id=[hid],hero_group=group,costume_group=typ*10000000+group*10000+100,costume_type=typ,costume_combination=0,passive_id=0,list_array_add_passive_id=[]);put('DB_costume_base',x)
  item=deepcopy(base_items[old]);item.update(item_id=new,item_name=bossitem['item_name'],item_icon=base_items[ssr]['item_icon']);put('DB_item_info',item,'item_id')
 for n,key in [('DB_skin_evolution','matching_hero_id'),('DB_skin_awaken_resource','hero_id'),('DB_skin_skill_levelup','hero_id'),('DB_skin_transcend','hero_id'),('DB_skin_exceed','hero_id')]:clone_hero_rules(n,key,sourcehero,hid)
 events[:]=[x for x in events if x['product_id'] not in [sid,sid+1]];normal[:]=[x for x in normal if x['product_id'] not in [sid,sid+1]]
 product=deepcopy(shop_template);product.update(id=52001+index,product_id=sid,product_count=1,product_free_count=0,product_category=1,price_coin_item_type='herocoin',price_coin_type=4,price_count=30,skin_discount=30,buy_limited_count=0,period_buy_limited_count=0,period_buy_limited_type=0,buy_limited_start='',buy_limited_end='');events.append(product)
 report.append(dict(model=model,source_monster=mid,hero=hid,skin_ssr=sid,skin_ur=sid+1,body=bodyid,head=headid,weapon=weaponid,coin=coinid,price_sr_coins=30,skills={k:skills[k] for k in ['skill_a_1_id','skill_a_2_id','skill_a_3_id','skill_b_1_id','skill_b_2_id','skill_b_3_id','special_id_1']}))
for n,c in classes.items():
 (root/f'Research/DecodedCache/{n}.boss.offline.json').write_text(json.dumps(tables[n],indent=2))
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));env=UnityPy.load(str(target));checked={o.read().m_Name:o.read().m_Script for o in env.objects if o.type.name=='TextAsset'}
for n,c in classes.items():assert checked[n].encode('utf8','surrogateescape')==write_table(tables[n],c)
manifest=root/'dist/cache/br-b.bin';b=bytearray(manifest.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));manifest.write_bytes(b)
(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2));(root/'Research/DecodedCache/items.json').write_text(json.dumps(tables['DB_item_info'],indent=2));(root/'Research/DecodedCache/DB_coin_shop.offline.json').write_text(json.dumps(normal,indent=2));(root/'Research/DecodedCache/DB_coin_shop_event.offline.json').write_text(json.dumps(events,indent=2))
# Extend server lookup tables while retaining the existing summon pools and event stages.
f=root/'Server/Protocol/LocalGachaCatalog.h';s=f.read_text();start=s.index('inline const Skin Skins[] = {');end=s.index('\n};',start);s=s[:start]+'inline const Skin Skins[] = {\n'+''.join('{%d,%d,%d},\n'%(r['id'],r['matching_hero_id'],r['rating']) for r in tables['DB_skin_base'])+s[end:];f.write_text(s)
runpy.run_path(str(root/'Tools/build_development_catalog.py'),run_name='__main__');runpy.run_path(str(root/'Tools/build_material_catalog.py'),run_name='__main__')
# Native growth recipes copied only for these new heroes, leave all other restoration catalogs intact.
f=root/'Server/Protocol/LocalEconomyCatalog.h';s=f.read_text()
for name,key in [('EconomyCosts','hero'),('SuperAwakeningCosts','hero')]:
 a=s.index(' '+name+'[]={') if ' '+name+'[]={' in s else s.index(' '+name+'[] = {');b=s.index('\n};',a);section=s[a:b]
 section='\n'.join(line for line in section.splitlines() if not (line.startswith('{') and int(line[1:].split(',')[1 if name=='EconomyCosts' else 0]) in {x[4] for x in specs}))
 for _,_,ssr,_,hid,_,_ in specs:
  old=next(x for x in tables['DB_skin_base'] if x['id']==ssr)['matching_hero_id'];rows=[]
  for line in section.splitlines():
   if not line.startswith('{'):continue
   parts=line[1:].split(',');pos=1 if name=='EconomyCosts' else 0
   if int(parts[pos])==old and not (name=='EconomyCosts' and int(parts[0])==2):
    parts[pos]=str(hid);rows.append('{'+','.join(parts))
  section+='\n'+'\n'.join(rows)
 if name=='EconomyCosts':
  for r in report:
   skin=next(x for x in tables['DB_skin_base'] if x['id']==r['skin_ssr'])
   for rule in read_table('DB_evolution_break_base','DBEvolutionBreakBaseRow'):
    if rule['start_rating']!=skin['start_rating'] or rule['evolution_break_attribute']!=skin['attribute']:continue
    pairs=[(rule['evolution_break_key_id'],rule['evolution_break_key_count'])]+[(rule[f'evolution_break_material_id_{j}'],rule[f'evolution_break_material_count_{j}']) for j in range(1,4)]+[(rule['evolution_break_price_id'],rule['evolution_break_price_count'])]
    pairs=[(i,n) for i,n in pairs if i>0 and n>0];pairs+=[(0,0)]*(5-len(pairs))
    section+='\n{2,%d,%d,0,{%s},{%s}},'%(r['hero'],rule['evolution_break_step'],','.join(str(x[0]) for x in pairs),','.join(str(x[1]) for x in pairs))
 s=s[:a]+section+s[b:]
s='\n'.join(line for line in s.splitlines() if not any(line.startswith('{'+str(x[5])+',') or line.startswith('{'+str(x[5]+1)+',') for x in specs))+'\n'
a=s.index('inline const HeroCoin HeroCoins[]');b=s.index('\n};',a);s=s[:b]+''.join('\n{%d,%d},'%(r['skin_ssr'],r['coin'])+'\n{%d,%d},'%(r['skin_ur'],r['coin']) for r in report)+s[b:];f.write_text(s)
f=root/'Server/Protocol/LocalCosmeticCatalog.h';s=f.read_text();ids={r[k] for r in report for k in ['body','head','weapon']};s='\n'.join(line for line in s.splitlines() if not (line.strip().startswith('{') and int(line.strip()[1:].split(',')[0]) in ids))+'\n';a=s.index('\n};');s=s[:a]+''.join('\n{%d,%d,%d,%d},'%(x['id'],x['costume_type'],x['hero_group'],x['costume_group']) for x in tables['DB_costume_base'] if x['hero_group'] in [200,201,202,203])+s[a:];f.write_text(s)
f=root/'Server/Protocol/LocalSystemsCatalog.h';s=f.read_text();a=s.index('TrueAwakeningRecipeRows[]');b=s.index('\n};',a);section=s[a:b]
section='\n'.join(line for line in section.splitlines() if not (line.startswith('{') and int(line[1:].split(',')[0]) in {x[4] for x in specs}))
for _,_,ssr,_,hid,_,_ in specs:
 old=next(x for x in tables['DB_skin_base'] if x['id']==ssr)['matching_hero_id']
 for line in list(section.splitlines()):
  if line.startswith('{'+str(old)+','):section+='\n{'+str(hid)+line[len(str(old))+1:]
s=s[:a]+section+s[b:];f.write_text(s)
runpy.run_path(str(root/'Tools/refine_coin_shop.py'),run_name='__main__');runpy.run_path(str(root/'Tools/restore_coin_shop.py'),run_name='__main__')
(root/'dist/playable-story-bosses.json').write_text(json.dumps(report,indent=2));print('Player adapters:',report)
