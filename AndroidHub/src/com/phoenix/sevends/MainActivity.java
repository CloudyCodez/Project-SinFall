package com.phoenix.sevends;


import android.app.*;


import android.os.*;


import android.content.*;


import android.graphics.Color;


import android.text.InputType;


import android.widget.*;


import java.io.*;


import java.util.*;





public final class MainActivity extends Activity {


 private TextView status;


 private LinearLayout content;


 private final Handler handler=new Handler();


 private boolean running, switching;


 private String tab="Server";


 private final BroadcastReceiver receiver=new BroadcastReceiver(){@Override public void onReceive(Context c,Intent i){running=i.getBooleanExtra("running",false);if(status!=null)status.setText(i.getStringExtra("status"));}};


 @Override public void onCreate(Bundle saved){super.onCreate(saved);


  registerReceiver(receiver,new IntentFilter("com.phoenix.sevends.SERVER_STATUS"));


  LinearLayout layout=new LinearLayout(this);layout.setOrientation(1);layout.setPadding(28,32,28,24);layout.setBackgroundColor(Color.rgb(20,25,35));


  TextView title=text("7DS Offline Hub",28);layout.addView(title);


  status=text("Stopped",16);status.setTextColor(Color.rgb(100,225,170));status.setPadding(0,16,0,16);layout.addView(status);


  LinearLayout tabs=new LinearLayout(this);for(String label:new String[]{"Server","Accounts"}){Button b=new Button(this);b.setText(label);b.setOnClickListener(v->{tab=label;render();});tabs.addView(b,new LinearLayout.LayoutParams(0,-2,1));}layout.addView(tabs);


  ScrollView scroll=new ScrollView(this);content=new LinearLayout(this);content.setOrientation(1);scroll.addView(content);layout.addView(scroll,new LinearLayout.LayoutParams(-1,0,1));setContentView(layout);render();


 }


 private TextView text(String value,int size){TextView t=new TextView(this);t.setText(value);t.setTextColor(Color.WHITE);t.setTextSize(size);t.setPadding(0,12,0,12);return t;}


 private void button(String label,Runnable action){Button b=new Button(this);b.setText(label);b.setOnClickListener(v->action.run());content.addView(b);}


 private void error(Exception e){Toast.makeText(this,e.getMessage(),Toast.LENGTH_LONG).show();}


 private void startServer(){startForegroundService(new Intent(this,ServerService.class));status.setText("Starting…");}


 private boolean serviceExists(){ActivityManager am=(ActivityManager)getSystemService(ACTIVITY_SERVICE);for(ActivityManager.RunningServiceInfo s:am.getRunningServices(100))if(s.service.getClassName().equals(getPackageName()+".ServerService"))return true;return false;}


 @Override public void onResume(){super.onResume();if(serviceExists())startForegroundService(new Intent(this,ServerService.class));}


 @Override public void onDestroy(){unregisterReceiver(receiver);handler.removeCallbacksAndMessages(null);super.onDestroy();}


