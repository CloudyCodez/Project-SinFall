"""Register one Vegeta hero with native SSR -> UR -> LR evolution."""
from pathlib import Path
helper=Path(__file__).with_name('package_tg_roster.py')
prefix=helper.read_text(encoding='utf-8').split('# Fixed bonuses')[0]
prefix=prefix.replace("target=root/", "classes['DB_sfx']='DBSfxRow'\nclasses['DB_skin_ani']='DBSkinAniRow'\nclasses['DB_skin_awaken_stat']='DBSkinAwakenStatRow'\nclasses['DB_ability_resource']='DBAbilityResourceRow'\ntarget=root/",1)
exec(compile(prefix,str(helper),'exec'))

HERO=2997003;GROUP=350;SID=399921;MODEL='gogeta_blue';TID=1420000
strings={TID:'Super Saiyan God Super Saiyan Gogeta',TID+1:'Ultimate Fusion',TID+2:'Battle-only fusion of Ultra Instinct Sign Goku and Blue Vegeta.'}
hero=source('DB_hero_base',enc(1715901));hero.update(id=enc(HERO),hero_list=enc(702),hero_group=enc(GROUP),base_skin=enc(SID),hero_special=TID,hero_voice=-1,kind=enc(3),sub_kind_check=0,sub_kind=enc(0),list_array_hero_job_group=[3,12],collaboration_name=1400900,collaboration_kind=-1);put('DB_hero_base',hero)
x=source('DB_skin_base',399903);x.update(id=SID,base_skin_costume_id=3399871,base_head_costume_id=4999871,base_weapon_costume_id=899871,skin_portrait_base=MODEL+'_0001',matching_hero_id=HERO,category_group=2997001,hero_coin=0,hero_coin_count=0,before_change_hero_skin_id=399903,after_change_hero_model=1,change_hero_skin_id=0,collection=0,sort=10003,atk=1100.0,hp=15000.0,atk_add=65.0,def_add=55.0,hp_add=900.0);x['def']=800.0;put('DB_skin_base',x)
# Combine both LR forms' base stats and level growth at the same level.
goku=source('DB_skin_base',399903);vegeta=source('DB_skin_base',399913)
for field in ['atk','def','hp','atk_add','def_add','hp_add']:
 x[field]=1.5*(goku[field]+vegeta[field])
put('DB_skin_base',x)
for new,old in [(HERO,2997001),(SID,399903)]:
 x=source('DB_item_info',old,'item_id');x.update(item_id=new,item_icon='icon_skin_'+MODEL+'_0001_s',item_name=TID,item_nickname=TID+1,item_description=TID+2);put('DB_item_info',x,'item_id')
x=source('DB_skin_skill',399903);x.update(id=SID,ability_id=0)
for rank in range(1,4):x[f'skill_a_{rank}_id']=14200100+rank;x[f'skill_b_{rank}_id']=14200110+rank
for rank in range(1,7):x[f'special_id_{rank}']=14200190
put('DB_skin_skill',x)
x=source('DB_skin_ani',399903);x.update(id=SID);put('DB_skin_ani',x)
# A tag-created SkinData still resolves its new hero's passive row. Give the
# hidden form a complete row, without a second fusion ability or return button.
x=source('DB_skin_exclusive_passive',2997001,'hero_id');x.update(hero_id=HERO,list_array_ability_exclusive_passive_id=[]);put('DB_skin_exclusive_passive',x,'hero_id')
for n,new,old,typ in [('DB_skin_costume_resource',3399871,3399853,1),('DB_head_costume_resource',4999871,4999853,3),('DB_weapon_costume_resource',899871,899853,2)]:
 x=source(n,old);x.update(id=new,character_base=MODEL)
 if typ==1:x.update(resource_body='hero_'+MODEL+'_body_0001',resource_base_head='hero_'+MODEL+'_head_0001',portrait_base=MODEL+'_0001')
 if typ==3:x.update(resource_head='hero_'+MODEL+'_head_0001',error_check_head_resource='hero_'+MODEL+'_head_0001')
 put(n,x);x=source('DB_costume_base',old);x.update(id=new,costume_name=TID+1,hero_group=GROUP,costume_group=typ*10000000+GROUP*10000+100,list_array_matching_hero_id=[HERO],list_array_costume_hide_hero_id=[HERO]);put('DB_costume_base',x)
 x=source('DB_item_info',old,'item_id');x.update(item_id=new,item_name=TID+1,item_icon='icon_skin_'+MODEL+'_0001_s');put('DB_item_info',x,'item_id')
