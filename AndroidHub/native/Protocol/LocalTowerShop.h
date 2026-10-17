#pragma once
#include <ctime>
namespace GcLocal {
struct TowerShopProduct {int id,item,count,price,amount,dailyLimit,totalLimit;};
inline constexpr TowerShopProduct TowerShopProducts[]={
{1,542405,1,500083,300,0,3},
{2,520001,1,500083,180,0,5},
{3,5301001,1,500083,160,0,7},
{4,941017,1,500083,10,0,20},
{5,543219,15,500083,250,0,2},
{6,543221,15,500083,250,0,2},
{7,543207,1,500083,1000,0,1},
{8,543208,1,500083,1000,0,1},
{9,6010050,1,500083,300,0,1},
{10,6040045,1,500083,300,0,1},
{11,6201001,1,500084,50,0,5},
{12,6200001,1,500084,50,0,5},
{13,6203001,1,500084,50,0,5},
{14,6205001,1,500084,50,0,5},
{15,6202001,1,500084,50,0,5},
{16,6040036,1,500084,300,0,1},
{17,510001,100,500084,100,0,3},
{18,530001,100,500084,300,0,3},
{19,543219,10,500084,100,0,5},
{20,543221,10,500084,100,0,5},
{21,543220,10,500084,100,0,5},
{22,543209,1,500084,1000,0,1},
{23,6040042,1,500084,300,0,1},
{24,543210,1,500084,1000,0,1},
{25,542701,1,500085,1000,0,1},
{26,543215,1,500085,350,0,2},
{27,543216,1,500085,350,0,2},
{28,543217,1,500085,350,0,2},
{29,543218,1,500085,350,0,2},
{30,6010040,1,500085,300,0,1},
{31,6030073,1,500085,300,0,1},
{32,543222,1,500085,1000,0,1},
{33,6020067,1,500085,300,0,1},
{34,6020068,1,500085,300,0,1},
{35,6040063,1,500085,300,0,1},
};
inline const TowerShopProduct* FindTowerShopProduct(int id){for(const auto& p:TowerShopProducts)if(p.id==id)return &p;return nullptr;}
inline int TowerShopRewardType(int id){if(!FindTowerShopProduct(id))return 0;const auto* r=FindTowerShopProduct(id);if(r->item>=6000000&&r->item<6100000)return 216;return FinalBossRewardType(r->item);}
struct TowerShopPurchase {int day=0,daily=0,total=0;};
inline int TowerShopToday(){return int(std::time(nullptr)/86400);}
inline int TowerShopDaily(const TowerShopPurchase& p){return p.day==TowerShopToday()?p.daily:0;}
inline std::map<int,TowerShopPurchase>& TowerShopPurchases(){static std::map<int,TowerShopPurchase> r=[] {std::map<int,TowerShopPurchase> v;std::ifstream f("local-test-tower-shop.txt");int id;TowerShopPurchase p;while(f>>id>>p.day>>p.daily>>p.total)if(FindTowerShopProduct(id)&&p.daily>=0&&p.daily<=255&&p.total>=0&&p.total<=255)v[id]=p;return v;}();return r;}
inline void SaveTowerShopPurchases(){std::ofstream f("local-test-tower-shop.txt.tmp",std::ios::trunc);for(auto p:TowerShopPurchases())f<<p.first<<' '<<p.second.day<<' '<<p.second.daily<<' '<<p.second.total<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-tower-shop.txt.tmp",L"local-test-tower-shop.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save Tower shop purchases");}
}
