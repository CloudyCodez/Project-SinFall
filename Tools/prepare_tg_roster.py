"""Inventory the requested playable BTC identities and pull their local assets."""
import json,re,subprocess
from pathlib import Path
from tg_tables import ROOT,read

ADB='C:/Program Files (x86)/Android/android-sdk/platform-tools/adb.exe'
ASSETS=ROOT/'Research/TokyoGhoul/PortAssets';ASSETS.mkdir(exist_ok=True)
heroes=read('HeroBase');translations=read('TranslateForMultiEN')
def text(key):return translations.get(key,{}).get('2',[''])[0]
manifest={line.split('=',1)[0]:line for line in (ROOT/'Research/TokyoGhoul/manifest-current').read_text().splitlines()}
def dependencies(name):
    # Dependency column precedes the size and optional extension, whether or
    # not this row exposes a container-directory alias.
    columns=manifest.get(name,'').split('=')
    return columns[4].split(',') if len(columns)>4 and columns[4] else []

units=[]
for source,row in heroes.items():
    name=text('tid#RoleName_'+source) or text('tid#RoleEngName_'+source)
    if name not in ['Ken Kaneki','Toka Kirishima','Kisho Arima','Haise Sasaki']:continue
    title=text('tid#RoleTitle_'+source)
    seen=set();todo=[source,source+'_controller']
    while todo:
        key=todo.pop()
        if key in seen:continue
        seen.add(key);todo+=dependencies(key)
    relevant=sorted(key for key in seen if key in manifest and not key.endswith('_controller'))
    relevant += [source+'_head',source+'_full']
    materials=[n for n in relevant if n.endswith('_mat')]
    meshes=[n for n in relevant if n.startswith('res_mid_')]
    animations=[n for n in relevant if n.endswith('_ani')]
    # Some prefab bundles embed their own meshes instead of using res_mid.
    assert materials and animations,(source,relevant)
    units.append(dict(source=source,name=name.replace('Toka','Touka'),title=title,
        files=relevant,materials=materials,meshes=meshes,animations=animations,
        source_skills=row.get('29',[]),source_passives=row.get('30',[])+row.get('31',[])))
# Preserve the successful prototype's ids and files as the first entry.
units.sort(key=lambda u:(u['source']!='1065',int(u['source'])))
for index,unit in enumerate(units):
    unit.update(index=index,hero=2995001+index,ssr=399501+index*2,ur=399502+index*2,
        body=3399501+index*2,head=4999501+index*2,weapon=899501+index*2,
        coin=499905+index,model='kaneki_centipede' if index==0 else 'tg_'+unit['source'],
        group=204 if unit['name'] in ['Ken Kaneki','Haise Sasaki'] else 205 if unit['name']=='Touka Kirishima' else 206,
        text_base=990001+index*100,skill_base=990100+index*100,
        attribute=3 if unit['name']=='Ken Kaneki' else 2 if unit['name']=='Kisho Arima' else 1)
    for name in unit['files']:
        dest=ASSETS/name
        if dest.exists():continue
        prior=ROOT/'Research/TokyoGhoul/Kaneki'/name
        if prior.exists():dest.write_bytes(prior.read_bytes());continue
        subprocess.run([ADB,'-s','emulator-5554','pull',
            '/sdcard/Android/data/com.funcat.tgbtc/files/assets/'+name,str(dest)],check=True,
            stdout=subprocess.DEVNULL)
    print(unit['source'],unit['name'],unit['title'],'assets ready',flush=True)
out=ROOT/'Research/TokyoGhoul/roster-port-inventory.json'
out.write_text(json.dumps(units,ensure_ascii=False,indent=2),encoding='utf8')
print('Prepared',len(units),'playable variants')
