# Login System Security Testing Against Brute-Force and Credential Stuffing Attacks

> **Type:** Cybersecurity Lab Project | **Context:** Ethical Hacking / Security Research  
> **Institution:** RV College of Engineering | **Course:** Lab EL  
> **Team:** Saksham (1RV23CY047), Anjali (1RV23CY065), Aaditya Raj (1RV23CY001), Kavya (1RV23CY025)

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Objectives & Task Tracker](#2-objectives--task-tracker)
3. [System Architecture](#3-system-architecture)
4. [Technology Stack](#4-technology-stack)
5. [Implementation Plan](#5-implementation-plan)
6. [Metrics & Evaluation](#6-metrics--evaluation)
7. [Experiment Design](#7-experiment-design)
8. [Ethical Considerations](#8-ethical-considerations)
9. [Deliverables](#9-deliverables)
10. [Progress Dashboard](#10-progress-dashboard)

---

## 1. Project Overview

### Description

This project builds a **controlled cybersecurity testbed** to simulate, measure, and defend against two of the most common automated authentication attacks:

- **Brute-Force Attacks** — systematic password guessing using dictionaries or exhaustive enumeration
- **Credential Stuffing Attacks** — automated login attempts using username:password pairs leaked from prior breaches

The system consists of three integrated layers: a deliberately vulnerable Flask login application (the _target_), Python-based attack simulation scripts (the _attacker side_), and a toggleable defense layer with real-time monitoring (the _defender side_).

### Scope & Boundaries

| In Scope                                 | Out of Scope                        |
| ---------------------------------------- | ----------------------------------- |
| Simulated attacks on locally hosted app  | Attacks on any live/external system |
| Synthetic/fictional user credential data | Real user data of any kind          |
| Defense mechanism evaluation             | Production deployment               |
| Rule-based anomaly detection             | ML-based threat intelligence        |
| Basic OTP-based MFA simulation           | Full OAuth / SSO integration        |
| HaveIBeenPwned API (simulated locally)   | Actual breach database queries      |

All testing is performed exclusively within a sandboxed local environment. No real users, systems, or credentials are involved at any stage.

### Expected Final Output

1. A working vulnerable login web application (Flask + SQLite)
2. Three attack scripts covering brute-force, credential stuffing, and distributed attack scenarios
3. Five toggleable defense mechanisms with measurable outcomes
4. A real-time monitoring dashboard (Streamlit) showing live attack telemetry
5. A structured results report with comparative metrics across defense configurations
6. A final hardening guide with actionable recommendations

---

## 2. Objectives & Task Tracker

### Legend

- `[ ]` Not Started
- `[~]` In Progress
- `[x]` Completed

---

### MILESTONE 1 — Environment Setup & Project Foundation

**OBJ-1: Set up development environment and project structure**

| ID       | Task                                                              | Status | Depends On |
| -------- | ----------------------------------------------------------------- | ------ | ---------- |
| TASK-1.1 | Install Python 3.10+, Flask, SQLite, pip dependencies             | [x]    | —          |
| TASK-1.2 | Create project repository with folder structure (see §5)          | [x]    | TASK-1.1   |
| TASK-1.3 | Create `requirements.txt` with all dependencies                   | [x]    | TASK-1.1   |
| TASK-1.4 | Set up virtual environment (`venv`)                               | [x]    | TASK-1.1   |
| TASK-1.5 | Create `.env` file for config (secret key, DB path, toggle flags) | [x]    | TASK-1.2   |
| TASK-1.6 | Initialize SQLite database with schema                            | [x]    | TASK-1.2   |
| TASK-1.7 | Populate DB with 20 synthetic dummy user accounts                 | [x]    | TASK-1.6   |
| TASK-1.8 | Create `config.py` with defense toggle flags (all OFF by default) | [x]    | TASK-1.5   |

---

### MILESTONE 2 — Vulnerable Login System (Target)

**OBJ-2: Build the intentionally vulnerable login application**

| ID       | Task                                                                  | Status | Depends On   |
| -------- | --------------------------------------------------------------------- | ------ | ------------ |
| TASK-2.1 | Build Flask login route (`POST /login`) with basic auth logic         | [x]    | TASK-1.6     |
| TASK-2.2 | Create login HTML page (minimal, functional)                          | [x]    | TASK-2.1     |
| TASK-2.3 | Create protected dashboard page (visible after successful login)      | [x]    | TASK-2.1     |
| TASK-2.4 | Implement session management with Flask-Login                         | [x]    | TASK-2.1     |
| TASK-2.5 | Store passwords as plain MD5 hash (intentional weakness for Phase 2)  | [x]    | TASK-2.1     |
| TASK-2.6 | Add generic error messages (no username enumeration hints — baseline) | [x]    | TASK-2.1     |
| TASK-2.7 | Verify login works correctly end-to-end (manual test)                 | [~]    | TASK-2.1–2.6 |
| TASK-2.8 | Document all intentional weaknesses in `VULNERABILITIES.md`           | [x]    | TASK-2.7     |

---

### MILESTONE 3 — Logging & Monitoring System

**OBJ-3: Implement comprehensive attempt logging**

| ID       | Task                                                                                             | Status | Depends On         |
| -------- | ------------------------------------------------------------------------------------------------ | ------ | ------------------ |
| TASK-3.1 | Create `login_attempts` table in SQLite (id, ip, username, timestamp, success, blocked)          | [x]    | TASK-1.6           |
| TASK-3.2 | Log every login attempt to DB from `/login` route                                                | [x]    | TASK-3.1, TASK-2.1 |
| TASK-3.3 | Log request headers including X-Forwarded-For (for IP rotation simulation)                       | [x]    | TASK-3.2           |
| TASK-3.4 | Create `metrics` table (attack_type, defense_config, attempts, successes, blocked, duration_sec) | [x]    | TASK-3.1           |
| TASK-3.5 | Write helper function `log_experiment_result()` to save test run summaries                       | [x]    | TASK-3.4           |
| TASK-3.6 | Create `/api/logs` endpoint returning recent attempts as JSON                                    | [x]    | TASK-3.2           |
| TASK-3.7 | Create `/api/metrics` endpoint returning aggregated metrics as JSON                              | [x]    | TASK-3.4, TASK-3.5 |

---

### MILESTONE 4 — Attack Simulation Scripts

**OBJ-4: Build the attacker-side scripts**

| ID        | Task                                                                                      | Status | Depends On         |
| --------- | ----------------------------------------------------------------------------------------- | ------ | ------------------ |
| TASK-4.1  | Create `wordlists/passwords.txt` (500 common passwords, synthetic)                        | [x]    | TASK-1.2           |
| TASK-4.2  | Create `wordlists/credentials.txt` (200 username:password pairs, synthetic)               | [x]    | TASK-1.2           |
| TASK-4.3  | Create `wordlists/usernames.txt` (50 synthetic usernames)                                 | [x]    | TASK-1.2           |
| TASK-4.4  | Build `attack_bruteforce.py` — sequential password guessing against one username          | [x]    | TASK-4.1, TASK-2.7 |
| TASK-4.5  | Build `attack_credential_stuffing.py` — tries username:password pairs from list           | [x]    | TASK-4.2, TASK-2.7 |
| TASK-4.6  | Build `attack_distributed.py` — rotates X-Forwarded-For headers to simulate IP rotation   | [x]    | TASK-4.4, TASK-2.7 |
| TASK-4.7  | Add `--verbose` flag to all scripts for live attempt output                               | [x]    | TASK-4.4–4.6       |
| TASK-4.8  | Add metrics export to each script (saves results to `results/` folder)                    | [x]    | TASK-4.4–4.6       |
| TASK-4.9  | Build `attack_username_enum.py` — detects valid usernames via response timing differences | [x]    | TASK-2.7           |
| TASK-4.10 | Verify all scripts work against the unprotected app                                       | [~]    | TASK-4.4–4.9       |

---

### MILESTONE 5 — Defense Mechanisms

**OBJ-5: Implement toggleable defense layer**

| ID        | Task                                                                                | Status | Depends On         |
| --------- | ----------------------------------------------------------------------------------- | ------ | ------------------ |
| TASK-5.1  | Implement **Rate Limiting** — block IP after N requests/minute using Flask-Limiter  | [x]    | TASK-2.1, TASK-1.8 |
| TASK-5.2  | Implement **Account Lockout** — lock account after 5 failed attempts for 15 minutes | [x]    | TASK-3.1, TASK-2.1 |
| TASK-5.3  | Implement **IP Blocking** — permanent ban after 50 failed attempts from single IP   | [x]    | TASK-3.1, TASK-2.1 |
| TASK-5.4  | Implement **Mock CAPTCHA** — math question challenge after 3 failed attempts        | [x]    | TASK-2.2, TASK-2.1 |
| TASK-5.5  | Implement **Rule-Based Anomaly Detection** — alert if >20 attempts in 60 seconds    | [x]    | TASK-3.2           |
| TASK-5.6  | Implement **MFA Simulation** — email OTP (printed to console in test env)           | [x]    | TASK-2.4           |
| TASK-5.7  | Implement **Password Strength Checker** on registration page                        | [x]    | TASK-2.2           |
| TASK-5.8  | Implement **HaveIBeenPwned check** (local simulated version with mock API response) | [x]    | TASK-2.1           |
| TASK-5.9  | Connect all defenses to `config.py` toggle flags (ON/OFF per defense)               | [x]    | TASK-5.1–5.8       |
| TASK-5.10 | Test each defense independently — confirm it activates and deactivates cleanly      | [~]    | TASK-5.9           |

---

### MILESTONE 6 — Dashboard & Visualization

**OBJ-6: Build real-time monitoring dashboard**

| ID       | Task                                                                | Status | Depends On         |
| -------- | ------------------------------------------------------------------- | ------ | ------------------ |
| TASK-6.1 | Set up Streamlit project (`dashboard/app.py`)                       | [x]    | TASK-3.6, TASK-3.7 |
| TASK-6.2 | Build live login attempt feed (auto-refresh every 2 seconds)        | [x]    | TASK-6.1, TASK-3.6 |
| TASK-6.3 | Build attempts-per-minute bar chart using Plotly                    | [x]    | TASK-6.1, TASK-3.6 |
| TASK-6.4 | Build blocked vs. allowed pie chart                                 | [x]    | TASK-6.1, TASK-3.7 |
| TASK-6.5 | Build IP activity heatmap (attempt count per IP)                    | [x]    | TASK-6.1, TASK-3.6 |
| TASK-6.6 | Add defense toggle panel in dashboard sidebar                       | [x]    | TASK-6.1, TASK-5.9 |
| TASK-6.7 | Add experiment results comparison table                             | [x]    | TASK-6.1, TASK-3.7 |
| TASK-6.8 | Add anomaly alert banner (triggers when rule-based detection fires) | [x]    | TASK-6.1, TASK-5.5 |
| TASK-6.9 | Test dashboard with a full live attack scenario                     | [~]    | TASK-6.1–6.8       |

---

### MILESTONE 7 — Experiments & Evaluation

**OBJ-7: Run structured experiments and record results**

| ID        | Task                                                         | Status | Depends On          |
| --------- | ------------------------------------------------------------ | ------ | ------------------- |
| TASK-7.1  | Run Scenario 1: All defenses OFF — all three attack scripts  | [ ]    | TASK-4.10, TASK-5.9 |
| TASK-7.2  | Run Scenario 2: Rate limiting ONLY                           | [ ]    | TASK-7.1            |
| TASK-7.3  | Run Scenario 3: Account lockout ONLY                         | [ ]    | TASK-7.1            |
| TASK-7.4  | Run Scenario 4: IP blocking ONLY                             | [ ]    | TASK-7.1            |
| TASK-7.5  | Run Scenario 5: CAPTCHA ONLY                                 | [ ]    | TASK-7.1            |
| TASK-7.6  | Run Scenario 6: All defenses ON (combined)                   | [ ]    | TASK-7.2–7.5        |
| TASK-7.7  | Run Scenario 7: Distributed attack vs. all defenses ON       | [ ]    | TASK-7.6            |
| TASK-7.8  | Record all metrics in `results/experiment_results.csv`       | [ ]    | TASK-7.1–7.7        |
| TASK-7.9  | Generate comparison graphs from results CSV                  | [ ]    | TASK-7.8            |
| TASK-7.10 | Write analysis: which defenses worked, which failed, and why | [ ]    | TASK-7.9            |

---

### MILESTONE 8 — Final Report & Hardening Guide

**OBJ-8: Produce final documentation**

| ID       | Task                                                                            | Status | Depends On |
| -------- | ------------------------------------------------------------------------------- | ------ | ---------- |
| TASK-8.1 | Write project report: Introduction, Architecture, Attacks, Defenses, Results    | [ ]    | TASK-7.10  |
| TASK-8.2 | Write `HARDENING_GUIDE.md` with top 5 recommendations for real-world developers | [x]    | TASK-7.10  |
| TASK-8.3 | Prepare final presentation slides (Phase-II review)                             | [ ]    | TASK-8.1   |
| TASK-8.4 | Prepare live demo script (5–7 min walkthrough)                                  | [ ]    | TASK-8.1   |
| TASK-8.5 | Final code cleanup, comments, README update                                     | [x]    | TASK-8.1   |

---

## 3. System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                    LOCAL TESTBED                         │
│                                                         │
│  ┌──────────────┐    HTTP     ┌────────────────────┐    │
│  │  ATTACK      │ ─────────► │   FLASK LOGIN APP  │    │
│  │  SCRIPTS     │            │   (Target System)  │    │
│  │              │            │                    │    │
│  │ bruteforce   │            │  /login  (POST)    │    │
│  │ cred_stuff   │            │  /dashboard        │    │
│  │ distributed  │            │  /api/logs         │    │
│  │ enum         │            │  /api/metrics      │    │
│  └──────────────┘            └────────┬───────────┘    │
│                                       │                 │
│                               writes  │  reads          │
│                                       ▼                 │
│                            ┌─────────────────┐         │
│                            │   SQLite DB     │         │
│                            │                 │         │
│                            │ • users         │         │
│                            │ • login_attempts│         │
│                            │ • metrics       │         │
│                            │ • blocked_ips   │         │
│                            └────────┬────────┘         │
│                                     │                   │
│                              reads  │                   │
│                                     ▼                   │
│                        ┌────────────────────────┐      │
│                        │  STREAMLIT DASHBOARD   │      │
│                        │                        │      │
│                        │  • Live attempt feed   │      │
│                        │  • Attack charts       │      │
│                        │  • Defense toggles     │      │
│                        │  • Metrics comparison  │      │
│                        └────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### Component Descriptions

**Login Application (Flask)**
The target system. Runs on `localhost:5000`. Handles login requests, applies defense logic based on config flags, logs every attempt to SQLite, and exposes JSON API endpoints for the dashboard.

**Attack Scripts (Python)**
Four standalone Python scripts that send HTTP POST requests to the login endpoint. Each script records attempt count, success count, time taken, and writes a summary to `results/`.

**Defense Layer (Middleware + Config)**
Defense logic lives inside the Flask login route as conditional middleware, controlled by boolean flags in `config.py`. Setting `RATE_LIMIT_ENABLED = True` activates rate limiting without any code changes.

**SQLite Database**
Four tables: `users` (target accounts), `login_attempts` (every request), `metrics` (experiment summaries), `blocked_ips` (IP ban list). Single file, zero configuration.

**Streamlit Dashboard**
Reads directly from SQLite. Runs on `localhost:8501`. Polls the DB every 2 seconds for live updates. Also reads `config.py` to show/toggle defense states.

### Data Flow

1. Attack script sends `POST /login` with username + password
2. Flask checks `config.py` defense flags
3. If defense triggers → 429/403 response + blocked log entry
4. If passes → checks credentials against DB
5. Result (success/fail) written to `login_attempts` table
6. Dashboard polls `/api/logs` and `/api/metrics` every 2 seconds
7. Charts and counters update in real time

---

## 4. Technology Stack

| Layer            | Technology                                    | Purpose                   |
| ---------------- | --------------------------------------------- | ------------------------- |
| Web Framework    | Flask 2.x (Python)                            | Login app backend         |
| Auth             | Flask-Login                                   | Session management        |
| Rate Limiting    | Flask-Limiter                                 | Request throttling        |
| Database         | SQLite 3                                      | Attempt + metrics storage |
| ORM              | SQLAlchemy (optional)                         | DB access layer           |
| Attack Scripts   | Python + `requests`                           | HTTP attack simulation    |
| Dashboard        | Streamlit                                     | Real-time visualization   |
| Charts           | Plotly (via Streamlit)                        | Bar, pie, heatmap charts  |
| Frontend         | Jinja2 + minimal CSS                          | Login page templates      |
| Config           | Python `config.py` + `.env`                   | Defense toggle system     |
| Password Hashing | `hashlib` (MD5 baseline), `bcrypt` (hardened) | Intentional weak → strong |
| OTP (MFA sim)    | `pyotp`                                       | TOTP generation           |
| CAPTCHA          | Custom Flask route (math challenge)           | Bot deterrence simulation |
| Breach Check     | Local mock (`mock_pwned.py`)                  | HaveIBeenPwned simulation |
| Environment      | `python-dotenv`                               | Config from `.env`        |

---

## 5. Implementation Plan

### Repository Structure

```
login-security-testbed/
│
├── app/
│   ├── __init__.py
│   ├── routes.py          # Login, dashboard, API routes
│   ├── models.py          # SQLAlchemy models
│   ├── defenses.py        # Defense middleware functions
│   ├── logger.py          # Attempt logging helpers
│   └── templates/
│       ├── login.html
│       ├── dashboard.html
│       └── captcha.html
│
├── attacks/
│   ├── attack_bruteforce.py
│   ├── attack_credential_stuffing.py
│   ├── attack_distributed.py
│   └── attack_username_enum.py
│
├── wordlists/
│   ├── passwords.txt
│   ├── credentials.txt
│   └── usernames.txt
│
├── dashboard/
│   └── app.py             # Streamlit dashboard
│
├── results/
│   ├── experiment_results.csv
│   └── graphs/
│
├── mock_integrations/
│   └── mock_pwned.py      # Simulated HaveIBeenPwned API
│
├── config.py              # Defense toggle flags
├── database.db            # SQLite DB (auto-created)
├── requirements.txt
├── .env
├── README.md
├── VULNERABILITIES.md
└── HARDENING_GUIDE.md
```

---

### Phase 1 — Environment Setup

_(Corresponds to MILESTONE 1)_

```bash
# 1. Clone/create repo
mkdir login-security-testbed && cd login-security-testbed

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install flask flask-login flask-limiter sqlalchemy \
            requests streamlit plotly pyotp bcrypt \
            python-dotenv

pip freeze > requirements.txt
```

**`config.py` structure:**

```python
# Defense toggles — set to True to enable
RATE_LIMIT_ENABLED     = False
ACCOUNT_LOCKOUT        = False
IP_BLOCKING            = False
CAPTCHA_ENABLED        = False
ANOMALY_DETECTION      = False
MFA_ENABLED            = False
PWNED_CHECK_ENABLED    = False
PASSWORD_STRENGTH      = False

# Thresholds
RATE_LIMIT_REQUESTS    = 10       # requests per minute per IP
LOCKOUT_THRESHOLD      = 5        # failed attempts before lockout
LOCKOUT_DURATION_MIN   = 15       # lockout duration in minutes
IP_BLOCK_THRESHOLD     = 50       # failed attempts before IP ban
ANOMALY_THRESHOLD      = 20       # attempts per 60s to trigger alert
CAPTCHA_TRIGGER        = 3        # failed attempts before CAPTCHA
```

---

### Phase 2 — Build Vulnerable Login System

_(Corresponds to MILESTONE 2)_

**Core login route (`app/routes.py`):**

```python
@app.route('/login', methods=['POST'])
def login():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    username = request.form.get('username')
    password = request.form.get('password')

    # Defense checks run here (only if config flag is True)
    if config.IP_BLOCKING and is_blocked(ip):
        log_attempt(ip, username, success=False, blocked=True)
        return jsonify({'error': 'Blocked'}), 403

    if config.RATE_LIMIT_ENABLED:
        # Flask-Limiter handles this via decorator

    if config.ACCOUNT_LOCKOUT and is_locked(username):
        log_attempt(ip, username, success=False, blocked=True)
        return jsonify({'error': 'Account locked'}), 429

    # Credential check
    user = User.query.filter_by(username=username).first()
    if user and check_password(password, user.password_hash):
        log_attempt(ip, username, success=True, blocked=False)
        if config.MFA_ENABLED:
            return redirect('/mfa_verify')
        return redirect('/dashboard')
    else:
        log_attempt(ip, username, success=False, blocked=False)
        handle_failed_attempt(ip, username)  # updates lockout / IP counters
        return jsonify({'error': 'Invalid credentials'}), 401
```

**Database schema:**

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    locked_until DATETIME
);

CREATE TABLE login_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    username TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    success INTEGER,
    blocked INTEGER,
    attack_type TEXT
);

CREATE TABLE metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attack_type TEXT,
    defense_config TEXT,
    total_attempts INTEGER,
    successful INTEGER,
    blocked INTEGER,
    duration_sec REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE blocked_ips (
    ip TEXT PRIMARY KEY,
    blocked_at DATETIME,
    reason TEXT
);
```

---

### Phase 3 — Attack Simulation

_(Corresponds to MILESTONE 4)_

**`attacks/attack_bruteforce.py` structure:**

```python
import requests, time, argparse

TARGET = "http://localhost:5000/login"

def run(username, wordlist_path, verbose=False):
    results = {"attempts": 0, "success": 0, "blocked": 0, "start": time.time()}

    with open(wordlist_path) as f:
        passwords = f.read().splitlines()

    for password in passwords:
        r = requests.post(TARGET, data={"username": username, "password": password})
        results["attempts"] += 1

        if r.status_code == 200:
            results["success"] += 1
            if verbose: print(f"[SUCCESS] {username}:{password}")
            break
        elif r.status_code in [429, 403]:
            results["blocked"] += 1
            if verbose: print(f"[BLOCKED] after {results['attempts']} attempts")
            break
        else:
            if verbose: print(f"[FAIL] {password}")

    results["duration"] = time.time() - results["start"]
    save_results("bruteforce", results)
    return results
```

**`attacks/attack_distributed.py`** — same as brute force but rotates:

```python
import random

FAKE_IPS = [f"192.168.{random.randint(1,254)}.{random.randint(1,254)}" for _ in range(100)]

def get_headers():
    return {"X-Forwarded-For": random.choice(FAKE_IPS)}

# Pass headers=get_headers() to each requests.post() call
```

---

### Phase 4 — Defense Mechanisms

_(Corresponds to MILESTONE 5)_

Each defense is implemented as a conditional block inside the login route, gated by a `config.py` flag. Key implementations:

**Rate Limiting:**

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute", exempt_when=lambda: not config.RATE_LIMIT_ENABLED)
def login():
    ...
```

**Account Lockout:**

```python
def is_locked(username):
    user = User.query.filter_by(username=username).first()
    if user and user.locked_until and user.locked_until > datetime.utcnow():
        return True
    return False

def handle_failed_attempt(ip, username):
    user = User.query.filter_by(username=username).first()
    if user and config.ACCOUNT_LOCKOUT:
        user.failed_attempts += 1
        if user.failed_attempts >= config.LOCKOUT_THRESHOLD:
            user.locked_until = datetime.utcnow() + timedelta(minutes=config.LOCKOUT_DURATION_MIN)
        db.session.commit()
```

**Anomaly Detection (Rule-Based):**

```python
def check_anomaly(ip):
    sixty_seconds_ago = datetime.utcnow() - timedelta(seconds=60)
    recent = LoginAttempt.query.filter(
        LoginAttempt.ip == ip,
        LoginAttempt.timestamp >= sixty_seconds_ago
    ).count()
    if recent >= config.ANOMALY_THRESHOLD:
        trigger_alert(ip, recent)
        return True
    return False
```

---

### Phase 5 — Monitoring & Logging

_(Corresponds to MILESTONE 3)_

**`app/logger.py`:**

```python
def log_attempt(ip, username, success, blocked, attack_type=None):
    attempt = LoginAttempt(
        ip=ip,
        username=username,
        success=int(success),
        blocked=int(blocked),
        attack_type=attack_type,
        timestamp=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.commit()
```

**API endpoints:**

```python
@app.route('/api/logs')
def api_logs():
    logs = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).limit(100).all()
    return jsonify([l.to_dict() for l in logs])

@app.route('/api/metrics')
def api_metrics():
    total = LoginAttempt.query.count()
    blocked = LoginAttempt.query.filter_by(blocked=1).count()
    success = LoginAttempt.query.filter_by(success=1).count()
    return jsonify({"total": total, "blocked": blocked, "success": success})
```

---

### Phase 6 — Dashboard

_(Corresponds to MILESTONE 6)_

**`dashboard/app.py` skeleton:**

```python
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import time

DB_PATH = "../database.db"

st.title("Login Security Testbed — Live Monitor")

# Auto-refresh
refresh = st.empty()

while True:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM login_attempts ORDER BY timestamp DESC LIMIT 500", conn)
    conn.close()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Attempts", len(df))
    col2.metric("Blocked", df['blocked'].sum())
    col3.metric("Successful", df['success'].sum())

    # Attempts per minute chart
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_grouped = df.groupby(df['timestamp'].dt.floor('min')).size().reset_index(name='count')
    fig = px.bar(df_grouped, x='timestamp', y='count', title="Attempts Per Minute")
    st.plotly_chart(fig)

    # Live feed
    st.subheader("Recent Attempts")
    st.dataframe(df[['timestamp', 'ip', 'username', 'success', 'blocked']].head(20))

    time.sleep(2)
    st.rerun()
```

---

### Phase 7 — Testing & Evaluation

_(Corresponds to MILESTONE 7)_

**Experiment runner script (`run_experiment.py`):**

```python
import subprocess, csv, time, datetime
import config

SCENARIOS = [
    {"name": "No Defense",        "flags": {}},
    {"name": "Rate Limit Only",   "flags": {"RATE_LIMIT_ENABLED": True}},
    {"name": "Lockout Only",      "flags": {"ACCOUNT_LOCKOUT": True}},
    {"name": "IP Block Only",     "flags": {"IP_BLOCKING": True}},
    {"name": "CAPTCHA Only",      "flags": {"CAPTCHA_ENABLED": True}},
    {"name": "All Defenses",      "flags": {"RATE_LIMIT_ENABLED": True,
                                             "ACCOUNT_LOCKOUT": True,
                                             "IP_BLOCKING": True,
                                             "CAPTCHA_ENABLED": True,
                                             "ANOMALY_DETECTION": True}},
]

for scenario in SCENARIOS:
    # Update config flags
    # Run attack scripts
    # Collect metrics from /api/metrics
    # Write to results/experiment_results.csv
    pass
```

---

## 6. Metrics & Evaluation

### Primary Metrics

| Metric                    | Description                                              | How Collected                            |
| ------------------------- | -------------------------------------------------------- | ---------------------------------------- |
| **Attack Success Rate**   | % of attacks that resulted in successful login           | `success / total_attempts * 100` from DB |
| **Time to Compromise**    | Seconds from first attempt to first successful login     | `duration_sec` in metrics table          |
| **Attempts Before Block** | How many requests before defense triggered               | `attempts` counter in attack scripts     |
| **Block Rate**            | % of attempts blocked by defense                         | `blocked / total_attempts * 100`         |
| **False Positive Rate**   | Legitimate users blocked (manual test with normal login) | Manual test during evaluation            |
| **Detection Latency**     | Time from attack start to anomaly alert                  | Timestamp diff in anomaly log            |

### Results Template (`experiment_results.csv`)

```csv
scenario,attack_type,total_attempts,successes,blocked,duration_sec,success_rate,block_rate,timestamp
No Defense,bruteforce,500,1,0,12.3,0.2%,0%,2025-01-01 10:00:00
Rate Limit Only,bruteforce,15,0,14,3.1,0%,93%,2025-01-01 10:05:00
...
```

### Evaluation Criteria

- A defense is **effective** if it reduces attack success rate to 0% or reduces attempts-to-breach by >90%
- A defense has **acceptable false positives** if it does not block a legitimate user performing ≤10 login attempts per minute
- **Combined defenses** should show synergistic effect vs. individual defenses

---

## 7. Experiment Design

### Test Scenarios

| Scenario                    | Defenses Active | Expected Observation                                                              |
| --------------------------- | --------------- | --------------------------------------------------------------------------------- |
| **S1 — Baseline**           | None            | Brute force succeeds within seconds; credential stuffing cracks multiple accounts |
| **S2 — Rate Limiting**      | Rate limit only | Attack slows significantly; eventually succeeds with slower pace                  |
| **S3 — Account Lockout**    | Lockout only    | Single-target attacks blocked; multi-account credential stuffing still works      |
| **S4 — IP Blocking**        | IP block only   | Regular attacks stopped; distributed attack bypasses this defense                 |
| **S5 — CAPTCHA**            | CAPTCHA only    | Automated scripts halted immediately; human-in-loop required                      |
| **S6 — Combined**           | All five        | Near-zero success rate; even distributed attack heavily degraded                  |
| **S7 — Distributed vs All** | All five        | Tests resilience of combined defenses against IP-rotating attacker                |

### Variables

- **Independent:** Defense configuration (which defenses are ON)
- **Dependent:** Attack success rate, block rate, time to compromise
- **Controlled:** Same wordlists, same target accounts, same attack scripts across all scenarios

---

## 8. Ethical Considerations

### Safe Testing Environment

- All attacks run exclusively against `localhost` — never on external systems
- The application is never exposed to the internet during testing
- All user accounts are synthetic (e.g., `user_001@test.local` with generated passwords)
- No real passwords or personal data are used at any stage

### Responsible Usage

- Attack scripts include a warning banner on launch confirming local-only use
- `VULNERABILITIES.md` documents what was intentionally made weak and why
- Code is not published publicly without proper safeguards and disclaimers
- The project is conducted under academic supervision at RVCE

### Legal Awareness

- Testing is conducted solely within the team's own controlled environment
- No external networks, services, or systems are targeted
- This work constitutes ethical security research under academic context
- Students understand that using these scripts against unauthorized systems is illegal under the IT Act, 2000 (India) and equivalent laws

---

## 9. Deliverables

| Deliverable                           | Format                  | Location             |
| ------------------------------------- | ----------------------- | -------------------- |
| Vulnerable login web application      | Flask app (Python)      | `app/`               |
| Attack simulation scripts (4 scripts) | Python                  | `attacks/`           |
| Defense mechanism implementations     | Integrated in Flask app | `app/defenses.py`    |
| Real-time monitoring dashboard        | Streamlit app           | `dashboard/`         |
| Experiment results data               | CSV + graphs            | `results/`           |
| Final project report                  | Markdown / PDF          | `REPORT.md`          |
| Hardening guide                       | Markdown                | `HARDENING_GUIDE.md` |
| Phase-II presentation slides          | PowerPoint              | `presentation/`      |
| Vulnerability documentation           | Markdown                | `VULNERABILITIES.md` |
| README with setup instructions        | Markdown                | `README.md`          |

---

## 10. Progress Dashboard

### Master Checklist

| ID    | Milestone                   | Tasks Total | Completed | Status |
| ----- | --------------------------- | ----------- | --------- | ------ |
| OBJ-1 | Environment Setup           | 8           | 8         | [x]    |
| OBJ-2 | Vulnerable Login System     | 8           | 7         | [~]    |
| OBJ-3 | Logging & Monitoring        | 7           | 7         | [x]    |
| OBJ-4 | Attack Scripts              | 10          | 9         | [~]    |
| OBJ-5 | Defense Mechanisms          | 10          | 9         | [~]    |
| OBJ-6 | Dashboard                   | 9           | 8         | [~]    |
| OBJ-7 | Experiments & Evaluation    | 10          | 0         | [ ]    |
| OBJ-8 | Final Report & Presentation | 5           | 2         | [~]    |

### Progress Summary

| Metric          | Value |
| --------------- | ----- |
| **Total Tasks** | 67    |
| **Completed**   | 50    |
| **In Progress** | 4     |
| **Not Started** | 13    |
| **% Complete**  | 75%   |

### Phase Completion Tracker

| Phase   | Description             | Status                                     |
| ------- | ----------------------- | ------------------------------------------ |
| Phase 1 | Environment Setup       | [x] Completed                              |
| Phase 2 | Vulnerable Login System | [~] In Progress (testing pending)          |
| Phase 3 | Attack Simulation       | [~] In Progress (validation pending)       |
| Phase 4 | Defense Mechanisms      | [~] In Progress (validation pending)       |
| Phase 5 | Monitoring & Logging    | [x] Completed                              |
| Phase 6 | Dashboard               | [~] In Progress (live attack test pending) |
| Phase 7 | Testing & Evaluation    | [ ] Not Started                            |
| Phase 8 | Report & Deliverables   | [~] In Progress                            |

---

_Last updated: Phase-I Review | Next review: Phase-II Demo_
