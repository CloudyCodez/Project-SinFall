"""Retarget original downloaded Vegeta/Gogeta skeletal attacks."""
import json
import build_db_legends_animations as a
FORMS=[('vegeta_base','d4ce14d6bf9b0ffafad0d25fff9671e4cc554b0b','Vegeta','b8491db0ed055b1b9a21c470ef82a5a68dbabbf7','Vegeta_SPA_GyallickHo'),('vegeta_super','d4ce14d6bf9b0ffafad0d25fff9671e4cc554b0b','Vegeta','b8491db0ed055b1b9a21c470ef82a5a68dbabbf7','Vegeta_SPA_GyallickHo'),('vegeta_blue','921db8c8af5d0e7d363e0f8f52b1615c8643df3a','VegetaSSGSS','795734530cf0c5ae19b2950fd518df72ec84c0d5','VegetaSSGSS_ULA_ULTIMATEATTACK'),('gogeta_blue','0078d08dd86329535d70b2ee86e03e38d82b4df5','GTB_05','cf64bd9148ba32c05dcb7ed675ba614cb62d8e8d','GTB_05_SPA_Kamehameha_ATC')]
if __name__=='__main__':
 for form in FORMS:a.build(*form,effect_base=198500020 if form[0]=='vegeta_blue' else 198500000 if form[0]=='gogeta_blue' else 198500010)
 (a.OUT/'br-m.bin').write_bytes(a.write(*a.ctx.manifest));(a.OUT/'assets.json').write_text(json.dumps(a.ctx.report,indent=2))
