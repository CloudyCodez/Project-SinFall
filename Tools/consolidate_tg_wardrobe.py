"""Move alternate BTC outfits into native wardrobe slots, preserving legacy IDs.

Legacy skin/hero rows stay readable for save migration. Only canonical heroes
remain obtainable; Centipede Kaneki is deliberately a separate combat hero.
"""
from pathlib import Path
import json, re, math
helper = Path(__file__).with_name('package_tg_roster.py')
exec(compile(helper.read_text().split('# Fixed bonuses')[0], str(helper), 'exec'))

preferred = {'Ken Kaneki':'1007', 'Touka Kirishima':'1005', 'Kisho Arima':'1002',
             'Juzo Suzuya':'1003', 'Haise Sasaki':'1102'}
by_name = {}
for u in units:
    if u['source']=='1065': continue
    by_name.setdefault(u['name'].strip(), []).append(u)
canonical = {}
for name, variants in by_name.items():
    canonical[name] = next((u for u in variants if u['source']==preferred.get(name)),
                           min(variants, key=lambda u:int(u['source'])))
kept = [u for u in units if u['source']=='1065' or canonical[u['name'].strip()]['source']==u['source']]
# The login ownership record encodes heroGroup in one byte. The original
# roster reused race-wide groups; give each retained hero a distinct safe key.
hero_groups={u['hero']:204+i for i,u in enumerate(kept)}
assert len(set(hero_groups.values()))==len(kept) and max(hero_groups.values())<=255
costume_remaps=[]
# Keep historical equipped-group migrations when packaging repeatedly.
previous_header=root/'Server/Protocol/LocalTgWardrobe.h'
if previous_header.exists():
    section=re.search(r'TgCostumeGroupMigrations\[\] = \{(.*?)\};',previous_header.read_text(),re.S)
    if section:
        costume_remaps.extend(tuple(map(int,m)) for m in re.findall(r'\{(\d+),(\d+),(\d+)\}',section.group(1)))
for u in units:
    base=u if u in kept else canonical[u['name'].strip()]
    group=hero_groups[base['hero']]
    h=next(r for r in tables['DB_hero_base'] if r['id']==enc(u['hero']))
    h['hero_group']=enc(group)
    h['hero_display']=enc(1 if u in kept else 0)
    if u not in kept:
        # Native wardrobe ownership also derives a cosmetic's owner from the
        # skin whose base costume references it, independently of matching lists.
        for skin in tables['DB_skin_base']:
            if skin['id'] in [u['ssr'],u['ur']]:
                skin['matching_hero_id']=base['hero']
                skin['category_group']=base['hero']
    for field,typ in [('body',1),('head',3),('weapon',2)]:
        row=next(r for r in tables['DB_costume_base'] if r['id']==u[field])
        old_group=row['costume_group'];new_group=typ*10000000+group*10000+200+u['index']
        row.update(hero_group=group,costume_group=new_group,
                   list_array_matching_hero_id=[base['hero']],
                   list_array_costume_hide_hero_id=[base['hero']])
        mapping=(base['hero'],old_group,new_group)
        if old_group!=new_group and mapping not in costume_remaps:
            costume_remaps.append(mapping)
migrations = []
cosmetic_owner = {}
for u in units:
    if u in kept: continue
    base = canonical[u['name'].strip()]
    migrations.append(dict(source=u['source'], canonical=base['source'],
                           old_hero=u['hero'], hero=base['hero'], group=hero_groups[base['hero']],
                           old_ssr=u['ssr'], ssr=base['ssr'], old_ur=u['ur'], ur=base['ur']))
    for field, typ in [('body',1),('head',3),('weapon',2)]:
        row=next(r for r in tables['DB_costume_base'] if r['id']==u[field])
        # IsDisplayCostume requires at least one visible hero in this list.
        # Despite its 'hide' name, an empty array rejects the costume entirely.
        row.update(list_array_matching_hero_id=[base['hero']], list_array_costume_hide_hero_id=[base['hero']])
        cosmetic_owner[u[field]]=base['hero']

obsolete={u['ssr'] for u in units if u not in kept}|{u['ur'] for u in units if u not in kept}
pool=tables['DB_gamble_group']
pool[:]=[r for r in pool if r['skin_id'] not in obsolete]
tg=[r for r in pool if r['gamble_group']==9900]
skin_by_id={r['id']:r for r in tables['DB_skin_base']}
counts={rating:sum(skin_by_id[r['skin_id']]['rating']==rating for r in tg) for rating in (3,4,5)}
assert counts[5]==len(kept) and all(counts.values())
denominator=math.lcm(*counts.values())*100
rates={3:55,4:37,5:8}
for r in tg:
    rating=skin_by_id[r['skin_id']]['rating']
    r['gamble_rate']=1000

# Native lookup and migration hooks use one generated mapping.
out=['#pragma once','namespace GcLocal {',
     'struct TgWardrobeMigration {int oldSkin,skin,oldHero,hero,group;};',
     'inline constexpr TgWardrobeMigration TgWardrobeMigrations[] = {']
