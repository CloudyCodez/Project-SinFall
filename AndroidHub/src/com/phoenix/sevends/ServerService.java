package com.phoenix.sevends;
import android.app.*;
import android.content.*;
import android.os.*;
import android.util.Log;
import java.io.*;
import java.net.*;
import java.nio.charset.StandardCharsets;

public final class ServerService extends Service {
 static {System.loadLibrary("gcserver");}
 private static native boolean startNative(String directory);
 public static volatile boolean running;
 public static volatile String status="Stopped";
 private PowerManager.WakeLock wake;
 private volatile ServerSocket http;
 private void publish(){Intent update=new Intent("com.phoenix.sevends.SERVER_STATUS");update.setPackage(getPackageName());update.putExtra("running",running);update.putExtra("status",status);sendBroadcast(update);}
 @Override public void onCreate(){
  super.onCreate();
  NotificationManager nm=(NotificationManager)getSystemService(NOTIFICATION_SERVICE);
  nm.createNotificationChannel(new NotificationChannel("server","Offline server",NotificationManager.IMPORTANCE_LOW));
  Intent open=new Intent(this,MainActivity.class);
  PendingIntent pi=PendingIntent.getActivity(this,0,open,PendingIntent.FLAG_IMMUTABLE);
  startForeground(7,new Notification.Builder(this,"server").setContentTitle("7DS Offline server").setContentText("Running on this phone").setSmallIcon(android.R.drawable.stat_notify_sync).setContentIntent(pi).build());
  new Thread(()->{
   try {
    File state=ProfileStore.runtimeDirectory(this);state.mkdirs();
    File config=new File(getFilesDir(),"content");copyAssets("content",config);
    ProfileStore.saveOptions(this);
    if(!startNative(state.getAbsolutePath()))throw new IOException("Could not start game listener");
    http=new ServerSocket(5100,8,InetAddress.getByName("127.0.0.1"));
    running=true;status="Server running • "+ProfileStore.name(ProfileStore.directory(this,ProfileStore.active(this)),"Original account")+"  -  "+ProfileStore.mode(this);publish();
    wake=((PowerManager)getSystemService(POWER_SERVICE)).newWakeLock(PowerManager.PARTIAL_WAKE_LOCK,"7DS:LocalServer");wake.acquire();
    while(true){Socket socket=http.accept();new Thread(()->serve(socket,config)).start();}
   }catch(Exception e){status="Server error: "+e.getMessage();Log.e("GCPhoneServer",status,e);publish();}
  },"7DS server").start();
 }
 private void copyAssets(String asset,File destination)throws IOException{
  String[] children=getAssets().list(asset);
  if(children!=null&&children.length>0){destination.mkdirs();for(String child:children)copyAssets(asset+"/"+child,new File(destination,child));}
  else {destination.getParentFile().mkdirs();try(InputStream in=getAssets().open(asset);OutputStream out=new FileOutputStream(destination)){byte[] b=new byte[32768];int n;while((n=in.read(b))!=-1)out.write(b,0,n);}}
 }
 private void serve(Socket socket,File root){try(Socket s=socket){
  s.setSoTimeout(10000);BufferedReader reader=new BufferedReader(new InputStreamReader(s.getInputStream(),StandardCharsets.US_ASCII));String line=reader.readLine();if(line==null)return;
  String[] fields=line.split(" ");if(fields.length<2)return;String path=fields[1].split("\\?",2)[0];
  while((line=reader.readLine())!=null&&!line.isEmpty()){}
  if(path.startsWith("/nmss/"))path="/"+path.substring(path.lastIndexOf('/')+1);
  OutputStream out=s.getOutputStream();File file=new File(root,path.substring(1));
  if(!file.getCanonicalPath().startsWith(root.getCanonicalPath()+File.separator)||!file.isFile()){out.write("HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n".getBytes(StandardCharsets.US_ASCII));return;}
  out.write(("HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: "+file.length()+"\r\nConnection: close\r\n\r\n").getBytes(StandardCharsets.US_ASCII));
  try(InputStream in=new FileInputStream(file)){byte[] b=new byte[32768];int n;while((n=in.read(b))!=-1)out.write(b,0,n);}out.flush();
 }catch(Exception e){Log.w("GCPhoneServer","Bootstrap request: "+e.getMessage());}}
 @Override public int onStartCommand(Intent i,int flags,int id){publish();return START_STICKY;}
 @Override public IBinder onBind(Intent i){return null;}
 @Override public void onDestroy(){if(wake!=null&&wake.isHeld())wake.release();running=false;status="Stopped";publish();try{if(http!=null)http.close();}catch(IOException ignored){}super.onDestroy();android.os.Process.killProcess(android.os.Process.myPid());}
}
