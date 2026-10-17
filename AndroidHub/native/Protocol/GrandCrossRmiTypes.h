#pragma once

#include <cstdint>
#include <string>
#include <stdexcept>
#include <vector>
#include "ProudNetServer.h"
#include "LocalGachaCatalog.h"
#include "LocalTestAccount.h"
#include "LocalMaterialCatalog.h"
#include "LocalStoryCatalog.h"
#include "LocalStoryProgress.h"
#include "LocalBattleCatalog.h"
#include "LocalFinalBossCatalog.h"
#include "LocalDescentCatalog.h"
#include "LocalBattleProgress.h"
#include "LocalDescentState.h"
#include "LocalCoinCatalog.h"
#include "LocalExtraInventory.h"
#include "LocalDevelopmentState.h"
#include "LocalEquipmentState.h"
#include "LocalTeams.h"
#include "LocalQuestState.h"
#include "LocalChapterSkipCatalog.h"
#include "LocalStoryInteractions.h"
#include "LocalProgressionState.h"
#include "LocalFoodState.h"
#include "LocalTownArtifactState.h"
#include "LocalRelicUpgradeState.h"
#include "LocalFinalBossShop.h"
#include "LocalTowerShop.h"

// PIDL has no built-in 64-bit scalar token in this SDK version; exposing this
// alias lets generated declarations retain the client's Int64 width.
using int64 = int64_t;
using uint8 = uint8_t;
using int16 = int16_t;
struct LocalIntListRequest {std::vector<int> ids;};

// Field order follows the public client type field order recovered from the
// matching 2.113.1 metadata. These types are used only by local RMI handlers.
struct NetmarbleSDKInfo {
    Proud::String sdkJson;
    Proud::String storeType;
    Proud::String countryCode;
    Proud::String joinedCountryCode;
    Proud::String languageCode;
    Proud::String platformADID;
    Proud::String UDID;
    Proud::String OS;
    Proud::String timeZone;
    Proud::String sdkADID;
};

struct VersionInfo {
    int32_t clientVersion = 0;
    int32_t cdnVersion = 0;
};

struct NetmarbleAccountInfo {
    Proud::String netmarblePlayerID;
    int64_t usn = 0;
    uint8_t banStatus = 0;
    int16_t banReason = 0;
    int16_t banCode = 0;
    int32_t banLimitSec = 0;
    Proud::String nickName;
    bool languageChangeAble = false;
    bool needMobileConnect = false;
    int32_t recommendHeroID = 0;
    int32_t recommendSkinID = 0;
    uint8_t cndGambleReceived = 0;
};

// The 2.113.1 client login document contains hundreds of fields.  Most are
// collections or optional feature state, but the wire contract is positional:
// omitting even an empty field shifts every value that follows it.  These two
// lightweight values deliberately expose only the local account fields we
// seed while their serializers below emit the complete schema (empty/zero for
// systems which have not yet been entered).
struct LoginUserResultInfo {
    int64_t usn = 73310001;
    int32_t sessionKey = 7331;
    Proud::String name = _PNT("Cloud");
};

struct LoginServiceInfo { };
struct LocalReconnectResult { int32_t sessionKey=0; };
struct LobbyInfo { };
struct LocalStageInfo { };
struct LocalTeamChange { uint8_t index = 1; GcLocal::TeamState team; };
struct LocalTeamInfo { uint8_t index=1; };
struct LocalArtifactTeam { GcLocal::ArtifactTeamState team; };
struct LocalArtifactTeamList { std::vector<LocalArtifactTeam> teams; };
struct LocalStageStartRequest { int32_t stage = 0; uint8_t index = 0; int32_t teamIndex=0; };
struct LocalStageStartResult { int32_t stage = 0; uint8_t index = 0; int mode = 0; };
struct LocalCancelResult {int32_t request=0,error=100;};
struct LocalPayback {};
struct LocalNoItem {};
struct LocalDestroyDiscovery {};
struct LocalCoinShopInfo {};
struct LocalCoinBuyRequest { int32_t shop=0; uint8_t count=0;std::vector<std::pair<int,int>> payments; };
struct LocalCoinBuyResult { int32_t shop=0,count=0; bool event=false,newHero=false;std::vector<std::pair<int,int>> payments; };
struct LocalFortCoinOpenRequest { int32_t area=0; };
struct LocalTranscendRequest { int32_t hero=0; uint8_t rank=0; std::vector<std::pair<int,int>> items; };
struct LocalSystemsResult {int32_t serial=0,kind=0,skin=0,other=0;std::vector<std::pair<int,int>> items;std::vector<int> serials;std::vector<std::pair<int,uint8_t>> successes;};
struct LocalMailResult {int kind=0;bool claimed=false;};
struct LocalBoxRequest {int32_t item=0,count=0;Proud::String answer;std::vector<int> choices;};
struct LocalBoxResult {int32_t item=0;std::vector<std::pair<int,int>> drops;};
struct LocalLegendResult { int32_t previous=0,skin=0; std::vector<std::pair<int32_t,int32_t>> costs; };
struct LocalOneStepResult { int32_t previous=0,skin=0,item=0; };
struct LocalGrowthResult { int32_t skin=0,kind=0; std::vector<int> items; };
struct LocalStageClearRequest { int32_t stage = 0; bool win = false; };
struct LocalNativeReward { int type=0,id=0,count=0,serial=0; };
struct LocalStageClearResult { int32_t stage = 0; bool win = false; bool first=false; int gold=0;std::vector<std::pair<int,int>> experience;LocalNativeReward nativeFirst;std::vector<LocalNativeReward> nativeDrops;std::pair<int,int> firstReward={0,0};std::vector<std::pair<int,int>> drops; bool omitClearReward=false; };
struct LocalLevelUpRequest { int32_t skin = 0; std::vector<std::pair<int32_t,int32_t>> materials; };
struct LocalLevelUpResult { int32_t skin = 0; std::vector<std::pair<int32_t,int32_t>> materials; };
struct LocalQuestStartResult { int32_t quest = 0; };
struct LocalQuestProgressResult { int32_t quest = 0;std::vector<std::pair<int,int>> drops; };
struct LocalQuestClearResult { int32_t quest = 0, next = 0;std::vector<LocalNativeReward> rewards;std::vector<std::pair<int,int>> consumed; };
struct LocalRelicUpgradeResult {int costume=0;std::vector<std::pair<int,int>> costs;};
struct LocalFinalBossInfo {};
struct LocalFinalBossClearExtra {};
struct LocalFinalBossRank {};
struct LocalTownInfoResult {int town=0;};
struct LocalTownDonationResult {int town=0,count=0;};
struct LocalChestResult {int npc=0,item=0;};
struct LocalUnionRequest {int id=0;std::vector<std::pair<int,int>> items;};
struct LocalUnionResult {int id=0;std::vector<std::pair<int,int>> items;};
struct LocalFoodResult {int item=0,recipe=0;bool toggle=false;};
struct LocalCookingRequest {int32_t npc=0,count=0;std::vector<int> materials;bool immediately=false;};
struct LocalCookingResult {int recipe=0,count=0,npc=0;bool immediately=false;std::vector<std::pair<int,int>> costs,drops;};
struct LocalTownBuyRequest {std::vector<std::pair<int,uint8_t>> products;};
struct LocalTownShopResult {int town=0;};
struct LocalTownBuyResult {std::vector<std::pair<int,int>> costs,drops;std::vector<int> products;};
struct LocalEvolutionResult { int32_t previous = 0, skin = 0; bool first = false; std::vector<std::pair<int32_t,int32_t>> costs; };
struct LocalBreakResult { int32_t skin = 0; std::vector<std::pair<int32_t,int32_t>> costs; };
struct LocalSkillResult { int32_t skin = 0; std::vector<std::pair<int32_t,int32_t>> costs; };
struct LocalAwakenResult { int32_t skin = 0; std::vector<std::pair<int32_t,int32_t>> costs; };
struct LocalPassiveResult { int32_t skin = 0; };
struct MissionResult { bool sync=false; };
struct LocalMissionClearRequest { std::vector<std::pair<int,uint8_t>> missions; };
struct LocalMissionClearResult {std::vector<int> chains;std::vector<LocalNativeReward> rewards;};
struct LocalAchievementResult {int order=0,item=0,count=0;};
struct LocalChapterSkipResult {int cost=0,topStage=0;std::vector<int> quests,stages;std::vector<LocalNativeReward> rewards;};
struct LocalChapterResult {std::vector<LocalNativeReward> rewards;};
struct LocalGuideResult {bool clear=false;std::vector<LocalNativeReward> rewards;std::vector<std::pair<int,int>> upgrades;};
struct EmptyItemResults { };
struct BillingVerifyResultInfo { };
struct GcString { Proud::String value; };
struct IntList { std::vector<int32_t> values; };
struct AttendanceResult { };
struct EventPacketInfo { };
struct LocalDescentInfo {int stage=0;};
struct GambleShopInfo { int32_t group = 0; };
struct GambleChecksumList { std::vector<int32_t> entries; };
struct GambleTimeSwitchLobbyInfo { };
struct GambleShopBuyRequest {
    int32_t group = 0; uint8_t amount = 0, price = 0, ad = 0, tickets = 0;
};
struct GambleShopBuyResult {
    int32_t group = 0, event = 0; uint8_t amount = 0;
    std::vector<int32_t> skins, newHeroes, coins;
};

