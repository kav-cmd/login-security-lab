# SecureLab - Login Security Testbed

A modern, interactive security testbed for testing authentication attacks and defenses with real-time monitoring and live defense controls.

## What This Project Does

**In 60 seconds:** SecureLab is an educational security platform that simulates real-world login attacks and defense mechanisms. It features a vulnerable Flask login system, 4 automated attack scripts, 8 configurable defense mechanisms with live toggling, real-time monitoring dashboard, and a modern dark-mode UI for demonstrations.

## 🎯 Quick Start (5 minutes)

```bash
# Terminal 1: Start Flask app
python run.py
# Opens http://localhost:5000

# Terminal 2: Start analytics dashboard (optional)
streamlit run dashboard/app.py
# Opens http://localhost:8501

# Terminal 3: Run an attack
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
# Watch real-time monitoring in the dashboard
```

## ✨ Key Features

| Component | Purpose |
|-----------|---------|
| **Modern Login UI** | Dark-mode interface with vulnerability annotations and live attack monitoring |
| **User Registration** | Create test accounts with password validation |
| **Enhanced Dashboard** | Real-time stats, defense status, and session information |
| **5 Attack Scripts** | Brute force, credential stuffing, distributed (IP rotation), username enumeration, CAPTCHA bypass |
| **8 Defense Mechanisms** | Rate limiting, account lockout, IP blocking, CAPTCHA, anomaly detection, MFA, pwned check, password strength |
| **Live Defense Controls** | Toggle defenses in real-time via dashboard or API (no restart required) |
| **Streamlit Analytics** | Real-time monitoring with charts, metrics, and attack classification |
| **Vulnerability Annotations** | Interactive overlay showing 6 security vulnerabilities |

## 🚀 New Features

### User Experience
- ✅ **User Registration** - Create test accounts at `/register`
- ✅ **Modern Dark-Mode UI** - Professional industrial aesthetic across all pages
- ✅ **Vulnerability Annotations** - Click "🔍 Show Vulnerabilities" to see security issues
- ✅ **Enhanced Dashboard** - Stats cards, defense status grid, and action buttons

### Defense Management
- ✅ **Live Defense Toggling** - Change defenses without restarting Flask
- ✅ **Real-Time API** - POST `/api/config` to toggle defenses programmatically
- ✅ **Dashboard Controls** - Toggle switches in Streamlit sidebar
- ✅ **Instant Feedback** - Toast notifications confirm changes

## 📚 Documentation

### Essential Guides

| File | Purpose | Time |
|------|---------|------|
| **DEFENSE_CONFIGURATION_GUIDE.md** | Complete defense reference with attack comparisons | 30 min |
| **TESTING_GUIDE.md** | Step-by-step testing scenarios for each defense | 20 min |
| **IMPLEMENTATION_VERIFICATION.md** | Attack scripts deep dive and bypass analysis | 15 min |
| **UPDATE_SUMMARY.md** | Recent UI improvements and new features | 5 min |

### Legacy Documentation

| File | Purpose | Time |
|------|---------|------|
| `SETUP.md` | Installation & environment setup | 10 min |
| `DEMO.md` | Step-by-step demonstration guide | 30 min |
| `REFERENCE.md` | Technical specs and architecture | 45 min |
| `project.md` | Complete project specification | 45 min |

## 🛠️ Installation

```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify setup
python verify_project.py
# Expected: "SUCCESS: ALL CHECKS PASSED"

# 4. Start the application
python run.py
```

## 👤 Test Accounts

**Pre-populated accounts** (username:password):
```
admin / admin123
user001 / password123
john_doe / qwerty
alice_smith / letmein
bob_jones / 123456
(+ 15 more — see app/models.py)
```

**Or create your own:**
- Visit http://localhost:5000/register
- Username: min 3 characters
- Password: min 6 characters (or 8+ with uppercase, lowercase, digit if PASSWORD_STRENGTH enabled)

## 🎮 Available Commands

### Database Management
```bash
python db_utils.py init       # Initialize database
python db_utils.py stats      # Show statistics
python db_utils.py clear      # Clear all data
```

