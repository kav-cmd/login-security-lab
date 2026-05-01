# ⚡ QUICK REFERENCE CARD - Demonstration Checklist

> Print this page or keep it open while demonstrating

---

## 🚀 DEMO QUICK START (30 minutes)

### Terminal 1: Flask App

```bash
cd "F:\IEH lab project"
python run.py
```

**✅ Ready when you see:** `Press CTRL+C to stop`

### Terminal 2: Dashboard

```bash
cd "F:\IEH lab project"
streamlit run dashboard/app.py
```

**✅ Ready when you see:** `Local URL: http://localhost:8501`

### Browser Tabs

- **Tab 1:** http://localhost:5000 (Flask app)
- **Tab 2:** http://localhost:8501 (Dashboard)

---

## 🧪 5-MINUTE TEST SEQUENCE

### Test 1: Manual Login (Success)

- **URL:** http://localhost:5000
- **Username:** `admin`
- **Password:** `admin123`
- **Expected:** Redirect to dashboard
- **Dashboard:** Shows 1 attempt

### Test 2: Manual Login (Failure)

- **Username:** `admin`
- **Password:** `wrongpassword`
- **Expected:** Error message
- **Dashboard:** Shows 2 attempts total

### Test 3: Brute Force Attack

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

- **Expected:** Finds password, succeeds
- **Dashboard:** Shows ~500 attempts, success rate ~0.2%
- **Time:** 5-10 seconds

---

## 🛡️ DEFENSE TESTING SEQUENCE

### Config Template - Copy Each One

**No Defense:**

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**Rate Limit Only:**

```python
RATE_LIMIT_ENABLED = True     # ← CHANGE THIS
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**Account Lockout Only:**

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = True        # ← CHANGE THIS
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**IP Blocking Only:**

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = True            # ← CHANGE THIS
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**CAPTCHA Only:**

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = True        # ← CHANGE THIS
ANOMALY_DETECTION = False
```

**All Defenses:**

```python
RATE_LIMIT_ENABLED = True
ACCOUNT_LOCKOUT = True
IP_BLOCKING = True
CAPTCHA_ENABLED = True
ANOMALY_DETECTION = True
```

---

## 🔄 FOR EACH DEFENSE TEST

1. **Edit `config.py`** - Set defense flags
2. **Restart Flask** - Ctrl+C then `python run.py`
3. **Clear DB** - `del database.db`
4. **Clear Dashboard** - Refresh http://localhost:8501
5. **Run Attack:**
   ```bash
   python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
   ```
6. **Observe Dashboard** - Watch success rate, block rate
7. **Record Result** - Note what happened

---

## 📊 EXPECTED RESULTS

| Defense     | Attack Stopped? | How                  | Demo Value                    |
| ----------- | --------------- | -------------------- | ----------------------------- |
| None        | ❌ No           | Succeeds in 5-10 sec | Shows baseline vulnerability  |
| Rate Limit  | ✅ Yes          | ~10-15 attempts      | Shows defense limits attacks  |
| Lockout     | ✅ Yes          | 5 failed attempts    | Shows per-account protection  |
| IP Block    | ✅ Yes (but...) | 50 attempts blocked  | Defeated by distributed       |
| CAPTCHA     | ✅ Yes          | After 3 failures     | Most effective single defense |
| All         | ✅ Yes          | Multiple layers      | Shows defense synergy         |
| Distributed | ⚠️ Partial      | IP rotation bypasses | Shows real attacker tactics   |

---

## 💬 KEY TALKING POINTS

### When showing No Defense:

> "Without any defenses, an automated attack succeeds in just **5-10 seconds**. This is why security is critical."

### When showing Rate Limiting:

> "Rate limiting slows down attacks, but a patient attacker can still succeed by waiting between requests."

### When showing Account Lockout:

> "Account lockout prevents single-account attacks. But an attacker with many user accounts (credential stuffing) will bypass this."

### When showing IP Blocking:

> "IP blocking works against local attackers, but **distributed attacks from different IPs can bypass** this defense."

### When showing CAPTCHA:

> "CAPTCHA is the most effective defense against automated attacks because **machines can't solve them**."

### When showing All Defenses:

> "Combined defenses create **multiple barriers**. Even if one is bypassed, others catch the attack."

### When showing Distributed:

> "Sophisticated attackers rotate IPs. Even with all defenses, distributed attacks can be challenging. Best practice: combine with **behavioral analysis and threat intelligence**."

---

