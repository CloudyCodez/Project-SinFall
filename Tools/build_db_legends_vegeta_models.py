"""Convert exact downloaded Vegeta/Gogeta ModelOrder references."""
import json
import build_db_legends_models as c
FORMS=[dict(name='vegeta_base',order='9ad77cb9544574e8874773d888d92b529b32054f'),dict(name='vegeta_super',order='8bdf05010e929650ab43ce71c48c949e159e1335'),dict(name='vegeta_blue',order='2a306ffc871a12fd8de91d3876df760c87108309'),dict(name='gogeta_blue',order='9ed73024de7a66781045bd83abcbfb15fbf00591')]
if __name__=='__main__':
 for f in FORMS:c.build(f)
 (c.OUT/'br-m.bin').write_bytes(c.write(*c.manifest));(c.OUT/'assets.json').write_text(json.dumps(c.report,indent=2))
