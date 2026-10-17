from pathlib import Path
import re,shutil
ROOT=Path(__file__).resolve().parents[1];source=ROOT/'Research/PhoneClientSmali';target=ROOT/'Research/PhoneClientDecoded'
count=0
for directory in source.glob('smali*'):
 if not directory.is_dir():continue
 dest=target/directory.name
 shutil.copytree(directory,dest,dirs_exist_ok=True)
 for p in dest.rglob('*.smali'):
  text=p.read_text()
  def replace(m):
   global count
   count+=1;reg=m.group(2)
   return f'    invoke-static {{{reg}}}, Lcom/phoenix/offline/Bootstrap;->rewrite(Ljava/lang/String;)Ljava/lang/String;\n\n    move-result-object {reg}\n\n'+m.group(0)
  text=re.sub(r'    invoke-direct \{([vp]\d+), ([vp]\d+)\}, Ljava/net/URL;-><init>\(Ljava/lang/String;\)V',replace,text)
  p.write_text(text)
helper=target/'smali/com/phoenix/offline/Bootstrap.smali';helper.parent.mkdir(parents=True,exist_ok=True)
helper.write_text('''.class public final Lcom/phoenix/offline/Bootstrap;
.super Ljava/lang/Object;
.method public static rewrite(Ljava/lang/String;)Ljava/lang/String;
    .locals 3
    if-eqz p0, :unchanged
    const-string v0, "https://nmss.gcdn.netmarble.com/"
    invoke-virtual {p0, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
    move-result v0
    if-eqz v0, :unchanged
    const/16 v0, 0x2f
    invoke-virtual {p0, v0}, Ljava/lang/String;->lastIndexOf(I)I
    move-result v0
    add-int/lit8 v0, v0, 0x1
    invoke-virtual {p0, v0}, Ljava/lang/String;->substring(I)Ljava/lang/String;
    move-result-object v1
    new-instance v2, Ljava/lang/StringBuilder;
    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V
    const-string v0, "http://127.0.0.1:5100/"
    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;
    invoke-virtual {v2}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;
    move-result-object p0
    :unchanged
    return-object p0
.end method
''')
for p in target.glob('classes*.dex'):p.unlink()
print('Patched',count,'URL construction sites; only NMSS URLs are redirected')
