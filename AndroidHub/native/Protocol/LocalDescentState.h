#pragma once
namespace GcLocal {
inline constexpr int DescentEventSequence=140001,DescentEventSubIndex=1000001,DescentPointItem=912305;
inline int DescentClearFlags(){int flags=0;for(auto r:DescentStages)if(BattleClears().count({6,r.id}))flags|=1<<r.index;return flags;}
inline int& DescentRewardFlags(){static int flags=[] {int value=0;std::ifstream f("local-test-descent-rewards.txt");f>>value;return value>=0&&(value&~62)==0?value:0;}();return flags;}
inline void SaveDescentRewards(){std::ofstream f("local-test-descent-rewards.txt.tmp",std::ios::trunc);f<<DescentRewardFlags();f.close();if(!f||!MoveFileExW(L"local-test-descent-rewards.txt.tmp",L"local-test-descent-rewards.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save event boss rewards");}
struct DescentPointReward{int step,needed,item,count;};
// The historic Crocshell reward table is absent. Reuse the preserved five-tier event point track with Crocshell's own point item.
inline constexpr DescentPointReward DescentPointRewards[]={{1,3,900906,15},{2,6,1260127,40},{3,9,542405,3},{4,12,1260128,40},{5,15,5301001,5}};
}
