"""Map boss-only models to native card/monster records before player conversion."""
from read_plain_table import read_table,root
import json
resources=read_table('DB_monster_resource','DBMonsterResourceRow');cards={((r['id']^0x66666666)&0xffffffff):r for r in read_table('DB_monster_skill','DBMonsterSkillRow')};monsters={((r['id']^0xc1c1c1c1)&0xffffffff):r for r in read_table('DB_monster_base','DBMonsterBaseRow')}
hero_models={r['character_base'] for r in read_table('DB_skin_costume_resource','DBSkinCostumeResourceRow')}
stages=json.loads((root/'Research/DecodedCache/DB_stage.json').read_text());story_ids={r.get(key,0) for r in stages if r['type'] in ['main','north_main','another_main','disaster_main','extra'] for key in [*(f'monster_id_{i}' for i in range(1,7)),*(f'boss_id_{i}' for i in range(1,5))]}
by_model={}
for r in resources:
 mid=(r['id']^0x50505050)&0xffffffff;model=r['character_base']
 if (mid not in story_ids and model not in ['demon_king_meliodas','monspeet_indura','derieri_indura']) or model in hero_models or not str(r['resource_body']).startswith('hero_'):continue
 if mid not in cards or mid not in monsters:continue
 c=cards[mid];decoded={k:(c[k]^0x66666666)&0xffffffff for k in ['skill_a_1_id','skill_a_2_id','skill_a_3_id','skill_b_1_id','skill_b_2_id','skill_b_3_id','special_id']}
 candidate={'monster_id':mid,'character_base':model,'body':r['resource_body'],'head':r['resource_head'],'portrait':r['potrait_base'],'animation_directory':r['ani_directory_name'],'cards':decoded,'has_two_ranked_cards_and_ultimate':all(decoded.values()),'shop_price_sr_coins':30,'status':'needs_player_hero_and_cosmetic_records_and_runtime_validation'}
 by_model.setdefault(model,[]).append(candidate)
report={'priority':['demon_king_meliodas','monspeet_indura','derieri_indura'],'story_boss_models':by_model,'native_hero_models_excluded':len(hero_models)}
(root/'dist/story-boss-conversion-map.json').write_text(json.dumps(report,indent=2));print('Mapped',len(by_model),'story-only model groups');print({k:len(v) for k,v in by_model.items() if k in report['priority']})
