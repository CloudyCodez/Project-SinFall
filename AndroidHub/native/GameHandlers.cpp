#include <android/log.h>
#include <cstdio>
#include <memory>
#include <string>
#include "Windows.h"

#include "PhoneProtocol.h"
#include "Protocol/GrandCrossRmiTypes.h"
#include "Protocol/LocalEconomyCatalog.h"
#include "Protocol/LocalCampaignRewards.h"

#include "Protocol/LocalQuestCatalog.inc"
using namespace Proud;

namespace {


SevenDSCancelS2C::Proxy g_cancelProxy;
inline bool CancelRequest(HostID remote,int request,int error=100) {
    g_cancelProxy.CG_CommonCancel(remote,RmiContext::ReliableSend,LocalCancelResult{request,error});return true;
}
SevenDSArtifactTeamS2C::Proxy g_artifactTeamProxy;
class ArtifactTeamStub final : public SevenDSArtifactTeamC2S::Stub {
public: DECRMI_SevenDSArtifactTeamC2S_CG_RequestArtifactTeamChange;
    DECRMI_SevenDSArtifactTeamC2S_CG_RequestArtifactDescentBossTeamChange;
} g_artifactTeamStub;
DEFRMI_SevenDSArtifactTeamC2S_CG_RequestArtifactTeamChange(ArtifactTeamStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    std::set<int> selected;
    for(int id:request.team.cards)if(id && (!GcLocal::Artifacts().count(id)||!selected.insert(id).second))return CancelRequest(remote,12603);
    GcLocal::ArtifactTeams()[request.team.index]=request.team;GcLocal::SaveArtifactTeams();
    g_artifactTeamProxy.CG_RequestArtifactTeamChangeOK(remote,RmiContext::ReliableSend);return true;
}
DEFRMI_SevenDSArtifactTeamC2S_CG_RequestArtifactDescentBossTeamChange(ArtifactTeamStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    std::set<int> indices;
    for(const auto& t:request.teams){
        if(!indices.insert(t.team.index).second)return CancelRequest(remote,12604);
        std::set<int> cards;
        for(int id:t.team.cards)if(id&&(!GcLocal::Artifacts().count(id)||!cards.insert(id).second))return CancelRequest(remote,12604);
    }
    for(const auto& t:request.teams)GcLocal::ArtifactTeams()[t.team.index]=t.team;
    GcLocal::SaveArtifactTeams();
    g_artifactTeamProxy.CG_RequestArtifactDescentBossTeamChangeOK(remote,RmiContext::ReliableSend);return true;
}
inline std::vector<std::pair<int,int>> DevelopmentCosts(int hero,int kind,int level,int rating=0) {
    for(const auto& row:GcLocal::EconomyCosts)if(row.hero==hero && row.kind==kind && row.level==level && (!rating||!row.rating||row.rating==rating)){
        std::vector<std::pair<int,int>> result;for(int i=0;i<5;++i)if(row.items[i]&&row.counts[i])result.emplace_back(row.items[i],row.counts[i]);return result;
    }
    if(GcLocal::CustomMode())return {};throw std::runtime_error("Missing native development recipe");
}
SevenDSTrueAwakeningS2C::Proxy g_trueProxy;
class TrueAwakeningStub final : public SevenDSTrueAwakeningC2S::Stub {
public: DECRMI_SevenDSTrueAwakeningC2S_CG_RequestSkinExceed;
} g_trueStub;
DEFRMI_SevenDSTrueAwakeningC2S_CG_RequestSkinExceed(TrueAwakeningStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    int skin=GcLocal::ActiveSkin(hero);const auto* row=GcLocal::DevelopmentRow(skin);
    if(!row||rank!=1||(type!=1&&type!=2))return CancelRequest(remote,10116);
    auto& state=GcLocal::DevelopmentStates()[skin];
    if(GcLocal::SkinLevel(skin)<100||state.awaken<6||state.transcend<6||(type==1?state.exceed:state.exceedSupreme)||(type==2&&!state.exceed))return CancelRequest(remote,10116);
    const GcLocal::TrueAwakeningRecipe* recipe=nullptr;
    for(const auto& r:GcLocal::TrueAwakeningRecipeRows)if(r.hero_id==hero&&r.exceed_type==type){recipe=&r;break;}
    if(!recipe)return CancelRequest(remote,10116);
    std::vector<std::pair<int,int>> costs={{recipe->exceed_price_id,recipe->exceed_price_count}};
    const int items[]={recipe->exceed_material_id_1,recipe->exceed_material_id_2,recipe->exceed_material_id_3,recipe->exceed_material_id_4};
    const int counts[]={recipe->exceed_material_count_1,recipe->exceed_material_count_2,recipe->exceed_material_count_3,recipe->exceed_material_count_4};
    for(int i=0;i<4;++i)if(items[i]&&counts[i])costs.emplace_back(items[i],counts[i]);
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10116,101);
    if(type==1)state.exceed=1;else state.exceedSupreme=1;state.exceedSelect=type;GcLocal::SaveDevelopment();
    LocalSystemsResult result;result.kind=30;result.skin=skin;result.items=costs;
    g_trueProxy.CG_RequestSkinExceedOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSTrueSelectS2C::Proxy g_trueSelectProxy;
class TrueSelectStub final : public SevenDSTrueSelectC2S::Stub {
public: DECRMI_SevenDSTrueSelectC2S_CG_RequestSkinExceedSelect;
} g_trueSelectStub;
DEFRMI_SevenDSTrueSelectC2S_CG_RequestSkinExceedSelect(TrueSelectStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);int skin=GcLocal::ActiveSkin(hero);
    if(!skin||(type!=1&&type!=2))return CancelRequest(remote,13695);
    auto& s=GcLocal::DevelopmentStates()[skin];if(type==1?!s.exceed:!s.exceedSupreme)return CancelRequest(remote,13695);
    s.exceedSelect=type;GcLocal::SaveDevelopment();LocalSystemsResult r;r.kind=31;r.skin=skin;
    g_trueSelectProxy.CG_RequestSkinExceedSelectOK(remote,RmiContext::ReliableSend,r);return true;
}
SevenDSRelicS2C::Proxy g_relicProxy;
class RelicStub final : public SevenDSRelicC2S::Stub {
public: DECRMI_SevenDSRelicC2S_CG_RequestCostumeCraft;
} g_relicStub;
DEFRMI_SevenDSRelicC2S_CG_RequestCostumeCraft(RelicStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    const GcLocal::RelicRecipe* recipe=nullptr;
    for(const auto& r:GcLocal::RelicRecipeRows)if(r.costume_id==costume){recipe=&r;break;}
    if(!recipe||!GcLocal::FindCosmetic(costume)||GcLocal::OwnCosmetic(costume))return CancelRequest(remote,10107);
    std::vector<std::pair<int,int>> costs;
    if(quick){if(!recipe->quick_token)return CancelRequest(remote,10107);costs.emplace_back(recipe->quick_token,1);}
    else {costs.emplace_back(recipe->need_gold_id,recipe->need_gold);
        const int items[]={recipe->need_item_1,recipe->need_item_2,recipe->need_item_3,recipe->need_item_4};
        const int counts[]={recipe->need_item_count_1,recipe->need_item_count_2,recipe->need_item_count_3,recipe->need_item_count_4};
        for(int i=0;i<4;++i)if(items[i]&&counts[i])costs.emplace_back(items[i],counts[i]);}
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10107,101);
    GcLocal::CraftedCosmetics().insert(costume);GcLocal::SaveCraftedCosmetics();
    LocalSystemsResult r;r.kind=32;r.other=costume;r.items=costs;g_relicProxy.CG_RequestCostumeCraftOK(remote,RmiContext::ReliableSend,r);return true;
}
SevenDSQuestS2C::Proxy g_questProxy;
SevenDSMailS2C::Proxy g_mailProxy;
class MailStub final : public SevenDSMailC2S::Stub {
public: DECRMI_SevenDSMailC2S_CG_RequestMailList;
 DECRMI_SevenDSMailC2S_CG_RequestMailConfirm;
 DECRMI_SevenDSMailC2S_CG_RequestMailConfirmAll;
} g_mailStub;
DEFRMI_SevenDSMailC2S_CG_RequestMailList(MailStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);g_mailProxy.CG_RequestMailListOK(remote,RmiContext::ReliableSend,LocalMailResult{});return true;}
DEFRMI_SevenDSMailC2S_CG_RequestMailConfirm(MailStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(serial!=1||multi||!GcLocal::ClaimWelcome())return CancelRequest(remote,10452);g_mailProxy.CG_RequestMailConfirmOK(remote,RmiContext::ReliableSend,LocalMailResult{1,true});return true;}
DEFRMI_SevenDSMailC2S_CG_RequestMailConfirmAll(MailStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);bool claimed=GcLocal::ClaimWelcome();g_mailProxy.CG_RequestMailConfirmAllOK(remote,RmiContext::ReliableSend,LocalMailResult{2,claimed});return true;}
inline const GcLocal::EconomyStage* EconomyStage(int mode,int id){if(mode==6)for(const auto& r:GcLocal::DescentEconomy)if(r.id==id)return &r;if(mode==5)for(const auto& r:GcLocal::FinalBossEconomy)if(r.id==id)return &r;for(const auto& r:GcLocal::EconomyStages)if(r.mode==mode&&r.id==id)return &r;return nullptr;}
inline bool PayStage(int mode,int id) {
    const auto* row=EconomyStage(mode,id);if(!row|| (row->staminaItem&&row->stamina&&!GcLocal::Spend({{row->staminaItem,row->stamina}})))return false;
    if(row->stamina)GcLocal::RecordMission(12,0,row->stamina);return true;
}
inline std::vector<LocalNativeReward> GrantCampaignReward(int type,int item,int count){
 std::vector<LocalNativeReward> rewards;
 if(type<200){GcLocal::Grant(item,count);rewards.push_back({type,item,count,0});}
 else if(type==211){const auto* skin=GcLocal::FindSkin(item);if(!skin)return rewards;
   if(!GcLocal::OwnedHeroes().count(skin->hero)){rewards.push_back({210,skin->hero,1,0});GcLocal::OwnedSkins().insert(item);rewards.push_back({211,item,1,0});GcLocal::SaveAccount();}
   else for(auto c:GcLocal::HeroCoins)if(c.skin==item){GcLocal::Grant(c.coin,count);rewards.push_back({GcLocal::FindMaterialType(c.coin),c.coin,count,0});break;}
 }else if(type==212&&GcLocal::EquipmentBaseRow(item)){for(int i=0;i<count;++i){auto& w=GcLocal::CreateEquipment(item);rewards.push_back({212,item,1,w.serial});}GcLocal::SaveEquipments();}
 else if(type==216){GcLocal::Artifacts().insert(item);GcLocal::SaveExtraInventory();rewards.push_back({216,item,count,0});}
 else if(type>=213&&type<=215&&GcLocal::FindCosmetic(item)){GcLocal::CraftedCosmetics().insert(item);GcLocal::SaveCraftedCosmetics();rewards.push_back({type,item,count,0});}
 return rewards;
}
void GrantPvpExemptions(){
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
  const int type=r.type;if(!type||r.count<=0)continue;
  auto grants=GrantCampaignReward(type,r.item,r.count);if(grants.empty())continue;
  GcLocal::PvpGrantedProducts().insert(r.source);GcLocal::SavePvpGrants();
 }
}
inline void CaptureBattleParty(int remote,int teamIndex){
 GcLocal::AutoFoodConsumed()=GcLocal::PrepareBattleFood(remote);
 auto& party=GcLocal::ActiveBattleHeroes()[remote];party.clear();
 auto it=GcLocal::Teams().find(teamIndex);if(it==GcLocal::Teams().end())return;
 std::set<int> seen;
 for(auto slot:it->second.slots)if(GcLocal::OwnedSkins().count(slot.skin)&&GcLocal::FindSkin(slot.skin)->hero==slot.hero&&seen.insert(slot.hero).second)party.push_back(slot.skin);
}
inline LocalStageClearResult CompleteStage(int mode,int id,bool win,bool first,int remote) {
    const int goldBonus=GcLocal::BattleFoodBonus(remote,true),experienceBonus=GcLocal::BattleFoodBonus(remote,false);
    LocalStageClearResult result;result.stage=id;result.win=win;result.first=first;GcLocal::FinishBattleFood(remote);
    if(!win)return result;
    GcLocal::RecordQuestBattle(mode,id);
    GcLocal::RecordMission(mode==5?118:mode==1?7:mode==2?70:mode==3?71:(GcLocal::FindCampaignStage(0,id)&&GcLocal::FindCampaignStage(0,id)->main?8:71),0,1);
    GcLocal::Grant(500011,GcLocal::StageDiamondReward());
    const auto* row=EconomyStage(mode,id);if(!row)return result;
    GcLocal::AccountExperience()=int(std::min<int64_t>(2147483647LL,int64_t(GcLocal::AccountExperience())+(std::max)(0,row->userExp)));GcLocal::SaveAccountExperience();
    auto party=GcLocal::ActiveBattleHeroes().find(remote);
    if(party!=GcLocal::ActiveBattleHeroes().end())for(int skin:party->second){
      auto& state=GcLocal::DevelopmentStates()[skin];const int cap=GcLocal::ExperienceCap(skin);
      int gain=int(std::min<int64_t>((std::max)(0,cap-state.exp),(std::max)(int64_t(0),int64_t(row->heroExp)*(100+experienceBonus)/100)));
      state.exp+=gain;result.experience.emplace_back(skin,gain);
    }
    if(!result.experience.empty())GcLocal::SaveDevelopment();
    for(const auto& reward:GcLocal::CampaignRewards)if(reward.mode==mode&&reward.stage==id&&(!reward.first||first)){
      auto granted=GrantCampaignReward(reward.type,reward.item,reward.count);
      if(reward.first&&!granted.empty()){result.nativeFirst=granted.back();granted.pop_back();}
      result.nativeDrops.insert(result.nativeDrops.end(),granted.begin(),granted.end());
    }
    if(GcLocal::CustomMode())return result;
    result.gold=int(std::min<int64_t>(2147483647,int64_t(row->gold)*(100+goldBonus)/100));GcLocal::Grant(500012,result.gold);GcLocal::RecordMission(2,0,result.gold);
    if(mode!=0&&mode!=3&&first&&row->firstItem&&row->firstCount){result.firstReward={row->firstItem,row->firstCount};GcLocal::Grant(row->firstItem,row->firstCount);}
    std::map<int,int> drops;std::vector<const GcLocal::FarmingDrop*> entries;std::vector<double> weights;
    for(const auto& d:row->drops)if(d.item&&d.count&&d.weight>0){entries.push_back(&d);weights.push_back(d.weight);}
    static std::mt19937 rng(std::random_device{}());
    if(!entries.empty()){const auto* d=entries[std::discrete_distribution<size_t>(weights.begin(),weights.end())(rng)];drops[d->item]+=d->count;}
    if(mode==1&&GcLocal::EasyFarm()){
        for(const auto& d:row->drops)if(d.item&&d.count&&d.weight>0)drops[d.item]=(std::max)(drops[d.item],d.count*10);
        if(row->area==10){const int baseGold=result.gold;result.gold=(std::max)(baseGold,500000);GcLocal::Grant(500012,result.gold-baseGold);drops[500019]+=3;drops[5301001]+=10;drops[912089]+=1;}
        else if(row->area==1){drops[80000511]+=1;drops[541403]+=20;}
        else if(row->area==5){drops[543301]+=1;drops[543304]+=1;drops[542701]+=5;}
        else {drops[510101]+=20;drops[542701]+=3;}
    }
    for(auto p:drops){GcLocal::Grant(p.first,p.second);result.drops.push_back(p);}return result;
}
SevenDSEquipmentS2C::Proxy g_equipmentProxy;
class EquipmentStub final : public SevenDSEquipmentC2S::Stub {
public:
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipExchange;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipExchangeAll;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponSell;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponGrind;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipRecommend;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquip;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponUnEquip;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponUpgrade;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEvolution;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponUpgradeRetry;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEvolutionRetry;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponOptionEnhance;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponLock;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponUnLock;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponCarve;
    DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponCarveRemove;
} g_equipmentStub;
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipExchange(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    // Native requests use WeaponPartsType (1..6); saved slot arrays use 0..5.
    const int slotIndex=slot-1;
    if(slotIndex<0||slotIndex>5||pickedSkin==targetSkin||!GcLocal::OwnedSkins().count(pickedSkin)||!GcLocal::OwnedSkins().count(targetSkin))return CancelRequest(remote,10132);
    auto picked=GcLocal::Equipments().find(pickedSerial);
    if(picked==GcLocal::Equipments().end()||picked->second.skin!=pickedSkin||picked->second.slot!=slotIndex)return CancelRequest(remote,10132);
    int current=0;for(const auto& w:GcLocal::Equipments())if(w.second.skin==targetSkin&&w.second.slot==slotIndex){current=w.first;break;}
    if(current!=targetSerial)return CancelRequest(remote,10132);
    if(current){auto& displaced=GcLocal::Equipments().at(current);displaced.skin=0;displaced.slot=0;}
    picked->second.skin=targetSkin;picked->second.slot=slotIndex;GcLocal::SaveEquipments();
    LocalSystemsResult result;result.kind=11;result.skin=targetSkin;result.other=pickedSkin;result.serial=pickedSerial;result.serials.push_back(current);
    g_equipmentProxy.CG_RequestWeaponEquipExchangeOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipExchangeAll(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    if(targetSkin==sourceSkin||!GcLocal::OwnedSkins().count(targetSkin)||!GcLocal::OwnedSkins().count(sourceSkin)||(mode!=2&&mode!=3))return CancelRequest(remote,10133);
    LocalSystemsResult result;result.kind=12;result.skin=targetSkin;result.other=sourceSkin;
    for(auto& entry:GcLocal::Equipments()){
        auto& w=entry.second;
        if(w.skin==sourceSkin)w.skin=targetSkin;
        else if(w.skin==targetSkin){if(mode==3)w.skin=sourceSkin;else{w.skin=0;w.slot=0;result.serials.push_back(w.serial);}}
    }
    GcLocal::SaveEquipments();g_equipmentProxy.CG_RequestWeaponEquipExchangeAllOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponSell(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    if(request.ids.empty()||(sellType!=0&&sellType!=2)||basepoint!=0)return CancelRequest(remote,10123);
    std::set<int> selected;int currency=0;int64_t amount=0;
    for(int id:request.ids){auto it=GcLocal::Equipments().find(id);
        if(it==GcLocal::Equipments().end()||it->second.locked||it->second.skin||it->second.carve||!selected.insert(id).second)return CancelRequest(remote,10123);
        const GcLocal::EquipmentSale* sale=nullptr;for(const auto& r:GcLocal::EquipmentSaleRows)if(r.item_id==it->second.base){sale=&r;break;}
        if(!sale||!sale->sell_on||sale->sell_cost<0||(currency&&currency!=sale->sell_id))return CancelRequest(remote,10123);
        currency=sale->sell_id;amount+=sale->sell_cost;
    }
    if(!currency||amount>INT32_MAX)return CancelRequest(remote,10123);
    for(int id:request.ids)GcLocal::Equipments().erase(id);GcLocal::SaveEquipments();GcLocal::Grant(currency,int(amount));
    LocalSystemsResult result;result.kind=2;result.serials=request.ids;result.items.emplace_back(currency,int(amount));
    g_equipmentProxy.CG_RequestWeaponSellOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipRecommend(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    if(!GcLocal::OwnedSkins().count(skin)||request.ids.size()>6)return CancelRequest(remote,10134);
    std::set<int> selected,slots;
    for(int id:request.ids){
        auto it=GcLocal::Equipments().find(id);
        if(it==GcLocal::Equipments().end()||!selected.insert(id).second)return CancelRequest(remote,10134);
        const auto* base=GcLocal::EquipmentBaseRow(it->second.base);
        if(!base||base->weapon_parts<1||base->weapon_parts>6||!slots.insert(base->weapon_parts-1).second||
           (it->second.skin&&it->second.skin!=skin))return CancelRequest(remote,10134);
    }
    LocalSystemsResult result;result.kind=13;result.skin=skin;
    for(auto& p:GcLocal::Equipments())if(p.second.skin==skin){p.second.skin=0;p.second.slot=0;result.serials.push_back(p.first);}
    for(int id:request.ids){auto& w=GcLocal::Equipments().at(id);w.skin=skin;w.slot=GcLocal::EquipmentBaseRow(w.base)->weapon_parts-1;
        if(std::find(result.serials.begin(),result.serials.end(),id)==result.serials.end())result.serials.push_back(id);}
    GcLocal::SaveEquipments();g_equipmentProxy.CG_RequestWeaponEquipRecommendOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponGrind(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    if(request.ids.empty())return CancelRequest(remote,10124);
    std::set<int> selected;std::vector<const GcLocal::EquipmentGrind*> recipes;
    for(int id:request.ids){auto it=GcLocal::Equipments().find(id);
        if(it==GcLocal::Equipments().end()||it->second.locked||it->second.skin||it->second.carve||!selected.insert(id).second)return CancelRequest(remote,10124);
        const auto* base=GcLocal::EquipmentBaseRow(it->second.base);const GcLocal::EquipmentGrind* recipe=nullptr;
        for(const auto& r:GcLocal::EquipmentGrindRows)if(r.weapon_rating==base->weapon_rating&&r.weapon_enchant==it->second.evolution*5+it->second.upgrade&&r.fellowship_level==1){recipe=&r;break;}
        if(!recipe)return CancelRequest(remote,10124);recipes.push_back(recipe);
    }
    static std::mt19937 rng(std::random_device{}());std::map<int,int> rewards;LocalSystemsResult result;result.kind=3;result.serials=request.ids;
    for(const auto* r:recipes){int roll=std::uniform_int_distribution<int>(1,10000)(rng);
        int outcome=roll<=r->bonus_rate_1?0:roll<=r->bonus_rate_1+r->bonus_rate_2?1:2;
        int stones=outcome==0?r->grind_item_count_1:outcome==1?r->grind_item_count_2:r->grind_item_count_3;
        int evolutions=outcome==0?r->evolution_item_count_1:outcome==1?r->evolution_item_count_2:r->evolution_item_count_3;
        rewards[r->grind_item_id]+=stones;result.successes.emplace_back(stones,uint8_t(outcome));
        const int weights[]={r->evolution_item_rate_1,r->evolution_item_rate_2,r->evolution_item_rate_3,r->evolution_item_rate_4,r->evolution_item_rate_5,r->evolution_item_rate_6};
        int total=0;for(int w:weights)total+=w;
        for(int i=0;i<evolutions&&total>0;++i){int pick=std::uniform_int_distribution<int>(1,total)(rng);for(int j=0;j<6;++j){pick-=weights[j];if(pick<=0){++rewards[510101+j];break;}}}
    }
    for(int id:request.ids)GcLocal::Equipments().erase(id);GcLocal::SaveEquipments();
    GcLocal::RecordMission(22,0,int(request.ids.size()));GcLocal::RecordQuestAction("weapon_grind",0,int(request.ids.size()));
    for(auto p:rewards)if(p.second>0){GcLocal::Grant(p.first,p.second);result.items.push_back(p);}
    g_equipmentProxy.CG_RequestWeaponGrindOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponUpgradeRetry(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);
    if(it==GcLocal::Equipments().end())return CancelRequest(remote,10126);auto& w=it->second;const auto* base=GcLocal::EquipmentBaseRow(w.base);
    int cost=0;for(const auto& r:GcLocal::EquipmentBaseChangeRows)if(r.weapon_rating==base->weapon_rating){if(r.need_material_id_1==item)cost=r.need_material_count_1;else if(r.need_material_id_2==item)cost=r.need_material_count_2;else if(r.need_material_id_3==item)cost=r.need_material_count_3;}
    if(!cost)return CancelRequest(remote,10126);std::vector<std::pair<int,int>> costs={{item,cost}};
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10126,101);static std::mt19937 rng(std::random_device{}());
    w.value=std::uniform_int_distribution<int>(base->status_value_min,base->status_value_max)(rng);GcLocal::SaveEquipments();
    LocalSystemsResult r;r.kind=5;r.serial=serial;r.items=costs;g_equipmentProxy.CG_RequestWeaponUpgradeRetryOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEvolutionRetry(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);
    if(it==GcLocal::Equipments().end()||slot<0||slot>=int(it->second.options.size()))return CancelRequest(remote,10128);
    auto& w=it->second;const auto* base=GcLocal::EquipmentBaseRow(w.base);const GcLocal::EquipmentOptionChange* recipe=nullptr;
    for(const auto& r:GcLocal::EquipmentOptionChangeRows)if(r.weapon_rating==base->weapon_rating&&r.evolution_count==slot+1&&r.reroll&&r.change_material_id==item){recipe=&r;break;}
    if(!recipe)return CancelRequest(remote,10128);std::vector<std::pair<int,int>> costs={{item,recipe->change_material_count}};
    if(recipe->change_price_id&&recipe->change_price_count)costs.emplace_back(recipe->change_price_id,recipe->change_price_count);
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10128,101);
    std::vector<const GcLocal::EquipmentOption*> options;for(const auto& o:GcLocal::EquipmentOptionRows)if(o.random_option_group==base->random_option_id)options.push_back(&o);
    static std::mt19937 rng(std::random_device{}());const auto* o=options.at(std::uniform_int_distribution<size_t>(0,options.size()-1)(rng));
    w.options[slot]={o->id,std::uniform_int_distribution<int>(o->option_effect_min,o->option_effect_max)(rng)};GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=7;r.serial=serial;r.items=costs;
    g_equipmentProxy.CG_RequestWeaponEvolutionRetryOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponOptionEnhance(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);
    if(it==GcLocal::Equipments().end()||slot<0||slot>=int(it->second.options.size()))return CancelRequest(remote,10129);
    auto& w=it->second;const auto* base=GcLocal::EquipmentBaseRow(w.base);const GcLocal::EquipmentOptionChange* recipe=nullptr;
    for(const auto& r:GcLocal::EquipmentOptionChangeRows)if(r.weapon_rating==base->weapon_rating&&r.evolution_count==slot+1&&!r.reroll){recipe=&r;break;}
    if(!recipe)return CancelRequest(remote,10129);std::vector<std::pair<int,int>> costs={{recipe->change_material_id,recipe->change_material_count}};
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10129,101);
    static std::mt19937 rng(std::random_device{}());int increase=std::uniform_int_distribution<int>(1,100)(rng)<=recipe->option_rate_1?recipe->option_change_min_1:recipe->option_change_min_2;
    for(const auto& o:GcLocal::EquipmentOptionRows)if(o.id==w.options[slot].first)w.options[slot].second=(std::min)(o.option_effect_max,w.options[slot].second+increase);
    GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=8;r.serial=serial;r.items=costs;g_equipmentProxy.CG_RequestWeaponOptionEnhanceOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquip(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    // Convert the native one-based equipment part to the saved array index.
    const int slotIndex=slot-1;
    auto found=GcLocal::Equipments().find(serial);
    if(!GcLocal::OwnedSkins().count(skin)||found==GcLocal::Equipments().end()||slotIndex<0||slotIndex>=6)return CancelRequest(remote,10121);
    auto& w=found->second;const auto* base=GcLocal::EquipmentBaseRow(w.base);
    if(!base||base->weapon_parts!=slotIndex+1||w.skin)return CancelRequest(remote,10121);
    int previous=0;for(const auto& p:GcLocal::Equipments())if(p.second.skin==skin&&p.second.slot==slotIndex){previous=p.first;break;}
    // Keep displaced equipment rather than destructively deleting it.
    if(previous){GcLocal::Equipments().at(previous).skin=0;GcLocal::Equipments().at(previous).slot=0;}
    w.skin=skin;w.slot=slotIndex;GcLocal::SaveEquipments();LocalSystemsResult r;r.skin=skin;r.serial=serial;r.other=previous;
    g_equipmentProxy.CG_RequestWeaponEquipOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponUnEquip(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    const int slotIndex=slot-1;
    if(!GcLocal::OwnedSkins().count(skin)||slotIndex<0||slotIndex>=6)return CancelRequest(remote,10122);
    int serial=0;for(const auto& p:GcLocal::Equipments())if(p.second.skin==skin&&p.second.slot==slotIndex){serial=p.first;break;}
    if(!serial)return CancelRequest(remote,10122);auto& w=GcLocal::Equipments().at(serial);w.skin=0;w.slot=0;GcLocal::SaveEquipments();
    LocalSystemsResult r;r.kind=1;r.skin=skin;r.serial=serial;g_equipmentProxy.CG_RequestWeaponUnEquipOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponUpgrade(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);
    if(it==GcLocal::Equipments().end())return CancelRequest(remote,10125);auto& w=it->second;const auto* base=GcLocal::EquipmentBaseRow(w.base);
    if(w.upgrade>=5||gauge<0)return CancelRequest(remote,10125);
    const GcLocal::EquipmentUpgrade* recipe=nullptr;for(const auto& r:GcLocal::EquipmentUpgradeRows)if(r.weapon_rating==base->weapon_rating&&r.upgrade_level==w.evolution*5+w.upgrade+1){recipe=&r;break;}
    if(!recipe)return CancelRequest(remote,10125);
    std::vector<std::pair<int,int>> costs={{recipe->upgrade_material_id,recipe->upgrade_material_count},{recipe->upgrade_price_id,recipe->upgrade_price_count}};
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10125,101);
    // Native success probability; Custom avoids repeated material grinding.
    static std::mt19937 rng(std::random_device{}());bool success=GcLocal::CustomMode()||std::uniform_int_distribution<int>(1,10000)(rng)<=recipe->upgrade_per;if(success)++w.upgrade;
    GcLocal::RecordMission(success?20:21,0,1);GcLocal::RefreshQuestSnapshots();GcLocal::SaveQuests();
    GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=4;r.serial=serial;r.items=costs;
    g_equipmentProxy.CG_RequestWeaponUpgradeOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEvolution(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);
    if(it==GcLocal::Equipments().end())return CancelRequest(remote,10127);auto& w=it->second;const auto* base=GcLocal::EquipmentBaseRow(w.base);
    if(w.upgrade!=5||w.evolution>=5)return CancelRequest(remote,10127);
    const GcLocal::EquipmentEvolution* recipe=nullptr;for(const auto& r:GcLocal::EquipmentEvolutionRows)if(r.weapon_rating==base->weapon_rating&&r.evolution_count==w.evolution+1){recipe=&r;break;}
    if(!recipe)return CancelRequest(remote,10127);
    std::vector<std::pair<int,int>> costs={{recipe->evolution_material_id,recipe->evolution_material_count},{recipe->evolution_price_id,recipe->evolution_price_count}};
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10127,101);++w.evolution;w.upgrade=0;
    GcLocal::RecordMission(23,0,1);GcLocal::RefreshQuestSnapshots();GcLocal::SaveQuests();
    for(const auto& o:GcLocal::EquipmentOptionRows)if(o.random_option_group==base->random_option_id){w.options.emplace_back(o.id,o.option_effect_min);break;}
    GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=6;r.serial=serial;r.items=costs;
    g_equipmentProxy.CG_RequestWeaponEvolutionOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponLock(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);if(it==GcLocal::Equipments().end())return CancelRequest(remote,10130);
    it->second.locked=true;GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=9;r.serial=serial;g_equipmentProxy.CG_RequestWeaponLockOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponUnLock(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);if(it==GcLocal::Equipments().end())return CancelRequest(remote,10131);
    it->second.locked=false;GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=10;r.serial=serial;g_equipmentProxy.CG_RequestWeaponUnLockOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponCarve(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);
    if(it==GcLocal::Equipments().end()||!heroGroup)return CancelRequest(remote,10135);auto& w=it->second;const auto* base=GcLocal::EquipmentBaseRow(w.base);
    if(w.carve||w.upgrade!=5||w.evolution!=5)return CancelRequest(remote,10135);
    const GcLocal::EquipmentCarve* recipe=nullptr;for(const auto& r:GcLocal::EquipmentCarveRows)if(r.weapon_rating==base->weapon_rating&&r.weapon_parts==base->weapon_parts){recipe=&r;break;}
    if(!recipe)return CancelRequest(remote,10135);
    std::vector<std::pair<int,int>> costs={{recipe->carve_item_id_1,recipe->carve_item_count_1},{recipe->carve_item_id_2,recipe->carve_item_count_2},{recipe->carve_price_id,recipe->carve_price_count}};
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10135,101);w.carve=heroGroup;GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=14;r.serial=serial;r.items=costs;
    g_equipmentProxy.CG_RequestWeaponCarveOK(remote,RmiContext::ReliableSend,r);return true;
}
DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponCarveRemove(EquipmentStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);
    if(it==GcLocal::Equipments().end()||!it->second.carve)return CancelRequest(remote,10136);auto& w=it->second;const auto* base=GcLocal::EquipmentBaseRow(w.base);
    const GcLocal::EquipmentCarve* recipe=nullptr;for(const auto& r:GcLocal::EquipmentCarveRows)if(r.weapon_rating==base->weapon_rating&&r.weapon_parts==base->weapon_parts){recipe=&r;break;}
    if(!recipe)return CancelRequest(remote,10136);std::vector<std::pair<int,int>> costs={{recipe->carve_clear_price_id,recipe->carve_clear_price_count}};
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10136,101);w.carve=0;GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=15;r.serial=serial;r.items=costs;
    g_equipmentProxy.CG_RequestWeaponCarveRemoveOK(remote,RmiContext::ReliableSend,r);return true;
}
SevenDSBoxS2C::Proxy g_boxProxy;
class BoxStub final : public SevenDSBoxC2S::Stub {
public: DECRMI_SevenDSBoxC2S_CG_RequestItemUseBoxOpen;
} g_boxStub;
DEFRMI_SevenDSBoxC2S_CG_RequestItemUseBoxOpen(BoxStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    const GcLocal::ItemBox* row=nullptr;for(const auto& r:GcLocal::ItemBoxRows)if(r.item_id==request.item){row=&r;break;}
    if(!row||row->box_type!=1||request.count<1||request.count>1000)return CancelRequest(remote,11105);
    std::vector<std::pair<int,int>> drops;
    // Each recipe is a native fixed reward bundle, not a random/select box.
    const int* fields=&row->item_id_1;
    for(int i=0;i<20;++i)if(fields[i*3]&&fields[i*3+1])drops.emplace_back(fields[i*3],fields[i*3+1]*request.count);
    if(!GcLocal::Spend({{request.item,request.count}}))return CancelRequest(remote,11105,101);
    for(auto p:drops)GcLocal::Grant(p.first,p.second);
    LocalBoxResult r;r.item=request.item;r.drops=drops;g_boxProxy.CG_RequestItemUseBoxOpenOK(remote,RmiContext::ReliableSend,r);return true;
}
SevenDSEquipmentTicketS2C::Proxy g_equipmentTicketProxy;
class EquipmentTicketStub final : public SevenDSEquipmentTicketC2S::Stub {
public: DECRMI_SevenDSEquipmentTicketC2S_CG_RequestItemUseWeaponTicket;
} g_equipmentTicketStub;
DEFRMI_SevenDSEquipmentTicketC2S_CG_RequestItemUseWeaponTicket(EquipmentTicketStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    int growth=0;for(const auto& r:GcLocal::EquipmentTicketRows)if(r.item_id==item){growth=r.item_param_1;break;}
    const GcLocal::EquipmentGrowth* row=nullptr;for(const auto& r:GcLocal::EquipmentGrowthRows)if(r.id==growth){row=&r;break;}
    GcLocal::EquipmentGrowth selection{};
    int selectionGroup=0;for(const auto& r:GcLocal::EquipmentSelectionTicketRows)if(r.item_id==item){selectionGroup=r.item_param_1;break;}
    if(selectionGroup)for(const auto& r:GcLocal::EquipmentSelectionRows)if(r.id==selected&&r.select_group==selectionGroup&&r.item_id){
        selection={r.id,r.item_id,r.weapon_evolution_count,r.weapon_upgrade_count,0,r.weapon_status_amount,r.evolution_option_amount,r.fixed_option_tenths,r.evolution_option_1,r.evolution_option_2,r.evolution_option_3,r.evolution_option_4,r.evolution_option_5};row=&selection;break;
    }
    if(!row||!GcLocal::EquipmentBaseRow(row->item_id))return CancelRequest(remote,11108);
    if(!GcLocal::Spend({{item,1}}))return CancelRequest(remote,11108,101);
    auto& w=GcLocal::CreateEquipment(row->item_id);w.upgrade=row->weapon_upgrade_count;w.evolution=row->weapon_evolution_count;
    w.carve=row->is_carve?selected:0;const int opts[]={row->evolution_option_1,row->evolution_option_2,row->evolution_option_3,row->evolution_option_4,row->evolution_option_5};
    const auto* base=GcLocal::EquipmentBaseRow(w.base);
    for(int i=0;i<w.evolution&&i<5;++i)for(const auto& o:GcLocal::EquipmentOptionRows)if(selectionGroup?(o.random_option_group==base->random_option_id&&(opts[i]==0||o.id==opts[i])):o.id==opts[i]){w.options.emplace_back(o.id,row->fixed_option_tenths?row->fixed_option_tenths:o.option_effect_max);break;}
    GcLocal::SaveEquipments();LocalSystemsResult r;r.kind=33;r.serial=w.serial;r.other=item;
    g_equipmentTicketProxy.CG_RequestItemUseWeaponTicketOK(remote,RmiContext::ReliableSend,r);return true;
}
class QuestStub final : public SevenDSQuestC2S::Stub {
public: DECRMI_SevenDSQuestC2S_CG_RequestQuestStart;
    DECRMI_SevenDSQuestC2S_CG_RequestQuestProgress;
    DECRMI_SevenDSQuestC2S_CG_RequestQuestClear;
} g_questStub;
DEFRMI_SevenDSQuestC2S_CG_RequestQuestStart(QuestStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    int guide=GcLocal::GuideStepForQuest(questID);if(guide&&(guide!=GcLocal::Progression().guideStep||GcLocal::Progression().guideRewarded))return CancelRequest(remote,10801);
    if (!GcLocal::FindQuest(questID)||(!GcLocal::Quests().count(questID)&&!GcLocal::CanStartQuest(questID))) return CancelRequest(remote,10801);
    GcLocal::StartQuest(questID); GcLocal::SaveQuests();
    g_questProxy.CG_RequestQuestStartOK(remote,RmiContext::ReliableSend,LocalQuestStartResult{questID}); return true;
}
DEFRMI_SevenDSQuestC2S_CG_RequestQuestProgress(QuestStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    const auto* row=GcLocal::FindQuest(questID);const auto* rule=GcLocal::FindQuestRule(questID);
    auto it=GcLocal::Quests().find(questID);
    if(!row||!rule||it==GcLocal::Quests().end()||it->second.status!=1)return CancelRequest(remote,10802);
    auto& q=it->second;
    const std::string type=rule->type;
    if(GcLocal::SnapshotQuestType(type)){GcLocal::RefreshQuestSnapshots();GcLocal::SaveQuests();g_questProxy.CG_RequestQuestProgressOK(remote,RmiContext::ReliableSend,LocalQuestProgressResult{questID});return true;}
    // Battle objectives come only from an accepted battle result, never from an increment request.
    if(type=="stage"||type=="stage_array"||type=="battle_quest_count"||type=="cook_count"||type=="basepoint_shop_buy") {
        g_questProxy.CG_RequestQuestProgressOK(remote,RmiContext::ReliableSend,LocalQuestProgressResult{questID});return true;
    }
    if(propIndex>=q.progress.size()||propIndex>=row->requirements.size()||
       (!rule->needs.empty()&&(propIndex>=rule->needs.size()||rule->needs[propIndex]!=needID)))return CancelRequest(remote,10802);
    LocalQuestProgressResult result{questID};
    if(q.progress[propIndex]<row->requirements[propIndex]){
        if(type=="collect"){
            if(GcLocal::FindMaterialType(needID)==0||GcLocal::FindMaterialType(needID)>=200)return CancelRequest(remote,10802);
            GcLocal::Grant(needID,1);result.drops.emplace_back(needID,1);
        }
        ++q.progress[propIndex];
    }
    GcLocal::SaveQuests(); g_questProxy.CG_RequestQuestProgressOK(remote,RmiContext::ReliableSend,result); return true;
}
DEFRMI_SevenDSQuestC2S_CG_RequestQuestClear(QuestStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    const auto* row = GcLocal::FindQuest(questID); if (!row) return false;
    auto it=GcLocal::Quests().find(questID);
    if(it==GcLocal::Quests().end())return CancelRequest(remote,10803);
    auto& q=it->second;
    if(q.status==2){g_questProxy.CG_RequestQuestClearOK(remote,RmiContext::ReliableSend,LocalQuestClearResult{questID,GcLocal::FindQuest(row->next)?row->next:0,{}});return true;}
    GcLocal::RefreshQuestSnapshots();if(!GcLocal::QuestReady(questID))return CancelRequest(remote,10803);
    std::vector<std::pair<int,int>> consumed;
    const auto* rule=GcLocal::FindQuestRule(questID);
    bool keep=true;for(auto r:GcLocal::QuestItemRules)if(r.quest==questID){keep=r.keep;break;}
    if(rule&&!keep&&(std::string(rule->type)=="collect"||std::string(rule->type)=="deliver")){
        if(rule->needs.size()!=row->requirements.size())return CancelRequest(remote,10803);
        for(size_t i=0;i<rule->needs.size();++i)if(row->requirements[i]>0)consumed.emplace_back(rule->needs[i],row->requirements[i]);
        if(!GcLocal::Spend(consumed))return CancelRequest(remote,10803,101);
    }
    std::vector<LocalNativeReward> rewards;
    for(auto r:GcLocal::QuestRewards)if(r.quest==questID){
        if(r.type<200){GcLocal::Grant(r.item,r.count);rewards.push_back({r.type,r.item,r.count,0});}
        else if(r.type==211){const auto* skin=GcLocal::FindSkin(r.item);if(!skin)continue;
            if(!GcLocal::OwnedHeroes().count(skin->hero)){rewards.push_back({210,skin->hero,1,0});GcLocal::OwnedSkins().insert(r.item);rewards.push_back({211,r.item,r.count,0});GcLocal::SaveAccount();}
            else for(auto c:GcLocal::HeroCoins)if(c.skin==r.item){GcLocal::Grant(c.coin,r.count);rewards.push_back({GcLocal::FindMaterialType(c.coin),c.coin,r.count,0});break;}}
        else if(r.type==212&&GcLocal::EquipmentBaseRow(r.item)){auto& w=GcLocal::CreateEquipment(r.item);GcLocal::SaveEquipments();rewards.push_back({212,r.item,r.count,w.serial});}
        else if(r.type==216){GcLocal::Artifacts().insert(r.item);GcLocal::SaveExtraInventory();rewards.push_back({216,r.item,r.count,0});}
        else if(r.type>=213&&r.type<=215&&GcLocal::FindCosmetic(r.item)){GcLocal::CraftedCosmetics().insert(r.item);GcLocal::SaveCraftedCosmetics();rewards.push_back({r.type,r.item,r.count,0});}
    }
    q.status=2; q.progress=row->requirements;
    if(rule&&rule->story)GcLocal::RecordMission(37,0,1);
    const int next=GcLocal::FindQuest(row->next) ? row->next : 0;
    if (next) {
        bool fresh=!GcLocal::Quests().count(next);GcLocal::StartQuest(next);
        if(fresh)for(auto r:GcLocal::QuestItemRules)if(r.quest==next&&r.item&&r.count>0){rewards.push_back({GcLocal::FindMaterialType(r.item),r.item,r.count,0});break;}
    }
    GcLocal::SaveQuests(); g_questProxy.CG_RequestQuestClearOK(remote,RmiContext::ReliableSend,LocalQuestClearResult{questID,next,rewards,consumed});
    std::printf("[Grand Cross Local] cleared quest %d; next %d.\n",questID,next); return true;
}
SevenDSRecipeInfoS2C::Proxy g_recipeInfoProxy;
class RecipeInfoStub final : public SevenDSRecipeInfoC2S::Stub {
public: DECRMI_SevenDSRecipeInfoC2S_CG_RequestCookingRecipeOrderInfo;
} g_recipeInfoStub;
DEFRMI_SevenDSRecipeInfoC2S_CG_RequestCookingRecipeOrderInfo(RecipeInfoStub){
 g_recipeInfoProxy.CG_RequestCookingRecipeOrderInfoOK(remote,RmiContext::ReliableSend,EmptyItemResults{});return true;
}
SevenDSCookingS2C::Proxy g_cookingProxy;
class CookingStub final : public SevenDSCookingC2S::Stub {
public: DECRMI_SevenDSCookingC2S_CG_RequestCookingStart;
} g_cookingStub;
DEFRMI_SevenDSCookingC2S_CG_RequestCookingStart(CookingStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 if(request.npc<=0||request.count<=0||request.count>100)return CancelRequest(remote,10869);
 auto supplied=request.materials;std::sort(supplied.begin(),supplied.end());
 if(std::adjacent_find(supplied.begin(),supplied.end())!=supplied.end())return CancelRequest(remote,10869);
 const GcLocal::CookingRule* cooking=nullptr;
 for(const auto& row:GcLocal::CookingRules){
  std::vector<int> expected;for(int id:row.materials)if(id)expected.push_back(id);std::sort(expected.begin(),expected.end());
  bool match=expected==supplied;
  // Native story cooking can select only its two gathered main ingredients.
  if(!match&&supplied.size()==2&&row.quest){auto it=GcLocal::Quests().find(row.quest);std::vector<int> two={row.materials[0],row.materials[1]};std::sort(two.begin(),two.end());match=it!=GcLocal::Quests().end()&&it->second.status==1&&two==supplied;}
  if(match){cooking=&row;break;}
 }
 if(!cooking)return CancelRequest(remote,10869);
 const GcLocal::RecipeRule* recipe=nullptr;for(const auto& row:GcLocal::RecipeRules)if(row.cooking==cooking->id){recipe=&row;break;}
 if(!recipe)return CancelRequest(remote,10869);
 LocalCookingResult result;result.recipe=recipe->id;result.count=request.count;result.npc=request.npc;result.immediately=request.immediately;
 for(int id:supplied)result.costs.emplace_back(id,request.count);
 if(!GcLocal::Spend(result.costs))return CancelRequest(remote,10869,101);
 int foodCount=cooking->minCount*request.count;
 GcLocal::Grant(cooking->food,foodCount);result.drops.emplace_back(cooking->food,foodCount);
 auto& exp=GcLocal::RecipeExperience()[recipe->id];exp=int(std::min<int64_t>(recipe->maxExp,int64_t(exp)+int64_t(recipe->experience)*request.count));GcLocal::SaveRecipes();
 GcLocal::RecordQuestAction("cook_count",cooking->food,request.count);
 GcLocal::RecordMission(28,0,request.count);GcLocal::RecordMission(66,0,1);
 g_cookingProxy.CG_RequestCookingStartOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSTownShopS2C::Proxy g_townShopProxy;
class TownShopStub final : public SevenDSTownShopC2S::Stub {
public: DECRMI_SevenDSTownShopC2S_CG_RequestBasePointShopInfo;
 DECRMI_SevenDSTownShopC2S_CG_RequestBasePointShopBuy;
} g_townShopStub;
DEFRMI_SevenDSTownShopC2S_CG_RequestBasePointShopInfo(TownShopStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 bool known=false;for(auto r:GcLocal::TownShopRules)if(r.town==basepointID)known=true;
 if(!known)return CancelRequest(remote,10659);
 g_townShopProxy.CG_RequestBasePointShopInfoOK(remote,RmiContext::ReliableSend,LocalTownShopResult{basepointID});return true;
}
DEFRMI_SevenDSTownShopC2S_CG_RequestBasePointShopBuy(TownShopStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 std::set<int> seen;std::map<int,int> costs,drops;LocalTownBuyResult result;
 for(auto p:request.products){
  const auto* r=GcLocal::FindTownProduct(p.first);
  if(!r||!p.second||!seen.insert(p.first).second||r->level>1||GcLocal::TownShopCounts()[p.first]+p.second>r->limit)return CancelRequest(remote,10660);
  costs[r->currency]+=r->price*p.second;drops[r->item]+=r->count*p.second;result.products.push_back(p.first);
 }
 for(auto p:costs)result.costs.push_back(p);for(auto p:drops)result.drops.push_back(p);
 if(!GcLocal::Spend(result.costs))return CancelRequest(remote,10660,101);
 for(auto p:result.drops)GcLocal::Grant(p.first,p.second);
 for(auto p:request.products){GcLocal::TownShopCounts()[p.first]+=p.second;GcLocal::RecordQuestAction("basepoint_shop_buy",p.first,p.second);}
 for(auto p:request.products)GcLocal::RecordMission(26,0,p.second);
 GcLocal::SaveTownShops();g_townShopProxy.CG_RequestBasePointShopBuyOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSMainSkinS2C::Proxy g_mainSkinProxy;
class MainSkinStub final : public SevenDSMainSkinC2S::Stub {
public: DECRMI_SevenDSMainSkinC2S_CG_RequestMainSkinChange;
} g_mainSkinStub;
DEFRMI_SevenDSMainSkinC2S_CG_RequestMainSkinChange(MainSkinStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    if(!GcLocal::OwnedSkins().count(skin))return false;
    GcLocal::SaveMainSkin(skin);
    g_mainSkinProxy.CG_RequestMainSkinChangeOK(remote,RmiContext::ReliableSend,skin);return true;
}
static bool AppendDevelopmentRecipe(int hero,int kind,int level,int rating,std::vector<std::pair<int32_t,int32_t>>& costs){
 for(const auto& r:GcLocal::EconomyCosts)if(r.hero==hero&&r.kind==kind&&r.level==level&&(!rating||!r.rating||r.rating==rating)){for(int i=0;i<5;++i)if(r.items[i]&&r.counts[i])costs.emplace_back(r.items[i],r.counts[i]);return true;}return false;
}
static int NextEvolutionSkin(int previous){const auto* before=GcLocal::DevelopmentRow(previous);const auto* skin=GcLocal::FindSkin(previous);if(!before||!skin)return 0;for(auto r:GcLocal::DevelopmentSkins)if(r.rating==before->rating+1&&GcLocal::FindSkin(r.id)->hero==skin->hero)return r.id;return 0;}
static bool LegendEligible(int skin){const auto* row=GcLocal::DevelopmentRow(skin);if(!row||row->rating!=6)return false;const auto& state=GcLocal::DevelopmentStates()[skin];return GcLocal::SkinLevel(skin)>=100&&state.awaken>=6&&state.transcend>=6&&NextEvolutionSkin(skin)!=0;}
static void CommitEvolution(int previous,int next){
 auto state=GcLocal::DevelopmentStates()[previous];state.exp=0;if(GcLocal::DevelopmentRow(next)->rating==7)state.limitBreak=0;GcLocal::DevelopmentStates()[next]=state;
 if(GcLocal::UnlockedPassives().erase(previous))GcLocal::UnlockedPassives().insert(next);
 for(auto& t:GcLocal::Teams())for(auto& slot:t.second.slots){if(slot.skin==previous)slot.skin=next;if(slot.fateSkin==previous)slot.fateSkin=next;}
 GcLocal::ReplaceEquipmentSkin(previous,next);GcLocal::ReplaceMainSkin(previous,next);GcLocal::OwnedSkins().erase(previous);GcLocal::OwnedSkins().insert(next);
}
static void SaveEvolution(){GcLocal::SaveDevelopment();GcLocal::SavePassives();GcLocal::SaveTeams();GcLocal::SaveAccount();}
SevenDSLegendS2C::Proxy g_legendProxy;
class LegendStub final : public SevenDSLegendC2S::Stub {
public: DECRMI_SevenDSLegendC2S_CG_RequestSkinLegendEvolution;
} g_legendStub;
DEFRMI_SevenDSLegendC2S_CG_RequestSkinLegendEvolution(LegendStub) {
 std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);int previous=GcLocal::ActiveSkin(targetHeroID);
 if(!LegendEligible(previous))return CancelRequest(remote,10113);
 int next=NextEvolutionSkin(previous);LocalLegendResult result{previous,next,{}};
 if(!AppendDevelopmentRecipe(targetHeroID,1,6,0,result.costs))return CancelRequest(remote,10113);
 if(!GcLocal::Spend(result.costs))return CancelRequest(remote,10113,101);
 CommitEvolution(previous,next);SaveEvolution();g_legendProxy.CG_RequestSkinLegendEvolutionOK(remote,RmiContext::ReliableSend,result);return true;
}
// One-step package settings are taken from DB_config_game:
// one_step_evolution_item_lite=912089, package=911424; both UR/6 awakening/level90.
SevenDSOneStepLiteS2C::Proxy g_oneStepLiteProxy;
SevenDSOneStepS2C::Proxy g_oneStepProxy;
class OneStepLiteStub final : public SevenDSOneStepLiteC2S::Stub {
public: DECRMI_SevenDSOneStepLiteC2S_CG_RequestSkinOneStepEvolutionLite;
} g_oneStepLiteStub;
class OneStepStub final : public SevenDSOneStepC2S::Stub {
public: DECRMI_SevenDSOneStepC2S_CG_RequestSkinOneStepEvolution;
} g_oneStepStub;
LocalOneStepResult ApplyOneStep(int hero,int item,bool pay=true) {
    const int previous=GcLocal::ActiveSkin(hero);
    const auto* before=GcLocal::DevelopmentRow(previous);
    if(!before) throw std::runtime_error("One-step hero is not owned");
    int next=previous;
    // Paid one-step tokens skip directly to an available LR form.
    if(pay)for(const auto& candidate:GcLocal::DevelopmentSkins)
        if(candidate.rating==7 && GcLocal::FindSkin(candidate.id)->hero==hero){next=candidate.id;break;}
    if(next==previous && before->rating<6) {
        next=0;
        for(const auto& row:GcLocal::DevelopmentSkins)
            if(row.rating==6 && GcLocal::FindSkin(row.id)->hero==hero){next=row.id;break;}
        if(!next) throw std::runtime_error("One-step hero has no UR evolution");
    }
    if(pay&&!GcLocal::Spend({{item,1}}))throw std::runtime_error("Not enough one-step tokens");
    auto state=GcLocal::DevelopmentStates()[previous];
    const auto* row=GcLocal::DevelopmentRow(next);
    state.awaken=(std::max)(state.awaken,6);
    if(row->rating==6) state.limitBreak=(std::max)(state.limitBreak,(std::max)(0,(90-row->maxLevel)/5));
    GcLocal::DevelopmentStates()[next]=state;
    GcLocal::DevelopmentStates()[next].exp=(pay&&row->rating==7)?0:(std::max)(state.exp,GcLocal::ExperienceCap(next));
    if(pay&&row->rating==7)GcLocal::DevelopmentStates()[next].limitBreak=0;
    if(previous!=next) {
        if(GcLocal::UnlockedPassives().erase(previous)) GcLocal::UnlockedPassives().insert(next);
        for(auto& t:GcLocal::Teams())for(auto& slot:t.second.slots){
            if(slot.skin==previous)slot.skin=next;
            if(slot.fateSkin==previous)slot.fateSkin=next;
        }
        GcLocal::ReplaceEquipmentSkin(previous,next);GcLocal::ReplaceMainSkin(previous,next);GcLocal::OwnedSkins().erase(previous);GcLocal::OwnedSkins().insert(next);
    }
    GcLocal::SaveDevelopment();GcLocal::SavePassives();GcLocal::SaveTeams();GcLocal::SaveAccount();
    std::printf("[Grand Cross Local] one-step hero %d skin %d -> %d, limit %d, awaken %d.\n",hero,previous,next,GcLocal::DevelopmentStates()[next].limitBreak,state.awaken);
    return {previous,next,item};
}
DEFRMI_SevenDSOneStepLiteC2S_CG_RequestSkinOneStepEvolutionLite(OneStepLiteStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    if(GcLocal::SeededMaterialCount(912089)<1)return CancelRequest(remote,13505,101);
    if(!GcLocal::ActiveSkin(targetHeroID))return CancelRequest(remote,13505);
    const auto result=ApplyOneStep(targetHeroID,912089);
    g_oneStepLiteProxy.CG_RequestSkinOneStepEvolutionLiteOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSOneStepC2S_CG_RequestSkinOneStepEvolution(OneStepStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    if(GcLocal::SeededMaterialCount(911424)<1)return CancelRequest(remote,10110,101);
    if(!GcLocal::ActiveSkin(targetHeroID))return CancelRequest(remote,10110);
    const auto result=ApplyOneStep(targetHeroID,911424);
    g_oneStepProxy.CG_RequestSkinOneStepEvolutionOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSEvolutionS2C::Proxy g_evolutionProxy;
SevenDSLimitBreakS2C::Proxy g_limitBreakProxy;
class EvolutionStub final : public SevenDSEvolutionC2S::Stub {
public: DECRMI_SevenDSEvolutionC2S_CG_RequestSkinEvolution;
    DECRMI_SevenDSEvolutionC2S_CG_RequestSkinSkillLevelUp;
} g_evolutionStub;
class LimitBreakStub final : public SevenDSLimitBreakC2S::Stub {
public: DECRMI_SevenDSLimitBreakC2S_CG_RequestSkinOverEvolution;
} g_limitBreakStub;
DEFRMI_SevenDSEvolutionC2S_CG_RequestSkinEvolution(EvolutionStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    const int previous = GcLocal::ActiveSkin(targetHeroID);
    const auto* before = GcLocal::DevelopmentRow(previous); if (!before || before->rating>=6) return CancelRequest(remote,10089);
    int next = 0;
    for (const auto& row : GcLocal::DevelopmentSkins)
        if (row.rating == before->rating + 1 && GcLocal::FindSkin(row.id)->hero == targetHeroID) { next = row.id; break; }
    if (!next) return CancelRequest(remote,10089);
    std::vector<std::pair<int32_t,int32_t>> costs;
    if(!AppendDevelopmentRecipe(targetHeroID,1,before->rating,0,costs))return CancelRequest(remote,10089);
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10089,101);
    auto state = GcLocal::DevelopmentStates()[previous]; state.exp = 0;
    GcLocal::DevelopmentStates()[next] = state;
    if (GcLocal::UnlockedPassives().erase(previous)) GcLocal::UnlockedPassives().insert(next);
    for (auto& t : GcLocal::Teams()) for (auto& slot : t.second.slots) {
        if (slot.skin == previous) slot.skin = next;
        if (slot.fateSkin == previous) slot.fateSkin = next;
    }
    GcLocal::ReplaceEquipmentSkin(previous,next);GcLocal::ReplaceMainSkin(previous,next);GcLocal::OwnedSkins().erase(previous); GcLocal::OwnedSkins().insert(next);
    GcLocal::SaveDevelopment(); GcLocal::SavePassives(); GcLocal::SaveTeams(); GcLocal::SaveAccount();
    g_evolutionProxy.CG_RequestSkinEvolutionOK(remote,RmiContext::ReliableSend,LocalEvolutionResult{previous,next,true,costs});
    std::printf("[Grand Cross Local] evolved hero %d skin %d -> %d.\n",targetHeroID,previous,next); return true;
}
DEFRMI_SevenDSEvolutionC2S_CG_RequestSkinSkillLevelUp(EvolutionStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    const int id = GcLocal::ActiveSkin(targetHeroID); if (!id || skillLevelUpCount < 1 || skillLevelUpCount > 5 || GcLocal::DevelopmentStates()[id].skill+skillLevelUpCount>5) return CancelRequest(remote,10090);
    std::vector<std::pair<int,int>> costs;
    for(int level=GcLocal::DevelopmentStates()[id].skill+2;level<=(std::min)(6,GcLocal::DevelopmentStates()[id].skill+int(skillLevelUpCount)+1);++level){if(!AppendDevelopmentRecipe(targetHeroID,4,level,0,costs))return CancelRequest(remote,10090);}
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10090,101);
    auto& state = GcLocal::DevelopmentStates()[id]; state.skill = (std::min)(5,state.skill + int(skillLevelUpCount)); GcLocal::SaveDevelopment();
    g_evolutionProxy.CG_RequestSkinSkillLevelUpOK(remote,RmiContext::ReliableSend,LocalSkillResult{id,costs});
    std::printf("[Grand Cross Local] ultimate hero %d level %d.\n",targetHeroID,state.skill + 1); return true;
}
static bool ApplyLimitBreak(int hero,int target,LocalBreakResult& result) {
 const int skin=GcLocal::ActiveSkin(hero);const auto* row=GcLocal::DevelopmentRow(skin);
 if(!row||row->rating!=6)return false;
 const auto& state=GcLocal::DevelopmentStates()[skin];
 if(target<=state.limitBreak||target>8||GcLocal::SkinLevel(skin)<row->maxLevel+5*state.limitBreak)return false;
 std::map<int,int64_t> totals;
 for(int step=state.limitBreak+1;step<=target;++step){auto costs=DevelopmentCosts(hero,2,step);if(costs.empty())return false;for(auto p:costs)totals[p.first]+=p.second;}
 for(auto p:totals){if(p.second<=0||p.second>2147483647)return false;result.costs.emplace_back(p.first,int(p.second));}
 if(!GcLocal::Spend(result.costs))return false;
 result.skin=skin;GcLocal::DevelopmentStates()[skin].limitBreak=target;GcLocal::SaveDevelopment();return true;
}
DEFRMI_SevenDSLimitBreakC2S_CG_RequestSkinOverEvolution(LimitBreakStub) {
 std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);LocalBreakResult result;int skin=GcLocal::ActiveSkin(targetHeroID);
 if(!skin||!ApplyLimitBreak(targetHeroID,GcLocal::DevelopmentStates()[skin].limitBreak+1,result))return CancelRequest(remote,10096);
 g_limitBreakProxy.CG_RequestSkinOverEvolutionOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSStraightLimitBreakS2C::Proxy g_straightBreakProxy;
class StraightLimitBreakStub final : public SevenDSStraightLimitBreakC2S::Stub {
public: DECRMI_SevenDSStraightLimitBreakC2S_CG_RequestSkinOverEvolutionStraight;
} g_straightBreakStub;
DEFRMI_SevenDSStraightLimitBreakC2S_CG_RequestSkinOverEvolutionStraight(StraightLimitBreakStub) {
 std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);LocalBreakResult result;
 if(!ApplyLimitBreak(targetHeroID,int(targetMaxLevelCount),result))return CancelRequest(remote,10112);
 g_straightBreakProxy.CG_RequestSkinOverEvolutionStraightOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSCosmeticShopS2C::Proxy g_cosmeticShopProxy;
class CosmeticShopStub final : public SevenDSCosmeticShopC2S::Stub {
public: DECRMI_SevenDSCosmeticShopC2S_CG_RequestCostumeShopInfo;
} g_cosmeticShopStub;
DEFRMI_SevenDSCosmeticShopC2S_CG_RequestCostumeShopInfo(CosmeticShopStub) {
    g_cosmeticShopProxy.CG_RequestCostumeShopInfoOK(remote,RmiContext::ReliableSend,EmptyItemResults{},EmptyItemResults{});
    std::puts("[Grand Cross Local] opened native costume wardrobe (10669)."); return true;
}
SevenDSCosmeticEquipS2C::Proxy g_cosmeticEquipProxy;
SevenDSStoryCostumeS2C::Proxy g_storyCostumeProxy;
class StoryCostumeStub final : public SevenDSStoryCostumeC2S::Stub {
public: DECRMI_SevenDSStoryCostumeC2S_CG_RequestStoryCostume;
} g_storyCostumeStub;
DEFRMI_SevenDSStoryCostumeC2S_CG_RequestStoryCostume(StoryCostumeStub) {
    g_storyCostumeProxy.CG_RequestStoryCostumeOK(remote, RmiContext::ReliableSend, EmptyItemResults{}, EmptyItemResults{});
    std::puts("[Grand Cross Local] completed story costume check (10101); cosmetic wardrobe granted on login.");
    return true;
}
class CosmeticEquipStub final : public SevenDSCosmeticEquipC2S::Stub {
public:
    DECRMI_SevenDSCosmeticEquipC2S_CG_RequestCostumeEquip;
    DECRMI_SevenDSCosmeticEquipC2S_CG_RequestCostumeUnEquip;
} g_cosmeticEquipStub;
inline int ChangeCosmetic(int costume, int hero, bool equip) {
    const auto* row = GcLocal::FindCosmetic(costume);
    int skin = 0;
    skin = GcLocal::ActiveSkin(hero);
    if (!row || !skin) throw std::runtime_error("Unknown cosmetic or unowned hero");
    auto& e = GcLocal::CosmeticEquipments()[hero];
    int& group = row->type == 1 ? e.outfit : (row->type == 2 ? e.weapon : e.head);
    group = equip ? row->group : 0; GcLocal::SaveCosmetics();
    std::printf("[Grand Cross Local] cosmetic %d hero %d equipped=%d\n", costume, hero, equip);
    return skin;
}
DEFRMI_SevenDSCosmeticEquipC2S_CG_RequestCostumeEquip(CosmeticEquipStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    const int skin = ChangeCosmetic(costumeID, targetHeroID, true);
    g_cosmeticEquipProxy.CG_RequestCostumeEquipOK(remote, RmiContext::ReliableSend, LocalPassiveResult{skin}); return true;
}
DEFRMI_SevenDSCosmeticEquipC2S_CG_RequestCostumeUnEquip(CosmeticEquipStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    const int skin = ChangeCosmetic(costumeID, targetHeroID, false);
    g_cosmeticEquipProxy.CG_RequestCostumeUnEquipOK(remote, RmiContext::ReliableSend, LocalPassiveResult{skin}); return true;
}
SevenDSPassiveS2C::Proxy g_passiveProxy;
class PassiveStub final : public SevenDSPassiveC2S::Stub {
public: DECRMI_SevenDSPassiveC2S_CG_RequestGetExclusiveSkill;
} g_passiveStub;
DEFRMI_SevenDSPassiveC2S_CG_RequestGetExclusiveSkill(PassiveStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    int id = 0;
    id = GcLocal::ActiveSkin(heroId);
    if (!id) return false;
    GcLocal::UnlockedPassives().insert(id); GcLocal::SavePassives();
    g_passiveProxy.CG_RequestGetExclusiveSkillOK(remote,RmiContext::ReliableSend,LocalPassiveResult{id});
    std::printf("[Grand Cross Local] unlocked passive for hero %d skin %d.\n",heroId,id); return true;
}
SevenDSDevelopmentS2C::Proxy g_developmentProxy;
class DevelopmentStub final : public SevenDSDevelopmentC2S::Stub {
public:
    DECRMI_SevenDSDevelopmentC2S_CG_RequestSkinLevelUpBySkinMaterial;
    DECRMI_SevenDSDevelopmentC2S_CG_RequestSkinAwaken;
} g_developmentStub;
DEFRMI_SevenDSDevelopmentC2S_CG_RequestSkinLevelUpBySkinMaterial(DevelopmentStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    if (!GcLocal::OwnedSkins().count(request.skin)) return false;
    int64_t gain = 0; const int maxExp = GcLocal::ExperienceCap(request.skin);
    for (const auto& item : request.materials) {
        bool valid = false;
        for (const auto& row : GcLocal::ExperienceMaterials) if (row.id == item.first) { gain += int64_t(row.exp) * item.second; valid = true; }
        if (!valid) return false;
    }
    if(!GcLocal::Spend(request.materials))return CancelRequest(remote,10081,101);
    auto& state = GcLocal::DevelopmentStates()[request.skin];
    state.exp = int(std::min<int64_t>(maxExp,int64_t(state.exp) + gain)); GcLocal::SaveDevelopment();
    GcLocal::RecordMission(92,0,1);GcLocal::RecordMission(61,0,1);
    g_developmentProxy.CG_RequestSkinLevelUpBySkinMaterialOK(remote,RmiContext::ReliableSend,LocalLevelUpResult{request.skin,request.materials});
    std::printf("[Grand Cross Local] leveled skin %d to exp %d; materials replenished.\n",request.skin,state.exp); return true;
}
DEFRMI_SevenDSDevelopmentC2S_CG_RequestSkinAwaken(DevelopmentStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    int id = 0;
    id = GcLocal::ActiveSkin(hero);
    if (!id || awaken < 1 || awaken > 6) return CancelRequest(remote,10085);
    if(awaken<=GcLocal::DevelopmentStates()[id].awaken){g_developmentProxy.CG_RequestSkinAwakenOK(remote,RmiContext::ReliableSend,LocalAwakenResult{id,{}});return true;}
    std::vector<std::pair<int,int>> costs;
    for(int level=GcLocal::DevelopmentStates()[id].awaken+1;level<=awaken;++level){if(!AppendDevelopmentRecipe(hero,3,level,0,costs))return CancelRequest(remote,10085);}
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10085,101);
    auto& state = GcLocal::DevelopmentStates()[id];
    int added=(std::max)(0,int(awaken)-state.awaken);state.awaken = (std::max)(state.awaken,int(awaken)); GcLocal::SaveDevelopment();
    GcLocal::RecordMission(19,0,added);GcLocal::RefreshQuestSnapshots();GcLocal::SaveQuests();
    g_developmentProxy.CG_RequestSkinAwakenOK(remote,RmiContext::ReliableSend,LocalAwakenResult{id,costs}); return true;
}
SevenDSAwakenStraightS2C::Proxy g_awakenStraightProxy;
class AwakenStraightStub final : public SevenDSAwakenStraightC2S::Stub {
public: DECRMI_SevenDSAwakenStraightC2S_CG_RequestSkinAwakenStraight;
} g_awakenStraightStub;
DEFRMI_SevenDSAwakenStraightC2S_CG_RequestSkinAwakenStraight(AwakenStraightStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    const int id=GcLocal::ActiveSkin(hero);
    if(!id||awaken<1||awaken>6)return CancelRequest(remote,10120);
    auto& state=GcLocal::DevelopmentStates()[id];
    if(awaken<=state.awaken){g_awakenStraightProxy.CG_RequestSkinAwakenStraightOK(remote,RmiContext::ReliableSend,LocalAwakenResult{id,{}});return true;}
    std::vector<std::pair<int32_t,int32_t>> costs;
    for(int level=state.awaken+1;level<=awaken;++level)
        if(!AppendDevelopmentRecipe(hero,3,level,0,costs))return CancelRequest(remote,10120);
    if(!GcLocal::Spend(costs))return CancelRequest(remote,10120,101);
    const int added=awaken-state.awaken;state.awaken=awaken;GcLocal::SaveDevelopment();
    GcLocal::RecordMission(19,0,added);GcLocal::RefreshQuestSnapshots();GcLocal::SaveQuests();
    g_awakenStraightProxy.CG_RequestSkinAwakenStraightOK(remote,RmiContext::ReliableSend,LocalAwakenResult{id,costs});
    return true;
}
SevenDSBattleReadyS2C::Proxy g_battleReadyProxy;
class BattleReadyStub final : public SevenDSBattleReadyC2S::Stub {
public: DECRMI_SevenDSBattleReadyC2S_CG_RequestIngameBattleStart;
} g_battleReadyStub;
DEFRMI_SevenDSBattleReadyC2S_CG_RequestIngameBattleStart(BattleReadyStub) {
    g_battleReadyProxy.CG_RequestIngameBattleStartOK(remote, RmiContext::ReliableSend);
    std::puts("[Grand Cross Local] acknowledged battle ready (10336)."); return true;
}
SevenDSStoryStartS2C::Proxy g_storyStartProxy;
class StoryStartStub final : public SevenDSStoryStartC2S::Stub {
public: DECRMI_SevenDSStoryStartC2S_CG_Request_Main_Stage_Start;
    DECRMI_SevenDSStoryStartC2S_CG_Request_Main_Stage_Clear;
} g_storyStartStub;
DEFRMI_SevenDSStoryStartC2S_CG_Request_Main_Stage_Start(StoryStartStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 if(!EconomyStage(0,request.stage)||!GcLocal::CanEnterCampaign(0,request.stage))return CancelRequest(remote,10156);
 if(!PayStage(0,request.stage))return CancelRequest(remote,10156,101);
 GcLocal::ActiveBattles()[remote]={0,request.stage};CaptureBattleParty(remote,request.teamIndex);
 g_storyStartProxy.CG_Request_Main_Stage_StartOK(remote, RmiContext::ReliableSend, LocalStageStartResult{request.stage,request.index});
 std::printf("[Grand Cross Local] start story battle %d.\n", request.stage); return true;
}

