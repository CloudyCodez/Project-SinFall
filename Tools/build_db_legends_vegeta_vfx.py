"""Convert Vegeta's original Galick Gun and Final Flash particle prefabs."""
import json
import build_db_legends_vfx as v
EFFECTS=[]
for namespace,file,names,base in [
 ('vegeta','04b9f2f248b8531c1e7b40d98ab89b7abc5fa415',
  ['galickgun_crg01','galickgun_beam','galickgun_beamend','galickgun_crg02'],198500010),
 ('vegeta_blue','2c4205c186be8d575f7aa172f891d39410b540c7',
  ['finalflash_crg','finalflash_beambody','finalflash_fireend','finalflash_fire'],198500020),
]:
 for offset,(label,name) in enumerate(zip(['charge','beam','impact','release'],names),1):
  EFFECTS.append((label,name,base+offset,file,namespace))
if __name__=='__main__':
 for effect in EFFECTS:v.build(*effect)
 (v.c.OUT/'br-m.bin').write_bytes(v.c.write(*v.c.manifest))
 (v.c.OUT/'assets.json').write_text(json.dumps(v.c.report,indent=2))
 (v.c.ROOT/'Research/DBLegends/vegeta-vfx-registration.json').write_text(json.dumps([
  dict(id=id,path='DragonBall/'+namespace,filename='fx_'+namespace+'_'+label)
  for label,name,id,file,namespace in EFFECTS],indent=2))
