"""Refine retained TG identities without resetting wardrobe/evolution content."""
from pathlib import Path
helper=Path(__file__).with_name('package_tg_roster.py')
exec(compile(helper.read_text().split('# Fixed bonuses')[0],str(helper),'exec'))
kept=set(json.loads((root/'Research/TokyoGhoul/wardrobe-migration.json').read_text())['kept'])
anteiku={'Ken Kaneki','Touka Kirishima','Hinami Fueguchi','Yoshimura','Renji Yomo','Nishiki Nishio','Enji Koma','Kaya Irimi'}
ccg=({u['name'].strip() for u in units if u['race']=='Human'}-{'Hideyoshi Nagachika'})|{'Haise Sasaki','Yoshitoki Washu'}
strings={1431000:'CCG',1431001:'Anteiku'}
factions={13:ccg,14:anteiku}
for group,names in factions.items():
    row=deepcopy(tables['DB_hero_job_group'][0])
    row.update(id=group,hero_job_group_name=1431000+group-13,sorting_number=group,
               list_array_hero_id=[u['hero'] for u in units if u['name'].strip() in names],list_array_union_id=[])
    put('DB_hero_job_group',row)
for u in units:
    h=next(r for r in tables['DB_hero_base'] if r['id']==enc(u['hero']))
    groups=set(h['list_array_hero_job_group'])-{13,14}
    groups.update(g for g,names in factions.items() if u['name'].strip() in names)
    h['list_array_hero_job_group']=sorted(groups)

passives={((r['id']^0x4c4c4c4c)&0xffffffff):r for r in tables['DB_skill_passive']}
exclusives={r['hero_id']:r for r in tables['DB_skin_exclusive_passive']}
template=next(r for r in tables['DB_skill_passive'] if r['effect_keyword']=='pass_one_array_apply_hero_job_group_atk_def_hp_inc_per_ally' and r['exclusive_type']=='normal')
report=[]
healers={'Hinami Fueguchi','Yoshimura','Akira Mado','Hideyoshi Nagachika','Ryoko Fueguchi','Itori','Saiko Yonebayashi'}
tanks={'Noro','Yukinori Shinohara','Iwao Kuroiwa','Nishiki Nishio','Renji Yomo','Naki'}
elites={'Kisho Arima','Eto','Matasaka Kamishiro','Yakumo Omori','Rize Kamishiro'}
skins={r['id']:r for r in tables['DB_skin_base']}
baseline={5:deepcopy(skins[399401]),6:deepcopy(skins[399402])}
for u in units:
    # Range presentation does not set native damage targets. Match both.
    for offset in (1,2,3,11,12,13,90):
        card=next(r for r in tables['DB_skill_card_base'] if r['id']==enc(u['skill_base']+offset,0x65656565))
        card['target']=4 if card['range_type']==2 else 2
