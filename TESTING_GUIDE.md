# Defense Testing & Demonstration Guide

## Quick Start Testing

This guide provides step-by-step instructions for demonstrating each defense mechanism using the included attack scripts.

---

## Prerequisites

1. **Start the Flask application:**

   ```bash
   python run.py
   ```

2. **Start the Streamlit dashboard (optional but recommended):**

   ```bash
   streamlit run dashboard/app.py
   ```

3. **Access points:**
   - Login: http://localhost:5000
   - Dashboard: http://localhost:5000/dashboard
   - Analytics: http://localhost:8501

---

## Test Scenarios

### Scenario 1: Baseline (No Defenses)

**Goal:** Show how vulnerable the system is without any protections

**Configuration:**

```python
# In config.py - all defenses OFF
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
MFA_ENABLED = False
PWNED_CHECK_ENABLED = False
PASSWORD_STRENGTH = False
```

**Test Steps:**

1. **Run brute force attack:**

   ```bash
   python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
   ```

2. **Observe:**
   - Attack runs at full speed (100+ attempts/second)
   - No blocking or throttling
   - System processes all attempts
   - In Streamlit dashboard: See rapid increase in failed attempts

3. **Expected Result:**
   - ✗ 1000+ passwords tested in seconds
   - ✗ No protection mechanisms triggered
   - ✗ System completely vulnerable

**Key Takeaway:** Without defenses, attackers have unlimited attempts at full speed.

---

### Scenario 2: Rate Limiting Defense

**Goal:** Demonstrate how rate limiting slows down attacks

**Configuration:**

```python
RATE_LIMIT_ENABLED = True  # ← Enable this
RATE_LIMIT_REQUESTS = 8    # 8 requests per minute
# All others OFF
```

**Test Steps:**

1. **Enable rate limiting:**
   - Via Dashboard: Toggle "Rate Limiting" ON
   - Via API:
     ```bash
     curl -X POST http://localhost:5000/api/config \
       -H "Content-Type: application/json" \
       -d '{"defense_name": "RATE_LIMIT_ENABLED", "value": true}'
     ```

2. **Run brute force attack:**

   ```bash
   python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
   ```

3. **Observe:**
   - First 8 attempts succeed
   - 9th attempt receives: `429 Too Many Requests`
   - Attack script pauses/fails
   - In Streamlit: See "Blocked" count increase

4. **Expected Result:**
   - ✓ Only 8 attempts per minute allowed
   - ✓ Attack significantly slowed down
   - ✓ 429 errors logged in dashboard

**Key Takeaway:** Rate limiting makes brute force attacks impractical by limiting attempt speed.

**Try This:**

- Wait 60 seconds and run attack again → 8 more attempts allowed
- Run attack from different IP → Each IP gets 8 attempts/minute

---

### Scenario 3: Account Lockout Defense

**Goal:** Show how account lockout protects specific accounts

**Configuration:**

```python
ACCOUNT_LOCKOUT = True     # ← Enable this
LOCKOUT_THRESHOLD = 5      # Lock after 5 failures
LOCKOUT_DURATION_MIN = 15  # Lock for 15 minutes
# All others OFF
```

**Test Steps:**

1. **Enable account lockout:**
   - Via Dashboard: Toggle "Account Lockout" ON

2. **Run targeted attack on admin account:**

   ```bash
   python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
   ```

3. **Observe:**
   - First 5 attempts processed
   - 6th attempt receives: `429 Account temporarily locked`
   - All subsequent attempts blocked for 15 minutes
   - In Streamlit: See account lockout triggered

4. **Expected Result:**
   - ✓ Account locked after 5 failures
   - ✓ Cannot login even with correct password
   - ✓ Must wait 15 minutes

**Try This:**

- Attempt to login with correct password → Still locked
- Try different username → Works (lockout is per-account)
- Wait 15 minutes → Account automatically unlocked

**Key Takeaway:** Account lockout prevents unlimited password guessing on specific accounts.

---

### Scenario 4: CAPTCHA Defense

**Goal:** Demonstrate how CAPTCHA stops automated attacks

