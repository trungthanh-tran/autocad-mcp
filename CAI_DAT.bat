@echo off
setlocal
cd /d "%~dp0code"
title Cai dat cadtroly MCP
echo Dang cai cadtroly MCP, vui long cho...
where py >nul 2>nul
if errorlevel 1 (
  echo Khong tim thay Python. Hay cai Python 3.14 va chon Add Python to PATH.
  pause
  exit /b 1
)
if not exist ".venv\Scripts\python.exe" py -3.14 -m venv .venv
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements-mcp.lock
.venv\Scripts\python.exe -m pip install -e .
if errorlevel 1 (
  echo CAI DAT THAT BAI. Hay chup anh cua so nay gui nguoi quan tri.
  pause
  exit /b 1
)
.venv\Scripts\python.exe -m cadtroly.cli init
echo.
echo CAI DAT HOAN TAT - cadtroly 0.2.0
echo Bay gio mo VSCode va lam theo DEPLOY_VSCODE.md.
pause
