#pragma once
#include "LocalTownArtifactCatalog.h"
namespace GcLocal {
inline bool KnownTown(int id){for(auto r:TownRules)if(r.id==id)return true;for(auto r:TownChests)if(r.town==id)return true;return false;}
inline std::map<int,int>& TownDonationExperience(){static auto rows=[] {std::map<int,int> rows;std::ifstream f("local-test-town-donations.txt");int town,exp;while(f>>town>>exp)if(KnownTown(town)&&exp>=0&&exp<=36000)rows[town]=exp;return rows;}();return rows;}
inline void SaveTownDonations(){std::ofstream f("local-test-town-donations.txt.tmp",std::ios::trunc);for(auto p:TownDonationExperience())f<<p.first<<' '<<p.second<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-town-donations.txt.tmp",L"local-test-town-donations.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save town donations");}
inline int TownExperience(int id){int64_t exp=TownDonationExperience()[id];for(auto r:TownQuestRewards)if(r.town==id&&QuestCompleted(r.quest))exp+=r.exp;return int(std::min<int64_t>(2147483647LL,exp));}
inline int TownNextThreshold(int town){int next=2147483647;int exp=TownExperience(town);for(auto r:TownRules)if(r.id==town&&r.level<5&&r.exp>exp)next=(std::min)(next,r.exp);return next==2147483647?0:next;}
inline std::set<int>& OpenChests(){static std::set<int> ids=[] {std::set<int> ids;std::ifstream f("local-test-town-chests.txt");int id;while(f>>id)for(auto r:TownChests)if(r.npc==id)ids.insert(id);return ids;}();return ids;}
inline void SaveChests(){std::ofstream f("local-test-town-chests.txt.tmp",std::ios::trunc);for(int id:OpenChests())f<<id<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-town-chests.txt.tmp",L"local-test-town-chests.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save town chests");}
inline const ArtifactUnionRule* FindArtifactUnion(int id){for(const auto& r:ArtifactUnionRules)if(r.id==id)return &r;return nullptr;}
inline std::map<int,int>& ArtifactUnionExperience(){static std::map<int,int> rows=[] {std::map<int,int> rows;std::ifstream f("local-test-artifact-unions.txt");int id,exp;while(f>>id>>exp){const auto* r=FindArtifactUnion(id);if(r&&exp>=0&&exp<=r->cap)rows[id]=exp;}return rows;}();return rows;}
inline void SaveArtifactUnions(){std::ofstream f("local-test-artifact-unions.txt.tmp",std::ios::trunc);for(auto p:ArtifactUnionExperience())f<<p.first<<' '<<p.second<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-artifact-unions.txt.tmp",L"local-test-artifact-unions.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save artifact unions");}
}