SevenDSMercenaryS2C::Proxy g_mercenaryProxy;
DEFRMI_SevenDSStoryStartC2S_CG_Request_Main_Stage_Clear(StoryStartStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    bool known = false;
    for (const auto& stage : GcLocal::StoryStages) if (stage.id == request.stage) known = true;
    if (!known) return CancelRequest(remote,10157);
    auto active=GcLocal::ActiveBattles().find(remote);
    if(active==GcLocal::ActiveBattles().end()||active->second!=std::make_pair(0,int(request.stage)))return CancelRequest(remote,10157);
    const bool first = request.win && GcLocal::BattleClears().insert({0,request.stage}).second;
    if(first)GcLocal::SaveBattleProgress();
    if(request.win&&GcLocal::FindCampaignStage(0,request.stage)->mainRoute&&request.stage>GcLocal::MainStageClear()){GcLocal::MainStageClear()=request.stage;GcLocal::SaveStoryProgress();}
    g_storyStartProxy.CG_Request_Main_Stage_ClearOK(remote, RmiContext::ReliableSend, CompleteStage(0,request.stage,request.win,first,remote),first,EmptyItemResults{});
    GcLocal::ActiveBattleHeroes().erase(remote);GcLocal::ActiveBattles().erase(active);
    std::printf("[Grand Cross Local] story stage %d result %s.\n", request.stage,request.win ? "win" : "loss"); return true;
}
SevenDSStoryInfoS2C::Proxy g_storyInfoProxy;
class StoryInfoStub final : public SevenDSStoryInfoC2S::Stub {
public: DECRMI_SevenDSStoryInfoC2S_CG_RequestStageInfo;
} g_storyInfoStub;
DEFRMI_SevenDSStoryInfoC2S_CG_RequestStageInfo(StoryInfoStub) {
 g_storyInfoProxy.CG_RequestStageInfoOK(remote, RmiContext::ReliableSend, LocalStageInfo{});
 std::puts("[Grand Cross Local] sent story stage info (10151)."); return true;
}

