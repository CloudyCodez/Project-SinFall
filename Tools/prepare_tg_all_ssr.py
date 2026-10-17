"""Append every source SSR/UR identity without renumbering installed heroes."""
import json, subprocess
from pathlib import Path
from tg_tables import ROOT,read

ADB='C:/Program Files (x86)/Android/android-sdk/platform-tools/adb.exe'
folder=ROOT/'Research/TokyoGhoul/PortAssets';folder.mkdir(exist_ok=True)
path=ROOT/'Research/TokyoGhoul/roster-port-inventory.json'
units=json.loads(path.read_text());existing={u['source'] for u in units};unavailable=[]
heroes=read('HeroBase');tr=read('TranslateForMultiEN')
manifest={line.split('=',1)[0]:line for line in (ROOT/'Research/TokyoGhoul/manifest-current').read_text().splitlines()}
def text(key):return tr.get(key,{}).get('2',[''])[0]
def dependencies(name):
    p=manifest.get(name,'').split('=');return p[4].split(',') if len(p)>4 and p[4] else []
groups={u['name']:u['group'] for u in units};nextgroup=max(groups.values())+1
# Localized role-name entries are absent for four older release variants.
# Their source skill/weapon descriptions and model-controller identities
# distinguish these forms from their original counterpart.
names={'1072':'Kohtaro Amon','1073':'Kureo Mado','1076':'Ayato Kirishima','1079':'Renji Yomo'}
human_names={'Kisho Arima','Juzo Suzuya','Kohtaro Amon','Kureo Mado','Akira Mado','Yukinori Shinohara','Kosuke Hoji','Iwao Kuroiwa','Take Hirako','Kori Ui','Mogan Tanakamaru','Ayumu Hogi','Chu Hachikawa','Kyoji Misaka','Kiyoko Aura','Hideyoshi Nagachika','Urie Kuki','Toru Mitsuki','Ginshi Shirazu','Saiko Yonebayashi'}
for sid,row in sorted(heroes.items(),key=lambda p:int(p[0])):
    if row.get('9',[0])[0] not in [4,55] or sid in existing:continue
    name=text('tid#RoleName_'+sid) or text('tid#RoleEngName_'+sid) or names.get(sid)
    if not name:raise ValueError(('Unknown source identity',sid))
    name=name.replace('Toka','Touka').replace('\xa0',' ')
    title=text('tid#RoleTitle_'+sid)
    if not title:raise ValueError(('Missing source title',sid))
    todo=[sid,sid+'_controller'];seen=set()
    while todo:
        n=todo.pop()
        if n in seen:continue
        seen.add(n);todo+=dependencies(n)
    files=sorted(n for n in seen if n in manifest and not n.endswith('_controller'))+[sid+'_head',sid+'_full']
    index=len(units)
    if name not in groups:groups[name]=nextgroup;nextgroup+=1
    unit=dict(source=sid,name=name,title=title,files=files,materials=[n for n in files if n.endswith('_mat')],meshes=[n for n in files if n.startswith('res_mid_')],animations=[n for n in files if n.endswith('_ani')],source_skills=row.get('29',[]),source_passives=row.get('30',[])+row.get('31',[]),source_rating=row['9'][0],index=index,hero=2995001+index,ssr=399501+index*2,ur=399502+index*2,body=3399501+index*2,head=4999501+index*2,weapon=899501+index*2,coin=499905+index,model='tg_'+sid,group=groups[name],text_base=1100000+(index-26)*100,skill_base=11000000+(index-26)*100,attribute=1+int(sid)%3)
    if not unit['materials'] or not unit['animations']:
        unavailable.append(dict(source=sid,name=name,title=title,reason='No model/controller dependency entry in this source manifest'))
        continue
    units.append(unit)
for u in units:
    u['race']='Human' if u['name'] in human_names or u['source']=='1049' else 'Ghoul'
    u['characteristic']='Tokyo Ghoul'
    u.setdefault('source_rating',heroes[u['source']]['9'][0])
path.write_text(json.dumps(units,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'Research/TokyoGhoul/unavailable-ssr-models.json').write_text(json.dumps(unavailable,indent=2))
print('Inventory:',len(units),'forms;',sum(u['source_rating'] in [4,55] for u in units),'source SSR/UR forms; installed IDs preserved',flush=True)
missing=[]
for unit in units:
    for name in unit['files']:
        dest=folder/name
        if dest.exists():continue
        result=subprocess.run([ADB,'-s','emulator-5554','pull','/sdcard/Android/data/com.funcat.tgbtc/files/assets/'+name,str(dest)],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        if result.returncode:missing.append(dict(source=unit['source'],asset=name,error=result.stderr.decode(errors='replace')))
    print(unit['source'],unit['name'],unit['title'],'source assets checked',flush=True)
(ROOT/'Research/TokyoGhoul/missing-ssr-assets.json').write_text(json.dumps(missing,indent=2))
if missing:raise SystemExit(f'{len(missing)} source files are not cached; see missing-ssr-assets.json')
