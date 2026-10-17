"""Source-informed, bounded GC kits using existing native effect handlers."""
import re,json
from tg_tables import read,ROOT
SOURCE=read('HeroBase');SKILLS=read('FightingSkill');TEXT=read('TranslateForMultiEN')
def translate(key):return TEXT.get(key,{}).get('2',[''])[0]
def source_description(u):
    ids=u['source_passives']+u['source_skills']
    return ' '.join(translate('tid#SkillDesc_'+k) for k in ids).lower()
# Distinct native stat/effect packages: role bonuses are race-filtered, never
# broad bonuses to every GC unit. Variant strengths follow source keywords.
IDENTITY_KITS = {
 'Ken Kaneki': ('One-Eyed Hunger', [('basic',25),('steal',30),('ramp',10)]),
 'Haise Sasaki': ('Quinx Commander', [('basic',25,'human'),('reduce',20),('ramp',8)]),
 'Touka Kirishima': ('Crimson Wing', [('atk',30,'ghoul'),('crit',35),('critdmg',40)]),
 'Kisho Arima': ('The White Reaper', [('basic',30),('critdmg',40),('reduce',25)]),
 'Hinami Fueguchi': ('Gentle Guardian', [('hp',35,'ghoul'),('reduce',20,'ghoul'),('regen',30)]),
 'Yoshimura': ('Anteiku Sanctuary', [('basic',30,'ghoul'),('reduce',20,'ghoul'),('regen',30)]),
 'Eto': ('One-Eyed Revolution', [('atk',35,'ghoul'),('critdmg',40),('ramp',10)]),
 'Sen Takatsuki': ('A Story of Ghouls', [('hp',30,'ghoul'),('atk',25,'ghoul'),('reduce',25)]),
 'Ayato Kirishima': ('Black Rabbit', [('atk',35),('crit',35),('ramp',10)]),
 'Rize Kamishiro': ('Voracious Appetite', [('hp',35),('steal',40),('atk',30)]),
 'Renji Yomo': ('Silent Protector', [('def',35,'ghoul'),('reduce',25),('ramp',9)]),
 'Shu Tsukiyama': ('Gourmet Obsession', [('crit',35),('critdmg',40),('steal',35)]),
 'Nishiki Nishio': ('Territorial Resolve', [('hp',30),('reduce',30),('ramp',10)]),
 'Yakumo Omori': ('Jason Unchained', [('atk',35),('steal',35),('ramp',10)]),
 'Noro': ('Undying Hunger', [('hp',40),('regen',40),('reduce',25)]),
 'Tatara': ('Aogiri Inferno', [('atk',30,'ghoul'),('atk',35),('critdmg',35)]),
 'Naki': ('White Suits Brotherhood', [('hp',30,'ghoul'),('def',30,'ghoul'),('ramp',10)]),
 'Miza Kusakari': ('Three Blades', [('atk',30),('crit',35),('reduce',25)]),
 'Uta': ('Behind the Mask', [('crit',40),('critdmg',35),('steal',30)]),
 'Itori': ('Hidden Network', [('basic',25,'ghoul'),('regen',35),('reduce',25)]),
 'Roma Hoito': ('Clown Masquerade', [('hp',35),('steal',30),('ramp',9)]),
 'Nico': ('Clown Vitality', [('hp',30,'ghoul'),('regen',40),('def',25)]),
 'Matasaka Kamishiro': ('Unrivaled Martial Arts', [('basic',30),('reduce',30),('ramp',10)]),
 'Kurona Yasuhisa': ('Black Twin', [('atk',30,'ghoul'),('steal',35),('crit',30)]),
 'Nashiro Yasuhisa': ('White Twin', [('hp',30,'ghoul'),('regen',35),('critdmg',35)]),
 'Ryoko Fueguchi': ("A Mother's Shelter", [('hp',35,'ghoul'),('def',25,'ghoul'),('regen',35)]),
 'Enji Koma': ('Devil Ape', [('atk',35),('def',30),('ramp',9)]),
 'Kaya Irimi': ('Black Dog', [('crit',35),('reduce',25),('ramp',10)]),
 'Nutcracker': ('Merciless Trap', [('critdmg',40),('atk',30),('steal',30)]),
 'Elder Bin': ('Aogiri Vanguard', [('atk',30,'ghoul'),('def',30),('crit',25)]),
 'Younger Bin': ('Aogiri Pursuit', [('hp',30,'ghoul'),('atk',35),('critdmg',30)]),
 'Kohtaro Amon': ('Unyielding Justice', [('basic',25,'human'),('atk',35),('reduce',25)]),
 'Akira Mado': ('Tactical Command', [('def',30,'human'),('atk',30,'human'),('regen',25)]),
 'Kureo Mado': ('Quinque Obsession', [('atk',35),('crit',30),('critdmg',40)]),
 'Juzo Suzuya': ('Dancing Blades', [('crit',40),('critdmg',40),('ramp',10)]),
 'Yukinori Shinohara': ('Veteran Shield', [('hp',30,'human'),('reduce',20,'human'),('def',35)]),
 'Iwao Kuroiwa': ('Ironclad Resolve', [('def',35,'human'),('hp',35),('reduce',30)]),
 'Take Hirako': ('Squad Discipline', [('atk',30,'human'),('crit',30),('reduce',25)]),
 'Kori Ui': ('Elite Precision', [('basic',30),('crit',35),('critdmg',35)]),
 'Kiyoko Aura': ('Seasoned Commander', [('basic',25,'human'),('def',35),('rampdef',10)]),
 'Kosuke Hoji': ('Steadfast Investigator', [('atk',30,'human'),('critdmg',35),('reduce',25)]),
 'Mogan Tanakamaru': ('Heavy Artillery', [('atk',40),('critdmg',35),('hp',25)]),
 'Chu Hachikawa': ('Relentless Pursuit', [('atk',35),('crit',30),('ramp',10)]),
 'Ayumu Hogi': ('Partner Cover', [('hp',30,'human'),('def',30),('crit',35)]),
 'Yoshitoki Washu': ('CCG Authority', [('basic',30,'human'),('reduce',20,'human'),('hp',30)]),
 'Hideyoshi Nagachika': ('Unbreakable Friendship', [('hp',30,'ally'),('def',25,'ally'),('reduce',25)]),
 'Urie Kuki': ('Quinx Ambition', [('atk',35),('crit',35),('ramp',10)]),
 'Ginshi Shirazu': ('Quinx Frontline', [('hp',30,'human'),('atk',35),('reduce',25)]),
 'Saiko Yonebayashi': ('Quinx Reserve', [('hp',35),('regen',35),('critdmg',40)]),
 'Toru Mitsuki': ('Quinx Focus', [('crit',40),('steal',30),('ramp',9)]),
 'Kyoji Misaka': ('Investigator Formation', [('def',30,'human'),('atk',30),('reduce',25)]),
}

