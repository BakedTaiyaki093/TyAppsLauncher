@echo off
cd /d %~dp0

taskkill /F /IM TyAppsLauncher.exe >nul 2>&1
timeout /t 2 /nobreak >nul

start /B TyAppsLauncher.exe --app "TyApps" --args "--no-sandbox --disable-gpu --disable-software-rasterizer --disable-dev-shm-usage --disable-web-security --disable-features=IsolateOrigins,site-per-process"

exit