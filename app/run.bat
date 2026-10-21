@echo off
rem AI Tro ly AutoCAD - chay giao dien. Lan dau: pip install -e ".[web,llm]"
cd /d "%~dp0"
if not exist "%USERPROFILE%\CAD-kho" python -m cadtroly.cli init
python -m cadtroly.cli ui
if errorlevel 1 pause
