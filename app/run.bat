@echo off
rem UI legacy - khong phai quy trinh MCP chinh. MCP chay bang: python -m cadtroly.mcp
cd /d "%~dp0"
if not exist "%USERPROFILE%\CAD-kho" python -m cadtroly.cli init
python -m cadtroly.cli ui
if errorlevel 1 pause