### Attack Scripts
```bash
# Brute Force - Single account, many passwords
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v

# Credential Stuffing - Many accounts, leaked passwords
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v

# Distributed - IP rotation to bypass rate limiting
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v

# Username Enumeration - Discover valid usernames
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v

# CAPTCHA Bypass - Demonstrate math CAPTCHA is machine-solvable
# Single user mode (like brute force)
python attacks/attack_captcha_bypass.py -u admin -w wordlists/passwords.txt -v

# Multi-user mode (test multiple accounts)
python attacks/attack_captcha_bypass.py -v

# Custom wordlists (multi-user)
python attacks/attack_captcha_bypass.py -U wordlists/usernames.txt -P wordlists/passwords.txt -v
```

### Automated Testing
```bash
# Run all experiments (generates results CSV and graphs)
python run_experiments.py
```

## 🏗️ Project Structure

```
F:\IEH lab project\
├── app/                           # Flask application
│   ├── routes.py                 # Login endpoints, registration, API
│   ├── models.py                 # Database schemas
│   ├── defenses.py               # Defense logic
│   ├── runtime_config.py         # Live config management (NEW)
│   └── templates/                # HTML pages
│       ├── login.html           # Modern login with vulnerability annotations
│       ├── register.html        # User registration (NEW)
│       ├── dashboard.html       # Enhanced dashboard (NEW)
│       ├── captcha.html         # CAPTCHA challenge
│       └── mfa.html             # MFA verification
├── attacks/                       # Attack scripts
│   ├── attack_bruteforce.py
│   ├── attack_credential_stuffing.py
│   ├── attack_distributed.py
│   ├── attack_username_enum.py
│   └── attack_captcha_bypass.py
├── dashboard/                     # Streamlit analytics
│   └── app.py                    # Real-time monitoring with defense toggles
├── wordlists/                     # Test data
│   ├── passwords.txt
│   ├── credentials.txt
│   └── usernames.txt
├── results/                       # Experiment outputs
├── config.py                      # 🔑 Defense configuration
├── run.py                         # Start Flask app
└── Documentation/
    ├── DEFENSE_CONFIGURATION_GUIDE.md    # Complete defense reference
    ├── TESTING_GUIDE.md                  # Testing scenarios
    ├── IMPLEMENTATION_VERIFICATION.md    # Attack analysis
    └── UPDATE_SUMMARY.md                 # Recent changes
```

## ⚙️ Configuration

### Defense Toggles (config.py)

```python
# All defenses OFF by default - toggle to True to enable
RATE_LIMIT_ENABLED = False       # 8 requests/minute per IP
ACCOUNT_LOCKOUT = False          # Lock after 5 failed attempts (15 min)
IP_BLOCKING = False              # Ban IP after 50 total failures
CAPTCHA_ENABLED = False          # Math challenge after 3 failures
ANOMALY_DETECTION = False        # Alert if >20 attempts/60s
MFA_ENABLED = False              # Multi-factor authentication (TOTP)
PWNED_CHECK_ENABLED = False      # Check against HaveIBeenPwned database
PASSWORD_STRENGTH = False        # Enforce 8+ chars, upper, lower, digit
```

### 🔥 Live Defense Toggling (No Restart Required!)

**Method 1: Dashboard UI**
1. Open http://localhost:5000
2. Login to access dashboard
3. See defense status grid
4. Or use Streamlit dashboard at http://localhost:8501
5. Toggle switches in sidebar

**Method 2: API**
```bash
# Enable rate limiting
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{"defense_name": "RATE_LIMIT_ENABLED", "value": true}'

# Disable account lockout
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{"defense_name": "ACCOUNT_LOCKOUT", "value": false}'

# Check current configuration
curl http://localhost:5000/api/config
```

**Method 3: Edit config.py (Legacy)**
- Edit `config.py` and change values
- Restart Flask: `Ctrl+C` then `python run.py`

## 🔌 API Endpoints

