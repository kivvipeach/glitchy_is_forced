@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" simulate.py
if errorlevel 1 pause