SevenDSGachaBuyS2C::Proxy g_gachaBuyProxy;
class GachaBuyStub final : public SevenDSGachaBuyC2S::Stub {
public:
    DECRMI_SevenDSGachaBuyC2S_CG_RequestGambleShopBuy;
} g_gachaBuyStub;
DEFRMI_SevenDSGachaBuyC2S_CG_RequestGambleShopBuy(GachaBuyStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    GambleShopBuyResult result; result.group = gambleRequest.group; result.amount = gambleRequest.amount;
    int count = 0;
    for (const auto& b : GcLocal::Banners) if (b.group == result.group) {
        count = result.amount == 0 ? b.single : b.multiple; result.event = 100000 + b.id; break;
    }
    if (count < 1 || count > 11 || result.amount > 1) return false;
    if(!GcLocal::Spend({{500011,result.amount==0?3:30}}))return CancelRequest(remote,10651,101);
    auto heroes = GcLocal::OwnedHeroes();
    for (int i = 0; i < count; ++i) {
        const int id=GcLocal::RollSkin(result.group),hero=GcLocal::FindSkin(id)->hero;
        result.skins.push_back(id);
        if(heroes.insert(hero).second){GcLocal::OwnedSkins().insert(id);result.newHeroes.push_back(hero);result.coins.push_back(0);}
        else {int coin=0;for(const auto& row:GcLocal::HeroCoins)if(row.skin==id){coin=row.coin;break;}
            if(!coin)throw std::runtime_error("Missing duplicate hero coin");GcLocal::Grant(coin,1);result.coins.push_back(coin);}
    }
    GcLocal::SaveAccount();
    GcLocal::RecordMission(30,0,count);GcLocal::RecordMission(29,0,result.amount==0?3:30);
    GcLocal::RecordMission(3,0,int(result.newHeroes.size()));
    for(int coin:result.coins)if(coin)GcLocal::RecordMission(58,0,1);
    g_gachaBuyProxy.CG_RequestGambleShopBuyOK(remote, RmiContext::ReliableSend, result);
    std::printf("[Grand Cross Local] summoned %d skins from group %d; diamonds unchanged.\n", count, result.group);
    return true;
}
SevenDSGachaShopS2C::Proxy g_gachaShopProxy;
class GachaShopStub final : public SevenDSGachaShopC2S::Stub {
public:
    DECRMI_SevenDSGachaShopC2S_CG_RequestGambleShopInfo;
} g_gachaShopStub;
DEFRMI_SevenDSGachaShopC2S_CG_RequestGambleShopInfo(GachaShopStub) {
    const int group = gambleType;
    g_gachaShopProxy.CG_RequestGambleShopInfoOK(remote, RmiContext::ReliableSend,
        GambleShopInfo{group}, GambleTimeSwitchLobbyInfo{});
    std::printf("[Grand Cross Local] draw shop %d group %d (10703).\n", gambleType, group);
    return true;
}
SevenDSGachaItemS2C::Proxy g_gachaItemProxy;
class GachaItemStub final : public SevenDSGachaItemC2S::Stub {
public:
    DECRMI_SevenDSGachaItemC2S_CG_RequestItemGambleShopInfo;
} g_gachaItemStub;
DEFRMI_SevenDSGachaItemC2S_CG_RequestItemGambleShopInfo(GachaItemStub) {
    g_gachaItemProxy.CG_RequestItemGambleShopInfoOK(remote, RmiContext::ReliableSend,
        EmptyItemResults{}, 86400);
    std::puts("[Grand Cross Local] answered item draw shop info (10654).");
    return true;
}
SevenDSGameS2C::Proxy g_gameResponseProxy;
SevenDSCostumeS2C::Proxy g_costumeResponseProxy;
SevenDSAttendanceS2C::Proxy g_attendanceResponseProxy;
class AttendanceStub final : public SevenDSAttendanceC2S::Stub {
public:
    DECRMI_SevenDSAttendanceC2S_CG_RequestAttendanceReward;
} g_attendanceStub;
DEFRMI_SevenDSAttendanceC2S_CG_RequestAttendanceReward(AttendanceStub) {
    g_attendanceResponseProxy.CG_RequestAttendanceRewardOK(remote, RmiContext::ReliableSend,
        AttendanceResult{}, EmptyItemResults{}, EmptyItemResults{});
    std::puts("[Grand Cross Local] completed attendance (10867).");
    return true;
}
class CostumeStub final : public SevenDSCostumeC2S::Stub {
public:
    DECRMI_SevenDSCostumeC2S_CG_RequestCostumeUnLock;
} g_costumeStub;
DEFRMI_SevenDSCostumeC2S_CG_RequestCostumeUnLock(CostumeStub) {
    g_costumeResponseProxy.CG_RequestCostumeUnLockOK(remote, RmiContext::ReliableSend,
        EmptyItemResults{}, EmptyItemResults{}, EmptyItemResults{}, MissionResult{});
    std::puts("[Grand Cross Local] completed starter costume check (10295).");
    return true;
}

