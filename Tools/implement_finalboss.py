from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'Server/Protocol/GrandCrossRmiTypes.h';s=p.read_text()
s=s.replace('#include "LocalBattleCatalog.h"','#include "LocalBattleCatalog.h"\n#include "LocalFinalBossCatalog.h"')
s=s.replace('struct LocalTownInfoResult {','struct LocalFinalBossInfo {};\nstruct LocalFinalBossClearExtra {};\nstruct LocalFinalBossRank {};\nstruct LocalTownInfoResult {')
s=s.replace(' if(value.mode==3){',' if(value.mode==5){const auto* battle=GcLocal::FindFinalBoss(value.stage);if(battle)monsters=battle->monsters;}else if(value.mode==3){')
s=s.replace('int count = 0; for (int i=0;i<10;++i) if (monsters[i]) ++count;', 'int size=value.mode==5?9:10;int count = 0; for (int i=0;i<size;++i) if (monsters[i]) ++count;')
s=s.replace('for (int i=0;i<10;++i) if (monsters[i])\n   msg << int32_t(monsters[i]) << int32_t(i >= 6 ? i-6 : 0) << uint8_t(0) << uint8_t(i >= 6 ? 1 : 0);','for (int i=0;i<size;++i) if (monsters[i])\n   msg << int32_t(monsters[i]) << int32_t(value.mode==5?i%3:(i >= 6 ? i-6 : 0)) << uint8_t(0) << uint8_t(value.mode==5?i/3:(i >= 6 ? 1 : 0));')
s+='''
namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalFinalBossInfo&){int current=0;std::set<int> seasons;for(auto r:GcLocal::FinalBossSettings){seasons.insert(r.season);current=(std::max)(current,r.season);}msg<<int32_t(current)<<int32_t(0);msg.WriteScalar(int32_t(sizeof(GcLocal::FinalBossSettings)/sizeof(GcLocal::FinalBossSettings[0])));for(auto r:GcLocal::FinalBossSettings)msg<<int32_t(r.id)<<int32_t(r.group)<<int32_t(0)<<int32_t(2147483647)<<uint8_t(0);msg<<int32_t(2147483647)<<int32_t(GcLocal::SeededMaterialCount(500806));msg.WriteScalar(int32_t(seasons.size()));for(int id:seasons)msg<<int32_t(id)<<int32_t(0)<<int32_t(2147483647);WriteZeroSchema(msg,"cibcc");return msg;}
inline CMessage& operator>>(CMessage& msg,LocalFinalBossInfo&){return msg;}
inline void AppendTextOut(String& s,LocalFinalBossInfo&){s+=L"<FinalBossInfo>";}
inline CMessage& operator<<(CMessage& msg,const LocalFinalBossClearExtra&){WriteZeroSchema(msg,"iiiccliiiciiiicii");return msg;}
inline CMessage& operator>>(CMessage& msg,LocalFinalBossClearExtra&){return msg;}
inline void AppendTextOut(String& s,LocalFinalBossClearExtra&){s+=L"<FinalBossScore>";}
inline CMessage& operator<<(CMessage& msg,const LocalFinalBossRank&){WriteZeroSchema(msg,"cciiliiiciii");return msg;}
inline CMessage& operator>>(CMessage& msg,LocalFinalBossRank&){return msg;}
inline void AppendTextOut(String& s,LocalFinalBossRank&){s+=L"<FinalBossRank>";}
}
'''
p.write_text(s)
p=root/'Server/Protocol/LocalBattleProgress.h';s=p.read_text().replace('if (FindCampaignStage(mode,stage)||FindBattleStage(mode,stage))','if (FindCampaignStage(mode,stage)||FindBattleStage(mode,stage)||(mode==5&&FindFinalBoss(stage)))');p.write_text(s)
p=root/'Server/GrandCrossLocalServer.cpp';s=p.read_text()
s='#include "Protocol/Generated/SevenDSFinalBossC2S_stub.h"\n#include "Protocol/Generated/SevenDSFinalBossS2C_proxy.h"\n#include "Protocol/Generated/SevenDSFinalBossRankC2S_stub.h"\n#include "Protocol/Generated/SevenDSFinalBossRankS2C_proxy.h"\n'+s
s=s.replace('inline const GcLocal::EconomyStage* EconomyStage(int mode,int id){for','inline const GcLocal::EconomyStage* EconomyStage(int mode,int id){if(mode==5)for(const auto& r:GcLocal::FinalBossEconomy)if(r.id==id)return &r;for')
s=s.replace('GcLocal::RecordMission(mode==1?7:', 'GcLocal::RecordMission(mode==5?118:mode==1?7:')
code='''SevenDSFinalBossS2C::Proxy g_finalBossProxy;
class FinalBossStub final : public SevenDSFinalBossC2S::Stub {public:
DECRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Start;
DECRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Clear;
DECRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Continue;
DECRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Season_Info;
} g_finalBossStub;
DEFRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Start(FinalBossStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(!GcLocal::FindFinalBoss(request.stage))return CancelRequest(remote,10187);if(!PayStage(5,request.stage))return CancelRequest(remote,10187,101);GcLocal::ActiveBattles()[remote]={5,request.stage};CaptureBattleParty(remote,request.teamIndex);GcLocal::RecordMission(119,0,1);g_finalBossProxy.CG_Request_FinalBoss_Stage_StartOK(remote,RmiContext::ReliableSend,LocalStageStartResult{request.stage,request.index,5},EmptyItemResults{},LocalPayback{});return true;}
DEFRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Clear(FinalBossStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);auto it=GcLocal::ActiveBattles().find(remote);if(it==GcLocal::ActiveBattles().end()||it->second!=std::make_pair(5,int(request.stage)))return CancelRequest(remote,10188);bool first=request.win&&GcLocal::BattleClears().insert({5,request.stage}).second;if(first)GcLocal::SaveBattleProgress();g_finalBossProxy.CG_Request_FinalBoss_Stage_ClearOK(remote,RmiContext::ReliableSend,CompleteStage(5,request.stage,request.win,first,remote),LocalFinalBossClearExtra{});GcLocal::ActiveBattleHeroes().erase(remote);GcLocal::ActiveBattles().erase(it);return true;}
DEFRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Continue(FinalBossStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);auto it=GcLocal::ActiveBattles().find(remote);if(it==GcLocal::ActiveBattles().end()||it->second.first!=5)return CancelRequest(remote,10189);if(!GcLocal::Spend({{500011,1}}))return CancelRequest(remote,10189,101);g_finalBossProxy.CG_Request_FinalBoss_Stage_ContinueOK(remote,RmiContext::ReliableSend,EmptyItemResults{},int16_t(1),LocalPayback{});return true;}
DEFRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Season_Info(FinalBossStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);g_finalBossProxy.CG_Request_FinalBoss_Season_InfoOK(remote,RmiContext::ReliableSend,LocalFinalBossInfo{});return true;}
SevenDSFinalBossRankS2C::Proxy g_finalBossRankProxy;
class FinalBossRankStub final : public SevenDSFinalBossRankC2S::Stub {public:DECRMI_SevenDSFinalBossRankC2S_CG_Request_FinalBoss_Season_Rank_Info;} g_finalBossRankStub;
DEFRMI_SevenDSFinalBossRankC2S_CG_Request_FinalBoss_Season_Rank_Info(FinalBossRankStub){g_finalBossRankProxy.CG_Request_FinalBoss_Season_Rank_InfoOK(remote,RmiContext::ReliableSend,LocalFinalBossRank{});return true;}
'''
marker='// This is deliberately a transport-only';s=s.replace(marker,code+'\n'+marker)
s=s.replace('    server->AttachProxy(&g_townInfoProxy);','    server->AttachProxy(&g_finalBossProxy);server->AttachStub(&g_finalBossStub);\n    server->AttachProxy(&g_finalBossRankProxy);server->AttachStub(&g_finalBossRankStub);\n    server->AttachProxy(&g_townInfoProxy);')
p.write_text(s)
contracts={
 'SevenDSFinalBossC2S':(10186,'CG_Request_FinalBoss_Stage_Start([in] LocalStageStartRequest request);\n CG_Request_FinalBoss_Stage_Clear([in] LocalStageClearRequest request);\n CG_Request_FinalBoss_Stage_Continue();\n CG_Request_FinalBoss_Season_Info();'),
 'SevenDSFinalBossS2C':(18898,'CG_Request_FinalBoss_Stage_StartOK([in] LocalStageStartResult result,[in] EmptyItemResults events,[in] LocalPayback payback);\n CG_Request_FinalBoss_Stage_ClearOK([in] LocalStageClearResult result,[in] LocalFinalBossClearExtra extra);\n CG_Request_FinalBoss_Stage_ContinueOK([in] EmptyItemResults costs,[in] int16 count,[in] LocalPayback payback);\n CG_Request_FinalBoss_Season_InfoOK([in] LocalFinalBossInfo result);'),
 'SevenDSFinalBossRankC2S':(10206,'CG_Request_FinalBoss_Season_Rank_Info([in] int seasonID,[in] int bossGroupID);'),
 'SevenDSFinalBossRankS2C':(18902,'CG_Request_FinalBoss_Season_Rank_InfoOK([in] LocalFinalBossRank result);')}
for ns,(base,methods) in contracts.items():(root/f'Server/Protocol/{ns}.PIDL').write_text('#include "GrandCrossRmiTypes.h"\nglobal %s %d\n{\n %s\n}\n'%(ns,base,methods))
