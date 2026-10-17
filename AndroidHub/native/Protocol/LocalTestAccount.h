#pragma once
#include <algorithm>
#include <fstream>
#include <mutex>
#include <set>
#include <random>
#include <stdexcept>
#include <vector>
#include <map>
#include <limits>
#include "LocalMaterialCatalog.h"
#include <Windows.h>
#include "LocalGachaCatalog.h"
#include "LocalTgWardrobe.h"

namespace GcLocal {
inline constexpr int TestDiamonds = 2000000000;
inline constexpr int TestMaterialCount = 999999;
inline bool CustomMode() {
    static bool custom=[] {std::ifstream f("local-test-options.txt");std::string k;while(f>>k)if(k=="mode=vanilla")return false;return true;}();return custom;
}
inline bool EasyFarm() {
    if(CustomMode())return false;
    std::ifstream f("local-test-options.txt");std::string k;while(f>>k)if(k=="ez_farm=1")return true;return false;
}
inline std::map<int,int>& Wallet() {
    static auto balances=[] {std::map<int,int> r;std::ifstream f("local-test-wallet.txt");int id,count;
        if(!f){r[500012]=100000;r[500020]=100;r[541401]=30;for(int box:{1260018,1260111,1260112,1260113,1260114,1260115})r[box]=1;}
        while(f>>id>>count)if(id>=0 && count>=0)r[id]=count;return r;}();return balances;
}
inline void SaveWallet() {
    std::ofstream f("local-test-wallet.txt.tmp",std::ios::trunc);for(const auto& r:Wallet())f<<r.first<<' '<<r.second<<'\n';f.close();
    if(!f || !MoveFileExW(L"local-test-wallet.txt.tmp",L"local-test-wallet.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save wallet");
}
inline int SeededMaterialCount(int id) {
    if(!CustomMode()){auto it=Wallet().find(id);return it==Wallet().end()?0:it->second;}
    if(id==500011)return TestDiamonds;if(id==500012)return 99999999;
    return id>=543301 && id<=543305 ? 2000000000 : TestMaterialCount;
}
inline bool Spend(const std::vector<std::pair<int,int>>& costs) {
    std::map<int,int64_t> totals;
    for(auto c:costs){if(c.first<=0||c.second<0)return false;totals[c.first]+=c.second;}
    if(CustomMode())return true;
    for(auto c:totals)if(c.second>SeededMaterialCount(c.first))return false;
    for(auto c:totals)Wallet()[c.first]-=int(c.second);SaveWallet();return true;
}
inline void Grant(int id,int count) {
    if(id<=0||count<=0)return;
    if(!CustomMode()){Wallet()[id]=int((std::min)(int64_t(INT32_MAX),int64_t(SeededMaterialCount(id))+count));SaveWallet();}
}
inline bool WelcomePending(){return !CustomMode()&&!Wallet().count(0);}
inline bool ClaimWelcome(){if(!WelcomePending())return false;Wallet()[500011]=SeededMaterialCount(500011)+600;Wallet()[0]=1;SaveWallet();return true;}
inline int StageDiamondReward() {
    std::ifstream file("local-test-options.txt"); std::string value;
    while (file >> value) if (value.rfind("gem_multiplier=",0)==0) {
        try { return (std::max)(0,(std::min)(10000,std::stoi(value.substr(15)))); }
        catch (...) { return 5; }
    }
    return 5;
}
inline std::mutex AccountMutex;
inline bool GrantAllForNewProfiles() {
    std::ifstream config("local-test-options.txt"); std::string key;
    while (config >> key) if (key == "grant_all=1") return true;
    return false;
}
inline std::vector<int> AllHeroPool() {
    std::vector<int> result;
    for (const auto& skin : Skins) {
        if (skin.hero <= 0 || IsTgWardrobeSkin(skin.id) || skin.id==399921 || skin.id==399933) continue;
        bool base = true;
        for (const auto& other : Skins) if (other.hero == skin.hero &&
            (other.rating < skin.rating || (other.rating == skin.rating && other.id < skin.id))) { base = false; break; }
        if (base) result.push_back(skin.id);
    }
    return result;
}
inline std::set<int>& OwnedSkins() {
    static std::set<int> skins = [] {
        BackupTgWardrobeSaves();
        std::set<int> result;
        std::ifstream input("local-test-account-skins.txt"); int id;
        if (!input) result.insert(300104);
        if (!input && CustomMode() && GrantAllForNewProfiles())
            for (int skin : AllHeroPool()) result.insert(skin);
        while (input >> id) {
            id=CanonicalTgSkin(id);
            for (const auto& skin : Skins) if (skin.id == id) result.insert(id);
        }
        return result;
    }();
    return skins;
}
inline const Skin* FindSkin(int id) {
    for (const auto& skin : Skins) if (skin.id == id) return &skin;
    return nullptr;
}
inline std::set<int> OwnedHeroes() {
    std::set<int> heroes;
    for (int id : OwnedSkins()) if (const auto* skin = FindSkin(id)) heroes.insert(skin->hero);
    return heroes;
}
inline void SaveAccount() {
    std::ofstream file("local-test-account-skins.txt.tmp", std::ios::trunc);
    for (int id : OwnedSkins()) file << id << '\n';
    file.close();
    if (!file || !MoveFileExW(L"local-test-account-skins.txt.tmp", L"local-test-account-skins.txt",
                             MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH))
        throw std::runtime_error("Could not save local test account");
}
inline int RollSkin(int group) {
    std::vector<const PoolEntry*> pool; std::vector<double> weights;
    for (const auto& entry : Pool)
        if (entry.group == group && entry.weight > 0 && FindSkin(entry.skin)) {
            pool.push_back(&entry); weights.push_back(entry.weight);
        }
    if (pool.empty()) throw std::runtime_error("No matching client summon pool");
    static std::mt19937 generator(std::random_device{}());
    return pool[std::discrete_distribution<size_t>(weights.begin(), weights.end())(generator)]->skin;
}
}