**Configuration:**

```python
CAPTCHA_ENABLED = True  # ← Enable this
CAPTCHA_TRIGGER = 3     # Show CAPTCHA after 3 failures
# All others OFF
```

**Test Steps:**

1. **Enable CAPTCHA:**
   - Via Dashboard: Toggle "CAPTCHA" ON

2. **Manual test (browser):**
   - Go to http://localhost:5000
   - Enter username: "testuser"
   - Enter wrong password 3 times
   - On 3rd attempt: CAPTCHA appears with math question
   - Solve CAPTCHA to proceed

3. **Run automated attack:**

   ```bash
   python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
   ```

4. **Observe:**
   - First 3 attempts processed
   - 3rd attempt receives CAPTCHA challenge
   - Automated script cannot solve CAPTCHA
   - Attack fails

5. **Expected Result:**
   - ✓ CAPTCHA appears after 3 failures
   - ✓ Automated scripts blocked
   - ✓ Humans can still login (with extra step)

**Key Takeaway:** CAPTCHA effectively stops automated attacks while allowing human access.

---

### Scenario 4.5: CAPTCHA Bypass Attack (Educational)

**Goal:** Demonstrate that math CAPTCHAs provide no real protection

**Configuration:**

```python
CAPTCHA_ENABLED = True  # ← Enable this
CAPTCHA_TRIGGER = 3     # Show CAPTCHA after 3 failures
# All others OFF
```

**Test Steps:**

1. **Enable CAPTCHA:**
   - Via Dashboard: Toggle "CAPTCHA" ON

2. **Run CAPTCHA bypass attack:**

   ```bash
   python attacks/attack_captcha_bypass.py -v
   ```

3. **Observe:**
   - Script fetches login page and extracts CAPTCHA question from HTML
   - Parses question: "What is 7 + 3?"
   - Computes answer using regex and arithmetic: "10"
   - Submits credentials with computed answer
   - CAPTCHA bypassed in <1ms
   - Attack continues uninterrupted

4. **Expected Result:**
   - ✗ Math CAPTCHA provides zero protection
   - ✗ Script solves CAPTCHAs faster than humans
   - ✗ Attack proceeds at full speed

**Console Output Example:**
```
[CAPTCHA] Question: What is 7 + 3?
[CAPTCHA] Computed answer: 10 (solved in <1ms)
[+] SUCCESS! admin:password123
    [!] CAPTCHA was bypassed automatically
```

**Key Takeaway:** 
- Math CAPTCHAs are "security theater" - they look secure but provide no real protection
- Arithmetic challenges in HTML are trivially machine-solvable
- Use proof-of-work CAPTCHAs (Cloudflare Turnstile, hCaptcha) for real security
- This demonstrates the difference between perceived security and actual security

**Educational Value:**
This scenario teaches:
1. Why simple text-based challenges fail
2. How attackers parse HTML and compute answers programmatically
3. The importance of proper CAPTCHA implementation
4. Defense-in-depth: CAPTCHA alone is insufficient

---

### Scenario 5: Anomaly Detection

**Goal:** Show how anomaly detection catches rapid attacks

**Configuration:**

```python
ANOMALY_DETECTION = True  # ← Enable this
ANOMALY_THRESHOLD = 20    # 20 attempts in 60 seconds
# All others OFF
```

**Test Steps:**

1. **Enable anomaly detection:**
   - Via Dashboard: Toggle "Anomaly Detection" ON

2. **Run high-speed attack:**

   ```bash
   python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
   ```

3. **Observe:**
   - First 20 attempts in 60 seconds processed
   - 21st attempt receives: `429 Suspicious activity detected`
   - Console shows: `[ANOMALY ALERT] IP x.x.x.x made 20 attempts in 60 seconds`
   - IP blocked for remainder of 60-second window

4. **Expected Result:**
   - ✓ Rapid attacks detected immediately
   - ✓ Alert generated
   - ✓ IP temporarily blocked

**Try This:**

- Wait 60 seconds → Counter resets, 20 more attempts allowed
- Run slow attack (1 attempt per 5 seconds) → No anomaly detected

