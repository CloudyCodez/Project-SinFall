from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'Server/Protocol/GrandCrossRmiTypes.h';s=p.read_text().replace('#include "LocalFoodState.h"','#include "LocalFoodState.h"\n#include "LocalTownArtifactState.h"')
s=s.replace('struct LocalFoodResult {','struct LocalTownInfoResult {int town=0;};\nstruct LocalChestResult {int npc=0,item=0;};\nstruct LocalUnionRequest {int id=0;std::vector<std::pair<int,int>> items;};\nstruct LocalUnionResult {int id=0;std::vector<std::pair<int,int>> items;};\nstruct LocalFoodResult {')
s=s.replace('else if(index==432)', 'else if(index==428){std::set<int> towns;for(auto r:GcLocal::TownRules)towns.insert(r.id);for(auto r:GcLocal::TownChests)towns.insert(r.town);msg.WriteScalar(int32_t(towns.size()));for(int town:towns)WriteTownInfo(msg,town);}\n        else if(index==585){msg.WriteScalar(int32_t(GcLocal::ArtifactUnionExperience().size()));for(auto p:GcLocal::ArtifactUnionExperience())msg<<int32_t(p.first)<<int32_t(p.second);}\n        else if(index==432)')
marker='inline CMessage& operator<<(CMessage& msg, const LoginUserResultInfo& value)'
helper='''inline void WriteTownInfo(CMessage& msg,int town){int flags=0;for(auto r:GcLocal::TownChests)if(r.town==town&&GcLocal::OpenChests().count(r.npc))flags|=1<<r.index;msg<<int32_t(town)<<int32_t(GcLocal::TownExperience(town))<<int32_t(0)<<int32_t(flags)<<int32_t(0)<<int32_t(0)<<int32_t(0);msg.WriteScalar(int32_t(0));}
'''
assert marker in s;s=s.replace(marker,helper+marker)
s+='''
namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalTownInfoResult& v){WriteTownInfo(msg,v.town);WriteZeroSchema(msg,"oilbsiiiddiiiihbdohhiibibbbooobboobooooooboooobchbc");WriteQuestProgressList(msg);WriteZeroSchema(msg,"cciiisiiiiiosiiii");return msg;}
inline CMessage& operator>>(CMessage& msg,LocalTownInfoResult&){return msg;}
inline void AppendTextOut(String& s,LocalTownInfoResult&){s+=L"<TownInfo>";}
inline CMessage& operator<<(CMessage& msg,const LocalChestResult& v){msg<<int32_t(v.npc);if(v.item)WriteCommonResult(msg,v.item,1);else msg<<LocalNoItem{};msg<<MissionResult{};return msg;}
inline CMessage& operator>>(CMessage& msg,LocalChestResult&){return msg;}
inline void AppendTextOut(String& s,LocalChestResult&){s+=L"<TownChest>";}
inline CMessage& operator>>(CMessage& msg,LocalUnionRequest& v){msg>>v.id;int n;msg.ReadScalar(n);if(n<1||n>100)throw std::runtime_error("Invalid artifact materials");for(int i=0;i<n;++i){int id,count;msg>>id>>count;if(count<1||count>1000000)throw std::runtime_error("Invalid artifact amount");v.items.emplace_back(id,count);}return msg;}
inline CMessage& operator<<(CMessage& msg,const LocalUnionRequest&){return msg;}
inline void AppendTextOut(String& s,LocalUnionRequest&){s+=L"<UnionUpgrade>";}
inline CMessage& operator<<(CMessage& msg,const LocalUnionResult& v){msg<<int32_t(v.id)<<int32_t(GcLocal::ArtifactUnionExperience()[v.id]);msg.WriteScalar(int32_t(v.items.size()));for(auto p:v.items)WriteCommonResult(msg,p.first,-p.second);msg<<MissionResult{}<<LocalPayback{};return msg;}
inline CMessage& operator>>(CMessage& msg,LocalUnionResult&){return msg;}
inline void AppendTextOut(String& s,LocalUnionResult&){s+=L"<UnionResult>";}
}
'''
p.write_text(s)
p=root/'Server/GrandCrossLocalServer.cpp';s=p.read_text()
for name in ['TownInfo','TownChest','ArtifactUnion']:
 s='#include "Protocol/Generated/SevenDS'+name+'C2S_stub.h"\n#include "Protocol/Generated/SevenDS'+name+'S2C_proxy.h"\n'+s
