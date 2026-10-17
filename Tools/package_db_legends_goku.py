"""Register one Goku hero with native SSR -> UR -> LR evolution."""
from pathlib import Path
helper=Path(__file__).with_name('package_tg_roster.py')
prefix=helper.read_text(encoding='utf-8').split('# Fixed bonuses')[0]
prefix=prefix.replace("target=root/", "classes['DB_sfx']='DBSfxRow'\nclasses['DB_skin_ani']='DBSkinAniRow'\nclasses['DB_skin_awaken_stat']='DBSkinAwakenStatRow'\ntarget=root/",1)
exec(compile(prefix,str(helper),'exec'))
HERO=2997001;GROUP=350;COIN=498999;TID=1400000
FORMS=[(399901,'goku_base','Goku',5,399401),(399902,'goku_blue','Super Saiyan God Super Saiyan Goku',6,399402),(399903,'goku_ui','Ultra Instinct Sign Goku',7,300219)]
strings={TID:'Goku',TID+1:'Saiyan Beyond Limits',1400900:'Dragon Ball Legends',TID+40:'Saiyan Battle Instinct',TID+41:'Increases basic stats by 25%, Critical Chance by 30%, and reduces damage taken by 20%.'}
# Preserve the TG coin row used by an earlier prototype registration.
for u in units:
    if u['coin']==499950:
        x=source('DB_item_info',499904,'item_id');x.update(item_id=u['coin'],item_icon=f"icon_hero_{u['model']}_0001_s",item_name=u['text_base'],item_nickname=u['text_base']+1,item_description=u['text_base']+2);put('DB_item_info',x,'item_id')
hero=source('DB_hero_base',enc(2994001));hero.update(id=enc(HERO),hero_list=enc(700),hero_group=enc(GROUP),base_skin=enc(399901),hero_special=TID,hero_voice=-1,kind=enc(3),sub_kind_check=0,sub_kind=enc(0),list_array_hero_job_group=[3,12],collaboration_name=1400900,collaboration_kind=-1);put('DB_hero_base',hero)
for effect in json.loads((root/'Research/DBLegends/vfx-registration.json').read_text()):
    x=source('DB_sfx',100130300);x.update(effect,attach_type=0,create_socket='fx_spawn_righthand' if effect['id']!=198500003 else '',force_sfx_scale=0)
    if effect['id']==198500003:x['attach_type']=2
    put('DB_sfx',x)
job=source('DB_hero_job_group',12 if any(x['id']==12 for x in tables['DB_hero_job_group']) else 11)
members=job['list_array_hero_id'] if job['id']==12 else []
job.update(id=12,hero_job_group_name=1400900,sorting_number=12,list_array_hero_id=list(dict.fromkeys([*members,HERO])));put('DB_hero_job_group',job)
for id,old in [(HERO,2994001),(COIN,499904)]:
    x=source('DB_item_info',old,'item_id');x.update(item_id=id,item_icon='icon_hero_goku_base_0001_s',item_name=TID,item_nickname=TID+1);put('DB_item_info',x,'item_id')
