#pragma once
#include <map>
namespace GcLocal {
struct TeamSlot { uint8_t slot = 0; int hero = 0; uint8_t group = 0; int skin = 0, fateHero = 0; uint8_t fateGroup = 0; int fateSkin = 0; };
struct TeamState { std::vector<TeamSlot> slots; int bp = 0, buff = 0; };
struct ArtifactTeamState { uint8_t index=0; int unionId=0; std::vector<int> cards; };
inline std::map<int,ArtifactTeamState>& ArtifactTeams() {
    static auto rows=[] {std::map<int,ArtifactTeamState> result; std::ifstream f("local-test-artifact-teams.txt");
        int index,unionId,count; while(f>>index>>unionId>>count) {if(index<0||index>255||count<0||count>5)break;
            ArtifactTeamState t; t.index=uint8_t(index); t.unionId=unionId;
            for(int i=0,id;i<count&&f>>id;++i)t.cards.push_back(id);
            if(int(t.cards.size())==count)result[index]=t;
        } return result;}(); return rows;
}
inline void SaveArtifactTeams() {
    std::ofstream f("local-test-artifact-teams.txt.tmp",std::ios::trunc);
    for(const auto& p:ArtifactTeams()){f<<p.first<<' '<<p.second.unionId<<' '<<p.second.cards.size();for(int id:p.second.cards)f<<' '<<id;f<<'\n';}
    f.close();if(!f||!MoveFileExW(L"local-test-artifact-teams.txt.tmp",L"local-test-artifact-teams.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH))throw std::runtime_error("Could not save artifact teams");
}
inline std::map<int, TeamState>& Teams() {
    static std::map<int, TeamState> value = [] {
        std::map<int, TeamState> rows; std::ifstream file("local-test-teams.txt");
        int index, slot, hero, group, skin, fateHero, fateGroup, fateSkin, bp, buff;
        while (file >> index >> slot >> hero >> group >> skin >> fateHero >> fateGroup >> fateSkin >> bp >> buff)
            if (index >= 0 && index < 256 && slot >= 0 && slot < 8) {
                hero=CanonicalTgHero(hero);skin=CanonicalTgSkin(skin);
                fateHero=CanonicalTgHero(fateHero);fateSkin=CanonicalTgSkin(fateSkin);
                auto& t = rows[index];
                for(const auto& existing:t.slots)if(hero && existing.hero==hero){hero=0;skin=0;group=0;break;}
                t.slots.push_back({uint8_t(slot),hero,uint8_t(group),skin,fateHero,uint8_t(fateGroup),fateSkin}); t.bp=bp; t.buff=buff;
            }
        if (!rows.count(201)) for (uint8_t i=0;i<4;++i) rows[201].slots.push_back({i,i==0?1004001:0,0,i==0?300104:0,0,0,0});
        return rows;
    }(); return value;
}
inline void SaveTeams() {
    std::ofstream file("local-test-teams.txt.tmp",std::ios::trunc);
    for (const auto& t : Teams()) for (const auto& s : t.second.slots)
        file << t.first << ' ' << int(s.slot) << ' ' << s.hero << ' ' << int(s.group) << ' ' << s.skin << ' ' << s.fateHero << ' ' << int(s.fateGroup) << ' ' << s.fateSkin << ' ' << t.second.bp << ' ' << t.second.buff << '\n';
    file.close();
    if (!file || !MoveFileExW(L"local-test-teams.txt.tmp",L"local-test-teams.txt",MOVEFILE_REPLACE_EXISTING|MOVEFILE_WRITE_THROUGH)) throw std::runtime_error("Could not save teams");
}
}
