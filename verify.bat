@echo off
echo ========================================
echo Project Verification
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Checking project structure and dependencies...
echo.

python verify_project.py

echo.
pause
