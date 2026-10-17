#pragma once
#include <vector>
#include <string>
#include <cstring>
#include <stdexcept>
#include <type_traits>
#include <cstdint>
#define _PNT(x) L##x
namespace Proud {
using HostID=int;
struct RmiContext { static RmiContext ReliableSend; }; inline RmiContext RmiContext::ReliableSend;
struct String {
 std::wstring value;
 String()=default;String(const wchar_t* p):value(p){};
 int GetLength()const{return value.size();} const wchar_t* GetString()const{return value.c_str();}
 bool IsEmpty()const{return value.empty();}String& operator+=(const wchar_t* p){value+=p;return *this;}
};
struct StringT2A {std::string value; StringT2A(const String& s){for(auto c:s.value)value+=char(c);} const char* GetString()const{return value.c_str();}};
struct CMessage {
 std::vector<uint8_t> data;size_t position=0;
 int GetLength()const{return data.size();}
 void Write(const uint8_t* p,int n){data.insert(data.end(),p,p+n);}
 bool Read(uint8_t* p,int n){if(n<0||position+n>data.size())throw std::runtime_error("Truncated packet");memcpy(p,data.data()+position,n);position+=n;return true;}
 template<class T,std::enable_if_t<std::is_arithmetic_v<T>,int> =0> CMessage& operator<<(T x){Write(reinterpret_cast<const uint8_t*>(&x),sizeof x);return *this;}
 template<class T,std::enable_if_t<std::is_arithmetic_v<T>,int> =0> CMessage& operator>>(T& x){Read(reinterpret_cast<uint8_t*>(&x),sizeof x);return *this;}
 template<class T>void WriteScalar(T x){int64_t v=x;bool neg=v<0;uint64_t u=neg?~v:v;for(;;){uint8_t b=u&127;u>>=7;if(u){*this<<uint8_t(b|128);}else {if(b&64){*this<<uint8_t(b|128);b=0;}*this<<uint8_t(b|(neg?64:0));break;}}}
 template<class T>bool ReadScalar(T& x){uint64_t u=0;int shift=0;for(int i=0;i<10;i++){uint8_t b;*this>>b;if(b&128){u|=uint64_t(b&127)<<shift;shift+=7;}else {u|=uint64_t(b&63)<<shift;x=T(b&64?~u:u);return true;}}throw std::runtime_error("Invalid scalar");}
 CMessage& operator<<(const String& s){WriteScalar(int64_t(s.GetLength()*2));for(auto c:s.value)*this<<uint16_t(c);return *this;}
 CMessage& operator>>(String& s){int64_t n;ReadScalar(n);if(n<0||n>1048576||(n&1))throw std::runtime_error("Invalid string");s.value.clear();for(int i=0;i<n/2;i++){uint16_t c;*this>>c;s.value+=wchar_t(c);}return *this;}
};
}
bool PhoneSend(int fd,const Proud::CMessage& message);
