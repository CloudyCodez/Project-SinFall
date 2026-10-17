package com.phoenix.sevends;
import android.content.Context;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

final class ProfileStore {
 static final String DEFAULT="legacy";
 static String active(Context c){return c.getSharedPreferences("hub",0).getString("active_profile",DEFAULT);}
 static void saveOptions(Context c)throws IOException{
  File dir=runtimeDirectory(c);dir.mkdirs();
  android.content.SharedPreferences settings=c.getSharedPreferences("hub",0);
  String content="mode="+mode(c)+"\nez_farm="+(settings.getBoolean("ez_farm_"+active(c),false)&&mode(c).equals("vanilla")?"1":"0")+"\ngrant_all="+(settings.getBoolean("grant_all",false)?"1":"0")+"\ngem_multiplier="+settings.getInt("gem_multiplier",5)+"\n";
  File tmp=new File(dir,"local-test-options.txt.tmp"),target=new File(dir,"local-test-options.txt");
  try(FileOutputStream out=new FileOutputStream(tmp)){out.write(content.getBytes(StandardCharsets.UTF_8));out.getFD().sync();}
  if(!tmp.renameTo(target))throw new IOException("Could not save options");
 }
 static String mode(Context c){return c.getSharedPreferences("hub",0).getString("mode_"+active(c),"custom");}
 static File runtimeDirectory(Context c)throws IOException{
  File dir=directory(c,active(c));return mode(c).equals("vanilla")?new File(dir,"vanilla"):dir;
 }
 static File directory(Context c,String id)throws IOException{
  if(!id.equals(DEFAULT)&&!id.matches("[a-f0-9-]{36}"))throw new IOException("Invalid profile ID");
  File root=c.getFilesDir(),dir=id.equals(DEFAULT)?new File(root,"profile"):new File(new File(root,"profiles"),id);
  if(!dir.getCanonicalPath().startsWith(root.getCanonicalPath()+File.separator))throw new IOException("Invalid profile path");
  return dir;
 }
 static LinkedHashMap<String,String> accounts(Context c)throws IOException{
  LinkedHashMap<String,String> rows=new LinkedHashMap<>();
  if(!c.getSharedPreferences("hub",0).getBoolean("legacy_deleted",false)){File legacy=directory(c,DEFAULT);legacy.mkdirs();rows.put(DEFAULT,name(legacy,"Original account"));}
  File[] files=new File(c.getFilesDir(),"profiles").listFiles();
  if(files!=null){Arrays.sort(files,Comparator.comparing(File::getName));for(File f:files)if(f.isDirectory()&&f.getName().matches("[a-f0-9-]{36}"))rows.put(f.getName(),name(f,"Account"));}
  return rows;
 }
 static String name(File dir,String fallback)throws IOException{
  File file=new File(dir,"profile-name.txt");if(!file.exists())return fallback;
  try(BufferedReader in=new BufferedReader(new InputStreamReader(new FileInputStream(file),StandardCharsets.UTF_8))){String value=in.readLine();return value==null||value.isEmpty()?fallback:value;}
 }
 static String create(Context c,String label)throws IOException{
  label=label.trim();if(label.isEmpty()||label.length()>32||label.contains("\n"))throw new IOException("Use a name of 1–32 characters");
  String id=UUID.randomUUID().toString();File dir=directory(c,id);
  if(!dir.mkdirs())throw new IOException("Could not create account");
  try(FileOutputStream out=new FileOutputStream(new File(dir,"profile-name.txt"))){out.write(label.getBytes(StandardCharsets.UTF_8));out.getFD().sync();}
  return id;
 }
 static void select(Context c,String id)throws IOException{
  if(!accounts(c).containsKey(id))throw new IOException("Account does not exist");
  if(!c.getSharedPreferences("hub",0).edit().putString("active_profile",id).commit())throw new IOException("Could not switch account");
 }
 static void delete(Context c,String id)throws IOException{
  if(id.equals(active(c)))throw new IOException("Switch to another account before deleting this one");
  File dir=directory(c,id);remove(dir,dir.getCanonicalPath());
  if(id.equals(DEFAULT))c.getSharedPreferences("hub",0).edit().putBoolean("legacy_deleted",true).commit();
 }
 private static void remove(File file,String root)throws IOException{
  String path=file.getCanonicalPath();if(!path.equals(root)&&!path.startsWith(root+File.separator))throw new IOException("Unsafe account path");
  File[] children=file.listFiles();if(children!=null)for(File child:children)remove(child,root);
  if(file.exists()&&!file.delete())throw new IOException("Could not delete account file");
 }
}