### Read-Only Endpoints
```
GET  /api/logs        → Recent login attempts (JSON)
GET  /api/metrics     → Aggregated statistics
GET  /api/config      → Current defense configuration
GET  /api/stats       → Detailed statistics
```

### Write Endpoints (NEW)
```
POST /api/config      → Toggle defense mechanisms
     Body: {"defense_name": "RATE_LIMIT_ENABLED", "value": true}
     Returns: {"success": true, "defense_name": "...", "new_value": ...}
```

### User Endpoints
```
GET  /                → Redirect to login
GET  /login           → Login page
POST /login           → Process login
GET  /register        → Registration page (NEW)
POST /register        → Create account (NEW)
GET  /dashboard       → User dashboard (requires auth)
GET  /logout          → Logout
```

## 🎨 UI Features

### Login Page
- **Modern Dark-Mode Design** - Professional industrial aesthetic
- **Vulnerability Annotations** - Click "🔍 Show Vulnerabilities" to see 6 security issues
- **Sign Up Link** - Create new test accounts
- **Responsive Design** - Works on mobile and desktop

### Dashboard
- **Welcome Section** - Personalized greeting with username
- **Stats Cards** - Authentication status, active defenses count, session type
- **Defense Status Grid** - Real-time ON/OFF status for all 8 defenses
- **Action Buttons** - Quick links to analytics and login testing
- **Modern UI** - Matches login page aesthetic

### Streamlit Analytics
- **Real-Time Metrics** - Total attempts, blocked, success rate
- **Defense Toggles** - Interactive switches in sidebar
- **Attack Visualization** - Charts and graphs
- **Top IPs** - Most active attacking addresses

## 📊 Attack Scripts Comparison

| Attack Type | Target | Source IPs | Speed | Stealth | Bypasses Rate Limit? |
|-------------|--------|------------|-------|---------|---------------------|
| **Brute Force** | 1 account | 1 IP | Fast | Low | ❌ No |
| **Credential Stuffing** | Many accounts | 1 IP | Moderate | Medium | ❌ No |
| **Distributed** | 1 account | Many IPs | Fast | High | ✅ Yes |
| **Username Enum** | Discovery | 1 IP | Slow | Very High | ⚠️ Partially |
| **CAPTCHA Bypass** | Any account | 1 IP | Fast | Low | ❌ No |

### Which Defenses Stop Which Attacks?

| Defense | Brute Force | Credential Stuffing | Distributed | Username Enum | CAPTCHA Bypass |
|---------|-------------|---------------------|-------------|---------------|----------------|
| Rate Limiting | ✅ Very Effective | ✅ Very Effective | ❌ Not Effective | ⚠️ Partially | ✅ Very Effective |
| Account Lockout | ✅ Very Effective | ⚠️ Partially | ✅ Very Effective | ❌ Not Effective | ✅ Very Effective |
| IP Blocking | ✅ Effective | ✅ Effective | ❌ Not Effective | ❌ Not Effective | ✅ Effective |
| CAPTCHA (Math) | ✅ Very Effective | ⚠️ Partially | ✅ Very Effective | ❌ Not Effective | ❌ **Bypassable** |
| Anomaly Detection | ✅ Very Effective | ✅ Very Effective | ⚠️ Partially | ⚠️ Partially | ✅ Very Effective |
| MFA | ✅ Very Effective | ✅ Very Effective | ✅ Very Effective | N/A | ✅ Very Effective |
| Pwned Check | ⚠️ Partially | ✅ Very Effective | ⚠️ Partially | ❌ Not Effective | ⚠️ Partially |
| Password Strength | ❌ Not Effective | ❌ Not Effective | ❌ Not Effective | ❌ Not Effective | ❌ Not Effective |

**Note:** Math CAPTCHAs are trivially bypassable by parsing HTML and computing answers. Use proof-of-work CAPTCHAs (Cloudflare Turnstile, hCaptcha) for real protection.

**See `IMPLEMENTATION_VERIFICATION.md` for detailed analysis**

## 🎓 Learning Path

### Beginner (1-2 hours)
1. Read `DEFENSE_CONFIGURATION_GUIDE.md` - Understand each defense
2. Run Quick Start commands
3. Try toggling defenses and running attacks
4. Observe differences in dashboard

