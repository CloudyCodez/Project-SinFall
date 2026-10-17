#pragma once
#include "LocalProgressionCatalog.h"
namespace GcLocal {
struct MissionState { int claimed=0,progress=0; };
inline const MissionRule* FindMission(int chain,int index){for(const auto& r:MissionRules)if(r.chain==chain&&r.index==index)return &r;return nullptr;}
inline std::map<int,MissionState>& Missions(){
 static std::map<int,MissionState> rows=[] {std::map<int,MissionState> rows;for(auto r:MissionRules)rows.emplace(r.chain,MissionState{});
  std::ifstream f("local-test-missions.txt");int chain,index,progress;while(f>>chain>>index>>progress)if(rows.count(chain)&&index>=0&&index<=255&&progress>=0&&(index==0||FindMission(chain,index)))rows[chain]={index,progress};return rows;}();return rows;
}
inline void SaveMissions(){std::ofstream f("local-test-missions.txt.tmp",std::ios::trunc);for(auto p:Missions())f<<p.first<<' '<<p.second.claimed<<' '<<p.second.progress<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-missions.txt.tmp",L"local-test-missions.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save missions");}
inline bool& MissionClientReady(){static bool ready=false;return ready;}
inline int AccountRank(){int level=1;for(auto r:AccountLevels)if(AccountExperience()>=r.exp)level=(std::max)(level,r.level+1);return level;}
inline void RefreshMissionSnapshots(){for(auto& p:Missions()){const auto* r=FindMission(p.first,p.second.claimed+1);if(!r)continue;
 int value=-1;if(r->type==1)value=AccountRank();else if(r->type==3&&!r->value)value=int(OwnedHeroes().size());else if(r->type==4&&!r->value)value=int(OwnedSkins().size());
 if(value>=0)p.second.progress=(std::max)(p.second.progress,value);
}}
inline void RecordMission(int type,int value,int count){if(count<=0)return;for(auto& p:Missions()){
 const auto* r=FindMission(p.first,p.second.claimed+1);if(!r||r->type!=type||(r->value&&r->value!=value))continue;
 p.second.progress=int(std::min<int64_t>(2147483647LL,int64_t(p.second.progress)+count));
 }SaveMissions();}
inline int AchievementPoints(){int points=0;for(auto r:MissionRules)if(Missions().at(r.chain).claimed>=r.index)points+=r.points;return points;}
struct ProgressionState {int achievementOrder=0,guideStep=0;bool guideRewarded=false,guideFinal=false;uint64_t chapterFlags=0;};
inline ProgressionState& Progression(){static ProgressionState s=[] {ProgressionState s;std::ifstream f("local-test-progression.txt");f>>s.achievementOrder>>s.guideStep>>s.guideRewarded>>s.guideFinal>>s.chapterFlags;s.achievementOrder=(std::max)(0,(std::min)(30,s.achievementOrder));s.guideStep=(std::max)(0,(std::min)(20,s.guideStep));return s;}();return s;}
inline void SaveProgression(){const auto& s=Progression();std::ofstream f("local-test-progression.txt.tmp",std::ios::trunc);f<<s.achievementOrder<<' '<<s.guideStep<<' '<<s.guideRewarded<<' '<<s.guideFinal<<' '<<s.chapterFlags<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-progression.txt.tmp",L"local-test-progression.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save progression");}
inline int GuideStepForQuest(int id){for(auto q:GuideQuests)if(q.quest==id)return q.step;return 0;}
inline bool GuideStepComplete(){const auto& s=Progression();int found=0;for(auto q:GuideQuests)if(q.step==s.guideStep){++found;if(!QuestCompleted(q.quest))return false;}return found>0;}
inline bool SnapshotQuestType(const std::string& type){return type=="weapon_upgrade_level"||type=="weapon_evolution_level"||type=="player_rank"||type=="hero_awaken"||type=="hero_awaken_count"||type=="hero_transcend"||type=="weapon_equip_count";}
inline void RefreshQuestSnapshots(){
 for(auto& p:Quests()){const auto* r=FindQuestRule(p.first);const auto* q=FindQuest(p.first);if(!r||!q||p.second.status!=1)continue;
  if(GuideStepForQuest(p.first)&&std::string(r->type)=="stage"&&q->requirements==std::vector<int>{1}&&q->stages.size()==1){int mode=r->stageMode;bool complete=(mode==0||mode==4)?CampaignStageCompleted(q->stages[0]):BattleClears().count({mode,q->stages[0]})>0;if(complete)p.second.progress={1};}
  if(!SnapshotQuestType(r->type))continue;
  std::string type=r->type;int need=r->needs.empty()?0:r->needs[0],value=0;
  if(type=="player_rank")value=AccountRank()>=need?1:0;
  else if(type=="weapon_upgrade_level"||type=="weapon_evolution_level"){for(auto w:Equipments())if((type=="weapon_upgrade_level"?w.second.upgrade:w.second.evolution)>=need)++value;}
  else if(type=="weapon_equip_count"){for(auto w:Equipments())if(w.second.skin)++value;}
  else for(int skin:OwnedSkins()){const auto& state=DevelopmentStates()[skin];
   if(type=="hero_awaken"&&FindSkin(skin)->hero==need)value=(std::max)(value,state.awaken);
   else if(type=="hero_awaken_count"&&state.awaken>=need)++value;
   else if(type=="hero_transcend"&&state.transcend>=need)++value;
  }
  if(p.second.progress.size()==1)p.second.progress[0]=(std::max)(p.second.progress[0],(std::min)(q->requirements[0],value));
 }
}
inline const ChapterRule* FindChapter(int region){for(const auto& r:ChapterRules)if(r.region==region)return &r;return nullptr;}
inline bool ChapterComplete(const ChapterRule& r){if(r.quests.empty())return false;for(int id:r.quests)if(!QuestCompleted(id))return false;return true;}
}
