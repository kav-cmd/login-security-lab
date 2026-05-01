# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies
```bash
# Navigate to project directory
cd "F:\IEH lab project"

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### Step 2: Start the Application

**Terminal 1 - Flask Login App**
```bash
python run.py
```
Access at: http://localhost:5000

**Terminal 2 - Monitoring Dashboard**
```bash
cd dashboard
streamlit run app.py
```
Access at: http://localhost:8501

### Step 3: Run Your First Attack

```bash
# Terminal 3 - Attack Simulation
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

Watch the attack in real-time on the dashboard!

---

## 🎯 Test Scenarios

### Scenario 1: Baseline (No Defenses)
```python
# config.py - Keep all defenses OFF (default)
```
Run attack and observe success rate.

### Scenario 2: Enable Rate Limiting
```python
# config.py
RATE_LIMIT_ENABLED = True
```
Restart Flask app, run attack again, compare results.

### Scenario 3: All Defenses
```python
# config.py - Set all to True
RATE_LIMIT_ENABLED = True
ACCOUNT_LOCKOUT = True
IP_BLOCKING = True
CAPTCHA_ENABLED = True
ANOMALY_DETECTION = True
```
Restart Flask app, run attack, observe blocking.

---

## 📊 Available Test Accounts

- `admin` / `admin123`
- `user001` / `password123`
- `john_doe` / `qwerty`
- `alice_smith` / `letmein`
- (17 more accounts - see app/models.py)

---

## 🛠️ Useful Commands

```bash
# Database management
python db_utils.py init     # Initialize database
python db_utils.py stats    # Show statistics
python db_utils.py clear    # Clear all data

# Run all experiments automatically
python run_experiments.py

# Individual attacks
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v
```

---

## 📁 Key Files

- `config.py` - Toggle defenses ON/OFF
- `README.md` - Complete documentation
- `VULNERABILITIES.md` - Security weaknesses explained
- `HARDENING_GUIDE.md` - Production best practices
- `PROJECT_SUMMARY.md` - Project overview

---

## ⚠️ Important Reminders

1. **Local testing only** - Never use against external systems
2. **Restart Flask app** after changing config.py
3. **Clear database** between experiments for clean results
4. **Monitor dashboard** while attacks are running

---

## 🎓 Learning Path

1. Run baseline attack (no defenses)
2. Enable defenses one by one
3. Compare effectiveness
4. Try distributed attack vs all defenses
5. Document your findings

---

**Ready to start? Run the commands in Step 1!**
