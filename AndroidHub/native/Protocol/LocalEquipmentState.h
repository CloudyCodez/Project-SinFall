#pragma once
#include <sstream>
#include "LocalSystemsCatalog.h"
namespace GcLocal {
struct EquipmentState {int serial=0,base=0,upgrade=0,evolution=0,value=0,carve=0,skin=0,slot=0;bool locked=false;std::vector<std::pair<int,int>> options;};
inline const EquipmentBase* EquipmentBaseRow(int id){for(const auto& r:EquipmentBaseRows)if(r.id==id)return &r;return nullptr;}
inline std::map<int,EquipmentState>& Equipments(){static auto rows=[] {
    BackupTgWardrobeSaves();std::map<int,EquipmentState> r;std::ifstream f("local-test-equipment.txt");std::string line;
    while(std::getline(f,line)){std::istringstream in(line);EquipmentState w;int count=0;
        if(!(in>>w.serial>>w.base>>w.upgrade>>w.evolution>>w.value>>w.carve>>w.skin>>w.slot>>w.locked>>count)||!EquipmentBaseRow(w.base)||count<0||count>5)continue;
        for(int i=0,id,value;i<count&&in>>id>>value;++i)w.options.emplace_back(id,value);r[w.serial]=w;
    }
    std::set<std::pair<int,int>> occupied;
    for(const auto& p:r)if(p.second.skin && !IsTgWardrobeSkin(p.second.skin))occupied.insert({p.second.skin,p.second.slot});
    for(auto& p:r)if(IsTgWardrobeSkin(p.second.skin)){
        auto& w=p.second;w.skin=CanonicalTgSkin(w.skin);
        if(!occupied.insert({w.skin,w.slot}).second){w.skin=0;w.slot=0;}
    }
    return r;}();return rows;}
inline void SaveEquipments(){std::ofstream f("local-test-equipment.txt.tmp",std::ios::trunc);for(auto p:Equipments()){const auto& w=p.second;f<<w.serial<<' '<<w.base<<' '<<w.upgrade<<' '<<w.evolution<<' '<<w.value<<' '<<w.carve<<' '<<w.skin<<' '<<w.slot<<' '<<w.locked<<' '<<w.options.size();for(auto o:w.options)f<<' '<<o.first<<' '<<o.second;f<<'\n';}f.close();if(!f||!MoveFileExW(L"local-test-equipment.txt.tmp",L"local-test-equipment.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save equipment");}
inline EquipmentState& CreateEquipment(int id,bool developed=false){const auto* base=EquipmentBaseRow(id);if(!base)throw std::runtime_error("Invalid equipment base");int serial=Equipments().empty()?1:Equipments().rbegin()->first+1;EquipmentState w;w.serial=serial;w.base=id;w.value=base->status_value_max;if(developed){w.upgrade=5;w.evolution=5;for(int i=0;i<5;++i){const EquipmentOption* option=nullptr;for(const auto& o:EquipmentOptionRows)if(o.random_option_group==base->random_option_id){option=&o;break;}if(option)w.options.emplace_back(option->id,option->option_effect_max);}}Equipments()[serial]=w;return Equipments().at(serial);}
inline std::set<int>& CraftedCosmetics(){static auto r=[] {std::set<int> s;std::ifstream f("local-test-crafted-cosmetics.txt");int id;while(f>>id)if(FindCosmetic(id))s.insert(id);return s;}();return r;}
inline void SaveCraftedCosmetics(){std::ofstream f("local-test-crafted-cosmetics.txt.tmp",std::ios::trunc);for(int id:CraftedCosmetics())f<<id<<'\n';f.close();if(!f||!MoveFileExW(L"local-test-crafted-cosmetics.txt.tmp",L"local-test-crafted-cosmetics.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save relic ownership");}
inline bool OwnCosmetic(int id){if(CraftedCosmetics().count(id))return true;const int hero=TgWardrobeHero(id);if(hero && OwnedHeroes().count(hero))return true;if(!CustomMode())return false;for(auto r:RelicRecipeRows)if(r.costume_id==id)return false;return true;}
inline void ReplaceEquipmentSkin(int oldId,int newId){for(auto& p:Equipments())if(p.second.skin==oldId)p.second.skin=newId;SaveEquipments();}
}
