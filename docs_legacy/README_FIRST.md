# 🎬 READ THIS FIRST - Your Entry Point

> You just downloaded a login security testbed with 20+ markdown files. Start here.

---

## ⏱️ You have 5 minutes? Read this:

**This project demonstrates authentication attacks and defenses:**

- 🟢 Run a vulnerable login app on `localhost:5000`
- 🔴 Launch 4 automated attacks against it
- 🛡️ Enable/disable 5 defenses in `config.py`
- 📊 Watch real-time dashboard on `localhost:8501`
- 📈 Generate experiment results and graphs

**Result:** Show that combined defenses work, single defenses don't.

---

## 🚀 You have 15 minutes? Do this:

```bash
# Terminal 1
cd "F:\IEH lab project"
python run.py

# Terminal 2 (new window)
cd "F:\IEH lab project"
streamlit run dashboard/app.py

# Terminal 3 (new window)
cd "F:\IEH lab project"
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v

# Browser Tab 1: http://localhost:5000
# Browser Tab 2: http://localhost:8501
# Watch the attack succeed in the dashboard!
```

Then read: **DEMO_MASTER_GUIDE.md** (10 min)

---

## 📚 You want to understand everything? Read in order:

1. **DEMO_MASTER_GUIDE.md** (⭐ Start here) - 15 min
2. **DEMONSTRATION_GUIDE.md** - 30 min step-by-step
3. **QUICK_REFERENCE_CARD.md** - 5 min cheat sheet
4. **README.md** - 10 min full overview
5. **VULNERABILITIES.md** - 10 min what's weak?
6. **HARDENING_GUIDE.md** - 15 min how to fix?

Then optionally:

- **project.md** (45 min) - Complete technical spec
- **PRESENTATION_OUTLINE.md** (10 min) - Presentation slides
- **MARKDOWN_FILES_GUIDE.md** (10 min) - Map of all docs

---

## 🎯 Pick your path:

### 🏃 "I want to DEMO this in 20 minutes"

→ Read **DEMO_MASTER_GUIDE.md** + **QUICK_REFERENCE_CARD.md**  
→ Then follow **DEMONSTRATION_GUIDE.md steps 1-5**

### 🧑‍🎓 "I want to LEARN everything"

→ Read **README.md** then **VULNERABILITIES.md** then **HARDENING_GUIDE.md**  
→ Then follow **DEMONSTRATION_GUIDE.md all 10 steps**

### 👨‍💼 "I need to PRESENT this"

→ Read **PRESENTATION_OUTLINE.md** + **DEMO_SCRIPT.md**  
→ Run experiments: `python run_experiments.py`  
→ Show results + graphs

### 🔧 "I need to SET THIS UP"

→ Read **INSTALL.md** then **QUICK_START.md**  
→ Run `python verify_project.py` (should show 35/35)

---

## 🗺️ The 23 Markdown Files (you don't need to read all!)

| Must Read                   | Should Read             | Reference             | Optional                       |
| --------------------------- | ----------------------- | --------------------- | ------------------------------ |
| **DEMO_MASTER_GUIDE.md** ⭐ | VULNERABILITIES.md      | README.md             | project.md                     |
| **DEMONSTRATION_GUIDE.md**  | HARDENING_GUIDE.md      | QUICK_START.md        | STATUS.md                      |
| **QUICK_REFERENCE_CARD.md** | PRESENTATION_OUTLINE.md | INSTALL.md            | COMPLETION_CHECKLIST.md        |
|                             | DEMO_SCRIPT.md          | QUICKSTART_WINDOWS.md | TESTING_CHECKLIST.md           |
|                             |                         | START_HERE.md         | EXPERIMENT_RESULTS_TEMPLATE.md |
|                             |                         |                       | PROJECT_SUMMARY.md             |
|                             |                         |                       | FINAL_SUMMARY.md               |
|                             |                         |                       | MARKDOWN_FILES_GUIDE.md        |
|                             |                         |                       | SETUP_COMMANDS.md              |

---

## 🎬 THE 10-STEP DEMO (What you'll do)

