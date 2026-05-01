# Testing Checklist

## Phase 1: Installation & Setup

### Step 1: Install Dependencies
```bash
cd "F:\IEH lab project"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Expected Result:** All packages install successfully

### Step 2: Verify Installation
```bash
python verify_project.py
```

**Expected Result:** All checks pass (35/35)

---

## Phase 2: Basic Functionality Testing (TASK-2.7)

### Step 3: Start Flask Application
```bash
python run.py
```

**Expected Result:**
- Server starts on http://localhost:5000
- Database created automatically
- 20 users populated
- No errors in console

### Step 4: Manual Login Test
1. Open browser: http://localhost:5000
2. Try login with: `admin` / `admin123`
3. Should redirect to dashboard
4. Verify you see "Welcome, admin!"
5. Click logout
6. Try wrong password: `admin` / `wrongpass`
7. Should see "Invalid credentials" error

**Mark TASK-2.7 as [x] if all tests pass**

---

## Phase 3: Dashboard Testing (TASK-6.9)

### Step 5: Start Dashboard (New Terminal)
```bash
cd "F:\IEH lab project"
venv\Scripts\activate
cd dashboard
streamlit run app.py
```

**Expected Result:**
- Dashboard opens at http://localhost:8501
- Shows "No login attempts recorded yet" message
- Defense status panel shows all defenses OFF

### Step 6: Generate Test Data
Manually login a few times (success and failure) to generate data.

**Expected Result:**
- Dashboard updates automatically
- Shows login attempts in table
- Charts display data
- Metrics update

**Mark TASK-6.9 as [x] if dashboard works correctly**

---

## Phase 4: Attack Script Testing (TASK-4.10)

### Step 7: Test Brute Force Attack
```bash
# New terminal
cd "F:\IEH lab project"
venv\Scripts\activate
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

Type `yes` when prompted.

**Expected Result:**
- Script runs without errors
- Finds password "admin123"
- Shows success message
- Dashboard shows all attempts in real-time

### Step 8: Test Credential Stuffing
```bash
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v
```

**Expected Result:**
- Tests multiple username:password pairs
- Finds valid accounts
- Shows compromised accounts list

### Step 9: Test Distributed Attack
```bash
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 20 -v
```

**Expected Result:**
- Rotates through fake IPs
- Shows different IPs in dashboard
- Successfully finds password

### Step 10: Test Username Enumeration
```bash
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v
```

**Expected Result:**
- Analyzes response times
- Identifies potential valid usernames

**Mark TASK-4.10 as [x] if all attack scripts work**

---

## Phase 5: Defense Testing (TASK-5.10)

### Step 11: Test Rate Limiting
1. Edit `config.py`: Set `RATE_LIMIT_ENABLED = True`
2. Restart Flask app (Ctrl+C, then `python run.py`)
3. Run brute force attack
4. **Expected:** Attack gets blocked after 10 attempts/minute

### Step 12: Test Account Lockout
1. Edit `config.py`: Set `ACCOUNT_LOCKOUT = True`, others `False`
2. Restart Flask app
3. Run brute force attack
4. **Expected:** Account locks after 5 failed attempts

### Step 13: Test IP Blocking
1. Edit `config.py`: Set `IP_BLOCKING = True`, others `False`
2. Restart Flask app
3. Run brute force attack with many attempts
4. **Expected:** IP gets permanently blocked

### Step 14: Test CAPTCHA
1. Edit `config.py`: Set `CAPTCHA_ENABLED = True`, others `False`
2. Restart Flask app
3. Run brute force attack
4. **Expected:** CAPTCHA challenge appears after 3 failures

### Step 15: Test All Defenses Combined
1. Edit `config.py`: Set ALL defenses to `True`
2. Restart Flask app
3. Run all attack scripts
4. **Expected:** Very low success rate, most attempts blocked

**Mark TASK-5.10 as [x] if all defenses work correctly**

---

## Phase 6: Database Utilities

### Step 16: Test Database Commands
```bash
# View statistics
python db_utils.py stats

# Clear database (for fresh experiments)
python db_utils.py clear
```

---

## Completion Checklist

- [ ] Dependencies installed successfully
- [ ] Flask app starts without errors
- [ ] Manual login/logout works
- [ ] Dashboard displays data correctly
- [ ] Brute force attack works
- [ ] Credential stuffing works
- [ ] Distributed attack works
- [ ] Username enumeration works
- [ ] Rate limiting defense works
- [ ] Account lockout defense works
- [ ] IP blocking defense works
- [ ] CAPTCHA defense works
- [ ] All defenses combined work
- [ ] Database utilities work

---

## Next Phase After Testing

Once all tests pass, proceed to:
- **MILESTONE 7**: Run structured experiments
- Record metrics for each scenario
- Generate comparison graphs
- Write analysis report
