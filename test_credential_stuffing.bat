@echo off
echo ========================================
echo Running Credential Stuffing Attack Test
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Credentials file: wordlists/credentials.txt
echo.
echo This will test the credential stuffing attack script.
echo Make sure Flask app is running on localhost:5000
echo.
pause

python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v

echo.
echo Attack completed. Check the dashboard for results.
pause
