@echo off
setlocal
call "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\Common7\Tools\VsDevCmd.bat" -arch=x64 -host_arch=x64
if errorlevel 1 exit /b 1
set SDK=C:\Program Files (x86)\Nettention\ProudNet
set PIDL=%SDK%\util\PIDL.exe
if not exist "%SDK%\include\ProudNetServer.h" (
  echo ProudNet SDK headers were not found at "%SDK%".
  exit /b 1
)
if not exist "%SDK%\lib\x64\dll\Release\ProudNetServer.lib" (
  echo ProudNet SDK x64 server library was not found.
  exit /b 1
)
if not exist "%PIDL%" (
  echo ProudNet PIDL compiler was not found at "%PIDL%".
  exit /b 1
)
if not exist "Protocol\Generated" mkdir "Protocol\Generated"
for %%P in (Protocol\*.PIDL) do (
  "%PIDL%" -cpp "%%P" -outdir "Protocol\Generated"
  if errorlevel 1 exit /b 1
)
if errorlevel 1 exit /b 1
if defined GC_TRANSPORT_COMPACT "C:\Users\conno\AppData\Local\Python\pythoncore-3.14-64\python.exe" ..\Tools\prepare_phone_compact.py
cl /nologo /MP4 /std:c++17 /EHsc /D USE_PROUDNET_DLL /FI"%SDK%\include\ProudNetServer.h" /I "%SDK%\include" /I Protocol GrandCrossLocalServer.cpp Protocol\Generated\*.cpp /link /LIBPATH:"%SDK%\lib\x64\dll\Release" ProudNetServer.lib ProudNetClient.lib /OUT:GrandCrossLocalServer.exe
if errorlevel 1 exit /b 1
if errorlevel 1 exit /b 1
copy /y "%SDK%\lib\x64\dll\Release\ProudNetServer.dll" . >nul
copy /y "%SDK%\lib\x64\dll\Release\ProudNetClient.dll" . >nul
copy /y "%SDK%\lib\x64\dll\Release\libcrypto-3-x64.dll" . >nul
copy /y "%SDK%\lib\x64\dll\Release\libssl-3-x64.dll" . >nul
echo Build succeeded.


