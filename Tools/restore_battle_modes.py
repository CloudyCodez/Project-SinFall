"""Generate native Fort Solgres/Boss catalogs and their exact RMI contracts."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
protocol = ROOT / 'Server/Protocol'
catalog = ['#pragma once', 'namespace GcLocal {',
           'struct BattleStage { int mode, id; int monsters[10]; };',
           'inline const BattleStage BattleStages[] = {']
for mode, table in [(1, 'week'), (2, 'boss')]:
    rows = json.loads((ROOT / f'Research/DecodedCache/DB_stage_{table}.json').read_text())
    for row in rows:
        monsters = [row.get(f'monster_id_{i}', 0) for i in range(1, 7)]
        monsters += [row.get(f'boss_id_{i}', 0) for i in range(1, 5)]
        assert any(monsters), (table, row['id'])
        catalog.append('{%d,%d,{%s}},' % (mode, row['id'], ','.join(map(str, monsters))))
catalog += ['};', 'inline const BattleStage* FindBattleStage(int mode, int id) {',
            'for (const auto& row : BattleStages) if (row.mode == mode && row.id == id) return &row;',
            'return nullptr; }', '}']
(protocol / 'LocalBattleCatalog.h').write_text('\n'.join(catalog) + '\n')
for name, cbase, sbase in [('Week',10152,18815), ('Boss',10167,18818)]:
    ns = f'SevenDS{name}Battle'
    c2s = f'''#include "GrandCrossRmiTypes.h"
global {ns}C2S {cbase}
{{
 CG_Request_{name}_Stage_Start([in] LocalStageStartRequest request);
 CG_Request_{name}_Stage_Clear([in] LocalStageClearRequest request);
 CG_Request_{name}_Stage_Continue();
}}
'''
    start_extra = ', [in] LocalNoItem useItem' if name == 'Week' else ''
    clear_extra = '[in] EmptyItemResults apList, [in] EmptyItemResults packageList, [in] EmptyItemResults items' if name == 'Week' else '[in] LocalDestroyDiscovery discovery, [in] bool first, [in] EmptyItemResults packageList'
    s2c = f'''#include "GrandCrossRmiTypes.h"
global {ns}S2C {sbase}
{{
 CG_Request_{name}_Stage_StartOK([in] LocalStageStartResult result, [in] LocalPayback payback{start_extra});
 CG_Request_{name}_Stage_ClearOK([in] LocalStageClearResult result, [in] bool flag, {clear_extra});
 CG_Request_{name}_Stage_ContinueOK([in] EmptyItemResults items, [in] short count, [in] LocalPayback payback);
}}
'''
    (protocol / (ns+'C2S.PIDL')).write_text(c2s)
    (protocol / (ns+'S2C.PIDL')).write_text(s2c)
source = ROOT / 'Server/GrandCrossLocalServer.cpp'
text = source.read_text()
handlers = []
for mode, name in [(1,'Week'), (2,'Boss')]:
    ns = f'SevenDS{name}Battle'
    for side, suffix in [('C2S','stub'), ('S2C','proxy')]:
        include = f'#include "Protocol/Generated/{ns}{side}_{suffix}.h"'
        if include not in text: text = include + '\n' + text
    start_extra = ',LocalNoItem{}' if mode == 1 else ''
    clear_args = 'first,EmptyItemResults{},EmptyItemResults{},EmptyItemResults{}' if mode == 1 else 'false,LocalDestroyDiscovery{},first,EmptyItemResults{}'
    handlers.append(f'''
{ns}S2C::Proxy g_{name.lower()}BattleProxy;
class {name}BattleStub final : public {ns}C2S::Stub {{
public:
 DECRMI_{ns}C2S_CG_Request_{name}_Stage_Start;
 DECRMI_{ns}C2S_CG_Request_{name}_Stage_Clear;
 DECRMI_{ns}C2S_CG_Request_{name}_Stage_Continue;
}} g_{name.lower()}BattleStub;
DEFRMI_{ns}C2S_CG_Request_{name}_Stage_Start({name}BattleStub) {{
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 if (!GcLocal::FindBattleStage({mode},request.stage)) return false;
 GcLocal::ActiveBattles()[remote] = {{{mode},request.stage}};
 g_{name.lower()}BattleProxy.CG_Request_{name}_Stage_StartOK(remote,RmiContext::ReliableSend,LocalStageStartResult{{request.stage,request.index,{mode}}},LocalPayback{{}}{start_extra});
 std::printf("[Grand Cross Local] {name} start %d.\\n",request.stage); return true;
}}
DEFRMI_{ns}C2S_CG_Request_{name}_Stage_Clear({name}BattleStub) {{
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 auto active=GcLocal::ActiveBattles().find(remote);
 if (active==GcLocal::ActiveBattles().end() || active->second != std::make_pair({mode},int(request.stage))) return false;
 bool first=false;
 if (request.win) {{ first=GcLocal::BattleClears().insert({{{mode},request.stage}}).second; GcLocal::SaveBattleProgress(); }}
 g_{name.lower()}BattleProxy.CG_Request_{name}_Stage_ClearOK(remote,RmiContext::ReliableSend,LocalStageClearResult{{request.stage,request.win}},{clear_args});
 GcLocal::ActiveBattles().erase(active);
 std::printf("[Grand Cross Local] {name} clear %d win=%d.\\n",request.stage,int(request.win)); return true;
}}
DEFRMI_{ns}C2S_CG_Request_{name}_Stage_Continue({name}BattleStub) {{
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 auto active=GcLocal::ActiveBattles().find(remote);
 if (active==GcLocal::ActiveBattles().end() || active->second.first != {mode}) return false;
 g_{name.lower()}BattleProxy.CG_Request_{name}_Stage_ContinueOK(remote,RmiContext::ReliableSend,EmptyItemResults{{}},int16_t(1),LocalPayback{{}}); return true;
}}
''')
    registration = f'    server->AttachStub(&g_{name.lower()}BattleStub);\n    server->AttachProxy(&g_{name.lower()}BattleProxy);\n'
    if registration not in text:
        text = text.replace('    server->AttachStub(&g_storyStartStub);',registration+'    server->AttachStub(&g_storyStartStub);')
begin, end = '// BEGIN RESTORED BATTLE HANDLERS', '// END RESTORED BATTLE HANDLERS'
if begin in text:
    text = text[:text.index(begin)] + text[text.index(end)+len(end):]
marker = '// This is deliberately a transport-only'
text = text.replace(marker,begin+'\n'+''.join(handlers)+end+'\n\n'+marker)
source.write_text(text)
print('Generated',len(catalog)-9,'stage rows and six battle requests')
