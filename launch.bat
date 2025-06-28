@echo off
setlocal
set "basedir=%~dp0"
cd /d "%basedir%"
echo [INFO] Working directory: %cd%
echo [INFO] Terminating TyAppsLauncher...

:: プロセスの強制終了（非同期）
start /B cmd /c "taskkill /F /IM tal.exe >nul 2>&1"
start /B cmd /c "taskkill /F /IM TyAppsLauncher.exe >nul 2>&1"

:: 状態ログ付きループ処理
set count=1
:loop
timeout /t 1 /nobreak >nul

echo [INFO] Waiting for processes to exit... Attempt %count%
set /a count+=1
if %count% GTR 3 set count=1

tasklist | findstr /i "TyAppsLauncher.exe" >nul
tasklist | findstr /i "tal.exe" >nul
if %errorlevel% == 0 goto loop

:: 起動
echo [INFO] Starting tal.exe...
start "" /B "%basedir%tal.exe" --app "TyApps" --args "--no-sandbox --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage --disable-web-security --disable-features=IsolateOrigins,site-per-process"
exit