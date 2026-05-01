# Login System Security Testbed

> **Educational Cybersecurity Project**  
> Testing authentication security against brute-force and credential stuffing attacks

## ⚠️ Important Notice

**FOR EDUCATIONAL PURPOSES ONLY**

This project is a controlled security testbed designed for learning about authentication vulnerabilities and defense mechanisms. All testing must be performed exclusively in a local environment. **Never use these tools against systems you don't own or have explicit authorization to test.**

## 📋 Project Overview

This testbed simulates real-world authentication attacks and defense mechanisms in a safe, controlled environment. It consists of:

- **Vulnerable Flask Login Application** - Intentionally weak authentication system
- **Attack Simulation Scripts** - Automated attack tools (brute-force, credential stuffing, distributed, username enumeration)
- **Defense Mechanisms** - Toggleable security controls (rate limiting, account lockout, IP blocking, CAPTCHA, MFA, anomaly detection)
- **Real-Time Dashboard** - Live monitoring with Streamlit
- **Comprehensive Logging** - SQLite database tracking all attempts

## 🎯 Learning Objectives

- Understand common authentication attack vectors
- Implement and evaluate defense mechanisms
- Analyze attack patterns and success rates
- Learn security best practices through hands-on experimentation

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

### Installation

1. **Clone or navigate to the project directory**

```bash
cd "F:\IEH lab project"
```

2. **Create and activate virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create environment file**

```bash
copy .env.example .env
```

### Running the Application

**Terminal 1 - Flask Login Application**

```bash
python run.py
```

The app will run on `http://localhost:5000`

**Terminal 2 - Streamlit Dashboard**

```bash
cd dashboard
streamlit run app.py
```

The dashboard will run on `http://localhost:8501`

## 🎮 Usage

### 1. Configure Defenses

Edit `config.py` to enable/disable defenses:

```python
RATE_LIMIT_ENABLED = True   # Enable rate limiting
ACCOUNT_LOCKOUT = True       # Enable account lockout
IP_BLOCKING = False          # Disable IP blocking
CAPTCHA_ENABLED = False      # Disable CAPTCHA
```

Restart the Flask app after changes.

### 2. Run Attack Simulations

**Brute Force Attack**

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

**Credential Stuffing**

```bash
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v
```

**Distributed Attack (IP Rotation)**

```bash
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 100
```

**Username Enumeration**

```bash
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v
```

### 3. Monitor in Real-Time

Open the Streamlit dashboard at `http://localhost:8501` to see:

- Live login attempts
- Attack metrics and charts
- Defense status
- IP activity heatmap

## 📁 Project Structure

```
login-security-testbed/
├── app/                      # Flask application
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── routes.py            # Login routes & API
│   ├── defenses.py          # Defense mechanisms
│   ├── logger.py            # Logging utilities
│   └── templates/           # HTML templates
├── attacks/                  # Attack scripts
│   ├── attack_bruteforce.py
│   ├── attack_credential_stuffing.py
│   ├── attack_distributed.py
│   └── attack_username_enum.py
├── wordlists/               # Test data
│   ├── passwords.txt
│   ├── credentials.txt
│   └── usernames.txt
├── dashboard/               # Streamlit dashboard
│   └── app.py
├── results/                 # Attack results (auto-generated)
├── config.py               # Defense configuration
├── run.py                  # Flask app runner
├── requirements.txt        # Python dependencies
└── database.db            # SQLite database (auto-created)
```

## 🛡️ Defense Mechanisms

| Defense               | Description                              | Config Flag           |
| --------------------- | ---------------------------------------- | --------------------- |
| **Rate Limiting**     | Limits requests per IP per minute        | `RATE_LIMIT_ENABLED`  |
| **Account Lockout**   | Locks account after N failed attempts    | `ACCOUNT_LOCKOUT`     |
| **IP Blocking**       | Permanently blocks IPs after threshold   | `IP_BLOCKING`         |
| **CAPTCHA**           | Math challenge after failed attempts     | `CAPTCHA_ENABLED`     |
| **Anomaly Detection** | Alerts on suspicious activity patterns   | `ANOMALY_DETECTION`   |
| **MFA**               | Two-factor authentication simulation     | `MFA_ENABLED`         |
| **Pwned Check**       | Checks passwords against breach database | `PWNED_CHECK_ENABLED` |
| **Password Strength** | Enforces strong password requirements    | `PASSWORD_STRENGTH`   |

## 🧪 Running Experiments

### Automated (Recommended)

Run all Milestone 7 scenarios automatically:

```bash
python run_experiments.py
```

This generates:

- `results/experiment_results.csv`
- `results/graphs/success_rate_comparison.html`
- `results/graphs/block_rate_comparison.html`
- `results/graphs/duration_comparison.html`

### Manual

1. Set defense configuration in `config.py`
2. Clear database: delete `database.db` (it will be recreated)
3. Start Flask app
4. Run attack script with `--save` flag
5. Record metrics from dashboard
6. Repeat with different defense configurations

## 📊 Test Accounts

The system includes 20 pre-populated test accounts:

- `admin` / `admin123`
- `user001` / `password123`
- `john_doe` / `qwerty`
- `alice_smith` / `letmein`
- (See `app/models.py` for full list)

## 🔍 API Endpoints

- `GET /api/logs` - Recent login attempts (JSON)
- `GET /api/metrics` - Aggregated metrics (JSON)
- `GET /api/config` - Current defense configuration (JSON)
- `GET /api/stats` - Detailed statistics (JSON)

## 📚 Documentation

- `VULNERABILITIES.md` - Intentional weaknesses documentation
- `HARDENING_GUIDE.md` - Security recommendations
- `project.md` - Complete project specification

## 🤝 Team

**RV College of Engineering - Lab EL**

- Saksham (1RV23CY047)
- Anjali (1RV23CY065)
- Aaditya Raj (1RV23CY001)
- Kavya (1RV23CY025)

## ⚖️ Legal & Ethical

This project is conducted under academic supervision for educational purposes only. All testing is performed in a controlled local environment with synthetic data.

**Using these tools against unauthorized systems is illegal** under:

- IT Act, 2000 (India)
- Computer Fraud and Abuse Act (USA)
- Computer Misuse Act (UK)
- Similar laws worldwide

## 📝 License

Educational use only. Not for production deployment.

## 🆘 Troubleshooting

**Database locked error**

```bash
# Close all connections and restart
rm database.db
python run.py
```

**Port already in use**

```bash
# Change port in run.py or kill existing process
# Windows: netstat -ano | findstr :5000
# Linux: lsof -i :5000
```

**Module not found**

```bash
# Ensure virtual environment is activated
pip install -r requirements.txt
```

## 📞 Support

For issues or questions, contact the team or refer to project documentation.

---

**Remember: With great power comes great responsibility. Use this knowledge ethically.**
