@echo off
echo ========================================
echo Database Utilities
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Select an option:
echo 1. Show database statistics
echo 2. Clear database (reset all data)
echo 3. Initialize database
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    python db_utils.py stats
)
if "%choice%"=="2" (
    python db_utils.py clear
)
if "%choice%"=="3" (
    python db_utils.py init
)

echo.
pause