namespace Proud {
inline void WriteDevelopmentSkin(CMessage&,int);
inline CMessage& operator<<(CMessage& msg, const EventPacketInfo&);
inline CMessage& operator<<(CMessage& msg,const LocalDescentInfo&);
inline CMessage& operator<<(CMessage& msg, const LocalStageInfo&);
inline void WriteGcString(CMessage& msg,const Proud::String& value) { msg << value; }
inline void ReadGcString(CMessage& msg,Proud::String& value) { msg >> value; }
inline CMessage& operator<<(CMessage& msg, const VersionInfo& value) {
    msg << value.clientVersion << value.cdnVersion;
    return msg;
}

inline CMessage& operator>>(CMessage& msg, VersionInfo& value) {
    msg >> value.clientVersion >> value.cdnVersion;
    return msg;
}

inline void AppendTextOut(String& out, VersionInfo&) {
    out += L"<VersionInfo>";
}

inline CMessage& operator<<(CMessage& msg, const NetmarbleSDKInfo& value) {
    msg << value.sdkJson << value.storeType << value.countryCode
        << value.joinedCountryCode << value.languageCode << value.platformADID
        << value.UDID << value.OS << value.timeZone << value.sdkADID;
    return msg;
}

inline CMessage& operator>>(CMessage& msg, NetmarbleSDKInfo& value) {
    msg >> value.sdkJson >> value.storeType >> value.countryCode
        >> value.joinedCountryCode >> value.languageCode >> value.platformADID
        >> value.UDID >> value.OS >> value.timeZone >> value.sdkADID;
    return msg;
}

inline void AppendTextOut(String& out, NetmarbleSDKInfo&) {
    out += L"<NetmarbleSDKInfo>";
}

inline CMessage& operator<<(CMessage& msg, const NetmarbleAccountInfo& value) {
    WriteGcString(msg, value.netmarblePlayerID);
    msg << value.usn << value.banStatus
        << value.banReason << value.banCode << value.banLimitSec
        ;
    WriteGcString(msg, value.nickName);
    msg << value.languageChangeAble << value.needMobileConnect
        << value.recommendHeroID << value.recommendSkinID
        << value.cndGambleReceived;
    return msg;
}

inline CMessage& operator>>(CMessage& msg, NetmarbleAccountInfo& value) {
    msg >> value.netmarblePlayerID >> value.usn >> value.banStatus
        >> value.banReason >> value.banCode >> value.banLimitSec
        >> value.nickName >> value.languageChangeAble >> value.needMobileConnect
        >> value.recommendHeroID >> value.recommendSkinID
        >> value.cndGambleReceived;
    return msg;
}

inline void AppendTextOut(String& out, NetmarbleAccountInfo&) {
    out += L"<NetmarbleAccountInfo>";
}

inline void WriteZeroSchema(CMessage& msg, const char* schema) {
    for (const char* token = schema; *token; ++token) {
        switch (*token) {
        case 'c': msg.WriteScalar(int32_t(0)); break;
        case 'i': msg << int32_t(0); break;
        case 'l': msg << int64_t(0); break;
        case 'h': msg << int16_t(0); break;
        case 'b': msg << uint8_t(0); break;
        case 'o': msg << false; break;
        case 's': WriteGcString(msg, Proud::String()); break;
        case 'f': msg << float(0); break;
        case 'q': msg << double(0); break;
        case 'd':
            // CommonPacket.Marshaler writes DateTime.Ticks then DateTime.Kind.
            msg << int64_t(0) << int32_t(0);
            break;
        }
    }
}

inline void ReadZeroSchema(CMessage& msg, const char* schema) {
    for (const char* token = schema; *token; ++token) {
        int32_t i = 0; int64_t l = 0; int16_t h = 0; uint8_t b = 0;
        bool o = false; float f = 0; double q = 0; Proud::String s;
        switch (*token) {
        case 'c': msg.ReadScalar(i); break;
        case 'i': msg >> i; break;
        case 'l': msg >> l; break;
        case 'h': msg >> h; break;
        case 'b': msg >> b; break;
        case 'o': msg >> o; break;
        case 's': ReadGcString(msg, s); break;
        case 'f': msg >> f; break;
        case 'q': msg >> q; break;
        case 'd': msg >> l >> i; break;
        }
    }
}

inline CMessage& operator<<(CMessage& msg,const LocalCancelResult& v) {msg << v.request;WriteGcString(msg,Proud::String(L"Local server"));msg << uint32_t(v.error) << uint32_t(v.error==101?1021:1012) << true;return msg;}
inline CMessage& operator>>(CMessage& msg,LocalCancelResult&) {return msg;}
inline void AppendTextOut(String& out,LocalCancelResult&) {out+=L"<RequestRejected>";}
inline void WriteWeapon(CMessage& msg,int serial) {
    const auto& w=GcLocal::Equipments().at(serial);msg << int32_t(w.serial) << int32_t(w.base) << uint8_t(w.upgrade) << uint8_t(w.evolution);
    msg.WriteScalar(int32_t(w.options.size()));for(auto o:w.options)msg << int32_t(o.first) << int32_t(o.second);
    msg << int32_t(0) << int32_t(0) << int64_t(0) << int32_t(0) << bool(w.skin!=0) << int32_t(w.value) << w.locked << uint8_t(w.carve);
}
inline void WriteWeaponSlots(CMessage& msg,int skin) {std::vector<int> slots(6,0);bool any=false;for(auto p:GcLocal::Equipments()){const auto& w=p.second;if(w.skin==skin&&w.slot>=0&&w.slot<6){slots[w.slot]=w.serial;any=true;}}msg.WriteScalar(int32_t(any?6:0));if(any)for(int id:slots)msg << int32_t(id);}
inline void WriteCommonResult(CMessage& msg,int id,int count=0,int owner=0) {msg << uint8_t(GcLocal::FindMaterialType(id)) << int32_t(id) << int32_t(GcLocal::SeededMaterialCount(id)) << int32_t(count) << uint8_t(0) << int32_t(owner);WriteZeroSchema(msg,"iiiioi");}
inline void WriteCommonResults(CMessage& msg,const std::vector<std::pair<int,int>>& items,bool reward=false){msg.WriteScalar(int32_t(items.size()));for(auto p:items)WriteCommonResult(msg,p.first,reward?p.second:0);}
inline const char* LoginUserZeroSchema() {
    return
        "iiiccccciiclicccccccicbiociiccclsibilicccccccicbiociicccbcdccciiiiiiiiicccccbciiiiiiiiiiilllbbbi"
        "iciilicccccccicbiociiccciiccilliiliiliilicchhciiccciicbscicciiosibbbbbbcobbbboiobboibbbiicibbbbb"
        "bbibbbbbbbbbbiiiiiiiiicccccbciiiiiiiiiiilllbbbiiciilicccccccicbiociiccciiccilliiliiliilicchhciic"
        "cciicbscicciiocccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccb"
        "bcioiiccbbbbbbbbbccbibiiiiioiiocicclbiicibcccccciilbsiiiddiiiihbdohhiibisiicbcccocciboboicccccci"
        "illlllbisilsssoiiiiibbhhshhhcbhbibsiscooccibodcccbcibcicchhhocobiiblbccccciiiociiiiiccbcibioiiio"
        "oiiccccccccicbiiiicciciiiiiiiciiioccc";
}

inline void WriteTownInfo(CMessage& msg,int town){int flags=0;for(auto r:GcLocal::TownChests)if(r.town==town&&GcLocal::OpenChests().count(r.npc))flags|=1<<r.index;msg<<int32_t(town)<<int32_t(GcLocal::TownExperience(town))<<int32_t(0)<<int32_t(flags)<<int32_t(0)<<int32_t(0)<<int32_t(0);msg.WriteScalar(int32_t(0));}
inline CMessage& operator<<(CMessage& msg, const LoginUserResultInfo& value) {
    std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);
    msg << value.usn << value.sessionKey;
    WriteGcString(msg, value.name);
    // Flattened from CommonPacket.Marshaler.Read(LoginUserResultInfo) and the
    // matching 2.113.1 metadata. Lists use ProudNet scalar counts;
    // referenced records are recursively represented by their zero schema.
    // Tutorial list is field 0x108, token 461 after the account header.
    // Complete every tutorial type; the main tutorial step is already finished.
    const char* schema = LoginUserZeroSchema();
    for (int index = 0; schema[index]; ++index) {
        if(index==1){msg<<int32_t(GcLocal::AccountExperience());}
        else if(index==427){msg.WriteScalar(int32_t(GcLocal::RecipeExperience().size()));for(auto p:GcLocal::RecipeExperience())msg<<int32_t(p.first)<<int32_t(p.second)<<true;}
        else if(index==467){const auto& food=GcLocal::Food();msg<<int32_t(food.item)<<uint8_t(food.used)<<food.automatic;index+=2;}
        else if(index==428){std::set<int> towns;for(auto r:GcLocal::TownRules)towns.insert(r.id);for(auto r:GcLocal::TownChests)towns.insert(r.town);msg.WriteScalar(int32_t(towns.size()));for(int town:towns)WriteTownInfo(msg,town);}
        else if(index==585){msg.WriteScalar(int32_t(GcLocal::ArtifactUnionExperience().size()));for(auto p:GcLocal::ArtifactUnionExperience())msg<<int32_t(p.first)<<int32_t(p.second);}
        else if(index==432){msg<<int32_t(GcLocal::Progression().achievementOrder);}
        else if(index==481){msg<<int64_t(GcLocal::Progression().chapterFlags);WriteZeroSchema(msg,"llll");index+=4;}
        else if(index==542){msg<<GcLocal::Progression().guideRewarded;}
        else if(index==543){msg<<uint8_t(GcLocal::Progression().guideStep);}
        else if (index == 4) { // userHeroList: Meliodas, confirmed against DB_skin_base.
            const auto heroes = GcLocal::OwnedHeroes();
            msg.WriteScalar(int32_t(heroes.size())); for (int hero : heroes) msg << int32_t(hero);
        } else if (index == 5) { // userSkinList
            msg.WriteScalar(int32_t(GcLocal::OwnedSkins().size()));
            for (int id : GcLocal::OwnedSkins()) {
                const auto* skin = GcLocal::FindSkin(id);
                const auto& state = GcLocal::DevelopmentStates()[id];
                msg << int32_t(skin->hero) << int32_t(id) << int32_t(state.exp) << int32_t(0)
                    << uint8_t(0) << GcLocal::AwakeningFlags(state.awaken) << uint8_t(state.skill) << uint8_t(state.limitBreak) << uint8_t(GcLocal::UnlockedPassives().count(id) ? 1 : 0);
                WriteWeaponSlots(msg,id);msg.WriteScalar(int32_t(0));
                const auto& equipment = GcLocal::CosmeticEquipments()[skin->hero];
                msg << int32_t(equipment.outfit) << int32_t(equipment.weapon) << int32_t(equipment.head);
                WriteZeroSchema(msg, "obbcbhh"); msg << uint8_t(state.transcend);
                msg << int32_t(0) << uint8_t(0) << uint8_t(state.exceed) << uint8_t(0) << uint8_t(state.exceedSupreme) << uint8_t(state.exceedSelect);
            }
        } else if (index == 6) {
            msg.WriteScalar(int32_t(GcLocal::Equipments().size()));for(auto p:GcLocal::Equipments())WriteWeapon(msg,p.first);
        } else if (index == 7) { // userCommonItemList: local test wallet.
            std::map<int,int> inventory;
            for (int id : GcLocal::MaterialIds)
                if(GcLocal::SeededMaterialCount(id)>0)inventory[id]=GcLocal::SeededMaterialCount(id);
            if(GcLocal::CustomMode())for(const auto& row:GcLocal::ExtraItems())inventory[row.first]=(std::max)(GcLocal::TestMaterialCount,row.second);
            msg.WriteScalar(int32_t(inventory.size()));
            for(const auto& row:inventory)msg<<int32_t(row.first)<<int32_t(row.second);
        } else if (index == 583) {
            msg.WriteScalar(int32_t(GcLocal::Artifacts().size()));
            for(int id:GcLocal::Artifacts())msg<<int32_t(id);
        } else if (index == 584) {
            msg.WriteScalar(int32_t(GcLocal::ArtifactTeams().size()));
            for(const auto& p:GcLocal::ArtifactTeams()) {
                msg<<p.second.index<<int32_t(p.second.unionId);msg.WriteScalar(int32_t(p.second.cards.size()));
                for(int id:p.second.cards)msg<<int32_t(id);
            }
        } else if (index == 8) {
            // Absolute capacities, not purchase counts. The seeded test materials
            // must leave room for battle drops and development rewards.
            msg << int32_t(5000) << int32_t(5000); index += 1;
        } else if (index == 10) {
            msg.WriteScalar(int32_t(GcLocal::Teams().size()));
            for (const auto& entry : GcLocal::Teams()) {
                msg << uint8_t(entry.first); WriteGcString(msg,Proud::String(L"Local team"));
                msg.WriteScalar(int32_t(entry.second.slots.size()));
                for (const auto& slot : entry.second.slots)
                    msg << slot.slot << int32_t(slot.hero) << slot.group << int32_t(slot.skin) << int32_t(slot.fateHero) << slot.fateGroup << int32_t(slot.fateSkin);
                msg << int32_t(entry.second.buff);
            }
        } else if (index == 62) {
            msg << LocalStageInfo{}; index += 96;
        } else if (index == 431) {
            msg.WriteScalar(int32_t(GcLocal::Quests().size()));
            for (const auto& q : GcLocal::Quests()) {
                msg << int32_t(q.first) << q.second.status;
                msg.WriteScalar(int32_t(q.second.progress.size()));
                for (int value : q.second.progress) msg << int32_t(value);
                msg << q.second.interaction;
            }
        } else if (index == 61) { // userAPInfoList
            msg.WriteScalar(int32_t(3));
            for (uint8_t type = 1; type <= 3; ++type)
                msg << type << int32_t(GcLocal::CustomMode()?100:GcLocal::SeededMaterialCount(500020)) << int64_t(639269064000000000LL) << int32_t(1) << int32_t(0);
        } else if (index == 305) { // dailyReset.eventPacketInfo
            msg << EventPacketInfo{};
            index += 77;
        } else if (index == 589) { // lobbyVisualType: Britannia tavern.
            msg << uint8_t(1);
        } else if (index == 476) {
            msg.WriteScalar(int32_t(GcLocal::RelicUpgrades().size()));for(auto p:GcLocal::RelicUpgrades())msg<<int32_t(p.first.first)<<int32_t(p.first.second)<<uint8_t(p.second);
        } else if (index >= 473 && index <= 475) { // Native outfit / weapon / head ownership lists.
            const int type = index - 472;
            int count = 0; for (const auto& c : GcLocal::Cosmetics) if (c.type == type && GcLocal::OwnCosmetic(c.id)) ++count;
            msg.WriteScalar(int32_t(count));
            for (const auto& c : GcLocal::Cosmetics) if (c.type == type && GcLocal::OwnCosmetic(c.id))
                msg << int32_t(c.id) << int32_t(0) << uint8_t(0) << uint8_t(c.heroGroup)
                    << int32_t(c.group) << int64_t(0) << int32_t(0); // DateTime.MinValue: permanent.
        } else if (index == 479) { // mainSkinID
            msg << int32_t(GcLocal::MainSkin());
        } else if (index == 168) { // dailyReset.attendanceInfo.isRewardedToday
            // Local testing begins after today's attendance has been claimed.
            // No live-service attendance calendar is installed for this account.
            msg << true;
        } else if (index == 461) {
            std::printf("[Profile] tutorial payload offset=%d\n", msg.GetLength());
            msg.WriteScalar(int32_t(63));
            for (uint8_t type = 0; type <= 62; ++type)
                msg << type << uint8_t(3) << int32_t(10000);
        } else {
            char field[] = { schema[index], 0 };
            WriteZeroSchema(msg, field);
        }
    }
    return msg;
}