 private void render(){content.removeAllViews();if(tab.equals("Accounts")){renderAccounts();return;}


  content.addView(text("Your private server runs on this phone. Start it here, then launch the game.",16));


  button("Set up / update game",()->startActivity(new Intent(this,ClientInstallActivity.class)));
  button("Start Server",()->startServer());


  button("Launch Game",()->{if(!running){Toast.makeText(this,"Start the server first",Toast.LENGTH_SHORT).show();return;}Intent launch=getPackageManager().getLaunchIntentForPackage("com.netmarble.nanagb");if(launch!=null)startActivity(launch);else Toast.makeText(this,"Install the client APK first",Toast.LENGTH_LONG).show();});


  content.addView(text("Play mode",20));


  RadioGroup modes=new RadioGroup(this);modes.setOrientation(LinearLayout.HORIZONTAL);


  for(String value:new String[]{"custom","vanilla"}){RadioButton choice=new RadioButton(this);choice.setText(value.equals("custom")?"Custom: unlimited":"Vanilla: earn resources");choice.setTextColor(Color.WHITE);choice.setChecked(ProfileStore.mode(this).equals(value));choice.setOnClickListener(v->{if(!ProfileStore.mode(this).equals(value)){getSharedPreferences("hub",0).edit().putString("mode_"+ProfileStore.active(this),value).commit();switchAccount(ProfileStore.active(this));}});modes.addView(choice,new LinearLayout.LayoutParams(0,-2,1));}content.addView(modes);


  content.addView(text("Each mode has its own save. Changing modes restarts the server; reopen the game from its title screen.",14));


  if(ProfileStore.mode(this).equals("vanilla")){


   Switch farm=new Switch(this);farm.setText("EZ Farm  -  richer Fort Solgres drops");farm.setTextColor(Color.WHITE);farm.setChecked(getSharedPreferences("hub",0).getBoolean("ez_farm_"+ProfileStore.active(this),false));


   farm.setOnCheckedChangeListener((b,value)->{getSharedPreferences("hub",0).edit().putBoolean("ez_farm_"+ProfileStore.active(this),value).commit();try{ProfileStore.saveOptions(this);}catch(IOException e){error(e);}});content.addView(farm);


   content.addView(text("Gold: awakening and Super Awakening coins. EXP: equipment tickets and EXP materials. Books: attribute-matched relic tokens and LR materials.",14));


  }


  button("Restart Server",()->switchAccount(ProfileStore.active(this)));


  Switch grant=new Switch(this);grant.setText("Grant all units to new accounts");grant.setTextColor(Color.WHITE);grant.setChecked(getSharedPreferences("hub",0).getBoolean("grant_all",false));grant.setPadding(0,22,0,12);


  grant.setOnCheckedChangeListener((b,value)->{getSharedPreferences("hub",0).edit().putBoolean("grant_all",value).commit();try{ProfileStore.saveOptions(this);}catch(IOException e){error(e);}});content.addView(grant);


  content.addView(text("Stage diamond multiplier",20));


  EditText multiplier=new EditText(this);multiplier.setTextColor(Color.WHITE);multiplier.setInputType(InputType.TYPE_CLASS_NUMBER);multiplier.setText(String.valueOf(getSharedPreferences("hub",0).getInt("gem_multiplier",5)));content.addView(multiplier);


  content.addView(text("1× = 1 diamond per successful clear. Repeated clears count. Use 0 to disable; maximum 10000×. Custom keeps unlimited balances; Vanilla earns the configured amount.",14));


  button("Save Multiplier",()->{try{int value=Integer.parseInt(multiplier.getText().toString());if(value<0||value>10000)throw new IllegalArgumentException("Choose 0–10000");getSharedPreferences("hub",0).edit().putInt("gem_multiplier",value).commit();ProfileStore.saveOptions(this);Toast.makeText(this,"Saved: "+value+"×",Toast.LENGTH_SHORT).show();}catch(Exception e){error(e);}});


 }


 private void renderAccounts(){


  content.addView(text("Each account keeps its own units, teams, story, and battle progress. Switching restarts the server; return to the game title screen afterward.",16));


  button("Create Account",()->{EditText name=new EditText(this);name.setSingleLine(true);name.setHint("Account name");new AlertDialog.Builder(this).setTitle("Create local account").setView(name).setNegativeButton("Cancel",null).setPositiveButton("Create",(d,w)->{try{String id=ProfileStore.create(this,name.getText().toString());switchAccount(id);}catch(IOException e){error(e);}}).show();});


  try{String active=ProfileStore.active(this);for(Map.Entry<String,String> account:ProfileStore.accounts(this).entrySet()){


   String id=account.getKey();content.addView(text(account.getValue()+(id.equals(active)?" • Active":""),20));


   if(!id.equals(active))button("Switch to "+account.getValue(),()->switchAccount(id));


   if(!id.equals(active))button("Delete "+account.getValue(),()->new AlertDialog.Builder(this).setTitle("Delete account?").setMessage("Permanently delete "+account.getValue()+" and all of its local progress?").setNegativeButton("Cancel",null).setPositiveButton("Delete",(d,w)->{try{ProfileStore.delete(this,id);render();}catch(IOException e){error(e);}}).show());


  }}catch(IOException e){error(e);}


 }


 private void switchAccount(String id){


  if(switching)return;


  try{ProfileStore.select(this,id);ProfileStore.saveOptions(this);}catch(IOException e){error(e);return;}


  switching=true;running=false;status.setText("Switching account…");stopService(new Intent(this,ServerService.class));


  long deadline=SystemClock.elapsedRealtime()+10000;


  handler.post(new Runnable(){public void run(){if(serviceExists()){if(SystemClock.elapsedRealtime()>deadline){switching=false;status.setText("Server did not stop. Tap Start Server after reopening Hub.");return;}handler.postDelayed(this,100);return;}switching=false;startServer();render();}});


 }


}


