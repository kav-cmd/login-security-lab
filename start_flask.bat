@echo off
echo ========================================
echo Starting Flask Login Application
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if database exists
if not exist database.db (
    echo Creating database for the first time...
    echo.
)

REM Start Flask app
echo Starting Flask server on http://localhost:5000
echo Press Ctrl+C to stop
echo.
python run.py

pause
