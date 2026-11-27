@echo off
rem FreeSail's launcher for Windows (package 130; tools/bundle.py writes it into the download).
rem It runs the game with the Python in this folder and nothing of the machine's own: the
rem interpreter by its own path, -I (no user site, no PYTHON* variables), -B (nothing written
rem beside the code), -X utf8; its python311._pth names the only places it imports from.
setlocal
title FreeSail
set "HERE=%~dp0"
if not exist "%HERE%python\python.exe" goto notunpacked
if not exist "%HERE%game\freesail\__main__.py" goto notunpacked
set "PYTHONHOME="
set "PYTHONPATH="
set "PYTHONSTARTUP="
set "PYTHONUSERBASE="
set "PYTHONDONTWRITEBYTECODE=1"
set "PYTHONNOUSERSITE=1"
set "PYTHONUTF8=1"
echo.
echo   FreeSail ({{NAME}}) is starting.
echo.
echo   This window is the game's server: keep it open while you play.
echo   In a few seconds your web browser opens the harbour, at
echo       http://localhost:8000/harbour
echo   (if it does not, open that address yourself). Begin with "A first passage".
echo.
echo   To stop the game: close this window, or press Ctrl+C in it
echo   (if it then asks "Terminate batch job (Y/N)?", press Y).
echo.
echo   Your saves and settings are kept in "%APPDATA%\FreeSail",
echo   not in this folder: a newer download keeps them.
echo.
"%HERE%python\python.exe" -I -B -X utf8 -m freesail %*
set "CODE=%ERRORLEVEL%"
echo.
echo   FreeSail has stopped (exit code %CODE%).
if not "%CODE%"=="0" echo   If that was not you, START HERE.txt says where to tell us what went wrong.
echo.
pause
exit /b %CODE%

:notunpacked
echo.
echo   FreeSail cannot start from here: its folder is still inside the zip, or not all of it
echo   was unpacked.
echo.
echo   Close this window. Right-click the zip you downloaded, choose "Extract All...",
echo   then open the folder it makes and double-click FreeSail in it.
echo.
pause
exit /b 1
