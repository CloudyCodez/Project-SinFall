"""Register obtainable Black SSR/UR and his battle-only Rosé transformation."""
from pathlib import Path
helper=Path(__file__).with_name('package_tg_roster.py')
prefix=helper.read_text(encoding='utf-8').split('# Fixed bonuses')[0]
prefix=prefix.replace('target=root/', "classes.update(DB_sound='DBSoundRow',DB_sfx='DBSfxRow',DB_skin_ani='DBSkinAniRow',DB_skin_awaken_stat='DBSkinAwakenStatRow',DB_ability_resource='DBAbilityResourceRow')\ntarget=root/",1)
exec(compile(prefix,str(helper),'exec'))
HERO=2997004;ROSE=2997005;GROUP=352;COIN=498997;TID=1450000
FORMS=[(399931,HERO,'goku_black',399901),(399932,HERO,'goku_black',399902),(399933,ROSE,'goku_black_rose',399902)]
strings={TID:'Goku Black',TID+1:'Divine Usurper',TID+2:'Transform into Super Saiyan Rosé once per battle.',TID+100:'Super Saiyan Rosé Goku Black',TID+101:'Beauty of Divine Power',TID+30:'Super Saiyan Rosé',TID+31:'Transform into Super Saiyan Rosé for the remainder of battle. Gain stronger basic stats and a new attack kit. Usable once while alive.',TID+40:'Divine Supremacy',TID+41:'Increases basic stats by 20% and Critical Damage by 30%.',TID+140:'Divine Perfection',TID+141:'Increases basic stats by 30% and Critical Damage by 50%. Attacks recover HP equal to 20% of damage dealt.'}
for hero in [HERO,ROSE]:
 x=source('DB_hero_base',enc(2997001));x.update(id=enc(hero),hero_display=enc(1 if hero==HERO else 0),hero_list=enc(703 if hero==HERO else 704),hero_group=enc(GROUP),base_skin=enc(399931 if hero==HERO else 399933),hero_special=TID if hero==HERO else TID+100,hero_voice=-1);put('DB_hero_base',x)
 for n,old in [('DB_item_info',2997001)]:
  x=source(n,old,'item_id');x.update(item_id=hero,item_name=TID if hero==HERO else TID+100,item_nickname=TID+1 if hero==HERO else TID+101,item_icon='icon_hero_goku_black_0001_s' if hero==HERO else 'icon_hero_goku_black_rose_0001_s');put(n,x,'item_id')