for i,(sid,model,title,rating,donor) in enumerate(FORMS):
    tid=TID+i*100;skill=14000100+i*100;body=3399851+i;head=4999851+i;weapon=899851+i
    strings[tid]=title;strings[tid+1]=['Earth-Raised Saiyan','Power of the Gods','Instinct Awakened'][i]
    x=source('DB_skin_base',donor);x.update(id=sid,base_skin_costume_id=body,base_head_costume_id=head,base_weapon_costume_id=weapon,skin_portrait_base=model+'_0001',sort=10000+i,category_group=HERO,matching_hero_id=HERO,hero_coin=COIN,hero_coin_count=1,attribute=3,costume_set_count='1/1/1/1',weapon_hide_display=1);put('DB_skin_base',x)
    x=source('DB_item_info',donor,'item_id');x.update(item_id=sid,item_icon=f'icon_skin_{model}_0001_s',item_name=tid,item_nickname=tid+1,item_description=1400900);put('DB_item_info',x,'item_id')
    x=source('DB_skin_skill',399401);x['id']=sid
    for rank in range(1,4):x[f'skill_a_{rank}_id']=skill+rank;x[f'skill_b_{rank}_id']=skill+10+rank
    for rank in range(1,7):x[f'special_id_{rank}']=skill+90
    put('DB_skin_skill',x)
    x=source('DB_skin_ani',300100);x.update(id=sid,awaken_neck_ani_check=0);put('DB_skin_ani',x)
    for n,new,old,typ in [('DB_skin_costume_resource',body,3399401,1),('DB_head_costume_resource',head,4999401,3),('DB_weapon_costume_resource',weapon,899401,2)]:
        x=source(n,old);x.update(id=new,character_base=model)
        if typ==1:x.update(resource_body=f'hero_{model}_body_0001',resource_base_head=f'hero_{model}_head_0001',portrait_base=model+'_0001',model_scale=0.9,gacha_model_scale=0.9)
        if typ==3:x.update(resource_head=f'hero_{model}_head_0001',error_check_head_resource=f'hero_{model}_head_0001')
        put(n,x);x=source('DB_costume_base',old);x.update(id=new,costume_name=tid+1,hero_group=GROUP,costume_group=typ*10000000+GROUP*10000+100+i,list_array_matching_hero_id=[HERO],list_array_costume_hide_hero_id=[HERO]);put('DB_costume_base',x)
        x=source('DB_item_info',old,'item_id');x.update(item_id=new,item_name=tid+1,item_icon=f'icon_hero_{model}_0001_s');put('DB_item_info',x,'item_id')
    for phase,offset,folder,donorstart,amounts in [(1,0,'skill_01',202100,[180,270,450]),(2,10,'skill_02',202110,[140,210,350]),(3,89,'skill_03',202189,[550])]:
        titleid=tid+10+phase;strings[titleid]=['Martial Arts Rush','Ki Blast Volley','Kamehameha'][phase-1];strings[titleid+10]='Inflicts damage equal to {melee_val} of Attack on '+('one enemy.' if phase==1 else 'all enemies.')
        for rank,mult in enumerate(amounts,1):
            new=skill+offset+rank;old=donorstart+rank
            x=source('DB_skill_card_base',enc(old,0x65656565));x.update(id=enc(new,0x65656565),skill_name=titleid,skill_explain=titleid+10,attack_type=1,range_type=1 if phase==1 else 2,atk_per=fenc(mult+i*20),atk_per_add=fenc(0),list_array_buff_id_list=[],list_array_option_id_list=[]);put('DB_skill_card_base',x)
            # RANGE_TYPE controls melee/ranged movement; TARGET selects enemies.
            x['target']=2 if phase==1 else 4
            x=source('DB_skill_card_resource',enc(old,0x11111111));x.update(id=enc(new,0x11111111),skill_folder=folder,icon='icon_monster_single_attack' if phase==1 else 'icon_monster_special',cut_in_special='',list_array_special_end_sfx_id=[],special_end_ani=0,special_end_ui_sfx='',special_end_sound_id=enc(0,0x11111111),skill_final_end_sound_id=enc(0,0x11111111),skill_final_end_sfx_id=enc(0,0x11111111),last_hit_sfx_id=enc(0,0x11111111),post_effect_type=enc(0,0x11111111));
            if phase>=2:x['hit_sfx_id']=enc(198500003,0x11111111)
            put('DB_skill_card_resource',x)
for n,key in [('DB_skin_evolution','matching_hero_id'),('DB_skin_awaken_resource','hero_id'),('DB_skin_skill_levelup','hero_id'),('DB_skin_transcend','hero_id'),('DB_skin_exceed','hero_id')]:rules(n,key,2994001,HERO)
rules('DB_skin_awaken_stat','hero_id',1005001,HERO)
# The native LR materials/formula come from Elizabeth's existing LR recipe.
lr=next(x for x in tables['DB_skin_evolution'] if x['matching_hero_id']==1035003 and x['evolution_rating']==6);lr=deepcopy(lr);lr.update(id=max(x['id'] for x in tables['DB_skin_evolution'])+1,matching_hero_id=HERO);tables['DB_skin_evolution'].append(lr)
ids=[]
for j,(keyword,value) in enumerate([('pass_atk_def_hp_inc_per',25),('pass_crit_add_per',30),('pass_get_dmg_dec_per',20)]):
    pid=985000+j;ids.append(pid);x=deepcopy(next(x for x in tables['DB_skill_passive'] if x['effect_keyword']==keyword and x['target']=='self' and x['exclusive_type']=='normal' and x['list_array_apply_contents']==[1]))
    x.update(id=enc(pid,0x4c4c4c4c),name=TID+40,explain=TID+41,first_stack=enc(1,0x4c4c4c4c),max_stack=enc(1,0x4c4c4c4c),effect_value=fenc(value,0x4c4c4c4c),effect_value_add=fenc(0,0x4c4c4c4c),active_sfx_id=enc(0,0x4c4c4c4c),passive_sfx_id=enc(0,0x4c4c4c4c),list_array_hero_target=[],list_array_kind_target=[],kind_target=enc(0,0x4c4c4c4c),list_array_apply_hero_job_group=[]);put('DB_skill_passive',x)
