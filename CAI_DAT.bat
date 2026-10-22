@echo off
setlocal
set "ROOT=%~dp0"
set "CODE=%ROOT%code"
cd /d "%CODE%"
title Cai dat cadtroly MCP
echo Dang cai cadtroly MCP, vui long cho...
if not exist "%CODE%\pyproject.toml" (
  echo Khong tim thay thu muc code. Hay dat CAI_DAT.bat canh thu muc code.
  pause
  exit /b 1
)

py -3.14 -c "import sys" >nul 2>nul
if not errorlevel 1 goto :python_ok

echo Chua co Python 3.14. Dang tai bo cai chinh thuc tu python.org...
set "PY_URL=https://www.python.org/ftp/python/3.14.9/python-3.14.9-amd64.exe"
set "PY_INSTALLER=%TEMP%\python-3.14.9-amd64.exe"
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -UseBasicParsing -Uri '%PY_URL%' -OutFile '%PY_INSTALLER%'"
if errorlevel 1 (
  echo Khong tai duoc Python. Kiem tra ket noi Internet va chay lai.
  pause
  exit /b 1
)
start /wait "" "%PY_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0
del /q "%PY_INSTALLER%" >nul 2>nul
py -3.14 -c "import sys" >nul 2>nul
if errorlevel 1 (
  echo Cai Python 3.14 that bai. Hay khoi dong lai Windows va chay lai.
  pause
  exit /b 1
)

:python_ok
echo Python 3.14 da san sang.
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