inline CMessage& operator>>(CMessage& msg, LoginUserResultInfo& value) {
    msg >> value.usn >> value.sessionKey >> value.name;
    ReadZeroSchema(msg, LoginUserZeroSchema());
    return msg;
}
inline void AppendTextOut(String& out, LoginUserResultInfo&) { out += L"<LoginUserResultInfo>"; }

inline CMessage& operator<<(CMessage& msg, const LoginServiceInfo&) {
    static const char schema[] = "disiddddboisi";
    WriteZeroSchema(msg, schema);
    return msg;
}

inline CMessage& operator>>(CMessage& msg, LoginServiceInfo&) {
    ReadZeroSchema(msg, "disiddddboisi");
    return msg;
}
inline void AppendTextOut(String& out, LoginServiceInfo&) { out += L"<LoginServiceInfo>"; }
inline CMessage& operator<<(CMessage& msg,const LocalReconnectResult& v) {
    // Exact UserDailyReset layout from CommonPacket.Marshaler.Read at 0x36b7c44.
    static const char schema[]="bbbbbbcobbbboiobboibbbiicibbbbbbbibbbbbbbbbbiiiiiiiiicccccbciiiiiiiiiiilllbbbiiciilicccccccicbiociiccciiccilliiliiliilicchhciiccciicbscicciiocccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccbbcioiiccbbbbbbbbbccbibiiiiioiiocicclbiicibc";
    for(size_t i=0;i<44;++i){char part[]={schema[i],0};WriteZeroSchema(msg,part);}
    msg<<LocalStageInfo{};WriteZeroSchema(msg,schema+141);msg<<int32_t(v.sessionKey)<<LoginServiceInfo{};return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalReconnectResult&){return msg;}
inline void AppendTextOut(String& out,LocalReconnectResult&){out+=L"<Reconnect>";}
inline CMessage& operator<<(CMessage& msg, const GcString& s) { WriteGcString(msg, s.value); return msg; }
inline CMessage& operator>>(CMessage& msg, GcString& s) { ReadGcString(msg, s.value); return msg; }
inline void AppendTextOut(String& out, GcString&) { out += L"<GcString>"; }
inline CMessage& operator<<(CMessage& msg, const EmptyItemResults&) { msg.WriteScalar(int32_t(0)); return msg; }
inline CMessage& operator>>(CMessage& msg, EmptyItemResults&) { int32_t n; msg.ReadScalar(n); return msg; }
inline void AppendTextOut(String& out, EmptyItemResults&) { out += L"<EmptyItemResults>"; }
inline CMessage& operator<<(CMessage& msg, const IntList& list) {
    msg.WriteScalar(int32_t(list.values.size()));
    for (auto i : list.values) msg << i;
    return msg;
}
inline CMessage& operator>>(CMessage& msg, IntList& list) {
    int32_t count = 0;
    if (!msg.ReadScalar(count) || count < 0 || count > 10000) throw std::runtime_error("Invalid list count");
    list.values.resize(count);
    for (auto& i : list.values) msg >> i;
    return msg;
}
inline void AppendTextOut(String& out, IntList&) { out += L"<IntList>"; }
inline CMessage& operator<<(CMessage& msg, const MissionResult& v) {
 if(v.sync||GcLocal::MissionClientReady()){
  GcLocal::RefreshMissionSnapshots();msg.WriteScalar(int32_t(GcLocal::Missions().size()));
  for(auto p:GcLocal::Missions())msg<<int32_t(p.first)<<uint8_t(p.second.claimed)<<int32_t(p.second.progress);
 }else msg.WriteScalar(int32_t(0));
 WriteZeroSchema(msg,"cccccc");return msg;
}
inline CMessage& operator>>(CMessage& msg, MissionResult&) { ReadZeroSchema(msg, "ccccccc"); return msg; }
inline void AppendTextOut(String& out, MissionResult&) { out += L"<MissionResult>"; }
inline CMessage& operator<<(CMessage& msg, const BillingVerifyResultInfo&) { WriteZeroSchema(msg, "hilsooos"); return msg; }
inline CMessage& operator>>(CMessage& msg, BillingVerifyResultInfo&) { ReadZeroSchema(msg, "hilsooos"); return msg; }
inline void AppendTextOut(String& out, BillingVerifyResultInfo&) { out += L"<BillingVerifyResultInfo>"; }
inline CMessage& operator<<(CMessage& msg, const AttendanceResult&) { WriteZeroSchema(msg, "obbbboiobboibbbiiccccccccccc"); return msg; }
inline CMessage& operator>>(CMessage& msg, AttendanceResult&) { ReadZeroSchema(msg, "obbbboiobboibbbiiccccccccccc"); return msg; }
inline void AppendTextOut(String& out, AttendanceResult&) { out += L"<AttendanceResult>"; }
inline CMessage& operator<<(CMessage& msg, const EventPacketInfo&) {
    const int count = int(sizeof(GcLocal::Banners) / sizeof(GcLocal::Banners[0]));
    for (int i = 0; i < 78; ++i) {
        if (i == 0) {
            msg.WriteScalar(count+1);
            for (const auto& banner : GcLocal::Banners) {
                msg << int32_t(100000 + banner.id) << int32_t(5000);
                const std::wstring json = L"{\"EVENT_SUB_INDEX\":[" + std::to_wstring(banner.id) + L"]}";
                WriteGcString(msg, Proud::String(json.c_str()));
                for (int s = 0; s < 4; ++s) WriteGcString(msg, Proud::String());
                msg << uint8_t(1); WriteGcString(msg, Proud::String());
                msg << uint8_t(0); WriteGcString(msg, Proud::String());
                msg << uint8_t(0) << int32_t(0) << int32_t(2147483647);
                msg << int64_t(3155378975999999999LL) << int32_t(1);
                msg << int64_t(638712864000000000LL) << int32_t(1);
                msg << uint8_t(0) << int32_t(0) << int32_t(2147483647) << int32_t(0) << false << uint8_t(0);
            }
            msg<<int32_t(GcLocal::DescentEventSequence)<<int32_t(40000);
            WriteGcString(msg,Proud::String(L"{\"EVENT_SUB_INDEX\":[1000001],\"EVENT_REGION\":[1000001]}"));
            WriteGcString(msg,Proud::String(L"Event Boss: Crocshell"));
            for(int k=0;k<3;++k)WriteGcString(msg,Proud::String());
            msg<<uint8_t(2);WriteGcString(msg,Proud::String(L"Challenge four difficulties and collect boss rewards."));
            msg<<uint8_t(1);WriteGcString(msg,Proud::String(L"Battle"));
            msg<<uint8_t(1)<<int32_t(0)<<int32_t(2147483647)<<int64_t(3155378975999999999LL)<<int32_t(1)<<int64_t(638712864000000000LL)<<int32_t(1)<<uint8_t(0)<<int32_t(0)<<int32_t(2147483647)<<int32_t(0)<<false<<uint8_t(0);
        } else if(i==36){msg.WriteScalar(int32_t(1));msg<<LocalDescentInfo{};
        } else if (i == 5) {
            msg.WriteScalar(count);
            for (const auto& banner : GcLocal::Banners)
                msg << int32_t(100000 + banner.id) << int32_t(banner.id) << uint8_t(0);
        } else msg.WriteScalar(int32_t(0));
    }
    return msg;
}
inline CMessage& operator>>(CMessage& msg, EventPacketInfo&) {
    for (int i = 0; i < 78; ++i) { int32_t count = 0; msg.ReadScalar(count); }
    return msg;
}
inline void AppendTextOut(String& out, EventPacketInfo&) { out += L"<EventPacketInfo>"; }
inline CMessage& operator<<(CMessage& msg, const GambleShopInfo& info) {
    msg << info.group << int32_t(0) << int32_t(2147483647); return msg;
}
inline CMessage& operator>>(CMessage& msg, GambleShopInfo& info) { msg >> info.group; ReadZeroSchema(msg, "ii"); return msg; }
inline void AppendTextOut(String& out, GambleShopInfo&) { out += L"<GambleShopInfo>"; }
inline CMessage& operator<<(CMessage& msg, const GambleTimeSwitchLobbyInfo&) { WriteZeroSchema(msg, "ii"); return msg; }
inline CMessage& operator>>(CMessage& msg, GambleTimeSwitchLobbyInfo&) { ReadZeroSchema(msg, "ii"); return msg; }
inline void AppendTextOut(String& out, GambleTimeSwitchLobbyInfo&) { out += L"<GambleTimeSwitchLobbyInfo>"; }
inline CMessage& operator<<(CMessage& msg, const GambleChecksumList& list) {
    msg.WriteScalar(int32_t(list.entries.size() / 2));
    for (auto i : list.entries) msg << i;
    return msg;
}
inline CMessage& operator>>(CMessage& msg, GambleChecksumList& list) {
    int32_t count = 0;
    if (!msg.ReadScalar(count) || count < 0 || count > 10000) throw std::runtime_error("Invalid gacha checksum count");
    list.entries.resize(count * 2); for (auto& i : list.entries) msg >> i; return msg;
}
inline void AppendTextOut(String& out, GambleChecksumList&) { out += L"<GambleChecksumList>"; }
inline CMessage& operator<<(CMessage& msg, const GambleShopBuyRequest& v) { msg << v.group << v.amount << v.price << v.ad << v.tickets; return msg; }
inline CMessage& operator>>(CMessage& msg, GambleShopBuyRequest& v) { msg >> v.group >> v.amount >> v.price >> v.ad >> v.tickets; return msg; }
inline void AppendTextOut(String& out, GambleShopBuyRequest&) { out += L"<GambleShopBuyRequest>"; }
inline CMessage& operator<<(CMessage& msg, const GambleShopBuyResult& v) {
    // Cost updates include an unchanged wallet and any newly created owners.
    msg.WriteScalar(int32_t(1 + v.newHeroes.size()));
    msg << uint8_t(1) << int32_t(500011) << int32_t(GcLocal::SeededMaterialCount(500011));
    WriteZeroSchema(msg, "ibiiiiioi");
    for (int hero : v.newHeroes) {
        msg << uint8_t(210) << int32_t(hero);
        WriteZeroSchema(msg, "ibiiiiioi");
    }
    msg.WriteScalar(int32_t(v.skins.size()));
    for (size_t index=0;index<v.skins.size();++index) {
        const int id=v.skins[index];const auto* skin=GcLocal::FindSkin(id);
        const int coin=index<v.coins.size()?v.coins[index]:0;
        if(coin)msg << uint8_t(GcLocal::FindMaterialType(coin)) << int32_t(coin) << int32_t(GcLocal::SeededMaterialCount(coin));
        else {msg << uint8_t(211);WriteDevelopmentSkin(msg,id);}
        msg << int32_t(1) << uint8_t(0) << int32_t(id);WriteZeroSchema(msg,"iiiioi");
    }
    WriteZeroSchema(msg, "bibiiiiioi"); // no bonus item
    const char* daily = "bbbbbbcobbbboiobboibbbiicibbbbbbbibbbbbbbbbbiiiiiiiiicccccbciiiiiiiiiiilllbbbiiciilicccccccicbiociiccciiccilliiliiliilicchhciiccciicbscicciiocccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccbbcioiiccbbbbbbbbbccbibiiiiioiiocicclbiicibc";
    for (int i = 0; daily[i]; ++i) {
        if (i == 7) msg << true;
        else if (i == 144) { msg << EventPacketInfo{}; i += 77; }
        else { char field[] = {daily[i], 0}; WriteZeroSchema(msg, field); }
    }
    msg << v.group << v.amount;
    WriteZeroSchema(msg, "ccccccc");
    msg << v.event << false;
    msg << v.group << v.event << int32_t(0) << uint8_t(0) << int32_t(0);
    msg << false;
    WriteZeroSchema(msg, "iiiiciiibiihiiiciiiiiiibiiii");
    return msg;
}
inline CMessage& operator>>(CMessage& msg, GambleShopBuyResult&) { return msg; }
inline void AppendTextOut(String& out, GambleShopBuyResult&) { out += L"<GambleShopBuyResult>"; }
inline const char* LobbyZeroSchema() {
    return "cbbbooobboobooooooboooobcciioiocccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccoilbsiiiddiiiihbdohhiibiicohbciiciiccibccccbibciobccccbbcohibbioicooooiiiibihioiiooooiossciiicooccccibbiiioobbiiiooiiioiooiiiooiiiibbiiiooiicciibobbcbbciiccccciciicoiciiccicbbbbbiooiciibiiiibiici";
}
inline void WriteQuestProgressList(CMessage& msg);
inline void WriteFinalBossSeason(CMessage& msg);
inline int LocalDailyResetSeconds(){const auto now=std::time(nullptr);return 86400-int(now%86400);}
inline CMessage& operator<<(CMessage& msg, const LobbyInfo&) {
    const char* schema = LobbyZeroSchema();
    for (int i = 0; schema[i]; ++i) {
        if (i == 31) { msg << EventPacketInfo{}; i += 77; }
        else if(i==136){msg<<int32_t(LocalDailyResetSeconds());}
        else if(i==137){WriteQuestProgressList(msg);}
        else if(i==138){msg<<true;}
        else if(i==142){WriteFinalBossSeason(msg);i+=9;}
        else { char field[] = {schema[i], 0}; WriteZeroSchema(msg, field); }
    }
    return msg;
}
inline CMessage& operator>>(CMessage& msg, LobbyInfo&) { ReadZeroSchema(msg, LobbyZeroSchema()); return msg; }
inline void AppendTextOut(String& out, LobbyInfo&) { out += L"<LobbyInfo>"; }
}


