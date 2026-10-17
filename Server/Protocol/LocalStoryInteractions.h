#pragma once
#include <ctime>
#include "LocalStoryInteractionsCatalog.h"
namespace GcLocal {
inline std::map<int,int>& RecipeExperience(){
 static std::map<int,int> rows=[] {std::map<int,int> rows;std::ifstream f("local-test-recipes.txt");int id,exp;while(f>>id>>exp)for(auto r:RecipeRules)if(r.id==id){rows[id]=(std::max)(0,(std::min)(exp,r.maxExp));break;}return rows;}();return rows;
}
inline void SaveRecipes(){std::ofstream f("local-test-recipes.txt.tmp",std::ios::trunc);for(auto p:RecipeExperience())f<<p.first<<' '<<p.second<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-recipes.txt.tmp",L"local-test-recipes.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save recipes");}
inline std::map<int,int>& TownShopCounts(){
 static std::map<int,int> rows=[] {std::map<int,int> rows;std::ifstream f("local-test-town-shops.txt");long long day;int id,count;if(f>>day&&day==std::time(nullptr)/86400)while(f>>id>>count)if(count>=0&&count<=255)rows[id]=count;return rows;}();
 static long long day=std::time(nullptr)/86400;long long today=std::time(nullptr)/86400;if(today!=day){rows.clear();day=today;}return rows;
}
inline void SaveTownShops(){std::ofstream f("local-test-town-shops.txt.tmp",std::ios::trunc);f<<std::time(nullptr)/86400<<'\n';for(auto p:TownShopCounts())f<<p.first<<' '<<p.second<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-town-shops.txt.tmp",L"local-test-town-shops.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save town purchases");}
inline const TownShopRule* FindTownProduct(int id){for(const auto& r:TownShopRules)if(r.id==id)return &r;return nullptr;}
inline void RecordQuestAction(const char* type,int need,int count){
 for(auto& p:Quests()){
  const auto* rule=FindQuestRule(p.first);const auto* row=FindQuest(p.first);
  if(!rule||!row||p.second.status!=1||std::string(rule->type)!=type)continue;
  if(rule->needs.empty()&&!p.second.progress.empty()&&!row->requirements.empty())p.second.progress[0]=int(std::min<int64_t>(row->requirements[0],int64_t(p.second.progress[0])+count));
  for(size_t i=0;i<rule->needs.size()&&i<p.second.progress.size()&&i<row->requirements.size();++i)
   if(rule->needs[i]==need)p.second.progress[i]=int(std::min<int64_t>(row->requirements[i],int64_t(p.second.progress[i])+count));
 }
 SaveQuests();
}
}
