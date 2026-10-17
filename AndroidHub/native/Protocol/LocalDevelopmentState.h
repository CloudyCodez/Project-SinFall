#pragma once
#include <map>
#include <sstream>
#include "LocalDevelopmentCatalog.h"
#include "LocalCosmeticCatalog.h"
namespace GcLocal {
inline std::set<int>& UnlockedPassives() {
    static std::set<int> result = [] {
        std::set<int> ids; std::ifstream file("local-test-passives.txt"); int id;
        while (file >> id) {id=CanonicalTgSkin(id);if (FindSkin(id)) ids.insert(id);}
        return ids;
    }(); return result;
}
inline void SavePassives() {
    std::ofstream file("local-test-passives.txt.tmp", std::ios::trunc);
    for (int id : UnlockedPassives()) file << id << '\n';
    file.close();
    if (!file || !MoveFileExW(L"local-test-passives.txt.tmp", L"local-test-passives.txt", MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH))
        throw std::runtime_error("Could not save passive unlocks");
}
struct CosmeticEquipment { int outfit = 0, weapon = 0, head = 0; };
inline std::map<int, CosmeticEquipment>& CosmeticEquipments() {
    static std::map<int, CosmeticEquipment> result = [] {
        std::map<int, CosmeticEquipment> rows; std::ifstream file("local-test-cosmetics.txt");
        int hero; CosmeticEquipment row;
        while (file >> hero >> row.outfit >> row.weapon >> row.head) {
            const int canonical=CanonicalTgHero(hero);
            row.outfit=CanonicalTgCostumeGroup(canonical,row.outfit);
            row.weapon=CanonicalTgCostumeGroup(canonical,row.weapon);
            row.head=CanonicalTgCostumeGroup(canonical,row.head);
            if(canonical==hero || !rows.count(canonical))rows[canonical] = row;
        }
        return rows;
    }(); return result;
}
inline void SaveCosmetics() {
    std::ofstream file("local-test-cosmetics.txt.tmp", std::ios::trunc);
    for (const auto& entry : CosmeticEquipments())
        file << entry.first << ' ' << entry.second.outfit << ' ' << entry.second.weapon << ' ' << entry.second.head << '\n';
    file.close();
    if (!file || !MoveFileExW(L"local-test-cosmetics.txt.tmp", L"local-test-cosmetics.txt", MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH))
        throw std::runtime_error("Could not save equipped cosmetics");
}
struct DevelopmentState { int exp = 0, awaken = 0, skill = 0, limitBreak = 0, transcend = 0, exceed = 0, exceedSupreme = 0, exceedSelect = 0; };
// UserSkin.awaken contains the native flags for star positions 1..6.
// Save files and recipes keep the completed count; convert only at the wire.
inline uint8_t AwakeningFlags(int count) {
    return count <= 0 ? 0 : uint8_t(((1u << (std::min)(count,6)) - 1u) << 1);
}
inline std::map<int, DevelopmentState>& DevelopmentStates() {
    static std::map<int, DevelopmentState> states = [] {
        std::map<int, DevelopmentState> result; std::ifstream file("local-test-development.txt");
        int id; DevelopmentState state;
        std::string line;while(std::getline(file,line)){std::istringstream in(line);DevelopmentState state;int id;
            if(!(in>>id>>state.exp>>state.awaken>>state.skill>>state.limitBreak>>state.transcend))continue;
            in>>state.exceed>>state.exceedSupreme>>state.exceedSelect;
            id=CanonicalTgSkin(id);
            if(FindSkin(id)&&state.exp>=0&&state.awaken>=0&&state.awaken<=6){
                auto& merged=result[id];
                merged.exp=(std::max)(merged.exp,state.exp);merged.awaken=(std::max)(merged.awaken,state.awaken);
                merged.skill=(std::max)(merged.skill,state.skill);merged.limitBreak=(std::max)(merged.limitBreak,state.limitBreak);
                merged.transcend=(std::max)(merged.transcend,state.transcend);merged.exceed=(std::max)(merged.exceed,state.exceed);
                merged.exceedSupreme=(std::max)(merged.exceedSupreme,state.exceedSupreme);merged.exceedSelect=(std::max)(merged.exceedSelect,state.exceedSelect);
            }
        }
        return result;
    }(); return states;
}
inline void SaveDevelopment() {
    std::ofstream file("local-test-development.txt.tmp", std::ios::trunc);
    for (const auto& entry : DevelopmentStates()) {
        const auto& s = entry.second;
        file << entry.first << ' ' << s.exp << ' ' << s.awaken << ' ' << s.skill << ' ' << s.limitBreak << ' ' << s.transcend << ' ' << s.exceed << ' ' << s.exceedSupreme << ' ' << s.exceedSelect << '\n';
    }
    file.close();
    if (!file || !MoveFileExW(L"local-test-development.txt.tmp", L"local-test-development.txt", MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH))
        throw std::runtime_error("Could not save hero development");
}
inline const DevelopmentSkin* DevelopmentRow(int id) {
    for (const auto& row : DevelopmentSkins) if (row.id == id) return &row;
    return nullptr;
}
inline int ActiveSkin(int hero) {
    int result = 0, rating = -1;
    for (int id : OwnedSkins()) if (FindSkin(id)->hero == hero) {
        const auto* row = DevelopmentRow(id);
        if (row && row->rating > rating) { result = id; rating = row->rating; }
    }
    return result;
}
inline int SkinLevel(int id) {
    const auto* row=DevelopmentRow(id);if(!row)return 0;
    const auto& state=DevelopmentStates()[id];int level=1;
    for(const auto& e:ExperienceLevels){int exp=row->rating>=7?e.rank4:row->rating>=5?e.rank3:e.rank2;if(state.exp>=exp)level=(std::max)(level,e.level+1);}
    return (std::min)(level,row->maxLevel+5*state.limitBreak);
}
inline int& MainSkinSelection() {
    static int selected=[] {int id=0;std::ifstream f("local-test-main-skin.txt");f>>id;return id;}();return selected;
}
inline int MainSkin() {const int id=MainSkinSelection();return OwnedSkins().count(id)?id:ActiveSkin(1004001);}
inline void SaveMainSkin(int id) {
    std::ofstream f("local-test-main-skin.txt.tmp",std::ios::trunc);f<<id;f.close();
    if(!f || !MoveFileExW(L"local-test-main-skin.txt.tmp",L"local-test-main-skin.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save main hero");
    MainSkinSelection()=id;
}
inline void ReplaceMainSkin(int previous,int next) {if(MainSkin()==previous)SaveMainSkin(next);}
inline int ExperienceCap(int id) {
    const auto* row = DevelopmentRow(id); if (!row) return 0;
    const auto& state = DevelopmentStates()[id];
    if (!state.limitBreak) return row->maxExp;
    const int level = row->maxLevel + 5 * state.limitBreak;
    for (const auto& e : ExperienceLevels) if (e.level == level - 1) return row->rating >= 5 ? e.rank3 : e.rank2;
    return row->maxExp;
}

}
