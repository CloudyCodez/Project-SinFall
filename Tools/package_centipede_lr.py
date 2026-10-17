"""Add Centipede's native LR evolution and a distinct high-power LR kit."""
from pathlib import Path
helper=Path(__file__).with_name('package_tg_roster.py')
prefix=helper.read_text().split('# Fixed bonuses')[0]
prefix=prefix.replace('target=root/',"classes.update(DB_skin_ani='DBSkinAniRow',DB_skin_awaken_stat='DBSkinAwakenStatRow')\ntarget=root/",1)
exec(compile(prefix,str(helper),'exec'))
HERO=2995001;SID=399950;SKILL=14300100;TID=1430100
assert not any(x['id']==SID and x['matching_hero_id']!=HERO for x in tables['DB_skin_base'])
base=source('DB_skin_base',399502);native=source('DB_skin_base',300219)
row=deepcopy(base)
for key in ['rating','max_level','evolution_level','start_rating','select_rank_exp','level_initializtion']:
    row[key]=native[key]
row.update(id=SID,sort=10150)
for stat in ['atk','def','hp','atk_add','def_add','hp_add']:row[stat]=base[stat]*2.0
row.update(crit_per=60.0,crit_atk_per=160.0,hp_steal_per=30.0,dmg_res=20.0)
put('DB_skin_base',row)
item=source('DB_item_info',399502,'item_id');item.update(item_id=SID,item_name=TID,item_nickname=TID+1);put('DB_item_info',item,'item_id')
ani=source('DB_skin_ani',300100);ani.update(id=SID,awaken_neck_ani_check=0);put('DB_skin_ani',ani)
skill=source('DB_skin_skill',399502);skill['id']=SID
for rank in range(1,4):skill[f'skill_a_{rank}_id']=SKILL+rank;skill[f'skill_b_{rank}_id']=SKILL+10+rank
for rank in range(1,7):skill[f'special_id_{rank}']=SKILL+90
put('DB_skin_skill',skill)
def option(keyword,value=None):
    choices=[x for x in tables['DB_skill_card_option'] if x['effect_keyword']==keyword]
    if value is not None:
        choices=[x for x in choices if abs(struct.unpack('<f',struct.pack('<I',(x['effect_value']^0xbdbdbdbd)&0xffffffff))[0]-value)<.001]
    assert choices,(keyword,value)
    return (choices[0]['id']^0xbdbdbdbd)&0xffffffff
strings={TID:'Ken Kaneki',TID+1:'Centipede — Unshackled Hunger',TID+10:'Predatory Rending',TID+11:'Centipede Catastrophe',TID+12:'Devour the Battlefield',
 TID+20:'Inflicts damage equal to {melee_val} of Attack on one enemy and Lifesteals 60% of the damage.',
 TID+21:'Inflicts damage equal to {melee_val} of Attack on all enemies, ignoring Defense.',
 TID+22:'Inflicts damage equal to {melee_val} of Attack on all enemies, Lifesteals 60% of the damage, and removes 2 Ultimate Move Gauge orbs.'}
for phase,offset,amounts in [(1,0,[240,360,600]),(2,10,[200,300,500]),(3,89,[800])]:
    for rank,mult in enumerate(amounts,1):
        old=990100+offset+rank;new=SKILL+offset+rank
        options=([option('skill_hp_steal_add_per',60)] if phase==1 else
                 [option('skill_ignore_fixed_def')] if phase==2 else
                 [option('skill_hp_steal_add_per',60),option('skill_stamina_dec',2)])
        card=source('DB_skill_card_base',enc(old,0x65656565))
        card.update(id=enc(new,0x65656565),skill_name=TID+9+phase,skill_explain=TID+19+phase,
                    atk_per=fenc(mult),atk_per_add=fenc(0),target=2 if phase==1 else 4,
                    range_type=1 if phase==1 else 2,list_array_option_id_list=options,list_array_buff_id_list=[])
        put('DB_skill_card_base',card)
        res=source('DB_skill_card_resource',enc(old,0x11111111));res['id']=enc(new,0x11111111)
        res['icon']='icon_monster_single_attack' if phase==1 else 'icon_monster_special';put('DB_skill_card_resource',res)
# Existing UR growth recipes remain; only append the official LR recipe tier.
recipe=source('DB_skin_evolution',next(x['id'] for x in tables['DB_skin_evolution'] if x['matching_hero_id']==1035003 and x['evolution_rating']==6))
tables['DB_skin_evolution'][:]=[x for x in tables['DB_skin_evolution'] if not(x['matching_hero_id']==HERO and x['evolution_rating']==6)]
recipe.update(id=max(x['id'] for x in tables['DB_skin_evolution'])+1,matching_hero_id=HERO);tables['DB_skin_evolution'].append(recipe)
rules('DB_skin_awaken_stat','hero_id',1005001,HERO)
for o in env.objects:
    if o.type.name=='TextAsset':
        a=o.read()
        if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'));mf=root/'dist/cache/br-b.bin';data=bytearray(mf.read_bytes());struct.pack_into('<I',data,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));mf.write_bytes(data)
for name in classes:(root/f'Research/DecodedCache/{name}.tg.offline.json').write_text(json.dumps(tables[name],indent=2))
(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2))
(root/'Research/DecodedCache/items.json').write_text(json.dumps(tables['DB_item_info'],indent=2))
suffix=helper.read_text();lang=suffix[suffix.index("path=root/'dist/kaneki-assets/enl/"):suffix.index("(root/'dist/tg-roster-cards.json')")];exec(compile(lang,str(helper),'exec'))
f=root/'Server/Protocol/LocalGachaCatalog.h';s=f.read_text();a=s.index('inline const Skin Skins[] = {');b=s.index('\n};',a);s=s[:a]+'inline const Skin Skins[] = {\n'+''.join('{%d,%d,%d},\n'%(x['id'],x['matching_hero_id'],x['rating']) for x in tables['DB_skin_base'])+s[b:];f.write_text(s)
runpy.run_path(str(root/'Tools/build_development_catalog.py'),run_name='__main__')
f=root/'Server/Protocol/LocalEconomyCatalog.h';s=f.read_text();a=s.index('inline const HeroCoin HeroCoins[]');b=s.index('\n};',a)
if '{399950,' not in s[a:b]:s=s[:b]+'\n{399950,498500},'+s[b:];f.write_text(s)
if '{1,2995001,6,0,' not in s:
    donor=next(line for line in s.splitlines() if line.startswith('{1,2997001,6,0,'))
    start=s.index('EconomyCosts[]');end=s.index('\n};',start)
    s=s[:end]+'\n'+donor.replace('2997001','2995001',1)+s[end:];f.write_text(s)
(root/'Research/TokyoGhoul/centipede-lr-registration.json').write_text(json.dumps(dict(hero=HERO,skin=SID,skill=SKILL),indent=2))
print('Registered Centipede native LR evolution, doubled basic/growth stats, lifesteal, AoE defense-ignore and ultimate gauge drain')
