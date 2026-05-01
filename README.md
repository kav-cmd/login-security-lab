# Login Security Testbed

A controlled environment for testing authentication attacks and defenses against brute-force and credential stuffing attacks.

## What This Project Does

**In 60 seconds:** This is a security testbed that simulates real-world login attacks and evaluates defense mechanisms. It runs a vulnerable Flask login app, launches 4 types of automated attacks, tests 8 defense mechanisms via a toggleable config, and displays everything on a real-time monitoring dashboard.

## Quick Start (5 minutes)

```bash
# Terminal 1: Start Flask app
python run.py
# Opens http://localhost:5000

# Terminal 2: Start dashboard (new window)
streamlit run dashboard/app.py
# Opens http://localhost:8501

# Terminal 3: Run attack (new window)
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
# Watch the dashboard—you'll see ~500 login attempts in real-time
# Attack cracks the password in 5-10 seconds (no defenses enabled)
```

## Key Features

| Component | Purpose |
|-----------|---------|
| **Flask App** | Intentionally vulnerable login system (MD5 hashing, no defenses by default) |
| **4 Attack Scripts** | Brute force, credential stuffing, distributed (IP rotation), username enumeration |
| **8 Defense Mechanisms** | Rate limiting, account lockout, IP blocking, CAPTCHA, anomaly detection, MFA, password strength, breach check |
| **Streamlit Dashboard** | Real-time monitoring with charts, metrics, and attempt feed |
| **Experiment Runner** | Automated testing across 7 scenarios with consolidated results |

## Next Steps

1. **First-time setup?** → Read `SETUP.md`
2. **Want to see it in action?** → Read `DEMO.md`
3. **Need technical details?** → Read `REFERENCE.md`
4. **Understanding the security?** → Read `project.md`

## Installation (Quick Reference)

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify setup
python verify_project.py
# Expected: "SUCCESS: ALL CHECKS PASSED (35/35)"
```

## Test Accounts

All accounts have the format `username:password`:

```
admin / admin123
user001 / password123
john_doe / qwerty
alice_smith / letmein
(+ 16 more — see app/models.py)
```

## Available Commands

```bash
# Database management
python db_utils.py init       # Initialize database
python db_utils.py stats      # Show statistics
python db_utils.py clear      # Clear all data

# Run attacks (choose one)
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v

# Run all experiments (generates results CSV and graphs)
python run_experiments.py
```

## Project Structure

```
F:\IEH lab project\
├── app/                    # Flask application
│   ├── routes.py          # Login endpoints and API
│   ├── models.py          # Database schemas
│   ├── defenses.py        # Defense logic
│   └── templates/         # HTML pages
├── attacks/               # Attack scripts
│   ├── attack_bruteforce.py
│   ├── attack_credential_stuffing.py
│   ├── attack_distributed.py
│   └── attack_username_enum.py
├── dashboard/             # Streamlit monitoring
│   └── app.py
├── wordlists/             # Test data
│   ├── passwords.txt
│   ├── credentials.txt
│   └── usernames.txt
├── results/               # Experiment outputs
│   ├── experiment_results.csv
│   └── graphs/
├── config.py              # 🔑 TOGGLE DEFENSES HERE
├── run.py                 # Start Flask app
├── run_experiments.py      # Run all 7 scenarios
└── verify_project.py      # Check installation
```

## Configuration

All defense mechanisms are toggled in `config.py`:

```python
# Defense toggles (set to True to enable)
RATE_LIMIT_ENABLED = False       # 10 requests/minute
ACCOUNT_LOCKOUT = False          # Lock after 5 failed attempts
IP_BLOCKING = False              # Ban IP after 50 attempts
CAPTCHA_ENABLED = False          # Math challenge after 3 failures
ANOMALY_DETECTION = False        # Alert if >20 attempts/60s
MFA_ENABLED = False              # Multi-factor authentication
PWNED_CHECK_ENABLED = True       # Check against common passwords
PASSWORD_STRENGTH = False        # Enforce password requirements
```

**Important:** Restart Flask after changing `config.py`

## API Endpoints

The Flask app exposes JSON endpoints for integration:

```
GET  /api/logs        → Recent login attempts
GET  /api/metrics     → Aggregated statistics
GET  /api/config      → Current defense configuration
GET  /api/stats       → Detailed statistics
```

## Example Results

After running experiments, you'll see metrics like:

```
Scenario              | Success Rate | Time to Block
─────────────────────────────────────────────────
No Defense           | ~100%         | N/A
Rate Limit Only      | ~10%          | 5-10 min
Account Lockout      | ~0%           | 5 attempts
IP Blocking          | ~5%           | 50 attempts
CAPTCHA Only         | ~0%           | 3 attempts
All Defenses         | ~0%           | <10 attempts
Distributed vs All   | ~0%           | IP rotation fails
```

## Learning Path

1. **Beginner** → Run quick demo → Read vulnerabilities → Read hardening guide
2. **Intermediate** → Run all experiments → Analyze results → Review code
3. **Advanced** → Modify defenses → Create custom attacks → Write analysis

## Documentation Files

| File | Purpose | Time |
|------|---------|------|
| `SETUP.md` | Installation & environment setup | 10 min |
| `DEMO.md` | Step-by-step demonstration guide | 30 min |
| `REFERENCE.md` | Technical specs, architecture, vulnerabilities | 45 min |
| `project.md` | Complete project specification | 45 min |

## Troubleshooting

**Port 5000 in use?**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Module not found?**
```bash
pip install -r requirements.txt
```

**Database locked?**
```bash
del database.db
python run.py
```

**Flask not reloading config changes?**
- Press Ctrl+C in Flask terminal and restart `python run.py`
- Config is cached on startup

## Important Notes

⚠️ **This is an educational tool for learning purposes only:**
- Never use against external systems without authorization
- All testing must be performed locally only
- No real credentials or sensitive data used
- Complies with IT Act, 2000 (India) for educational context

## Project Status

✅ **Fully Implemented**
- Flask application
- 4 attack scripts
- 8 defense mechanisms
- Real-time dashboard
- Automated experiments
- Comprehensive documentation

See `executed.md` for detailed implementation checklist.

## License

Educational project by RV College of Engineering | Course Lab EL

---

**Ready to get started?** → Read `SETUP.md`  
**Want to see it work?** → Read `DEMO.md`  
**Need technical details?** → Read `REFERENCE.md`
