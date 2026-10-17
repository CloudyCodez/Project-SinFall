#include "ProudNetServer.h"
#include "Windows.h"
#include "Protocol/GrandCrossRmiTypes.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>
#include <jni.h>
#include <android/log.h>
#include <thread>
#include <atomic>
#include <mutex>
#include <signal.h>
bool PhoneDispatch(int fd,uint16_t id,Proud::CMessage& message);
void PhoneLogRoster();
static std::atomic<bool> started=false;
static std::mutex sendLock;
static bool writeAll(int fd,const uint8_t* p,size_t n){while(n){auto k=send(fd,p,n,MSG_NOSIGNAL);if(k<=0)return false;p+=k;n-=k;}return true;}
static bool readAll(int fd,uint8_t* p,size_t n){while(n){auto k=recv(fd,p,n,0);if(k<=0)return false;p+=k;n-=k;}return true;}
bool PhoneSend(int fd,const Proud::CMessage& m){std::lock_guard<std::mutex> lock(sendLock);uint8_t header[6]={9,9};uint32_t size=m.data.size();memcpy(header+2,&size,4);if(size>=3&&m.data[0]==1){uint16_t id=0;memcpy(&id,m.data.data()+1,2);if(id==14548||id==14001)__android_log_print(ANDROID_LOG_INFO,"GCPhoneServer","Result %u bytes=%u",id,size);}return writeAll(fd,header,6)&&writeAll(fd,m.data.data(),size);}
static void client(int fd){
 try {
  Proud::CMessage hello;hello<<uint8_t(5);PhoneSend(fd,hello);
  for(;;){uint8_t header[2];if(!readAll(fd,header,2))break;
   if(header[0]!=9||header[1]!=9){ // internal one-byte idle ping uses the compact transport header
    uint8_t length;if(!readAll(fd,&length,1))break;
    if(length>63)throw std::runtime_error("Unexpected control packet");
    std::vector<uint8_t> control(length);if(!readAll(fd,control.data(),length))break;
    continue;
   }
   uint32_t n;if(!readAll(fd,reinterpret_cast<uint8_t*>(&n),4))break;
   if(n==0||n>1048576)throw std::runtime_error("Invalid frame length");
   Proud::CMessage m;m.data.resize(n);if(!readAll(fd,m.data.data(),n))break;
   uint8_t type;m>>type;
   if(type==6){
    static const uint8_t accepted[]={0x0d,3,0,0,0,0,0x12,0x31,0,0x32,0,0x37,0,0x2e,0,0x30,0,0x2e,0,0x30,0,0x2e,0,0x31,0,0xef,0xf5};
    Proud::CMessage reply;reply.Write(accepted,sizeof accepted);PhoneSend(fd,reply);
   }else if(type==1){uint16_t id;m>>id;__android_log_print(ANDROID_LOG_INFO,"GCPhoneServer","Request %u",id);
    if(id==10103||id==10120||id==10085){auto diagnostic=m;int32_t hero=0;diagnostic>>hero;int32_t value=0;if(id==10103)diagnostic>>value;else{uint8_t rank=0;diagnostic>>rank;value=rank;}__android_log_print(ANDROID_LOG_INFO,"GCPhoneServer","Awakening request=%u hero=%d value=%d",id,hero,value);}
    if(id==10103||id==10120||id==10085){auto diagnostic=m;int32_t hero=0;diagnostic>>hero;std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);int skin=GcLocal::ActiveSkin(hero);__android_log_print(ANDROID_LOG_INFO,"GCPhoneServer","Awakening state hero=%d skin=%d stars=%d",hero,skin,skin?GcLocal::DevelopmentStates()[skin].awaken:-1);}
    if(id==11108){auto diagnostic=m;int32_t ticket=0,selected=0;diagnostic>>ticket>>selected;__android_log_print(ANDROID_LOG_INFO,"GCPhoneServer","Equipment ticket item=%d selection=%d bytes=%zu",ticket,selected,m.data.size()-m.position);}
    if(id==10121){auto diagnostic=m;int32_t skin=0,serial=0,slot=0;bool remove=false;diagnostic>>skin>>serial>>slot>>remove;std::lock_guard<std::mutex> lock(GcLocal::AccountMutex);auto it=GcLocal::Equipments().find(serial);const auto* base=it==GcLocal::Equipments().end()?nullptr:GcLocal::EquipmentBaseRow(it->second.base);__android_log_print(ANDROID_LOG_INFO,"GCPhoneServer","Equip skin=%d owned=%d serial=%d found=%d slot=%d parts=%d previousSkin=%d remove=%d",skin,int(GcLocal::OwnedSkins().count(skin)),serial,int(it!=GcLocal::Equipments().end()),slot,base?base->weapon_parts:-1,it==GcLocal::Equipments().end()?-1:it->second.skin,int(remove));}
    bool handled=PhoneDispatch(fd,id,m);if(!handled)__android_log_print(ANDROID_LOG_WARN,"GCPhoneServer","Unhandled request %u",id);if(id==10055)PhoneLogRoster();}
  }
 }catch(const std::exception& e){__android_log_print(ANDROID_LOG_ERROR,"GCPhoneServer","Session: %s",e.what());}
 close(fd);
}
extern "C" JNIEXPORT jboolean JNICALL Java_com_phoenix_sevends_ServerService_startNative(JNIEnv* env,jclass,jstring path){
 if(started.exchange(true))return true;
 const char* dir=env->GetStringUTFChars(path,nullptr);int result=chdir(dir);env->ReleaseStringUTFChars(path,dir);if(result){started=false;return false;}
 int listener=socket(AF_INET,SOCK_STREAM,0);int yes=1;setsockopt(listener,SOL_SOCKET,SO_REUSEADDR,&yes,sizeof yes);
 sockaddr_in addr{};addr.sin_family=AF_INET;addr.sin_port=htons(5001);addr.sin_addr.s_addr=htonl(INADDR_LOOPBACK);
 if(bind(listener,reinterpret_cast<sockaddr*>(&addr),sizeof addr)||listen(listener,8)){close(listener);started=false;return false;}
 std::thread([listener]{for(;;){int fd=accept(listener,nullptr,nullptr);if(fd>=0)std::thread(client,fd).detach();}}).detach();
 __android_log_print(ANDROID_LOG_INFO,"GCPhoneServer","On-phone server listening on 127.0.0.1:5001");return true;
}