### Intermediate (3-4 hours)
1. Read `TESTING_GUIDE.md` - Follow all test scenarios
2. Run each attack script with different defense combinations
3. Analyze results in Streamlit dashboard
4. Review code in `app/routes.py` and `app/defenses.py`

### Advanced (5+ hours)
1. Read `IMPLEMENTATION_VERIFICATION.md` - Deep dive into attack mechanics
2. Modify defense thresholds in `config.py`
3. Create custom attack scripts
4. Implement additional defenses
5. Write security analysis report

## 🔍 Example Demonstration Flow

### Scenario: Show Defense Effectiveness

```bash
# 1. Start with no defenses (baseline)
# Edit config.py: All defenses = False
python run.py

# 2. Run brute force attack
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
# Result: Password cracked in seconds

# 3. Enable Rate Limiting
# Via API or dashboard: RATE_LIMIT_ENABLED = True

# 4. Run same attack
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
# Result: Blocked after 8 attempts

# 5. Enable Account Lockout
# Via API or dashboard: ACCOUNT_LOCKOUT = True

# 6. Run same attack
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
# Result: Account locked after 5 attempts

# 7. Try distributed attack to bypass rate limiting
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -v
# Result: Still blocked by account lockout!
```

## 🐛 Troubleshooting

### Port 5000 in use?
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Module not found?
```bash
pip install -r requirements.txt
```

### Database locked?
```bash
# Windows
del database.db

# Linux/Mac
rm database.db

# Then restart
python run.py
```

### Defense changes not working?
- **If using config.py:** Restart Flask (`Ctrl+C` then `python run.py`)
- **If using API/Dashboard:** Changes apply immediately, no restart needed
- Check console for error messages

### Attack scripts not found?
```bash
# Make sure you're in project root
cd "F:\IEH lab project"

# Scripts are in attacks/ directory
python attacks/attack_bruteforce.py --help
```

### Wordlists missing?
```bash
# Check if wordlists directory exists
ls wordlists/

# Should contain:
# - passwords.txt
# - credentials.txt
# - usernames.txt
```

## ⚠️ Important Notes

**This is an educational tool for learning purposes only:**
- ✅ Use only on localhost (127.0.0.1)
- ✅ Never test against external systems without authorization
- ✅ All testing must be performed locally
- ✅ No real credentials or sensitive data
- ✅ Complies with IT Act, 2000 (India) for educational context
- ❌ Not for production use
- ❌ Intentionally vulnerable by design

## 📈 Project Status

### ✅ Fully Implemented
- Flask application with modern UI
- User registration system
- 4 attack scripts with detailed analysis
- 8 defense mechanisms with live toggling
- Real-time monitoring dashboard
- API for programmatic control
- Comprehensive documentation (20,000+ words)
- Vulnerability annotations
- Enhanced dashboard

### 🎯 Recent Updates (Latest)
- ✅ Simplified login page (removed redundant attack monitor)
- ✅ Added user registration at `/register`
- ✅ Enhanced dashboard with modern UI
- ✅ Live defense toggling via API and dashboard
- ✅ Created comprehensive defense guide
- ✅ Added testing scenarios guide
- ✅ Attack scripts deep dive documentation

## 📝 License

Educational project for RV College of Engineering | Information Security Lab

## 🚀 Quick Links

- **Login:** http://localhost:5000
- **Register:** http://localhost:5000/register
- **Dashboard:** http://localhost:5000/dashboard (after login)
- **Analytics:** http://localhost:8501 (Streamlit)
- **API Config:** http://localhost:5000/api/config

## 📖 Next Steps

1. **First time?** → Read `DEFENSE_CONFIGURATION_GUIDE.md`
2. **Want to test?** → Read `TESTING_GUIDE.md`
3. **Need attack details?** → Read `IMPLEMENTATION_VERIFICATION.md`
4. **Recent changes?** → Read `UPDATE_SUMMARY.md`

---

**Ready to start?** Run `python run.py` and visit http://localhost:5000 🚀
