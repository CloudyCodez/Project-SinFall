#pragma once
#include "Protocol/GrandCrossRmiTypes.h"
namespace SevenDSArtifactTeamC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestArtifactTeamChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalArtifactTeam& request) { return false; }
#define DECRMI_SevenDSArtifactTeamC2S_CG_RequestArtifactTeamChange bool CG_RequestArtifactTeamChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalArtifactTeam& request) override
#define DEFRMI_SevenDSArtifactTeamC2S_CG_RequestArtifactTeamChange(DerivedClass) bool DerivedClass::CG_RequestArtifactTeamChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalArtifactTeam& request)
virtual bool CG_RequestArtifactDescentBossTeamChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalArtifactTeamList& request) { return false; }
#define DECRMI_SevenDSArtifactTeamC2S_CG_RequestArtifactDescentBossTeamChange bool CG_RequestArtifactDescentBossTeamChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalArtifactTeamList& request) override
#define DEFRMI_SevenDSArtifactTeamC2S_CG_RequestArtifactDescentBossTeamChange(DerivedClass) bool DerivedClass::CG_RequestArtifactDescentBossTeamChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalArtifactTeamList& request)
};
}
namespace SevenDSArtifactTeamS2C {
class Proxy { public:
bool CG_RequestArtifactTeamChangeOK(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(15093); return PhoneSend(remote,m); }
bool CG_RequestArtifactDescentBossTeamChangeOK(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(15094); return PhoneSend(remote,m); }
};
}
namespace SevenDSArtifactUnionC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestArtifactUnionUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalUnionRequest& request) { return false; }
#define DECRMI_SevenDSArtifactUnionC2S_CG_RequestArtifactUnionUpgrade bool CG_RequestArtifactUnionUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalUnionRequest& request) override
#define DEFRMI_SevenDSArtifactUnionC2S_CG_RequestArtifactUnionUpgrade(DerivedClass) bool DerivedClass::CG_RequestArtifactUnionUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalUnionRequest& request)
};
}
namespace SevenDSArtifactUnionS2C {
class Proxy { public:
bool CG_RequestArtifactUnionUpgradeOK(Proud::HostID remote, Proud::RmiContext& context, const LocalUnionResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(15092); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSAttendanceC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestAttendanceReward(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& deviceType) { return false; }
#define DECRMI_SevenDSAttendanceC2S_CG_RequestAttendanceReward bool CG_RequestAttendanceReward(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& deviceType) override
#define DEFRMI_SevenDSAttendanceC2S_CG_RequestAttendanceReward(DerivedClass) bool DerivedClass::CG_RequestAttendanceReward(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& deviceType)
};
}
namespace SevenDSAttendanceS2C {
class Proxy { public:
bool CG_RequestAttendanceRewardOK(Proud::HostID remote, Proud::RmiContext& context, const AttendanceResult& attendanceResult, const EmptyItemResults& userPackageMissionInfoList, const EmptyItemResults& resultQuestProgressInfoList) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14227); m << attendanceResult; m << userPackageMissionInfoList; m << resultQuestProgressInfoList; return PhoneSend(remote,m); }
};
}
namespace SevenDSAwakenStraightC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinAwakenStraight(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& awaken) { return false; }
#define DECRMI_SevenDSAwakenStraightC2S_CG_RequestSkinAwakenStraight bool CG_RequestSkinAwakenStraight(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& awaken) override
#define DEFRMI_SevenDSAwakenStraightC2S_CG_RequestSkinAwakenStraight(DerivedClass) bool DerivedClass::CG_RequestSkinAwakenStraight(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& awaken)
};
}
namespace SevenDSAwakenStraightS2C {
class Proxy { public:
bool CG_RequestSkinAwakenStraightOK(Proud::HostID remote, Proud::RmiContext& context, const LocalAwakenResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14135); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSBattleReadyC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestIngameBattleStart(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSBattleReadyC2S_CG_RequestIngameBattleStart bool CG_RequestIngameBattleStart(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSBattleReadyC2S_CG_RequestIngameBattleStart(DerivedClass) bool DerivedClass::CG_RequestIngameBattleStart(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSBattleReadyS2C {
class Proxy { public:
bool CG_RequestIngameBattleStartOK(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18802); return PhoneSend(remote,m); }
};
}
namespace SevenDSBootstrapC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestLobbySetAttendanceHero(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& attendanceHeroID, const int& activeAttendanceHeroID) { return false; }
#define DECRMI_SevenDSBootstrapC2S_CG_RequestLobbySetAttendanceHero bool CG_RequestLobbySetAttendanceHero(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& attendanceHeroID, const int& activeAttendanceHeroID) override
#define DEFRMI_SevenDSBootstrapC2S_CG_RequestLobbySetAttendanceHero(DerivedClass) bool DerivedClass::CG_RequestLobbySetAttendanceHero(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& attendanceHeroID, const int& activeAttendanceHeroID)
};
}
namespace SevenDSBootstrapS2C {
class Proxy { public:
bool CG_RequestLobbySetAttendanceHeroOK(Proud::HostID remote, Proud::RmiContext& context, const int& attendanceHeroID, const int& activeAttendanceHeroID) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14248); m << attendanceHeroID; m << activeAttendanceHeroID; return PhoneSend(remote,m); }
};
}
namespace SevenDSBossBattleC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_Request_Boss_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) { return false; }
#define DECRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Start bool CG_Request_Boss_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) override
#define DEFRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Start(DerivedClass) bool DerivedClass::CG_Request_Boss_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request)
virtual bool CG_Request_Boss_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) { return false; }
#define DECRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Clear bool CG_Request_Boss_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) override
#define DEFRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Clear(DerivedClass) bool DerivedClass::CG_Request_Boss_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request)
virtual bool CG_Request_Boss_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Continue bool CG_Request_Boss_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSBossBattleC2S_CG_Request_Boss_Stage_Continue(DerivedClass) bool DerivedClass::CG_Request_Boss_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSBossBattleS2C {
class Proxy { public:
bool CG_Request_Boss_Stage_StartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageStartResult& result, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18819); m << result; m << payback; return PhoneSend(remote,m); }
bool CG_Request_Boss_Stage_ClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageClearResult& result, const bool& flag, const LocalDestroyDiscovery& discovery, const bool& first, const EmptyItemResults& packageList) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18820); m << result; m << flag; m << discovery; m << first; m << packageList; return PhoneSend(remote,m); }
bool CG_Request_Boss_Stage_ContinueOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& items, const short& count, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18821); m << items; m << count; m << payback; return PhoneSend(remote,m); }
};
}
namespace SevenDSBoxC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestItemUseBoxOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBoxRequest& request) { return false; }
#define DECRMI_SevenDSBoxC2S_CG_RequestItemUseBoxOpen bool CG_RequestItemUseBoxOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBoxRequest& request) override
#define DEFRMI_SevenDSBoxC2S_CG_RequestItemUseBoxOpen(DerivedClass) bool DerivedClass::CG_RequestItemUseBoxOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBoxRequest& request)
};
}
namespace SevenDSBoxS2C {
class Proxy { public:
bool CG_RequestItemUseBoxOpenOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBoxResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14545); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSBulkGrowthC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinAwakenAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) { return false; }
#define DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinAwakenAtOnce bool CG_RequestSkinAwakenAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) override
#define DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinAwakenAtOnce(DerivedClass) bool DerivedClass::CG_RequestSkinAwakenAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request)
virtual bool CG_RequestSkinTranscendAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) { return false; }
#define DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinTranscendAtOnce bool CG_RequestSkinTranscendAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) override
#define DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinTranscendAtOnce(DerivedClass) bool DerivedClass::CG_RequestSkinTranscendAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request)
virtual bool CG_RequestSkinEvolutionAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) { return false; }
#define DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinEvolutionAtOnce bool CG_RequestSkinEvolutionAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) override
#define DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinEvolutionAtOnce(DerivedClass) bool DerivedClass::CG_RequestSkinEvolutionAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request)
virtual bool CG_RequestSkinOverEvolutionAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) { return false; }
#define DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinOverEvolutionAtOnce bool CG_RequestSkinOverEvolutionAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) override
#define DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinOverEvolutionAtOnce(DerivedClass) bool DerivedClass::CG_RequestSkinOverEvolutionAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request)
virtual bool CG_RequestSkinExclusiveSkillAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkPassiveRequest& request) { return false; }
#define DECRMI_SevenDSBulkGrowthC2S_CG_RequestSkinExclusiveSkillAtOnce bool CG_RequestSkinExclusiveSkillAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkPassiveRequest& request) override
#define DEFRMI_SevenDSBulkGrowthC2S_CG_RequestSkinExclusiveSkillAtOnce(DerivedClass) bool DerivedClass::CG_RequestSkinExclusiveSkillAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkPassiveRequest& request)
};
}
namespace SevenDSBulkGrowthS2C {
class Proxy { public:
bool CG_RequestSkinAwakenAtOnceOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBulkGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14138); m << result; return PhoneSend(remote,m); }
bool CG_RequestSkinTranscendAtOnceOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBulkGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14139); m << result; return PhoneSend(remote,m); }
bool CG_RequestSkinEvolutionAtOnceOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBulkGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14140); m << result; return PhoneSend(remote,m); }
bool CG_RequestSkinOverEvolutionAtOnceOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBulkGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14141); m << result; return PhoneSend(remote,m); }
bool CG_RequestSkinExclusiveSkillAtOnceOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBulkGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14142); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSBulkLevelC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinLevelUpAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) { return false; }
#define DECRMI_SevenDSBulkLevelC2S_CG_RequestSkinLevelUpAtOnce bool CG_RequestSkinLevelUpAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request) override
#define DEFRMI_SevenDSBulkLevelC2S_CG_RequestSkinLevelUpAtOnce(DerivedClass) bool DerivedClass::CG_RequestSkinLevelUpAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkLevelRequest& request)
};
}
namespace SevenDSBulkLevelS2C {
class Proxy { public:
bool CG_RequestSkinLevelUpAtOnceOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBulkLevelResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14137); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSBulkUltimateC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinSkillLevelUpAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkSkillRequest& request) { return false; }
#define DECRMI_SevenDSBulkUltimateC2S_CG_RequestSkinSkillLevelUpAtOnce bool CG_RequestSkinSkillLevelUpAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkSkillRequest& request) override
#define DEFRMI_SevenDSBulkUltimateC2S_CG_RequestSkinSkillLevelUpAtOnce(DerivedClass) bool DerivedClass::CG_RequestSkinSkillLevelUpAtOnce(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalBulkSkillRequest& request)
};
}
namespace SevenDSBulkUltimateS2C {
class Proxy { public:
bool CG_RequestSkinSkillLevelUpAtOnceOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBulkGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14136); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSCancelS2C {
class Proxy { public:
bool CG_CommonCancel(Proud::HostID remote, Proud::RmiContext& context, const LocalCancelResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14001); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSChapterC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestQuestChapterClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& region) { return false; }
#define DECRMI_SevenDSChapterC2S_CG_RequestQuestChapterClear bool CG_RequestQuestChapterClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& region) override
#define DEFRMI_SevenDSChapterC2S_CG_RequestQuestChapterClear(DerivedClass) bool DerivedClass::CG_RequestQuestChapterClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& region)
};
}
namespace SevenDSChapterS2C {
class Proxy { public:
bool CG_RequestQuestChapterClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalChapterResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14190); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSChapterSkipC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestItemUseChapterSkip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int32_t& skipID) { return false; }
#define DECRMI_SevenDSChapterSkipC2S_CG_RequestItemUseChapterSkip bool CG_RequestItemUseChapterSkip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int32_t& skipID) override
#define DEFRMI_SevenDSChapterSkipC2S_CG_RequestItemUseChapterSkip(DerivedClass) bool DerivedClass::CG_RequestItemUseChapterSkip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int32_t& skipID)
};
}
namespace SevenDSChapterSkipS2C {
class Proxy { public:
bool CG_RequestItemUseChapterSkipOK(Proud::HostID remote, Proud::RmiContext& context, const LocalChapterSkipResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14551); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSCoinShopC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCoinShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSCoinShopC2S_CG_RequestCoinShopInfo bool CG_RequestCoinShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSCoinShopC2S_CG_RequestCoinShopInfo(DerivedClass) bool DerivedClass::CG_RequestCoinShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestCoinShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCoinBuyRequest& request) { return false; }
#define DECRMI_SevenDSCoinShopC2S_CG_RequestCoinShopBuy bool CG_RequestCoinShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCoinBuyRequest& request) override
#define DEFRMI_SevenDSCoinShopC2S_CG_RequestCoinShopBuy(DerivedClass) bool DerivedClass::CG_RequestCoinShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCoinBuyRequest& request)
virtual bool CG_RequestEventCoinShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCoinBuyRequest& request) { return false; }
#define DECRMI_SevenDSCoinShopC2S_CG_RequestEventCoinShopBuy bool CG_RequestEventCoinShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCoinBuyRequest& request) override
#define DEFRMI_SevenDSCoinShopC2S_CG_RequestEventCoinShopBuy(DerivedClass) bool DerivedClass::CG_RequestEventCoinShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCoinBuyRequest& request)
};
}
namespace SevenDSCoinShopS2C {
class Proxy { public:
bool CG_RequestCoinShopInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalCoinShopInfo& info) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18518); m << info; return PhoneSend(remote,m); }
bool CG_RequestCoinShopBuyOK(Proud::HostID remote, Proud::RmiContext& context, const LocalCoinBuyResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18519); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSCookingC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCookingStart(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCookingRequest& request) { return false; }
#define DECRMI_SevenDSCookingC2S_CG_RequestCookingStart bool CG_RequestCookingStart(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCookingRequest& request) override
#define DEFRMI_SevenDSCookingC2S_CG_RequestCookingStart(DerivedClass) bool DerivedClass::CG_RequestCookingStart(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalCookingRequest& request)
};
}
namespace SevenDSCookingS2C {
class Proxy { public:
bool CG_RequestCookingStartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalCookingResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14229); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSCosmeticEquipC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCostumeEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costumeID, const int& targetHeroID) { return false; }
#define DECRMI_SevenDSCosmeticEquipC2S_CG_RequestCostumeEquip bool CG_RequestCostumeEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costumeID, const int& targetHeroID) override
#define DEFRMI_SevenDSCosmeticEquipC2S_CG_RequestCostumeEquip(DerivedClass) bool DerivedClass::CG_RequestCostumeEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costumeID, const int& targetHeroID)
virtual bool CG_RequestCostumeUnEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costumeID, const int& targetHeroID) { return false; }
#define DECRMI_SevenDSCosmeticEquipC2S_CG_RequestCostumeUnEquip bool CG_RequestCostumeUnEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costumeID, const int& targetHeroID) override
#define DEFRMI_SevenDSCosmeticEquipC2S_CG_RequestCostumeUnEquip(DerivedClass) bool DerivedClass::CG_RequestCostumeUnEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costumeID, const int& targetHeroID)
};
}
namespace SevenDSCosmeticEquipS2C {
class Proxy { public:
bool CG_RequestCostumeEquipOK(Proud::HostID remote, Proud::RmiContext& context, const LocalPassiveResult& userSkin) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14111); m << userSkin; return PhoneSend(remote,m); }
bool CG_RequestCostumeUnEquipOK(Proud::HostID remote, Proud::RmiContext& context, const LocalPassiveResult& userSkin) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14112); m << userSkin; return PhoneSend(remote,m); }
};
}
namespace SevenDSCosmeticShopC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCostumeShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSCosmeticShopC2S_CG_RequestCostumeShopInfo bool CG_RequestCostumeShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSCosmeticShopC2S_CG_RequestCostumeShopInfo(DerivedClass) bool DerivedClass::CG_RequestCostumeShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSCosmeticShopS2C {
class Proxy { public:
bool CG_RequestCostumeShopInfoOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& shopBuyInfoList, const EmptyItemResults& shopTimeItemInfoList) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18521); m << shopBuyInfoList; m << shopTimeItemInfoList; return PhoneSend(remote,m); }
};
}
namespace SevenDSCostumeC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCostumeUnLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const IntList& targetHeroIDList, const IntList& costumeGroupIDList, const IntList& targetHeroGroupIDList) { return false; }
#define DECRMI_SevenDSCostumeC2S_CG_RequestCostumeUnLock bool CG_RequestCostumeUnLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const IntList& targetHeroIDList, const IntList& costumeGroupIDList, const IntList& targetHeroGroupIDList) override
#define DEFRMI_SevenDSCostumeC2S_CG_RequestCostumeUnLock(DerivedClass) bool DerivedClass::CG_RequestCostumeUnLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const IntList& targetHeroIDList, const IntList& costumeGroupIDList, const IntList& targetHeroGroupIDList)
};
}
namespace SevenDSCostumeS2C {
class Proxy { public:
bool CG_RequestCostumeUnLockOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& getItemResultInfoList, const EmptyItemResults& updateSkinList, const EmptyItemResults& equipSkinList, const MissionResult& missionResult) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14113); m << getItemResultInfoList; m << updateSkinList; m << equipSkinList; m << missionResult; return PhoneSend(remote,m); }
};
}
namespace SevenDSDescentC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_Request_DescentBoss_EventStage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) { return false; }
#define DECRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Start bool CG_Request_DescentBoss_EventStage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) override
#define DEFRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Start(DerivedClass) bool DerivedClass::CG_Request_DescentBoss_EventStage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request)
virtual bool CG_Request_DescentBoss_EventStage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) { return false; }
#define DECRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Clear bool CG_Request_DescentBoss_EventStage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) override
#define DEFRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Clear(DerivedClass) bool DerivedClass::CG_Request_DescentBoss_EventStage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request)
virtual bool CG_Request_DescentBoss_EventStage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Continue bool CG_Request_DescentBoss_EventStage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSDescentC2S_CG_Request_DescentBoss_EventStage_Continue(DerivedClass) bool DerivedClass::CG_Request_DescentBoss_EventStage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_Request_DescentBoss_Event_Point_Reward(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSEQ, const int& step) { return false; }
#define DECRMI_SevenDSDescentC2S_CG_Request_DescentBoss_Event_Point_Reward bool CG_Request_DescentBoss_Event_Point_Reward(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSEQ, const int& step) override
#define DEFRMI_SevenDSDescentC2S_CG_Request_DescentBoss_Event_Point_Reward(DerivedClass) bool DerivedClass::CG_Request_DescentBoss_Event_Point_Reward(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSEQ, const int& step)
};
}
namespace SevenDSDescentS2C {
class Proxy { public:
bool CG_Request_DescentBoss_EventStage_StartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageStartResult& result, const EmptyItemResults& extra, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18957); m << result; m << extra; m << payback; return PhoneSend(remote,m); }
bool CG_Request_DescentBoss_EventStage_ClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageClearResult& result, const LocalDescentInfo& info, const EmptyItemResults& progress, const int& next, const int& points) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18958); m << result; m << info; m << progress; m << next; m << points; return PhoneSend(remote,m); }
bool CG_Request_DescentBoss_EventStage_ContinueOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& items, const int16& count, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18959); m << items; m << count; m << payback; return PhoneSend(remote,m); }
bool CG_Request_DescentBoss_Event_Point_RewardOK(Proud::HostID remote, Proud::RmiContext& context, const LocalDescentRewardResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18960); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSDevelopmentC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinLevelUpBySkinMaterial(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalLevelUpRequest& request) { return false; }
#define DECRMI_SevenDSDevelopmentC2S_CG_RequestSkinLevelUpBySkinMaterial bool CG_RequestSkinLevelUpBySkinMaterial(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalLevelUpRequest& request) override
#define DEFRMI_SevenDSDevelopmentC2S_CG_RequestSkinLevelUpBySkinMaterial(DerivedClass) bool DerivedClass::CG_RequestSkinLevelUpBySkinMaterial(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalLevelUpRequest& request)
virtual bool Reserved02(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSDevelopmentC2S_Reserved02 bool Reserved02(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSDevelopmentC2S_Reserved02(DerivedClass) bool DerivedClass::Reserved02(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool Reserved03(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSDevelopmentC2S_Reserved03 bool Reserved03(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSDevelopmentC2S_Reserved03(DerivedClass) bool DerivedClass::Reserved03(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool Reserved04(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSDevelopmentC2S_Reserved04 bool Reserved04(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSDevelopmentC2S_Reserved04(DerivedClass) bool DerivedClass::Reserved04(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestSkinAwaken(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& awaken) { return false; }
#define DECRMI_SevenDSDevelopmentC2S_CG_RequestSkinAwaken bool CG_RequestSkinAwaken(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& awaken) override
#define DEFRMI_SevenDSDevelopmentC2S_CG_RequestSkinAwaken(DerivedClass) bool DerivedClass::CG_RequestSkinAwaken(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& awaken)
};
}
namespace SevenDSDevelopmentS2C {
class Proxy { public:
bool CG_RequestSkinLevelUpBySkinMaterialOK(Proud::HostID remote, Proud::RmiContext& context, const LocalLevelUpResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14101); m << result; return PhoneSend(remote,m); }
bool Reserved02(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14102); return PhoneSend(remote,m); }
bool Reserved03(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14103); return PhoneSend(remote,m); }
bool Reserved04(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14104); return PhoneSend(remote,m); }
bool CG_RequestSkinAwakenOK(Proud::HostID remote, Proud::RmiContext& context, const LocalAwakenResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14105); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSEquipmentC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestWeaponEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const int& serial, const int& slot, const bool& remove) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquip bool CG_RequestWeaponEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const int& serial, const int& slot, const bool& remove) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquip(DerivedClass) bool DerivedClass::CG_RequestWeaponEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const int& serial, const int& slot, const bool& remove)
virtual bool CG_RequestWeaponUnEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const int& slot) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponUnEquip bool CG_RequestWeaponUnEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const int& slot) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponUnEquip(DerivedClass) bool DerivedClass::CG_RequestWeaponUnEquip(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const int& slot)
virtual bool CG_RequestWeaponSell(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalIntListRequest& request, const int& sellType, const int& basepoint) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponSell bool CG_RequestWeaponSell(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalIntListRequest& request, const int& sellType, const int& basepoint) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponSell(DerivedClass) bool DerivedClass::CG_RequestWeaponSell(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalIntListRequest& request, const int& sellType, const int& basepoint)
virtual bool CG_RequestWeaponGrind(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalIntListRequest& request) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponGrind bool CG_RequestWeaponGrind(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalIntListRequest& request) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponGrind(DerivedClass) bool DerivedClass::CG_RequestWeaponGrind(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalIntListRequest& request)
virtual bool CG_RequestWeaponUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int16& gauge) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponUpgrade bool CG_RequestWeaponUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int16& gauge) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponUpgrade(DerivedClass) bool DerivedClass::CG_RequestWeaponUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int16& gauge)
virtual bool CG_RequestWeaponUpgradeRetry(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& item) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponUpgradeRetry bool CG_RequestWeaponUpgradeRetry(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& item) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponUpgradeRetry(DerivedClass) bool DerivedClass::CG_RequestWeaponUpgradeRetry(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& item)
virtual bool CG_RequestWeaponEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEvolution bool CG_RequestWeaponEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEvolution(DerivedClass) bool DerivedClass::CG_RequestWeaponEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial)
virtual bool CG_RequestWeaponEvolutionRetry(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& slot, const int& item) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEvolutionRetry bool CG_RequestWeaponEvolutionRetry(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& slot, const int& item) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEvolutionRetry(DerivedClass) bool DerivedClass::CG_RequestWeaponEvolutionRetry(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& slot, const int& item)
virtual bool CG_RequestWeaponOptionEnhance(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& slot, const uint8& enhanceType) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponOptionEnhance bool CG_RequestWeaponOptionEnhance(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& slot, const uint8& enhanceType) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponOptionEnhance(DerivedClass) bool DerivedClass::CG_RequestWeaponOptionEnhance(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const int& slot, const uint8& enhanceType)
virtual bool CG_RequestWeaponLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponLock bool CG_RequestWeaponLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponLock(DerivedClass) bool DerivedClass::CG_RequestWeaponLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial)
virtual bool CG_RequestWeaponUnLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponUnLock bool CG_RequestWeaponUnLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponUnLock(DerivedClass) bool DerivedClass::CG_RequestWeaponUnLock(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial)
virtual bool CG_RequestWeaponEquipExchange(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& pickedSerial, const int& pickedSkin, const int& targetSerial, const int& targetSkin, const int& slot, const bool& remove) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipExchange bool CG_RequestWeaponEquipExchange(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& pickedSerial, const int& pickedSkin, const int& targetSerial, const int& targetSkin, const int& slot, const bool& remove) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipExchange(DerivedClass) bool DerivedClass::CG_RequestWeaponEquipExchange(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& pickedSerial, const int& pickedSkin, const int& targetSerial, const int& targetSkin, const int& slot, const bool& remove)
virtual bool CG_RequestWeaponEquipExchangeAll(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetSkin, const int& sourceSkin, const int& mode) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipExchangeAll bool CG_RequestWeaponEquipExchangeAll(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetSkin, const int& sourceSkin, const int& mode) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipExchangeAll(DerivedClass) bool DerivedClass::CG_RequestWeaponEquipExchangeAll(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetSkin, const int& sourceSkin, const int& mode)
virtual bool CG_RequestWeaponEquipRecommend(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const LocalIntListRequest& request) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipRecommend bool CG_RequestWeaponEquipRecommend(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const LocalIntListRequest& request) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponEquipRecommend(DerivedClass) bool DerivedClass::CG_RequestWeaponEquipRecommend(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin, const LocalIntListRequest& request)
virtual bool CG_RequestWeaponCarve(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSeq, const int& serial, const uint8& heroGroup) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponCarve bool CG_RequestWeaponCarve(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSeq, const int& serial, const uint8& heroGroup) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponCarve(DerivedClass) bool DerivedClass::CG_RequestWeaponCarve(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSeq, const int& serial, const uint8& heroGroup)
virtual bool CG_RequestWeaponCarveRemove(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSeq, const int& serial) { return false; }
#define DECRMI_SevenDSEquipmentC2S_CG_RequestWeaponCarveRemove bool CG_RequestWeaponCarveRemove(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSeq, const int& serial) override
#define DEFRMI_SevenDSEquipmentC2S_CG_RequestWeaponCarveRemove(DerivedClass) bool DerivedClass::CG_RequestWeaponCarveRemove(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& eventSeq, const int& serial)
};
}
namespace SevenDSEquipmentS2C {
class Proxy { public:
bool CG_RequestWeaponEquipOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19400); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponUnEquipOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19401); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponSellOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19402); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponGrindOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19403); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponUpgradeOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19404); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponUpgradeRetryOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19405); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponEvolutionOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19406); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponEvolutionRetryOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19407); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponOptionEnhanceOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19408); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponLockOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19409); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponUnLockOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19410); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponEquipExchangeOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19411); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponEquipExchangeAllOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19412); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponEquipRecommendOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19413); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponCarveOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19414); m << result; return PhoneSend(remote,m); }
bool CG_RequestWeaponCarveRemoveOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(19415); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSEquipmentTicketC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestItemUseWeaponTicket(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& item, const int& selected) { return false; }
#define DECRMI_SevenDSEquipmentTicketC2S_CG_RequestItemUseWeaponTicket bool CG_RequestItemUseWeaponTicket(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& item, const int& selected) override
#define DEFRMI_SevenDSEquipmentTicketC2S_CG_RequestItemUseWeaponTicket(DerivedClass) bool DerivedClass::CG_RequestItemUseWeaponTicket(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& item, const int& selected)
};
}
namespace SevenDSEquipmentTicketS2C {
class Proxy { public:
bool CG_RequestItemUseWeaponTicketOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14548); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSEventCoinS2C {
class Proxy { public:
bool CG_RequestEventCoinShopBuyOK(Proud::HostID remote, Proud::RmiContext& context, const LocalCoinBuyResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18574); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSEvolutionC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) { return false; }
#define DECRMI_SevenDSEvolutionC2S_CG_RequestSkinEvolution bool CG_RequestSkinEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) override
#define DEFRMI_SevenDSEvolutionC2S_CG_RequestSkinEvolution(DerivedClass) bool DerivedClass::CG_RequestSkinEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID)
virtual bool CG_RequestSkinSkillLevelUp(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID, const uint8& skillLevelUpCount) { return false; }
#define DECRMI_SevenDSEvolutionC2S_CG_RequestSkinSkillLevelUp bool CG_RequestSkinSkillLevelUp(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID, const uint8& skillLevelUpCount) override
#define DEFRMI_SevenDSEvolutionC2S_CG_RequestSkinSkillLevelUp(DerivedClass) bool DerivedClass::CG_RequestSkinSkillLevelUp(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID, const uint8& skillLevelUpCount)
};
}
namespace SevenDSEvolutionS2C {
class Proxy { public:
bool CG_RequestSkinEvolutionOK(Proud::HostID remote, Proud::RmiContext& context, const LocalEvolutionResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14107); m << result; return PhoneSend(remote,m); }
bool CG_RequestSkinSkillLevelUpOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSkillResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14108); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSFinalBossC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_Request_FinalBoss_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) { return false; }
#define DECRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Start bool CG_Request_FinalBoss_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) override
#define DEFRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Start(DerivedClass) bool DerivedClass::CG_Request_FinalBoss_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request)
virtual bool CG_Request_FinalBoss_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) { return false; }
#define DECRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Clear bool CG_Request_FinalBoss_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) override
#define DEFRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Clear(DerivedClass) bool DerivedClass::CG_Request_FinalBoss_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request)
virtual bool CG_Request_FinalBoss_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Continue bool CG_Request_FinalBoss_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Stage_Continue(DerivedClass) bool DerivedClass::CG_Request_FinalBoss_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_Request_FinalBoss_Season_Info(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Season_Info bool CG_Request_FinalBoss_Season_Info(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSFinalBossC2S_CG_Request_FinalBoss_Season_Info(DerivedClass) bool DerivedClass::CG_Request_FinalBoss_Season_Info(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSFinalBossRankC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_Request_FinalBoss_Season_Rank_Info(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& seasonID, const int& bossGroupID) { return false; }
#define DECRMI_SevenDSFinalBossRankC2S_CG_Request_FinalBoss_Season_Rank_Info bool CG_Request_FinalBoss_Season_Rank_Info(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& seasonID, const int& bossGroupID) override
#define DEFRMI_SevenDSFinalBossRankC2S_CG_Request_FinalBoss_Season_Rank_Info(DerivedClass) bool DerivedClass::CG_Request_FinalBoss_Season_Rank_Info(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& seasonID, const int& bossGroupID)
};
}
namespace SevenDSFinalBossRankS2C {
class Proxy { public:
bool CG_Request_FinalBoss_Season_Rank_InfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalFinalBossRank& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18903); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSFinalBossS2C {
class Proxy { public:
bool CG_Request_FinalBoss_Stage_StartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageStartResult& result, const EmptyItemResults& events, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18899); m << result; m << events; m << payback; return PhoneSend(remote,m); }
bool CG_Request_FinalBoss_Stage_ClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageClearResult& result, const LocalFinalBossClearExtra& extra) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18900); m << result; m << extra; return PhoneSend(remote,m); }
bool CG_Request_FinalBoss_Stage_ContinueOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& costs, const int16& count, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18901); m << costs; m << count; m << payback; return PhoneSend(remote,m); }
bool CG_Request_FinalBoss_Season_InfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalFinalBossInfo& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18902); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSFinalBossShopC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestFinalBossShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSFinalBossShopC2S_CG_RequestFinalBossShopInfo bool CG_RequestFinalBossShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSFinalBossShopC2S_CG_RequestFinalBossShopInfo(DerivedClass) bool DerivedClass::CG_RequestFinalBossShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestFinalBossShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& season, const int& product, const uint8& count) { return false; }
#define DECRMI_SevenDSFinalBossShopC2S_CG_RequestFinalBossShopBuy bool CG_RequestFinalBossShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& season, const int& product, const uint8& count) override
#define DEFRMI_SevenDSFinalBossShopC2S_CG_RequestFinalBossShopBuy(DerivedClass) bool DerivedClass::CG_RequestFinalBossShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& season, const int& product, const uint8& count)
};
}
namespace SevenDSFinalBossShopS2C {
class Proxy { public:
bool CG_RequestFinalBossShopInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalFinalBossShopInfo& info) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18556); m << info; return PhoneSend(remote,m); }
bool CG_RequestFinalBossShopBuyOK(Proud::HostID remote, Proud::RmiContext& context, const LocalFinalBossShopBuy& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18557); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSFoodAutoC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestFoodBuffAutoUseOnOff(Proud::HostID remote, Proud::RmiContext& rmiContext, const bool& isAutoUse) { return false; }
#define DECRMI_SevenDSFoodAutoC2S_CG_RequestFoodBuffAutoUseOnOff bool CG_RequestFoodBuffAutoUseOnOff(Proud::HostID remote, Proud::RmiContext& rmiContext, const bool& isAutoUse) override
#define DEFRMI_SevenDSFoodAutoC2S_CG_RequestFoodBuffAutoUseOnOff(DerivedClass) bool DerivedClass::CG_RequestFoodBuffAutoUseOnOff(Proud::HostID remote, Proud::RmiContext& rmiContext, const bool& isAutoUse)
};
}
namespace SevenDSFoodAutoS2C {
class Proxy { public:
bool CG_RequestFoodBuffAutoUseOnOffOK(Proud::HostID remote, Proud::RmiContext& context, const LocalFoodResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14543); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSFoodC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCookingUseCookingBuff(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& foodItemID, const bool& isAutoUse) { return false; }
#define DECRMI_SevenDSFoodC2S_CG_RequestCookingUseCookingBuff bool CG_RequestCookingUseCookingBuff(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& foodItemID, const bool& isAutoUse) override
#define DEFRMI_SevenDSFoodC2S_CG_RequestCookingUseCookingBuff(DerivedClass) bool DerivedClass::CG_RequestCookingUseCookingBuff(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& foodItemID, const bool& isAutoUse)
};
}
namespace SevenDSFoodS2C {
class Proxy { public:
bool CG_RequestCookingUseCookingBuffOK(Proud::HostID remote, Proud::RmiContext& context, const LocalFoodResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14236); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSFortCoinC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestWeekStageCoinOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalFortCoinOpenRequest& request) { return false; }
#define DECRMI_SevenDSFortCoinC2S_CG_RequestWeekStageCoinOpen bool CG_RequestWeekStageCoinOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalFortCoinOpenRequest& request) override
#define DEFRMI_SevenDSFortCoinC2S_CG_RequestWeekStageCoinOpen(DerivedClass) bool DerivedClass::CG_RequestWeekStageCoinOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalFortCoinOpenRequest& request)
};
}
namespace SevenDSFortCoinS2C {
class Proxy { public:
bool CG_RequestWeekStageCoinOpenOK(Proud::HostID remote, Proud::RmiContext& context, const int& area, const int& remaining, const int& reset, const int& opened, const EmptyItemResults& items) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18961); m << area; m << remaining; m << reset; m << opened; m << items; return PhoneSend(remote,m); }
};
}
namespace SevenDSFortKeyC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestWeekStageKeyOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& area, const uint8& count) { return false; }
#define DECRMI_SevenDSFortKeyC2S_CG_RequestWeekStageKeyOpen bool CG_RequestWeekStageKeyOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& area, const uint8& count) override
#define DEFRMI_SevenDSFortKeyC2S_CG_RequestWeekStageKeyOpen(DerivedClass) bool DerivedClass::CG_RequestWeekStageKeyOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& area, const uint8& count)
};
}
namespace SevenDSFortKeyS2C {
class Proxy { public:
bool CG_RequestWeekStageKeyOpenOK(Proud::HostID remote, Proud::RmiContext& context, const int& area, const uint8& count, const int& remaining, const LocalNoItem& item, const MissionResult& mission) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18978); m << area; m << count; m << remaining; m << item; m << mission; return PhoneSend(remote,m); }
};
}
namespace SevenDSGachaBuyC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestGambleShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const GambleShopBuyRequest& gambleRequest) { return false; }
#define DECRMI_SevenDSGachaBuyC2S_CG_RequestGambleShopBuy bool CG_RequestGambleShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const GambleShopBuyRequest& gambleRequest) override
#define DEFRMI_SevenDSGachaBuyC2S_CG_RequestGambleShopBuy(DerivedClass) bool DerivedClass::CG_RequestGambleShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const GambleShopBuyRequest& gambleRequest)
};
}
namespace SevenDSGachaBuyS2C {
class Proxy { public:
bool CG_RequestGambleShopBuyOK(Proud::HostID remote, Proud::RmiContext& context, const GambleShopBuyResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18506); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSGachaItemC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestItemGambleShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGachaItemC2S_CG_RequestItemGambleShopInfo bool CG_RequestItemGambleShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGachaItemC2S_CG_RequestItemGambleShopInfo(DerivedClass) bool DerivedClass::CG_RequestItemGambleShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSGachaItemS2C {
class Proxy { public:
bool CG_RequestItemGambleShopInfoOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& buyInfoList, const int& remainSec) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18507); m << buyInfoList; m << remainSec; return PhoneSend(remote,m); }
};
}
namespace SevenDSGachaShopC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestGambleShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& gambleType, const GambleChecksumList& gambleCheckSumInfoList) { return false; }
#define DECRMI_SevenDSGachaShopC2S_CG_RequestGambleShopInfo bool CG_RequestGambleShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& gambleType, const GambleChecksumList& gambleCheckSumInfoList) override
#define DEFRMI_SevenDSGachaShopC2S_CG_RequestGambleShopInfo(DerivedClass) bool DerivedClass::CG_RequestGambleShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& gambleType, const GambleChecksumList& gambleCheckSumInfoList)
};
}
namespace SevenDSGachaShopS2C {
class Proxy { public:
bool CG_RequestGambleShopInfoOK(Proud::HostID remote, Proud::RmiContext& context, const GambleShopInfo& gambleShopInfo, const GambleTimeSwitchLobbyInfo& gambleTimeSwitchLobbyInfo) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18528); m << gambleShopInfo; m << gambleTimeSwitchLobbyInfo; return PhoneSend(remote,m); }
};
}
namespace SevenDSGameC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool ReservedRequest01(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest01 bool ReservedRequest01(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest01(DerivedClass) bool DerivedClass::ReservedRequest01(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest02(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest02 bool ReservedRequest02(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest02(DerivedClass) bool DerivedClass::ReservedRequest02(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest03(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest03 bool ReservedRequest03(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest03(DerivedClass) bool DerivedClass::ReservedRequest03(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool CG_RequestTeamInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& teamIndex) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestTeamInfo bool CG_RequestTeamInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& teamIndex) override
#define DEFRMI_SevenDSGameC2S_CG_RequestTeamInfo(DerivedClass) bool DerivedClass::CG_RequestTeamInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& teamIndex)
virtual bool CG_RequestTeamSlotChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTeamChange& request) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestTeamSlotChange bool CG_RequestTeamSlotChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTeamChange& request) override
#define DEFRMI_SevenDSGameC2S_CG_RequestTeamSlotChange(DerivedClass) bool DerivedClass::CG_RequestTeamSlotChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTeamChange& request)
virtual bool ReservedRequest06(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest06 bool ReservedRequest06(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest06(DerivedClass) bool DerivedClass::ReservedRequest06(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool CG_RequestLobbyInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestLobbyInfo bool CG_RequestLobbyInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_CG_RequestLobbyInfo(DerivedClass) bool DerivedClass::CG_RequestLobbyInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest08(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest08 bool ReservedRequest08(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest08(DerivedClass) bool DerivedClass::ReservedRequest08(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool CG_RequestMercenaryList(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestMercenaryList bool CG_RequestMercenaryList(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_CG_RequestMercenaryList(DerivedClass) bool DerivedClass::CG_RequestMercenaryList(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest10(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest10 bool ReservedRequest10(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest10(DerivedClass) bool DerivedClass::ReservedRequest10(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest11(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest11 bool ReservedRequest11(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest11(DerivedClass) bool DerivedClass::ReservedRequest11(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest12(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest12 bool ReservedRequest12(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest12(DerivedClass) bool DerivedClass::ReservedRequest12(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest13(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest13 bool ReservedRequest13(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest13(DerivedClass) bool DerivedClass::ReservedRequest13(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest14(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest14 bool ReservedRequest14(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest14(DerivedClass) bool DerivedClass::ReservedRequest14(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool CG_RequestEventList(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestEventList bool CG_RequestEventList(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_CG_RequestEventList(DerivedClass) bool DerivedClass::CG_RequestEventList(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest16(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest16 bool ReservedRequest16(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest16(DerivedClass) bool DerivedClass::ReservedRequest16(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest17(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest17 bool ReservedRequest17(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest17(DerivedClass) bool DerivedClass::ReservedRequest17(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest18(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest18 bool ReservedRequest18(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest18(DerivedClass) bool DerivedClass::ReservedRequest18(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest19(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest19 bool ReservedRequest19(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest19(DerivedClass) bool DerivedClass::ReservedRequest19(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest20(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest20 bool ReservedRequest20(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest20(DerivedClass) bool DerivedClass::ReservedRequest20(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest21(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest21 bool ReservedRequest21(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest21(DerivedClass) bool DerivedClass::ReservedRequest21(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest22(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest22 bool ReservedRequest22(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest22(DerivedClass) bool DerivedClass::ReservedRequest22(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest23(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest23 bool ReservedRequest23(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest23(DerivedClass) bool DerivedClass::ReservedRequest23(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool CG_RequestServerVersion(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestServerVersion bool CG_RequestServerVersion(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_CG_RequestServerVersion(DerivedClass) bool DerivedClass::CG_RequestServerVersion(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest25(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest25 bool ReservedRequest25(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest25(DerivedClass) bool DerivedClass::ReservedRequest25(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest26(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest26 bool ReservedRequest26(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest26(DerivedClass) bool DerivedClass::ReservedRequest26(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest27(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest27 bool ReservedRequest27(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest27(DerivedClass) bool DerivedClass::ReservedRequest27(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest28(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest28 bool ReservedRequest28(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest28(DerivedClass) bool DerivedClass::ReservedRequest28(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest29(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest29 bool ReservedRequest29(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest29(DerivedClass) bool DerivedClass::ReservedRequest29(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest30(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest30 bool ReservedRequest30(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest30(DerivedClass) bool DerivedClass::ReservedRequest30(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest31(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest31 bool ReservedRequest31(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest31(DerivedClass) bool DerivedClass::ReservedRequest31(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest32(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest32 bool ReservedRequest32(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest32(DerivedClass) bool DerivedClass::ReservedRequest32(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest33(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest33 bool ReservedRequest33(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest33(DerivedClass) bool DerivedClass::ReservedRequest33(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest34(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest34 bool ReservedRequest34(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest34(DerivedClass) bool DerivedClass::ReservedRequest34(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest35(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest35 bool ReservedRequest35(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest35(DerivedClass) bool DerivedClass::ReservedRequest35(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest36(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest36 bool ReservedRequest36(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest36(DerivedClass) bool DerivedClass::ReservedRequest36(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest37(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest37 bool ReservedRequest37(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest37(DerivedClass) bool DerivedClass::ReservedRequest37(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest38(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest38 bool ReservedRequest38(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest38(DerivedClass) bool DerivedClass::ReservedRequest38(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest39(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest39 bool ReservedRequest39(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest39(DerivedClass) bool DerivedClass::ReservedRequest39(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest40(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest40 bool ReservedRequest40(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest40(DerivedClass) bool DerivedClass::ReservedRequest40(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest41(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest41 bool ReservedRequest41(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest41(DerivedClass) bool DerivedClass::ReservedRequest41(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest42(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest42 bool ReservedRequest42(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest42(DerivedClass) bool DerivedClass::ReservedRequest42(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest43(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest43 bool ReservedRequest43(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest43(DerivedClass) bool DerivedClass::ReservedRequest43(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest44(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest44 bool ReservedRequest44(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest44(DerivedClass) bool DerivedClass::ReservedRequest44(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest45(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest45 bool ReservedRequest45(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest45(DerivedClass) bool DerivedClass::ReservedRequest45(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest46(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest46 bool ReservedRequest46(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest46(DerivedClass) bool DerivedClass::ReservedRequest46(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest47(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest47 bool ReservedRequest47(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest47(DerivedClass) bool DerivedClass::ReservedRequest47(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest48(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest48 bool ReservedRequest48(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest48(DerivedClass) bool DerivedClass::ReservedRequest48(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest49(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest49 bool ReservedRequest49(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest49(DerivedClass) bool DerivedClass::ReservedRequest49(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool ReservedRequest50(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest50 bool ReservedRequest50(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest50(DerivedClass) bool DerivedClass::ReservedRequest50(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool CG_RequestSecurityToken(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestSecurityToken bool CG_RequestSecurityToken(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_CG_RequestSecurityToken(DerivedClass) bool DerivedClass::CG_RequestSecurityToken(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestNetmarbleAuth(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestNetmarbleAuth bool CG_RequestNetmarbleAuth(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_CG_RequestNetmarbleAuth(DerivedClass) bool DerivedClass::CG_RequestNetmarbleAuth(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestAuthenticateCreate(Proud::HostID remote, Proud::RmiContext& rmiContext, const Proud::String& netmarblePlayerID, const NetmarbleSDKInfo& sdkInfo) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestAuthenticateCreate bool CG_RequestAuthenticateCreate(Proud::HostID remote, Proud::RmiContext& rmiContext, const Proud::String& netmarblePlayerID, const NetmarbleSDKInfo& sdkInfo) override
#define DEFRMI_SevenDSGameC2S_CG_RequestAuthenticateCreate(DerivedClass) bool DerivedClass::CG_RequestAuthenticateCreate(Proud::HostID remote, Proud::RmiContext& rmiContext, const Proud::String& netmarblePlayerID, const NetmarbleSDKInfo& sdkInfo)
virtual bool ReservedRequest54(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest54 bool ReservedRequest54(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest54(DerivedClass) bool DerivedClass::ReservedRequest54(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& value)
virtual bool CG_RequestLogin(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestLogin bool CG_RequestLogin(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_CG_RequestLogin(DerivedClass) bool DerivedClass::CG_RequestLogin(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestLoginInstantly(Proud::HostID remote, Proud::RmiContext& rmiContext, const int64& usn, const NetmarbleSDKInfo& sdkInfo, const int& sessionKey, const VersionInfo& versionInfo, const Proud::String& rejoinData, const int64& clientTimeTick, const int& reconnectRequestRmiID, const uint8& languageType, const int& talkChannelID, const int& buildCountry) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestLoginInstantly bool CG_RequestLoginInstantly(Proud::HostID remote, Proud::RmiContext& rmiContext, const int64& usn, const NetmarbleSDKInfo& sdkInfo, const int& sessionKey, const VersionInfo& versionInfo, const Proud::String& rejoinData, const int64& clientTimeTick, const int& reconnectRequestRmiID, const uint8& languageType, const int& talkChannelID, const int& buildCountry) override
#define DEFRMI_SevenDSGameC2S_CG_RequestLoginInstantly(DerivedClass) bool DerivedClass::CG_RequestLoginInstantly(Proud::HostID remote, Proud::RmiContext& rmiContext, const int64& usn, const NetmarbleSDKInfo& sdkInfo, const int& sessionKey, const VersionInfo& versionInfo, const Proud::String& rejoinData, const int64& clientTimeTick, const int& reconnectRequestRmiID, const uint8& languageType, const int& talkChannelID, const int& buildCountry)
virtual bool ReservedRequest57(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest57 bool ReservedRequest57(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest57(DerivedClass) bool DerivedClass::ReservedRequest57(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest58(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest58 bool ReservedRequest58(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest58(DerivedClass) bool DerivedClass::ReservedRequest58(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest59(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest59 bool ReservedRequest59(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest59(DerivedClass) bool DerivedClass::ReservedRequest59(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest60(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest60 bool ReservedRequest60(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest60(DerivedClass) bool DerivedClass::ReservedRequest60(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest61(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest61 bool ReservedRequest61(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest61(DerivedClass) bool DerivedClass::ReservedRequest61(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest62(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest62 bool ReservedRequest62(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest62(DerivedClass) bool DerivedClass::ReservedRequest62(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest63(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest63 bool ReservedRequest63(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest63(DerivedClass) bool DerivedClass::ReservedRequest63(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest64(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest64 bool ReservedRequest64(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest64(DerivedClass) bool DerivedClass::ReservedRequest64(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest65(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest65 bool ReservedRequest65(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest65(DerivedClass) bool DerivedClass::ReservedRequest65(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest66(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest66 bool ReservedRequest66(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest66(DerivedClass) bool DerivedClass::ReservedRequest66(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest67(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest67 bool ReservedRequest67(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest67(DerivedClass) bool DerivedClass::ReservedRequest67(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest68(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest68 bool ReservedRequest68(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest68(DerivedClass) bool DerivedClass::ReservedRequest68(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest69(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest69 bool ReservedRequest69(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest69(DerivedClass) bool DerivedClass::ReservedRequest69(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest70(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest70 bool ReservedRequest70(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest70(DerivedClass) bool DerivedClass::ReservedRequest70(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest71(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest71 bool ReservedRequest71(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest71(DerivedClass) bool DerivedClass::ReservedRequest71(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest72(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest72 bool ReservedRequest72(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest72(DerivedClass) bool DerivedClass::ReservedRequest72(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool ReservedRequest73(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGameC2S_ReservedRequest73 bool ReservedRequest73(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGameC2S_ReservedRequest73(DerivedClass) bool DerivedClass::ReservedRequest73(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestBillingCouponVerify(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& verifyType) { return false; }
#define DECRMI_SevenDSGameC2S_CG_RequestBillingCouponVerify bool CG_RequestBillingCouponVerify(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& verifyType) override
#define DEFRMI_SevenDSGameC2S_CG_RequestBillingCouponVerify(DerivedClass) bool DerivedClass::CG_RequestBillingCouponVerify(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& verifyType)
};
}
namespace SevenDSGameS2C {
class Proxy { public:
bool ReservedResponse01(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14001); m << value; return PhoneSend(remote,m); }
bool ReservedResponse02(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14002); m << value; return PhoneSend(remote,m); }
bool ReservedResponse03(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14003); m << value; return PhoneSend(remote,m); }
bool CG_RequestTeamInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalTeamInfo& team) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14004); m << team; return PhoneSend(remote,m); }
bool ReservedResponse05(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14005); m << value; return PhoneSend(remote,m); }
bool ReservedResponse06(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14006); m << value; return PhoneSend(remote,m); }
bool ReservedResponse07(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14007); m << value; return PhoneSend(remote,m); }
bool ReservedResponse08(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14008); m << value; return PhoneSend(remote,m); }
bool ReservedResponse09(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14009); m << value; return PhoneSend(remote,m); }
bool CG_RequestTeamSlotChangeOK(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14010); return PhoneSend(remote,m); }
bool ReservedResponse11(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14011); m << value; return PhoneSend(remote,m); }
bool CG_RequestLobbyInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LobbyInfo& lobbyInfo, const MissionResult& missionResult, const EmptyItemResults& deleteItemResultInfoList, const LoginServiceInfo& loginServiceInfo) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14012); m << lobbyInfo; m << missionResult; m << deleteItemResultInfoList; m << loginServiceInfo; return PhoneSend(remote,m); }
bool ReservedResponse13(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14013); m << value; return PhoneSend(remote,m); }
bool ReservedResponse14(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14014); m << value; return PhoneSend(remote,m); }
bool ReservedResponse15(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14015); m << value; return PhoneSend(remote,m); }
bool ReservedResponse16(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14016); m << value; return PhoneSend(remote,m); }
bool ReservedResponse17(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14017); m << value; return PhoneSend(remote,m); }
bool ReservedResponse18(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14018); m << value; return PhoneSend(remote,m); }
bool CG_RequestEventListOK(Proud::HostID remote, Proud::RmiContext& context, const EventPacketInfo& eventPacketInfo) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14019); m << eventPacketInfo; return PhoneSend(remote,m); }
bool ReservedResponse20(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14020); m << value; return PhoneSend(remote,m); }
bool ReservedResponse21(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14021); m << value; return PhoneSend(remote,m); }
bool ReservedResponse22(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14022); m << value; return PhoneSend(remote,m); }
bool ReservedResponse23(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14023); m << value; return PhoneSend(remote,m); }
bool ReservedResponse24(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14024); m << value; return PhoneSend(remote,m); }
bool ReservedResponse25(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14025); m << value; return PhoneSend(remote,m); }
bool ReservedResponse26(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14026); m << value; return PhoneSend(remote,m); }
bool ReservedResponse27(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14027); m << value; return PhoneSend(remote,m); }
bool ReservedResponse28(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14028); m << value; return PhoneSend(remote,m); }
bool ReservedResponse29(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14029); m << value; return PhoneSend(remote,m); }
bool CG_RequestServerVersionOK(Proud::HostID remote, Proud::RmiContext& context, const Proud::String& serverVersionInfo) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14030); m << serverVersionInfo; return PhoneSend(remote,m); }
bool ReservedResponse31(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14031); m << value; return PhoneSend(remote,m); }
bool ReservedResponse32(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14032); m << value; return PhoneSend(remote,m); }
bool ReservedResponse33(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14033); m << value; return PhoneSend(remote,m); }
bool ReservedResponse34(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14034); m << value; return PhoneSend(remote,m); }
bool ReservedResponse35(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14035); m << value; return PhoneSend(remote,m); }
bool ReservedResponse36(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14036); m << value; return PhoneSend(remote,m); }
bool ReservedResponse37(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14037); m << value; return PhoneSend(remote,m); }
bool ReservedResponse38(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14038); m << value; return PhoneSend(remote,m); }
bool ReservedResponse39(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14039); m << value; return PhoneSend(remote,m); }
bool ReservedResponse40(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14040); m << value; return PhoneSend(remote,m); }
bool ReservedResponse41(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14041); m << value; return PhoneSend(remote,m); }
bool ReservedResponse42(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14042); m << value; return PhoneSend(remote,m); }
bool ReservedResponse43(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14043); m << value; return PhoneSend(remote,m); }
bool ReservedResponse44(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14044); m << value; return PhoneSend(remote,m); }
bool ReservedResponse45(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14045); m << value; return PhoneSend(remote,m); }
bool ReservedResponse46(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14046); m << value; return PhoneSend(remote,m); }
bool ReservedResponse47(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14047); m << value; return PhoneSend(remote,m); }
bool ReservedResponse48(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14048); m << value; return PhoneSend(remote,m); }
bool ReservedResponse49(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14049); m << value; return PhoneSend(remote,m); }
bool ReservedResponse50(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14050); m << value; return PhoneSend(remote,m); }
bool CG_RequestSecurityTokenOK(Proud::HostID remote, Proud::RmiContext& context, const Proud::String& securityToken) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14051); m << securityToken; return PhoneSend(remote,m); }
bool CG_RequestNetmarbleAuthOK(Proud::HostID remote, Proud::RmiContext& context, const NetmarbleAccountInfo& info) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14052); m << info; return PhoneSend(remote,m); }
bool CG_RequestAuthenticateCreateOK(Proud::HostID remote, Proud::RmiContext& context, const NetmarbleAccountInfo& info) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14053); m << info; return PhoneSend(remote,m); }
bool ReservedResponse54(Proud::HostID remote, Proud::RmiContext& context, const int& value) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14054); m << value; return PhoneSend(remote,m); }
bool CG_RequestLoginOK(Proud::HostID remote, Proud::RmiContext& context, const LoginUserResultInfo& userInfo, const LoginServiceInfo& loginServiceInfo) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14055); m << userInfo; m << loginServiceInfo; return PhoneSend(remote,m); }
bool CG_RequestLoginInstantlyOK(Proud::HostID remote, Proud::RmiContext& context, const LocalReconnectResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14056); m << result; return PhoneSend(remote,m); }
bool ReservedResponse57(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14057); return PhoneSend(remote,m); }
bool ReservedResponse58(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14058); return PhoneSend(remote,m); }
bool ReservedResponse59(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14059); return PhoneSend(remote,m); }
bool ReservedResponse60(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14060); return PhoneSend(remote,m); }
bool ReservedResponse61(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14061); return PhoneSend(remote,m); }
bool ReservedResponse62(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14062); return PhoneSend(remote,m); }
bool ReservedResponse63(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14063); return PhoneSend(remote,m); }
bool ReservedResponse64(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14064); return PhoneSend(remote,m); }
bool ReservedResponse65(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14065); return PhoneSend(remote,m); }
bool ReservedResponse66(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14066); return PhoneSend(remote,m); }
bool ReservedResponse67(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14067); return PhoneSend(remote,m); }
bool ReservedResponse68(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14068); return PhoneSend(remote,m); }
bool ReservedResponse69(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14069); return PhoneSend(remote,m); }
bool ReservedResponse70(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14070); return PhoneSend(remote,m); }
bool ReservedResponse71(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14071); return PhoneSend(remote,m); }
bool ReservedResponse72(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14072); return PhoneSend(remote,m); }
bool ReservedResponse73(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14073); return PhoneSend(remote,m); }
bool ReservedResponse74(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14074); return PhoneSend(remote,m); }
bool ReservedResponse75(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14075); return PhoneSend(remote,m); }
bool ReservedResponse76(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14076); return PhoneSend(remote,m); }
bool ReservedResponse77(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14077); return PhoneSend(remote,m); }
bool ReservedResponse78(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14078); return PhoneSend(remote,m); }
bool ReservedResponse79(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14079); return PhoneSend(remote,m); }
bool ReservedResponse80(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14080); return PhoneSend(remote,m); }
bool ReservedResponse81(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14081); return PhoneSend(remote,m); }
bool ReservedResponse82(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14082); return PhoneSend(remote,m); }
bool ReservedResponse83(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14083); return PhoneSend(remote,m); }
bool CG_RequestBillingCouponVerifyOK(Proud::HostID remote, Proud::RmiContext& context, const BillingVerifyResultInfo& verifyResultInfo, const GcString& netmarble_reward_id) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14084); m << verifyResultInfo; m << netmarble_reward_id; return PhoneSend(remote,m); }
};
}
namespace SevenDSGuideC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestQuestGuideListAllClearReward(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGuideC2S_CG_RequestQuestGuideListAllClearReward bool CG_RequestQuestGuideListAllClearReward(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGuideC2S_CG_RequestQuestGuideListAllClearReward(DerivedClass) bool DerivedClass::CG_RequestQuestGuideListAllClearReward(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestQuestGuideListStepStart(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGuideC2S_CG_RequestQuestGuideListStepStart bool CG_RequestQuestGuideListStepStart(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGuideC2S_CG_RequestQuestGuideListStepStart(DerivedClass) bool DerivedClass::CG_RequestQuestGuideListStepStart(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestQuestGuideListStepClear(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSGuideC2S_CG_RequestQuestGuideListStepClear bool CG_RequestQuestGuideListStepClear(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSGuideC2S_CG_RequestQuestGuideListStepClear(DerivedClass) bool DerivedClass::CG_RequestQuestGuideListStepClear(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSGuideS2C {
class Proxy { public:
bool CG_RequestQuestGuideListAllClearRewardOK(Proud::HostID remote, Proud::RmiContext& context, const LocalNoItem& result, const MissionResult& mission) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14194); m << result; m << mission; return PhoneSend(remote,m); }
bool CG_RequestQuestGuideListStepStartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalGuideResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14195); m << result; return PhoneSend(remote,m); }
bool CG_RequestQuestGuideListStepClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalGuideResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14196); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSLegendC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinLegendEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) { return false; }
#define DECRMI_SevenDSLegendC2S_CG_RequestSkinLegendEvolution bool CG_RequestSkinLegendEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) override
#define DEFRMI_SevenDSLegendC2S_CG_RequestSkinLegendEvolution(DerivedClass) bool DerivedClass::CG_RequestSkinLegendEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID)
};
}
namespace SevenDSLegendS2C {
class Proxy { public:
bool CG_RequestSkinLegendEvolutionOK(Proud::HostID remote, Proud::RmiContext& context, const LocalLegendResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14130); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSLimitBreakC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinOverEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) { return false; }
#define DECRMI_SevenDSLimitBreakC2S_CG_RequestSkinOverEvolution bool CG_RequestSkinOverEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) override
#define DEFRMI_SevenDSLimitBreakC2S_CG_RequestSkinOverEvolution(DerivedClass) bool DerivedClass::CG_RequestSkinOverEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID)
};
}
namespace SevenDSLimitBreakS2C {
class Proxy { public:
bool CG_RequestSkinOverEvolutionOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBreakResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14114); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSMailC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestMailList(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& language) { return false; }
#define DECRMI_SevenDSMailC2S_CG_RequestMailList bool CG_RequestMailList(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& language) override
#define DEFRMI_SevenDSMailC2S_CG_RequestMailList(DerivedClass) bool DerivedClass::CG_RequestMailList(Proud::HostID remote, Proud::RmiContext& rmiContext, const uint8& language)
virtual bool CG_RequestMailConfirm(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const bool& multi) { return false; }
#define DECRMI_SevenDSMailC2S_CG_RequestMailConfirm bool CG_RequestMailConfirm(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const bool& multi) override
#define DEFRMI_SevenDSMailC2S_CG_RequestMailConfirm(DerivedClass) bool DerivedClass::CG_RequestMailConfirm(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& serial, const bool& multi)
virtual bool CG_RequestMailConfirmAll(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSMailC2S_CG_RequestMailConfirmAll bool CG_RequestMailConfirmAll(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSMailC2S_CG_RequestMailConfirmAll(DerivedClass) bool DerivedClass::CG_RequestMailConfirmAll(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSMailS2C {
class Proxy { public:
bool CG_RequestMailListOK(Proud::HostID remote, Proud::RmiContext& context, const LocalMailResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14151); m << result; return PhoneSend(remote,m); }
bool CG_RequestMailConfirmOK(Proud::HostID remote, Proud::RmiContext& context, const LocalMailResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14152); m << result; return PhoneSend(remote,m); }
bool CG_RequestMailConfirmAllOK(Proud::HostID remote, Proud::RmiContext& context, const LocalMailResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14153); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSMainSkinC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestMainSkinChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin) { return false; }
#define DECRMI_SevenDSMainSkinC2S_CG_RequestMainSkinChange bool CG_RequestMainSkinChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin) override
#define DEFRMI_SevenDSMainSkinC2S_CG_RequestMainSkinChange(DerivedClass) bool DerivedClass::CG_RequestMainSkinChange(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& skin)
};
}
namespace SevenDSMainSkinS2C {
class Proxy { public:
bool CG_RequestMainSkinChangeOK(Proud::HostID remote, Proud::RmiContext& context, const int& skin) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14018); m << skin; return PhoneSend(remote,m); }
};
}
namespace SevenDSMaxAwakenC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinMaxAwaken(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const int& item) { return false; }
#define DECRMI_SevenDSMaxAwakenC2S_CG_RequestSkinMaxAwaken bool CG_RequestSkinMaxAwaken(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const int& item) override
#define DEFRMI_SevenDSMaxAwakenC2S_CG_RequestSkinMaxAwaken(DerivedClass) bool DerivedClass::CG_RequestSkinMaxAwaken(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const int& item)
};
}
namespace SevenDSMaxAwakenS2C {
class Proxy { public:
bool CG_RequestSkinMaxAwakenOK(Proud::HostID remote, Proud::RmiContext& context, const LocalGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14121); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSMercenaryS2C {
class Proxy { public:
bool CG_RequestMercenaryListOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& mercenaries) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18976); m << mercenaries; return PhoneSend(remote,m); }
};
}
namespace SevenDSMissionC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestMissionProgress(Proud::HostID remote, Proud::RmiContext& rmiContext, const int16& missionType, const int& missionTypeValue, const int& addValue) { return false; }
#define DECRMI_SevenDSMissionC2S_CG_RequestMissionProgress bool CG_RequestMissionProgress(Proud::HostID remote, Proud::RmiContext& rmiContext, const int16& missionType, const int& missionTypeValue, const int& addValue) override
#define DEFRMI_SevenDSMissionC2S_CG_RequestMissionProgress(DerivedClass) bool DerivedClass::CG_RequestMissionProgress(Proud::HostID remote, Proud::RmiContext& rmiContext, const int16& missionType, const int& missionTypeValue, const int& addValue)
virtual bool CG_RequestMissionClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalMissionClearRequest& request) { return false; }
#define DECRMI_SevenDSMissionC2S_CG_RequestMissionClear bool CG_RequestMissionClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalMissionClearRequest& request) override
#define DEFRMI_SevenDSMissionC2S_CG_RequestMissionClear(DerivedClass) bool DerivedClass::CG_RequestMissionClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalMissionClearRequest& request)
virtual bool ReservedMissionEventClear(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSMissionC2S_ReservedMissionEventClear bool ReservedMissionEventClear(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSMissionC2S_ReservedMissionEventClear(DerivedClass) bool DerivedClass::ReservedMissionEventClear(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestMissionGetAchievePointReward(Proud::HostID remote, Proud::RmiContext& rmiContext, const int16& rewardOrder) { return false; }
#define DECRMI_SevenDSMissionC2S_CG_RequestMissionGetAchievePointReward bool CG_RequestMissionGetAchievePointReward(Proud::HostID remote, Proud::RmiContext& rmiContext, const int16& rewardOrder) override
#define DEFRMI_SevenDSMissionC2S_CG_RequestMissionGetAchievePointReward(DerivedClass) bool DerivedClass::CG_RequestMissionGetAchievePointReward(Proud::HostID remote, Proud::RmiContext& rmiContext, const int16& rewardOrder)
};
}
namespace SevenDSMissionS2C {
class Proxy { public:
bool CG_RequestMissionProgressOK(Proud::HostID remote, Proud::RmiContext& context, const MissionResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14181); m << result; return PhoneSend(remote,m); }
bool CG_RequestMissionClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalMissionClearResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14182); m << result; return PhoneSend(remote,m); }
bool ReservedMissionEventClearOK(Proud::HostID remote, Proud::RmiContext& context) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14183); return PhoneSend(remote,m); }
bool CG_RequestMissionGetAchievePointRewardOK(Proud::HostID remote, Proud::RmiContext& context, const LocalAchievementResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14184); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSOneStepC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinOneStepEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) { return false; }
#define DECRMI_SevenDSOneStepC2S_CG_RequestSkinOneStepEvolution bool CG_RequestSkinOneStepEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) override
#define DEFRMI_SevenDSOneStepC2S_CG_RequestSkinOneStepEvolution(DerivedClass) bool DerivedClass::CG_RequestSkinOneStepEvolution(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID)
};
}
namespace SevenDSOneStepLiteC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinOneStepEvolutionLite(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) { return false; }
#define DECRMI_SevenDSOneStepLiteC2S_CG_RequestSkinOneStepEvolutionLite bool CG_RequestSkinOneStepEvolutionLite(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID) override
#define DEFRMI_SevenDSOneStepLiteC2S_CG_RequestSkinOneStepEvolutionLite(DerivedClass) bool DerivedClass::CG_RequestSkinOneStepEvolutionLite(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID)
};
}
namespace SevenDSOneStepLiteS2C {
class Proxy { public:
bool CG_RequestSkinOneStepEvolutionLiteOK(Proud::HostID remote, Proud::RmiContext& context, const LocalOneStepResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(15500); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSOneStepS2C {
class Proxy { public:
bool CG_RequestSkinOneStepEvolutionOK(Proud::HostID remote, Proud::RmiContext& context, const LocalOneStepResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14031); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSPackageInfoC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestPackageShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSPackageInfoC2S_CG_RequestPackageShopInfo bool CG_RequestPackageShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSPackageInfoC2S_CG_RequestPackageShopInfo(DerivedClass) bool DerivedClass::CG_RequestPackageShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSPackageInfoS2C {
class Proxy { public:
bool CG_RequestPackageShopInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalPackageInfo& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18527); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSPassiveC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestGetExclusiveSkill(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& heroId) { return false; }
#define DECRMI_SevenDSPassiveC2S_CG_RequestGetExclusiveSkill bool CG_RequestGetExclusiveSkill(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& heroId) override
#define DEFRMI_SevenDSPassiveC2S_CG_RequestGetExclusiveSkill(DerivedClass) bool DerivedClass::CG_RequestGetExclusiveSkill(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& heroId)
};
}
namespace SevenDSPassiveS2C {
class Proxy { public:
bool CG_RequestGetExclusiveSkillOK(Proud::HostID remote, Proud::RmiContext& context, const LocalPassiveResult& userSkin) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14127); m << userSkin; return PhoneSend(remote,m); }
};
}
namespace SevenDSQuestBattleC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_Request_Quest_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) { return false; }
#define DECRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Start bool CG_Request_Quest_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) override
#define DEFRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Start(DerivedClass) bool DerivedClass::CG_Request_Quest_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request)
virtual bool CG_Request_Quest_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) { return false; }
#define DECRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Clear bool CG_Request_Quest_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) override
#define DEFRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Clear(DerivedClass) bool DerivedClass::CG_Request_Quest_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request)
virtual bool CG_Request_Quest_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Continue bool CG_Request_Quest_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSQuestBattleC2S_CG_Request_Quest_Stage_Continue(DerivedClass) bool DerivedClass::CG_Request_Quest_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSQuestBattleS2C {
class Proxy { public:
bool CG_Request_Quest_Stage_StartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageStartResult& result, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18813); m << result; m << payback; return PhoneSend(remote,m); }
bool CG_Request_Quest_Stage_ClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageClearResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18814); m << result; return PhoneSend(remote,m); }
bool CG_Request_Quest_Stage_ContinueOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& items, const short& count, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18815); m << items; m << count; m << payback; return PhoneSend(remote,m); }
};
}
namespace SevenDSQuestC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestQuestStart(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID) { return false; }
#define DECRMI_SevenDSQuestC2S_CG_RequestQuestStart bool CG_RequestQuestStart(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID) override
#define DEFRMI_SevenDSQuestC2S_CG_RequestQuestStart(DerivedClass) bool DerivedClass::CG_RequestQuestStart(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID)
virtual bool CG_RequestQuestProgress(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID, const int& needID, const uint8& propIndex) { return false; }
#define DECRMI_SevenDSQuestC2S_CG_RequestQuestProgress bool CG_RequestQuestProgress(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID, const int& needID, const uint8& propIndex) override
#define DEFRMI_SevenDSQuestC2S_CG_RequestQuestProgress(DerivedClass) bool DerivedClass::CG_RequestQuestProgress(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID, const int& needID, const uint8& propIndex)
virtual bool CG_RequestQuestClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID) { return false; }
#define DECRMI_SevenDSQuestC2S_CG_RequestQuestClear bool CG_RequestQuestClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID) override
#define DEFRMI_SevenDSQuestC2S_CG_RequestQuestClear(DerivedClass) bool DerivedClass::CG_RequestQuestClear(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& questID)
};
}
namespace SevenDSQuestS2C {
class Proxy { public:
bool CG_RequestQuestStartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalQuestStartResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14185); m << result; return PhoneSend(remote,m); }
bool CG_RequestQuestProgressOK(Proud::HostID remote, Proud::RmiContext& context, const LocalQuestProgressResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14186); m << result; return PhoneSend(remote,m); }
bool CG_RequestQuestClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalQuestClearResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14187); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSRecipeActiveC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestRecipeActive(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& recipeID) { return false; }
#define DECRMI_SevenDSRecipeActiveC2S_CG_RequestRecipeActive bool CG_RequestRecipeActive(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& recipeID) override
#define DEFRMI_SevenDSRecipeActiveC2S_CG_RequestRecipeActive(DerivedClass) bool DerivedClass::CG_RequestRecipeActive(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& recipeID)
};
}
namespace SevenDSRecipeActiveS2C {
class Proxy { public:
bool CG_RequestRecipeActiveOK(Proud::HostID remote, Proud::RmiContext& context, const LocalFoodResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14230); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSRecipeInfoC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCookingRecipeOrderInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSRecipeInfoC2S_CG_RequestCookingRecipeOrderInfo bool CG_RequestCookingRecipeOrderInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSRecipeInfoC2S_CG_RequestCookingRecipeOrderInfo(DerivedClass) bool DerivedClass::CG_RequestCookingRecipeOrderInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSRecipeInfoS2C {
class Proxy { public:
bool CG_RequestCookingRecipeOrderInfoOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& orders) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14231); m << orders; return PhoneSend(remote,m); }
};
}
namespace SevenDSRelicC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCostumeCraft(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costume, const bool& quick) { return false; }
#define DECRMI_SevenDSRelicC2S_CG_RequestCostumeCraft bool CG_RequestCostumeCraft(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costume, const bool& quick) override
#define DEFRMI_SevenDSRelicC2S_CG_RequestCostumeCraft(DerivedClass) bool DerivedClass::CG_RequestCostumeCraft(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costume, const bool& quick)
};
}
namespace SevenDSRelicS2C {
class Proxy { public:
bool CG_RequestCostumeCraftOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14125); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSRelicUpgradeC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestCostumeCraftUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costume, const uint8& upgradeType) { return false; }
#define DECRMI_SevenDSRelicUpgradeC2S_CG_RequestCostumeCraftUpgrade bool CG_RequestCostumeCraftUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costume, const uint8& upgradeType) override
#define DEFRMI_SevenDSRelicUpgradeC2S_CG_RequestCostumeCraftUpgrade(DerivedClass) bool DerivedClass::CG_RequestCostumeCraftUpgrade(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& costume, const uint8& upgradeType)
};
}
namespace SevenDSRelicUpgradeS2C {
class Proxy { public:
bool CG_RequestCostumeCraftUpgradeOK(Proud::HostID remote, Proud::RmiContext& context, const LocalRelicUpgradeResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14131); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSStoryCostumeC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestStoryCostume(Proud::HostID remote, Proud::RmiContext& rmiContext, const IntList& idList) { return false; }
#define DECRMI_SevenDSStoryCostumeC2S_CG_RequestStoryCostume bool CG_RequestStoryCostume(Proud::HostID remote, Proud::RmiContext& rmiContext, const IntList& idList) override
#define DEFRMI_SevenDSStoryCostumeC2S_CG_RequestStoryCostume(DerivedClass) bool DerivedClass::CG_RequestStoryCostume(Proud::HostID remote, Proud::RmiContext& rmiContext, const IntList& idList)
};
}
namespace SevenDSStoryCostumeS2C {
class Proxy { public:
bool CG_RequestStoryCostumeOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& getItems, const EmptyItemResults& userStoryCostumeItemList) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14119); m << getItems; m << userStoryCostumeItemList; return PhoneSend(remote,m); }
};
}
namespace SevenDSStoryInfoC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestStageInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSStoryInfoC2S_CG_RequestStageInfo bool CG_RequestStageInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSStoryInfoC2S_CG_RequestStageInfo(DerivedClass) bool DerivedClass::CG_RequestStageInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSStoryInfoS2C {
class Proxy { public:
bool CG_RequestStageInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageInfo& info) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18800); m << info; return PhoneSend(remote,m); }
};
}
namespace SevenDSStoryStartC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_Request_Main_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) { return false; }
#define DECRMI_SevenDSStoryStartC2S_CG_Request_Main_Stage_Start bool CG_Request_Main_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) override
#define DEFRMI_SevenDSStoryStartC2S_CG_Request_Main_Stage_Start(DerivedClass) bool DerivedClass::CG_Request_Main_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request)
virtual bool CG_Request_Main_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) { return false; }
#define DECRMI_SevenDSStoryStartC2S_CG_Request_Main_Stage_Clear bool CG_Request_Main_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) override
#define DEFRMI_SevenDSStoryStartC2S_CG_Request_Main_Stage_Clear(DerivedClass) bool DerivedClass::CG_Request_Main_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request)
};
}
namespace SevenDSStoryStartS2C {
class Proxy { public:
bool CG_Request_Main_Stage_StartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageStartResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18804); m << result; return PhoneSend(remote,m); }
bool CG_Request_Main_Stage_ClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageClearResult& result, const bool& isFirstMainStageClear, const EmptyItemResults& userPackageMissionInfoList) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18805); m << result; m << isFirstMainStageClear; m << userPackageMissionInfoList; return PhoneSend(remote,m); }
};
}
namespace SevenDSStraightLimitBreakC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinOverEvolutionStraight(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID, const uint8_t& targetMaxLevelCount) { return false; }
#define DECRMI_SevenDSStraightLimitBreakC2S_CG_RequestSkinOverEvolutionStraight bool CG_RequestSkinOverEvolutionStraight(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID, const uint8_t& targetMaxLevelCount) override
#define DEFRMI_SevenDSStraightLimitBreakC2S_CG_RequestSkinOverEvolutionStraight(DerivedClass) bool DerivedClass::CG_RequestSkinOverEvolutionStraight(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& targetHeroID, const uint8_t& targetMaxLevelCount)
};
}
namespace SevenDSStraightLimitBreakS2C {
class Proxy { public:
bool CG_RequestSkinOverEvolutionStraightOK(Proud::HostID remote, Proud::RmiContext& context, const LocalBreakResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14129); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSSuperAwakenC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinTranscend(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTranscendRequest& request) { return false; }
#define DECRMI_SevenDSSuperAwakenC2S_CG_RequestSkinTranscend bool CG_RequestSkinTranscend(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTranscendRequest& request) override
#define DEFRMI_SevenDSSuperAwakenC2S_CG_RequestSkinTranscend(DerivedClass) bool DerivedClass::CG_RequestSkinTranscend(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTranscendRequest& request)
virtual bool CG_RequestSkinTranscendReset(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& itemIndex) { return false; }
#define DECRMI_SevenDSSuperAwakenC2S_CG_RequestSkinTranscendReset bool CG_RequestSkinTranscendReset(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& itemIndex) override
#define DEFRMI_SevenDSSuperAwakenC2S_CG_RequestSkinTranscendReset(DerivedClass) bool DerivedClass::CG_RequestSkinTranscendReset(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& itemIndex)
};
}
namespace SevenDSSuperAwakenS2C {
class Proxy { public:
bool CG_RequestSkinTranscendOK(Proud::HostID remote, Proud::RmiContext& context, const LocalGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14123); m << result; return PhoneSend(remote,m); }
bool CG_RequestSkinTranscendResetOK(Proud::HostID remote, Proud::RmiContext& context, const LocalGrowthResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14124); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSTowerShopC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestYggdrasilTowerShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSTowerShopC2S_CG_RequestYggdrasilTowerShopInfo bool CG_RequestYggdrasilTowerShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSTowerShopC2S_CG_RequestYggdrasilTowerShopInfo(DerivedClass) bool DerivedClass::CG_RequestYggdrasilTowerShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext)
virtual bool CG_RequestYggdrasilTowerShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& product, const uint8& count) { return false; }
#define DECRMI_SevenDSTowerShopC2S_CG_RequestYggdrasilTowerShopBuy bool CG_RequestYggdrasilTowerShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& product, const uint8& count) override
#define DEFRMI_SevenDSTowerShopC2S_CG_RequestYggdrasilTowerShopBuy(DerivedClass) bool DerivedClass::CG_RequestYggdrasilTowerShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& product, const uint8& count)
};
}
namespace SevenDSTowerShopS2C {
class Proxy { public:
bool CG_RequestYggdrasilTowerShopInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalTowerShopInfo& info) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18572); m << info; return PhoneSend(remote,m); }
bool CG_RequestYggdrasilTowerShopBuyOK(Proud::HostID remote, Proud::RmiContext& context, const LocalTowerShopBuy& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18573); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSTownChestC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestBasePointUniqueInteractiveOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& npcID) { return false; }
#define DECRMI_SevenDSTownChestC2S_CG_RequestBasePointUniqueInteractiveOpen bool CG_RequestBasePointUniqueInteractiveOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& npcID) override
#define DEFRMI_SevenDSTownChestC2S_CG_RequestBasePointUniqueInteractiveOpen(DerivedClass) bool DerivedClass::CG_RequestBasePointUniqueInteractiveOpen(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& npcID)
};
}
namespace SevenDSTownChestS2C {
class Proxy { public:
bool CG_RequestBasePointUniqueInteractiveOpenOK(Proud::HostID remote, Proud::RmiContext& context, const LocalChestResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14304); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSTownDonationC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestBasePointGoldDonation(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& town, const int& item, const int& count) { return false; }
#define DECRMI_SevenDSTownDonationC2S_CG_RequestBasePointGoldDonation bool CG_RequestBasePointGoldDonation(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& town, const int& item, const int& count) override
#define DEFRMI_SevenDSTownDonationC2S_CG_RequestBasePointGoldDonation(DerivedClass) bool DerivedClass::CG_RequestBasePointGoldDonation(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& town, const int& item, const int& count)
};
}
namespace SevenDSTownDonationS2C {
class Proxy { public:
bool CG_RequestBasePointGoldDonationOK(Proud::HostID remote, Proud::RmiContext& context, const LocalTownDonationResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14301); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSTownInfoC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestBasePointInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& basePointID) { return false; }
#define DECRMI_SevenDSTownInfoC2S_CG_RequestBasePointInfo bool CG_RequestBasePointInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& basePointID) override
#define DEFRMI_SevenDSTownInfoC2S_CG_RequestBasePointInfo(DerivedClass) bool DerivedClass::CG_RequestBasePointInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& basePointID)
};
}
namespace SevenDSTownInfoS2C {
class Proxy { public:
bool CG_RequestBasePointInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalTownInfoResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14013); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSTownShopC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestBasePointShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& basepointID, const bool& isCommonShop) { return false; }
#define DECRMI_SevenDSTownShopC2S_CG_RequestBasePointShopInfo bool CG_RequestBasePointShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& basepointID, const bool& isCommonShop) override
#define DEFRMI_SevenDSTownShopC2S_CG_RequestBasePointShopInfo(DerivedClass) bool DerivedClass::CG_RequestBasePointShopInfo(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& basepointID, const bool& isCommonShop)
virtual bool CG_RequestBasePointShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTownBuyRequest& request) { return false; }
#define DECRMI_SevenDSTownShopC2S_CG_RequestBasePointShopBuy bool CG_RequestBasePointShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTownBuyRequest& request) override
#define DEFRMI_SevenDSTownShopC2S_CG_RequestBasePointShopBuy(DerivedClass) bool DerivedClass::CG_RequestBasePointShopBuy(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalTownBuyRequest& request)
};
}
namespace SevenDSTownShopS2C {
class Proxy { public:
bool CG_RequestBasePointShopInfoOK(Proud::HostID remote, Proud::RmiContext& context, const LocalTownShopResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18512); m << result; return PhoneSend(remote,m); }
bool CG_RequestBasePointShopBuyOK(Proud::HostID remote, Proud::RmiContext& context, const LocalTownBuyResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18513); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSTrueAwakeningC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinExceed(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& rank, const uint8& type) { return false; }
#define DECRMI_SevenDSTrueAwakeningC2S_CG_RequestSkinExceed bool CG_RequestSkinExceed(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& rank, const uint8& type) override
#define DEFRMI_SevenDSTrueAwakeningC2S_CG_RequestSkinExceed(DerivedClass) bool DerivedClass::CG_RequestSkinExceed(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& rank, const uint8& type)
};
}
namespace SevenDSTrueAwakeningS2C {
class Proxy { public:
bool CG_RequestSkinExceedOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(14133); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSTrueSelectC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_RequestSkinExceedSelect(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& type) { return false; }
#define DECRMI_SevenDSTrueSelectC2S_CG_RequestSkinExceedSelect bool CG_RequestSkinExceedSelect(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& type) override
#define DEFRMI_SevenDSTrueSelectC2S_CG_RequestSkinExceedSelect(DerivedClass) bool DerivedClass::CG_RequestSkinExceedSelect(Proud::HostID remote, Proud::RmiContext& rmiContext, const int& hero, const uint8& type)
};
}
namespace SevenDSTrueSelectS2C {
class Proxy { public:
bool CG_RequestSkinExceedSelectOK(Proud::HostID remote, Proud::RmiContext& context, const LocalSystemsResult& result) { Proud::CMessage m; m << uint8_t(1) << uint16_t(15603); m << result; return PhoneSend(remote,m); }
};
}
namespace SevenDSWeekBattleC2S {
class Stub { public: virtual ~Stub()=default;
virtual bool CG_Request_Week_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) { return false; }
#define DECRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Start bool CG_Request_Week_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request) override
#define DEFRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Start(DerivedClass) bool DerivedClass::CG_Request_Week_Stage_Start(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageStartRequest& request)
virtual bool CG_Request_Week_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) { return false; }
#define DECRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Clear bool CG_Request_Week_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request) override
#define DEFRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Clear(DerivedClass) bool DerivedClass::CG_Request_Week_Stage_Clear(Proud::HostID remote, Proud::RmiContext& rmiContext, const LocalStageClearRequest& request)
virtual bool CG_Request_Week_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) { return false; }
#define DECRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Continue bool CG_Request_Week_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext) override
#define DEFRMI_SevenDSWeekBattleC2S_CG_Request_Week_Stage_Continue(DerivedClass) bool DerivedClass::CG_Request_Week_Stage_Continue(Proud::HostID remote, Proud::RmiContext& rmiContext)
};
}
namespace SevenDSWeekBattleS2C {
class Proxy { public:
bool CG_Request_Week_Stage_StartOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageStartResult& result, const LocalPayback& payback, const LocalNoItem& useItem) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18816); m << result; m << payback; m << useItem; return PhoneSend(remote,m); }
bool CG_Request_Week_Stage_ClearOK(Proud::HostID remote, Proud::RmiContext& context, const LocalStageClearResult& result, const bool& flag, const EmptyItemResults& apList, const EmptyItemResults& packageList, const EmptyItemResults& items) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18817); m << result; m << flag; m << apList; m << packageList; m << items; return PhoneSend(remote,m); }
bool CG_Request_Week_Stage_ContinueOK(Proud::HostID remote, Proud::RmiContext& context, const EmptyItemResults& items, const short& count, const LocalPayback& payback) { Proud::CMessage m; m << uint8_t(1) << uint16_t(18818); m << items; m << count; m << payback; return PhoneSend(remote,m); }
};
}