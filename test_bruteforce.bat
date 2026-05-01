@echo off
echo ========================================
echo Running Brute Force Attack Test
echo ========================================
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

echo Target: admin
echo Wordlist: wordlists/passwords.txt
echo.
echo This will test the brute force attack script.
echo Make sure Flask app is running on localhost:5000
echo.
pause

python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v

echo.
echo Attack completed. Check the dashboard for results.
pause
