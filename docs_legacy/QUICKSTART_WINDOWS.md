# Quick Start Guide - Windows

## 🚀 Step-by-Step Setup

### 1. Install Dependencies (First Time Only)

Open Command Prompt in the project folder and run:

```cmd
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Or simply double-click: **`verify.bat`** to check installation.

---

## 🎮 Running the Application

### Method 1: Using Batch Files (Easiest)

**Step 1:** Double-click **`start_flask.bat`**
- Opens Flask app on http://localhost:5000
- Keep this window open

**Step 2:** Double-click **`start_dashboard.bat`** (in a new window)
- Opens dashboard on http://localhost:8501
- Keep this window open

**Step 3:** Double-click **`test_bruteforce.bat`**
- Runs attack simulation
- Watch results in dashboard

### Method 2: Using Command Prompt

**Terminal 1 - Flask App:**
```cmd
venv\Scripts\activate
python run.py
```

**Terminal 2 - Dashboard:**
```cmd
venv\Scripts\activate
cd dashboard
streamlit run app.py
```

**Terminal 3 - Attack:**
```cmd
venv\Scripts\activate
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

---

## 🧪 Testing Scenarios

### Test 1: Baseline (No Defenses)

1. Make sure all defenses are OFF in `config.py`
2. Start Flask app and dashboard
3. Run: **`test_bruteforce.bat`**
4. **Expected:** Attack succeeds, finds password quickly

### Test 2: With Rate Limiting

1. Edit `config.py`: Set `RATE_LIMIT_ENABLED = True`
2. Restart Flask app (Ctrl+C, then run again)
3. Run: **`test_bruteforce.bat`**
4. **Expected:** Attack gets blocked after 10 attempts/minute

### Test 3: With All Defenses

1. Edit `config.py`: Set ALL defenses to `True`
2. Restart Flask app
3. Run: **`test_bruteforce.bat`**
4. **Expected:** Attack blocked quickly, very low success rate

---

## 🛠️ Utility Scripts

- **`verify.bat`** - Check project setup
- **`manage_database.bat`** - View stats or clear database
- **`test_bruteforce.bat`** - Run brute force attack
- **`test_credential_stuffing.bat`** - Run credential stuffing attack

---

## 📊 Viewing Results

1. **Dashboard** (http://localhost:8501)
   - Live attack monitoring
   - Charts and graphs
   - Defense status

2. **Database Stats**
   - Run: **`manage_database.bat`** → Option 1

3. **Browser Login**
   - Go to: http://localhost:5000
   - Try: `admin` / `admin123`

---

## 🔧 Troubleshooting

**Flask app won't start:**
- Check if port 5000 is already in use
- Make sure virtual environment is activated

**Dashboard won't start:**
- Check if port 8501 is already in use
- Make sure Flask app is running first

**Attack script errors:**
- Make sure Flask app is running on localhost:5000
- Check that wordlist files exist

**Clear everything and start fresh:**
```cmd
venv\Scripts\activate
python db_utils.py clear
python run.py
```

---

## ✅ Success Indicators

You'll know everything is working when:
- ✓ Flask app shows "Running on http://127.0.0.1:5000"
- ✓ Dashboard opens in browser automatically
- ✓ Attack script shows "ATTACK SUCCESSFUL"
- ✓ Dashboard updates in real-time with attempts
- ✓ You can login manually at localhost:5000

---

## 📝 Next Steps After Testing

Once basic testing works:
1. Test each defense mechanism individually
2. Run experiments with different configurations
3. Record metrics for comparison
4. Generate analysis report

See **`TESTING_CHECKLIST.md`** for detailed test procedures.
