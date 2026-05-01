# Demonstration Guide

Step-by-step instructions for demonstrating the login security testbed. Choose a demo length that fits your time.

## Prerequisites

- Installation complete (`python verify_project.py` passes with 35/35)
- Read `SETUP.md` if you haven't already
- Recommend reading this file completely before starting
- Have 3 terminal windows ready

## Demo Duration Options

| Duration | Scope | Section |
|----------|-------|---------|
| **5 min** | Flash demo | Quick Demo |
| **15 min** | Basic demo | Quick Demo + step 5 |
| **30 min** | Full demo | All major steps |
| **60+ min** | Complete | Run `python run_experiments.py` |

## Quick Demo (5 minutes)

For when you're short on time but want to show the system works.

### Setup (1 minute)

```bash
# Terminal 1: Start Flask
python run.py

# Terminal 2: Start Dashboard (wait for Terminal 1 to be ready first)
streamlit run dashboard/app.py

# Open browsers
# Tab 1: http://localhost:5000
# Tab 2: http://localhost:8501
```

### Execution (4 minutes)

```bash
# Terminal 3: Run attack
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

**What to tell your audience:**

> "This is a security testbed. That Flask app is intentionally vulnerable - it uses weak password hashing and has no defenses. I'm running an automated password-guessing attack. Watch the dashboard..."

**Watch for:**
- Dashboard updates with each attempt
- Attempts per minute chart spikes
- After ~5-10 seconds: `[SUCCESS] Password found: admin123`

> "Without any security, the attack cracked the account in just 5 seconds. This is why defaults aren't enough."

---

## Full Demo (30 minutes)

Complete walkthrough of the system with defense testing.

### Step 1: Verify Installation (3 minutes)

```bash
python verify_project.py
```

**Expected:** 
```
SUCCESS: ALL CHECKS PASSED (35/35)
```

If anything fails:
- Run: `pip install -r requirements.txt`
- Try verify again

### Step 2: Start Flask App (2 minutes)

**Terminal 1:**

```bash
cd "F:\IEH lab project"
python run.py
```

**Expected output:**
```
  URL: http://localhost:5000
  Press CTRL+C to stop
```

✅ Keep this terminal open.

### Step 3: Start Streamlit Dashboard (2 minutes)

**Terminal 2 (new window):**

```bash
cd "F:\IEH lab project"
streamlit run dashboard/app.py
```

**Expected output:**
```
Local URL: http://localhost:8501
```

✅ Dashboard will auto-open in browser, or visit `http://localhost:8501` manually.

### Step 4: Test Manual Login (3 minutes)

**Browser Tab 1:** Open `http://localhost:5000`

**Test 1: Successful login**
- Username: `admin`
- Password: `admin123`
- Expected: Redirects to protected dashboard

**Test 2: Failed login**
- Username: `admin`
- Password: `wrongpassword`
- Expected: Error message, no enumeration hints

**Test 3: Manual logout**
- Click logout
- Expected: Returns to login page

**Check dashboard (Tab 2):**
- Should show 2-3 login attempts logged
- "Recent Attempts" table shows entries
- "Attempts Per Minute" shows spikes

**Talking point:** "The system logs every login attempt. Now let me show what happens when we run an automated attack."

### Step 5: No Defenses Attack (5 minutes)

**Before attacking:**

1. Check `config.py` - all defenses should be OFF:
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

2. Clear database:
```bash
del database.db
```

3. Refresh dashboard tab (F5)

**Terminal 3 (new window):**

```bash
cd "F:\IEH lab project"
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

When prompted: Type `yes`

**What happens:**
- Terminal 3: Shows each password attempt (`[FAIL] password123`, `[FAIL] qwerty`, ...)
- Dashboard Tab 2: Updates in real-time
  - Attempts counter increasing rapidly
  - Chart spikes
  - Blocked = 0 (no defenses)
- After ~5-10 seconds: `[SUCCESS] ✓ admin123`

**Output in Terminal 3:**
```
==============================================================
  ATTACK SUMMARY
==============================================================
Attack Type:       bruteforce
Total Attempts:    ~500 (or fewer if found)
Successful:        1
Failed:            ~499
Blocked:           0
Duration:          X.XX seconds
==============================================================
```

**Talking point:** "Without ANY security, the attack succeeded in just [X] seconds. It tried hundreds of passwords per minute. This is a real threat."

### Step 6: With Rate Limiting (5 minutes)

**Update `config.py`:**
```python
RATE_LIMIT_ENABLED = True  # ← ENABLE THIS
# Others = False
```

**Restart Flask:**
- Terminal 1: Ctrl+C
- Run: `python run.py` again
- Wait for "Running on..." message

**Clear database:**
```bash
del database.db
```

**Run attack again:**
```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**What happens:**
- Attack tries 10-15 passwords, then blocked
- Dashboard shows: "Blocked" counter increases
- Terminal 3: `[BLOCKED] ✗ Attack blocked`
- Attack stops

**Talking point:** "With rate limiting, the system restricts login attempts to 10 per minute. The attack is now impractical. But a patient attacker could still succeed by waiting. So we need more defenses."

### Step 7: With Account Lockout (5 minutes)

**Update `config.py`:**
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = True  # ← ENABLE THIS
```

**Restart Flask & clear database (same process)**

**Run attack:**
```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**What happens:**
- Attack tries 5 passwords (our threshold)
- After 5 failures, account locks
- 6th attempt: `[BLOCKED] ✗ Account temporarily locked`
- Attack stops

**Talking point:** "Account lockout blocks the attack after 5 failed attempts. The account is locked for 15 minutes. This stops targeted attacks, but it can also lock out legitimate users who forget their password."

