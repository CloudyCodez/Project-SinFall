@echo off
setlocal
if not exist "%~dp0GrandCrossLocalServer.exe" call "%~dp0Build-GrandCross-Local.cmd"
if errorlevel 1 (
  echo Grand Cross local server build failed.
  pause
  exit /b 1
)
"%~dp0GrandCrossLocalServer.exe"