def profile(u):
    if u['source']=='1065':
        return ('Unshackled Centipede', [('basic',40,'ghoul'),('steal',30),('ramp',10)])
    name, entries=IDENTITY_KITS[u['name'].strip()]
    entries=list(entries)
    desc=source_description(u)
    # Source variants emphasize a different personal strength while keeping
    # their character's team role. No unbounded triggers or fabricated stacks.
    if u['source'] not in ['1005','1002']:
        if 'shield' in desc or 'damage taken' in desc: entries[-1]=('reduce',30)
        elif 'regen' in desc: entries[-1]=('regen',35)
        elif 'heal' in desc or 'restore' in desc: entries[-1]=('steal',35) if u['race']=='Ghoul' else ('regen',35)
    return (u['title']+' — '+name, entries)

def card(u,phase,rank,options):
    sid=u['source'];desc=translate('tid#SkillDesc_'+sid+'_v1s1').lower() if phase==1 else translate('tid#SkillDesc_'+sid+'_n1s1').lower()
    alltargets='all enemies' in desc
    source=SKILLS.get(sid+('_v1s1' if phase==1 else '_n1s1'),{})
    for key in source.get('22',[]):desc+=' '+translate(key).lower()
    if 'crit' in desc:keyword='skill_crit_atk_inc_per';label='with increased Critical Damage'
    elif 'def' in desc or u['race']=='Human':keyword='skill_break_defence';label='with Shatter (ignores Resistance)'
    elif 'debuff' in desc:keyword='skill_dot_buff_dmg_add_per';label='with bonus damage against debuffed enemies'
    else:keyword='skill_ignore_fixed_def';label='ignoring Defense'
    opt=next((r for r in options if r['effect_keyword']==keyword),None)
    if opt is None:keyword='skill_break_defence';label='with Shatter (ignores Resistance)';opt=next(r for r in options if r['effect_keyword']==keyword)
    option=(opt['id']^0xbdbdbdbd)&0xffffffff
    mult=([140,210,350] if alltargets else [180,270,420])[rank-1] if phase<3 else (420 if alltargets else 600)
    name=(u['title']+' — '+(['Kagune Strike','Kagune Assault','Kagune Release'] if u['race']=='Ghoul' else ['Quinque Strike','Quinque Assault','Quinque Release'])[phase-1])
    explanation='Inflicts damage equal to {melee_val} of Attack on '+('all enemies' if alltargets else 'one enemy')+' '+label+'.'
    return dict(name=name,description=explanation,range=2 if alltargets else 1,multiplier=mult,option=option,keyword=keyword)
