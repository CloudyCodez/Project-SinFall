#pragma once
#include <map>
#include <set>
#include <fstream>
#include "LocalStoryRules.h"
#include "LocalWeekIndices.h"
namespace GcLocal {
inline std::set<std::pair<int,int>>& BattleClears() {
    static auto clears = [] { std::set<std::pair<int,int>> result;
        std::ifstream file("local-test-battles.txt"); int mode,stage;
        while (file >> mode >> stage) if (FindCampaignStage(mode,stage)||FindBattleStage(mode,stage)||(mode==5&&FindFinalBoss(stage))||(mode==6&&FindDescent(stage))) result.insert({mode,stage});
        return result; }();
    return clears;
}
inline void SaveBattleProgress() {
    std::ofstream file("local-test-battles.txt.tmp",std::ios::trunc);
    for (const auto& row : BattleClears()) file << row.first << ' ' << row.second << '\n';
    file.close();
    if (!file || !MoveFileExW(L"local-test-battles.txt.tmp",L"local-test-battles.txt",MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH))
        throw std::runtime_error("Could not save battle progress");
}
// WeekData indexes its native first-clear bitmap in blocks of 60 bits.
inline std::vector<int64_t> WeekStageClearFlags() {
    std::vector<int64_t> flags;
    for (const auto& clear : BattleClears()) {
        if (clear.first != 1 || clear.second < 0) continue;
        const int index=WeekIndexForStage(clear.second);
        if(index<0)continue;
        const size_t block = size_t(index / 60);
        if (flags.size() <= block) flags.resize(block + 1, 0);
        flags[block] |= int64_t(1) << (index % 60);
    }
    return flags;
}
// Validate completion against the stage actually entered by this connection.
inline std::map<int,std::pair<int,int>>& ActiveBattles() {
    static std::map<int,std::pair<int,int>> active; return active;
}
inline std::map<int,std::vector<int>>& ActiveBattleHeroes(){static std::map<int,std::vector<int>> heroes;return heroes;}
}
