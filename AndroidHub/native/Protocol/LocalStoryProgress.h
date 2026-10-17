#pragma once
#include <fstream>
namespace GcLocal {
inline int& MainStageClear() {
    static int stage = [] { int value = 100101; std::ifstream file("local-test-story.txt"); file >> value; return value; }();
    return stage;
}
inline void SaveStoryProgress() {
    std::ofstream file("local-test-story.txt.tmp", std::ios::trunc);
    file << MainStageClear() << '\n'; file.close();
    if (!file || !MoveFileExW(L"local-test-story.txt.tmp", L"local-test-story.txt", MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH))
        throw std::runtime_error("Could not save story progress");
}
inline int& AccountExperience(){static int value=[] {int exp=0;std::ifstream f("local-test-account-exp.txt");f>>exp;return (std::max)(0,exp);}();return value;}
inline void SaveAccountExperience(){std::ofstream f("local-test-account-exp.txt.tmp",std::ios::trunc);f<<AccountExperience()<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-account-exp.txt.tmp",L"local-test-account-exp.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save account experience");}
}
