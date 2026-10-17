#pragma once
#include <array>
#include "LocalStoryRules.h"
#include "LocalStoryInteractionsCatalog.h"
namespace GcLocal {
struct QuestRow { int id, next; std::vector<int> requirements, stages; };
extern const QuestRow QuestCatalog[2350];
inline const QuestRow* FindQuest(int id) { for (const auto& row : QuestCatalog) if (row.id == id) return &row; return nullptr; }
struct QuestState { uint8_t status = 1, interaction = 0; std::vector<int> progress; };
inline std::map<int,QuestState>& Quests() {
    static std::map<int,QuestState> rows = [] {
        std::map<int,QuestState> result; std::ifstream file("local-test-quests.txt");
        int id, status, interaction, count;
        while (file >> id >> status >> interaction >> count) {
            if (!FindQuest(id) || count < 0 || count > 100) break;
            QuestState row; row.status=uint8_t(status); row.interaction=uint8_t(interaction);
            for (int i=0,v;i<count && file>>v;++i) row.progress.push_back(v);
            result[id]=row;
        }
        if (result.empty()) result[1] = QuestState{1,0,{0}};
        return result;
    }(); return rows;
}
inline void SaveQuests() {
    std::ofstream file("local-test-quests.txt.tmp",std::ios::trunc);
    for (const auto& q : Quests()) {
        file << q.first << ' ' << int(q.second.status) << ' ' << int(q.second.interaction) << ' ' << q.second.progress.size();
        for (int count : q.second.progress) file << ' ' << count;
        file << '\n';
    }
    file.close();
    if (!file || !MoveFileExW(L"local-test-quests.txt.tmp",L"local-test-quests.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH)) throw std::runtime_error("Could not save quests");
}
inline void StartQuest(int id) {
    const auto* row = FindQuest(id); if (!row) throw std::runtime_error("Unknown quest");
    if (!Quests().count(id)) {
        QuestState s; s.progress.resize(row->requirements.size(),0); Quests()[id]=s;
        for(auto r:QuestItemRules)if(r.quest==id&&r.item&&r.count>0){Grant(r.item,r.count);break;}
    }
}
inline bool QuestCompleted(int id){auto it=Quests().find(id);return it!=Quests().end()&&it->second.status==2;}
inline bool CanStartQuest(int id){const auto* rule=FindQuestRule(id);return rule&&(!rule->parent||QuestCompleted(rule->parent));}
inline bool QuestReady(int id){const auto* row=FindQuest(id);auto it=Quests().find(id);return row&&it!=Quests().end()&&it->second.status==1&&it->second.progress==row->requirements;}
// Older profiles saved a campaign cursor without a per-stage ledger. Recover only
// its actual prerequisite chain, rather than treating every smaller ID as cleared.
inline bool CampaignStageCompleted(int id){
 if(BattleClears().count({0,id}))return true;
 int cursor=MainStageClear();std::set<int> visited;
 while(cursor&&visited.insert(cursor).second){
  if(cursor==id)return true;
  const auto* row=FindCampaignStage(0,cursor);if(!row)break;cursor=row->needStage;
 }
 return false;
}
inline bool CanEnterCampaign(int mode,int id){
 const auto* row=FindCampaignStage(mode,id);if(!row)return false;
 if(row->needStage&&!CampaignStageCompleted(row->needStage))return false;
 if(row->needQuest&&!QuestCompleted(row->needQuest))return false;
 if(row->startQuest){auto it=Quests().find(row->startQuest);if(it==Quests().end())return false;}
 return true;
}
// Native main-route checkpoints include sub_enemy/sub_reward rows. The
// combat classification "main" alone omits the road battle before Vanya.
inline int MainRouteCursor(){
 int cursor=MainStageClear();
 for(auto clear:BattleClears())if(clear.first==0){const auto* r=FindCampaignStage(0,clear.second);if(r&&r->mainRoute)cursor=(std::max)(cursor,r->id);}
 return cursor;
}
inline std::map<int,std::array<int,5>> SideRouteCursors(){
 std::map<int,std::array<int,5>> result;
 for(const auto& r:CampaignStages)if(r.mode==0&&r.region>0&&r.side>=1&&r.side<=5&&CampaignStageCompleted(r.id)){
  auto& top=result[r.region][r.side-1];top=(std::max)(top,r.id);
 }
 return result;
}
inline void RecordQuestBattle(int mode,int stage){
 for(auto& p:Quests()){
  const auto* row=FindQuest(p.first);const auto* rule=FindQuestRule(p.first);
  bool freeStage=mode==0&&FindCampaignStage(0,stage)&&!FindCampaignStage(0,stage)->main;
  if(!row||!rule||p.second.status!=1||(rule->stageMode>=0&&rule->stageMode!=mode&&!(rule->stageMode==4&&freeStage))||
     (std::string(rule->type)!="stage"&&std::string(rule->type)!="stage_array"&&std::string(rule->type)!="battle_quest_count"))continue;
  auto match=std::find(row->stages.begin(),row->stages.end(),stage);if(!row->stages.empty()&&match==row->stages.end())continue;
  if(p.second.progress.size()!=row->requirements.size())continue;
  size_t index=row->requirements.size()==1||row->stages.empty()?0:size_t(match-row->stages.begin());
  if(index<p.second.progress.size())p.second.progress[index]=(std::min)(row->requirements[index],p.second.progress[index]+1);
 }
 SaveQuests();
}
}
