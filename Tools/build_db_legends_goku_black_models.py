"""Convert the downloaded Legends Goku Black/Rosé ModelOrder pair."""
import json
import build_db_legends_models as c
FORMS=[
 dict(name='goku_black',order='0c3e3fe51f2da7265fcd07aff6f32f1a995d9105'),
 dict(name='goku_black_rose',order='311dbd63cf48d5ffc971b7f606f99adf26a18a54'),
]
if __name__=='__main__':
 for form in FORMS:c.build(form)
 (c.OUT/'br-m.bin').write_bytes(c.write(*c.manifest))
 (c.OUT/'assets.json').write_text(json.dumps(c.report,indent=2))
