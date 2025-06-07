@echo off
cd /d %~dp0

:: 管理者権限チェック
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo Requesting Administrator Privileges...
    powershell Start-Process "%~f0" -Verb RunAs
    exit
)

title Preparing to terminate TyAppsLauncher...
timeout /t 1 /nobreak >nul

:: `taskkill` を非同期で実行
start /B cmd /c "taskkill /F /IM TyAppsLauncher.exe >nul 2>&1"

:: ピリオドのカウントを管理
setlocal enabledelayedexpansion
set count=1

:loop
timeout /t 1 /nobreak >nul

:: ピリオドの表示変更
if %count%==1 (title Terminating TyAppsLauncher.)
if %count%==2 (title Terminating TyAppsLauncher..)
if %count%==3 (title Terminating TyAppsLauncher...)

:: ピリオドのカウント更新
set /a count+=1
if %count% GTR 3 set count=1

:: `taskkill` の処理が終わったか確認
tasklist | findstr /i "TyAppsLauncher.exe" >nul
if %errorlevel% == 0 goto loop

:: `taskkill` 完了後に `start` 実行
title Launching TyAppsLauncher...
start /B TyAppsLauncher.exe --app "TyApps" --args "--no-sandbox --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage --disable-web-security --disable-features=IsolateOrigins,site-per-process"
exit