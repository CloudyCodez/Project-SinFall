package com.phoenix.offline;

import android.app.*;
import android.os.*;
import android.content.*;
import android.widget.*;
import java.io.*;
import java.util.zip.*;
import org.json.*;

/** Runs inside the client UID, so Android/data needs no cross-app storage permission. */
public final class AssetSetupActivity extends Activity {
 private TextView status;private Button start;private Thread worker;private PowerManager.WakeLock wake;
 private File marker(){return new File(getFilesDir(),"sinfall-assets-v1.complete");}
 @Override public void onCreate(Bundle state){super.onCreate(state);
  if(marker().isFile()){launch();return;}
  LinearLayout view=new LinearLayout(this);view.setOrientation(1);view.setPadding(32,48,32,24);
  status=new TextView(this);status.setTextSize(18);status.setText("Project SinFall tester setup\n\nDownload the preserved assets once, then play offline. Allow about 17 GB free for assets, in addition to the installed game. Keep this screen open until setup completes. Completed packs are retained across retries.");view.addView(status);
  start=new Button(this);start.setText("Download assets and play");start.setOnClickListener(v->begin());view.addView(start);setContentView(view);
 }
 private void report(String s){runOnUiThread(()->status.setText(s));}
 private void launch(){Intent i=new Intent();i.setClassName(this,"com.netmarble.fpplugin.FPActivity");startActivity(i);finish();}
 private void begin(){if(worker!=null&&worker.isAlive())return;start.setEnabled(false);getWindow().addFlags(128);
  worker=new Thread(()->{try{
   wake=((PowerManager)getSystemService(POWER_SERVICE)).newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,"SinFall:AssetSetup");wake.acquire(4*60*60*1000L);
   JSONObject manifest=ReleaseFiles.manifest();JSONArray packs=manifest.getJSONArray("assets");
   File root=getExternalFilesDir(null);if(root==null)throw new IOException("External app storage unavailable");
   File downloads=new File(root,"sinfall-downloads");downloads.mkdirs();
   for(int p=0;p<packs.length();p++){
    JSONObject spec=packs.getJSONObject(p);File done=new File(getFilesDir(),"pack-"+spec.getString("sha256")+".complete");if(done.exists())continue;
    File zip=ReleaseFiles.download(spec,downloads,this::report);report("Installing asset pack "+(p+1)+" / "+packs.length());
    if(root.getUsableSpace()<spec.getLong("unpacked_size")+67108864L)throw new IOException("Not enough space to extract assets");
    long expanded=0;int entries=0;
    try(ZipInputStream in=new ZipInputStream(new BufferedInputStream(new FileInputStream(zip)))){
     ZipEntry e;byte[] buffer=new byte[262144];while((e=in.getNextEntry())!=null){
      String name=e.getName();if(!name.startsWith("bm/")||name.contains("\\"))throw new IOException("Invalid asset path");
      File dest=new File(root,name);if(!dest.getCanonicalPath().startsWith(new File(root,"bm").getCanonicalPath()+File.separator))throw new IOException("Unsafe asset path");
      if(e.isDirectory()){dest.mkdirs();continue;}dest.getParentFile().mkdirs();File partial=new File(dest.getPath()+".sinfall-partial");
      try(OutputStream out=new FileOutputStream(partial)){int n;while((n=in.read(buffer))!=-1){expanded+=n;if(expanded>spec.getLong("unpacked_size"))throw new IOException("Asset size limit exceeded");out.write(buffer,0,n);}}
      if(dest.exists()&&!dest.delete())throw new IOException("Cannot replace asset");if(!partial.renameTo(dest))throw new IOException("Cannot install asset");entries++;
     }
    }
    if(expanded!=spec.getLong("unpacked_size")||entries!=spec.getInt("files"))throw new IOException("Incomplete asset pack");
    try(FileOutputStream out=new FileOutputStream(done)){out.write(1);}zip.delete();
   }
   // Base cache extraction can replace catalogs/manifests from a previous install.
   // Re-arm only the packaged-content installers; account and game preferences stay intact.
   File[] preferences=new File(getApplicationInfo().dataDir,"shared_prefs").listFiles();
   if(preferences!=null)for(File preference:preferences){String name=preference.getName();
    if(name.equals("offline_catalog.xml")||name.equals("offline_catalog_manifest.xml")||name.matches("offline_custom_[0-9]+\\.xml")){
     if(!getSharedPreferences(name.substring(0,name.length()-4),0).edit().clear().commit())throw new IOException("Cannot refresh packaged content installer");
    }
   }
   try(FileOutputStream out=new FileOutputStream(marker())){out.write(manifest.getString("version").getBytes("UTF-8"));}
   runOnUiThread(this::launch);
  }catch(Exception e){report("Setup paused: "+e.getMessage()+"\nTap to retry. Completed packs will be skipped.");runOnUiThread(()->start.setEnabled(true));}
  finally{if(wake!=null&&wake.isHeld())wake.release();runOnUiThread(()->getWindow().clearFlags(128));}
  },"SinFall asset setup");worker.start();
 }
 @Override public void onBackPressed(){if(worker!=null&&worker.isAlive())Toast.makeText(this,"Keep setup open until the download completes",Toast.LENGTH_LONG).show();else super.onBackPressed();}
}
