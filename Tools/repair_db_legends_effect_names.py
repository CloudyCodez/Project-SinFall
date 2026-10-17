"""Correct previously built Legends effects to match native pool lookup keys."""
from pathlib import PurePosixPath
import json
import build_db_legends_models as c
count=0
for row in list(c.report):
 if not row['logical'].startswith('phoenix_dbl_') or '_vfx_' not in row['logical']:continue
 e=c.UnityPy.load(str(c.OUT/row['file']))
 paths=[(p,v.asset.m_PathID) for o in e.objects if o.type.name=='AssetBundle' for p,v in o.read().m_Container]
 for path,objid in paths:
  if not path.endswith('.prefab'):continue
  o=e.assets[0].objects[objid];assert o.type.name=='GameObject'
  t=o.read_typetree();t['m_Name']=PurePosixPath(path).stem;o.save_typetree(t)
 deps=c.bundles[c.bundle_key(row['file'])]['deps'];c.report.remove(row);c.emit(e,row['logical'],paths,deps);count+=1
(c.OUT/'br-m.bin').write_bytes(c.write(*c.manifest))
(c.OUT/'assets.json').write_text(json.dumps(c.report,indent=2))
print('Corrected',count,'native effect pool names')
