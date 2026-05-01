# Complete Project Demonstration Guide

> A step-by-step walkthrough to demonstrate the entire login security testbed project

---

## 📋 Overview

This guide walks you through every component of the project in the correct order. Estimated time: **30-45 minutes** for a full run.

**Project Scope:**

- Vulnerable Flask login application
- 4 attack simulation scripts
- 5 toggleable defense mechanisms
- Real-time Streamlit dashboard
- Automated experiment runner (Milestone 7)

---

## 🚀 Step 0: Verify Installation (5 minutes)

**Before starting, confirm everything is set up:**

```bash
cd "F:\IEH lab project"
python verify_project.py
```

**Expected output:**

```
SUCCESS: ALL CHECKS PASSED (35/35)
```

If you see `MISSING` items, run:

```bash
pip install -r requirements.txt
```

---

## 🔥 Step 1: Start the Flask Login Application (2 minutes)

**Terminal 1:** Open a new command prompt and start the Flask server:

```bash
cd "F:\IEH lab project"
python run.py
```

**Expected output:**

```
============================================================
  LOGIN SECURITY TESTBED
  Flask Application Starting...
============================================================

  URL: http://localhost:5000
  Dashboard: http://localhost:8501 (run separately)

  Press CTRL+C to stop
============================================================
```

**⚠️ Important:** Keep this terminal open!

---

## 📊 Step 2: Start the Streamlit Dashboard (2 minutes)

**Terminal 2:** Open a NEW command prompt and start the dashboard:

```bash
cd "F:\IEH lab project"
streamlit run dashboard/app.py
```

**Expected output:**

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
```

**✅ Access point:** Open browser → `http://localhost:8501`

---

## 🧪 Step 3: Test Basic Login (Manual Verification) (3 minutes)

**Browser Tab 1:** Open Flask app → http://localhost:5000

**Test #1: Successful Login**

- Username: `admin`
- Password: `admin123`
- Expected: Redirects to dashboard page

**Test #2: Failed Login**

- Username: `admin`
- Password: `wrongpassword`
- Expected: Returns error message, attempt logged in database

**Test #3: Non-existent User**

- Username: `nonexistent`
- Password: `anypassword`
- Expected: Generic error (no username enumeration)

**View in Dashboard:**

