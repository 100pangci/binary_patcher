@echo off
setlocal
cd /d "%~dp0.."
py -3.11 -m pip install -r requirements-build.txt
if errorlevel 1 exit /b %errorlevel%
py -3.11 scripts\build.py
exit /b %errorlevel%
