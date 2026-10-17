from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=root/'Server/Protocol/GrandCrossRmiTypes.h';s=p.read_text()
s=s.replace('#include "LocalProgressionState.h"','#include "LocalProgressionState.h"\n#include "LocalFoodState.h"')
s=s.replace('struct LocalCookingRequest {','struct LocalFoodResult {int item=0,recipe=0;bool toggle=false;};\nstruct LocalCookingRequest {')
s=s.replace('else if(index==432)', 'else if(index==467){const auto& food=GcLocal::Food();msg<<int32_t(food.item)<<uint8_t(food.used)<<food.automatic;index+=2;}\n        else if(index==432)')
s=s.replace('msg << MissionResult{} << false; WriteZeroSchema(msg,"ibo"); WriteZeroSchema(msg,"bibiiiiioi");','msg << MissionResult{} << false;const auto& food=GcLocal::Food();msg<<int32_t(food.item)<<uint8_t(food.used)<<food.automatic;if(GcLocal::AutoFoodConsumed())WriteCommonResult(msg,GcLocal::AutoFoodConsumed(),-1);else WriteZeroSchema(msg,"bibiiiiioi");')
# WriteCommonResult is defined below StageStart, so forward declare it.
s=s.replace('inline CMessage& operator<<(CMessage& msg, const LocalStageStartResult& value)', 'inline void WriteCommonResult(CMessage&,int,int);\ninline CMessage& operator<<(CMessage& msg, const LocalStageStartResult& value)')
s+='''
namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalFoodResult& v){
 if(v.recipe)msg<<int32_t(v.recipe)<<int32_t(GcLocal::RecipeExperience()[v.recipe])<<true;
 else {const auto& s=GcLocal::Food();msg<<int32_t(s.item)<<uint8_t(s.used)<<s.automatic;}
 if(!v.toggle){if(v.item)WriteCommonResult(msg,v.item,-1);else msg<<LocalNoItem{};msg<<MissionResult{};WriteQuestProgressList(msg);}return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalFoodResult&){return msg;}
inline void AppendTextOut(String& s,LocalFoodResult&){s+=L"<FoodResult>";}
}
'''
p.write_text(s)
p=root/'Server/GrandCrossLocalServer.cpp';s=p.read_text()
for name in ['Food','FoodAuto','RecipeActive']:
 s='#include "Protocol/Generated/SevenDS'+name+'C2S_stub.h"\n#include "Protocol/Generated/SevenDS'+name+'S2C_proxy.h"\n'+s
