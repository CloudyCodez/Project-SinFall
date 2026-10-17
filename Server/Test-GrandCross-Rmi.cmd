@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64
if errorlevel 1 exit /b 1
set SDK=C:\Program Files (x86)\Nettention\ProudNet
set PIDL=%SDK%\util\PIDL.exe
if not exist "%SDK%\include\ProudNetClient.h" (
  echo ProudNet SDK client headers were not found.
  exit /b 1
)
if not exist "Protocol\Generated" mkdir "Protocol\Generated"
"%PIDL%" -cpp "Protocol\SevenDSGameC2S.PIDL" "Protocol\SevenDSGameS2C.PIDL" -outdir "Protocol\Generated"
if errorlevel 1 exit /b 1
cl /nologo /std:c++17 /EHsc /D USE_PROUDNET_DLL /FI"%SDK%\include\ProudNetClient.h" /I "%SDK%\include" /I Protocol Protocol\GrandCrossRmiSmokeClient.cpp Protocol\Generated\SevenDSGameC2S_common.cpp Protocol\Generated\SevenDSGameC2S_proxy.cpp Protocol\Generated\SevenDSGameC2S_stub.cpp Protocol\Generated\SevenDSGameS2C_common.cpp Protocol\Generated\SevenDSGameS2C_proxy.cpp Protocol\Generated\SevenDSGameS2C_stub.cpp /link /LIBPATH:"%SDK%\lib\x64\dll\Release" ProudNetClient.lib /OUT:Protocol\GrandCrossRmiSmokeClient.exe
if errorlevel 1 exit /b 1
copy /y "%SDK%\lib\x64\dll\Release\ProudNetClient.dll" Protocol >nul
copy /y "%SDK%\lib\x64\dll\Release\libcrypto-3-x64.dll" Protocol >nul
copy /y "%SDK%\lib\x64\dll\Release\libssl-3-x64.dll" Protocol >nul
echo Smoke client built. Start the local server first, then run Protocol\GrandCrossRmiSmokeClient.exe.
