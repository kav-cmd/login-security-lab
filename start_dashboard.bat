@echo off
echo ========================================
echo Starting Streamlit Dashboard
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Streamlit dashboard
echo Starting dashboard on http://localhost:8501
echo Press Ctrl+C to stop
echo.
cd dashboard
streamlit run app.py

pause
