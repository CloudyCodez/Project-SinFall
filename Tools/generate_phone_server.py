"""Generate Android adapters around the existing game handlers and serializers."""
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]; src=ROOT/'Server'; out=ROOT/'AndroidHub/native';out.mkdir(parents=True,exist_ok=True)
(out/'Protocol').mkdir(exist_ok=True)
for p in (src/'Protocol').iterdir():
 if p.suffix in ('.h','.inc'):
  text=p.read_text()
  if p.name=='GrandCrossRmiTypes.h':
   text=re.sub(r'inline void WriteGcString\(.*?\n}\ninline CMessage& operator<<', 'inline void WriteGcString(CMessage& msg,const Proud::String& value) { msg << value; }\ninline void ReadGcString(CMessage& msg,Proud::String& value) { msg >> value; }\ninline CMessage& operator<<',text,count=1,flags=re.S)
  (out/'Protocol'/p.name).write_text(text)
protocol={}
for p in (src/'Protocol').glob('*.PIDL'):
 t=re.sub(r'//[^\n]*','',p.read_text()); match=re.search(r'global\s+(\w+)\s+(\d+)\s*\{(.*?)\}',t,re.S)
 if not match:continue
 ns,base,body=match.groups();methods=[]
 for index,m in enumerate(re.finditer(r'(\w+)\s*\((.*?)\)\s*;',body,re.S),1):
  name,args=m.groups();params=[]
  for arg in args.split(','):
   arg=re.sub(r'\[.*?\]','',arg).strip()
   if arg:
    typ,key=arg.rsplit(None,1);params.append((typ,key))
  methods.append((int(base)+index,name,params))
 protocol[ns]=methods
game=(src/'GrandCrossLocalServer.cpp').read_text(); game=game[:game.index('// This is deliberately a transport-only')]
game=re.sub(r'#include "Protocol/Generated/[^\n]+\n','',game)
game=game.replace('#include "ProudNetServer.h"','#include "PhoneProtocol.h"').replace('#include <Windows.h>','#include "Windows.h"')
game='#include <android/log.h>\n'+game
headers=['#pragma once','#include "Protocol/GrandCrossRmiTypes.h"']
dispatch=[]
for ns,methods in protocol.items():
 headers.append('namespace '+ns+' {')
 if ns.endswith('S2C'):
  headers.append('class Proxy { public:')
  for ident,name,params in methods:
   args=', '.join('const '+typ+'& '+key for typ,key in params)
   headers.append(f'bool {name}(Proud::HostID remote, Proud::RmiContext& context'+(', '+args if args else '')+') { Proud::CMessage m; m << uint8_t(1) << uint16_t('+str(ident)+'); '+''.join('m << '+key+'; ' for _,key in params)+'return PhoneSend(remote,m); }')
  headers.append('};')
 else:
  headers.append('class Stub { public: virtual ~Stub()=default;')
  for ident,name,params in methods:
   sig='Proud::HostID remote, Proud::RmiContext& rmiContext'+''.join(', const '+typ+'& '+key for typ,key in params)
   headers.append(f'virtual bool {name}({sig}) {{ return false; }}')
   headers.append(f'#define DECRMI_{ns}_{name} bool {name}({sig}) override')
   headers.append(f'#define DEFRMI_{ns}_{name}(DerivedClass) bool DerivedClass::{name}({sig})')
  headers.append('};')
 headers.append('}')
classes={}
for cls,ns,body,instance in re.findall(r'class\s+(\w+)\s+final\s*:\s*public\s+(\w+)::Stub\s*\{(.*?)\}\s*(\w*)\s*;',game,re.S):
 if not instance:
  match=re.search(r'\b'+cls+r'\s+(g_\w+)\s*;',game); instance=match.group(1) if match else ''
 if instance: classes[ns]=instance
for ns,instance in classes.items():
 for ident,name,params in protocol[ns]:
  if f'DEFRMI_{ns}_{name}(' not in game:continue
  declarations=''.join(typ+' '+key+'{}; m >> '+key+'; ' for typ,key in params)
  args=''.join(', '+key for _,key in params)
  dispatch.append(f'case {ident}: {{ {declarations} return {instance}.{name}(fd,Proud::RmiContext::ReliableSend{args}); }}')
game+='\nbool PhoneDispatch(int fd,uint16_t id,Proud::CMessage& m) { switch(id) {\n'+'\n'.join(dispatch)+'\ndefault: std::printf("Unhandled RMI %u\\n",id); return false; }}\n'
game+='''
void PhoneLogRoster() {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 const auto heroes=GcLocal::OwnedHeroes();int tg=0;
 for(int hero:heroes)if(hero>=2995001&&hero<=2995121)++tg;
 __android_log_print(ANDROID_LOG_INFO,"GCPhoneRoster","Login owned heroes=%zu skins=%zu TG=%d Centipede=%d",heroes.size(),GcLocal::OwnedSkins().size(),tg,int(heroes.count(2995001)));
 for(int skin:GcLocal::OwnedSkins()){const auto* row=GcLocal::FindSkin(skin);if(row&&row->hero>=2995001&&row->hero<=2995121)__android_log_print(ANDROID_LOG_INFO,"GCPhoneRoster","Owned TG hero=%d skin=%d",row->hero,skin);}
}
'''
(out/'PhoneProtocol.h').write_text('\n'.join(headers))
(out/'GameHandlers.cpp').write_text(game)
print('Adapted',len(dispatch),'existing handlers for Android')