### Step 8: With All Defenses (5 minutes)

**Update `config.py`:**
```python
RATE_LIMIT_ENABLED = True
ACCOUNT_LOCKOUT = True
IP_BLOCKING = True
CAPTCHA_ENABLED = True
ANOMALY_DETECTION = True
```

**Restart Flask & clear database**

**Run attack:**
```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**What happens:**
- Attack tries 1-2 passwords
- CAPTCHA triggers after 3 failures
- Multiple defenses activate
- Attack completely blocked

**Dashboard shows:**
- Blocked counter high
- Defense status panel shows all defenses ON
- Success rate 0%

**Talking point:** "With all defenses combined, the attack is stopped instantly. This is called defense-in-depth. No single defense is perfect, but multiple layers working together are very effective. This is how banks and Google protect you."

### Step 9: Run Full Experiments (45-60 minutes, optional)

Run all 7 scenarios automatically:

```bash
# Reset config to baseline (all OFF)
# Then:
python run_experiments.py
```

When prompted: Type `yes`

**What it does:**
- Runs all 7 scenarios automatically
- Each scenario tests 3 attacks (brute force, credential stuffing, distributed)
- Total: 21 experiments
- Takes ~60 minutes

**Generated files:**
```
results/
  ├── experiment_results.csv
  ├── graphs/
  │   ├── success_rate_comparison.html
  │   ├── block_rate_comparison.html
  │   └── duration_comparison.html
```

**View results:**
```bash
# Open CSV in Excel/spreadsheet
start results/experiment_results.csv

# Open graphs in browser
start results/graphs/success_rate_comparison.html
```

### Step 10: Review & Close (2 minutes)

**Discussion points:**

1. **Attack Success Rates:**
   - No Defense: ~100%
   - Rate Limit Only: ~10%
   - Lockout Only: ~0% (single-target)
   - CAPTCHA Only: ~0%
   - All Combined: ~0%

2. **Key Insights:**
   - Attacks are fast and automated
   - Single defenses have bypasses
   - Multiple defenses are synergistic
   - Defense design requires tradeoffs (security vs. UX)

**Close down:**
```bash
# Terminal 1: Ctrl+C (stop Flask)
# Terminal 2: Ctrl+C (stop Streamlit)
# Keep database.db for review (optional: del database.db)
```

---

## Defense Testing Cheat Sheet

**For quick reference while demoing:**

### Config Templates

**No Defense (Baseline):**
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**Rate Limit Only:**
```python
RATE_LIMIT_ENABLED = True
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
```

**Account Lockout Only:**
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = True
IP_BLOCKING = False
CAPTCHA_ENABLED = False
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

### For Each Test

1. Edit `config.py`
2. Restart Flask (Ctrl+C, then `python run.py`)
3. Clear database: `del database.db`
4. Refresh dashboard (F5 in browser)
5. Run attack script
6. Observe results
7. Note success rate & block rate

### Quick Commands

```bash
# Start all 3 components
python run.py                    # Terminal 1
streamlit run dashboard/app.py   # Terminal 2
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v  # Terminal 3

# Run credential stuffing
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v --save

# Run distributed attack
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v --save

# Run all experiments
python run_experiments.py
```

---

## Talking Points

### Opening

> "I'm going to show you how fast automated attacks can crack login systems, and what actually stops them."

### Baseline (No Defenses)

> "Without any defenses, an automated attack cracks the password in just 5-10 seconds. It tries hundreds of passwords per minute. This is the vulnerability we're protecting against."

### Single Defenses

> "Now let's enable rate limiting. The attack can only try a few passwords per minute. It gets blocked much faster, but a patient attacker could still succeed by waiting. That's why single defenses aren't enough."

### Combined Defenses

> "With all defenses active, the attack is stopped almost immediately. This is called defense-in-depth. If one defense is bypassed, others catch the attack. This is how real systems protect you."

### Closing

> "The key insight: NO SINGLE defense is perfect. You need MULTIPLE LAYERS. If one fails, others catch the attack. This is why banks use rate limiting AND account lockout AND MFA together."

---

## Expected Results Summary

| Scenario | Success Rate | Key Finding |
|----------|--------------|-------------|
| **No Defense** | ~100% | Attack succeeds immediately |
| **Rate Limit** | ~10% | Attack slowed, not stopped |
| **Lockout** | ~0% | Effective against targeted attacks |
| **IP Block** | ~5% | Can be bypassed by IP rotation |
| **CAPTCHA** | ~0% | Most effective single defense |
| **All Combined** | ~0% | Attacks completely blocked |

---

## Troubleshooting During Demo

| Problem | Solution |
|---------|----------|
| Flask won't start | Check port 5000: `netstat -ano \| findstr :5000` |
| Dashboard blank | Make a manual login first, then refresh |
| Attack script fails | Verify Flask is running on `http://localhost:5000` |
| Config changes don't work | Restart Flask (Ctrl+C then run again) |
| Database locked | Close all windows, `del database.db`, restart |
| Terminal text unclear | Run with output redirect: `command > output.txt` |

---

## Success Checklist

Before you demo:
- [ ] Installation verified (35/35 checks)
- [ ] Read this entire guide
- [ ] Tested each component once
- [ ] Browsers ready with correct URLs
- [ ] `config.py` accessible for editing
- [ ] Backup screenshots ready (just in case)

During demo:
- [ ] Flask app running on :5000
- [ ] Dashboard running on :8501
- [ ] Database cleared for clean tests
- [ ] Config matches intended scenario
- [ ] Attack scripts ready to run

---

**Ready to start?** Follow "Quick Demo" or "Full Demo" sections above. Good luck!
