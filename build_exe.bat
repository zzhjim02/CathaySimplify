@echo off
title CathaySimplify Build

set "ROOT=%~dp0"
set "SRC=%ROOT%src"

if not exist "%ROOT%venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found
    echo   Run setup.bat first
    pause
    exit /b 1
)

call "%ROOT%venv\Scripts\activate.bat"

echo ================================
echo   Building EXEs
echo ================================
echo.

echo [1/2] Building DEV version (console)...
pyinstaller --onefile --console ^
    --name "CathaySimplify-DEV" ^
    --icon "%ROOT%CathaySimplify.ico" ^
    --hidden-import opencc --hidden-import chardet --hidden-import tkinterdnd2 ^
    --distpath "%ROOT%dist\DEV" ^
    --workpath "%ROOT%build\DEV" ^
    --noconfirm ^
    "%SRC%\converter.py"
if errorlevel 1 (
    echo [ERROR] DEV build failed
    pause
    exit /b 1
)
echo OK: dist\DEV\CathaySimplify-DEV.exe
echo.

echo [2/2] Building Release version (GUI only)...
pyinstaller --onefile --windowed ^
    --name "CathaySimplify" ^
    --icon "%ROOT%CathaySimplify.ico" ^
    --hidden-import opencc --hidden-import chardet --hidden-import tkinterdnd2 ^
    --distpath "%ROOT%dist\Release" ^
    --workpath "%ROOT%build\Release" ^
    --noconfirm ^
    "%SRC%\converter.py"
if errorlevel 1 (
    echo [ERROR] Release build failed
    pause
    exit /b 1
)
echo OK: dist\Release\CathaySimplify.exe
echo.

del /f /q "%ROOT%CathaySimplify.spec" >nul 2>&1
del /f /q "%ROOT%CathaySimplify-DEV.spec" >nul 2>&1
rmdir /s /q "%ROOT%build" >nul 2>&1

echo ================================
echo   All done!
echo   dist\DEV\     CathaySimplify-DEV.exe
echo   dist\Release\ CathaySimplify.exe
echo ================================
pause
