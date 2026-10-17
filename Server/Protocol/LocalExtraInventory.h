#pragma once
#include <map>
#include <set>
namespace GcLocal {
inline std::map<int,int>& ExtraItems() {
    static auto rows=[] {std::map<int,int> result;std::ifstream file("local-test-extra-items.txt");int id,count;
        while(file>>id>>count)if(id>0&&count>=0)result[id]=count;return result;}();return rows;
}
inline std::set<int>& Artifacts() {
    static auto rows=[] {std::set<int> result;std::ifstream file("local-test-artifacts.txt");int id;
        while(file>>id)if(id>0)result.insert(id);return result;}();return rows;
}
inline void SaveExtraInventory() {
    std::ofstream file("local-test-extra-items.txt.tmp",std::ios::trunc);
    for(const auto& row:ExtraItems())file<<row.first<<' '<<row.second<<'\n';file.close();
    if(!file||!MoveFileExW(L"local-test-extra-items.txt.tmp",L"local-test-extra-items.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save inventory");
    std::ofstream cards("local-test-artifacts.txt.tmp",std::ios::trunc);
    for(int id:Artifacts())cards<<id<<'\n';cards.close();
    if(!cards||!MoveFileExW(L"local-test-artifacts.txt.tmp",L"local-test-artifacts.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save artifacts");
}
}