for m in migrations:
    for old, new in [('old_ssr','ssr'),('old_ur','ur')]:
        out.append('{%d,%d,%d,%d,%d},'%(m[old],m[new],m['old_hero'],m['hero'],m['group']))
out += ['};',
 'inline int CanonicalTgSkin(int id){for(const auto& r:TgWardrobeMigrations)if(r.oldSkin==id)return r.skin;return id;}',
 'inline int CanonicalTgHero(int id){for(const auto& r:TgWardrobeMigrations)if(r.oldHero==id)return r.hero;return id;}',
 'inline bool IsTgWardrobeSkin(int id){return CanonicalTgSkin(id)!=id;}',
 'struct TgWardrobeOwner {int cosmetic,hero;};','inline constexpr TgWardrobeOwner TgWardrobeOwners[] = {']
out += ['{%d,%d},'%p for p in sorted(cosmetic_owner.items())]
out += ['};','inline int TgWardrobeHero(int id){for(const auto& r:TgWardrobeOwners)if(r.cosmetic==id)return r.hero;return 0;}','}']
out.insert(-1,'struct TgCostumeGroupMigration {int hero,oldGroup,group;};\ninline constexpr TgCostumeGroupMigration TgCostumeGroupMigrations[] = {\n'+''.join('{%d,%d,%d},\n'%r for r in costume_remaps)+'};\ninline int CanonicalTgCostumeGroup(int hero,int group){if(!group)return 0;for(const auto& r:TgCostumeGroupMigrations)if(r.hero==hero&&r.oldGroup==group)return r.group;return group;}')
out.insert(-1, '''inline void BackupTgWardrobeSaves(){static bool done=[] {
 for(const char* name:{"local-test-account-skins.txt","local-test-development.txt","local-test-passives.txt","local-test-cosmetics.txt","local-test-teams.txt","local-test-equipment.txt"}){
  const std::string backup=std::string(name)+".tg-wardrobe-v1.bak";
  std::ifstream exists(backup,std::ios::binary);if(exists)continue;
  std::ifstream input(name,std::ios::binary);if(!input)continue;
  std::ofstream output(backup,std::ios::binary);output<<input.rdbuf();output.close();
  if(!output)throw std::runtime_error("Could not back up Tokyo Ghoul save migration");
 }return true;}();(void)done;}''')
(root/'Server/Protocol/LocalTgWardrobe.h').write_text('\n'.join(out)+'\n')

f=root/'Server/Protocol/LocalCosmeticCatalog.h';s=f.read_text()
for u in units:
    for field,typ in [('body',1),('head',3),('weapon',2)]:
        row=next(r for r in tables['DB_costume_base'] if r['id']==u[field])
        pattern=r'\{%d,\d+,\d+,\d+\},'%u[field]
        entry='{%d,%d,%d,%d},'%(u[field],typ,row['hero_group'],row['costume_group'])
        if re.search(pattern,s):s=re.sub(pattern,entry,s)
        else:
            end=s.index('\n};');s=s[:end]+'\n'+entry+s[end:]
f.write_text(s)
f=root/'Server/Protocol/LocalGachaCatalog.h';s=f.read_text()
a=s.index('inline const PoolEntry Pool[]');b=s.index('\n};',a)
lines=[]
for line in s[a:b].splitlines():
    if line.startswith('{'):
        values=[int(v) for v in line.strip('{}, ').split(',')]
        if values[1] in obsolete or values[0]==9900:continue
    lines.append(line)
for r in tg:
    skin=skin_by_id[r['skin_id']]
    weight=rates[skin['rating']]*denominator//(100*counts[skin['rating']])
    lines.append('{9900,%d,%d,1,0},'%(skin['id'],weight))
s=s[:a]+'\n'.join(lines)+s[b:];f.write_text(s)

for o in env.objects:
    if o.type.name=='TextAsset':
        a=o.read()
        if a.m_Name in classes:
            a.m_Script=write_table(tables[a.m_Name],classes[a.m_Name]).decode('utf8','surrogateescape');a.save()
target.write_bytes(env.file.save(packer='lz4'))
manifest=root/'dist/cache/br-b.bin';data=bytearray(manifest.read_bytes())
struct.pack_into('<I',data,12,zlib.crc32(b''.join(f.save() for f in env.file.files.values())));manifest.write_bytes(data)
for name in ['DB_costume_base','DB_gamble_group','DB_hero_base','DB_skin_base']:
    (root/f'Research/DecodedCache/{name}.tg.offline.json').write_text(json.dumps(tables[name],indent=2))
(root/'Research/DecodedCache/skins.json').write_text(json.dumps(tables['DB_skin_base'],indent=2))
(root/'Research/TokyoGhoul/wardrobe-migration.json').write_text(json.dumps(dict(kept=[u['source'] for u in kept],migrations=migrations),indent=2))
print('Consolidated',len(units),'TG variants into',len(kept),'heroes;',len(migrations),'outfits retained in native wardrobe')
