from pathlib import Path
p=Path('E:/7DS-Offline');f=p/'Server/GrandCrossLocalServer.cpp';s=f.read_text();old='''  auto& count=GcLocal::ExtraItems()[row->item];
  count=int((std::min)(int64_t(2000000000),int64_t((std::max)(GcLocal::TestMaterialCount,count))+request.count*row->count));
  GcLocal::SaveExtraInventory();''';new='''  if(GcLocal::CustomMode()){
   auto& count=GcLocal::ExtraItems()[row->item];
   count=int((std::min)(int64_t(2000000000),int64_t((std::max)(GcLocal::TestMaterialCount,count))+request.count*row->count));
   GcLocal::SaveExtraInventory();
  }''';assert old in s;s=s.replace(old,new)
s=s.replace('#include "Protocol/Generated/SevenDSChapterC2S_stub.h"','#include "Protocol/Generated/SevenDSChapterSkipC2S_stub.h"\n#include "Protocol/Generated/SevenDSChapterSkipS2C_proxy.h"\n#include "Protocol/Generated/SevenDSChapterC2S_stub.h"')
marker='// This is deliberately a transport-only';idx=s.index(marker)
handler='''
SevenDSChapterSkipS2C::Proxy g_chapterSkipProxy;
class ChapterSkipStub final : public SevenDSChapterSkipC2S::Stub {public: DECRMI_SevenDSChapterSkipC2S_CG_RequestItemUseChapterSkip;} g_chapterSkipStub;
DEFRMI_SevenDSChapterSkipC2S_CG_RequestItemUseChapterSkip(ChapterSkipStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 const auto* rule=GcLocal::FindChapterSkip(skipID);
 if(!rule||rule->cost<1||rule->quests.empty())return CancelRequest(remote,11112);
 if(rule->previous){const auto* prev=GcLocal::FindChapterSkip(rule->previous);if(!prev||prev->quests.empty())return CancelRequest(remote,11112);for(int q:prev->quests)if(!GcLocal::QuestCompleted(q))return CancelRequest(remote,11112);}
 LocalChapterSkipResult result;result.cost=rule->cost;
 for(int id:rule->quests)if(!GcLocal::QuestCompleted(id)){if(!GcLocal::FindQuest(id))return CancelRequest(remote,11112);result.quests.push_back(id);}
 for(int id:rule->stages)if(!GcLocal::BattleClears().count({0,id}))result.stages.push_back(id);
 if(result.quests.empty()&&result.stages.empty())return CancelRequest(remote,11112);
 if(!GcLocal::Spend({{500035,rule->cost}}))return CancelRequest(remote,11112,101);
 for(int id:result.quests){GcLocal::StartQuest(id);auto& state=GcLocal::Quests()[id];state.status=2;state.progress=GcLocal::FindQuest(id)->requirements;
  for(auto r:GcLocal::QuestRewards)if(r.quest==id){auto rewards=GrantCampaignReward(r.type,r.item,r.count);result.rewards.insert(result.rewards.end(),rewards.begin(),rewards.end());}
  const auto* qrule=GcLocal::FindQuestRule(id);if(qrule&&qrule->story)GcLocal::RecordMission(37,0,1);
 }
 for(int id:result.stages){GcLocal::BattleClears().insert({0,id});const auto* row=GcLocal::FindCampaignStage(0,id);if(row&&row->main&&id>GcLocal::MainStageClear()){GcLocal::MainStageClear()=id;result.topStage=id;}
  for(const auto& stage:GcLocal::EconomyStages)if(stage.mode==0&&stage.id==id&&stage.firstItem&&stage.firstCount){auto rewards=GrantCampaignReward(GcLocal::FindMaterialType(stage.firstItem),stage.firstItem,stage.firstCount);result.rewards.insert(result.rewards.end(),rewards.begin(),rewards.end());break;}
 }
 for(int id:result.quests){int next=GcLocal::FindQuest(id)->next;if(next&&GcLocal::FindQuest(next)&&!GcLocal::Quests().count(next))GcLocal::StartQuest(next);}
 GcLocal::RefreshQuestSnapshots();GcLocal::SaveQuests();GcLocal::SaveStoryProgress();GcLocal::SaveBattleProgress();
 g_chapterSkipProxy.CG_RequestItemUseChapterSkipOK(remote,RmiContext::ReliableSend,result);return true;
}

'''
s=s[:idx]+handler+s[idx:];s=s.replace('server->AttachProxy(&g_chapterProxy);server->AttachStub(&g_chapterStub);','server->AttachProxy(&g_chapterProxy);server->AttachStub(&g_chapterStub);\n    server->AttachProxy(&g_chapterSkipProxy);server->AttachStub(&g_chapterSkipStub);');f.write_text(s)
f=p/'Server/Protocol/GrandCrossRmiTypes.h';s=f.read_text();s=s.replace('#include "LocalQuestState.h"','#include "LocalQuestState.h"\n#include "LocalChapterSkipCatalog.h"');s=s.replace('std::vector<std::pair<int,int>> drops; };','std::vector<std::pair<int,int>> drops; bool omitClearReward=false; };',1);s=s.replace('const int diamondReward=value.win ? GcLocal::StageDiamondReward() : 0;','const int diamondReward=value.win && !value.omitClearReward ? GcLocal::StageDiamondReward() : 0;');s=s.replace('struct LocalChapterResult {','struct LocalChapterSkipResult {int cost=0,topStage=0;std::vector<int> quests,stages;std::vector<LocalNativeReward> rewards;};\nstruct LocalChapterResult {')
s+='''
inline CMessage& operator<<(CMessage& msg,const LocalChapterSkipResult& v){
 WriteCommonResult(msg,500035,-v.cost);
 msg.WriteScalar(int32_t(v.quests.size()));for(int id:v.quests)msg<<int32_t(id);
 msg.WriteScalar(int32_t(v.stages.size()));for(int id:v.stages)msg<<int32_t(id);
 msg.WriteScalar(int32_t(0)); // Boss clear list: story skip rules contain no boss-mode stages.
 msg.WriteScalar(int32_t(0)); // Quest state refresh follows the native result.
 msg.WriteScalar(int32_t(v.topStage?1:0));if(v.topStage){LocalStageClearResult top;top.stage=v.topStage;top.win=true;top.first=true;top.omitClearReward=true;msg<<top;}
 msg.WriteScalar(int32_t(v.rewards.size()));for(auto r:v.rewards)WriteNativeReward(msg,r);
 msg<<MissionResult{};msg.WriteScalar(int32_t(0));
 msg.WriteScalar(int32_t(GcLocal::Quests().size()));for(auto q:GcLocal::Quests())WriteQuest(msg,q.first);
 return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalChapterSkipResult&){return msg;}
inline void AppendTextOut(String& out,LocalChapterSkipResult&){out+=L"<ChapterSkip>";}
''';f.write_text(s)
for ns,base,method in [('SevenDSChapterSkipC2S',11111,'CG_RequestItemUseChapterSkip([in] int32_t skipID);'),('SevenDSChapterSkipS2C',14550,'CG_RequestItemUseChapterSkipOK([in] LocalChapterSkipResult result);')]:
 (p/f'Server/Protocol/{ns}.PIDL').write_text('#include "GrandCrossRmiTypes.h"\nglobal %s %d\n{\n %s\n}\n'%(ns,base,method))
f=p/'Tools/generate_local_gacha_catalog.py';s=f.read_text();s+='\nif __name__==\'__main__\':\n runpy.run_path(str(root/\'Tools/package_hidden_heroes.py\'),run_name=\'__main__\')\n';f.write_text(s)