- Switch to dashboard tab (http://localhost:8501)
- You should see 3 login attempts recorded
- "Attempts Per Minute" chart shows activity
- "Recent Login Attempts" table shows details

---

## ⚔️ Step 4: Run Brute Force Attack (No Defenses) (5-10 minutes)

**Before attack:**

1. Verify `config.py` has all defenses **OFF**:

   ```python
   RATE_LIMIT_ENABLED = False
   ACCOUNT_LOCKOUT = False
   IP_BLOCKING = False
   CAPTCHA_ENABLED = False
   ANOMALY_DETECTION = False
   ```

2. Clear the database:

   ```bash
   del database.db
   ```

3. Watch the dashboard in real-time (http://localhost:8501)

**Terminal 3:** Run the brute force attack:

```bash
cd "F:\IEH lab project"
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**What happens:**

- Attack tries passwords from `wordlists/passwords.txt` one by one
- With `-v` flag, you see each attempt: `[FAIL] password123`, `[FAIL] qwerty`, ...
- When password is found, you see: `[SUCCESS] ✓ Password found: admin123`
- Results saved to `results/bruteforce_TIMESTAMP.json`

**Dashboard updates (live):**

- Total Attempts counter increases
- Attempts Per Minute chart spikes
- Recent Attempts table fills with login records
- All attempts show `Success=✅ No, Blocked=✓ No` (no defenses)

**Output in Terminal 3:**

```
==============================================================
  ATTACK SUMMARY
==============================================================
Attack Type:       bruteforce
Total Attempts:    500 (or fewer if password found)
Successful:        1
Failed:            499 (or remainder)
Blocked:           0
Duration:          X.XX seconds
Cracked Password:  admin123
==============================================================
```

---

## 🛡️ Step 5: Enable Defenses & Test Attack Blocking (10 minutes)

### 5A: Test Rate Limiting

**Update `config.py`:**

```python
RATE_LIMIT_ENABLED = True    # Enable
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**Restart Flask:**

- Stop Flask in Terminal 1 (Ctrl+C)
- Start it again: `python run.py`
- Wait for "Flask is running" message

**Clear database:**

```bash
del database.db
```

**Run attack again:**

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**Expected behavior:**

- Attack stops after ~10-15 attempts (rate limit threshold)
- Dashboard shows: `[BLOCKED] ✗ Attack blocked after 10 attempts`
- Terminal shows: `[BLOCKED] Status: 429` (Too Many Requests)
- Compare results: **Baseline succeeded in X attempts → Rate Limiting stopped in 10 attempts**

### 5B: Test Account Lockout

**Update `config.py`:**

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = True       # Enable
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**Restart Flask + Clear DB (as before)**

**Run attack:**

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**Expected behavior:**

- Attack tries 5 passwords
- After 5 failed attempts, account locks
- 6th attempt returns: `[BLOCKED] Status: 429 Account temporarily locked`
- Dashboard shows blocked after exactly 5 attempts
- Account is locked for 15 minutes (configurable in `config.py`)

### 5C: Test IP Blocking

**Update `config.py`:**

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = True           # Enable
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**Restart Flask + Clear DB**

**Run regular brute force:**

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**Expected behavior:**

- Attack tries ~50 passwords
- After 50 failed attempts, IP is permanently banned
- 51st attempt returns: `[BLOCKED] Status: 403 Your IP has been blocked`
- This defense is more effective against single IPs
- To bypass: use distributed attack (next step)

**Run distributed attack:**

```bash
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v --save
```

**Expected behavior:**

- Attack rotates through 50 fake IPs
- Each IP only gets a few attempts before triggering rate limit
- But new IPs bypass the per-IP block
- Shows that **IP rotation defeats single-IP blocking**

### 5D: Test CAPTCHA

**Update `config.py`:**

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = True       # Enable
ANOMALY_DETECTION = False
```

**Restart Flask + Clear DB**

**Run attack:**

```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**Expected behavior:**

- Attack tries 3 passwords
- On 4th failed attempt, CAPTCHA is triggered
- Automated script cannot solve the CAPTCHA
- Attack blocks: `[BLOCKED] ✗ Attack blocked`
- This is most effective against automated attacks

---

## 🔐 Step 6: Test All Defenses Combined (10 minutes)

**Update `config.py`:**

```python
RATE_LIMIT_ENABLED = True
ACCOUNT_LOCKOUT = True
IP_BLOCKING = True
CAPTCHA_ENABLED = True
ANOMALY_DETECTION = True
```

**Restart Flask + Clear DB**

**Run all three attack types:**

```bash
# Brute force
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save

# Credential stuffing
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v --save

# Distributed
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v --save
```

**Expected behavior:**

- **Brute Force:** Blocked by CAPTCHA after 3 failed attempts
- **Credential Stuffing:** Blocked by rate limiting + account lockout
- **Distributed:** Blocked by rate limiting on different IPs + IP blocking after 50 attempts
- Dashboard shows: **0% success rate** across all attacks
- All defenses working in synergy

**Comparison:**

```
Attack Type          | No Defense | All Defenses
--------------------------------------------------
Brute Force          | Success    | Blocked (CAPTCHA)
Credential Stuffing  | Success    | Blocked (Rate Limit)
Distributed          | Success    | Blocked (IP Ban + Rate Limit)
```

---

## 📈 Step 7: Run Full Experiment Suite (Milestone 7) (45-60 minutes)

**This automates all scenarios and generates comparison charts.**

**Update `config.py` to baseline (all OFF):**

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**Terminal 4:** Run the experiment runner:

```bash
cd "F:\IEH lab project"
python run_experiments.py
```

**What it does:**

1. Prompts: "Continue? (yes/no):" → Type **`yes`**
2. Runs all 7 scenarios:
   - ✅ No Defense (baseline)
   - ✅ Rate Limit Only
   - ✅ Account Lockout Only
   - ✅ IP Blocking Only
   - ✅ CAPTCHA Only
   - ✅ All Defenses Combined
   - ✅ Distributed vs All Defenses
3. Each scenario runs 3 attacks:
   - Brute force
   - Credential stuffing
   - Distributed
4. **Total: 21 experiments** (~60 minutes)

**Output files created:**

```
results/
  ├── experiment_results.csv          # Consolidated data
  ├── graphs/
  │   ├── success_rate_comparison.html
  │   ├── block_rate_comparison.html
  │   └── duration_comparison.html
  ├── bruteforce_TIMESTAMP.json       # Individual results
  ├── credential_stuffing_TIMESTAMP.json
  └── distributed_TIMESTAMP.json
```

**View results:**

```bash
# Open CSV in Excel/spreadsheet
start results/experiment_results.csv

# Open HTML graphs in browser
start results/graphs/success_rate_comparison.html
```

**Expected findings:**

- **No Defense:** 100% success rate, ~2-5 seconds to compromise
- **Rate Limit Only:** 80-90% blocked, takes longer
- **Account Lockout Only:** Stops single-target attacks, fails multi-account
- **IP Blocking Only:** Fails against distributed attacks
- **CAPTCHA Only:** Nearly 100% effective against automated attacks
- **All Combined:** 0% success rate, maximum defense

---

## 📚 Step 8: Review Documentation (5 minutes)

**Open in browser or text editor:**

1. **`VULNERABILITIES.md`** - What weaknesses exist and why
2. **`HARDENING_GUIDE.md`** - How to fix them in production
3. **`API_ENDPOINTS.md`** - JSON endpoints for integration
4. **`EXPERIMENT_RESULTS_TEMPLATE.md`** - How to fill in your own results

---

## 🎬 Step 9: View API Endpoints (Optional, 3 minutes)

**Test API calls directly:**

```bash
# In PowerShell or Terminal
curl http://localhost:5000/api/logs
curl http://localhost:5000/api/metrics
curl http://localhost:5000/api/config
curl http://localhost:5000/api/stats
```

Or use the browser:

- http://localhost:5000/api/logs
- http://localhost:5000/api/metrics
- http://localhost:5000/api/config
- http://localhost:5000/api/stats

**Sample `/api/metrics` response:**

```json
{
  "total": 523,
  "blocked": 450,
  "success": 1,
  "failed": 72
}
```

---

## 🎓 Step 10: Cleanup (2 minutes)

**Stop Flask:**

- In Terminal 1, press `Ctrl+C`

**Stop Dashboard:**

- In Terminal 2, press `Ctrl+C`

**Delete test database (optional):**

```bash
del database.db
```

**Note:** Keeping `database.db` lets you review historical data

---

## 📊 Expected Results Summary

| Scenario               | Success Rate | Key Finding                           |
| ---------------------- | ------------ | ------------------------------------- |
| **No Defense**         | ~100%        | Attacks succeed quickly               |
| **Rate Limit**         | ~5-10%       | Slows down but doesn't stop all       |
| **Account Lockout**    | ~90%         | Works for single-account, fails multi |
| **IP Blocking**        | ~80%         | Defeated by IP rotation               |
| **CAPTCHA**            | ~0-5%        | Most effective single defense         |
| **All Combined**       | ~0%          | Attacks completely blocked            |
| **Distributed vs All** | ~0%          | Even IP rotation fails                |

---

## 🐛 Troubleshooting

### Flask won't start

```bash
# Check if port 5000 is already in use
netstat -ano | findstr :5000
# Kill the process if needed: taskkill /PID <PID> /F
```

### Dashboard shows "No login attempts yet"

- Make sure Flask is running (check Terminal 1)
- Try a manual login first
- Wait 2 seconds for dashboard to auto-refresh

### Attack scripts fail with connection error

- Verify Flask is running on http://localhost:5000
- Try accessing it in browser first
- Check config.py has correct TARGET_URL

### Database locked error

```bash
# Close all connections and restart
del database.db
python run.py
```

### Results CSV is empty

- Make sure experiments completed without errors
- Check that `results/` directory exists
- Try running a single attack manually with `--save` flag

---

## ✅ Success Checklist

- [ ] Verified installation (35/35 checks pass)
- [ ] Flask app running on :5000
- [ ] Dashboard running on :8501
- [ ] Manual login test successful
- [ ] Brute force attack succeeds (no defenses)
- [ ] Rate limiting blocks attack
- [ ] Account lockout blocks attack
- [ ] IP blocking blocks attack
- [ ] CAPTCHA blocks attack
- [ ] All defenses combined block all attacks
- [ ] Distributed attack shows IP rotation
- [ ] Experiment suite completes
- [ ] Results CSV generated
- [ ] Graphs generated (3x HTML files)
- [ ] All findings align with expectations

---

## 🎯 What You've Demonstrated

✅ **Security Vulnerabilities**

- MD5 password hashing (weak)
- No rate limiting by default
- No account lockout
- No IP blocking
- Vulnerable to automated attacks

✅ **Defense Mechanisms**

- Rate limiting effectiveness
- Account lockout effectiveness
- IP blocking (and its bypass)
- CAPTCHA effectiveness
- Anomaly detection
- Defense synergy

✅ **Attack Methods**

- Brute force (password guessing)
- Credential stuffing (leaked pairs)
- Distributed attacks (IP rotation)
- Username enumeration (timing)

✅ **Real-Time Monitoring**

- Live dashboard updates
- Attempt logging
- Metrics aggregation
- IP activity heatmap

---

## 📖 Next Steps

1. **Fill EXPERIMENT_RESULTS_TEMPLATE.md** with your specific numbers
2. **Create presentation slides** using PRESENTATION_OUTLINE.md
3. **Write final report** with charts and findings
4. **Review HARDENING_GUIDE.md** for production recommendations

---

**Total Demo Time: ~2 hours for full experience**  
**Quick Demo Time: ~20 minutes for overview only**