```
1. Verify Installation (2 min)        python verify_project.py
2. Start Flask App (2 min)            python run.py
3. Start Dashboard (2 min)            streamlit run dashboard/app.py
4. Test Manual Login (2 min)          http://localhost:5000
5. Run Brute Force Attack (5 min)     python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt
6. Enable Rate Limiting (5 min)       Edit config.py, restart, attack again
7. Test Other Defenses (15 min)       IP blocking, CAPTCHA, all combined
8. View Results (5 min)               Check http://localhost:8501 dashboard
9. Run Full Experiments (optional)     python run_experiments.py (60 min)
10. Review Findings (5 min)            Read results/experiment_results.csv
```

**Total time: 30-60 minutes depending on depth**

---

## ✅ What you need before starting:

- [ ] Python 3.10+ installed
- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip install -r requirements.txt`
- [ ] Run `python verify_project.py` → should say "35/35 PASSED"
- [ ] 3+ terminal windows open
- [ ] 2+ browser tabs ready
- [ ] Read **DEMO_MASTER_GUIDE.md** (15 min)

---

## 🎓 What you'll learn:

✅ **How attacks work** (they're FAST and AUTOMATED)  
✅ **Why single defenses fail** (each has a bypass)  
✅ **Why multiple defenses matter** (layered security)  
✅ **Which defense is strongest** (CAPTCHA vs others)  
✅ **How to build secure systems** (best practices)

---

## 📊 Expected Results (spoiler):

| Scenario             | Success Rate | Key Insight                   |
| -------------------- | ------------ | ----------------------------- |
| No defense           | ~100%        | Attacks succeed instantly ⚠️  |
| Rate limit only      | ~10%         | Slows down but not perfect    |
| Account lockout only | ~90%         | Works for single account      |
| IP blocking only     | ~80%         | Defeated by IP rotation       |
| CAPTCHA only         | ~0%          | Most effective single defense |
| **All combined**     | **~0%**      | **Defense in depth wins** ✅  |

---

## 🚀 Quick start (if you already installed):

```bash
cd "F:\IEH lab project"

# Terminal 1:
python run.py

# Terminal 2:
streamlit run dashboard/app.py

# Terminal 3:
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt

# Browsers:
http://localhost:5000
http://localhost:8501
```

Watch the dashboard update in real-time as the attack runs!

---

## 🐛 Something broke?

**Most common issues:**

```
"Flask won't start"
→ `netstat -ano | findstr :5000`

"Attack script fails"
→ Make sure Flask is running

"Dashboard shows nothing"
→ Did you make 1 manual login first?

"Module not found"
→ `pip install -r requirements.txt`
```

See **INSTALL.md** troubleshooting section for more.

---

## 📖 Next Steps

1. **Pick your path above** (demo / learn / present / setup)
2. **Read the recommended markdown files** for your path
3. **Follow the steps** in DEMONSTRATION_GUIDE.md
4. **Show someone** what you built!
5. **Answer the 5 key questions** in DEMO_MASTER_GUIDE.md

---

## 💬 The Big Idea

> "Without defenses, attackers crack your login in 5 seconds.  
> With one defense, they find a workaround.  
> With multiple defenses, it's impossible.  
> This is why security is about layers, not silver bullets."

---

## 🎬 Ready to start?

**Pick ONE:**

- [ ] Quick demo → **DEMO_MASTER_GUIDE.md** (15 min read, then demo)
- [ ] Full understanding → **DEMONSTRATION_GUIDE.md** (30 min read, then 60 min demo)
- [ ] Present to others → **PRESENTATION_OUTLINE.md** (create slides)
- [ ] Deep learning → **README.md** + **VULNERABILITIES.md** + **HARDENING_GUIDE.md**

**Then:**

1. Open your chosen markdown file
2. Follow it step by step
3. Run the commands
4. Watch it work
5. Celebrate your secure system! 🎉

---

**Questions? Everything is documented. Use** `MARKDOWN_FILES_GUIDE.md` **to find answers.**