class GrandCrossC2SStub final : public SevenDSGameC2S::Stub {
public:
    DECRMI_SevenDSGameC2S_CG_RequestTeamInfo;
    DECRMI_SevenDSGameC2S_CG_RequestTeamSlotChange;
    DECRMI_SevenDSGameC2S_CG_RequestMercenaryList;
    DECRMI_SevenDSGameC2S_CG_RequestLobbyInfo;
    DECRMI_SevenDSGameC2S_CG_RequestEventList;
    DECRMI_SevenDSGameC2S_CG_RequestBillingCouponVerify;
    DECRMI_SevenDSGameC2S_CG_RequestServerVersion;
    DECRMI_SevenDSGameC2S_CG_RequestSecurityToken;
    DECRMI_SevenDSGameC2S_CG_RequestNetmarbleAuth;
    DECRMI_SevenDSGameC2S_CG_RequestAuthenticateCreate;
    DECRMI_SevenDSGameC2S_CG_RequestLogin;
    DECRMI_SevenDSGameC2S_CG_RequestLoginInstantly;
};

GrandCrossC2SStub g_gameRequestStub;
DEFRMI_SevenDSGameC2S_CG_RequestTeamInfo(GrandCrossC2SStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    g_gameResponseProxy.CG_RequestTeamInfoOK(remote,RmiContext::ReliableSend,LocalTeamInfo{teamIndex});return true;
}
DEFRMI_SevenDSGameC2S_CG_RequestTeamSlotChange(GrandCrossC2SStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    GcLocal::Teams()[request.index] = request.team; GcLocal::SaveTeams();
    g_gameResponseProxy.CG_RequestTeamSlotChangeOK(remote, RmiContext::ReliableSend);
    std::printf("[Grand Cross Local] accepted team %u with %zu slots.\n", request.index, request.team.slots.size());
    return true;
}
SevenDSBootstrapS2C::Proxy g_bootstrapResponseProxy;
class BootstrapStub final : public SevenDSBootstrapC2S::Stub {
public:
    DECRMI_SevenDSBootstrapC2S_CG_RequestLobbySetAttendanceHero;
};
BootstrapStub g_bootstrapRequestStub;
}

DEFRMI_SevenDSBootstrapC2S_CG_RequestLobbySetAttendanceHero(BootstrapStub) {
    g_bootstrapResponseProxy.CG_RequestLobbySetAttendanceHeroOK(remote, RmiContext::ReliableSend,
        attendanceHeroID, activeAttendanceHeroID);
    std::printf("[Grand Cross Local] updated attendance heroes %d / %d.\n", attendanceHeroID, activeAttendanceHeroID);
    return true;
}

