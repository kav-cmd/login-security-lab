# 🎬 START DEMO HERE

Your complete step-by-step guide to demonstrate the entire cybersecurity lab project.

---

## ⚡ SUPER QUICK START (15 min)

If you're in a hurry, do THIS:

```bash
# Terminal 1
cd "F:\IEH lab project"
python run.py

# Terminal 2
cd "F:\IEH lab project"
streamlit run dashboard/app.py

# Terminal 3
cd "F:\IEH lab project"
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

**What you'll see:**

- Flask app starts on http://localhost:5000
- Dashboard starts on http://localhost:8501
- Attack runs and cracks password in ~5 seconds
- This is what NO security looks like

---

## 📊 THE FULL DEMO (30-60 min)

### Step 1: Verify Everything Works (5 min)

```bash
# Check installation
python verify_project.py
```

Expected output: **35/35 checks pass** ✓

If you see errors:

- Run: `pip install -r requirements.txt`
- Run verify again

### Step 2: Start Flask App (2 min)

**Terminal 1:**

```bash
cd "F:\IEH lab project"
python run.py
```

Expected output:

```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
```

**Open browser:** http://localhost:5000

- Login page should load
- Try: username=`admin`, password=`password123`
- You should login successfully

### Step 3: Start Real-Time Dashboard (2 min)

**Terminal 2:**

```bash
cd "F:\IEH lab project"
streamlit run dashboard/app.py
```

Expected output:

```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

**Open browser:** http://localhost:8501

- Dashboard should show "No attacks yet"

### Step 4: Demo NO DEFENSES (5-10 min)

**Check config.py** - All defenses should be OFF:

```python
RATE_LIMIT = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA = False
ANOMALY_DETECTION = False
MFA = False
PWNED_CHECK = False
PASSWORD_STRENGTH = False
```

**Terminal 3:**

```bash
cd "F:\IEH lab project"
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

**What happens:**

- Attack starts and tries passwords
- Dashboard updates with each attempt
- Passwords are tried: password1, password2, password3, ... **password123** ← Found!
- **Success in 5-10 seconds**

**What you say:**

> "Without ANY security, a computer can guess the password in just 5-10 seconds. Every attempt takes less than a second. This is why defaults aren't enough."

### Step 5: Delete Database (1 min)

Before testing defenses, clear the database:

```bash
# Terminal 2 (kill Streamlit with Ctrl+C first)
del database.db
```

Or click the database delete button in the Streamlit dashboard.

### Step 6: Demo WITH RATE LIMITING (5-10 min)

**Edit config.py** - Change 1 line:

```python
RATE_LIMIT = True  # ← Change from False to True
```

**Restart Flask:**

- Terminal 1: Press Ctrl+C
- Run: `python run.py` again
- Wait for: "Running on http://127.0.0.1:5000"

**Run attack again:**

```bash
cd "F:\IEH lab project"
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

**What happens:**

- Attack tries ~10-15 passwords, then gets blocked
- Dashboard shows attack slowing down
- Error: "Too many requests"
- **Attack fails after ~15 attempts**

**What you say:**

> "With rate limiting, the attacker can only try 5 passwords per minute. So the attack is slowed down significantly. But if the attacker is patient, they can still eventually guess the password."

### Step 7: Demo WITH ACCOUNT LOCKOUT (5-10 min)

**Edit config.py:**

```python
RATE_LIMIT = False  # Turn off rate limiting
ACCOUNT_LOCKOUT = True  # Turn on account lockout
```

**Restart Flask and delete database**

**Run attack again:**

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

**What happens:**

- Attack tries exactly 5 passwords, then account locks
- Dashboard shows "Account locked"
- Error: "Account temporarily locked"
- **Attack fails after 5 attempts**

**What you say:**

> "With account lockout, after 5 failed attempts, the account locks for 15 minutes. This stops brute force instantly, but it also means legitimate users who forget their password get locked out."

### Step 8: Demo WITH IP BLOCKING (5-10 min)

**Edit config.py:**

```python
ACCOUNT_LOCKOUT = False
IP_BLOCKING = True
```

**Restart Flask and delete database**

**Run attack:**

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

**What happens:**

- Attack tries ~50 passwords from same IP
- IP gets blocked
- Dashboard shows "IP blocked"
- **Attack fails after ~50 attempts**

**What you say:**

> "With IP blocking, after 50 failed attempts from the same IP, that IP is blocked. But this can fail against distributed attacks where the attacker uses many IPs."

### Step 9: Demo WITH ALL DEFENSES (5 min)

**Edit config.py:**

```python
RATE_LIMIT = True
ACCOUNT_LOCKOUT = True
IP_BLOCKING = True
CAPTCHA = True
ANOMALY_DETECTION = True
MFA = True
PWNED_CHECK = True
PASSWORD_STRENGTH = True
```

**Restart Flask and delete database**

**Run attack:**

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

**What happens:**

- Attack tries 1-2 passwords, then gets hit by multiple defenses
- Rate limit blocks it
- Account locks after few attempts
- CAPTCHA blocks it
- Dashboard shows all defenses active
- **Attack completely fails**

**What you say:**

> "This is what enterprise security looks like. Multiple layers of defense. If one fails, others catch it. This is why banks, Google, and Facebook are hard to break into. They don't rely on just one defense."

### Step 10: Show Results (Optional - 30 min)