x=deepcopy(tables['DB_skin_exclusive_passive'][0]);x.update(hero_id=HERO,special_level_passive=0,exclusive_passive_id_1=ids[0],exclusive_passive_id_2=ids[1],exclusive_passive_id_3=ids[2]);put('DB_skin_exclusive_passive',x,'hero_id')
for o in env.objects:
    if o.type.name=='TextAsset':
        a=o.read()
        if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));mf=root/'dist/cache/br-b.bin';b=bytearray(mf.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));mf.write_bytes(b)
for n in classes:(root/f'Research/DecodedCache/{n}.tg.offline.json').write_text(json.dumps(tables[n],indent=2))
(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2));(root/'Research/DecodedCache/items.json').write_text(json.dumps(tables['DB_item_info'],indent=2))
# Reuse the tested language/currency/catalog writers, without rerunning TG kits.
suffix=helper.read_text(encoding='utf-8');lang=suffix[suffix.index("path=root/'dist/kaneki-assets/enl/"):suffix.index("(root/'dist/tg-roster-cards.json')")];exec(compile(lang,str(helper),'exec'))
f=root/'Server/Protocol/LocalGachaCatalog.h';s=f.read_text();a=s.index('inline const Skin Skins[] = {');b=s.index('\n};',a);s=s[:a]+'inline const Skin Skins[] = {\n'+''.join('{%d,%d,%d},\n'%(x['id'],x['matching_hero_id'],x['rating']) for x in tables['DB_skin_base'])+s[b:];f.write_text(s)
runpy.run_path(str(root/'Tools/build_development_catalog.py'),run_name='__main__');runpy.run_path(str(root/'Tools/build_material_catalog.py'),run_name='__main__')
units=[dict(hero=HERO,ssr=399901,ur=399902,body=3399851,head=4999851,weapon=899851,coin=COIN,group=GROUP)]
post=suffix[suffix.index("for filename,names in [('LocalEconomyCatalog.h'"):suffix.index("path=root/'dist/kaneki-assets/enl/")]
exec(compile(post,str(helper),'exec'))
f=root/'Server/Protocol/LocalEconomyCatalog.h';s=f.read_text();a=s.index('EconomyCosts[]');b=s.index('\n};',a)
s=s[:b]+'\n{1,2997001,6,0,{542406,542107,542701,500012,0},{6,3,100,2000000,0}},'+s[b:]
a=s.index('HeroCoins[]');b=s.index('\n};',a);section=s[a:b]
section=re.sub(r'\{39990[123],\d+\},','',section)
section+='\n'+''.join('{%d,%d},\n'%(sid,COIN) for sid,model,title,rating,donor in FORMS);s=s[:a]+section+s[b:];f.write_text(s)
f=root/'Server/Protocol/LocalCosmeticCatalog.h';s=f.read_text();a=s.index('\n};')
for i in [1,2]:
    for new,typ in [(3399851+i,1),(4999851+i,3),(899851+i,2)]:
        if '{%d,'%new not in s:s=s[:a]+'\n{%d,%d,%d,%d},'%(new,typ,GROUP,typ*10000000+GROUP*10000+100+i)+s[a:];a=s.index('\n};')
f.write_text(s)
(root/'Research/DBLegends/goku-registration.json').write_text(json.dumps(dict(hero=HERO,forms=FORMS),indent=2))
print('Registered Goku SSR, Blue UR, and Ultra Instinct Sign LR')
