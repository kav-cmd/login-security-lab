# 🚀 START HERE - Complete Project Guide

## Welcome to Your Login Security Testbed!

This is your **master guide** to complete the project. Follow these steps in order.

---

## 📍 Current Status

**✅ COMPLETED:**
- All code written (35 files)
- All documentation created (12 guides)
- All utilities and batch files ready
- Project structure complete

**⏳ REMAINING:**
- Install dependencies (15 min)
- Test the system (1-2 hours)
- Run experiments (4-6 hours)
- Write final report (2-3 hours)
- Prepare presentation (2-3 hours)

**Total Time to Complete: 10-15 hours**

---

## 🎯 Step-by-Step Completion Path

### PHASE 1: Installation (15 minutes)

**Step 1.1: Open Command Prompt**
```cmd
cd "F:\IEH lab project"
```

**Step 1.2: Create Virtual Environment**
```cmd
python -m venv venv
```

**Step 1.3: Activate Virtual Environment**
```cmd
venv\Scripts\activate
```
You should see `(venv)` in your prompt.

**Step 1.4: Install Dependencies**
```cmd
pip install -r requirements.txt
```
Wait for all packages to install (~5 minutes).

**Step 1.5: Verify Installation**
```cmd
python verify_project.py
```
Expected: "SUCCESS: ALL CHECKS PASSED (35/35)"

**✓ Mark in project.md:** TASK-1.4 as [x]

---

### PHASE 2: First Run Test (30 minutes)

**Step 2.1: Start Flask Application**

Open Command Prompt #1:
```cmd
cd "F:\IEH lab project"
venv\Scripts\activate
python run.py
```

Or double-click: **`start_flask.bat`**

Expected output:
```
======================================================================
  LOGIN SECURITY TESTBED
  Flask Application Starting...
======================================================================
  URL: http://localhost:5000
```

**Keep this window open!**

**Step 2.2: Test Manual Login**

1. Open browser: http://localhost:5000
2. You should see the login page
3. Try: `admin` / `wrongpassword` → Should fail
4. Try: `admin` / `admin123` → Should succeed
5. You should see "Welcome, admin!" dashboard
6. Click Logout

**✓ Mark in project.md:** TASK-2.7 as [x]

**Step 2.3: Start Dashboard**

Open Command Prompt #2:
```cmd
cd "F:\IEH lab project"
venv\Scripts\activate
cd dashboard
streamlit run app.py
```

Or double-click: **`start_dashboard.bat`**

Dashboard should open automatically in browser at http://localhost:8501

**Keep this window open!**

**Step 2.4: Verify Dashboard**

1. Dashboard should show "No login attempts recorded yet"
2. Defense status panel shows all defenses OFF
3. Try logging in manually again (success and failure)
4. Dashboard should update automatically
5. You should see attempts in the table

**✓ Mark in project.md:** TASK-6.9 as [x]

---

### PHASE 3: Attack Testing (1 hour)

**Step 3.1: Test Brute Force Attack**