**Key Takeaway:** Anomaly detection identifies and blocks suspicious behavior patterns.

---

### Scenario 6: IP Blocking Defense

**Goal:** Demonstrate permanent IP blocking for persistent attackers

**Configuration:**

```python
IP_BLOCKING = True         # ← Enable this
IP_BLOCK_THRESHOLD = 50    # Block after 50 total failures
# All others OFF
```

**Test Steps:**

1. **Enable IP blocking:**
   - Via Dashboard: Toggle "IP Blocking" ON

2. **Run extended attack (50+ attempts):**

   ```bash
   python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
   ```

3. **Observe:**
   - First 50 failures processed
   - 51st attempt receives: `403 Your IP has been blocked`
   - All subsequent attempts from this IP permanently blocked
   - In Streamlit: See IP added to blocked list

4. **Expected Result:**
   - ✓ IP permanently blocked after 50 failures
   - ✓ Cannot access login page at all
   - ✓ Requires manual unblock

**Try This:**

- Run attack from different IP → Works (blocking is per-IP)
- Try to access login page from blocked IP → 403 Forbidden

**Key Takeaway:** IP blocking permanently removes persistent attackers.

---

### Scenario 7: Multi-Factor Authentication (MFA)

**Goal:** Show how MFA protects against credential theft

**Configuration:**

```python
MFA_ENABLED = True  # ← Enable this
# All others OFF
```

**Test Steps:**

1. **Enable MFA:**
   - Via Dashboard: Toggle "MFA" ON

2. **Manual login test:**
   - Go to http://localhost:5000
   - Enter valid credentials: admin / admin123
   - Redirected to MFA page
   - Check console for OTP code: `[MFA] Your OTP code is: 123456`
   - Enter OTP code
   - Successfully logged in

3. **Run attack with correct password:**

   ```bash
   # Even if attacker has correct password
   python attack_bruteforce.py -u admin -p admin123 -v
   ```

4. **Observe:**
   - Password verification succeeds
   - MFA challenge presented
   - Attacker cannot proceed without OTP
   - Attack fails at MFA stage

5. **Expected Result:**
   - ✓ Password alone insufficient
   - ✓ OTP required for access
   - ✓ Stolen passwords useless

**Key Takeaway:** MFA provides strong protection even when passwords are compromised.

---

### Scenario 8: Pwned Password Check

**Goal:** Prevent use of compromised passwords

**Configuration:**

```python
PWNED_CHECK_ENABLED = True  # ← Enable this
# All others OFF
```

**Test Steps:**

1. **Enable pwned check:**
   - Via Dashboard: Toggle "Pwned Password Check" ON

2. **Test with common password (registration):**
   - Go to http://localhost:5000/register
   - Username: "newuser"
   - Password: "password123"
   - Click "Create Account"
   - Error: "This password was found in 2,384,093 known breaches"

3. **Test with unique password:**
   - Password: "MyUniqueP@ss2024"
   - Account created successfully

4. **Test during login:**
   - Try to login with breached password
   - Login blocked with breach count

5. **Expected Result:**
   - ✓ Common passwords rejected
   - ✓ Breach count displayed
   - ✓ Users forced to choose secure passwords

**Key Takeaway:** Pwned check prevents use of passwords exposed in data breaches.

---

### Scenario 9: Password Strength Enforcement

**Goal:** Ensure all passwords meet complexity requirements

**Configuration:**

```python
PASSWORD_STRENGTH = True  # ← Enable this
# All others OFF
```

**Test Steps:**

1. **Enable password strength:**
   - Via Dashboard: Toggle "Password Strength" ON

2. **Test weak passwords (registration):**
   - Go to http://localhost:5000/register
   - Try password: "abc" → Error: "Password must be at least 8 characters"
   - Try password: "abcdefgh" → Error: "Password must contain uppercase, lowercase, and numbers"
   - Try password: "Abcdefgh" → Error: "Password must contain uppercase, lowercase, and numbers"
   - Try password: "Abcd1234" → ✓ Accepted