x=source('DB_item_info',498999,'item_id');x.update(item_id=COIN,item_name=TID,item_icon='icon_hero_goku_black_0001_s');put('DB_item_info',x,'item_id')
x=source('DB_hero_job_group',12);x['list_array_hero_id']=list(dict.fromkeys([*x['list_array_hero_id'],HERO,ROSE]));put('DB_hero_job_group',x)
for i,(sid,hero,model,donor) in enumerate(FORMS):
 transformed=hero==ROSE;tid=TID+100 if transformed else TID;skill=14500100 if transformed else 14500000
 body=3399801+i;head=4999801+i;weapon=899801+i
 x=source('DB_skin_base',donor);x.update(id=sid,matching_hero_id=hero,category_group=HERO,base_skin_costume_id=body,base_head_costume_id=head,base_weapon_costume_id=weapon,skin_portrait_base=model+'_0001',hero_coin=0 if transformed else COIN,hero_coin_count=0 if transformed else 1,sort=10004+i,attribute=1,collection=0 if transformed else 1,change_hero_skin_id=0 if transformed else 399933,before_change_hero_skin_id=399932 if transformed else 0,after_change_hero_model=1 if transformed else 0,change_effect_id=0,costume_set_count='1/1/1/1')
 if transformed:
  for field in ['atk','def','hp','atk_add','def_add','hp_add']:x[field]*=1.35
 put('DB_skin_base',x)
 x=source('DB_item_info',donor,'item_id');x.update(item_id=sid,item_name=tid,item_nickname=tid+1,item_description=TID+2,item_icon=f'icon_skin_{model}_0001_s');put('DB_item_info',x,'item_id')
 x=source('DB_skin_ani',donor);x['id']=sid;put('DB_skin_ani',x)
 x=source('DB_skin_skill',donor);x.update(id=sid,ability_id=0 if transformed else 100011)
 for rank in range(1,4):x[f'skill_a_{rank}_id']=skill+rank;x[f'skill_b_{rank}_id']=skill+10+rank
 for rank in range(1,7):x[f'special_id_{rank}']=skill+90
 put('DB_skin_skill',x)
 for table,new,old,typ in [('DB_skin_costume_resource',body,3399852,1),('DB_head_costume_resource',head,4999852,3),('DB_weapon_costume_resource',weapon,899852,2)]:
  x=source(table,old);x.update(id=new,character_base=model)
  if typ==1:x.update(resource_body=f'hero_{model}_body_0001',resource_base_head=f'hero_{model}_head_0001',portrait_base=model+'_0001',model_scale=.9,gacha_model_scale=.9)
  if typ==3:x.update(resource_head=f'hero_{model}_head_0001',error_check_head_resource=f'hero_{model}_head_0001')
  put(table,x);x=source('DB_costume_base',old);x.update(id=new,costume_name=tid+1,hero_group=GROUP,costume_group=typ*10000000+GROUP*10000+100+i,list_array_matching_hero_id=[hero],list_array_costume_hide_hero_id=[hero]);put('DB_costume_base',x)
  x=source('DB_item_info',old,'item_id');x.update(item_id=new,item_name=tid+1,item_icon=f'icon_skin_{model}_0001_s');put('DB_item_info',x,'item_id')
 for offset,old in [(1,14000201),(2,14000202),(3,14000203),(11,14000211),(12,14000212),(13,14000213),(90,14000290)]:
  phase=1 if offset<10 else 2 if offset<90 else 3
  x=source('DB_skill_card_base',enc(old,0x65656565));x.update(id=enc(skill+offset,0x65656565),skill_name=tid+10+phase,skill_explain=tid+20+phase,list_array_buff_id_list=[],list_array_option_id_list=[],target=2 if phase==1 else 4,attack_type=1,range_type=1 if phase==1 else 2,atk_per=fenc(([200,300,500][offset-1] if phase==1 else [160,240,400][offset-11] if phase==2 else 650)*(1.15 if transformed else 1)))
  if transformed:x['list_array_option_id_list']=[(next(r['id'] for r in tables['DB_skill_card_option'] if r['effect_keyword']=='skill_hp_steal_add_per' and round(struct.unpack('<f',struct.pack('<I',(r['effect_value']^0xbdbdbdbd)&0xffffffff))[0])==20)^0xbdbdbdbd)&0xffffffff]
  put('DB_skill_card_base',x)
  x=source('DB_skill_card_resource',enc(old,0x11111111));x.update(id=enc(skill+offset,0x11111111),skill_folder=f'skill_0{phase}',cut_in_special='',hit_sfx_id=enc(198500053 if transformed else 198500043,0x11111111));put('DB_skill_card_resource',x)
 strings.update({tid+11:'Divine Blade Rush' if transformed else 'Black Power Rush',tid+12:'Rosé Ki Volley' if transformed else 'Dark Ki Volley',tid+13:'Divine Lasso' if transformed else 'Black Power Ball',tid+21:'Inflicts damage equal to {melee_val} of Attack on one enemy.',tid+22:'Inflicts damage equal to {melee_val} of Attack on all enemies.',tid+23:'Inflicts damage equal to {melee_val} of Attack on all enemies.'})

for hero in [HERO,ROSE]:
 for table,key in [('DB_skin_evolution','matching_hero_id'),('DB_skin_awaken_resource','hero_id'),('DB_skin_skill_levelup','hero_id'),('DB_skin_transcend','hero_id'),('DB_skin_exceed','hero_id'),('DB_skin_awaken_stat','hero_id')]:rules(table,key,2997001,hero)
 # Black stops at UR; Rosé is a transformation, never an owned evolution.
 tables['DB_skin_evolution'][:]=[x for x in tables['DB_skin_evolution'] if x['matching_hero_id']!=hero or x['evolution_rating']<6]
 ids=[]
 for j,(keyword,value) in enumerate([('pass_atk_def_hp_inc_per',30 if hero==ROSE else 20),('pass_crit_atk_add_per',50 if hero==ROSE else 30)]):
  pid=985030+(10 if hero==ROSE else 0)+j;ids.append(pid)
  x=deepcopy(next(x for x in tables['DB_skill_passive'] if x['effect_keyword']==keyword and x['target']=='self' and x['exclusive_type']=='normal'))
  x.update(id=enc(pid,0x4c4c4c4c),name=TID+140 if hero==ROSE else TID+40,explain=TID+141 if hero==ROSE else TID+41,first_stack=enc(1,0x4c4c4c4c),max_stack=enc(1,0x4c4c4c4c),effect_value=fenc(value,0x4c4c4c4c),effect_value_add=fenc(0,0x4c4c4c4c),list_array_apply_contents=[1],active_sfx_id=enc(0,0x4c4c4c4c),passive_sfx_id=enc(0,0x4c4c4c4c),list_array_hero_target=[],list_array_kind_target=[],kind_target=enc(0,0x4c4c4c4c),list_array_apply_hero_job_group=[]);put('DB_skill_passive',x)
 x=source('DB_skin_exclusive_passive',2997001,'hero_id');x.update(hero_id=hero,exclusive_passive_id_1=ids[0],exclusive_passive_id_2=ids[1],exclusive_passive_id_3=0,list_array_ability_exclusive_passive_id=[] if hero==ROSE else [985032]);put('DB_skin_exclusive_passive',x,'hero_id')