marker='inline void CaptureBattleParty(int remote,int teamIndex)'
code='''inline void GrantPvpExemptions(){
 // Both account modes receive native PvP rewards once, without replaying unrelated progression.
 for(auto& p:GcLocal::Missions()){
  for(;;){const auto* r=GcLocal::FindMission(p.first,p.second.claimed+1);if(!r||!GcLocal::PvpMissionType(r->type))break;
   if(r->item&&r->count>0)GrantCampaignReward(GcLocal::FindMaterialType(r->item),r->item,r->count);
   p.second.claimed=r->index;p.second.progress=0;GcLocal::SaveMissions();
  }
 }
 for(int id:GcLocal::PvpQuestIds){const auto* q=GcLocal::FindQuest(id);if(!q||GcLocal::QuestCompleted(id))continue;
  GcLocal::StartQuest(id);for(auto r:GcLocal::QuestRewards)if(r.quest==id)GrantCampaignReward(r.type,r.item,r.count);
  GcLocal::Quests()[id].status=2;GcLocal::Quests()[id].progress=q->requirements;GcLocal::SaveQuests();
 }
 for(auto r:GcLocal::PvpUnlockItems)if(!GcLocal::PvpGrantedProducts().count(r.source)){
  const int type=GcLocal::FindMaterialType(r.item);if(!type||r.count<=0)continue;
  auto grants=GrantCampaignReward(type,r.item,r.count);if(grants.empty())continue;
  GcLocal::PvpGrantedProducts().insert(r.source);GcLocal::SavePvpGrants();
 }
}
'''
assert marker in s;s=s.replace(marker,code+marker)
s=s.replace('auto& party=GcLocal::ActiveBattleHeroes()[remote];party.clear();','GcLocal::AutoFoodConsumed()=GcLocal::PrepareBattleFood(remote);\n auto& party=GcLocal::ActiveBattleHeroes()[remote];party.clear();')
s=s.replace('LocalStageClearResult result;result.stage=id;result.win=win;result.first=first;', 'LocalStageClearResult result;result.stage=id;result.win=win;result.first=first;GcLocal::FinishBattleFood(remote);')
s=s.replace('    LoginUserResultInfo user;','    {std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);GrantPvpExemptions();}\n    LoginUserResultInfo user;')
code='''SevenDSFoodS2C::Proxy g_foodProxy;
class FoodStub final : public SevenDSFoodC2S::Stub {public:DECRMI_SevenDSFoodC2S_CG_RequestCookingUseCookingBuff;} g_foodStub;
DEFRMI_SevenDSFoodC2S_CG_RequestCookingUseCookingBuff(FoodStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(!GcLocal::EatFood(foodItemID,isAutoUse))return CancelRequest(remote,10876,101);g_foodProxy.CG_RequestCookingUseCookingBuffOK(remote,RmiContext::ReliableSend,LocalFoodResult{foodItemID});return true;}
SevenDSFoodAutoS2C::Proxy g_foodAutoProxy;
class FoodAutoStub final : public SevenDSFoodAutoC2S::Stub {public:DECRMI_SevenDSFoodAutoC2S_CG_RequestFoodBuffAutoUseOnOff;} g_foodAutoStub;
DEFRMI_SevenDSFoodAutoC2S_CG_RequestFoodBuffAutoUseOnOff(FoodAutoStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);GcLocal::Food().automatic=isAutoUse;GcLocal::SaveFood();g_foodAutoProxy.CG_RequestFoodBuffAutoUseOnOffOK(remote,RmiContext::ReliableSend,LocalFoodResult{0,0,true});return true;}
SevenDSRecipeActiveS2C::Proxy g_recipeActiveProxy;
class RecipeActiveStub final : public SevenDSRecipeActiveC2S::Stub {public:DECRMI_SevenDSRecipeActiveC2S_CG_RequestRecipeActive;} g_recipeActiveStub;
DEFRMI_SevenDSRecipeActiveC2S_CG_RequestRecipeActive(RecipeActiveStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);int item=0;for(auto r:GcLocal::RecipeBooks)if(r.recipe==recipeID){item=r.item;break;}if(!item)return CancelRequest(remote,10870);if(!GcLocal::RecipeExperience().count(recipeID)){if(!GcLocal::Spend({{item,1}}))return CancelRequest(remote,10870,101);GcLocal::RecipeExperience()[recipeID]=0;GcLocal::SaveRecipes();GcLocal::RecordMission(68,0,1);}else item=0;g_recipeActiveProxy.CG_RequestRecipeActiveOK(remote,RmiContext::ReliableSend,LocalFoodResult{item,recipeID});return true;}
'''
marker='// This is deliberately a transport-only';assert marker in s;s=s.replace(marker,code+'\n'+marker)
s=s.replace('    server->AttachProxy(&g_chapterProxy);','    server->AttachProxy(&g_foodProxy);server->AttachStub(&g_foodStub);\n    server->AttachProxy(&g_foodAutoProxy);server->AttachStub(&g_foodAutoStub);\n    server->AttachProxy(&g_recipeActiveProxy);server->AttachStub(&g_recipeActiveStub);\n    server->AttachProxy(&g_chapterProxy);')
p.write_text(s)
specs=[('Food',10876,'CG_RequestCookingUseCookingBuff([in] int foodItemID,[in] bool isAutoUse)',14236,'CG_RequestCookingUseCookingBuffOK'),('FoodAuto',11103,'CG_RequestFoodBuffAutoUseOnOff([in] bool isAutoUse)',14543,'CG_RequestFoodBuffAutoUseOnOffOK'),('RecipeActive',10870,'CG_RequestRecipeActive([in] int recipeID)',14230,'CG_RequestRecipeActiveOK')]
for name,rid,method,response,ok in specs:
 for side,base,definition in [('C2S',rid-1,method),('S2C',response-1,ok+'([in] LocalFoodResult result)')]:
  (root/f'Server/Protocol/SevenDS{name}{side}.PIDL').write_text('#include "GrandCrossRmiTypes.h"\nglobal SevenDS'+name+side+' '+str(base)+'\n{\n '+definition+';\n}\n')