3. **Expected Result:**
   - ✓ Weak passwords rejected
   - ✓ All accounts have strong passwords
   - ✓ Brute force becomes harder

**Key Takeaway:** Password strength enforcement raises the minimum security bar.

---

## Combined Defense Testing

### Scenario 10: Layered Defense (Recommended Production Config)

**Goal:** Show how multiple defenses work together

**Configuration:**

```python
RATE_LIMIT_ENABLED = True
ACCOUNT_LOCKOUT = True
CAPTCHA_ENABLED = True
ANOMALY_DETECTION = True
PASSWORD_STRENGTH = True
PWNED_CHECK_ENABLED = True
# MFA and IP_BLOCKING optional
```

**Test Steps:**

1. **Enable all defenses:**
   - Via Dashboard: Toggle all defenses ON

2. **Run brute force attack:**

   ```bash
   python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
   ```

3. **Observe defense layers triggering:**
   - **0-3 attempts:** Processed normally
   - **3rd attempt:** CAPTCHA triggered (automated script fails)
   - **If CAPTCHA bypassed:** Rate limiting kicks in (8/minute)
   - **If rate limit bypassed:** Anomaly detection triggers (20/60s)
   - **If anomaly bypassed:** Account lockout after 5 failures
   - **If continued:** IP blocking after 50 total failures

4. **Expected Result:**
   - ✓ Multiple defense layers
   - ✓ Attack stopped at first layer (CAPTCHA)
   - ✓ Backup defenses ready if first layer fails
   - ✓ System highly secure

**Key Takeaway:** Layered defenses provide defense-in-depth security.

---

## Attack Script Reference

### Brute Force Attack

```bash
# Basic brute force
python attack_bruteforce.py -u admin -w wordlists/passwords.txt

# Verbose output
python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v

# Specific password
python attack_bruteforce.py -u admin -p admin123
```

### Credential Stuffing Attack

```bash
# Use leaked credentials
python attack_credential_stuffing.py -c wordlists/credentials.txt -v

# Test multiple accounts
python attack_credential_stuffing.py -c wordlists/credentials.txt
```

### Distributed Attack

```bash
# Simulate botnet (multiple IPs)
python attack_distributed.py -u admin -w wordlists/passwords.txt -v

# Bypass rate limiting with IP rotation
python attack_distributed.py -u admin -w wordlists/passwords.txt
```

### Username Enumeration

```bash
# Discover valid usernames
python attacks/attack_username_enum.py -u wordlists/usernames.txt -v

# Test specific username
python attacks/attack_username_enum.py -u admin
```

### CAPTCHA Bypass

```bash
# Single user mode (target specific account)
python attacks/attack_captcha_bypass.py -u admin -w wordlists/passwords.txt -v

# Multi-user mode (test multiple accounts)
python attacks/attack_captcha_bypass.py -v

# Custom wordlists (multi-user)
python attacks/attack_captcha_bypass.py -U wordlists/usernames.txt -P wordlists/passwords.txt -v

# With delay between requests
python attacks/attack_captcha_bypass.py -u admin -w wordlists/passwords.txt -v -d 0.5
```

---

## Demonstration Flow

### For Live Presentations

**Part 1: Show Vulnerability (5 minutes)**

1. Start with all defenses OFF
2. Run brute force attack
3. Show how quickly system is compromised
4. Display attack metrics in Streamlit dashboard

**Part 2: Enable Defenses One-by-One (15 minutes)**

1. Enable Rate Limiting → Show attack slowed
2. Enable Account Lockout → Show account protected
3. Enable CAPTCHA → Show automation blocked
4. Enable Anomaly Detection → Show rapid attacks caught
5. Show metrics improving with each defense

**Part 3: Show Layered Defense (5 minutes)**

1. Enable all defenses
2. Run same attack
3. Show attack stopped at first layer
4. Explain defense-in-depth concept

**Part 4: User Experience (5 minutes)**

1. Show legitimate user login (smooth)
2. Show user with wrong password (CAPTCHA after 3 attempts)
3. Show account lockout (after 5 failures)
4. Explain balance between security and usability

---

