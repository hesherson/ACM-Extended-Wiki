@echo off
setlocal
cd /d "%~dp0"
py -3 -c "import sys; assert sys.version_info >= (3,9)" >nul 2>&1
if not errorlevel 1 (
  set "WIKI_PYTHON=py -3"
) else (
  python -c "import sys; assert sys.version_info >= (3,9)" >nul 2>&1
  if errorlevel 1 (
    echo Python 3.9 or newer is needed only when rebuilding edited source files.
    echo This ZIP already includes the built website in docs.
    echo Install Python from https://www.python.org/downloads/windows/ to edit and rebuild.
    pause
    exit /b 1
  )
  set "WIKI_PYTHON=python"
)
%WIKI_PYTHON% build.py
if errorlevel 1 goto failed
%WIKI_PYTHON% scripts\check_wiki.py
if errorlevel 1 goto failed
echo Website built and checked. Open docs\index.html to preview.
echo In GitHub Desktop, review the changes, commit and push origin.
pause
exit /b 0
:failed
echo Build or validation failed. Read the error above before publishing.
pause
exit /b 1