namespace Proud {
inline CMessage& operator<<(CMessage& msg, const LocalStageInfo&) {
    msg << int32_t(GcLocal::MainRouteCursor());
    WriteZeroSchema(msg,"iiiiiiii");
    const auto routes=GcLocal::SideRouteCursors();msg.WriteScalar(int32_t(routes.size()));
    for(auto r:routes){msg<<int32_t(r.first);for(int top:r.second)msg<<int32_t(top);WriteZeroSchema(msg,"iillii");}
    const auto weeklyClears=GcLocal::WeekStageClearFlags();
    msg.WriteScalar(int32_t(weeklyClears.size()));
    for(int64_t flags:weeklyClears)msg<<flags;
    WriteZeroSchema(msg,"ccc");
    msg << uint8_t(3); // Wednesday; all local dungeon time windows stay open.
    WriteZeroSchema(msg,"ciiiiiiiiiii");
    for (int i=0;i<3;++i) msg << int64_t(2147483647);
    for (int i=0;i<3;++i) msg << uint8_t(1);
    WriteZeroSchema(msg,"iiciilicccccccicbiociiccciiccilliiliiliilicchhciiccciicbscicciio"); return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalStageInfo&) {
    ReadZeroSchema(msg, "iiiiiiiiicccccbciiiiiiiiiiilllbbbiiciilicccccccicbiociiccciiccilliiliiliilicchhciiccciicbscicciio"); return msg;
}
inline void AppendTextOut(String& out, LocalStageInfo&) { out += L"<StageInfo>"; }
}


