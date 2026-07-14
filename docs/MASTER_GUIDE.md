# Login Security Testbed — Master Project Guide (Single Document)

> **Project type:** Controlled cybersecurity testbed (local-only) for demonstrating and evaluating authentication attacks and defenses.
>
> **Safety / Ethics:** This project is designed for **authorized, local testing only** (e.g., `http://localhost:5000`). Do **not** use the included attack scripts against any external system.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [System Architecture](#2-system-architecture)
3. [Setup & Execution Guide](#3-setup--execution-guide)
4. [Feature Demonstration Guide](#4-feature-demonstration-guide)
5. [Attack Vector Simulation](#5-attack-vector-simulation)
6. [Defense Mechanisms](#6-defense-mechanisms)
7. [Attack vs Defense Mapping](#7-attack-vs-defense-mapping)
8. [Expected Results & Outputs](#8-expected-results--outputs)
9. [Demonstration Flow (Live Demo Script)](#9-demonstration-flow-live-demo-script)
10. [Cleanup & Reset (Optional)](#10-cleanup--reset-optional)

---

## 1. Project Overview

### Purpose

This repository implements a **login security testbed** that lets you:

- Run an intentionally weak (baseline) Flask login system.
- Launch common automated login attacks (brute force, credential stuffing, distributed/IP rotation, username enumeration).
- Toggle multiple defensive controls via a single config file (`config.py`).
- Observe behavior in real-time via a Streamlit monitoring dashboard.
- Run automated, repeatable experiments across multiple defense scenarios and generate comparative results.

### Problem It Solves

Authentication endpoints are frequently targeted by automated attacks (password guessing, reuse of leaked passwords, distributed attempts). In real systems, defenses are often added piecemeal and their effectiveness is not always measured.

This project provides a **repeatable environment** to:

- Demonstrate how quickly weak defenses fail.
- Compare defenses under consistent attack conditions.
- Teach **defense-in-depth** and the security-vs-usability trade-offs.

### Key Features (What’s Implemented)

**Core system**

- Vulnerable login flow (weak hashing by design): `app/models.py` (`User.check_password()` uses MD5).
- SQLite-backed logging of every login attempt: `app/logger.py` + `app/routes.py` + `app/models.py`.

**Attack simulations** (standalone scripts)

- Brute force: `attacks\attack_bruteforce.py`
- Credential stuffing: `attacks\attack_credential_stuffing.py`
- Distributed/IP rotation: `attacks\attack_distributed.py`
- Username enumeration (timing-based): `attacks\attack_username_enum.py`

**Defenses** (toggleable via `config.py`)

- Rate limiting (Flask-Limiter)
- Account lockout
- IP blocking
- CAPTCHA (math challenge)
- Anomaly detection (attempt burst rule)
- MFA simulation (OTP)
- Pwned password check (HaveIBeenPwned k-anonymity API)
- Password strength checker helper (implemented, but **not wired to a route in this build**)

**Monitoring & evaluation**

- Real-time dashboard: `dashboard\app.py` (Streamlit)
- Automated experiment runner: `run_experiments.py`

---

## 2. System Architecture

### End-to-End Workflow (Happy Path)

1. **User or attack script** sends `POST /login` with `username` and `password`.
2. Flask `/login` route executes **defense checks** in a fixed order (see [Decision Points](#decision-points-in-login-flow)).
3. If a defense triggers:
   - The system returns an error (usually **HTTP 403** or **HTTP 429**) and logs the attempt as **blocked**.
4. If defenses do not block the request:
   - The system verifies the password against the database (MD5 baseline check).
   - Logs the attempt as **success** or **failure**.
5. The **Streamlit dashboard** continuously reads the SQLite database and updates charts/metrics.

### Components & Interactions

#### A) Flask Login Application (Target)

- Entry: `run.py` → `app.create_app()` in `app\__init__.py`
- Routes: `app\routes.py`
- Defenses: `app\defenses.py`
- Models (SQLite tables): `app\models.py`

Key endpoints:

- `GET /login` → login HTML (`app/templates/login.html`)
- `POST /login` → login API/flow (defenses + auth)
- `GET /dashboard` → protected page (requires Flask-Login session)
- `GET /logout`
- `GET|POST /mfa_verify`
- Dashboard APIs:
  - `GET /api/logs?limit=100`
  - `GET /api/metrics`
  - `GET /api/config`
  - `GET /api/stats`

#### B) SQLite Database (Single file)

- File: `database.db` (path set by `config.DATABASE_PATH`)
- Schema is created by SQLAlchemy (`db.create_all()` in `app\__init__.py`) and also by `db_utils.py` when needed.

Tables:

- `users` — accounts, failed_attempts, lockouts, MFA secret field
- `login_attempts` — IP, username, timestamp, success, blocked
- `metrics` — experiment summary storage (not the same as `results/experiment_results.csv`)
- `blocked_ips` — permanent IP ban list

#### C) Attack Scripts (Attacker Side)

- Each script uses `requests` to send repeated `POST` requests to `http://localhost:5000/login`.
- Inputs come from wordlists in `wordlists\`.
- Optional `--save` writes JSON results to `results\`.

#### D) Streamlit Dashboard (Monitoring)

- File: `dashboard\app.py`
- Reads SQLite directly and displays:
  - total/blocked/success/failed counters
  - attempts per minute
  - status distribution
  - top IPs
  - recent attempts table
  - defense config status (sidebar)

**Note:** The dashboard’s “Attack Type Breakdown” section only appears if the `login_attempts.attack_type` column is populated. In the current code, `log_attempt()` is called without `attack_type`, so this field is typically `NULL`.

#### E) Experiment Runner (Automation)

- File: `run_experiments.py`
- Automatically:
  - edits `config.py` toggles for each scenario
  - clears `database.db`
  - starts/stops Flask for each run
  - runs attack scripts (auto-feeding `yes` to the “LOCAL TESTING ONLY” prompt)
  - consolidates results into `results\experiment_results.csv`
  - generates Plotly HTML graphs in `results\graphs\`

### Decision Points in Login Flow

`POST /login` in `app\routes.py` applies defenses in this order:

1. **IP Blocking** → if blocked: log blocked + `403` JSON
2. **Anomaly Detection** → if anomalous: print alert, log blocked + `429` JSON
3. **Account Lockout** → if locked: log blocked + `429` JSON
4. **CAPTCHA** → if required and not solved: returns **HTML CAPTCHA page** (`200`) and sets session answer
5. **HIBP Pwned Password Check** → if pwned: log blocked + `403` JSON
6. **Credential verification** (MD5 baseline)
7. **MFA** (if enabled) → redirect to `/mfa_verify` after password success

---

## 3. Setup & Execution Guide

### Prerequisites

- Python **3.10+**
- Internet access (optional, only needed for HIBP pwned-password checks)

### Step 0 — Open a terminal in the project root

```bat
cd "F:\IEH lab project"
```

### Step 1 — Create and activate a virtual environment

```bat
python -m venv venv
venv\Scripts\activate
```

### Step 2 — Install dependencies

```bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3 — Verify the project

```bat
python verify_project.py
```

Expected success indicator:

- `SUCCESS: ALL CHECKS PASSED (...)`

### Step 4 — Start the Flask app (Terminal 1)

```bat
python run.py
```

Open in browser:

- http://localhost:5000

### Step 5 — Start the Streamlit dashboard (Terminal 2)

```bat
streamlit run dashboard\app.py
```

Open in browser:

- http://localhost:8501

### Step 6 — (Optional) Use Windows helper scripts

These scripts activate `venv` and run common commands:

- `start_flask.bat`
- `start_dashboard.bat`
- `verify.bat`
- `manage_database.bat`

---

## 4. Feature Demonstration Guide

This section is written as “feature card” instructions: what it does, how to trigger it, expected outcome.

### 4.1 Web Login (Baseline Functionality)

- **What it does:** Allows interactive login to a protected page.
- **How to use:**
  1. Open http://localhost:5000
  2. Log in with a test account.
     - Example: `admin / admin123`
- **Expected result:** Browser redirects to `/dashboard` and shows “Welcome, admin!”.

### 4.2 Logging of Login Attempts

- **What it does:** Records every attempt in SQLite (`login_attempts`).
- **How to trigger:** Perform a successful and a failed login (or run an attack script).
- **Expected result:**
  - Dashboard shows non-zero “Total Attempts”.
  - `GET /api/logs` returns recent attempts.

### 4.3 Monitoring Dashboard (Streamlit)

- **What it does:** Visualizes attempts and defense configuration.
- **How to use:** Open http://localhost:8501
- **Expected result:**
  - Counters for Total/Blocked/Successful/Failed.
  - “Recent Login Attempts” table updates every ~2 seconds.

### 4.4 Defense Toggle System (`config.py`)

- **What it does:** Enables/disables defenses without code edits.
- **How to use:** Edit `config.py`, set flags to `True/False`, then **restart Flask**.
- **Expected result:** Dashboard sidebar reflects updated ON/OFF states.

### 4.5 JSON API Endpoints (for monitoring/integration)

- **What it does:** Exposes operational data as JSON.
- **How to use (examples):**
  - `http://localhost:5000/api/metrics`
  - `http://localhost:5000/api/config`
  - `http://localhost:5000/api/logs?limit=20`
- **Expected result:** JSON payloads reflecting the live database/config.

### 4.6 Automated Experiment Runner

- **What it does:** Runs multiple defense scenarios and writes consolidated results.
- **How to use:**
  ```bat
  python run_experiments.py
  ```
  Type `yes` when prompted.
- **Expected result:**
  - `results\experiment_results.csv`
  - `results\graphs\success_rate_comparison.html`
  - `results\graphs\block_rate_comparison.html`
  - `results\graphs\duration_comparison.html`

### 4.7 Database Utilities

- **What it does:** Initialize / reset / inspect DB.
- **How to use:**
  ```bat
  python db_utils.py init
  python db_utils.py stats
  python db_utils.py clear
  ```
- **Expected result:** Console output confirming schema creation, stats counts, or reset.

---

## 5. Attack Vector Simulation

> All attack scripts prompt: `Confirm this is LOCAL TESTING ONLY (yes/no):` — type `yes`.

### 5.1 Brute Force Attack

- **Attack name:** Brute force (dictionary-based)
- **Objective:** Guess one user’s password by trying many candidates.
- **Script:** `attacks\attack_bruteforce.py`
- **Inputs:**
  - `--username` target (e.g., `admin`)
  - `--wordlist` password list (e.g., `wordlists\passwords.txt`)
- **How to simulate (steps):**
  1. Start Flask (`python run.py`).
  2. Run:
     ```bat
     python attacks\attack_bruteforce.py -u admin -w wordlists\passwords.txt -v --save
     ```
  3. Observe dashboard updates.
- **System behavior:**
  - Sends repeated `POST /login`.
  - Receives `401` on invalid credentials, or `403/429` if blocked.
- **Observed outcome (example artifact):**
  - JSON saved in `results\bruteforce_*.json` with fields: attempts, success, blocked, duration_sec.

### 5.2 Credential Stuffing

- **Attack name:** Credential stuffing
- **Objective:** Compromise accounts by reusing leaked username:password pairs.
- **Script:** `attacks\attack_credential_stuffing.py`
- **Inputs:** `wordlists\credentials.txt` (format: `username:password`)
- **How to simulate:**
  ```bat
  python attacks\attack_credential_stuffing.py -c wordlists\credentials.txt -v --save
  ```
- **System behavior:**
  - Iterates pairs and attempts login for each.
  - May compromise multiple accounts.
- **Observed outcome:**
  - Results include `cracked_accounts` array.

### 5.3 Distributed / IP Rotation Attack

- **Attack name:** Distributed attack (IP rotation simulation)
- **Objective:** Reduce effectiveness of IP-based defenses by rotating “client IP”.
- **Script:** `attacks\attack_distributed.py`
- **How it’s simulated:** Sends `X-Forwarded-For: <fake_ip>` header.
- **Inputs:**
  - target username
  - wordlist
  - `--pool-size` number of fake IPs
- **How to simulate:**
  ```bat
  python attacks\attack_distributed.py -u admin -w wordlists\passwords.txt -p 50 -v --save
  ```
- **Important implementation note:**
  - The Flask app uses `X-Forwarded-For` for **IP blocking/anomaly checks** (`get_client_ip()` in `app/routes.py`).
  - Flask-Limiter’s key function uses `request.remote_addr` by default (`app/__init__.py`), so IP rotation **may not bypass rate limiting** in this build.

### 5.4 Username Enumeration (Timing)

- **Attack name:** Username enumeration (timing analysis)
- **Objective:** Identify likely-valid usernames by measuring response time differences.
- **Script:** `attacks\attack_username_enum.py`
- **Inputs:** `wordlists\usernames.txt`
- **How to simulate:**
  ```bat
  python attacks\attack_username_enum.py -u wordlists\usernames.txt -v --save
  ```
- **System behavior:**
  - Measures average response time per username.
  - Reports “potential valid usernames” if timing is significantly slower.

---

## 6. Defense Mechanisms

Each defense lists: what it addresses, implementation, where it applies, mitigation behavior, and before/after.

### 6.1 Rate Limiting (Flask-Limiter)

- **Defense name:** Rate limiting
- **Addresses:** High-rate brute-force / stuffing from a single client.
- **Implementation:** `@limiter.limit(...)` decorator on `/login` in `app/routes.py`.
- **Config keys:**
  - `RATE_LIMIT_ENABLED` (bool)
  - `RATE_LIMIT_REQUESTS` (requests/minute)
- **Mitigation:** Excess requests are rejected by Flask-Limiter (typically HTTP **429**).
- **Before vs after:**
  - **Before:** attacker can attempt continuously.
  - **After:** attacker quickly hits 429 and must wait.

### 6.2 Account Lockout

- **Defense name:** Account lockout
- **Addresses:** Targeted brute force against a single account.
- **Implementation:**
  - State: `users.failed_attempts`, `users.locked_until` (`app/models.py`)
  - Logic: `handle_failed_attempt()` and `is_account_locked()` (`app/defenses.py`)
  - Enforced in `app/routes.py`.
- **Config keys:**
  - `ACCOUNT_LOCKOUT`
  - `LOCKOUT_THRESHOLD` (default 5)
  - `LOCKOUT_DURATION_MIN` (default 15)
- **Mitigation:** After threshold failures, subsequent attempts return HTTP **429** with `{"error":"Account temporarily locked"}`.

### 6.3 IP Blocking

- **Defense name:** IP blocking
- **Addresses:** Persistent high-volume attack from one client.
- **Implementation:**
  - Table: `blocked_ips` (`app/models.py`)
  - Logic: `is_ip_blocked()` and `block_ip()` (`app/defenses.py`)
  - Counter: failed attempts per IP over a time window (`handle_failed_attempt()`)
- **Config keys:**
  - `IP_BLOCKING`
  - `IP_BLOCK_THRESHOLD` (default 50)
- **Mitigation:** Once blocked, requests return HTTP **403** with `{"error":"Your IP has been blocked"}`.

### 6.4 CAPTCHA (Math Challenge)

- **Defense name:** CAPTCHA
- **Addresses:** Automated scripts that cannot solve interactive challenges.
- **Implementation:**
  - `generate_captcha()`, `verify_captcha()`, `needs_captcha()` in `app/defenses.py`
  - UI: `app/templates/captcha.html`
  - Enforced in `app/routes.py`.
- **Config keys:**
  - `CAPTCHA_ENABLED`
  - `CAPTCHA_TRIGGER` (default 3 failed attempts)
- **Mitigation:** After trigger, the server returns a CAPTCHA HTML page until solved.
- **Important limitation (automation):** The current attack scripts treat any HTTP **200** as “success”, and the CAPTCHA page returns 200. For accurate CAPTCHA demonstrations, use the **browser** (manual) flow.

### 6.5 Anomaly Detection (Burst Rule)

- **Defense name:** Anomaly detection
- **Addresses:** Sudden bursts of attempts from one IP.
- **Implementation:** `check_anomaly()` in `app/defenses.py`, enforced in `app/routes.py`.
- **Config keys:**
  - `ANOMALY_DETECTION`
  - `ANOMALY_THRESHOLD` (default 20 attempts per 60 seconds)
- **Mitigation:** When threshold exceeded:
  - prints console alert: `[ANOMALY ALERT] ...`
  - returns HTTP **429** with `{"error":"Suspicious activity detected"}`

### 6.6 MFA Simulation (OTP)

- **Defense name:** MFA (simulated)
- **Addresses:** Password compromise (even if password is correct, second factor required).
- **Implementation:** `mfa_verify()` in `app/routes.py` + `app/templates/mfa.html`.
- **Config key:** `MFA_ENABLED`
- **Mitigation:** After successful password check, user is redirected to `/mfa_verify`. The OTP is printed to the Flask console (test-only behavior).

### 6.7 Pwned Password Check (HaveIBeenPwned)

- **Defense name:** Pwned password check (HIBP)
- **Addresses:** Use of known-compromised passwords (reduces credential stuffing effectiveness).
- **Implementation:** `check_pwned_password()` in `app/defenses.py`.
- **Config keys:**
  - `PWNED_CHECK_ENABLED` (default in this repo: **True**)
  - `HIBP_API_URL` (k-anonymity endpoint)
  - `HIBP_API_TIMEOUT`
- **Mitigation:** If password is found in HIBP response:
  - blocks login with HTTP **403**
  - error includes breach count when available
- **Availability behavior:** If HIBP is slow/unreachable, the implementation **fails open** (allows login) to avoid user lockouts.

### 6.8 Password Strength Checker (Implemented but Not Enforced Here)

- **Defense name:** Password strength checker (helper)
- **Addresses:** Weak password selection (at registration/change time).
- **Implementation:** `check_password_strength()` in `app/defenses.py`.
- **Config key:** `PASSWORD_STRENGTH`
- **Current limitation:** There is no registration/password-change route in this build that calls `check_password_strength()`. The function exists, but turning the toggle ON will not change login behavior.

---

## 7. Attack vs Defense Mapping

| Attack                  | Primary goal             | Defenses that mitigate                                          | Notes / limitations                                                                                                                       |
| ----------------------- | ------------------------ | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Brute force             | Crack one account        | Rate limiting, account lockout, CAPTCHA, anomaly detection, MFA | CAPTCHA/MFA require interactive flow; scripts may misreport success for CAPTCHA because of HTTP 200 HTML                                  |
| Credential stuffing     | Compromise many accounts | Rate limiting, anomaly detection, MFA, pwned-password check     | Lockout helps per-account but attacker can switch accounts                                                                                |
| Distributed/IP rotation | Bypass IP-based controls | Account lockout, CAPTCHA, MFA, pwned-password check             | IP rotation affects only defenses that trust `X-Forwarded-For` (this app does for some checks). Flask-Limiter uses remote_addr by default |
| Username enumeration    | Discover valid usernames | Generic errors help; constant-time responses recommended        | This project includes a timing-based enumeration script to illustrate timing leaks                                                        |

Effectiveness & limitations (high-level):

- **Single defenses** are rarely sufficient.
- **Defense-in-depth** (rate limit + lockout + CAPTCHA + MFA + monitoring) provides the strongest mitigation.

---

## 8. Expected Results & Outputs

### 8.1 Setup / Start-up Outputs

**Flask (`python run.py`)** prints a banner similar to:

```
LOGIN SECURITY TESTBED
URL: http://localhost:5000
Press CTRL+C to stop
```

**Streamlit (`streamlit run dashboard\app.py`)** prints:

- `Local URL: http://localhost:8501`

### 8.2 Normal Usage Indicators

Success indicators:

- Browser can open http://localhost:5000
- Login with `admin/admin123` shows dashboard page and logout button.
- Streamlit shows increasing “Total Attempts” after logins.

Failure indicators:

- Attack script reports connection errors → Flask not running / wrong port.
- Streamlit shows “No login attempts recorded yet” → no attempts in DB (or DB missing tables).

### 8.3 Attack Script Outputs

All attack scripts print:

- a banner
- target and input file
- a summary block

Common status indicators:

- `[SUCCESS]` → script believes login succeeded
- `[BLOCKED]` or `ATTACK BLOCKED` → HTTP 403/429
- `[FAIL]` → invalid credentials

Saved artifacts (when `--save` used):

- `results\bruteforce_*.json`
- `results\credential_stuffing_*.json`
- `results\distributed_*.json`
- `results\username_enum_*.json`

### 8.4 Defense Outputs (HTTP + UI)

- **Invalid credentials:** HTTP **401** JSON: `{"error":"Invalid credentials"}`
- **IP blocked:** HTTP **403** JSON: `{"error":"Your IP has been blocked"}`
- **Anomaly / lockout / limiter:** HTTP **429** JSON with reason
- **CAPTCHA triggered:** HTML page `captcha.html` (HTTP 200)
- **MFA enabled:** redirect to `/mfa_verify`; OTP printed to Flask console
- **HIBP pwned:** HTTP **403** JSON with breach count message

### 8.5 Experiment Runner Outputs

After `python run_experiments.py` completes:

- `results\experiment_results.csv`
- `results\graphs\*.html`

Open graphs:

```bat
start results\graphs\success_rate_comparison.html
```

---

## 9. Demonstration Flow (Live Demo Script)

This is a clean, presentation-ready script that follows the required sequence:

1. Setup → 2) Normal usage → 3) Trigger attack → 4) Show vulnerability → 5) Enable defense → 6) Show mitigation

### Demo Prep (1 minute)

- Ensure three terminals available.
- In each terminal (if needed):
  ```bat
  cd "F:\IEH lab project"
  venv\Scripts\activate
  ```

### Step 1 — Setup (Terminals 1 & 2)

1. **Terminal 1:**
   ```bat
   python run.py
   ```
2. **Terminal 2:**
   ```bat
   streamlit run dashboard\app.py
   ```
3. Open browser tabs:
   - Flask app: http://localhost:5000
   - Streamlit: http://localhost:8501

### Step 2 — Normal Usage (Manual login)

1. In Flask tab, log in:
   - Username: `admin`
   - Password: `admin123`
2. Show:
   - Protected dashboard page
   - Streamlit shows logged attempts

### Step 3 — Trigger an Attack (Baseline)

> For the clearest baseline demonstration, set defenses OFF in `config.py`.

Recommended baseline toggle set:

```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
MFA_ENABLED = False
PWNED_CHECK_ENABLED = False  # makes baseline purely vulnerable
```

Restart Flask after edits.

**Terminal 3:**

```bat
python attacks\attack_bruteforce.py -u admin -w wordlists\passwords.txt -v
```

Type `yes` to confirm.

### Step 4 — Show the Vulnerability

Call out:

- How quickly attempts accumulate.
- The dashboard spike in attempts/minute.
- Attack script summary showing success and short duration.

### Step 5 — Enable a Defense (Rate limiting)

1. Edit `config.py`:
   ```python
   RATE_LIMIT_ENABLED = True
   RATE_LIMIT_REQUESTS = 8
   ```
2. Restart Flask (Ctrl+C → `python run.py`).
3. (Optional for clean charts): delete DB
   ```bat
   del database.db
   ```

### Step 6 — Show Mitigation

Run the brute force attack again. Expected behavior:

- Attack gets HTTP 429 and stops (or slows dramatically).
- Streamlit “Blocked” increases (note: if Flask-Limiter blocks before route code runs, those blocks may not be logged).

### Step 7 — Demonstrate Defense-in-Depth (Lockout + MFA)

1. Set in `config.py`:
   ```python
   RATE_LIMIT_ENABLED = False
   ACCOUNT_LOCKOUT = True
   MFA_ENABLED = True
   ```
2. Restart Flask.
3. Run brute force again → expect block after ~5 failures (lockout).
4. Then do a **manual login** in the browser:
   - Successful password entry redirects to MFA page
   - OTP printed in Terminal 1
   - Enter OTP to complete login

### Optional Step — Show HIBP Breach Check

1. Set:
   ```python
   PWNED_CHECK_ENABLED = True
   ```
2. Restart Flask.
3. Attempt a login with a commonly breached password (example used in project docs: `password123`).

Expected:

- Login blocked with a message including breach count (if API reachable).
- If offline/timeout: console prints timeout and the system fails open.

---

## 10. Cleanup & Reset (Optional)

### Reset for a fresh demo run

1. Stop services:

- Flask terminal: Ctrl+C
- Streamlit terminal: Ctrl+C

2. Clear database:

```bat
del database.db
```

3. (Optional) Clear results artifacts:

```bat
del results\*.json
```

4. Restart Flask + Streamlit.

### One-command helpers

- `manage_database.bat` → stats / clear / init

---

## Appendix — Key Files (Where to Look)

- **Configuration:** `config.py`
- **Flask app factory:** `app\__init__.py`
- **Routes (login pipeline):** `app\routes.py`
- **Defenses:** `app\defenses.py`
- **Models / schema:** `app\models.py`
- **Attack scripts:** `attacks\*.py`
- **Dashboard:** `dashboard\app.py`
- **Experiments:** `run_experiments.py`
- **Wordlists:** `wordlists\*.txt`
- **Results:** `results\*`
