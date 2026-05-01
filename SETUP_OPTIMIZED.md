# Setup Guide

Installation and environment configuration instructions.

## System Requirements

- Python 3.10 or later
- Windows 10+ (or macOS/Linux)
- 2GB+ free disk space
- Command prompt/terminal access

## Installation (Step by Step)

### Step 1: Create Virtual Environment

Navigate to the project directory:

```bash
cd "F:\IEH lab project"

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

This installs:
- **flask** - Web framework
- **flask-login** - Session management
- **flask-limiter** - Rate limiting
- **flask-sqlalchemy** - Database ORM
- **requests** - HTTP client
- **streamlit** - Dashboard
- **plotly** - Charts
- **pyotp** - MFA/OTP
- **bcrypt** - Password hashing
- **pandas** - Data processing
- **python-dotenv** - Environment variables

### Step 3: Verify Installation

```bash
python verify_project.py
```

**Expected output:**
```
SUCCESS: ALL CHECKS PASSED (35/35)

Your project is ready to use!
```

If you see errors, ensure:
- Virtual environment is activated (you should see `(venv)` in your terminal prompt)
- All dependencies installed: `pip install -r requirements.txt`
- Python 3.10+ is being used: `python --version`

## Running the Application

The system has three components that run separately. **Open 3 terminal windows** and activate the virtual environment in each (`venv\Scripts\activate`).

### Terminal 1: Start Flask App

```bash
cd "F:\IEH lab project"
python run.py
```

**Expected output:**
```
======================================================================
  LOGIN SECURITY TESTBED
  Flask Application Starting...
======================================================================

  URL: http://localhost:5000
  Dashboard: http://localhost:8501 (run separately)

  Press CTRL+C to stop
======================================================================
```

✅ **Ready when:** You see "Press CTRL+C to stop"

### Terminal 2: Start Dashboard

```bash
cd "F:\IEH lab project"
streamlit run dashboard/app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

✅ **Ready when:** You see "Local URL: http://localhost:8501"

### Terminal 3: Run Attacks (After step 1 & 2 are running)

```bash
cd "F:\IEH lab project"
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

When prompted: Type `yes` to confirm local-only testing.

## Testing Access

### Browser Access

Once running, open your browser and navigate to:

1. **Flask Login App:** http://localhost:5000
2. **Streamlit Dashboard:** http://localhost:8501

### Test Accounts

```
admin / admin123
user001 / password123
john_doe / qwerty
alice_smith / letmein
```

Try logging in manually to verify the system works.

## Configuration

Edit `config.py` to control which defense mechanisms are active:

```python
# All OFF by default (vulnerable state)
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
MFA_ENABLED = False
PWNED_CHECK_ENABLED = True
PASSWORD_STRENGTH = False
```

### Changing Defenses

1. Edit `config.py` in any text editor
2. Change `False` to `True` for defenses you want to enable
3. **Restart Flask** (Ctrl+C in Terminal 1, then run `python run.py` again)
4. The Flask app will reload the new configuration

## Utility Commands

### Database Management

```bash
# View statistics
python db_utils.py stats

# Clear all data (start fresh)
python db_utils.py clear

# Initialize fresh database
python db_utils.py init
```

### Run Single Attacks

```bash
# Brute force (password guessing)
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save

# Credential stuffing (leaked pairs)
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v --save

# Distributed (IP rotation)
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v --save

# Username enumeration
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v
```

**Flags:**
- `-v` / `--verbose` - Show each attempt
- `--save` - Save results to JSON file
- `-p <number>` - For distributed: number of fake IPs

### Run All Experiments

```bash
python run_experiments.py
```

This runs all 7 defense scenarios with all 3 attacks. Takes ~60 minutes.

**Generates:**
- `results/experiment_results.csv` - Consolidated metrics
- `results/graphs/*.html` - Comparison charts
- `results/*_TIMESTAMP.json` - Individual attack results

## Troubleshooting

### "Port already in use" Error

Flask uses port 5000. If another process is using it:

```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with the number found above)
taskkill /PID <PID> /F

# Or change port in config.py and restart
```

### "Module not found" Error

Ensure virtual environment is activated and all dependencies installed:

```bash
# Check venv is active (should see "(venv)" in prompt)
which python    # macOS/Linux
where python    # Windows

# Re-install dependencies
pip install -r requirements.txt
```

### "Database locked" Error

The database is being used by multiple processes. Stop all Flask/Streamlit instances:

```bash
# Close all terminal windows running Flask/Streamlit
# Then delete the database and restart:
del database.db
python run.py
```

### "Connection refused" Error

Attack script can't connect to Flask. Verify:

1. Flask app is running in Terminal 1
2. Flask shows "Running on http://127.0.0.1:5000"
3. You can access http://localhost:5000 in browser
4. Target URL in attack script matches (should be `http://localhost:5000/login`)

### Configuration Changes Not Working

Flask caches configuration on startup. After editing `config.py`:

1. **Stop Flask** - Ctrl+C in Terminal 1
2. **Wait** - Give it 2 seconds to shut down
3. **Restart Flask** - Run `python run.py` again
4. **Clear database** - `del database.db` (optional, for clean test)
5. **Restart attack** - Run attack script again

## Cleanup

When finished testing, you can clean up:

```bash
# Stop Flask (Ctrl+C in its terminal)
# Stop Streamlit (Ctrl+C in its terminal)
# Optional: Delete test database
del database.db
# Optional: Delete results
rmdir /s results
```

The virtual environment and installed packages remain for next use.

## Next Steps

1. **Quick Demo?** → Read `DEMO.md`
2. **Understand Security?** → Read `REFERENCE.md`
3. **Full Technical Details?** → Read `project.md`

---

**✅ Installation complete!** Your system is ready. Now read `DEMO.md` to see it in action.
