# Reference

Complete technical specifications, architecture, security analysis, and experiment details.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Attack Methods](#attack-methods)
3. [Defense Mechanisms](#defense-mechanisms)
4. [Vulnerabilities](#vulnerabilities)
5. [Hardening Guide](#hardening-guide)
6. [Experiment Design](#experiment-design)
7. [API Reference](#api-reference)
8. [Database Schema](#database-schema)

---

## System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                    LOCAL TESTBED                         │
│                                                          │
│  ┌──────────────┐                ┌────────────────┐    │
│  │  ATTACK      │ HTTP POST      │  FLASK LOGIN   │    │
│  │  SCRIPTS     │ ─────────────→ │  APP           │    │
│  │              │                │  (Target)      │    │
│  │ - bruteforce │                │                │    │
│  │ - cred_stuff │                │  /login (POST) │    │
│  │ - distributed│                │  /api/logs     │    │
│  │ - enum       │                │  /api/metrics  │    │
│  └──────────────┘                └────────┬───────┘    │
│                                           │             │
│                                  writes/reads           │
│                                           │             │
│                                   ┌───────▼────────┐   │
│                                   │  SQLite DB     │   │
│                                   │                │   │
│                                   │ • users        │   │
│                                   │ • login_att    │   │
│                                   │ • metrics      │   │
│                                   │ • blocked_ips  │   │
│                                   └────────┬───────┘   │
│                                            │           │
│                                     reads  │           │
│                                            ▼           │
│                         ┌────────────────────────────┐ │
│                         │  STREAMLIT DASHBOARD       │ │
│                         │  localhost:8501            │ │
│                         │                            │ │
│                         │ • Live attempt feed        │ │
│                         │ • Real-time charts         │ │
│                         │ • Defense status           │ │
│                         │ • IP activity heatmap      │ │
│                         └────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Component Details

**Flask Application (Port 5000)**
- Single login route: `POST /login`
- Accepts: `username`, `password`
- Returns: Redirect (success) or JSON error (failure)
- Logs every attempt to database
- Defense logic integrated as conditional middleware

**Attack Scripts**
- Python + `requests` library
- Send HTTP POST to `/login`
- Track: attempts, successes, blocks, duration
- Export: JSON results with detailed metrics
- Run independently or via `run_experiments.py`

**SQLite Database**
- Auto-created on first run
- Four tables: `users`, `login_attempts`, `metrics`, `blocked_ips`
- Single file: `database.db` (no external service)

**Streamlit Dashboard**
- Reads directly from SQLite
- Auto-refreshes every 2 seconds
- Real-time chart updates
- Shows current defense configuration

### Data Flow

1. Attack script sends `POST /login` with username + password
2. Flask checks defense conditions in `app/defenses.py`
3. If defense triggers → returns 429/403 + logs blocked attempt
4. If passes → verifies credentials via MD5 hash comparison
5. Logs result (success/fail) to `login_attempts` table
6. Dashboard polls database every 2 seconds for updates
7. Charts and metrics update in real-time

---

## Attack Methods

### 1. Brute Force Attack

**What it does:** Systematically tries passwords from a wordlist against a single account.

**Script:** `attacks/attack_bruteforce.py`

**Command:**
```bash
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v --save
```

**Mechanism:**
- Load 500 common passwords from wordlist
- Try each password in sequence
- Stop when correct password found or wordlist exhausted
- Track: attempts, duration, success

**Expected Results (No Defenses):**
- Success: ~100%
- Time: 5-10 seconds
- Attempts: ~50-100

### 2. Credential Stuffing

**What it does:** Tests username:password pairs from leaked databases.

**Script:** `attacks/attack_credential_stuffing.py`

**Command:**
```bash
python attacks/attack_credential_stuffing.py -c wordlists/credentials.txt -v --save
```

**Mechanism:**
- Load 200 username:password pairs from wordlist
- Try each pair against login endpoint
- Track compromised accounts
- Simulates attacker using leaked databases

**Expected Results (No Defenses):**
- Success: ~5-10 accounts compromised
- Time: 30-60 seconds
- Useful against systems with multiple accounts

### 3. Distributed Attack

**What it does:** Rotates fake IP addresses to bypass IP-based defenses.

**Script:** `attacks/attack_distributed.py`

**Command:**
```bash
python attacks/attack_distributed.py -u admin -w wordlists/passwords.txt -p 50 -v --save
```

**Mechanism:**
- Generate 50 fake IP addresses
- Send each request from different IP (via X-Forwarded-For header)
- Distributes failed attempts across many IPs
- Bypasses per-IP rate limiting and IP blocking

**Expected Results (IP Blocking Only):**
- Success: ~80% (different IPs bypass IP block)
- Time: Faster than regular brute force
- Shows limitation of IP-based defenses

### 4. Username Enumeration

**What it does:** Detects valid usernames via response time differences.

**Script:** `attacks/attack_username_enum.py`

**Command:**
```bash
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v
```

**Mechanism:**
- Try usernames with dummy password
- Valid users: slower response (password check happens)
- Invalid users: faster response (early rejection)
- Time difference reveals valid accounts

**Defense:** Generic error messages prevent this. Our implementation already mitigates this.

---

## Defense Mechanisms

### 1. Rate Limiting

**What it does:** Restricts login attempts to N per minute from a single IP.

**Configuration:**
```python
RATE_LIMIT_ENABLED = True
RATE_LIMIT_REQUESTS = 10  # per minute
```

**Implementation:** Flask-Limiter decorator on `/login` route

**How it blocks:**
- Tracks requests per IP
- After 10 attempts/minute → returns 429 (Too Many Requests)
- Attack must wait before continuing

**Effectiveness:**
- ✅ Slows down attacks dramatically
- ⚠️ Can be bypassed by waiting or IP rotation
- ⚠️ Slows legitimate users on slow connections

**Expected Success Rate:** ~10% (if attacker waits)

### 2. Account Lockout

**What it does:** Temporarily locks account after N failed attempts.

**Configuration:**
```python
ACCOUNT_LOCKOUT = True
LOCKOUT_THRESHOLD = 5         # failures before lockout
LOCKOUT_DURATION_MIN = 15     # lockout duration
```

**Implementation:** Tracks `failed_attempts` in user record, sets `locked_until` timestamp

**How it blocks:**
- Count failed login attempts
- After 5 failures → lock account until 15 minutes pass
- Subsequent attempts return 429 (Account Locked)

**Effectiveness:**
- ✅ Very effective against single-account attacks
- ⚠️ Fails against credential stuffing (different accounts)
- ⚠️ Locks out legitimate users with wrong password

**Expected Success Rate:** ~0% (single account), ~90% (multiple accounts)

### 3. IP Blocking

**What it does:** Permanently bans IPs after many failed attempts.

**Configuration:**
```python
IP_BLOCKING = True
IP_BLOCK_THRESHOLD = 50  # attempts before ban
```

**Implementation:** Counts failed attempts per IP over 60 days, adds to `blocked_ips` table

**How it blocks:**
- Track attempts per IP
- After 50 failures from same IP → add to block list
- Blocked IPs get 403 (Forbidden)

**Effectiveness:**
- ✅ Good against single attacker
- ⚠️ Completely bypassed by IP rotation
- ⚠️ Can block legitimate users on shared networks

**Expected Success Rate:** ~5% (with IP rotation)

### 4. CAPTCHA Challenge

**What it does:** Requires solving a math puzzle after failed attempts.

**Configuration:**
```python
CAPTCHA_ENABLED = True
CAPTCHA_TRIGGER = 3  # failures before CAPTCHA
```

**Implementation:** Generates random math question (a + b = ?) after 3 failures

**How it blocks:**
- Track failed attempts per user
- After 3 failures → show CAPTCHA
- Must solve correctly to proceed
- Automated scripts cannot solve

**Effectiveness:**
- ✅ Most effective single defense
- ✅ Stops automated attacks 100%
- ⚠️ Affects legitimate user experience
- ⚠️ CAPTCHA farms exist (human solving)

**Expected Success Rate:** ~0% (attacks cannot solve)

### 5. Anomaly Detection

**What it does:** Alerts when suspicious patterns detected.

**Configuration:**
```python
ANOMALY_DETECTION = True
ANOMALY_THRESHOLD = 20  # attempts per 60 seconds
```

**Implementation:** Counts attempts from IP in last 60 seconds, triggers alert if threshold exceeded

**How it works:**
- Monitor login attempts in real-time
- If >20 attempts from single IP in 60 seconds → trigger alert
- Prints warning to Flask console
- Logs anomaly in dashboard

**Effectiveness:**
- ✅ Detects attacks in progress
- ℹ️ Alerting only (doesn't block automatically)
- ⚠️ Rule-based (doesn't adapt to new patterns)

**Expected:** No automatic blocking, but provides visibility

### 6. MFA (Multi-Factor Authentication)

**What it does:** Requires secondary authentication (OTP).

**Configuration:**
```python
MFA_ENABLED = True
```

**Implementation:** Uses pyotp TOTP, prints code to console in test environment

**How it works:**
- After password verified, user redirected to MFA page
- System generates TOTP code and prints to console
- User must enter correct code

**Effectiveness:**
- ✅ Prevents access even with correct password
- ⚠️ Adds friction to legitimate users
- ⚠️ Not bypassed by password attacks

### 7. Password Strength Check

**What it does:** Enforces minimum password complexity requirements.

**Configuration:**
```python
PASSWORD_STRENGTH = True
```

**Implementation:** Checks for min length (8), uppercase, lowercase, digits

**Effectiveness:**
- ✅ Prevents weak passwords
- ℹ️ Only checked at registration (not login attacks)

### 8. Pwned Password Check

**What it does:** Checks if password exists in known breach databases.

**Configuration:**
```python
PWNED_CHECK_ENABLED = True
```

**Implementation:** Local simulated list of 10 common passwords

**How it works:**
- Check if password exists in known leaked passwords list
- If found → block login with message "Password is too common"

**Effectiveness:**
- ✅ Prevents use of publicly known passwords
- ⚠️ Simulated (real version uses HaveIBeenPwned API)

---

## Vulnerabilities

### Intentional Weaknesses (Educational)

**1. MD5 Password Hashing**
- **Weakness:** Cryptographically broken, not salted
- **Impact:** Password hashes can be cracked offline
- **Why intentional:** Shows vulnerability of old hashing
- **Production fix:** Use bcrypt, Argon2, or scrypt

**2. No Rate Limiting (Default)**
- **Weakness:** Unlimited login attempts
- **Impact:** Brute force attacks complete in seconds
- **Why intentional:** Shows default vulnerability
- **Production fix:** Enable rate limiting by default

**3. No Account Lockout (Default)**
- **Weakness:** Accounts never lock, even after many failures
- **Impact:** Unlimited attempts against single account
- **Why intentional:** Demonstrates need for lockout
- **Production fix:** Implement account lockout with reasonable thresholds

**4. No CAPTCHA (Default)**
- **Weakness:** No bot detection
- **Impact:** Automated attacks proceed unimpeded
- **Why intentional:** Shows effectiveness of CAPTCHA
- **Production fix:** Add CAPTCHA after few failures

**5. No Multi-Factor Authentication (Default)**
- **Weakness:** Single factor only
- **Impact:** Password compromise = full account compromise
- **Why intentional:** Shows limitation of passwords alone
- **Production fix:** Implement MFA for sensitive accounts

**6. No IP-Based Defenses (Default)**
- **Weakness:** Malicious IPs never blocked
- **Impact:** Attacker can retry indefinitely
- **Why intentional:** Shows value of IP blocking (and its limitations)
- **Production fix:** Block IPs with anomalous activity

---

## Hardening Guide

### Production-Ready Security Checklist

#### Password Security

- [ ] Use bcrypt/Argon2 (not MD5)
- [ ] Use salt (auto in bcrypt)
- [ ] Minimum 12+ characters
- [ ] Require complexity (upper, lower, digit, symbol)
- [ ] Check against breach databases (HaveIBeenPwned)
- [ ] Implement password history (prevent reuse)

#### Rate Limiting & Account Protection

- [ ] Enable rate limiting by default (5-10 attempts/minute)
- [ ] Implement account lockout (3-5 attempts, 15-30 minutes)
- [ ] Ban IPs after threshold (50+ attempts)
- [ ] Log failed attempts for analysis
- [ ] Alert on suspicious patterns

#### Multi-Factor Authentication

- [ ] Require MFA for sensitive accounts
- [ ] Support TOTP apps (Authenticator, Authy, Google Authenticator)
- [ ] Support hardware keys (Yubikey, Google Titan)
- [ ] SMS only as fallback (not ideal)
- [ ] No SMS for banking/finance (too vulnerable)

#### Monitoring & Detection

- [ ] Real-time anomaly detection (machine learning preferred)
- [ ] Alert on failed patterns
- [ ] Integration with SIEM (Splunk, ELK)
- [ ] Threat intelligence feeds
- [ ] Geo-velocity checks (impossible travel)

#### Session Management

- [ ] Short session timeouts (15-30 minutes)
- [ ] Regenerate session ID on login
- [ ] Secure cookies (HTTPS only, httponly, sameSite)
- [ ] CSRF protection
- [ ] Device fingerprinting

#### API Security

- [ ] API rate limiting
- [ ] API key rotation
- [ ] OAuth 2.0 for delegated access
- [ ] JWT with short expiry
- [ ] API versioning

#### Infrastructure

- [ ] HTTPS only (HTTP redirects)
- [ ] TLS 1.2+ with strong ciphers
- [ ] WAF (Web Application Firewall)
- [ ] DDoS protection
- [ ] Regular security updates

### Code Review Checklist

- [ ] No hardcoded secrets
- [ ] Input validation on all forms
- [ ] Output escaping (prevent XSS)
- [ ] SQL parameterization (prevent SQLi)
- [ ] CSRF tokens on POST forms
- [ ] Secure redirect handling
- [ ] Error messages don't leak info
- [ ] Logging of security events

### Deployment Checklist

- [ ] Environment-specific configs
- [ ] Secrets in environment variables (not code)
- [ ] Regular backups with encryption
- [ ] Incident response plan
- [ ] Security training for team
- [ ] Third-party security audits
- [ ] Penetration testing before production

---

## Experiment Design

### Seven Test Scenarios

| # | Scenario | Defenses | Expected Success Rate |
|---|----------|----------|----------------------|
| 1 | No Defense (Baseline) | None | ~100% |
| 2 | Rate Limiting Only | Rate limit | ~10% |
| 3 | Account Lockout Only | Lockout | ~0% (single), ~90% (multi) |
| 4 | IP Blocking Only | IP block | ~80% (with IP rotation) |
| 5 | CAPTCHA Only | CAPTCHA | ~0% |
| 6 | All Defenses Combined | All 5 | ~0% |
| 7 | Distributed vs All | All 5 + IP rotation | ~0% |

### Methodology

**Variables:**
- **Independent:** Defense configuration
- **Dependent:** Attack success rate, block rate, attempts before block
- **Controlled:** Same wordlists, same target accounts, same attack scripts

**For Each Scenario:**
1. Set defense configuration in `config.py`
2. Clear database (`del database.db`)
3. Run 3 attacks (bruteforce, credential stuffing, distributed)
4. Record metrics:
   - Total attempts
   - Successful logins
   - Blocked attempts
   - Duration
   - Success rate = (successes / attempts) * 100
   - Block rate = (blocked / attempts) * 100

**Automated Runner:** `run_experiments.py`
- Runs all 7 scenarios automatically
- Executes 21 total experiments (7 scenarios × 3 attacks)
- Takes ~60 minutes
- Generates `results/experiment_results.csv` and graphs

---

## API Reference

### Authentication Endpoints

**Login:**
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin123
```

**Response (Success):**
```
HTTP 302 Redirect
Location: /dashboard
```

**Response (Failure):**
```json
HTTP 401
{
  "error": "Invalid credentials"
}
```

**Response (Blocked):**
```json
HTTP 429
{
  "error": "Account temporarily locked"
}
```

### Data Endpoints (JSON)

**Recent Attempts:**
```http
GET /api/logs?limit=100
```

**Response:**
```json
[
  {
    "id": 1,
    "ip": "127.0.0.1",
    "username": "admin",
    "timestamp": "2026-04-29T12:34:56.789Z",
    "success": false,
    "blocked": false,
    "attack_type": "bruteforce"
  },
  ...
]
```

**Metrics:**
```http
GET /api/metrics
```

**Response:**
```json
{
  "total": 523,
  "blocked": 450,
  "success": 1,
  "failed": 72
}
```

**Configuration:**
```http
GET /api/config
```

**Response:**
```json
{
  "rate_limit": true,
  "account_lockout": false,
  "ip_blocking": false,
  "captcha": false,
  "anomaly_detection": false,
  "mfa": false,
  "pwned_check": true,
  "password_strength": false
}
```

**Statistics:**
```http
GET /api/stats
```

**Response:**
```json
{
  "recent_attempts": 45,
  "unique_ips": 3,
  "top_ips": [
    {"ip": "127.0.0.1", "count": 42},
    {"ip": "192.168.1.1", "count": 3}
  ]
}
```

---

## Database Schema

### Users Table

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  failed_attempts INTEGER DEFAULT 0,
  locked_until DATETIME,
  mfa_secret TEXT
)
```

**Columns:**
- `id` - Primary key
- `username` - Unique username
- `password_hash` - MD5 hash of password (intentionally weak)
- `failed_attempts` - Counter for failed logins
- `locked_until` - Timestamp until which account is locked
- `mfa_secret` - TOTP secret for MFA

### Login Attempts Table

```sql
CREATE TABLE login_attempts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ip TEXT,
  username TEXT,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
  success INTEGER,
  blocked INTEGER,
  attack_type TEXT
)
```

**Columns:**
- `id` - Auto-increment ID
- `ip` - Client IP (respects X-Forwarded-For)
- `username` - Username attempted
- `timestamp` - When attempt occurred
- `success` - 1 if login successful, 0 otherwise
- `blocked` - 1 if request was blocked by defense, 0 otherwise
- `attack_type` - Type of attack (if known)

### Metrics Table

```sql
CREATE TABLE metrics (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  attack_type TEXT,
  defense_config TEXT,
  total_attempts INTEGER,
  successful INTEGER,
  blocked INTEGER,
  duration_sec REAL,
  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

**Purpose:** Stores experiment results for analysis

### Blocked IPs Table

```sql
CREATE TABLE blocked_ips (
  ip TEXT PRIMARY KEY,
  blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  reason TEXT
)
```

**Purpose:** Permanent IP ban list for IP blocking defense

---

## Performance Considerations

### Database

- SQLite suitable for educational/testing purposes
- For production: Use PostgreSQL, MySQL, or similar
- Indexes on `(ip, timestamp)` and `(username, timestamp)` recommended
- Regular vacuuming/optimization needed for long-running tests

### Rate Limiting

- In-memory counter (Flask-Limiter)
- Suitable for single-server testing
- For distributed systems: Use Redis backend

### Dashboard

- Streamlit suitable for monitoring, not production dashboards
- Auto-refresh every 2 seconds keeps CPU reasonable
- For production: Use proper APM tools (New Relic, Datadog, etc.)

---

## Security Notes

⚠️ **This code is intentionally vulnerable for educational purposes only.**

**DO NOT:**
- Deploy to production without hardening
- Use MD5 for passwords
- Leave all defenses off by default
- Use this against systems without authorization

**DO:**
- Study the vulnerabilities
- Understand how each defense works
- Learn why defense-in-depth matters
- Use as reference for secure implementation

**Legal Compliance:**
- All testing performed locally only
- No real systems or data at risk
- Educational purpose compliant with IT Act, 2000
- Use authorized by academic institution (RVCE)

---

This reference serves as comprehensive technical documentation. For practical guidance, see `DEMO.md` or `SETUP.md`.
