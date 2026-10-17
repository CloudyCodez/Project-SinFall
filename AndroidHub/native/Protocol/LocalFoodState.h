#pragma once
#include "LocalFoodPvpCatalog.h"
namespace GcLocal {
inline const FoodRule* FindFood(int id){for(const auto& r:FoodRules)if(r.id==id)return &r;return nullptr;}
struct FoodState {int item=0,used=0;bool automatic=false;int64_t expires=0;};
inline FoodState& Food(){static FoodState s=[] {FoodState s;std::ifstream f("local-test-food.txt");f>>s.item>>s.used>>s.automatic>>s.expires;const auto* r=FindFood(s.item);if(!r||s.used<0||s.used>255)return FoodState{};return s;}();return s;}
inline void SaveFood(){const auto& s=Food();std::ofstream f("local-test-food.txt.tmp",std::ios::trunc);f<<s.item<<' '<<s.used<<' '<<s.automatic<<' '<<s.expires<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-food.txt.tmp",L"local-test-food.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save food buff");}
inline bool FoodActive(){const auto& s=Food();const auto* r=FindFood(s.item);return r&&(!r->uses||s.used<r->uses)&&(!r->minutes||s.expires>std::time(nullptr));}
inline bool EatFood(int id,bool automatic){const auto* r=FindFood(id);if(!r||r->uses>255||!Spend({{id,1}}))return false;Food()={id,0,automatic,r->minutes?std::time(nullptr)+int64_t(r->minutes)*60:0};SaveFood();RecordQuestAction("food",id,1);RecordQuestAction("food_eat",id,1);RecordMission(59,0,1);return true;}
// The live battle retains its own snapshot so switching food cannot consume a
// different buff, and a rejected/replayed clear cannot consume food twice.
inline std::map<int,FoodState>& BattleFood(){static std::map<int,FoodState> rows;return rows;}
inline int BattleFoodBonus(int remote,bool gold){auto it=BattleFood().find(remote);if(it==BattleFood().end())return 0;const auto* food=FindFood(it->second.item);if(!food||food->combat)return 0;for(auto r:FoodRewardRules)if(r.id==food->passive)return gold?r.gold:r.experience;return 0;}
inline int& AutoFoodConsumed(){static int id=0;return id;}
inline int PrepareBattleFood(int remote){auto& s=Food();int consumed=0;if(s.automatic&&!FoodActive()&&FindFood(s.item)&&EatFood(s.item,true))consumed=s.item;if(FoodActive())BattleFood()[remote]=s;else BattleFood().erase(remote);return consumed;}
inline void FinishBattleFood(int remote){auto it=BattleFood().find(remote);if(it==BattleFood().end())return;const auto old=it->second;BattleFood().erase(it);auto& s=Food();const auto* r=FindFood(old.item);if(r&&r->uses&&s.item==old.item&&s.used==old.used&&s.expires==old.expires){s.used=(std::min)(r->uses,s.used+1);SaveFood();}}
inline std::set<int>& PvpGrantedProducts(){static std::set<int> ids=[] {std::set<int> ids;std::ifstream f("local-test-pvp-grants.txt");int id;while(f>>id)ids.insert(id);return ids;}();return ids;}
inline void SavePvpGrants(){std::ofstream f("local-test-pvp-grants.txt.tmp",std::ios::trunc);for(int id:PvpGrantedProducts())f<<id<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-pvp-grants.txt.tmp",L"local-test-pvp-grants.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save PvP grants");}
}