for offset in [1,2,3,11,12,13,90]:
 old=14000300+offset;new=14200100+offset
 x=source('DB_skill_card_base',enc(old,0x65656565));x.update(id=enc(new,0x65656565),skill_name=TID+10+(1 if offset<10 else 2 if offset<90 else 3),skill_explain=TID+20+(1 if offset<10 else 2 if offset<90 else 3),atk_per=fenc([220,330,550][offset-1] if offset<10 else [180,270,450][offset-11] if offset<90 else 700));put('DB_skill_card_base',x)
 x=source('DB_skill_card_resource',enc(old,0x11111111));x.update(id=enc(new,0x11111111));put('DB_skill_card_resource',x)
strings.update({TID+11:'Fusion Rush',TID+12:'Godly Ki Barrage',TID+13:'Ultimate Kamehameha',TID+21:'Inflicts damage equal to {melee_val} of Attack on one enemy.',TID+22:'Inflicts damage equal to {melee_val} of Attack on all enemies.',TID+23:'Inflicts damage equal to {melee_val} of Attack on all enemies.'})
# Neither a summon pool nor a login grant references this battle-only form.
assert not any(x['skin_id']==SID for x in tables['DB_gamble_group'])
# Native tag transformation preloads Gogeta without granting ownership.
x=source('DB_skin_base',399903);x.update(change_hero_skin_id=SID,change_effect_id=0);put('DB_skin_base',x)
x=source('DB_skin_skill',399903);x['ability_id']=100010;put('DB_skin_skill',x)
x=source('DB_ability_resource',100002);x.update(id=100010,ability_skill_card=14201000,ability_special_level=1);put('DB_ability_resource',x)
strings.update({TID+30:'Fusion!',TID+31:'When LR Ultra Instinct Sign Goku and LR Blue Vegeta are both alive on the battlefield, fuse into Blue Gogeta for the remainder of the battle. Both fighters leave; Gogeta replaces Goku. Once per battle.'})
x=source('DB_skill_card_base',enc(1900002,0x65656565));x.update(id=enc(14201000,0x65656565),skill_name=TID+30,skill_explain=TID+31,target=0,attack_type=13,list_array_option_id_list=[],list_array_buff_id_list=[]);put('DB_skill_card_base',x)
x=source('DB_skill_card_resource',enc(1900002,0x11111111));x.update(id=enc(14201000,0x11111111),skill_folder='ability',icon='icon_monster_special');put('DB_skill_card_resource',x)
pid=985020
x=deepcopy(next(x for x in tables['DB_skill_passive'] if x['effect_keyword']=='pass_start_combat_turn_button_ability'))
x.update(id=enc(pid,0x4c4c4c4c),name=TID+30,explain=TID+31,effect_value=fenc(1,0x4c4c4c4c),active_sfx_id=enc(0,0x4c4c4c4c),list_array_apply_contents=[1],list_array_exclusive_condition_icon=[]);put('DB_skill_passive',x)
x=source('DB_skin_exclusive_passive',2997001,'hero_id');x['list_array_ability_exclusive_passive_id']=[pid];put('DB_skin_exclusive_passive',x,'hero_id')
for o in env.objects:
    if o.type.name=='TextAsset':
        a=o.read()
        if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));mf=root/'dist/cache/br-b.bin';b=bytearray(mf.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));mf.write_bytes(b)
for n in classes:(root/f'Research/DecodedCache/{n}.tg.offline.json').write_text(json.dumps(tables[n],indent=2))
(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2));(root/'Research/DecodedCache/items.json').write_text(json.dumps(tables['DB_item_info'],indent=2))
# Reuse the tested language/currency/catalog writers, without rerunning TG kits.
suffix=helper.read_text(encoding='utf-8');lang=suffix[suffix.index("path=root/'dist/kaneki-assets/enl/"):suffix.index("(root/'dist/tg-roster-cards.json')")];exec(compile(lang,str(helper),'exec'))

print('Registered hidden Blue Gogeta battle form; LR-pair fusion ability registered')
