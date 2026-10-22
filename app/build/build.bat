@echo off
rem Dong goi goi UI legacy (Windows). Can: pip install -e . pyinstaller
cd /d "%~dp0\.."
python -m PyInstaller build\cadtroly.spec --noconfirm --clean --workpath build\_work --distpath dist || exit /b 1
set OUT=dist\AI-Tro-ly-AutoCAD
if exist build\bin\ant.exe ( if not exist "%OUT%\bin" mkdir "%OUT%\bin"
  copy /y build\bin\ant.exe "%OUT%\bin\ant.exe" >nul )
copy /y build\HUONG-DAN.txt "%OUT%\HUONG-DAN.txt" >nul
copy /y LICENSE "%OUT%\LICENSE.txt" >nul
echo.
echo Xong: %OUT%\AI-Tro-ly-AutoCAD.exe  (nen ca thu muc %OUT% roi gui doi tac)