Open Command Prompt #3:
```cmd
cd "F:\IEH lab project"
venv\Scripts\activate
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

Or double-click: **`test_bruteforce.bat`**

1. Type `yes` when prompted
2. Watch the attack run
3. Watch dashboard update in real-time
4. Attack should succeed and find password "admin123"

Expected output:
```
[+] ATTACK SUCCESSFUL!
[+] Username: admin
[+] Password: admin123
[+] Attempts: ~50
```

**Step 3.2: Test Credential Stuffing**

```cmd
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v
```

Or double-click: **`test_credential_stuffing.bat`**

Should find multiple valid accounts.

**Step 3.3: Test Distributed Attack**

```cmd
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 20 -v
```

Should show different IPs in dashboard.

**Step 3.4: Test Username Enumeration**

```cmd
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v
```

Should identify potential valid usernames.

**✓ Mark in project.md:** TASK-4.10 as [x]

---

### PHASE 4: Defense Testing (1 hour)

**Step 4.1: Clear Database**

```cmd
python db_utils.py clear
```
Type `yes` to confirm.

**Step 4.2: Test Rate Limiting**

1. Open `config.py` in a text editor
2. Change: `RATE_LIMIT_ENABLED = True`
3. Save file
4. Restart Flask app (Ctrl+C in Flask window, then run again)
5. Run brute force attack again
6. Attack should get blocked after ~10 attempts

**Step 4.3: Test Account Lockout**

1. Edit `config.py`: Set `ACCOUNT_LOCKOUT = True`, others `False`
2. Restart Flask app
3. Clear database
4. Run brute force attack
5. Account should lock after 5 failed attempts

**Step 4.4: Test All Defenses**

1. Edit `config.py`: Set ALL defenses to `True`
2. Restart Flask app
3. Clear database
4. Run brute force attack
5. Attack should be blocked almost immediately

**✓ Mark in project.md:** TASK-5.10 as [x]

---

### PHASE 5: Run Experiments (4-6 hours)

**Important:** Follow this process for each scenario!

**For Each Scenario:**
1. Edit `config.py` with scenario configuration
2. Restart Flask app
3. Clear database: `python db_utils.py clear`
4. Run attack scripts
5. Record results in `EXPERIMENT_RESULTS_TEMPLATE.md`
6. Take dashboard screenshots
7. Save metrics

**Scenario List:**
1. ✓ Baseline (all defenses OFF)
2. ✓ Rate limiting only
3. ✓ Account lockout only
4. ✓ IP blocking only
5. ✓ CAPTCHA only
6. ✓ All defenses combined
7. ✓ Distributed vs all defenses

**Metrics to Record:**
- Total attempts
- Successful attempts
- Blocked attempts
- Time to compromise
- Success rate
- Time to block

**✓ Mark in project.md:** TASK-7.1 through TASK-7.7 as [x]

---

### PHASE 6: Analysis & Report (2-3 hours)

**Step 6.1: Analyze Results**

1. Open `EXPERIMENT_RESULTS_TEMPLATE.md`
2. Fill in all recorded metrics
3. Calculate success rate reductions
4. Compare defense effectiveness
5. Identify patterns

**Step 6.2: Create Comparison Charts**

Using your data, create:
- Success rate comparison (bar chart)
- Time to compromise (line chart)
- Defense effectiveness matrix
- Before/after comparisons

**Step 6.3: Write Analysis**

Answer these questions:
- Which defense was most effective?
- Which defense was least effective?
- How effective were combined defenses?
- Can distributed attacks bypass defenses?
- What are the recommendations?

**✓ Mark in project.md:** TASK-7.8, TASK-7.9, TASK-7.10 as [x]

---

### PHASE 7: Presentation (2-3 hours)

**Step 7.1: Create Slides**

Use `PRESENTATION_OUTLINE.md` as template:
- 25 slides covering all aspects
- Include screenshots from your dashboard
- Add your experiment results
- Include comparison charts

**Step 7.2: Practice Demo**

Follow `DEMO_SCRIPT.md`:
- Practice the 7-minute walkthrough
- Test all components work
- Prepare backup screenshots
- Time yourself

**Step 7.3: Prepare for Q&A**

Review:
- VULNERABILITIES.md (know the weaknesses)
- HARDENING_GUIDE.md (know the solutions)
- Your experiment results (know the numbers)

**✓ Mark in project.md:** TASK-8.3, TASK-8.4 as [x]

---

### PHASE 8: Final Submission

**Step 8.1: Final Code Review**

- Check all files are present
- Remove any test data
- Verify documentation is complete
- Test on fresh terminal

**Step 8.2: Create Submission Package**

Include:
- All source code
- All documentation
- Experiment results
- Presentation slides
- README with setup instructions

**✓ Mark in project.md:** TASK-8.5 as [x]

---

## 📊 Progress Tracking

Update `project.md` as you complete each task:
- Change `[ ]` to `[x]` for completed tasks
- Change `[ ]` to `[~]` for in-progress tasks

**Current Progress:** 50/67 tasks (75%)

---

## 🆘 Troubleshooting

### Problem: Dependencies won't install
**Solution:**
```cmd
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Problem: Flask won't start
**Solution:**
- Check Python version: `python --version` (need 3.10+)
- Check port 5000: `netstat -ano | findstr :5000`
- Kill process if needed

### Problem: Dashboard won't load
**Solution:**
- Make sure Flask is running first
- Check port 8501 is free
- Try: `streamlit run dashboard/app.py --server.port 8502`

### Problem: Attack script fails
**Solution:**
- Verify Flask is running on localhost:5000
- Check wordlist files exist
- Make sure virtual environment is activated

### Problem: Database locked
**Solution:**
```cmd
python db_utils.py clear
```

---

## 📚 Quick Reference

**Essential Commands:**
```cmd
# Activate environment
venv\Scripts\activate

# Start Flask
python run.py

# Start Dashboard
cd dashboard && streamlit run app.py

# Run attack
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v

# Clear database
python db_utils.py clear

# View stats
python db_utils.py stats
```

**Essential Files:**
- `config.py` - Toggle defenses
- `project.md` - Track progress
- `EXPERIMENT_RESULTS_TEMPLATE.md` - Record results
- `DEMO_SCRIPT.md` - Presentation guide

---

## ✅ Success Checklist

- [ ] Dependencies installed
- [ ] Flask app runs
- [ ] Manual login works
- [ ] Dashboard displays data
- [ ] Brute force attack works
- [ ] All attack scripts tested
- [ ] All defenses tested
- [ ] Experiments completed
- [ ] Results analyzed
- [ ] Report written
- [ ] Presentation created
- [ ] Demo practiced

---

## 🎯 Your Next Action

**RIGHT NOW, DO THIS:**

1. Open Command Prompt
2. Run: `cd "F:\IEH lab project"`
3. Run: `python -m venv venv`
4. Run: `venv\Scripts\activate`
5. Run: `pip install -r requirements.txt`
6. Run: `python verify_project.py`

**Once that works, come back and continue with PHASE 2!**

---

## 📞 Need Help?

Refer to these guides:
- **INSTALL.md** - Detailed installation
- **QUICKSTART_WINDOWS.md** - Windows-specific help
- **TESTING_CHECKLIST.md** - Detailed test procedures
- **STATUS.md** - Current progress overview

---

**You're 75% done! Just testing and experiments remaining!** 💪

**Estimated time to complete: 10-15 hours of focused work**

**Good luck! 🚀**