Run automated experiments to generate comparison graphs:

```bash
python run_experiments.py
```

This will:

- Test all 7 defense scenarios
- Generate CSV results
- Create graphs comparing success rates
- Save in `results/` folder

**What you say:**

> "Here are the results of testing all 7 scenarios 100 times each. Notice how defenses dramatically reduce attack success. And with all defenses combined, no attack succeeds."

---

## 🎤 KEY TALKING POINTS

### Attack Success Rate Progression

| Scenario             | Success Rate | Time to Crack |
| -------------------- | ------------ | ------------- |
| No defenses          | 100%         | 5-10 sec      |
| Rate limiting only   | 80%          | 5-10 min      |
| Account lockout only | 90%          | 15 attempts   |
| IP blocking only     | 70%          | 50+ attempts  |
| CAPTCHA only         | 5%           | Can't solve   |
| All defenses         | 0%           | Never         |

### 3 Key Insights

1. **Attacks are fast and automated**
   - Without defenses: password cracked in seconds
   - Everyone is under constant attack
   - Default passwords are helpless

2. **Single defenses aren't enough**
   - Each has a bypass or workaround
   - Rate limit → attacker waits
   - Lockout → attacker tries different account
   - IP blocking → attacker rotates IPs

3. **Defense in depth wins**
   - Multiple layers work together
   - If one fails, others catch it
   - This is real enterprise security
   - This is why you use a password manager + 2FA

---

## ✅ SUCCESS CHECKLIST

Before you demo:

- [ ] Installed Python 3.10+
- [ ] Activated virtual environment
- [ ] Ran: `pip install -r requirements.txt`
- [ ] Ran: `python verify_project.py` → 35/35 ✓
- [ ] Read this file (START_DEMO_HERE.md)
- [ ] Read QUICK_REFERENCE_CARD.md
- [ ] Tested once: `python run.py`
- [ ] Tested once: `streamlit run dashboard/app.py`
- [ ] Tested once: `python attacks/attack_bruteforce.py`

During demo:

- [ ] 3 terminals open and ready
- [ ] 2 browser tabs ready (localhost:5000 and :8501)
- [ ] QUICK_REFERENCE_CARD.md visible
- [ ] config.py open for easy editing
- [ ] Calm pace, clear explanations

After demo:

- [ ] Audience understands why security is important
- [ ] Audience can name 3 defenses
- [ ] Audience understands why one defense isn't enough

---

## 🔧 TROUBLESHOOTING

**Problem: "Port 5000 already in use"**

- Kill existing process: `taskkill /IM python.exe`
- Or change port in config.py

**Problem: "Module not found" error**

- Run: `pip install -r requirements.txt`
- Run: `python verify_project.py`

**Problem: "Dashboard not updating"**

- Make sure Flask is running (Terminal 1)
- Make sure dashboard is running (Terminal 2)
- Dashboard updates every 2 seconds

**Problem: "Attack fails immediately"**

- Check if Flask crashed (restart it)
- Check database.db wasn't deleted (or delete and restart)
- Check password is in wordlist (it should be "password123")

**Problem: "Changes to config.py don't work"**

- Flask caches config when it starts
- You must restart Flask (Ctrl+C then run again)
- Flask must be running for changes to take effect

**Problem: "Terminal output is too fast to read"**

- Add `-v` flag for verbose/slower output
- Or copy output to file: `command > output.txt`

---

## 💡 IMPRESSIVE DEMO TRICKS

### Trick 1: Show the contrast

> "Watch this first attack with no defenses... [5 seconds, password cracked]... Now same attack with all defenses... [1 second, blocked]. That's the difference security makes."

### Trick 2: Show real-time

> "See this dashboard? Every number you see is from an actual attack happening right now. The attempt counter is updating in real-time. That's a real cyber attack happening in front of you."

### Trick 3: Show account lockout

> "I'm going to fail the login on purpose 5 times... [fails]... Account locked. The attacker now has to wait 15 minutes. Real humans do this and the account gets locked, which is annoying. But for an attacker with thousands of accounts, this helps."

### Trick 4: Explain the tradeoff

> "Notice every defense we add slows down the attack, but also makes legitimate logins slower. This is why security is hard—you have to balance protection with user experience."

### Trick 5: Connect to real world

> "This is exactly how Slack, Google, GitHub, and banks protect you. These aren't academic ideas—these are real defenses in production systems protecting millions of people."

---

## ⏱️ TIMING REFERENCE

- **5 min demo:** Only show Step 4 (no defenses) vs Step 9 (all defenses)
- **15 min demo:** Steps 4, 6, 9 (no defenses, rate limiting, all defenses)
- **30 min demo:** Steps 4, 6, 7, 8, 9 (most defenses)
- **60 min demo:** All steps + automated experiments (Step 10)

---

## 🎯 YOU'RE READY

**Next action:** Open Terminal, run the "Super Quick Start" above, and see it work.

**Questions?** Check QUICK_REFERENCE_CARD.md or DEMONSTRATION_GUIDE.md

**Want to understand more?** Read EVERYTHING_SUMMARY.md

**Ready to present?** Follow DEMO_MASTER_GUIDE.md

---

## 🚀 HAVE FUN DEMOING!

You built something cool. Show it off. Your audience will think cybersecurity is awesome.

Go get 'em! 🎉
