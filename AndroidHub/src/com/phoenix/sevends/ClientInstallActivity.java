package com.phoenix.sevends;

import android.app.*;
import android.os.*;
import android.content.*;
import android.content.pm.PackageInstaller;
import android.net.Uri;
import android.provider.Settings;
import android.widget.*;
import com.phoenix.offline.ReleaseFiles;
import org.json.*;
import java.io.*;
import java.security.*;

public final class ClientInstallActivity extends Activity {
 private TextView status;private Button start;private Thread worker;
 @Override public void onCreate(Bundle state){super.onCreate(state);
  LinearLayout layout=new LinearLayout(this);layout.setOrientation(1);layout.setPadding(32,48,32,24);
  status=new TextView(this);status.setTextSize(18);status.setText("Install the offline game\n\nThe Hub downloads and verifies the client. Android will ask you to approve installation. Open the game afterward to download its assets automatically. Keep setup open during downloads. You need about 24 GB free for a fresh setup.");layout.addView(status);
  start=new Button(this);start.setText("Download / install client");start.setOnClickListener(v->begin());layout.addView(start);setContentView(layout);result(getIntent());
 }
 private void report(String s){runOnUiThread(()->status.setText(s));}
 @Override protected void onNewIntent(Intent i){super.onNewIntent(i);setIntent(i);result(i);}
 private void result(Intent i){if(!i.hasExtra(PackageInstaller.EXTRA_STATUS))return;int code=i.getIntExtra(PackageInstaller.EXTRA_STATUS,-999);
  if(code==PackageInstaller.STATUS_PENDING_USER_ACTION){Intent confirm=i.getParcelableExtra(Intent.EXTRA_INTENT);if(confirm!=null)startActivity(confirm);}
  else if(code==PackageInstaller.STATUS_SUCCESS){report("Client installed. Open the game to download its asset packs, then start the Hub server and play.");File[] files=new File(getExternalFilesDir(null),"client-downloads").listFiles();if(files!=null)for(File f:files)f.delete();}
  else report("Android did not install the client: "+i.getStringExtra(PackageInstaller.EXTRA_STATUS_MESSAGE));
 }
 private void begin(){
  if(!getPackageManager().canRequestPackageInstalls()){startActivity(new Intent(Settings.ACTION_MANAGE_UNKNOWN_APP_SOURCES,Uri.parse("package:"+getPackageName())));return;}
  if(worker!=null&&worker.isAlive())return;start.setEnabled(false);getWindow().addFlags(128);
  worker=new Thread(()->{PowerManager.WakeLock wake=null;PackageInstaller.Session session=null;int id=-1;boolean committed=false;
   try{
    wake=((PowerManager)getSystemService(POWER_SERVICE)).newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,"SinFall:ClientSetup");wake.acquire(4*60*60*1000L);
    JSONObject manifest=ReleaseFiles.manifest(),client=manifest.getJSONObject("client");JSONArray parts=client.getJSONArray("parts");
    File root=getExternalFilesDir(null);if(root==null)throw new IOException("App storage unavailable");File folder=new File(root,"client-downloads");
    for(int p=0;p<parts.length();p++)ReleaseFiles.download(parts.getJSONObject(p),folder,this::report);
    if(root.getUsableSpace()<client.getLong("size")+67108864L)throw new IOException("Not enough space to stage the APK installation");
    PackageInstaller installer=getPackageManager().getPackageInstaller();PackageInstaller.SessionParams params=new PackageInstaller.SessionParams(PackageInstaller.SessionParams.MODE_FULL_INSTALL);
    params.setAppPackageName("com.netmarble.nanagb");params.setSize(client.getLong("size"));id=installer.createSession(params);session=installer.openSession(id);
    MessageDigest hash=MessageDigest.getInstance("SHA-256");long total=0;report("Preparing verified Android installation…");
    try(OutputStream out=session.openWrite("base.apk",0,client.getLong("size"))){byte[] b=new byte[262144];
     for(int p=0;p<parts.length();p++){try(InputStream in=new FileInputStream(new File(folder,parts.getJSONObject(p).getString("name")))){int n;while((n=in.read(b))!=-1){total+=n;hash.update(b,0,n);out.write(b,0,n);}}}session.fsync(out);
    }
    StringBuilder digest=new StringBuilder();for(byte v:hash.digest())digest.append(String.format("%02x",v&255));
    if(total!=client.getLong("size")||!digest.toString().equals(client.getString("sha256")))throw new IOException("Combined APK checksum mismatch");
    Intent callback=new Intent(this,ClientInstallActivity.class).addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP|Intent.FLAG_ACTIVITY_CLEAR_TOP);
    PendingIntent pi=PendingIntent.getActivity(this,77,callback,PendingIntent.FLAG_UPDATE_CURRENT|PendingIntent.FLAG_MUTABLE);
    session.commit(pi.getIntentSender());committed=true;report("Approve the Android install prompt to continue.");
   }catch(Exception e){report("Setup paused: "+e.getMessage()+"\nTap to retry; verified download parts are reused.");}
   finally{if(session!=null)session.close();if(!committed&&id>=0)getPackageManager().getPackageInstaller().abandonSession(id);if(wake!=null&&wake.isHeld())wake.release();runOnUiThread(()->{start.setEnabled(true);getWindow().clearFlags(128);});}
  },"SinFall client setup");worker.start();
 }
 @Override public void onBackPressed(){if(worker!=null&&worker.isAlive())Toast.makeText(this,"Keep setup open until installation is ready",Toast.LENGTH_LONG).show();else super.onBackPressed();}
}
