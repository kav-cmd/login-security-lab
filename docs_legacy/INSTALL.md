# Installation and Setup Instructions

## Step 1: Install Python Dependencies

Open a terminal in the project directory and run:

```bash
cd "F:\IEH lab project"

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-Login (session management)
- Flask-Limiter (rate limiting)
- Flask-SQLAlchemy (database ORM)
- requests (HTTP client for attacks)
- streamlit (dashboard)
- plotly (charts)
- pyotp (MFA/OTP)
- bcrypt (password hashing)
- python-dotenv (environment variables)
- pandas (data processing)

## Step 2: Verify Installation

```bash
python verify_project.py
```

You should see all checks pass.

## Step 3: Start the Flask Application

```bash
python run.py
```

The application will:
- Create the database automatically
- Populate 20 test user accounts
- Start on http://localhost:5000

You should see:
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

## Step 4: Start the Dashboard (New Terminal)

Open a second terminal:

```bash
cd "F:\IEH lab project"
venv\Scripts\activate
cd dashboard
streamlit run app.py
```

Dashboard will open at http://localhost:8501

## Step 5: Run Your First Attack (New Terminal)

Open a third terminal:

```bash
cd "F:\IEH lab project"
venv\Scripts\activate
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

When prompted, type `yes` to confirm local testing.

Watch the attack happen in real-time on the dashboard!

## Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"Port already in use" error:**
```bash
# Kill the process using the port
# Windows: netstat -ano | findstr :5000
# Then: taskkill /PID <process_id> /F
```

**Database locked error:**
```bash
python db_utils.py clear
```

## Quick Test Commands

```bash
# Check database stats
python db_utils.py stats

# Run brute force attack
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v

# Run credential stuffing
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v

# Run distributed attack
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v
```

## Changing Defense Configuration

Edit `config.py` and change defenses from `False` to `True`:

```python
RATE_LIMIT_ENABLED = True    # Enable rate limiting
ACCOUNT_LOCKOUT = True        # Enable account lockout
IP_BLOCKING = True            # Enable IP blocking
CAPTCHA_ENABLED = True        # Enable CAPTCHA
ANOMALY_DETECTION = True      # Enable anomaly detection
```

**Important:** Restart the Flask app after changing config.py

## Test Accounts

Try logging in with these credentials:
- admin / admin123
- user001 / password123
- john_doe / qwerty
- alice_smith / letmein

## Project Complete!

You now have a fully functional security testbed for testing authentication attacks and defenses.

Refer to:
- `README.md` - Complete documentation
- `QUICK_START.md` - Quick reference
- `VULNERABILITIES.md` - Security weaknesses explained
- `HARDENING_GUIDE.md` - Production best practices
