#pragma once
#include <cstdio>
#include <string>
#define MOVEFILE_REPLACE_EXISTING 1
#define MOVEFILE_WRITE_THROUGH 2
inline bool MoveFileExW(const wchar_t* from,const wchar_t* to,int){
 std::string a,b; while(*from)a.push_back(char(*from++));while(*to)b.push_back(char(*to++));return rename(a.c_str(),b.c_str())==0;
}