DEFRMI_SevenDSGameC2S_CG_RequestMercenaryList(GrandCrossC2SStub) {
    g_mercenaryProxy.CG_RequestMercenaryListOK(remote, RmiContext::ReliableSend, EmptyItemResults{}); return true;
}
DEFRMI_SevenDSGameC2S_CG_RequestEventList(GrandCrossC2SStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    g_gameResponseProxy.CG_RequestEventListOK(remote, RmiContext::ReliableSend, EventPacketInfo{});
    return true;
}

DEFRMI_SevenDSGameC2S_CG_RequestLobbyInfo(GrandCrossC2SStub) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);GcLocal::MissionClientReady()=true;
    g_gameResponseProxy.CG_RequestLobbyInfoOK(remote, RmiContext::ReliableSend,
        LobbyInfo{}, MissionResult{true}, EmptyItemResults{}, LoginServiceInfo{});
    std::puts("[Grand Cross Local] answered lobby info (10007).");
    return true;
}
DEFRMI_SevenDSGameC2S_CG_RequestBillingCouponVerify(GrandCrossC2SStub) {
    g_gameResponseProxy.CG_RequestBillingCouponVerifyOK(remote, RmiContext::ReliableSend,
        BillingVerifyResultInfo{}, GcString{});
    std::puts("[Grand Cross Local] answered local billing coupon check (10074).");
    return true;
}
DEFRMI_SevenDSGameC2S_CG_RequestSecurityToken(GrandCrossC2SStub) {
    g_gameResponseProxy.CG_RequestSecurityTokenOK(remote, RmiContext::ReliableSend, _PNT("local-test-session"));
    std::puts("[Grand Cross Local] answered security token (10051).");
    return true;
}

DEFRMI_SevenDSGameC2S_CG_RequestNetmarbleAuth(GrandCrossC2SStub) {
    NetmarbleAccountInfo account;
    account.netmarblePlayerID = _PNT("cloud-local");
    account.usn = 73310001;
    account.nickName = _PNT("Cloud");
    g_gameResponseProxy.CG_RequestNetmarbleAuthOK(remote, RmiContext::ReliableSend, account);
    std::puts("[Grand Cross Local] answered local authentication (10052).");
    return true;
}

DEFRMI_SevenDSGameC2S_CG_RequestServerVersion(GrandCrossC2SStub) {
    const Proud::String localVersion = L"2.113.1-local";
    g_gameResponseProxy.CG_RequestServerVersionOK(
        remote, RmiContext::ReliableSend, localVersion);
    std::puts("[Grand Cross Local] answered CG_RequestServerVersion (10024).");
    return true;
}

DEFRMI_SevenDSGameC2S_CG_RequestAuthenticateCreate(GrandCrossC2SStub) {
    NetmarbleAccountInfo account;
    account.netmarblePlayerID = netmarblePlayerID.IsEmpty()
        ? _PNT("cloud-local") : netmarblePlayerID;
    account.usn = 73310001;
    account.nickName = _PNT("Cloud");
    g_gameResponseProxy.CG_RequestAuthenticateCreateOK(
        remote, RmiContext::ReliableSend, account);
    std::printf("[Grand Cross Local] created local account (10053) for %s.\n",
        StringT2A(account.netmarblePlayerID).GetString());
    return true;
}

DEFRMI_SevenDSGameC2S_CG_RequestLoginInstantly(GrandCrossC2SStub) {
    std::lock_guard<std::mutex> guard(GcLocal::AccountMutex);
    if(usn!=73310001)return CancelRequest(remote,10056);
    // This Hub serves one selected local account. A reconnect can receive a new host ID.
    auto& battles=GcLocal::ActiveBattles();
    if(!battles.count(remote)&&battles.size()==1){
        int previous=battles.begin()->first;auto battle=battles.begin()->second;
        auto& parties=GcLocal::ActiveBattleHeroes();auto party=parties.find(previous);
        if(party!=parties.end()){parties[remote]=party->second;parties.erase(previous);}
        battles.clear();battles[remote]=battle;
    }
    g_gameResponseProxy.CG_RequestLoginInstantlyOK(remote,RmiContext::ReliableSend,LocalReconnectResult{sessionKey});return true;
}
DEFRMI_SevenDSGameC2S_CG_RequestLogin(GrandCrossC2SStub) {
    {std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);GrantPvpExemptions();}
    // Deliver the crossover prototype once per account for direct testing.
    {std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
     if(GcLocal::FindSkin(399501)&&!GcLocal::OwnedHeroes().count(2995001)){
      GcLocal::OwnedSkins().insert(399501);GcLocal::SaveAccount();
     }
     if(GcLocal::FindSkin(399901)&&!GcLocal::OwnedHeroes().count(2997001)){
      GcLocal::OwnedSkins().insert(399901);GcLocal::SaveAccount();
     }
     if(GcLocal::FindSkin(399911)&&!GcLocal::OwnedHeroes().count(2997002)){
      GcLocal::OwnedSkins().insert(399911);GcLocal::SaveAccount();
     }
     if(GcLocal::FindSkin(399931)&&!GcLocal::OwnedHeroes().count(2997004)){
      GcLocal::OwnedSkins().insert(399931);GcLocal::SaveAccount();
     }}
    LoginUserResultInfo user;
    user.usn = 73310001;
    user.name = _PNT("Cloud");
    LoginServiceInfo services;
    g_gameResponseProxy.CG_RequestLoginOK(
        remote, RmiContext::ReliableSend, user, services);
    std::puts("[Grand Cross Local] sent schema-complete local login (14055).");
    std::fflush(stdout);
    return true;
}

// BEGIN RESTORED BATTLE HANDLERS

SevenDSWeekBattleS2C::Proxy g_weekBattleProxy;
class WeekBattleStub final : public SevenDSWeekBattleC2S::Stub {
public:
 DECRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Start;
 DECRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Clear;
 DECRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Continue;
} g_weekBattleStub;
DEFRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Start(WeekBattleStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 if (!GcLocal::FindBattleStage(1,request.stage)) return false;
 if(!PayStage(1,request.stage))return CancelRequest(remote,10153,101);
 GcLocal::ActiveBattles()[remote] = {1,request.stage};CaptureBattleParty(remote,request.teamIndex);
 g_weekBattleProxy.CG_Request_Week_Stage_StartOK(remote,RmiContext::ReliableSend,LocalStageStartResult{request.stage,request.index,1},LocalPayback{},LocalNoItem{});
 std::printf("[Grand Cross Local] Week start %d.\n",request.stage); return true;
}
DEFRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Clear(WeekBattleStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 auto active=GcLocal::ActiveBattles().find(remote);
 if (active==GcLocal::ActiveBattles().end() || active->second != std::make_pair(1,int(request.stage))) return false;
 bool first=false;
 if (request.win) { first=GcLocal::BattleClears().insert({1,request.stage}).second; GcLocal::SaveBattleProgress(); }
 g_weekBattleProxy.CG_Request_Week_Stage_ClearOK(remote,RmiContext::ReliableSend,CompleteStage(1,request.stage,request.win,first,remote),first,EmptyItemResults{},EmptyItemResults{},EmptyItemResults{});
 GcLocal::ActiveBattleHeroes().erase(remote);GcLocal::ActiveBattles().erase(active);
 std::printf("[Grand Cross Local] Week clear %d win=%d.\n",request.stage,int(request.win)); return true;
}
DEFRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Continue(WeekBattleStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 auto active=GcLocal::ActiveBattles().find(remote);
 if (active==GcLocal::ActiveBattles().end() || active->second.first != 1) return false;
 g_weekBattleProxy.CG_Request_Week_Stage_ContinueOK(remote,RmiContext::ReliableSend,EmptyItemResults{},int16_t(1),LocalPayback{}); return true;
}

SevenDSBossBattleS2C::Proxy g_bossBattleProxy;
class BossBattleStub final : public SevenDSBossBattleC2S::Stub {
public:
 DECRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Start;
 DECRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Clear;
 DECRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Continue;
} g_bossBattleStub;
DEFRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Start(BossBattleStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 if (!GcLocal::FindBattleStage(2,request.stage)) return false;
 if(!PayStage(2,request.stage))return CancelRequest(remote,10168,101);
 GcLocal::ActiveBattles()[remote] = {2,request.stage};CaptureBattleParty(remote,request.teamIndex);
 g_bossBattleProxy.CG_Request_Boss_Stage_StartOK(remote,RmiContext::ReliableSend,LocalStageStartResult{request.stage,request.index,2},LocalPayback{});
 std::printf("[Grand Cross Local] Boss start %d.\n",request.stage); return true;
}
DEFRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Clear(BossBattleStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 auto active=GcLocal::ActiveBattles().find(remote);
 if (active==GcLocal::ActiveBattles().end() || active->second != std::make_pair(2,int(request.stage))) return false;
 bool first=false;
 if (request.win) { first=GcLocal::BattleClears().insert({2,request.stage}).second; GcLocal::SaveBattleProgress(); }
 g_bossBattleProxy.CG_Request_Boss_Stage_ClearOK(remote,RmiContext::ReliableSend,CompleteStage(2,request.stage,request.win,first,remote),false,LocalDestroyDiscovery{},first,EmptyItemResults{});
 GcLocal::ActiveBattleHeroes().erase(remote);GcLocal::ActiveBattles().erase(active);
 std::printf("[Grand Cross Local] Boss clear %d win=%d.\n",request.stage,int(request.win)); return true;
}
DEFRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Continue(BossBattleStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 auto active=GcLocal::ActiveBattles().find(remote);
 if (active==GcLocal::ActiveBattles().end() || active->second.first != 2) return false;
 g_bossBattleProxy.CG_Request_Boss_Stage_ContinueOK(remote,RmiContext::ReliableSend,EmptyItemResults{},int16_t(1),LocalPayback{}); return true;
}

SevenDSQuestBattleS2C::Proxy g_questBattleProxy;
class QuestBattleStub final : public SevenDSQuestBattleC2S::Stub {
public:
 DECRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Start;
 DECRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Clear;
 DECRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Continue;
} g_questBattleStub;
DEFRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Start(QuestBattleStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 if(!GcLocal::CanEnterCampaign(3,request.stage)||!EconomyStage(3,request.stage))return CancelRequest(remote,10165);
 if(!PayStage(3,request.stage))return CancelRequest(remote,10165,101);
 GcLocal::ActiveBattles()[remote]={3,request.stage};CaptureBattleParty(remote,request.teamIndex);
 g_questBattleProxy.CG_Request_Quest_Stage_StartOK(remote,RmiContext::ReliableSend,LocalStageStartResult{request.stage,request.index,3},LocalPayback{});return true;
}
DEFRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Clear(QuestBattleStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 auto it=GcLocal::ActiveBattles().find(remote);
 if(it==GcLocal::ActiveBattles().end()||it->second!=std::make_pair(3,int(request.stage)))return CancelRequest(remote,10166);
 bool first=false;
 if(request.win){first=GcLocal::BattleClears().insert({3,request.stage}).second;GcLocal::SaveBattleProgress();}
 g_questBattleProxy.CG_Request_Quest_Stage_ClearOK(remote,RmiContext::ReliableSend,CompleteStage(3,request.stage,request.win,first,remote));
 GcLocal::ActiveBattleHeroes().erase(remote);GcLocal::ActiveBattles().erase(it);return true;
}
DEFRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Continue(QuestBattleStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 auto it=GcLocal::ActiveBattles().find(remote);
 if(it==GcLocal::ActiveBattles().end()||it->second.first!=3)return CancelRequest(remote,10167);
 g_questBattleProxy.CG_Request_Quest_Stage_ContinueOK(remote,RmiContext::ReliableSend,EmptyItemResults{},int16_t(1),LocalPayback{});return true;
}

// END RESTORED BATTLE HANDLERS

SevenDSCoinShopS2C::Proxy g_coinShopProxy;
SevenDSMaxAwakenS2C::Proxy g_maxAwakenProxy;
SevenDSSuperAwakenS2C::Proxy g_superAwakenProxy;
class MaxAwakenStub final : public SevenDSMaxAwakenC2S::Stub {
public: DECRMI_SevenDSMaxAwakenC2S_CG_RequestSkinMaxAwaken;
} g_maxAwakenStub;
class SuperAwakenStub final : public SevenDSSuperAwakenC2S::Stub {
public: DECRMI_SevenDSSuperAwakenC2S_CG_RequestSkinTranscend;
 DECRMI_SevenDSSuperAwakenC2S_CG_RequestSkinTranscendReset;
} g_superAwakenStub;
DEFRMI_SevenDSMaxAwakenC2S_CG_RequestSkinMaxAwaken(MaxAwakenStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 const int id=GcLocal::ActiveSkin(hero);if(!id||!GcLocal::OwnedSkins().count(id)||(item!=500019&&item!=910750&&GcLocal::FindMaterialType(item)!=82))return CancelRequest(remote,10103);
 if(GcLocal::DevelopmentStates()[id].awaken>=6){g_maxAwakenProxy.CG_RequestSkinMaxAwakenOK(remote,RmiContext::ReliableSend,LocalGrowthResult{id,0,{}});return true;}
 if(!GcLocal::Spend({{item,1}}))return CancelRequest(remote,10103,101);GcLocal::DevelopmentStates()[id].awaken=6;GcLocal::SaveDevelopment();
 g_maxAwakenProxy.CG_RequestSkinMaxAwakenOK(remote,RmiContext::ReliableSend,LocalGrowthResult{id,0,{item}});return true;
}
DEFRMI_SevenDSSuperAwakenC2S_CG_RequestSkinTranscend(SuperAwakenStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 const int id=GcLocal::ActiveSkin(request.hero);if(!id||!GcLocal::OwnedSkins().count(id)||request.rank<1||request.rank>6)return CancelRequest(remote,10105);
 auto& state=GcLocal::DevelopmentStates()[id];if(state.awaken<6||request.rank<=state.transcend)return CancelRequest(remote,10105);
 auto costs=request.items;int64_t required=0,provided=0;
 for(int level=state.transcend+1;level<=request.rank;++level){
   bool found=false;for(const auto& row:GcLocal::SuperAwakeningCosts)if(row.hero==request.hero&&row.level==level){required+=row.gauge+(level>state.skill+1?row.addGauge:0);found=true;break;}
   if(!found)return CancelRequest(remote,10105);
   auto nativeCost=DevelopmentCosts(request.hero,5,level);costs.insert(costs.end(),nativeCost.begin(),nativeCost.end());
 }
 for(auto payment:request.items){int points=0;for(const auto& coin:GcLocal::SuperAwakeningCoins)if(coin.item==payment.first){points=coin.points;break;}
   if(!points)return CancelRequest(remote,10105);provided+=int64_t(points)*payment.second;
 }
 if(!GcLocal::CustomMode()&&provided<required)return CancelRequest(remote,10105,101);
 if(!GcLocal::Spend(costs))return CancelRequest(remote,10105,101);state.transcend=request.rank;GcLocal::SaveDevelopment();
 std::set<int> items{5301001};for(const auto& row:costs)items.insert(row.first);
 LocalGrowthResult result{id,1,{items.begin(),items.end()}};
 g_superAwakenProxy.CG_RequestSkinTranscendOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSSuperAwakenC2S_CG_RequestSkinTranscendReset(SuperAwakenStub) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 const int id=GcLocal::ActiveSkin(hero);if(!id||!GcLocal::OwnedSkins().count(id)||itemIndex>1)return CancelRequest(remote,10106);
 auto& state=GcLocal::DevelopmentStates()[id];if(!state.transcend)return CancelRequest(remote,10106);
 std::map<int,int> refunds;for(const auto& row:GcLocal::SuperAwakeningCosts)if(row.hero==hero&&row.level<=state.transcend)refunds[row.refundItem]+=row.refundCount;
 if(refunds.empty())return CancelRequest(remote,10106);
 const auto& cost=GcLocal::SuperAwakeningResetCosts[itemIndex];if(!GcLocal::Spend({{cost.item,cost.count}}))return CancelRequest(remote,10106,101);
 std::set<int> items{cost.item};for(auto refund:refunds)if(refund.first&&refund.second>0){GcLocal::Grant(refund.first,refund.second);items.insert(refund.first);}
 state.transcend=0;GcLocal::SaveDevelopment();
 g_superAwakenProxy.CG_RequestSkinTranscendResetOK(remote,RmiContext::ReliableSend,LocalGrowthResult{id,2,{items.begin(),items.end()}});return true;
}
SevenDSFortKeyS2C::Proxy g_fortKeyProxy;
SevenDSFortCoinS2C::Proxy g_fortCoinProxy;
class FortKeyStub final : public SevenDSFortKeyC2S::Stub {
public: DECRMI_SevenDSFortKeyC2S_CG_RequestWeekStageKeyOpen;
} g_fortKeyStub;
class FortCoinStub final : public SevenDSFortCoinC2S::Stub {
public: DECRMI_SevenDSFortCoinC2S_CG_RequestWeekStageCoinOpen;
} g_fortCoinStub;
DEFRMI_SevenDSFortKeyC2S_CG_RequestWeekStageKeyOpen(FortKeyStub) {
 if(area<1||area>10000||count<1)return false;
 g_fortKeyProxy.CG_RequestWeekStageKeyOpenOK(remote,RmiContext::ReliableSend,area,count,2147483647,LocalNoItem{},MissionResult{});return true;
}
DEFRMI_SevenDSFortCoinC2S_CG_RequestWeekStageCoinOpen(FortCoinStub) {
 if(request.area<1||request.area>10000)return false;
 g_fortCoinProxy.CG_RequestWeekStageCoinOpenOK(remote,RmiContext::ReliableSend,request.area,2147483647,2147483647,0,EmptyItemResults{});return true;
}
SevenDSEventCoinS2C::Proxy g_eventCoinProxy;
class CoinShopStub final : public SevenDSCoinShopC2S::Stub {
public:
 DECRMI_SevenDSCoinShopC2S_CG_RequestCoinShopInfo;
 DECRMI_SevenDSCoinShopC2S_CG_RequestCoinShopBuy;
 DECRMI_SevenDSCoinShopC2S_CG_RequestEventCoinShopBuy;
} g_coinShopStub;
DEFRMI_SevenDSCoinShopC2S_CG_RequestCoinShopInfo(CoinShopStub) {
 g_coinShopProxy.CG_RequestCoinShopInfoOK(remote,RmiContext::ReliableSend,LocalCoinShopInfo{});return true;
}
static bool BuyCoinProduct(int remote,const LocalCoinBuyRequest& request,bool event) {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 const auto* row=GcLocal::FindCoinProduct(request.shop,event);
 if(!row||request.count<1||request.count>100)return false;
 if(!GcLocal::CustomMode()) {
  int64_t total=0;for(auto p:request.payments){if(GcLocal::FindMaterialType(p.first)!=row->payType)return CancelRequest(remote,event?10667:10666);
   if(row->payType!=6){int rating=0;for(auto c:GcLocal::PaymentCoins)if(c.id==p.first)rating=c.rating;if(rating!=row->payRating)return CancelRequest(remote,event?10667:10666);}
   total+=p.second;}
  if(total!=int64_t(row->price)*request.count)return CancelRequest(remote,event?10667:10666);
  if(!GcLocal::Spend(request.payments))return CancelRequest(remote,event?10667:10666,101);
 }
 bool newHero=false;
 if(row->type==211) {
  const auto* skin=GcLocal::FindSkin(row->item);if(!skin)return false;
  newHero=!GcLocal::OwnedHeroes().count(skin->hero);
  if(newHero){GcLocal::OwnedSkins().insert(row->item);GcLocal::SaveAccount();}
  else {for(auto c:GcLocal::HeroCoins)if(c.skin==row->item){GcLocal::Grant(c.coin,request.count);break;}}
 } else if(row->type==216) {
  GcLocal::Artifacts().insert(row->item);GcLocal::SaveExtraInventory();
 } else {
  GcLocal::Grant(row->item,request.count*row->count);
  if(GcLocal::CustomMode()){
   auto& count=GcLocal::ExtraItems()[row->item];
   count=int((std::min)(int64_t(2000000000),int64_t((std::max)(GcLocal::TestMaterialCount,count))+request.count*row->count));
   GcLocal::SaveExtraInventory();
  }
 }
 LocalCoinBuyResult result{request.shop,request.count,event,newHero,request.payments};
 if(event)g_eventCoinProxy.CG_RequestEventCoinShopBuyOK(remote,RmiContext::ReliableSend,result);
 else g_coinShopProxy.CG_RequestCoinShopBuyOK(remote,RmiContext::ReliableSend,result);
 std::printf("[Grand Cross Local] coin purchase %d x%d.\n",request.shop,request.count);return true;
}
DEFRMI_SevenDSCoinShopC2S_CG_RequestCoinShopBuy(CoinShopStub) {return BuyCoinProduct(remote,request,false);}
DEFRMI_SevenDSCoinShopC2S_CG_RequestEventCoinShopBuy(CoinShopStub) {return BuyCoinProduct(remote,request,true);}