x=source('DB_skill_passive',enc(985020,0x4c4c4c4c));x.update(id=enc(985032,0x4c4c4c4c),name=TID+30,explain=TID+31);put('DB_skill_passive',x)
x=source('DB_ability_resource',100010);x.update(id=100011,ability_skill_card=14501000);put('DB_ability_resource',x)
for table,xor in [('DB_skill_card_base',0x65656565),('DB_skill_card_resource',0x11111111)]:
 x=source(table,enc(14201000,xor));x['id']=enc(14501000,xor)
 if table=='DB_skill_card_base':x.update(skill_name=TID+30,skill_explain=TID+31)
 put(table,x)
for effect in json.loads((root/'Research/DBLegends/black-vfx-registration.json').read_text()):
 x=source('DB_sfx',100130300);x.update(effect,attach_type=2 if effect['id'] in [198500043,198500053] else 0,create_socket='fx_spawn_righthand' if effect['id']<198500060 else 'fx_spawn_center',force_sfx_scale=0);put('DB_sfx',x)
for sound in json.loads((root/'Research/DBLegends/black-audio-registration.json').read_text()):
 put('DB_sound',sound)
# Add the obtainable SSR to the existing Legends banner, not the hidden form.
donor=next((x for x in tables['DB_gamble_group'] if x['skin_id']==399901),next(x for x in tables['DB_gamble_group'] if x['gamble_group']==1309))
for group in {donor['gamble_group']}:
 x=deepcopy(donor);x.update(id=max(x['id'] for x in tables['DB_gamble_group'])+1,gamble_group=group,skin_id=399931)
 if not any(r['gamble_group']==group and r['skin_id']==399931 for r in tables['DB_gamble_group']):tables['DB_gamble_group'].append(x)
assert not any(x['skin_id']==399933 for x in tables['DB_gamble_group'])
for o in env.objects:
 if o.type.name=='TextAsset':
  a=o.read()
  if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));mf=root/'dist/cache/br-b.bin';b=bytearray(mf.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));mf.write_bytes(b)
for n in classes:(root/f'Research/DecodedCache/{n}.tg.offline.json').write_text(json.dumps(tables[n],indent=2))
(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2));(root/'Research/DecodedCache/items.json').write_text(json.dumps(tables['DB_item_info'],indent=2))
suffix=helper.read_text(encoding='utf-8');lang=suffix[suffix.index("path=root/'dist/kaneki-assets/enl/"):suffix.index("(root/'dist/tg-roster-cards.json')")];exec(compile(lang,str(helper),'exec'))
f=root/'Server/Protocol/LocalGachaCatalog.h';s=f.read_text();a=s.index('inline const Skin Skins[] = {');b=s.index('\n};',a);s=s[:a]+'inline const Skin Skins[] = {\n'+''.join('{%d,%d,%d},\n'%(x['id'],x['matching_hero_id'],x['rating']) for x in tables['DB_skin_base'])+s[b:];f.write_text(s)
runpy.run_path(str(root/'Tools/build_development_catalog.py'),run_name='__main__');runpy.run_path(str(root/'Tools/build_material_catalog.py'),run_name='__main__')
units=[dict(hero=HERO,ssr=399931,ur=399932,body=3399801,head=4999801,weapon=899801,coin=COIN,group=GROUP)]
post=suffix[suffix.index("for filename,names in [('LocalEconomyCatalog.h'"):suffix.index("path=root/'dist/kaneki-assets/enl/")];post=post.replace(",('LocalSystemsCatalog.h',['TrueAwakeningRecipeRows'])",'');exec(compile(post,str(helper),'exec'))
(root/'Research/DBLegends/black-registration.json').write_text(json.dumps(dict(hero=HERO,hidden_hero=ROSE,forms=FORMS),indent=2))
print('Registered Black SSR/UR and battle-only Rosé, ability, distinct cards, passives and banner')
