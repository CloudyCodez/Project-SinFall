"""Package the permanent summon DB and install it before Unity initializes."""
from pathlib import Path
import hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];decoded=ROOT/'Research/PhoneClientDecoded'
name='30FF13B981773B83827E17DB9C456368';source=ROOT/'dist/cache/b'/name
asset=decoded/'assets/offline-db'/name;asset.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,asset)
version=hashlib.sha256(source.read_bytes()).hexdigest()
helper=decoded/'smali/com/phoenix/offline/SummonCatalog.smali';helper.parent.mkdir(parents=True,exist_ok=True)
helper.write_text('''.class public final Lcom/phoenix/offline/SummonCatalog;
.super Ljava/lang/Object;
.method public static install(Landroid/content/Context;)V
    .locals 8
    :try_start
    const-string v0, "offline_catalog"
    const/4 v1, 0x0
    invoke-virtual {p0, v0, v1}, Landroid/content/Context;->getSharedPreferences(Ljava/lang/String;I)Landroid/content/SharedPreferences;
    move-result-object v7
    const-string v0, "version"
    const-string v1, ""
    invoke-interface {v7, v0, v1}, Landroid/content/SharedPreferences;->getString(Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;
    move-result-object v1
    const-string v2, "VERSION"
    invoke-virtual {v2, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v1
    if-nez v1, :done
    const/4 v0, 0x0
    invoke-virtual {p0, v0}, Landroid/content/Context;->getExternalFilesDir(Ljava/lang/String;)Ljava/io/File;
    move-result-object v0
    if-eqz v0, :done
    new-instance v1, Ljava/io/File;
    const-string v2, "bm/b"
    invoke-direct {v1, v0, v2}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V
    invoke-virtual {v1}, Ljava/io/File;->mkdirs()Z
    new-instance v2, Ljava/io/File;
    const-string v3, "HASH"
    invoke-direct {v2, v1, v3}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V
    new-instance v3, Ljava/io/File;
    const-string v4, "HASH.tmp"
    invoke-direct {v3, v1, v4}, Ljava/io/File;-><init>(Ljava/io/File;Ljava/lang/String;)V
    invoke-virtual {p0}, Landroid/content/Context;->getAssets()Landroid/content/res/AssetManager;
    move-result-object v0
    const-string v1, "offline-db/HASH"
    invoke-virtual {v0, v1}, Landroid/content/res/AssetManager;->open(Ljava/lang/String;)Ljava/io/InputStream;
    move-result-object v0
    new-instance v1, Ljava/io/FileOutputStream;
    invoke-direct {v1, v3}, Ljava/io/FileOutputStream;-><init>(Ljava/io/File;)V
    const v4, 0x8000
    new-array v4, v4, [B
    :copy
    invoke-virtual {v0, v4}, Ljava/io/InputStream;->read([B)I
    move-result v5
    if-lez v5, :copied
    const/4 v6, 0x0
    invoke-virtual {v1, v4, v6, v5}, Ljava/io/FileOutputStream;->write([BII)V
    goto :copy
    :copied
    invoke-virtual {v0}, Ljava/io/InputStream;->close()V
    invoke-virtual {v1}, Ljava/io/FileOutputStream;->getFD()Ljava/io/FileDescriptor;
    move-result-object v0
    invoke-virtual {v0}, Ljava/io/FileDescriptor;->sync()V
    invoke-virtual {v1}, Ljava/io/FileOutputStream;->close()V
    invoke-virtual {v3, v2}, Ljava/io/File;->renameTo(Ljava/io/File;)Z
    move-result v0
    if-eqz v0, :done
    invoke-interface {v7}, Landroid/content/SharedPreferences;->edit()Landroid/content/SharedPreferences$Editor;
    move-result-object v0
    const-string v1, "version"
    const-string v2, "VERSION"
    invoke-interface {v0, v1, v2}, Landroid/content/SharedPreferences$Editor;->putString(Ljava/lang/String;Ljava/lang/String;)Landroid/content/SharedPreferences$Editor;
    invoke-interface {v0}, Landroid/content/SharedPreferences$Editor;->apply()V
    const-string v0, "GCOfflineCatalog"
    const-string v1, "Installed three-banner summon catalog"
    invoke-static {v0, v1}, Landroid/util/Log;->i(Ljava/lang/String;Ljava/lang/String;)I
    :try_end
    goto :done
    .catch Ljava/lang/Exception; {:try_start .. :try_end} :failed
    :failed
    move-exception v0
    const-string v1, "GCOfflineCatalog"
    const-string v2, "Cannot install summon catalog"
    invoke-static {v1, v2, v0}, Landroid/util/Log;->e(Ljava/lang/String;Ljava/lang/String;Ljava/lang/Throwable;)I
    :done
    return-void
.end method
'''.replace('VERSION',version).replace('HASH',name))
shutil.copy2(ROOT/'dist/cache/br-b.bin',decoded/'assets/offline-db/br-b.bin')
body=helper.read_text().split('.method public static install',1)[1]
body=('.method public static installManifest'+body).replace(name,'br-b.bin').replace('"bm/b"','"bm"').replace('"offline_catalog"','"offline_catalog_manifest"')
with helper.open('a') as f:f.write(body)
activity=decoded/'smali_classes3/com/netmarble/fpplugin/FPActivity.smali';text=activity.read_text()
call='    invoke-static {p0}, Lcom/phoenix/offline/SummonCatalog;->install(Landroid/content/Context;)V\n\n'
manifest_call='    invoke-static {p0}, Lcom/phoenix/offline/SummonCatalog;->installManifest(Landroid/content/Context;)V\n\n'
marker='    invoke-super {p0, p1}, Lcom/netmarble/unity/NMGUnityPlayerActivity;->onCreate(Landroid/os/Bundle;)V'
assert marker in text
if call.strip() not in text:text=text.replace(marker,call+marker)
if manifest_call.strip() not in text:text=text.replace(marker,manifest_call+marker)
activity.write_text(text)
print('Packaged summon DB',version)