// Native standard missions, chapter rewards and Hero's Way progression.
SevenDSMissionS2C::Proxy g_missionProxy;
class MissionStub final : public SevenDSMissionC2S::Stub {
public: DECRMI_SevenDSMissionC2S_CG_RequestMissionProgress;
 DECRMI_SevenDSMissionC2S_CG_RequestMissionClear;
 DECRMI_SevenDSMissionC2S_CG_RequestMissionGetAchievePointReward;
} g_missionStub;
DEFRMI_SevenDSMissionC2S_CG_RequestMissionProgress(MissionStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 if(addValue<0||addValue>1000)return CancelRequest(remote,10808);
 bool known=missionType==0;for(auto r:GcLocal::MissionRules)if(r.type==missionType){known=true;break;}
 if(!known)return CancelRequest(remote,10808);
 // These are client-only actions; server-owned activities update at their actual commit.
 if(addValue>0&&(missionType==31||missionType==36||missionType==39||missionType==41||missionType==44||missionType==45||missionType==46||missionType==47||missionType==48||missionType==49||missionType==98))GcLocal::RecordMission(missionType,missionTypeValue,addValue);
 GcLocal::MissionClientReady()=true;GcLocal::RefreshMissionSnapshots();GcLocal::SaveMissions();
 g_missionProxy.CG_RequestMissionProgressOK(remote,RmiContext::ReliableSend,MissionResult{true});return true;
}
DEFRMI_SevenDSMissionC2S_CG_RequestMissionClear(MissionStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);GcLocal::RefreshMissionSnapshots();
 auto prospective=GcLocal::Missions();std::set<std::pair<int,int>> seen;std::vector<const GcLocal::MissionRule*> claims;
 for(auto p:request.missions){const auto* r=GcLocal::FindMission(p.first,p.second);if(!r||!seen.insert(p).second)return CancelRequest(remote,10809);
  auto& state=prospective.at(p.first);if(p.second<=state.claimed)continue;
  if(p.second!=state.claimed+1||state.progress<r->target)return CancelRequest(remote,10809);
  state.claimed=p.second;claims.push_back(r);const auto* next=GcLocal::FindMission(p.first,p.second+1);if(next&&(next->type!=r->type||next->value!=r->value))state.progress=0;
 }
 LocalMissionClearResult result;int points=0;
 for(const auto* r:claims){auto rewards=GrantCampaignReward(GcLocal::FindMaterialType(r->item),r->item,r->count);result.rewards.insert(result.rewards.end(),rewards.begin(),rewards.end());result.chains.push_back(r->chain);points+=r->points;}
 GcLocal::Missions()=prospective;GcLocal::SaveMissions();if(points){GcLocal::Grant(500009,points);result.rewards.push_back({9,500009,points,0});}
 GcLocal::MissionClientReady()=true;g_missionProxy.CG_RequestMissionClearOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSMissionC2S_CG_RequestMissionGetAchievePointReward(MissionStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const GcLocal::AchievementRule* rule=nullptr;for(const auto& r:GcLocal::AchievementRules)if(r.order==rewardOrder){rule=&r;break;}
 if(!rule||rewardOrder>GcLocal::Progression().achievementOrder+1)return CancelRequest(remote,10811);
 LocalAchievementResult result;result.order=rewardOrder;
 if(rewardOrder>GcLocal::Progression().achievementOrder){if(GcLocal::AchievementPoints()<rule->target)return CancelRequest(remote,10811);
  GcLocal::Grant(rule->item,rule->count);GcLocal::Progression().achievementOrder=rewardOrder;GcLocal::SaveProgression();result.item=rule->item;result.count=rule->count;
 }
 GcLocal::MissionClientReady()=true;g_missionProxy.CG_RequestMissionGetAchievePointRewardOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSChapterS2C::Proxy g_chapterProxy;
class ChapterStub final : public SevenDSChapterC2S::Stub {public: DECRMI_SevenDSChapterC2S_CG_RequestQuestChapterClear;} g_chapterStub;
DEFRMI_SevenDSChapterC2S_CG_RequestQuestChapterClear(ChapterStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const auto* rule=GcLocal::FindChapter(region);
 if(!rule||rule->index<0||rule->index>=64)return CancelRequest(remote,10812);
 LocalChapterResult result;const uint64_t bit=uint64_t(1)<<rule->index;
 if(!(GcLocal::Progression().chapterFlags&bit)){
  if(!GcLocal::ChapterComplete(*rule))return CancelRequest(remote,10812);
  result.rewards=GrantCampaignReward(GcLocal::FindMaterialType(rule->item),rule->item,rule->count);GcLocal::Progression().chapterFlags|=bit;GcLocal::SaveProgression();
 }
 g_chapterProxy.CG_RequestQuestChapterClearOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSGuideS2C::Proxy g_guideProxy;
class GuideStub final : public SevenDSGuideC2S::Stub {
public: DECRMI_SevenDSGuideC2S_CG_RequestQuestGuideListAllClearReward;
 DECRMI_SevenDSGuideC2S_CG_RequestQuestGuideListStepStart;
 DECRMI_SevenDSGuideC2S_CG_RequestQuestGuideListStepClear;
} g_guideStub;
DEFRMI_SevenDSGuideC2S_CG_RequestQuestGuideListStepStart(GuideStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);auto& s=GcLocal::Progression();
 if(s.guideStep==0||(s.guideRewarded&&s.guideStep<20)){++s.guideStep;s.guideRewarded=false;}
 if(!s.guideRewarded)for(auto q:GcLocal::GuideQuests)if(q.step==s.guideStep)GcLocal::StartQuest(q.quest);
 GcLocal::RefreshQuestSnapshots();GcLocal::SaveQuests();GcLocal::SaveProgression();g_guideProxy.CG_RequestQuestGuideListStepStartOK(remote,RmiContext::ReliableSend,LocalGuideResult{});return true;
}
DEFRMI_SevenDSGuideC2S_CG_RequestQuestGuideListStepClear(GuideStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);auto& s=GcLocal::Progression();if(s.guideStep<1)return CancelRequest(remote,10821);
 LocalGuideResult result;result.clear=true;
 if(!s.guideRewarded){if(!GcLocal::GuideStepComplete())return CancelRequest(remote,10821);
  int skin=0;for(auto r:GcLocal::GuideRewards)if(r.step==s.guideStep){skin=r.skin;break;}
  const auto* row=GcLocal::FindSkin(skin);bool ur=false;if(row)for(auto r:GcLocal::DevelopmentSkins)if(r.rating==6&&GcLocal::FindSkin(r.id)->hero==row->hero){ur=true;break;}
  if(!row||!ur)return CancelRequest(remote,10821);
  result.rewards=GrantCampaignReward(211,skin,1);const auto upgraded=ApplyOneStep(row->hero,0,false);result.upgrades.emplace_back(upgraded.previous,upgraded.skin);
  s.guideRewarded=true;GcLocal::SaveProgression();
 }
 g_guideProxy.CG_RequestQuestGuideListStepClearOK(remote,RmiContext::ReliableSend,result);return true;
}
DEFRMI_SevenDSGuideC2S_CG_RequestQuestGuideListAllClearReward(GuideStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);auto& s=GcLocal::Progression();if(s.guideStep!=20||!s.guideRewarded)return CancelRequest(remote,10819);
 // Current client config sets the legacy final item to None; phase rewards are native.
 s.guideFinal=true;GcLocal::SaveProgression();g_guideProxy.CG_RequestQuestGuideListAllClearRewardOK(remote,RmiContext::ReliableSend,LocalNoItem{},MissionResult{});return true;
}

SevenDSFoodS2C::Proxy g_foodProxy;
class FoodStub final : public SevenDSFoodC2S::Stub {public:DECRMI_SevenDSFoodC2S_CG_RequestCookingUseCookingBuff;} g_foodStub;
DEFRMI_SevenDSFoodC2S_CG_RequestCookingUseCookingBuff(FoodStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(!GcLocal::EatFood(foodItemID,isAutoUse))return CancelRequest(remote,10876,101);g_foodProxy.CG_RequestCookingUseCookingBuffOK(remote,RmiContext::ReliableSend,LocalFoodResult{foodItemID});return true;}
SevenDSFoodAutoS2C::Proxy g_foodAutoProxy;
class FoodAutoStub final : public SevenDSFoodAutoC2S::Stub {public:DECRMI_SevenDSFoodAutoC2S_CG_RequestFoodBuffAutoUseOnOff;} g_foodAutoStub;
DEFRMI_SevenDSFoodAutoC2S_CG_RequestFoodBuffAutoUseOnOff(FoodAutoStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);GcLocal::Food().automatic=isAutoUse;GcLocal::SaveFood();g_foodAutoProxy.CG_RequestFoodBuffAutoUseOnOffOK(remote,RmiContext::ReliableSend,LocalFoodResult{0,0,true});return true;}
SevenDSRecipeActiveS2C::Proxy g_recipeActiveProxy;
class RecipeActiveStub final : public SevenDSRecipeActiveC2S::Stub {public:DECRMI_SevenDSRecipeActiveC2S_CG_RequestRecipeActive;} g_recipeActiveStub;
DEFRMI_SevenDSRecipeActiveC2S_CG_RequestRecipeActive(RecipeActiveStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);int item=0;for(auto r:GcLocal::RecipeBooks)if(r.recipe==recipeID){item=r.item;break;}if(!item)return CancelRequest(remote,10870);if(!GcLocal::RecipeExperience().count(recipeID)){if(!GcLocal::Spend({{item,1}}))return CancelRequest(remote,10870,101);GcLocal::RecipeExperience()[recipeID]=0;GcLocal::SaveRecipes();GcLocal::RecordMission(68,0,1);}else item=0;g_recipeActiveProxy.CG_RequestRecipeActiveOK(remote,RmiContext::ReliableSend,LocalFoodResult{item,recipeID});return true;}

SevenDSTownInfoS2C::Proxy g_townInfoProxy;
class TownInfoStub final : public SevenDSTownInfoC2S::Stub {public:DECRMI_SevenDSTownInfoC2S_CG_RequestBasePointInfo;} g_townInfoStub;
DEFRMI_SevenDSTownInfoC2S_CG_RequestBasePointInfo(TownInfoStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(!GcLocal::KnownTown(basePointID))return CancelRequest(remote,10008);g_townInfoProxy.CG_RequestBasePointInfoOK(remote,RmiContext::ReliableSend,LocalTownInfoResult{basePointID});return true;}
SevenDSTownChestS2C::Proxy g_townChestProxy;
class TownChestStub final : public SevenDSTownChestC2S::Stub {public:DECRMI_SevenDSTownChestC2S_CG_RequestBasePointUniqueInteractiveOpen;} g_townChestStub;
DEFRMI_SevenDSTownChestC2S_CG_RequestBasePointUniqueInteractiveOpen(TownChestStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const GcLocal::TownChest* row=nullptr;for(const auto& r:GcLocal::TownChests)if(r.npc==npcID)row=&r;if(!row||(row->quest&&!GcLocal::QuestCompleted(row->quest)))return CancelRequest(remote,10904);int item=0;if(GcLocal::OpenChests().insert(npcID).second){GcLocal::Grant(row->item,row->count);item=row->item;GcLocal::SaveChests();GcLocal::RecordMission(31,0,1);GcLocal::RecordQuestAction("unique_interactive",npcID,1);}g_townChestProxy.CG_RequestBasePointUniqueInteractiveOpenOK(remote,RmiContext::ReliableSend,LocalChestResult{npcID,item});return true;}
SevenDSArtifactUnionS2C::Proxy g_artifactUnionProxy;
class ArtifactUnionStub final : public SevenDSArtifactUnionC2S::Stub {public:DECRMI_SevenDSArtifactUnionC2S_CG_RequestArtifactUnionUpgrade;} g_artifactUnionStub;
DEFRMI_SevenDSArtifactUnionC2S_CG_RequestArtifactUnionUpgrade(ArtifactUnionStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const auto* r=GcLocal::FindArtifactUnion(request.id);if(!r||r->cap<=0)return CancelRequest(remote,12602);for(int card:r->cards)if(card&&!GcLocal::Artifacts().count(card))return CancelRequest(remote,12602);int64_t gain=0;for(auto p:request.items){int exp=0;for(auto m:GcLocal::UnionMaterials)if(m.id==p.first)exp=m.exp;if(!exp)return CancelRequest(remote,12602);gain+=int64_t(exp)*p.second;}int current=GcLocal::ArtifactUnionExperience()[request.id];if(current>=r->cap||gain<=0)return CancelRequest(remote,12602);if(!GcLocal::Spend(request.items))return CancelRequest(remote,12602,101);GcLocal::ArtifactUnionExperience()[request.id]=int(std::min<int64_t>(r->cap,int64_t(current)+gain));GcLocal::SaveArtifactUnions();g_artifactUnionProxy.CG_RequestArtifactUnionUpgradeOK(remote,RmiContext::ReliableSend,LocalUnionResult{request.id,request.items});return true;}

SevenDSFinalBossS2C::Proxy g_finalBossProxy;
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

SevenDSRelicUpgradeS2C::Proxy g_relicUpgradeProxy;
class RelicUpgradeStub final : public SevenDSRelicUpgradeC2S::Stub {public: DECRMI_SevenDSRelicUpgradeC2S_CG_RequestCostumeCraftUpgrade;} g_relicUpgradeStub;
DEFRMI_SevenDSRelicUpgradeC2S_CG_RequestCostumeCraftUpgrade(RelicUpgradeStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const auto* recipe=GcLocal::FindRelicUpgrade(costume,upgradeType);const auto* c=GcLocal::FindCosmetic(costume);
 if(!recipe||!c||upgradeType>=6||!GcLocal::OwnCosmetic(costume))return CancelRequest(remote,10114);
 auto key=std::make_pair(c->group,c->heroGroup);int bits=GcLocal::RelicUpgrades()[key];if(bits&(1<<upgradeType))return CancelRequest(remote,10114);
 LocalRelicUpgradeResult result;result.costume=costume;for(int i=0;i<6;++i)if(recipe->items[i]&&recipe->counts[i])result.costs.emplace_back(recipe->items[i],recipe->counts[i]);
 if(!GcLocal::Spend(result.costs))return CancelRequest(remote,10114,101);
 GcLocal::RelicUpgrades()[key]=bits|(1<<upgradeType);GcLocal::SaveRelicUpgrades();if(recipe->growth)GcLocal::Grant(540001,recipe->growth);
 g_relicUpgradeProxy.CG_RequestCostumeCraftUpgradeOK(remote,RmiContext::ReliableSend,result);return true;
}

SevenDSTownDonationS2C::Proxy g_townDonationProxy;
class TownDonationStub final : public SevenDSTownDonationC2S::Stub {public: DECRMI_SevenDSTownDonationC2S_CG_RequestBasePointGoldDonation;} g_townDonationStub;
DEFRMI_SevenDSTownDonationC2S_CG_RequestBasePointGoldDonation(TownDonationStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);int next=GcLocal::TownNextThreshold(town),exp=GcLocal::TownExperience(town);
 // Native SetNormalFellowShip uses 100 gold per friendship point. The UI
 // truncates its slider to the next friendship threshold.
 if(!GcLocal::KnownTown(town)||item!=500012||count<=0||count%100||!next||int64_t(count)/100>next-exp)return CancelRequest(remote,10901);
 if(!GcLocal::Spend({{item,count}}))return CancelRequest(remote,10901,101);
 GcLocal::TownDonationExperience()[town]+=count/100;GcLocal::SaveTownDonations();GcLocal::RecordMission(27,0,1);GcLocal::RecordMission(116,0,count);GcLocal::RecordMission(64,0,count/100);
 GcLocal::RecordQuestAction("donation",town,1);GcLocal::RecordQuestAction("donation_gold",town,count);GcLocal::RecordQuestAction("donation_value",town,count);GcLocal::RecordQuestAction("fellowship",town,count/100);
 g_townDonationProxy.CG_RequestBasePointGoldDonationOK(remote,RmiContext::ReliableSend,LocalTownDonationResult{town,count});return true;
}


SevenDSPackageInfoS2C::Proxy g_packageInfoProxy;
class PackageInfoStub final : public SevenDSPackageInfoC2S::Stub {public: DECRMI_SevenDSPackageInfoC2S_CG_RequestPackageShopInfo;} g_packageInfoStub;
DEFRMI_SevenDSPackageInfoC2S_CG_RequestPackageShopInfo(PackageInfoStub){g_packageInfoProxy.CG_RequestPackageShopInfoOK(remote,RmiContext::ReliableSend,LocalPackageInfo{});return true;}
SevenDSBulkLevelS2C::Proxy g_bulkLevelProxy;
class BulkLevelStub final : public SevenDSBulkLevelC2S::Stub {public: DECRMI_SevenDSBulkLevelC2S_CG_RequestSkinLevelUpAtOnce;} g_bulkLevelStub;
DEFRMI_SevenDSBulkLevelC2S_CG_RequestSkinLevelUpAtOnce(BulkLevelStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);LocalBulkLevelResult result;std::map<int,int64_t> costs;std::vector<std::pair<int,int>> gains;std::set<int> seen;
 if(request.entries.empty())return CancelRequest(remote,13571);
 for(auto e:request.entries){int skin=GcLocal::ActiveSkin(e.hero);if(!skin||!seen.insert(skin).second)return CancelRequest(remote,13571);int64_t gain=0;
  for(auto p:e.items){bool valid=p.first==500012;for(auto r:GcLocal::ExperienceMaterials)if(r.id==p.first){gain+=int64_t(r.exp)*p.second;valid=true;}if(!valid||p.second<=0)return CancelRequest(remote,13571);costs[p.first]+=p.second;if(costs[p.first]>2147483647)return CancelRequest(remote,13571);}
  int cap=GcLocal::ExperienceCap(skin),current=GcLocal::DevelopmentStates()[skin].exp;if(gain<=0||current>=cap)return CancelRequest(remote,13571);gains.emplace_back(skin,int(std::min<int64_t>(cap,int64_t(current)+gain)));result.skins.push_back(skin);result.entries.push_back(e);
 }
 for(auto p:costs)result.costs.emplace_back(p.first,int(p.second));if(!GcLocal::Spend(result.costs))return CancelRequest(remote,13571,101);
 for(auto p:gains)GcLocal::DevelopmentStates()[p.first].exp=p.second;GcLocal::SaveDevelopment();GcLocal::RecordMission(92,0,int(gains.size()));GcLocal::RecordMission(61,0,int(gains.size()));
 g_bulkLevelProxy.CG_RequestSkinLevelUpAtOnceOK(remote,RmiContext::ReliableSend,result);return true;
}