for u in units:
    if u['source'] not in kept:continue
    name=u['name'].strip();ex=exclusives[u['hero']]
    role='support' if name in healers else 'tank' if name in tanks else 'elite damage' if name in elites else 'damage'
    if u['source']!='1065':
        factors={'support':(.90,1.12,1.20),'tank':(.95,1.25,1.25),'elite damage':(1.20,1.05,1.10),'damage':(1.10,1.00,1.05)}[role]
        for sid,rating in [(u['ssr'],5),(u['ur'],6)]:
            skin=skins[sid]
            for stat,factor in zip(('atk','def','hp'),factors):
                for key in (stat,stat+'_add'):skin[key]=round(baseline[rating][key]*factor,3)
    # Commanders receive a native per-faction-member formation bonus. Other
    # components retain healing/defensive or offensive character identities.
    group=13 if name in {'Kisho Arima','Haise Sasaki','Kohtaro Amon','Akira Mado','Yoshitoki Washu'} else 14 if name in {'Yoshimura','Renji Yomo','Enji Koma','Kaya Irimi'} else None
    if group:
        pid=ex['exclusive_passive_id_1'];old=passives[pid];new=deepcopy(template)
        value=8 if group==13 else 10
        new.update(id=old['id'],name=old['name'],explain=old['explain'],explain_simple=-1,
                   effect_value=fenc(value,0x4c4c4c4c),effect_value_add=fenc(0,0x4c4c4c4c),
                   list_array_apply_hero_job_group=[group],kind_target=enc(0,0x4c4c4c4c),
                   list_array_kind_target=[],active_text=-1,active_sfx_id=enc(0,0x4c4c4c4c),passive_sfx_id=enc(0,0x4c4c4c4c),exclusive_invisible=0)
        put('DB_skill_passive',new)
        strings[new['explain']]=f"Increases own basic stats by {value}% for each {'CCG' if group==13 else 'Anteiku'} ally participating in battle."
    # Distinguish attacks using original native card option handlers.
    choices={
      'Ken Kaneki':('skill_hp_steal_add_per',30),
      'Rize Kamishiro':('skill_hp_steal_add_per',40),
      'Noro':('skill_hp_steal_add_per',40),
      'Kisho Arima':('skill_ignore_fixed_def',None),
      'Juzo Suzuya':('skill_crit_atk_inc_per',None),
      'Touka Kirishima':('skill_crit_atk_inc_per',None),
      'Yakumo Omori':('skill_stamina_dec',1),
      'Kureo Mado':('skill_stamina_dec',1),
    }
    if u['source']!='1065' and name in choices:
        keyword,value=choices[name];opts=[r for r in tables['DB_skill_card_option'] if r['effect_keyword']==keyword]
        if value is not None:opts=[r for r in opts if abs(struct.unpack('<f',struct.pack('<I',(r['effect_value']^0xbdbdbdbd)&0xffffffff))[0]-value)<.001]
        assert opts,(name,keyword,value)
        option=(opts[0]['id']^0xbdbdbdbd)&0xffffffff
        for rank in range(1,4):
            card=next(r for r in tables['DB_skill_card_base'] if r['id']==enc(u['skill_base']+rank,0x65656565))
            card['list_array_option_id_list']=[option]
            suffix={'skill_hp_steal_add_per':f'and Lifesteals {value}% of the damage','skill_ignore_fixed_def':'ignoring Defense','skill_crit_atk_inc_per':'with increased Critical Damage','skill_stamina_dec':'and removes 1 Ultimate Move Gauge orb'}[keyword]
            strings[card['skill_explain']]='Inflicts damage equal to {melee_val} of Attack on '+('all enemies' if card['range_type']==2 else 'one enemy')+' '+suffix+'.'
    if name in healers:
        heal=next(r for r in tables['DB_skill_card_option'] if r['effect_keyword']=='skill_dmg_per_heal_ally_all' and abs(struct.unpack('<f',struct.pack('<I',(r['effect_value']^0xbdbdbdbd)&0xffffffff))[0]-30)<.001)
        for rank in range(1,4):
            card=next(r for r in tables['DB_skill_card_base'] if r['id']==enc(u['skill_base']+10+rank,0x65656565))
            card['list_array_option_id_list']=[(heal['id']^0xbdbdbdbd)&0xffffffff]
            strings[card['skill_explain']]='Inflicts damage equal to {melee_val} of Attack on '+('all enemies' if card['range_type']==2 else 'one enemy')+' and heals all allies for 30% of damage dealt.'
    report.append(dict(source=u['source'],name=name,role=role,faction_bonus=group,attack=choices.get(name) if u['source']!='1065' else 'Centipede LR preserved'))

for o in env.objects:
    if o.type.name=='TextAsset':
        a=o.read()
        if a.m_Name in classes:a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'))
manifest=root/'dist/cache/br-b.bin';b=bytearray(manifest.read_bytes());struct.pack_into('<I',b,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));manifest.write_bytes(b)
for n in classes:(root/f'Research/DecodedCache/{n}.tg.offline.json').write_text(json.dumps(tables[n],indent=2))
# Use the same native encrypted translation writer as the roster packager.
language=helper.read_text().split("path=root/'dist/kaneki-assets/enl/",1)[1]
language="path=root/'dist/kaneki-assets/enl/"+language.split("(root/'dist/tg-roster-cards.json')",1)[0]
exec(compile(language,str(helper),'exec'))
(root/'Research/TokyoGhoul/combat-role-refinement.json').write_text(json.dumps(report,indent=2))
print('Refined',len(report),'retained TG roles; native CCG/Anteiku filters and distinct offensive mechanics')
