@echo off
setlocal
cd /d "%~dp0.."
echo Operation No Pants - ComfyUI Wan2.2 5B
echo This launches a local installer/UI, NOT an automatic video render.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0launch_wan_windows.ps1"
if errorlevel 1 (
 echo.
 echo SETUP FAILED. Read the error above; no success is claimed.
 pause
 exit /b 1
)
endlocal