namespace Proud {
inline CMessage& operator>>(CMessage& msg, LocalStageStartRequest& value) {
 msg >> value.stage; ReadZeroSchema(msg,"lib");msg>>value.teamIndex;ReadZeroSchema(msg,"ii");
 int64_t count = 0; msg.ReadScalar(count);
 if (count < 0 || count > 8) throw std::runtime_error("Invalid team stats");
 for (int i=0;i<count;++i) ReadZeroSchema(msg, "iiiiib");
 msg.ReadScalar(count);
 if (count < 0 || count > 16) throw std::runtime_error("Invalid stage NPC list");
 for (int i=0;i<count;++i) ReadZeroSchema(msg, "i");
 msg >> value.index; ReadZeroSchema(msg, "o"); return msg;
}
inline CMessage& operator<<(CMessage& msg, const LocalStageStartRequest&) { return msg; }
inline void AppendTextOut(String& out, LocalStageStartRequest&) { out += L"<StageStartRequest>"; }
inline CMessage& operator<<(CMessage& msg, const LocalStageStartResult& value) {
 const GcLocal::StoryStage* stage = nullptr;
 const int* monsters = nullptr;
 if(value.mode==6){const auto* battle=GcLocal::FindDescent(value.stage);if(battle)monsters=battle->monsters;}else if(value.mode==5){const auto* battle=GcLocal::FindFinalBoss(value.stage);if(battle)monsters=battle->monsters;}else if(value.mode==3){
   const auto* battle=GcLocal::FindCampaignStage(3,value.stage);
   if(battle)monsters=battle->monsters;
 } else if (value.mode) {
   const auto* battle = GcLocal::FindBattleStage(value.mode,value.stage);
   if (battle) monsters = battle->monsters;
 } else {
   for (const auto& row : GcLocal::StoryStages) if (row.id == value.stage) stage = &row;
   if (stage) monsters = stage->monsters;
 }
 if (!monsters) throw std::runtime_error("Unknown battle stage");
 msg << value.stage << int32_t(0) << false;
 int size=value.mode>=5?9:10;int count = 0; for (int i=0;i<size;++i) if (monsters[i]) ++count;
 msg.WriteScalar(count);
 for (int i=0;i<size;++i) if (monsters[i])
   msg << int32_t(monsters[i]) << int32_t(value.mode>=5?i%3:(i >= 6 ? i-6 : 0)) << uint8_t(0) << uint8_t(value.mode>=5?i/3:(i >= 6 ? 1 : 0));
 msg << uint8_t(1) << int32_t(GcLocal::CustomMode()?100:GcLocal::SeededMaterialCount(500020)) << int64_t(639269123000000000LL) << int32_t(1) << int32_t(0);
 msg << MissionResult{} << false;const auto& food=GcLocal::Food();msg<<int32_t(food.item)<<uint8_t(food.used)<<food.automatic;if(GcLocal::AutoFoodConsumed())WriteCommonResult(msg,GcLocal::AutoFoodConsumed(),-1);else WriteZeroSchema(msg,"bibiiiiioi");
 msg << false; WriteGcString(msg,Proud::String()); msg << int64_t(73310001) << uint8_t(0);
 msg.WriteScalar(int32_t(0)); msg << value.index;
 msg.WriteScalar(int32_t(0)); msg.WriteScalar(int32_t(0)); msg << int32_t(0); return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalStageStartResult&) { return msg; }
inline void AppendTextOut(String& out, LocalStageStartResult&) { out += L"<StageStartResult>"; }
inline CMessage& operator<<(CMessage& msg, const LocalPayback&) { WriteZeroSchema(msg,"iii"); return msg; }
inline CMessage& operator>>(CMessage& msg, LocalPayback&) { ReadZeroSchema(msg,"iii"); return msg; }
inline void AppendTextOut(String& out, LocalPayback&) { out += L"<Payback>"; }
inline CMessage& operator<<(CMessage& msg, const LocalNoItem&) { WriteZeroSchema(msg,"bibiiiiioi"); return msg; }
inline CMessage& operator>>(CMessage& msg, LocalNoItem&) { ReadZeroSchema(msg,"bibiiiiioi"); return msg; }
inline void AppendTextOut(String& out, LocalNoItem&) { out += L"<NoItem>"; }
inline CMessage& operator<<(CMessage& msg, const LocalDestroyDiscovery&) { WriteZeroSchema(msg,"iibbodibbodibbodi"); return msg; }
inline CMessage& operator>>(CMessage& msg, LocalDestroyDiscovery&) { ReadZeroSchema(msg,"iibbodibbodibbodi"); return msg; }
inline void AppendTextOut(String& out, LocalDestroyDiscovery&) { out += L"<DestroyDiscovery>"; }
inline CMessage& operator<<(CMessage& msg,const LocalTeamInfo& v) {
    msg<<uint8_t(v.index);WriteGcString(msg,Proud::String(L"Local team"));
    const auto it=GcLocal::Teams().find(v.index);
    if(it==GcLocal::Teams().end()){
        msg.WriteScalar(int32_t(4));for(uint8_t i=0;i<4;++i)msg<<i<<int32_t(0)<<uint8_t(0)<<int32_t(0)<<int32_t(0)<<uint8_t(0)<<int32_t(0);msg<<int32_t(0);
    }else{
        msg.WriteScalar(int32_t(it->second.slots.size()));for(const auto& slot:it->second.slots)msg<<slot.slot<<int32_t(slot.hero)<<slot.group<<int32_t(slot.skin)<<int32_t(slot.fateHero)<<slot.fateGroup<<int32_t(slot.fateSkin);msg<<int32_t(it->second.buff);
    }return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalTeamInfo&){return msg;}
inline void AppendTextOut(String& out,LocalTeamInfo&){out+=L"<TeamInfo>";}
inline CMessage& operator>>(CMessage& msg, LocalTeamChange& value) {
    msg >> value.index;
    int64_t count = 0; msg.ReadScalar(count);
    if (count < 0 || count > 8) throw std::runtime_error("Invalid team slot count");
    for (int i = 0; i < count; ++i) {
        uint8_t slot, group, fateGroup; int32_t hero, skin, fateHero, fateSkin;
        msg >> slot >> hero >> group >> skin >> fateHero >> fateGroup >> fateSkin;
        value.team.slots.push_back({slot,hero,group,skin,fateHero,fateGroup,fateSkin});
    }
    msg >> value.team.bp >> value.team.buff; return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalArtifactTeam& v) {
    msg>>v.team.index>>v.team.unionId;int count=0;msg.ReadScalar(count);
    if(count<0||count>5)throw std::runtime_error("Invalid artifact team size");
    for(int i=0,id;i<count;++i){msg>>id;v.team.cards.push_back(id);}return msg;
}
inline CMessage& operator<<(CMessage& msg,const LocalArtifactTeam& v){msg<<v.team.index<<int32_t(v.team.unionId);msg.WriteScalar(int32_t(v.team.cards.size()));for(int id:v.team.cards)msg<<int32_t(id);return msg;}
inline void AppendTextOut(String& out,LocalArtifactTeam&){out+=L"<ArtifactTeam>";}
inline CMessage& operator>>(CMessage& msg,LocalArtifactTeamList& v){int count=0;msg.ReadScalar(count);if(count<0||count>256)throw std::runtime_error("Invalid artifact team list size");for(int i=0;i<count;++i){LocalArtifactTeam t;msg>>t;v.teams.push_back(t);}return msg;}
inline CMessage& operator<<(CMessage& msg,const LocalArtifactTeamList& v){msg.WriteScalar(int32_t(v.teams.size()));for(const auto& t:v.teams)msg<<t;return msg;}
inline void AppendTextOut(String& out,LocalArtifactTeamList&){out+=L"<ArtifactTeams>";}
inline CMessage& operator<<(CMessage& msg, const LocalTeamChange&) { return msg; }
inline void AppendTextOut(String& out, LocalTeamChange&) { out += L"<TeamChange>"; }
inline CMessage& operator>>(CMessage& msg, LocalStageClearRequest& value) {
    // The remainder is client battle telemetry, which is not used for local
    // rewards. The stage and outcome are the leading fields in this build.
    msg >> value.stage >> value.win; return msg;
}
inline CMessage& operator<<(CMessage& msg, const LocalStageClearRequest&) { return msg; }
inline void AppendTextOut(String& out, LocalStageClearRequest&) { out += L"<StageClearRequest>"; }
inline void WriteNativeReward(CMessage& msg,const LocalNativeReward& r){
        if(r.type<200){WriteCommonResult(msg,r.id,r.count);return;}
        msg<<uint8_t(r.type);
        if(r.type==210)msg<<int32_t(r.id);
        else if(r.type==211)WriteDevelopmentSkin(msg,r.id);
        else if(r.type==212)WriteWeapon(msg,r.serial);
        else if(r.type==216)msg<<int32_t(r.id);
        else if(r.type>=213&&r.type<=215){const auto* c=GcLocal::FindCosmetic(r.id);if(!c)throw std::runtime_error("Missing quest cosmetic");msg<<int32_t(c->id)<<int32_t(0)<<uint8_t(0)<<uint8_t(c->heroGroup)<<int32_t(c->group)<<int64_t(0)<<int32_t(0);}
        else throw std::runtime_error("Unsupported quest reward");
        msg<<int32_t(r.count)<<uint8_t(0)<<int32_t(r.type==211?r.id:0)<<int32_t(r.type>=213&&r.type<=215?r.id:0)<<int32_t(0)<<int32_t(0)<<int32_t(r.type==216?r.id:0)<<false<<int32_t(0);
    }

inline CMessage& operator<<(CMessage& msg, const LocalStageClearResult& value) {
    msg << int32_t(GcLocal::AccountExperience()) << uint8_t(1) << int32_t(GcLocal::CustomMode()?100:GcLocal::SeededMaterialCount(500020)) << int64_t(639269123000000000LL) << int32_t(1) << int32_t(0) << value.win;
    msg.WriteScalar(int32_t(value.experience.size()));
    for(auto p:value.experience)msg<<int32_t(GcLocal::FindSkin(p.first)->hero)<<int32_t(p.first)<<int32_t(GcLocal::DevelopmentStates()[p.first].exp)<<int32_t(p.second)<<int32_t(0)<<false;
    msg.WriteScalar(int32_t(0));
    if(value.gold)WriteCommonResult(msg,500012,value.gold);else msg<<LocalNoItem{};
    msg.WriteScalar(int32_t(value.drops.size()+value.nativeDrops.size()));
    for(auto p:value.drops)WriteCommonResult(msg,p.first,p.second);
    for(auto r:value.nativeDrops)WriteNativeReward(msg,r);
    msg.WriteScalar(int32_t(0));
    if(value.nativeFirst.type)WriteNativeReward(msg,value.nativeFirst);else if(value.firstReward.first)WriteCommonResult(msg,value.firstReward.first,value.firstReward.second);else msg<<LocalNoItem{};
    // clearItemResultInfo: Hub-configured diamonds on wins, including repeats.
    // UserCommonItem reports the replenished test wallet; getItemCount drives
    // the native reward display independently of its unlimited balance.
    const int diamondReward=value.win && !value.omitClearReward ? GcLocal::StageDiamondReward() : 0;
    if (diamondReward) {
        msg << uint8_t(1) << int32_t(500011) << int32_t(GcLocal::SeededMaterialCount(500011)) << int32_t(diamondReward);
        WriteZeroSchema(msg,"biiiiioi");
    } else WriteZeroSchema(msg,"bibiiiiioi");
    WriteZeroSchema(msg,"cbibiiiiioibibiiiiioibibiiiiioicccbibiiiiioi");
    msg << value.first << value.stage << LocalStageInfo{};
    msg.WriteScalar(int32_t(GcLocal::Quests().size()));
    for (const auto& q : GcLocal::Quests()) {
        msg << int32_t(q.first) << q.second.status;
        msg.WriteScalar(int32_t(q.second.progress.size()));
        for (int progress : q.second.progress) msg << int32_t(progress);
        msg << q.second.interaction;
    }
    msg << MissionResult{}; WriteZeroSchema(msg,"ciicbiihccoc"); return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalStageClearResult&) { return msg; }
inline void AppendTextOut(String& out, LocalStageClearResult&) { out += L"<StageClearResult>"; }
inline void WriteDevelopmentSkin(CMessage& msg, int id) {
    const auto* skin = GcLocal::FindSkin(id);
    if (!skin) throw std::runtime_error("Unknown development skin");
    const auto& state = GcLocal::DevelopmentStates()[id];
    msg << int32_t(skin->hero) << int32_t(id) << int32_t(state.exp) << int32_t(0)
        << uint8_t(0) << GcLocal::AwakeningFlags(state.awaken) << uint8_t(state.skill) << uint8_t(state.limitBreak) << uint8_t(GcLocal::UnlockedPassives().count(id) ? 1 : 0);
    WriteWeaponSlots(msg,id);msg.WriteScalar(int32_t(0));
    const auto& equipment = GcLocal::CosmeticEquipments()[skin->hero];
    msg << int32_t(equipment.outfit) << int32_t(equipment.weapon) << int32_t(equipment.head);
    WriteZeroSchema(msg,"obbcbhh"); msg << uint8_t(state.transcend); msg << int32_t(0) << uint8_t(0) << uint8_t(state.exceed) << uint8_t(0) << uint8_t(state.exceedSupreme) << uint8_t(state.exceedSelect);
}
inline CMessage& operator>>(CMessage& msg, LocalLevelUpRequest& value) {
    msg >> value.skin; int64_t count = 0; msg.ReadScalar(count);
    if (count < 1 || count > 100) throw std::runtime_error("Invalid experience material count");
    for (int i = 0; i < count; ++i) {
        int32_t id, amount; msg >> id >> amount;
        if (amount < 1 || amount > GcLocal::TestMaterialCount) throw std::runtime_error("Invalid material amount");
        value.materials.emplace_back(id,amount);
    } return msg;
}
inline CMessage& operator<<(CMessage& msg, const LocalLevelUpRequest&) { return msg; }
inline void AppendTextOut(String& out, LocalLevelUpRequest&) { out += L"<LevelUpRequest>"; }
inline CMessage& operator<<(CMessage& msg, const LocalLevelUpResult& value) {
    WriteDevelopmentSkin(msg,value.skin);
    msg.WriteScalar(int32_t(value.materials.size()));
    for (const auto& item : value.materials) msg << item.first << item.second;
    msg.WriteScalar(int32_t(value.materials.size()));
    for(const auto& item:value.materials) {
        msg<<uint8_t(GcLocal::FindMaterialType(item.first))<<int32_t(item.first)<<int32_t(GcLocal::SeededMaterialCount(item.first));
        WriteZeroSchema(msg,"ibiiiiioi");
    }
    msg.WriteScalar(int32_t(value.materials.size()));
    for (int i = 0; i < value.materials.size(); ++i) msg << int32_t(i) << uint8_t(0);
    msg << MissionResult{}; WriteZeroSchema(msg,"ciiic"); return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalLevelUpResult&) { return msg; }
inline void AppendTextOut(String& out, LocalLevelUpResult&) { out += L"<LevelUpResult>"; }
inline CMessage& operator<<(CMessage& msg, const LocalAwakenResult& value) {
    WriteDevelopmentSkin(msg,value.skin); msg.WriteScalar(int32_t(value.costs.size()));for(auto p:value.costs)WriteCommonResult(msg,p.first,-p.second);msg << MissionResult{};
    WriteZeroSchema(msg,"ciiici"); return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalAwakenResult&) { return msg; }
inline void AppendTextOut(String& out, LocalAwakenResult&) { out += L"<AwakenResult>"; }
inline CMessage& operator<<(CMessage& msg, const LocalPassiveResult& value) { WriteDevelopmentSkin(msg,value.skin); return msg; }
inline CMessage& operator>>(CMessage& msg, LocalPassiveResult&) { return msg; }
inline void AppendTextOut(String& out, LocalPassiveResult&) { out += L"<PassiveResult>"; }
inline CMessage& operator<<(CMessage& msg, const LocalEvolutionResult& v) {
    msg << v.previous; WriteDevelopmentSkin(msg,v.skin); msg << MissionResult{};
    msg.WriteScalar(int32_t(0));msg.WriteScalar(int32_t(v.costs.size()));for(auto p:v.costs)WriteCommonResult(msg,p.first,-p.second);msg << v.first << bool(GcLocal::DevelopmentRow(v.skin)->rating == 6); WriteZeroSchema(msg,"iiic"); return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalEvolutionResult&) { return msg; }
inline void AppendTextOut(String& out, LocalEvolutionResult&) { out += L"<EvolutionResult>"; }
inline CMessage& operator<<(CMessage& msg, const LocalBreakResult& v) {
    WriteDevelopmentSkin(msg,v.skin); msg << MissionResult{}; msg.WriteScalar(int32_t(0));
    msg.WriteScalar(int32_t(v.costs.size())); for(auto p:v.costs)WriteCommonResult(msg,p.first,-p.second);
    WriteZeroSchema(msg,"iiii"); return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalBreakResult&) { return msg; }
inline void AppendTextOut(String& out, LocalBreakResult&) { out += L"<LimitBreakResult>"; }
inline CMessage& operator<<(CMessage& msg, const LocalSkillResult& v) {
    WriteDevelopmentSkin(msg,v.skin);msg.WriteScalar(int32_t(v.costs.size()));for(auto p:v.costs)WriteCommonResult(msg,p.first,-p.second);msg << MissionResult{}; WriteZeroSchema(msg,"ciiii"); return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalSkillResult&) { return msg; }
inline void AppendTextOut(String& out, LocalSkillResult&) { out += L"<UltimateUpgradeResult>"; }

inline void WriteQuest(CMessage& msg, int id) {
    const auto& q=GcLocal::Quests().at(id); msg << int32_t(id) << q.status;
    msg.WriteScalar(int32_t(q.progress.size())); for (int p : q.progress) msg << int32_t(p);
    msg << q.interaction;
}
inline CMessage& operator<<(CMessage& msg, const LocalQuestStartResult& v) {
    WriteQuest(msg,v.quest);int item=0;for(auto r:GcLocal::QuestItemRules)if(r.quest==v.quest){item=r.item;break;}
    if(item)WriteCommonResult(msg,item,0);else WriteZeroSchema(msg,"bibiiiiioi");msg.WriteScalar(int32_t(0));return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalQuestStartResult&) { return msg; }
inline void AppendTextOut(String& out, LocalQuestStartResult&) { out += L"<QuestStart>"; }
inline CMessage& operator<<(CMessage& msg, const LocalQuestProgressResult& v) {
    WriteQuest(msg,v.quest); WriteCommonResults(msg,v.drops,true); msg << MissionResult{}; return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalQuestProgressResult&) { return msg; }
inline void AppendTextOut(String& out, LocalQuestProgressResult&) { out += L"<QuestProgress>"; }
inline CMessage& operator<<(CMessage& msg, const LocalQuestClearResult& v) {
    msg << v.quest << int32_t(0);msg.WriteScalar(int32_t(v.rewards.size()));
    for(const auto& r:v.rewards)WriteNativeReward(msg,r);
    WriteCommonResults(msg,v.consumed);
    msg.WriteScalar(int32_t(v.next ? 2 : 1)); WriteQuest(msg,v.quest); if (v.next) WriteQuest(msg,v.next);
    msg << MissionResult{};
    WriteZeroSchema(msg,"iiiiiiiicc"); msg << uint8_t(1);
    msg.WriteScalar(int32_t(0)); msg.WriteScalar(int32_t(v.next ? 1 : 0)); if (v.next) msg << v.next;
    return msg;
}
inline CMessage& operator>>(CMessage& msg, LocalQuestClearResult&) { return msg; }
inline void AppendTextOut(String& out, LocalQuestClearResult&) { out += L"<QuestClear>"; }
inline CMessage& operator>>(CMessage& msg,LocalCookingRequest& v){
 msg>>v.npc;int n;msg.ReadScalar(n);if(n<1||n>3)throw std::runtime_error("Invalid cooking ingredients");
 for(int i=0,id;i<n;++i){msg>>id;v.materials.push_back(id);}msg>>v.count>>v.immediately;return msg;
}
inline CMessage& operator<<(CMessage& msg,const LocalCookingRequest&){return msg;}
inline void AppendTextOut(String& s,LocalCookingRequest&){s+=L"<CookingRequest>";}
inline void WriteQuestProgressList(CMessage& msg){msg.WriteScalar(int32_t(GcLocal::Quests().size()));for(auto p:GcLocal::Quests())WriteQuest(msg,p.first);}
inline CMessage& operator>>(CMessage& msg,LocalMissionClearRequest& v){int n;msg.ReadScalar(n);if(n<1||n>1000)throw std::runtime_error("Invalid mission claim list");for(int i=0;i<n;++i){int id;uint8_t index;msg>>id>>index;v.missions.emplace_back(id,index);}return msg;}
inline CMessage& operator<<(CMessage& msg,const LocalMissionClearRequest&){return msg;}
inline void AppendTextOut(String& s,LocalMissionClearRequest&){s+=L"<MissionClaims>";}
inline CMessage& operator<<(CMessage& msg,const LocalMissionClearResult& v){
 msg.WriteScalar(int32_t(v.chains.size()));for(int id:v.chains)msg<<int32_t(id);msg<<int32_t(0);
 msg.WriteScalar(int32_t(v.rewards.size()));for(auto r:v.rewards)WriteNativeReward(msg,r);
 msg<<MissionResult{true};WriteZeroSchema(msg,"cii");return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalMissionClearResult&){return msg;}
inline void AppendTextOut(String& s,LocalMissionClearResult&){s+=L"<MissionRewards>";}
inline CMessage& operator<<(CMessage& msg,const LocalAchievementResult& v){msg<<int16_t(v.order);WriteCommonResult(msg,500009);if(v.item)WriteCommonResult(msg,v.item,v.count);else msg<<LocalNoItem{};msg<<MissionResult{true};return msg;}
inline CMessage& operator>>(CMessage& msg,LocalAchievementResult&){return msg;}
inline void AppendTextOut(String& s,LocalAchievementResult&){s+=L"<AchievementReward>";}
inline CMessage& operator<<(CMessage& msg,const LocalChapterResult& v){msg<<int64_t(GcLocal::Progression().chapterFlags);WriteZeroSchema(msg,"llll");msg.WriteScalar(int32_t(v.rewards.size()));for(auto r:v.rewards)WriteNativeReward(msg,r);msg<<MissionResult{};return msg;}
inline CMessage& operator>>(CMessage& msg,LocalChapterResult&){return msg;}
inline void AppendTextOut(String& s,LocalChapterResult&){s+=L"<ChapterReward>";}
inline CMessage& operator<<(CMessage& msg,const LocalGuideResult& v){msg<<GcLocal::Progression().guideRewarded<<int16_t(GcLocal::Progression().guideStep);WriteQuestProgressList(msg);if(v.clear){msg.WriteScalar(int32_t(v.rewards.size()));for(auto r:v.rewards)WriteNativeReward(msg,r);msg<<MissionResult{};msg.WriteScalar(int32_t(v.upgrades.size()));for(auto p:v.upgrades){msg<<int32_t(p.first);WriteDevelopmentSkin(msg,p.second);}}return msg;}
inline CMessage& operator>>(CMessage& msg,LocalGuideResult&){return msg;}
inline void AppendTextOut(String& s,LocalGuideResult&){s+=L"<HeroWayPhase>";}
inline CMessage& operator<<(CMessage& msg,const LocalCookingResult& v){
 msg<<uint8_t(1)<<uint8_t(0);WriteCommonResults(msg,v.costs);WriteCommonResults(msg,v.drops,true);
 msg<<int32_t(v.recipe)<<int32_t(GcLocal::RecipeExperience()[v.recipe])<<true<<MissionResult{};
 WriteQuestProgressList(msg);msg<<int32_t(v.count)<<int32_t(v.npc)<<int32_t(0)<<v.immediately;return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalCookingResult&){return msg;}
inline void AppendTextOut(String& s,LocalCookingResult&){s+=L"<CookingResult>";}
inline CMessage& operator>>(CMessage& msg,LocalTownBuyRequest& v){
 int n;msg.ReadScalar(n);if(n<1||n>100)throw std::runtime_error("Invalid town shop purchase");
 for(int i=0,id;i<n;++i){uint8_t count;msg>>id>>count;v.products.emplace_back(id,count);}return msg;
}
inline CMessage& operator<<(CMessage& msg,const LocalTownBuyRequest&){return msg;}
inline void AppendTextOut(String& s,LocalTownBuyRequest&){s+=L"<TownBuyRequest>";}
inline void WriteTownProduct(CMessage& msg,int id){const auto* r=GcLocal::FindTownProduct(id);if(!r)throw std::runtime_error("Unknown town product");msg<<int32_t(id)<<int32_t(r->town)<<uint8_t(GcLocal::TownShopCounts()[id])<<uint8_t(0)<<int32_t(0)<<int32_t(0)<<uint8_t(0)<<uint8_t(0);}
inline CMessage& operator<<(CMessage& msg,const LocalTownShopResult& v){
 int n=0;for(auto r:GcLocal::TownShopRules)if(r.town==v.town)++n;
 msg.WriteScalar(int32_t(n));for(auto r:GcLocal::TownShopRules)if(r.town==v.town)WriteTownProduct(msg,r.id);msg<<uint8_t(0);return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalTownShopResult&){return msg;}
inline void AppendTextOut(String& s,LocalTownShopResult&){s+=L"<TownShopResult>";}
inline CMessage& operator<<(CMessage& msg,const LocalTownBuyResult& v){
 WriteCommonResults(msg,v.costs);WriteCommonResults(msg,v.drops,true);msg.WriteScalar(int32_t(v.products.size()));for(int id:v.products)WriteTownProduct(msg,id);
 WriteQuestProgressList(msg);msg<<MissionResult{}<<LocalPayback{};return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalTownBuyResult&){return msg;}
inline void AppendTextOut(String& s,LocalTownBuyResult&){s+=L"<TownBuyResult>";}

inline void WriteCoinBuyInfo(CMessage& msg,int id) {
    msg<<int32_t(id)<<int32_t(0)<<uint8_t(0)<<uint8_t(0)<<int32_t(0)<<int32_t(2147483647)<<uint8_t(0)<<uint8_t(0);
}
inline CMessage& operator<<(CMessage& msg,const LocalCoinShopInfo&) {
    for(bool event:{false,true}) {
        int count=0;for(const auto& row:GcLocal::CoinProducts)if(row.event==event)++count;
        msg.WriteScalar(count);for(const auto& row:GcLocal::CoinProducts)if(row.event==event)WriteCoinBuyInfo(msg,row.id);
    }return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalCoinShopInfo&) {return msg;}
inline void AppendTextOut(String& out,LocalCoinShopInfo&) {out+=L"<CoinShop>";}
inline CMessage& operator>>(CMessage& msg,LocalCoinBuyRequest& v) {
    msg>>v.shop>>v.count;int count;msg.ReadScalar(count);
    if(count<0||count>1000)throw std::runtime_error("Invalid payment list");
    for(int i=0;i<count;++i){int id,n;msg>>id>>n;if(n<1)throw std::runtime_error("Invalid coin payment");v.payments.emplace_back(id,n);}
    bool ad;msg>>ad;return msg;
}
inline CMessage& operator<<(CMessage& msg,const LocalCoinBuyRequest&) {return msg;}
inline void AppendTextOut(String& out,LocalCoinBuyRequest&) {out+=L"<CoinPurchase>";}
inline CMessage& operator<<(CMessage& msg,const LocalCoinBuyResult& v) {
    const auto* row=GcLocal::FindCoinProduct(v.shop,v.event);
    if(!row)throw std::runtime_error("Unknown coin product");
    msg<<v.shop;WriteCoinBuyInfo(msg,v.shop);
    msg.WriteScalar(int32_t(v.payments.size()+(v.newHero?1:0)));
    for(auto p:v.payments)WriteCommonResult(msg,p.first);
    if(v.newHero){const auto* skin=GcLocal::FindSkin(row->item);msg<<uint8_t(210)<<int32_t(skin->hero);WriteZeroSchema(msg,"ibiiiiioi");}
    int rewardType=row->type,rewardItem=row->item;
    if(row->type==211&&!v.newHero){for(auto c:GcLocal::HeroCoins)if(c.skin==row->item){rewardItem=c.coin;rewardType=GcLocal::FindMaterialType(c.coin);break;}}
    msg<<uint8_t(rewardType);
    if(rewardType==211) WriteDevelopmentSkin(msg,rewardItem);
    else if(rewardType==216)msg<<int32_t(rewardItem);
    else msg<<int32_t(rewardItem)<<int32_t(GcLocal::SeededMaterialCount(rewardItem));
    msg<<int32_t(v.count*row->count)<<uint8_t(0)<<int32_t(rewardType==211?rewardItem:0);
    WriteZeroSchema(msg,"iii");msg<<int32_t(rewardType==216?rewardItem:0)<<false<<int32_t(0);
    WriteZeroSchema(msg,"bidii");msg<<MissionResult{};msg.WriteScalar(int32_t(0));msg<<LocalPayback{};
    return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalCoinBuyResult&) {return msg;}
inline void AppendTextOut(String& out,LocalCoinBuyResult&) {out+=L"<CoinPurchaseResult>";}
inline CMessage& operator>>(CMessage& msg,LocalFortCoinOpenRequest& v) {
    msg>>v.area;int count;msg.ReadScalar(count);
    if(count<0||count>1000)throw std::runtime_error("Invalid dungeon payment list");
    for(int i=0;i<count;++i)ReadZeroSchema(msg,"ii");return msg;
}
inline CMessage& operator<<(CMessage& msg,const LocalFortCoinOpenRequest&) {return msg;}
inline void AppendTextOut(String& out,LocalFortCoinOpenRequest&) {out+=L"<FortCoinOpen>";}
inline CMessage& operator>>(CMessage& msg,LocalTranscendRequest& v) {
    msg>>v.hero>>v.rank;int count;msg.ReadScalar(count);
    if(count<0||count>100)throw std::runtime_error("Invalid awakening payment count");
    for(int i=0;i<count;++i){int id,amount;msg>>id>>amount;if(amount<1||amount>GcLocal::TestMaterialCount||!GcLocal::FindMaterialType(id))throw std::runtime_error("Invalid awakening material");v.items.emplace_back(id,amount);}return msg;
}
inline CMessage& operator<<(CMessage& msg,const LocalTranscendRequest&) {return msg;}
inline void AppendTextOut(String& out,LocalTranscendRequest&) {out+=L"<SuperAwaken>";}
inline CMessage& operator>>(CMessage& msg,LocalIntListRequest& v){int count;msg.ReadScalar(count);if(count<0||count>500)throw std::runtime_error("Invalid equipment selection");for(int i=0,id;i<count;++i){msg>>id;v.ids.push_back(id);}return msg;}
inline CMessage& operator<<(CMessage& msg,const LocalIntListRequest&){return msg;}
inline void AppendTextOut(String& out,LocalIntListRequest&){out+=L"<EquipmentSelection>";}
inline CMessage& operator>>(CMessage& msg,LocalBoxRequest& v){msg>>v.item>>v.count;ReadGcString(msg,v.answer);int count;msg.ReadScalar(count);if(count<0||count>20)throw std::runtime_error("Invalid box choices");for(int i=0,id;i<count;++i){msg>>id;v.choices.push_back(id);}return msg;}
inline CMessage& operator<<(CMessage& msg,const LocalBoxRequest&){return msg;}
inline void AppendTextOut(String& out,LocalBoxRequest&){out+=L"<BoxOpen>";}
inline CMessage& operator<<(CMessage& msg,const LocalBoxResult& v){WriteCommonResult(msg,v.item);WriteCommonResults(msg,v.drops,true);msg.WriteScalar(int32_t(0));msg<<MissionResult{};return msg;}
inline CMessage& operator<<(CMessage& msg,const LocalMailResult& v){
    if(v.kind==0){msg.WriteScalar(int32_t(GcLocal::WelcomePending()?1:0));
        if(GcLocal::WelcomePending())msg<<int32_t(1)<<int32_t(1)<<uint8_t(1)<<int32_t(500011)<<int32_t(600)<<int32_t(0)<<int64_t(639269064000000000LL)<<int32_t(1)<<int64_t(3155378975999999999LL)<<int32_t(1);
        WriteZeroSchema(msg,"cccc");return msg;
    }
    if(v.kind==1){msg<<int32_t(1);msg.WriteScalar(int32_t(0));}
    else {msg.WriteScalar(int32_t(v.claimed?1:0));if(v.claimed)msg<<int32_t(1);}
    WriteCommonResults(msg,v.claimed?std::vector<std::pair<int,int>>{{500011,600}}:std::vector<std::pair<int,int>>{},true);
    msg.WriteScalar(int32_t(0));msg<<MissionResult{};return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalMailResult&){return msg;}
inline void AppendTextOut(String& out,LocalMailResult&){out+=L"<WelcomeMail>";}
inline CMessage& operator>>(CMessage& msg,LocalBoxResult&){return msg;}
inline void AppendTextOut(String& out,LocalBoxResult&){out+=L"<BoxRewards>";}
inline CMessage& operator<<(CMessage& msg,const LocalSystemsResult& v) {
    if(v.kind==11){WriteDevelopmentSkin(msg,v.skin);WriteWeapon(msg,v.serial);WriteDevelopmentSkin(msg,v.other);msg<<false<<int32_t(v.serials.empty()?0:v.serials[0]);WriteCommonResults(msg,v.items);msg<<MissionResult{};WriteZeroSchema(msg,"ciii");return msg;}
    if(v.kind==12){WriteDevelopmentSkin(msg,v.skin);WriteDevelopmentSkin(msg,v.other);msg.WriteScalar(int32_t(v.serials.size()));for(int id:v.serials)WriteWeapon(msg,id);WriteCommonResults(msg,v.items);msg<<MissionResult{};WriteZeroSchema(msg,"ciii");return msg;}
    if(v.kind==13){WriteDevelopmentSkin(msg,v.skin);msg.WriteScalar(int32_t(v.serials.size()));for(int id:v.serials)WriteWeapon(msg,id);msg<<MissionResult{};WriteZeroSchema(msg,"c");return msg;}
    if(v.kind==30){WriteDevelopmentSkin(msg,v.skin);WriteCommonResults(msg,v.items);msg<<int32_t(GcLocal::SeededMaterialCount(540001))<<MissionResult{}<<int32_t(0);return msg;}
    if(v.kind==31){WriteDevelopmentSkin(msg,v.skin);msg<<MissionResult{};return msg;}
    if(v.kind==32){WriteCommonResults(msg,v.items);const auto* c=GcLocal::FindCosmetic(v.other);if(!c)throw std::runtime_error("Missing crafted cosmetic");
        msg<<uint8_t(212+c->type)<<int32_t(c->id)<<int32_t(0)<<uint8_t(0)<<uint8_t(c->heroGroup)<<int32_t(c->group)<<int64_t(0)<<int32_t(0);
        msg<<int32_t(1)<<uint8_t(0)<<int32_t(0)<<int32_t(c->id);WriteZeroSchema(msg,"iiioi");msg<<MissionResult{}<<LocalPayback{};return msg;}
    if(v.kind==33){WriteCommonResult(msg,v.other,-1);msg.WriteScalar(int32_t(1));msg<<uint8_t(212);WriteWeapon(msg,v.serial);msg<<int32_t(1);WriteZeroSchema(msg,"biiiiioi");msg<<MissionResult{};return msg;}
    if(v.kind==0){WriteDevelopmentSkin(msg,v.skin);WriteWeapon(msg,v.serial);msg<<int32_t(v.other)<<false;WriteCommonResults(msg,v.items);msg<<MissionResult{};WriteZeroSchema(msg,"ciii");return msg;}
    if(v.kind==1){WriteDevelopmentSkin(msg,v.skin);WriteWeapon(msg,v.serial);WriteCommonResults(msg,v.items);msg<<LocalPayback{};return msg;}
    if(v.kind==2||v.kind==3){msg.WriteScalar(int32_t(v.serials.size()));for(int id:v.serials)msg<<int32_t(id);
        if(v.kind==2){if(v.items.empty())msg<<LocalNoItem{};else WriteCommonResult(msg,v.items[0].first,v.items[0].second);msg<<MissionResult{};}
        else {WriteCommonResults(msg,v.items,true);msg.WriteScalar(int32_t(v.successes.size()));for(auto s:v.successes)msg<<int32_t(s.first)<<uint8_t(s.second);msg<<MissionResult{};WriteZeroSchema(msg,"cc");}return msg;}
    if(v.kind==8)msg<<uint8_t(1);
    WriteWeapon(msg,v.serial);
    if(v.kind==9||v.kind==10)return msg;
    if(v.kind==15){if(v.items.empty())msg<<LocalNoItem{};else WriteCommonResult(msg,v.items[0].first);msg<<LocalPayback{};return msg;}
    WriteCommonResults(msg,v.items);
    if(v.kind==4){msg<<MissionResult{};WriteZeroSchema(msg,"cbhiiicc");}
    else if(v.kind==5){msg<<LocalPayback{}<<MissionResult{};WriteZeroSchema(msg,"c");}
    else if(v.kind==6){WriteZeroSchema(msg,"c");msg<<MissionResult{}<<LocalPayback{};WriteZeroSchema(msg,"cc");}
    else if(v.kind==7){msg<<MissionResult{}<<LocalPayback{};WriteZeroSchema(msg,"c");}
    else if(v.kind==8){msg<<LocalPayback{}<<MissionResult{};}
    else if(v.kind==14){WriteZeroSchema(msg,"c");msg<<MissionResult{}<<LocalPayback{};}
    else if(v.kind==15){/* Remove uses a single ItemResultInfo, handled by its dedicated kind below. */}
    return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalSystemsResult&){return msg;}
inline void AppendTextOut(String& out,LocalSystemsResult&){out+=L"<NativeSystemResult>";}
inline CMessage& operator<<(CMessage& msg,const LocalLegendResult& v) {
    msg << v.previous;WriteDevelopmentSkin(msg,v.skin);msg << MissionResult{};msg.WriteScalar(int32_t(0));msg.WriteScalar(int32_t(v.costs.size()));for(auto p:v.costs)WriteCommonResult(msg,p.first,-p.second);
    msg << LocalPayback{} << int32_t(GcLocal::SeededMaterialCount(540001));return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalLegendResult&) {return msg;}
inline void AppendTextOut(String& out,LocalLegendResult&) {out+=L"<LegendEvolution>";}
// Native SkinOneStepEvolutionResult followed by its separate ItemResultInfo.
inline CMessage& operator<<(CMessage& msg,const LocalOneStepResult& v) {
    msg << v.previous << int32_t(GcLocal::SeededMaterialCount(540001));
    WriteDevelopmentSkin(msg,v.skin); msg << MissionResult{}; WriteZeroSchema(msg,"cc");
    msg << uint8_t(GcLocal::FindMaterialType(v.item)) << v.item << int32_t(GcLocal::SeededMaterialCount(v.item));
    WriteZeroSchema(msg,"ibiiiiioi"); return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalOneStepResult&) {return msg;}
inline void AppendTextOut(String& out,LocalOneStepResult&) {out+=L"<OneStepEvolution>";}
inline CMessage& operator<<(CMessage& msg,const LocalGrowthResult& v) {
    WriteDevelopmentSkin(msg,v.skin);msg.WriteScalar(int32_t(v.items.size()));
    for(int id:v.items){msg<<uint8_t(GcLocal::FindMaterialType(id))<<int32_t(id)<<int32_t(GcLocal::SeededMaterialCount(id));WriteZeroSchema(msg,"ibiiiiioi");}
    if(v.kind==0){msg<<MissionResult{};WriteZeroSchema(msg,"cc");msg<<int32_t(GcLocal::SeededMaterialCount(540001));}
    else {msg<<LocalPayback{};if(v.kind==1){msg<<int32_t(GcLocal::SeededMaterialCount(540001))<<MissionResult{};msg.WriteScalar(int32_t(0));}}
    return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalGrowthResult&) {return msg;}
inline void AppendTextOut(String& out,LocalGrowthResult&) {out+=L"<GrowthResult>";}

}

namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalFoodResult& v){
 if(v.recipe)msg<<int32_t(v.recipe)<<int32_t(GcLocal::RecipeExperience()[v.recipe])<<true;
 else {const auto& s=GcLocal::Food();msg<<int32_t(s.item)<<uint8_t(s.used)<<s.automatic;}
 if(!v.toggle){if(v.item)WriteCommonResult(msg,v.item,-1);else msg<<LocalNoItem{};msg<<MissionResult{};WriteQuestProgressList(msg);}return msg;
}
inline CMessage& operator>>(CMessage& msg,LocalFoodResult&){return msg;}
inline void AppendTextOut(String& s,LocalFoodResult&){s+=L"<FoodResult>";}
}

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

namespace Proud {
inline void WriteFinalBossSeason(CMessage& msg){int current=0;std::set<int> seasons;for(auto r:GcLocal::FinalBossSettings){seasons.insert(r.season);current=(std::max)(current,r.season);}msg<<int32_t(current)<<int32_t(0);msg.WriteScalar(int32_t(sizeof(GcLocal::FinalBossSettings)/sizeof(GcLocal::FinalBossSettings[0])));for(auto r:GcLocal::FinalBossSettings)msg<<int32_t(r.id)<<int32_t(r.group)<<int32_t(0)<<int32_t(2147483647)<<uint8_t(0);msg<<int32_t(2147483647)<<int32_t(GcLocal::SeededMaterialCount(500806));msg.WriteScalar(int32_t(seasons.size()));for(int id:seasons)msg<<int32_t(id)<<int32_t(0)<<int32_t(2147483647);WriteZeroSchema(msg,"cibc");}
inline CMessage& operator<<(CMessage& msg,const LocalFinalBossInfo&){WriteFinalBossSeason(msg);msg.WriteScalar(int32_t(0));return msg;}
inline CMessage& operator>>(CMessage& msg,LocalFinalBossInfo&){return msg;}
inline void AppendTextOut(String& s,LocalFinalBossInfo&){s+=L"<FinalBossInfo>";}
inline CMessage& operator<<(CMessage& msg,const LocalFinalBossClearExtra&){WriteZeroSchema(msg,"iiiccliiiciii");return msg;}
inline CMessage& operator>>(CMessage& msg,LocalFinalBossClearExtra&){return msg;}
inline void AppendTextOut(String& s,LocalFinalBossClearExtra&){s+=L"<FinalBossScore>";}
inline CMessage& operator<<(CMessage& msg,const LocalFinalBossRank&){WriteZeroSchema(msg,"cciiliiiciii");return msg;}
inline CMessage& operator>>(CMessage& msg,LocalFinalBossRank&){return msg;}
inline void AppendTextOut(String& s,LocalFinalBossRank&){s+=L"<FinalBossRank>";}
}

namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalRelicUpgradeResult& v){const auto* c=GcLocal::FindCosmetic(v.costume);if(!c)throw std::runtime_error("Unknown relic");msg<<int32_t(c->group)<<int32_t(c->heroGroup)<<uint8_t(GcLocal::RelicUpgrades()[{c->group,c->heroGroup}]);WriteCommonResults(msg,v.costs);msg<<LocalPayback{}<<int32_t(GcLocal::SeededMaterialCount(540001));return msg;}
inline CMessage& operator>>(CMessage& msg,LocalRelicUpgradeResult&){return msg;}
inline void AppendTextOut(String& s,LocalRelicUpgradeResult&){s+=L"<RelicUpgrade>";}
}

namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalTownDonationResult& v){WriteTownInfo(msg,v.town);WriteCommonResult(msg,500012,-v.count);msg.WriteScalar(int32_t(0));WriteZeroSchema(msg,"biii");msg<<MissionResult{};WriteQuestProgressList(msg);msg<<LocalPayback{};return msg;}
inline CMessage& operator>>(CMessage& msg,LocalTownDonationResult&){return msg;}
inline void AppendTextOut(String& s,LocalTownDonationResult&){s+=L"<TownDonation>";}
}

struct LocalPackageInfo {};
struct LocalBulkLevelEntry {int hero=0,index=0;std::vector<std::pair<int32_t,int32_t>> items;};
struct LocalBulkLevelRequest {std::vector<LocalBulkLevelEntry> entries;};
struct LocalBulkLevelResult {std::vector<int> skins;std::vector<std::pair<int32_t,int32_t>> costs;std::vector<LocalBulkLevelEntry> entries;};
struct LocalBulkGrowthResult {std::vector<std::pair<int,int>> skins;std::vector<std::pair<int32_t,int32_t>> costs;bool evolution=false,passive=false,packages=true;};
struct LocalBulkSkillRequest {std::vector<std::pair<int,int>> entries;};
struct LocalBulkPassiveRequest {std::vector<int> heroes;};
namespace Proud {
inline CMessage& operator>>(CMessage& m,LocalBulkSkillRequest& v){int n;m.ReadScalar(n);if(n<0||n>2048)throw std::runtime_error("Invalid bulk ultimate count");for(int i=0;i<n;++i){int hero,count;m>>hero>>count;v.entries.emplace_back(hero,count);}return m;}
inline CMessage& operator<<(CMessage& m,const LocalBulkSkillRequest&){return m;}
inline void AppendTextOut(String& out,LocalBulkSkillRequest&){out+=L"<BulkUltimate>";}
inline CMessage& operator>>(CMessage& m,LocalBulkPassiveRequest& v){int n;m.ReadScalar(n);if(n<0||n>2048)throw std::runtime_error("Invalid bulk passive count");for(int i=0;i<n;++i){int hero;m>>hero;v.heroes.push_back(hero);}return m;}
inline CMessage& operator<<(CMessage& m,const LocalBulkPassiveRequest&){return m;}
inline void AppendTextOut(String& out,LocalBulkPassiveRequest&){out+=L"<BulkPassive>";}
inline CMessage& operator<<(CMessage& m,const LocalBulkGrowthResult& v){
 m.WriteScalar(int32_t(v.skins.size()));for(auto p:v.skins){WriteDevelopmentSkin(m,p.second);if(v.evolution)m<<int32_t(p.first);}
 if(v.passive)return m;
 m.WriteScalar(int32_t(v.costs.size()));for(auto p:v.costs)WriteCommonResult(m,p.first,-p.second);
 m<<MissionResult{};m.WriteScalar(int32_t(0));m<<LocalPayback{};
 if(!v.evolution)m<<int32_t(0);
 if(v.packages)m.WriteScalar(int32_t(0));return m;
}
inline CMessage& operator>>(CMessage& m,LocalBulkGrowthResult&){return m;}
inline void AppendTextOut(String& out,LocalBulkGrowthResult&){out+=L"<BulkGrowth>";}
}
namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalPackageInfo&){WriteZeroSchema(msg,"c");msg<<int64_t(639269123000000000LL)<<int32_t(0);WriteZeroSchema(msg,"coici");return msg;}
inline CMessage& operator>>(CMessage& msg,LocalPackageInfo&){return msg;}
inline void AppendTextOut(String& out,LocalPackageInfo&){out+=L"<PackageInfo>";}
inline CMessage& operator>>(CMessage& msg,LocalBulkLevelRequest& v){int64_t n;msg.ReadScalar(n);if(n<0||n>2048)throw std::runtime_error("Invalid bulk hero count: "+std::to_string(n));for(int i=0;i<n;++i){LocalBulkLevelEntry e;msg>>e.hero>>e.index;int64_t k;msg.ReadScalar(k);if(k<0||k>100)throw std::runtime_error("Invalid bulk material count");for(int j=0;j<k;++j){int32_t id,count;msg>>id>>count;if(count<=0||count>GcLocal::TestMaterialCount)throw std::runtime_error("Invalid bulk material amount");e.items.emplace_back(id,count);}v.entries.push_back(e);}return msg;}
inline CMessage& operator<<(CMessage& msg,const LocalBulkLevelRequest&){return msg;}
inline void AppendTextOut(String& out,LocalBulkLevelRequest&){out+=L"<BulkLevelRequest>";}
inline CMessage& operator<<(CMessage& msg,const LocalBulkLevelResult& v){msg.WriteScalar(int32_t(v.skins.size()));for(int skin:v.skins)WriteDevelopmentSkin(msg,skin);msg.WriteScalar(int32_t(v.costs.size()));for(auto p:v.costs)WriteCommonResult(msg,p.first,-p.second);msg.WriteScalar(int32_t(v.entries.size()));for(auto e:v.entries){msg<<int32_t(e.hero);int n=0;for(auto p:e.items)if(p.first!=500012)++n;msg.WriteScalar(int32_t(n));int index=0;for(auto p:e.items)if(p.first!=500012)msg<<int32_t(index++)<<uint8_t(0);}msg<<MissionResult{};WriteZeroSchema(msg,"ciiiic");return msg;}
inline CMessage& operator>>(CMessage& msg,LocalBulkLevelResult&){return msg;}
inline void AppendTextOut(String& out,LocalBulkLevelResult&){out+=L"<BulkLevelResult>";}
}

