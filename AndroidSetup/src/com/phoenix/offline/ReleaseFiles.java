package com.phoenix.offline;

import org.json.*;
import java.io.*;
import java.net.*;
import java.security.*;

/** Shared, bounded-memory release downloader. Completed files are hash checked on reuse. */
public final class ReleaseFiles {
 public static final String MANIFEST="https://github.com/CloudyCodez/Project-SinFall/releases/download/v0.1.0-tester.1/release.json";
 public interface Progress { void update(String message); }
 public static InputStream open(String url) throws IOException {
  if(!url.startsWith("https://"))throw new IOException("HTTPS required");
  HttpURLConnection c=(HttpURLConnection)new URL(url).openConnection();
  c.setConnectTimeout(30000);c.setReadTimeout(60000);c.setRequestProperty("User-Agent","Project-SinFall/0.1");
  int code=c.getResponseCode();if(code!=200){c.disconnect();throw new IOException("Download returned HTTP "+code);}
  return new FilterInputStream(c.getInputStream()) {public void close()throws IOException{try{super.close();}finally{c.disconnect();}}};
 }
 public static JSONObject manifest()throws Exception{
  try(InputStream in=open(MANIFEST);ByteArrayOutputStream out=new ByteArrayOutputStream()){
   byte[] b=new byte[8192];int n;while((n=in.read(b))!=-1){out.write(b,0,n);if(out.size()>1048576)throw new IOException("Manifest too large");}
   JSONObject m=new JSONObject(out.toString("UTF-8"));if(m.getInt("schema")!=1)throw new IOException("Unsupported release schema");return m;
  }
 }
 public static String hash(File f)throws Exception{
  MessageDigest md=MessageDigest.getInstance("SHA-256");try(InputStream in=new FileInputStream(f)){byte[] b=new byte[262144];int n;while((n=in.read(b))!=-1)md.update(b,0,n);}
  StringBuilder s=new StringBuilder();for(byte v:md.digest())s.append(String.format("%02x",v&255));return s.toString();
 }
 public static boolean valid(File f,JSONObject spec)throws Exception{return f.isFile()&&f.length()==spec.getLong("size")&&hash(f).equals(spec.getString("sha256"));}
 public static File download(JSONObject spec,File folder,Progress progress)throws Exception{
  folder.mkdirs();String name=spec.getString("name");if(!name.matches("[A-Za-z0-9._-]+"))throw new IOException("Invalid release filename");
  File target=new File(folder,name);if(valid(target,spec))return target;
  File part=new File(folder,name+".partial");long expected=spec.getLong("size");
  if(expected<=0)throw new IOException("Invalid download size");
  if(folder.getUsableSpace()<expected+67108864L)throw new IOException("Insufficient free space for "+name);
  try(InputStream in=open(spec.getString("url"));OutputStream out=new FileOutputStream(part)){
   byte[] b=new byte[262144];long count=0,last=0;int n;
   while((n=in.read(b))!=-1){if(Thread.currentThread().isInterrupted())throw new IOException("Cancelled");count+=n;if(count>expected)throw new IOException("Download exceeds expected size");out.write(b,0,n);long now=System.currentTimeMillis();if(now-last>500){progress.update(name+": "+(count*100/expected)+"%");last=now;}}
  }
  if(!valid(part,spec)){part.delete();throw new IOException("Checksum mismatch: "+name);}
  if(target.exists()&&!target.delete())throw new IOException("Cannot replace "+name);
  if(!part.renameTo(target))throw new IOException("Cannot finish "+name);return target;
 }
 private ReleaseFiles(){}
}