## Troubleshooting Test Issues

### Attack Script Not Working

```bash
# Check if Flask is running
curl http://localhost:5000

# Check Python dependencies
pip install -r requirements.txt

# Run with verbose flag
python attack_bruteforce.py -u admin -w wordlists/passwords.txt -v
```

### Defenses Not Activating

```bash
# Check current configuration
curl http://localhost:5000/api/config

# Verify defense is enabled
# Should show "true" for enabled defenses

# Check Flask console for errors
# Look for defense trigger messages
```

### Database Issues

```bash
# Reset database
rm database.db
python run.py
# Database will be recreated with dummy users
```

### Rate Limit Not Working

```bash
# Check if using correct IP
# Rate limit is per IP address

# Wait 60 seconds for rate limit to reset
sleep 60

# Try from different IP or use distributed attack
python attack_distributed.py -u admin -w wordlists/passwords.txt
```

---

## Metrics to Monitor

### In Streamlit Dashboard (http://localhost:8501)

1. **Total Attempts** - Should increase during attacks
2. **Blocked Count** - Should increase when defenses active
3. **Success Rate** - Should be low during attacks
4. **Top IPs** - Shows attacking IP addresses
5. **Attempts Per Minute** - Shows attack velocity
6. **Attack Type Breakdown** - Classifies attack patterns

### In Flask Console

Look for these messages:

- `[ANOMALY ALERT] IP x.x.x.x made 20 attempts in 60 seconds`
- `[HIBP] Password detected in X breaches`
- `[MFA] Your OTP code is: XXXXXX`
- `[SECURITY] Pwned password detected`

---

## Quick Reference Card

| Defense           | Enable Command      | Test Attack                     | Expected Block          |
| ----------------- | ------------------- | ------------------------------- | ----------------------- |
| Rate Limiting     | Toggle in dashboard | `attack_bruteforce.py`          | After 8 attempts/min    |
| Account Lockout   | Toggle in dashboard | `attack_bruteforce.py -u admin` | After 5 failures        |
| IP Blocking       | Toggle in dashboard | Run 50+ failed attempts         | After 50 total failures |
| CAPTCHA           | Toggle in dashboard | `attack_captcha_bypass.py`          | Bypassed (math solvable) |
| Anomaly Detection | Toggle in dashboard | Fast attack                     | After 20 in 60s         |
| MFA               | Toggle in dashboard | Login manually                  | After password          |
| Pwned Check       | Toggle in dashboard | Register with "password123"     | Immediately             |
| Password Strength | Toggle in dashboard | Register with "abc"             | Immediately             |

---

## Educational Talking Points

### When Demonstrating to Students/Stakeholders

1. **Without Defenses:**
   - "Notice how the attacker can try thousands of passwords per second"
   - "This is why we need multiple layers of defense"

2. **With Rate Limiting:**
   - "Now the attacker is limited to 8 attempts per minute"
   - "What would take 10 seconds now takes hours"

3. **With Account Lockout:**
   - "Even if they bypass rate limiting, the account locks after 5 failures"
   - "This is why attackers target multiple accounts instead of one"

4. **With CAPTCHA:**
   - "Automated scripts cannot solve CAPTCHAs"
   - "This is the difference between human and bot"

5. **With All Defenses:**
   - "Defense-in-depth means multiple layers"
   - "If one defense fails, others are ready"
   - "This is how real-world systems protect themselves"

---

## Next Steps

After testing all defenses:

1. **Experiment with thresholds** - Adjust values in config.py
2. **Create custom attack scripts** - Test specific scenarios
3. **Monitor real-time metrics** - Use Streamlit dashboard
4. **Document findings** - Record which defenses work best
5. **Present results** - Use this guide for demonstrations

---

## Additional Resources

- **Main Documentation:** `DEFENSE_CONFIGURATION_GUIDE.md`
- **Implementation Summary:** `IMPLEMENTATION_SUMMARY.md`
- **Update Summary:** `UPDATE_SUMMARY.md`
- **Streamlit Dashboard:** http://localhost:8501
- **API Documentation:** Check `/api/config` endpoint