## 🐛 TROUBLESHOOTING

| Problem                 | Solution                                          |
| ----------------------- | ------------------------------------------------- |
| Flask won't start       | Port 5000 in use? `netstat -ano \| findstr :5000` |
| Dashboard shows no data | Did you log in first? Make 1 manual attempt.      |
| Attack script fails     | Flask running? Try `curl http://localhost:5000`   |
| Database locked         | Close all windows. `del database.db`. Restart.    |
| "No module" error       | Run: `pip install -r requirements.txt`            |
| Terminal text unclear   | Copy output to file: `command > output.txt`       |

---

## ⏱️ TIMING FOR DIFFERENT DEMOS

### **5-Minute Flash Demo**

1. Show Flask app + one login (1 min)
2. Show dashboard (1 min)
3. Run brute force attack (2 min)
4. Show it succeeded (1 min)

### **15-Minute Technical Demo**

1. Setup (2 min)
2. Manual login + dashboard (2 min)
3. Brute force (no defense) (3 min)
4. Rate limiting test (3 min)
5. All defenses test (3 min)
6. Show results (2 min)

### **30-Minute Full Demo**

1. Setup (2 min)
2. Manual testing (3 min)
3. Baseline (no defense) (5 min)
4. Individual defenses (12 min):
   - Rate limit (2 min)
   - Lockout (2 min)
   - IP block (3 min)
   - CAPTCHA (3 min)
   - All together (2 min)
5. Show results & dashboard (5 min)
6. Q&A (3 min)

### **60-Minute Full Experiment Suite**

- Just run: `python run_experiments.py`
- Then show results: `results/experiment_results.csv`
- Open graphs in browser: `results/graphs/*.html`

---

## 📱 LIVE DEMO DEMO MODE

**Best way to show everything in a tight demo:**

```bash
# Terminal 1
python run.py

# Terminal 2
streamlit run dashboard/app.py

# Browser Tab 1: http://localhost:5000
# Click Login
# Username: admin, Password: admin123
# Logout

# Browser Tab 2: http://localhost:8501
# Show the 1 attempt recorded

# Terminal 3:
# Config set to: Rate Limit Only
del database.db
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt

# Show Dashboard:
# "Attack was blocked after 10-15 attempts"
# vs baseline success in 5 seconds

# Conclusion: "With rate limiting, the attack is 90% ineffective"
```

---

## 📋 PRESENTATION CHECKLIST

- [ ] Flask terminal is open (http://localhost:5000)
- [ ] Dashboard terminal is open (http://localhost:8501)
- [ ] Browser tabs prepared
- [ ] config.py accessible (for editing)
- [ ] Terminal 3 ready for attacks
- [ ] Talking points printed/reviewed
- [ ] Timing practiced
- [ ] Backup: screenshots of expected results
- [ ] Backup: pre-recorded results (in case live fails)
- [ ] Have HARDENING_GUIDE.md open for Q&A

---

## 🎯 QUESTIONS YOU'LL GET ASKED

**"Why is this vulnerable?"**  
→ MD5 passwords, no rate limiting by default. See VULNERABILITIES.md

**"How do you fix it?"**  
→ Use bcrypt, add all defenses. See HARDENING_GUIDE.md

**"Can distributed attacks still win?"**  
→ Even with all defenses, sophisticated attacks need additional monitoring. See project.md

**"What about credential leaks?"**  
→ Use breach monitoring (HaveIBeenPwned check). Enabled in config.

**"What's the cost of defenses?"**  
→ Legitimate users face friction (CAPTCHA after failed attempts). Balance security vs UX.

**"Is CAPTCHA the silver bullet?"**  
→ No, just very effective. Captcha farms, accessibility issues. Combine with other defenses.

---

## 🏆 SUCCESS DEMO =

✅ Flask runs  
✅ Dashboard shows live data  
✅ Manual login works  
✅ Attack succeeds without defenses  
✅ Attack fails with even 1 defense  
✅ Audience understands the 3 attack types  
✅ Audience sees the 5 defense types  
✅ Audience knows combined defenses are strongest

---

## 📞 QUICK COPY-PASTE COMMANDS

```bash
# Start everything
python run.py

# In separate terminal
streamlit run dashboard/app.py

# In another terminal
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save

# Run all scenarios (1 hour)
python run_experiments.py

# View results
start results/experiment_results.csv
start results/graphs/success_rate_comparison.html
```

---

**Print this page or save to phone before demo!**