code='''SevenDSTownInfoS2C::Proxy g_townInfoProxy;
class TownInfoStub final : public SevenDSTownInfoC2S::Stub {public:DECRMI_SevenDSTownInfoC2S_CG_RequestBasePointInfo;} g_townInfoStub;
DEFRMI_SevenDSTownInfoC2S_CG_RequestBasePointInfo(TownInfoStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(!GcLocal::KnownTown(basePointID))return CancelRequest(remote,10008);g_townInfoProxy.CG_RequestBasePointInfoOK(remote,RmiContext::ReliableSend,LocalTownInfoResult{basePointID});return true;}
SevenDSTownChestS2C::Proxy g_townChestProxy;
class TownChestStub final : public SevenDSTownChestC2S::Stub {public:DECRMI_SevenDSTownChestC2S_CG_RequestBasePointUniqueInteractiveOpen;} g_townChestStub;
DEFRMI_SevenDSTownChestC2S_CG_RequestBasePointUniqueInteractiveOpen(TownChestStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const GcLocal::TownChest* row=nullptr;for(const auto& r:GcLocal::TownChests)if(r.npc==npcID)row=&r;if(!row||(row->quest&&!GcLocal::QuestCompleted(row->quest)))return CancelRequest(remote,10904);int item=0;if(GcLocal::OpenChests().insert(npcID).second){GcLocal::Grant(row->item,row->count);item=row->item;GcLocal::SaveChests();GcLocal::RecordMission(31,0,1);GcLocal::RecordQuestAction("unique_interactive",npcID,1);}g_townChestProxy.CG_RequestBasePointUniqueInteractiveOpenOK(remote,RmiContext::ReliableSend,LocalChestResult{npcID,item});return true;}
SevenDSArtifactUnionS2C::Proxy g_artifactUnionProxy;
class ArtifactUnionStub final : public SevenDSArtifactUnionC2S::Stub {public:DECRMI_SevenDSArtifactUnionC2S_CG_RequestArtifactUnionUpgrade;} g_artifactUnionStub;
DEFRMI_SevenDSArtifactUnionC2S_CG_RequestArtifactUnionUpgrade(ArtifactUnionStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const auto* r=GcLocal::FindArtifactUnion(request.id);if(!r||r->cap<=0)return CancelRequest(remote,12602);for(int card:r->cards)if(card&&!GcLocal::Artifacts().count(card))return CancelRequest(remote,12602);int64_t gain=0;for(auto p:request.items){int exp=0;for(auto m:GcLocal::UnionMaterials)if(m.id==p.first)exp=m.exp;if(!exp)return CancelRequest(remote,12602);gain+=int64_t(exp)*p.second;}int current=GcLocal::ArtifactUnionExperience()[request.id];if(current>=r->cap||gain<=0)return CancelRequest(remote,12602);if(!GcLocal::Spend(request.items))return CancelRequest(remote,12602,101);GcLocal::ArtifactUnionExperience()[request.id]=int(std::min<int64_t>(r->cap,int64_t(current)+gain));GcLocal::SaveArtifactUnions();g_artifactUnionProxy.CG_RequestArtifactUnionUpgradeOK(remote,RmiContext::ReliableSend,LocalUnionResult{request.id,request.items});return true;}
'''
marker='// This is deliberately a transport-only';assert marker in s;s=s.replace(marker,code+'\n'+marker)
s=s.replace('    server->AttachProxy(&g_foodProxy);','    server->AttachProxy(&g_townInfoProxy);server->AttachStub(&g_townInfoStub);\n    server->AttachProxy(&g_townChestProxy);server->AttachStub(&g_townChestStub);\n    server->AttachProxy(&g_artifactUnionProxy);server->AttachStub(&g_artifactUnionStub);\n    server->AttachProxy(&g_foodProxy);')
p.write_text(s)
specs=[('TownInfo',10008,'CG_RequestBasePointInfo([in] int basePointID)',14013,'CG_RequestBasePointInfoOK','LocalTownInfoResult'),('TownChest',10904,'CG_RequestBasePointUniqueInteractiveOpen([in] int npcID)',14304,'CG_RequestBasePointUniqueInteractiveOpenOK','LocalChestResult'),('ArtifactUnion',12602,'CG_RequestArtifactUnionUpgrade([in] LocalUnionRequest request)',15092,'CG_RequestArtifactUnionUpgradeOK','LocalUnionResult')]
for name,rid,method,response,ok,record in specs:
 for side,base,definition in [('C2S',rid-1,method),('S2C',response-1,ok+'([in] '+record+' result)')]:
  (root/f'Server/Protocol/SevenDS{name}{side}.PIDL').write_text('#include "GrandCrossRmiTypes.h"\nglobal SevenDS'+name+side+' '+str(base)+'\n{\n '+definition+';\n}\n')