struct LocalFinalBossShopInfo {};
struct LocalFinalBossShopBuy {int product=0,count=0;std::vector<LocalNativeReward> rewards;};
namespace Proud {
inline void WriteFinalBossBuy(CMessage& msg,int id){const auto* r=GcLocal::FindFinalBossProduct(id);auto p=GcLocal::FinalBossPurchases()[id];msg<<int32_t(r->season)<<int32_t(id)<<uint8_t(GcLocal::FinalBossDaily(p))<<int16_t(p.total);}
inline CMessage& operator<<(CMessage& msg,const LocalFinalBossShopInfo&){std::map<int,std::set<int>> seasons;for(auto r:GcLocal::FinalBossProducts)seasons[r.season].insert(r.price);msg.WriteScalar(int32_t(seasons.size()));for(auto s:seasons){msg<<int32_t(s.first)<<int32_t(0)<<int32_t(2147483647);msg.WriteScalar(int32_t(s.second.size()));for(int id:s.second)msg<<int32_t(id)<<int32_t(GcLocal::SeededMaterialCount(id));}msg.WriteScalar(int32_t(GcLocal::FinalBossPurchases().size()));for(auto p:GcLocal::FinalBossPurchases())WriteFinalBossBuy(msg,p.first);msg.WriteScalar(int32_t(0));return msg;}
inline CMessage& operator>>(CMessage& msg,LocalFinalBossShopInfo&){return msg;}
inline void AppendTextOut(String& s,LocalFinalBossShopInfo&){s+=L"<FinalBossShop>";}
inline CMessage& operator<<(CMessage& msg,const LocalFinalBossShopBuy& v){auto r=GcLocal::FindFinalBossProduct(v.product);msg.WriteScalar(int32_t(1));WriteCommonResult(msg,r->price,-r->amount*v.count);msg.WriteScalar(int32_t(v.rewards.size()));for(auto reward:v.rewards)WriteNativeReward(msg,reward);WriteFinalBossBuy(msg,v.product);msg<<MissionResult{}<<LocalPayback{};return msg;}
inline CMessage& operator>>(CMessage& msg,LocalFinalBossShopBuy&){return msg;}
inline void AppendTextOut(String& s,LocalFinalBossShopBuy&){s+=L"<FinalBossPurchase>";}
}

namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalDescentInfo&){msg<<int32_t(GcLocal::DescentEventSequence)<<int32_t(GcLocal::DescentEventSubIndex)<<int64_t(3155378975999999999LL)<<int32_t(1)<<int32_t(GcLocal::DescentClearFlags())<<int32_t(GcLocal::DescentRewardFlags())<<int32_t(0)<<int16_t(299)<<uint8_t(GcLocal::CustomMode()?255:0);return msg;}
inline CMessage& operator>>(CMessage& msg,LocalDescentInfo&){return msg;}
inline void AppendTextOut(String& s,LocalDescentInfo&){s+=L"<DescentInfo>";}
}

struct LocalDescentRewardResult {std::vector<LocalNativeReward> rewards;};
namespace Proud {
inline CMessage& operator<<(CMessage& msg,const LocalDescentRewardResult& v){msg<<LocalDescentInfo{};msg.WriteScalar(int32_t(v.rewards.size()));for(auto r:v.rewards)WriteNativeReward(msg,r);msg<<LocalPayback{};return msg;}
inline CMessage& operator>>(CMessage& msg,LocalDescentRewardResult&){return msg;}
inline void AppendTextOut(String& s,LocalDescentRewardResult&){s+=L"<DescentReward>";}
}

namespace Proud {
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

}

struct LocalTowerShopInfo {};
struct LocalTowerShopBuy {int product=0,count=0;std::vector<LocalNativeReward> rewards;};
namespace Proud {
inline void WriteTowerShopBuy(CMessage& msg,int id){auto p=GcLocal::TowerShopPurchases()[id];msg<<int32_t(id)<<int32_t(0)<<uint8_t(GcLocal::TowerShopDaily(p))<<uint8_t(0)<<int32_t(0)<<int32_t(2147483647)<<uint8_t(0)<<uint8_t(p.total);}
inline CMessage& operator<<(CMessage& msg,const LocalTowerShopInfo&){msg.WriteScalar(int32_t(GcLocal::TowerShopPurchases().size()));for(auto p:GcLocal::TowerShopPurchases())WriteTowerShopBuy(msg,p.first);msg<<int32_t(LocalDailyResetSeconds());return msg;}
inline CMessage& operator>>(CMessage& msg,LocalTowerShopInfo&){return msg;}
inline void AppendTextOut(String& s,LocalTowerShopInfo&){s+=L"<TowerShop>";}
inline CMessage& operator<<(CMessage& msg,const LocalTowerShopBuy& v){const auto* r=GcLocal::FindTowerShopProduct(v.product);msg.WriteScalar(int32_t(1));WriteCommonResult(msg,r->price,-r->amount*v.count);msg.WriteScalar(int32_t(v.rewards.size()));for(auto reward:v.rewards)WriteNativeReward(msg,reward);WriteTowerShopBuy(msg,v.product);msg<<MissionResult{}<<LocalPayback{};return msg;}
inline CMessage& operator>>(CMessage& msg,LocalTowerShopBuy&){return msg;}
inline void AppendTextOut(String& s,LocalTowerShopBuy&){s+=L"<TowerShopPurchase>";}
}