SevenDSBulkGrowthS2C::Proxy g_bulkGrowthProxy;
class BulkGrowthStub final : public SevenDSBulkGrowthC2S::Stub {
public:
 DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinAwakenAtOnce;
 DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinTranscendAtOnce;
 DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinEvolutionAtOnce;
 DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinOverEvolutionAtOnce;
 DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinExclusiveSkillAtOnce;
} g_bulkGrowthStub;
static bool PrepareBulkGrowth(const LocalBulkLevelRequest& request,int kind,LocalBulkGrowthResult& result){
 if(request.entries.empty())return false;std::set<int> seen;std::map<int,int64_t> totals;
 for(auto e:request.entries){int skin=GcLocal::ActiveSkin(e.hero);const auto* row=GcLocal::DevelopmentRow(skin);
  if(!row||!seen.insert(e.hero).second)return false;auto state=GcLocal::DevelopmentStates()[skin];std::vector<std::pair<int32_t,int32_t>> costs;int target=e.index;
  if(kind==1){
   int next=NextEvolutionSkin(skin);if(!next||target!=row->rating+1||(target==7&&!LegendEligible(skin)))return false;
   if(!AppendDevelopmentRecipe(e.hero,1,row->rating,0,costs))return false;result.skins.emplace_back(skin,next);result.evolution=true;
  }else if(kind==2){
   if(row->rating!=6||target<=state.limitBreak||target>8||GcLocal::SkinLevel(skin)<row->maxLevel+5*state.limitBreak)return false;
   for(int step=state.limitBreak+1;step<=target;++step)if(!AppendDevelopmentRecipe(e.hero,2,step,0,costs))return false;
   result.skins.emplace_back(skin,skin);
  }else if(kind==3){
   if(target<=state.awaken||target>6)return false;
   bool token=false;for(auto p:e.items)if(GcLocal::FindMaterialType(p.first)==82||p.first==910750){if(token||p.second!=1||target!=6)return false;token=true;costs.push_back(p);}
   if(!token)for(int step=state.awaken+1;step<=target;++step)if(!AppendDevelopmentRecipe(e.hero,3,step,0,costs))return false;
   result.skins.emplace_back(skin,skin);
  }else if(kind==5){
   if(state.awaken<6||target<=state.transcend||target>6)return false;int64_t required=0,provided=0;
   for(int step=state.transcend+1;step<=target;++step){bool found=false;for(auto r:GcLocal::SuperAwakeningCosts)if(r.hero==e.hero&&r.level==step){required+=r.gauge+(step>state.skill+1?r.addGauge:0);found=true;break;}if(!found||!AppendDevelopmentRecipe(e.hero,5,step,0,costs))return false;}
   for(auto p:e.items){if(p.first==500012)continue;int points=0;for(auto c:GcLocal::SuperAwakeningCoins)if(c.item==p.first){points=c.points;break;}if(!points)return false;provided+=int64_t(points)*p.second;costs.push_back(p);}
   if(provided<required){if(!GcLocal::CustomMode())return false;int points=0;for(auto c:GcLocal::SuperAwakeningCoins)if(c.item==5301001){points=c.points;break;}if(!points)return false;costs.emplace_back(5301001,int((required-provided+points-1)/points));}
   result.skins.emplace_back(skin,skin);
  }else return false;
  for(auto p:costs){totals[p.first]+=p.second;if(totals[p.first]>2147483647||p.second<=0)return false;}
 }
 for(auto p:totals)result.costs.emplace_back(p.first,int(p.second));return true;
}
static bool CommitBulkGrowth(const LocalBulkLevelRequest& request,int kind,LocalBulkGrowthResult& result){
 if(!PrepareBulkGrowth(request,kind,result)||!GcLocal::Spend(result.costs))return false;
 int awakenAdded=0;
 for(size_t i=0;i<request.entries.size();++i){auto p=result.skins[i];if(kind==1)CommitEvolution(p.first,p.second);else{auto& s=GcLocal::DevelopmentStates()[p.second];if(kind==2)s.limitBreak=request.entries[i].index;if(kind==3){awakenAdded+=request.entries[i].index-s.awaken;s.awaken=request.entries[i].index;}if(kind==5)s.transcend=request.entries[i].index;}}
 if(awakenAdded){GcLocal::RecordMission(19,0,awakenAdded);GcLocal::RefreshQuestSnapshots();GcLocal::SaveQuests();}
 if(kind==1)SaveEvolution();else GcLocal::SaveDevelopment();return true;
}
DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinAwakenAtOnce(BulkGrowthStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);LocalBulkGrowthResult result;if(!CommitBulkGrowth(request,3,result))return CancelRequest(remote,13572);g_bulkGrowthProxy.CG_RequestSkinAwakenAtOnceOK(remote,RmiContext::ReliableSend,result);return true;}
DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinTranscendAtOnce(BulkGrowthStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);LocalBulkGrowthResult result;if(!CommitBulkGrowth(request,5,result))return CancelRequest(remote,13573);g_bulkGrowthProxy.CG_RequestSkinTranscendAtOnceOK(remote,RmiContext::ReliableSend,result);return true;}
DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinEvolutionAtOnce(BulkGrowthStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);LocalBulkGrowthResult result;if(!CommitBulkGrowth(request,1,result))return CancelRequest(remote,13574);g_bulkGrowthProxy.CG_RequestSkinEvolutionAtOnceOK(remote,RmiContext::ReliableSend,result);return true;}
DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinOverEvolutionAtOnce(BulkGrowthStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);LocalBulkGrowthResult result;if(!CommitBulkGrowth(request,2,result))return CancelRequest(remote,13575);g_bulkGrowthProxy.CG_RequestSkinOverEvolutionAtOnceOK(remote,RmiContext::ReliableSend,result);return true;}
DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinExclusiveSkillAtOnce(BulkGrowthStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(request.heroes.empty())return CancelRequest(remote,13576);LocalBulkGrowthResult result;result.passive=true;std::set<int> seen;
 for(int hero:request.heroes){int skin=GcLocal::ActiveSkin(hero);if(!skin||!seen.insert(hero).second)return CancelRequest(remote,13576);result.skins.emplace_back(skin,skin);}
 for(auto p:result.skins)GcLocal::UnlockedPassives().insert(p.second);GcLocal::SavePassives();g_bulkGrowthProxy.CG_RequestSkinExclusiveSkillAtOnceOK(remote,RmiContext::ReliableSend,result);return true;
}
SevenDSBulkUltimateS2C::Proxy g_bulkUltimateProxy;
class BulkUltimateStub final : public SevenDSBulkUltimateC2S::Stub {public:DECRMI_SevenDSBulkUltimateC2S_CG_RequestSkinSkillLevelUpAtOnce;} g_bulkUltimateStub;
DEFRMI_SevenDSBulkUltimateC2S_CG_RequestSkinSkillLevelUpAtOnce(BulkUltimateStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(request.entries.empty())return CancelRequest(remote,13550);LocalBulkGrowthResult result;result.packages=false;std::set<int> seen;std::map<int,int64_t> totals;
 for(auto e:request.entries){int skin=GcLocal::ActiveSkin(e.first);if(!skin||!seen.insert(e.first).second)return CancelRequest(remote,13550);int current=GcLocal::DevelopmentStates()[skin].skill;
  if(e.second<1||current+e.second>5)return CancelRequest(remote,13550);std::vector<std::pair<int32_t,int32_t>> costs;
  for(int step=current+2;step<=current+e.second+1;++step)if(!AppendDevelopmentRecipe(e.first,4,step,0,costs))return CancelRequest(remote,13550);
  for(auto p:costs){totals[p.first]+=p.second;if(totals[p.first]>2147483647)return CancelRequest(remote,13550);}result.skins.emplace_back(skin,skin);
 }
 for(auto p:totals)result.costs.emplace_back(p.first,int(p.second));if(!GcLocal::Spend(result.costs))return CancelRequest(remote,13550,101);
 for(size_t i=0;i<result.skins.size();++i)GcLocal::DevelopmentStates()[result.skins[i].second].skill+=request.entries[i].second;GcLocal::SaveDevelopment();g_bulkUltimateProxy.CG_RequestSkinSkillLevelUpAtOnceOK(remote,RmiContext::ReliableSend,result);return true;
}

SevenDSFinalBossShopS2C::Proxy g_finalBossShopProxy;
class FinalBossShopStub final : public SevenDSFinalBossShopC2S::Stub {public: DECRMI_SevenDSFinalBossShopC2S_CG_RequestFinalBossShopInfo;DECRMI_SevenDSFinalBossShopC2S_CG_RequestFinalBossShopBuy;} g_finalBossShopStub;
DEFRMI_SevenDSFinalBossShopC2S_CG_RequestFinalBossShopInfo(FinalBossShopStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);g_finalBossShopProxy.CG_RequestFinalBossShopInfoOK(remote,RmiContext::ReliableSend,LocalFinalBossShopInfo{});return true;}
DEFRMI_SevenDSFinalBossShopC2S_CG_RequestFinalBossShopBuy(FinalBossShopStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const auto* r=GcLocal::FindFinalBossProduct(product);if(!r||r->season!=season||!count||!GcLocal::FinalBossRewardType(r->item)||!GcLocal::FindMaterialType(r->price))return CancelRequest(remote,10689);
 auto p=GcLocal::FinalBossPurchases()[product];int daily=GcLocal::FinalBossDaily(p);if((r->dailyLimit>0&&daily+count>r->dailyLimit)||(r->seasonLimit>0&&p.total+count>r->seasonLimit)||daily+count>255||p.total+count>32767)return CancelRequest(remote,10689);
 if(!GcLocal::Spend({{r->price,r->amount*count}}))return CancelRequest(remote,10689,101);auto rewards=GrantCampaignReward(GcLocal::FinalBossRewardType(r->item),r->item,r->count*count);GcLocal::FinalBossPurchases()[product]={GcLocal::FinalBossToday(),daily+count,p.total+count};GcLocal::SaveFinalBossPurchases();
 g_finalBossShopProxy.CG_RequestFinalBossShopBuyOK(remote,RmiContext::ReliableSend,LocalFinalBossShopBuy{product,count,rewards});return true;
}


SevenDSDescentS2C::Proxy g_descentProxy;
class DescentStub final : public SevenDSDescentC2S::Stub {public: DECRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Start;DECRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Clear;DECRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Continue;DECRMI_SevenDSDescentC2S_CG_Request_DescentBoss_Event_Point_Reward;} g_descentStub;
DEFRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Start(DescentStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);if(!GcLocal::FindDescent(request.stage))return CancelRequest(remote,10364);if(!PayStage(6,request.stage))return CancelRequest(remote,10364,101);GcLocal::ActiveBattles()[remote]={6,request.stage};CaptureBattleParty(remote,request.teamIndex);g_descentProxy.CG_Request_DescentBoss_EventStage_StartOK(remote,RmiContext::ReliableSend,LocalStageStartResult{request.stage,request.index,6},EmptyItemResults{},LocalPayback{});return true;}
DEFRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Clear(DescentStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const auto* row=GcLocal::FindDescent(request.stage);auto active=GcLocal::ActiveBattles().find(remote);if(!row||active==GcLocal::ActiveBattles().end()||active->second!=std::make_pair(6,request.stage))return CancelRequest(remote,10365);bool first=!GcLocal::BattleClears().count({6,request.stage});auto result=CompleteStage(6,request.stage,request.win,first,remote);if(request.win){GcLocal::BattleClears().insert({6,request.stage});GcLocal::SaveBattleProgress();if(row->point&&row->pointCount){auto rewards=GrantCampaignReward(GcLocal::FindMaterialType(row->point),row->point,row->pointCount);result.nativeDrops.insert(result.nativeDrops.end(),rewards.begin(),rewards.end());}}GcLocal::ActiveBattles().erase(active);GcLocal::ActiveBattleHeroes().erase(remote);g_descentProxy.CG_Request_DescentBoss_EventStage_ClearOK(remote,RmiContext::ReliableSend,result,LocalDescentInfo{request.win?request.stage:0},EmptyItemResults{},int32_t(0),int32_t(GcLocal::SeededMaterialCount(row->point)));return true;}
DEFRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Continue(DescentStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);auto active=GcLocal::ActiveBattles().find(remote);if(active==GcLocal::ActiveBattles().end()||active->second.first!=6)return CancelRequest(remote,10366);g_descentProxy.CG_Request_DescentBoss_EventStage_ContinueOK(remote,RmiContext::ReliableSend,EmptyItemResults{},int16_t(1),LocalPayback{});return true;}


DEFRMI_SevenDSDescentC2S_CG_Request_DescentBoss_Event_Point_Reward(DescentStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const GcLocal::DescentPointReward* row=nullptr;for(const auto& r:GcLocal::DescentPointRewards)if(r.step==step){row=&r;break;}if(eventSEQ!=GcLocal::DescentEventSequence||!row||step<1||step>5||(GcLocal::DescentRewardFlags()&(1<<step))||GcLocal::SeededMaterialCount(GcLocal::DescentPointItem)<row->needed)return CancelRequest(remote,10367);auto rewards=GrantCampaignReward(GcLocal::FindMaterialType(row->item),row->item,row->count);GcLocal::DescentRewardFlags()|=1<<step;GcLocal::SaveDescentRewards();g_descentProxy.CG_Request_DescentBoss_Event_Point_RewardOK(remote,RmiContext::ReliableSend,LocalDescentRewardResult{rewards});return true;}


SevenDSChapterSkipS2C::Proxy g_chapterSkipProxy;
class ChapterSkipStub final : public SevenDSChapterSkipC2S::Stub {public: DECRMI_SevenDSChapterSkipC2S_CG_RequestItemUseChapterSkip;} g_chapterSkipStub;
DEFRMI_SevenDSChapterSkipC2S_CG_RequestItemUseChapterSkip(ChapterSkipStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 const auto* rule=GcLocal::FindChapterSkip(skipID);
 if(!rule||rule->cost<1||rule->quests.empty())return CancelRequest(remote,11112);
 if(rule->previous){const auto* prev=GcLocal::FindChapterSkip(rule->previous);if(!prev||prev->quests.empty())return CancelRequest(remote,11112);for(int q:prev->quests)if(!GcLocal::QuestCompleted(q))return CancelRequest(remote,11112);}
 LocalChapterSkipResult result;result.cost=rule->cost;
 for(int id:rule->quests)if(!GcLocal::QuestCompleted(id)){if(!GcLocal::FindQuest(id))return CancelRequest(remote,11112);result.quests.push_back(id);}
 for(int id:rule->stages){const auto* stage=GcLocal::FindCampaignStage(0,id);bool complete=stage&&stage->main?GcLocal::CampaignStageCompleted(id):GcLocal::BattleClears().count({0,id})>0;if(!complete)result.stages.push_back(id);}
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

SevenDSTowerShopS2C::Proxy g_towerShopProxy;
class TowerShopStub final : public SevenDSTowerShopC2S::Stub {public: DECRMI_SevenDSTowerShopC2S_CG_RequestYggdrasilTowerShopInfo;DECRMI_SevenDSTowerShopC2S_CG_RequestYggdrasilTowerShopBuy;} g_towerShopStub;
DEFRMI_SevenDSTowerShopC2S_CG_RequestYggdrasilTowerShopInfo(TowerShopStub){std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);g_towerShopProxy.CG_RequestYggdrasilTowerShopInfoOK(remote,RmiContext::ReliableSend,LocalTowerShopInfo{});return true;}
DEFRMI_SevenDSTowerShopC2S_CG_RequestYggdrasilTowerShopBuy(TowerShopStub){
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);const auto* r=GcLocal::FindTowerShopProduct(product);if(!r||!count||!GcLocal::TowerShopRewardType(product)||!GcLocal::FindMaterialType(r->price))return CancelRequest(remote,12583);
 auto p=GcLocal::TowerShopPurchases()[product];int daily=GcLocal::TowerShopDaily(p);if((r->dailyLimit>0&&daily+count>r->dailyLimit)||(r->totalLimit>0&&p.total+count>r->totalLimit)||daily+count>255||p.total+count>255)return CancelRequest(remote,12583);
 if(!GcLocal::Spend({{r->price,r->amount*count}}))return CancelRequest(remote,12583,101);auto rewards=GrantCampaignReward(GcLocal::TowerShopRewardType(product),r->item,r->count*count);GcLocal::TowerShopPurchases()[product]={GcLocal::TowerShopToday(),daily+count,p.total+count};GcLocal::SaveTowerShopPurchases();
 g_towerShopProxy.CG_RequestYggdrasilTowerShopBuyOK(remote,RmiContext::ReliableSend,LocalTowerShopBuy{product,count,rewards});return true;
}


