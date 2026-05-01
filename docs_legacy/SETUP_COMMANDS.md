# Setup Instructions - Run These Commands

## Open Windows Command Prompt or PowerShell

Navigate to your project directory and run these commands:

```cmd
cd "F:\IEH lab project"

REM Create virtual environment (if not already created)
python -m venv venv

REM Activate virtual environment
venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install all dependencies
pip install -r requirements.txt

REM Verify installation
python verify_project.py
```

## Expected Output

After running `pip install -r requirements.txt`, you should see:

```
Successfully installed Flask-3.0.0 Flask-Login-0.6.3 Flask-Limiter-3.5.0 
Flask-SQLAlchemy-3.1.1 requests-2.31.0 streamlit-1.29.0 plotly-5.18.0 
pyotp-2.9.0 bcrypt-4.1.2 python-dotenv-1.0.0 pandas-2.1.4
```

After running `python verify_project.py`, you should see:

```
SUCCESS: ALL CHECKS PASSED (35/35)

Your project is ready to use!

Next steps:
  1. Run: python run.py
  2. Run: streamlit run dashboard/app.py
  3. Run: python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

## If You Encounter Errors

**"pip is not recognized":**
- Make sure Python is in your PATH
- Or use: `python -m pip` instead of `pip`

**"Permission denied":**
- Run Command Prompt as Administrator

**"Module not found" after installation:**
- Make sure virtual environment is activated (you should see `(venv)` in prompt)
- Try: `venv\Scripts\activate` again

## Once Installation is Complete

Let me know and we'll proceed to:
1. Start the Flask application
2. Start the dashboard
3. Run the first attack test