bool PhoneDispatch(int fd,uint16_t id,Proud::CMessage& m) { switch(id) {
case 12603: { LocalArtifactTeam request{}; m >> request;  return g_artifactTeamStub.CG_RequestArtifactTeamChange(fd,Proud::RmiContext::ReliableSend, request); }
case 12604: { LocalArtifactTeamList request{}; m >> request;  return g_artifactTeamStub.CG_RequestArtifactDescentBossTeamChange(fd,Proud::RmiContext::ReliableSend, request); }
case 10116: { int hero{}; m >> hero; uint8 rank{}; m >> rank; uint8 type{}; m >> type;  return g_trueStub.CG_RequestSkinExceed(fd,Proud::RmiContext::ReliableSend, hero, rank, type); }
case 13695: { int hero{}; m >> hero; uint8 type{}; m >> type;  return g_trueSelectStub.CG_RequestSkinExceedSelect(fd,Proud::RmiContext::ReliableSend, hero, type); }
case 10107: { int costume{}; m >> costume; bool quick{}; m >> quick;  return g_relicStub.CG_RequestCostumeCraft(fd,Proud::RmiContext::ReliableSend, costume, quick); }
case 10451: { uint8 language{}; m >> language;  return g_mailStub.CG_RequestMailList(fd,Proud::RmiContext::ReliableSend, language); }
case 10452: { int serial{}; m >> serial; bool multi{}; m >> multi;  return g_mailStub.CG_RequestMailConfirm(fd,Proud::RmiContext::ReliableSend, serial, multi); }
case 10453: {  return g_mailStub.CG_RequestMailConfirmAll(fd,Proud::RmiContext::ReliableSend); }
case 10121: { int skin{}; m >> skin; int serial{}; m >> serial; int slot{}; m >> slot; bool remove{}; m >> remove;  return g_equipmentStub.CG_RequestWeaponEquip(fd,Proud::RmiContext::ReliableSend, skin, serial, slot, remove); }
case 10122: { int skin{}; m >> skin; int slot{}; m >> slot;  return g_equipmentStub.CG_RequestWeaponUnEquip(fd,Proud::RmiContext::ReliableSend, skin, slot); }
case 10123: { LocalIntListRequest request{}; m >> request; int sellType{}; m >> sellType; int basepoint{}; m >> basepoint;  return g_equipmentStub.CG_RequestWeaponSell(fd,Proud::RmiContext::ReliableSend, request, sellType, basepoint); }
case 10124: { LocalIntListRequest request{}; m >> request;  return g_equipmentStub.CG_RequestWeaponGrind(fd,Proud::RmiContext::ReliableSend, request); }
case 10125: { int serial{}; m >> serial; int16 gauge{}; m >> gauge;  return g_equipmentStub.CG_RequestWeaponUpgrade(fd,Proud::RmiContext::ReliableSend, serial, gauge); }
case 10126: { int serial{}; m >> serial; int item{}; m >> item;  return g_equipmentStub.CG_RequestWeaponUpgradeRetry(fd,Proud::RmiContext::ReliableSend, serial, item); }
case 10127: { int serial{}; m >> serial;  return g_equipmentStub.CG_RequestWeaponEvolution(fd,Proud::RmiContext::ReliableSend, serial); }
case 10128: { int serial{}; m >> serial; int slot{}; m >> slot; int item{}; m >> item;  return g_equipmentStub.CG_RequestWeaponEvolutionRetry(fd,Proud::RmiContext::ReliableSend, serial, slot, item); }
case 10129: { int serial{}; m >> serial; int slot{}; m >> slot; uint8 enhanceType{}; m >> enhanceType;  return g_equipmentStub.CG_RequestWeaponOptionEnhance(fd,Proud::RmiContext::ReliableSend, serial, slot, enhanceType); }
case 10130: { int serial{}; m >> serial;  return g_equipmentStub.CG_RequestWeaponLock(fd,Proud::RmiContext::ReliableSend, serial); }
case 10131: { int serial{}; m >> serial;  return g_equipmentStub.CG_RequestWeaponUnLock(fd,Proud::RmiContext::ReliableSend, serial); }
case 10132: { int pickedSerial{}; m >> pickedSerial; int pickedSkin{}; m >> pickedSkin; int targetSerial{}; m >> targetSerial; int targetSkin{}; m >> targetSkin; int slot{}; m >> slot; bool remove{}; m >> remove;  return g_equipmentStub.CG_RequestWeaponEquipExchange(fd,Proud::RmiContext::ReliableSend, pickedSerial, pickedSkin, targetSerial, targetSkin, slot, remove); }
case 10133: { int targetSkin{}; m >> targetSkin; int sourceSkin{}; m >> sourceSkin; int mode{}; m >> mode;  return g_equipmentStub.CG_RequestWeaponEquipExchangeAll(fd,Proud::RmiContext::ReliableSend, targetSkin, sourceSkin, mode); }
case 10134: { int skin{}; m >> skin; LocalIntListRequest request{}; m >> request;  return g_equipmentStub.CG_RequestWeaponEquipRecommend(fd,Proud::RmiContext::ReliableSend, skin, request); }
case 10135: { int eventSeq{}; m >> eventSeq; int serial{}; m >> serial; uint8 heroGroup{}; m >> heroGroup;  return g_equipmentStub.CG_RequestWeaponCarve(fd,Proud::RmiContext::ReliableSend, eventSeq, serial, heroGroup); }
case 10136: { int eventSeq{}; m >> eventSeq; int serial{}; m >> serial;  return g_equipmentStub.CG_RequestWeaponCarveRemove(fd,Proud::RmiContext::ReliableSend, eventSeq, serial); }
case 11105: { LocalBoxRequest request{}; m >> request;  return g_boxStub.CG_RequestItemUseBoxOpen(fd,Proud::RmiContext::ReliableSend, request); }
case 11108: { int item{}; m >> item; int selected{}; m >> selected;  return g_equipmentTicketStub.CG_RequestItemUseWeaponTicket(fd,Proud::RmiContext::ReliableSend, item, selected); }
case 10801: { int questID{}; m >> questID;  return g_questStub.CG_RequestQuestStart(fd,Proud::RmiContext::ReliableSend, questID); }
case 10802: { int questID{}; m >> questID; int needID{}; m >> needID; uint8 propIndex{}; m >> propIndex;  return g_questStub.CG_RequestQuestProgress(fd,Proud::RmiContext::ReliableSend, questID, needID, propIndex); }
case 10803: { int questID{}; m >> questID;  return g_questStub.CG_RequestQuestClear(fd,Proud::RmiContext::ReliableSend, questID); }
case 10871: {  return g_recipeInfoStub.CG_RequestCookingRecipeOrderInfo(fd,Proud::RmiContext::ReliableSend); }
case 10869: { LocalCookingRequest request{}; m >> request;  return g_cookingStub.CG_RequestCookingStart(fd,Proud::RmiContext::ReliableSend, request); }
case 10659: { int basepointID{}; m >> basepointID; bool isCommonShop{}; m >> isCommonShop;  return g_townShopStub.CG_RequestBasePointShopInfo(fd,Proud::RmiContext::ReliableSend, basepointID, isCommonShop); }
case 10660: { LocalTownBuyRequest request{}; m >> request;  return g_townShopStub.CG_RequestBasePointShopBuy(fd,Proud::RmiContext::ReliableSend, request); }
case 10014: { int skin{}; m >> skin;  return g_mainSkinStub.CG_RequestMainSkinChange(fd,Proud::RmiContext::ReliableSend, skin); }
case 10113: { int targetHeroID{}; m >> targetHeroID;  return g_legendStub.CG_RequestSkinLegendEvolution(fd,Proud::RmiContext::ReliableSend, targetHeroID); }
case 13505: { int targetHeroID{}; m >> targetHeroID;  return g_oneStepLiteStub.CG_RequestSkinOneStepEvolutionLite(fd,Proud::RmiContext::ReliableSend, targetHeroID); }
case 10110: { int targetHeroID{}; m >> targetHeroID;  return g_oneStepStub.CG_RequestSkinOneStepEvolution(fd,Proud::RmiContext::ReliableSend, targetHeroID); }
case 10089: { int targetHeroID{}; m >> targetHeroID;  return g_evolutionStub.CG_RequestSkinEvolution(fd,Proud::RmiContext::ReliableSend, targetHeroID); }
case 10090: { int targetHeroID{}; m >> targetHeroID; uint8 skillLevelUpCount{}; m >> skillLevelUpCount;  return g_evolutionStub.CG_RequestSkinSkillLevelUp(fd,Proud::RmiContext::ReliableSend, targetHeroID, skillLevelUpCount); }
case 10096: { int targetHeroID{}; m >> targetHeroID;  return g_limitBreakStub.CG_RequestSkinOverEvolution(fd,Proud::RmiContext::ReliableSend, targetHeroID); }
case 10112: { int targetHeroID{}; m >> targetHeroID; uint8_t targetMaxLevelCount{}; m >> targetMaxLevelCount;  return g_straightBreakStub.CG_RequestSkinOverEvolutionStraight(fd,Proud::RmiContext::ReliableSend, targetHeroID, targetMaxLevelCount); }
case 10669: {  return g_cosmeticShopStub.CG_RequestCostumeShopInfo(fd,Proud::RmiContext::ReliableSend); }
case 10101: { IntList idList{}; m >> idList;  return g_storyCostumeStub.CG_RequestStoryCostume(fd,Proud::RmiContext::ReliableSend, idList); }
case 10093: { int costumeID{}; m >> costumeID; int targetHeroID{}; m >> targetHeroID;  return g_cosmeticEquipStub.CG_RequestCostumeEquip(fd,Proud::RmiContext::ReliableSend, costumeID, targetHeroID); }
case 10094: { int costumeID{}; m >> costumeID; int targetHeroID{}; m >> targetHeroID;  return g_cosmeticEquipStub.CG_RequestCostumeUnEquip(fd,Proud::RmiContext::ReliableSend, costumeID, targetHeroID); }
case 10109: { int heroId{}; m >> heroId;  return g_passiveStub.CG_RequestGetExclusiveSkill(fd,Proud::RmiContext::ReliableSend, heroId); }
case 10081: { LocalLevelUpRequest request{}; m >> request;  return g_developmentStub.CG_RequestSkinLevelUpBySkinMaterial(fd,Proud::RmiContext::ReliableSend, request); }
case 10085: { int hero{}; m >> hero; uint8 awaken{}; m >> awaken;  return g_developmentStub.CG_RequestSkinAwaken(fd,Proud::RmiContext::ReliableSend, hero, awaken); }
case 10120: { int hero{}; m >> hero; uint8 awaken{}; m >> awaken;  return g_awakenStraightStub.CG_RequestSkinAwakenStraight(fd,Proud::RmiContext::ReliableSend, hero, awaken); }
case 10336: {  return g_battleReadyStub.CG_RequestIngameBattleStart(fd,Proud::RmiContext::ReliableSend); }
case 10156: { LocalStageStartRequest request{}; m >> request;  return g_storyStartStub.CG_Request_Main_Stage_Start(fd,Proud::RmiContext::ReliableSend, request); }
case 10157: { LocalStageClearRequest request{}; m >> request;  return g_storyStartStub.CG_Request_Main_Stage_Clear(fd,Proud::RmiContext::ReliableSend, request); }
case 10151: {  return g_storyInfoStub.CG_RequestStageInfo(fd,Proud::RmiContext::ReliableSend); }
case 10651: { GambleShopBuyRequest gambleRequest{}; m >> gambleRequest;  return g_gachaBuyStub.CG_RequestGambleShopBuy(fd,Proud::RmiContext::ReliableSend, gambleRequest); }
case 10703: { int gambleType{}; m >> gambleType; GambleChecksumList gambleCheckSumInfoList{}; m >> gambleCheckSumInfoList;  return g_gachaShopStub.CG_RequestGambleShopInfo(fd,Proud::RmiContext::ReliableSend, gambleType, gambleCheckSumInfoList); }
case 10654: {  return g_gachaItemStub.CG_RequestItemGambleShopInfo(fd,Proud::RmiContext::ReliableSend); }
case 10867: { uint8 deviceType{}; m >> deviceType;  return g_attendanceStub.CG_RequestAttendanceReward(fd,Proud::RmiContext::ReliableSend, deviceType); }
case 10295: { IntList targetHeroIDList{}; m >> targetHeroIDList; IntList costumeGroupIDList{}; m >> costumeGroupIDList; IntList targetHeroGroupIDList{}; m >> targetHeroGroupIDList;  return g_costumeStub.CG_RequestCostumeUnLock(fd,Proud::RmiContext::ReliableSend, targetHeroIDList, costumeGroupIDList, targetHeroGroupIDList); }
case 10004: { uint8 teamIndex{}; m >> teamIndex;  return g_gameRequestStub.CG_RequestTeamInfo(fd,Proud::RmiContext::ReliableSend, teamIndex); }
case 10005: { LocalTeamChange request{}; m >> request;  return g_gameRequestStub.CG_RequestTeamSlotChange(fd,Proud::RmiContext::ReliableSend, request); }
case 10007: {  return g_gameRequestStub.CG_RequestLobbyInfo(fd,Proud::RmiContext::ReliableSend); }
case 10009: {  return g_gameRequestStub.CG_RequestMercenaryList(fd,Proud::RmiContext::ReliableSend); }
case 10015: {  return g_gameRequestStub.CG_RequestEventList(fd,Proud::RmiContext::ReliableSend); }
case 10024: {  return g_gameRequestStub.CG_RequestServerVersion(fd,Proud::RmiContext::ReliableSend); }
case 10051: {  return g_gameRequestStub.CG_RequestSecurityToken(fd,Proud::RmiContext::ReliableSend); }
case 10052: {  return g_gameRequestStub.CG_RequestNetmarbleAuth(fd,Proud::RmiContext::ReliableSend); }
case 10053: { Proud::String netmarblePlayerID{}; m >> netmarblePlayerID; NetmarbleSDKInfo sdkInfo{}; m >> sdkInfo;  return g_gameRequestStub.CG_RequestAuthenticateCreate(fd,Proud::RmiContext::ReliableSend, netmarblePlayerID, sdkInfo); }
case 10055: {  return g_gameRequestStub.CG_RequestLogin(fd,Proud::RmiContext::ReliableSend); }
case 10056: { int64 usn{}; m >> usn; NetmarbleSDKInfo sdkInfo{}; m >> sdkInfo; int sessionKey{}; m >> sessionKey; VersionInfo versionInfo{}; m >> versionInfo; Proud::String rejoinData{}; m >> rejoinData; int64 clientTimeTick{}; m >> clientTimeTick; int reconnectRequestRmiID{}; m >> reconnectRequestRmiID; uint8 languageType{}; m >> languageType; int talkChannelID{}; m >> talkChannelID; int buildCountry{}; m >> buildCountry;  return g_gameRequestStub.CG_RequestLoginInstantly(fd,Proud::RmiContext::ReliableSend, usn, sdkInfo, sessionKey, versionInfo, rejoinData, clientTimeTick, reconnectRequestRmiID, languageType, talkChannelID, buildCountry); }
case 10074: { int verifyType{}; m >> verifyType;  return g_gameRequestStub.CG_RequestBillingCouponVerify(fd,Proud::RmiContext::ReliableSend, verifyType); }
case 10892: { int attendanceHeroID{}; m >> attendanceHeroID; int activeAttendanceHeroID{}; m >> activeAttendanceHeroID;  return g_bootstrapRequestStub.CG_RequestLobbySetAttendanceHero(fd,Proud::RmiContext::ReliableSend, attendanceHeroID, activeAttendanceHeroID); }
case 10153: { LocalStageStartRequest request{}; m >> request;  return g_weekBattleStub.CG_Request_Week_Stage_Start(fd,Proud::RmiContext::ReliableSend, request); }
case 10154: { LocalStageClearRequest request{}; m >> request;  return g_weekBattleStub.CG_Request_Week_Stage_Clear(fd,Proud::RmiContext::ReliableSend, request); }
case 10155: {  return g_weekBattleStub.CG_Request_Week_Stage_Continue(fd,Proud::RmiContext::ReliableSend); }
case 10168: { LocalStageStartRequest request{}; m >> request;  return g_bossBattleStub.CG_Request_Boss_Stage_Start(fd,Proud::RmiContext::ReliableSend, request); }
case 10169: { LocalStageClearRequest request{}; m >> request;  return g_bossBattleStub.CG_Request_Boss_Stage_Clear(fd,Proud::RmiContext::ReliableSend, request); }
case 10170: {  return g_bossBattleStub.CG_Request_Boss_Stage_Continue(fd,Proud::RmiContext::ReliableSend); }
case 10165: { LocalStageStartRequest request{}; m >> request;  return g_questBattleStub.CG_Request_Quest_Stage_Start(fd,Proud::RmiContext::ReliableSend, request); }
case 10166: { LocalStageClearRequest request{}; m >> request;  return g_questBattleStub.CG_Request_Quest_Stage_Clear(fd,Proud::RmiContext::ReliableSend, request); }
case 10167: {  return g_questBattleStub.CG_Request_Quest_Stage_Continue(fd,Proud::RmiContext::ReliableSend); }
case 10103: { int hero{}; m >> hero; int item{}; m >> item;  return g_maxAwakenStub.CG_RequestSkinMaxAwaken(fd,Proud::RmiContext::ReliableSend, hero, item); }
case 10105: { LocalTranscendRequest request{}; m >> request;  return g_superAwakenStub.CG_RequestSkinTranscend(fd,Proud::RmiContext::ReliableSend, request); }
case 10106: { int hero{}; m >> hero; uint8 itemIndex{}; m >> itemIndex;  return g_superAwakenStub.CG_RequestSkinTranscendReset(fd,Proud::RmiContext::ReliableSend, hero, itemIndex); }
case 11102: { int area{}; m >> area; uint8 count{}; m >> count;  return g_fortKeyStub.CG_RequestWeekStageKeyOpen(fd,Proud::RmiContext::ReliableSend, area, count); }
case 11111: { LocalFortCoinOpenRequest request{}; m >> request;  return g_fortCoinStub.CG_RequestWeekStageCoinOpen(fd,Proud::RmiContext::ReliableSend, request); }
case 10665: {  return g_coinShopStub.CG_RequestCoinShopInfo(fd,Proud::RmiContext::ReliableSend); }
case 10666: { LocalCoinBuyRequest request{}; m >> request;  return g_coinShopStub.CG_RequestCoinShopBuy(fd,Proud::RmiContext::ReliableSend, request); }
case 10667: { LocalCoinBuyRequest request{}; m >> request;  return g_coinShopStub.CG_RequestEventCoinShopBuy(fd,Proud::RmiContext::ReliableSend, request); }
case 10808: { int16 missionType{}; m >> missionType; int missionTypeValue{}; m >> missionTypeValue; int addValue{}; m >> addValue;  return g_missionStub.CG_RequestMissionProgress(fd,Proud::RmiContext::ReliableSend, missionType, missionTypeValue, addValue); }
case 10809: { LocalMissionClearRequest request{}; m >> request;  return g_missionStub.CG_RequestMissionClear(fd,Proud::RmiContext::ReliableSend, request); }
case 10811: { int16 rewardOrder{}; m >> rewardOrder;  return g_missionStub.CG_RequestMissionGetAchievePointReward(fd,Proud::RmiContext::ReliableSend, rewardOrder); }
case 10812: { int region{}; m >> region;  return g_chapterStub.CG_RequestQuestChapterClear(fd,Proud::RmiContext::ReliableSend, region); }
case 10819: {  return g_guideStub.CG_RequestQuestGuideListAllClearReward(fd,Proud::RmiContext::ReliableSend); }
case 10820: {  return g_guideStub.CG_RequestQuestGuideListStepStart(fd,Proud::RmiContext::ReliableSend); }
case 10821: {  return g_guideStub.CG_RequestQuestGuideListStepClear(fd,Proud::RmiContext::ReliableSend); }
case 10876: { int foodItemID{}; m >> foodItemID; bool isAutoUse{}; m >> isAutoUse;  return g_foodStub.CG_RequestCookingUseCookingBuff(fd,Proud::RmiContext::ReliableSend, foodItemID, isAutoUse); }
case 11103: { bool isAutoUse{}; m >> isAutoUse;  return g_foodAutoStub.CG_RequestFoodBuffAutoUseOnOff(fd,Proud::RmiContext::ReliableSend, isAutoUse); }
case 10870: { int recipeID{}; m >> recipeID;  return g_recipeActiveStub.CG_RequestRecipeActive(fd,Proud::RmiContext::ReliableSend, recipeID); }
case 10008: { int basePointID{}; m >> basePointID;  return g_townInfoStub.CG_RequestBasePointInfo(fd,Proud::RmiContext::ReliableSend, basePointID); }
case 10904: { int npcID{}; m >> npcID;  return g_townChestStub.CG_RequestBasePointUniqueInteractiveOpen(fd,Proud::RmiContext::ReliableSend, npcID); }
case 12602: { LocalUnionRequest request{}; m >> request;  return g_artifactUnionStub.CG_RequestArtifactUnionUpgrade(fd,Proud::RmiContext::ReliableSend, request); }
case 10187: { LocalStageStartRequest request{}; m >> request;  return g_finalBossStub.CG_Request_FinalBoss_Stage_Start(fd,Proud::RmiContext::ReliableSend, request); }
case 10188: { LocalStageClearRequest request{}; m >> request;  return g_finalBossStub.CG_Request_FinalBoss_Stage_Clear(fd,Proud::RmiContext::ReliableSend, request); }
case 10189: {  return g_finalBossStub.CG_Request_FinalBoss_Stage_Continue(fd,Proud::RmiContext::ReliableSend); }
case 10190: {  return g_finalBossStub.CG_Request_FinalBoss_Season_Info(fd,Proud::RmiContext::ReliableSend); }
case 10207: { int seasonID{}; m >> seasonID; int bossGroupID{}; m >> bossGroupID;  return g_finalBossRankStub.CG_Request_FinalBoss_Season_Rank_Info(fd,Proud::RmiContext::ReliableSend, seasonID, bossGroupID); }
case 10114: { int costume{}; m >> costume; uint8 upgradeType{}; m >> upgradeType;  return g_relicUpgradeStub.CG_RequestCostumeCraftUpgrade(fd,Proud::RmiContext::ReliableSend, costume, upgradeType); }
case 10901: { int town{}; m >> town; int item{}; m >> item; int count{}; m >> count;  return g_townDonationStub.CG_RequestBasePointGoldDonation(fd,Proud::RmiContext::ReliableSend, town, item, count); }
case 10700: {  return g_packageInfoStub.CG_RequestPackageShopInfo(fd,Proud::RmiContext::ReliableSend); }
case 13571: { LocalBulkLevelRequest request{}; m >> request;  return g_bulkLevelStub.CG_RequestSkinLevelUpAtOnce(fd,Proud::RmiContext::ReliableSend, request); }
case 13572: { LocalBulkLevelRequest request{}; m >> request;  return g_bulkGrowthStub.CG_RequestSkinAwakenAtOnce(fd,Proud::RmiContext::ReliableSend, request); }
case 13573: { LocalBulkLevelRequest request{}; m >> request;  return g_bulkGrowthStub.CG_RequestSkinTranscendAtOnce(fd,Proud::RmiContext::ReliableSend, request); }
case 13574: { LocalBulkLevelRequest request{}; m >> request;  return g_bulkGrowthStub.CG_RequestSkinEvolutionAtOnce(fd,Proud::RmiContext::ReliableSend, request); }
case 13575: { LocalBulkLevelRequest request{}; m >> request;  return g_bulkGrowthStub.CG_RequestSkinOverEvolutionAtOnce(fd,Proud::RmiContext::ReliableSend, request); }
case 13576: { LocalBulkPassiveRequest request{}; m >> request;  return g_bulkGrowthStub.CG_RequestSkinExclusiveSkillAtOnce(fd,Proud::RmiContext::ReliableSend, request); }
case 13550: { LocalBulkSkillRequest request{}; m >> request;  return g_bulkUltimateStub.CG_RequestSkinSkillLevelUpAtOnce(fd,Proud::RmiContext::ReliableSend, request); }
case 10688: {  return g_finalBossShopStub.CG_RequestFinalBossShopInfo(fd,Proud::RmiContext::ReliableSend); }
case 10689: { int season{}; m >> season; int product{}; m >> product; uint8 count{}; m >> count;  return g_finalBossShopStub.CG_RequestFinalBossShopBuy(fd,Proud::RmiContext::ReliableSend, season, product, count); }
case 10364: { LocalStageStartRequest request{}; m >> request;  return g_descentStub.CG_Request_DescentBoss_EventStage_Start(fd,Proud::RmiContext::ReliableSend, request); }
case 10365: { LocalStageClearRequest request{}; m >> request;  return g_descentStub.CG_Request_DescentBoss_EventStage_Clear(fd,Proud::RmiContext::ReliableSend, request); }
case 10366: {  return g_descentStub.CG_Request_DescentBoss_EventStage_Continue(fd,Proud::RmiContext::ReliableSend); }
case 10367: { int eventSEQ{}; m >> eventSEQ; int step{}; m >> step;  return g_descentStub.CG_Request_DescentBoss_Event_Point_Reward(fd,Proud::RmiContext::ReliableSend, eventSEQ, step); }
case 11112: { int32_t skipID{}; m >> skipID;  return g_chapterSkipStub.CG_RequestItemUseChapterSkip(fd,Proud::RmiContext::ReliableSend, skipID); }
case 12582: {  return g_towerShopStub.CG_RequestYggdrasilTowerShopInfo(fd,Proud::RmiContext::ReliableSend); }
case 12583: { int product{}; m >> product; uint8 count{}; m >> count;  return g_towerShopStub.CG_RequestYggdrasilTowerShopBuy(fd,Proud::RmiContext::ReliableSend, product, count); }
default: std::printf("Unhandled RMI %u\n",id); return false; }}

void PhoneLogRoster() {
 std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
 const auto heroes=GcLocal::OwnedHeroes();int tg=0;
 for(int hero:heroes)if(hero>=2995001&&hero<=2995121)++tg;
 __android_log_print(ANDROID_LOG_INFO,"GCPhoneRoster","Login owned heroes=%zu skins=%zu TG=%d Centipede=%d",heroes.size(),GcLocal::OwnedSkins().size(),tg,int(heroes.count(2995001)));
 for(int skin:GcLocal::OwnedSkins()){const auto* row=GcLocal::FindSkin(skin);if(row&&row->hero>=2995001&&row->hero<=2995121)__android_log_print(ANDROID_LOG_INFO,"GCPhoneRoster","Owned TG hero=%d skin=%d",row->hero,skin);}
}
