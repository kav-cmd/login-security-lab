# Defense Configuration Guide

## Overview

SecureLab provides 8 configurable defense mechanisms to protect against various authentication attacks. Each defense can be toggled ON/OFF in real-time through the dashboard or API. This guide explains each defense, how it works, and its impact on both attackers and legitimate users.

---

## Defense Configurations

### 1. Rate Limiting (`RATE_LIMIT_ENABLED`)

**Default:** `False` (OFF)  
**Threshold:** 8 requests per minute per IP address

#### What It Does
Limits the number of login attempts from a single IP address within a time window. When enabled, any IP exceeding 8 requests per minute receives a 429 (Too Many Requests) error.

#### How It Helps
- **Blocks:** Brute force attacks, credential stuffing
- **Slows down:** Automated attack scripts that try many passwords rapidly
- **Protects:** Server resources from being overwhelmed

#### Attack Behavior Comparison

| Config State | Attack Behavior | Attack Success Rate |
|--------------|-----------------|---------------------|
| **OFF** | Attacker can send unlimited login attempts at full speed (100+ req/sec) | High - limited only by network speed |
| **ON** | After 8 attempts in 60 seconds, attacker receives 429 errors and must wait | Very Low - only 8 attempts per minute possible |

#### User Experience

**When OFF:**
- ✅ No restrictions on login attempts
- ✅ Fast, uninterrupted login experience
- ❌ Vulnerable to rapid-fire attacks

**When ON:**
- ✅ Protected from brute force attacks
- ⚠️ Legitimate users who mistype password 8+ times in a minute will be temporarily blocked
- ⚠️ Shared IP addresses (corporate networks, VPNs) may hit limits faster

**Example Attack:**
```bash
# Without rate limiting
python attack_bruteforce.py -u admin -w passwords.txt
# Result: 1000 attempts in 10 seconds

# With rate limiting
python attack_bruteforce.py -u admin -w passwords.txt
# Result: 8 attempts, then 429 errors for 60 seconds
```

---

### 2. Account Lockout (`ACCOUNT_LOCKOUT`)

**Default:** `False` (OFF)  
**Threshold:** 5 failed attempts  
**Lockout Duration:** 15 minutes

#### What It Does
Temporarily locks a user account after a specified number of failed login attempts. The account remains locked for 15 minutes, regardless of the IP address attempting to login.

#### How It Helps
- **Blocks:** Targeted brute force attacks on specific accounts
- **Prevents:** Password guessing attacks
- **Protects:** Individual user accounts from compromise

#### Attack Behavior Comparison

| Config State | Attack Behavior | Attack Success Rate |
|--------------|-----------------|---------------------|
| **OFF** | Attacker can try unlimited passwords for any username | High - only limited by password complexity |
| **ON** | After 5 wrong passwords, account locks for 15 minutes | Very Low - only 5 guesses per 15-minute window |

#### User Experience

**When OFF:**
- ✅ No account lockouts
- ✅ Can retry login unlimited times
- ❌ Accounts vulnerable to password guessing

**When ON:**
- ✅ Accounts protected from brute force
- ❌ Legitimate users who forget password get locked out after 5 attempts
- ❌ Must wait 15 minutes or contact admin to unlock
- ⚠️ Can be weaponized for denial-of-service (attacker locks out legitimate users)

**Example Attack:**
```bash
# Without account lockout
python attack_bruteforce.py -u admin -w 10000_passwords.txt
# Result: All 10,000 passwords tested

# With account lockout
python attack_bruteforce.py -u admin -w 10000_passwords.txt
# Result: Only first 5 passwords tested, then account locked
```

---

### 3. IP Blocking (`IP_BLOCKING`)

**Default:** `False` (OFF)  
**Threshold:** 50 failed attempts in 60 days  
**Duration:** Permanent (until manually removed)

#### What It Does
Permanently blocks IP addresses that accumulate too many failed login attempts over time. Once blocked, the IP cannot access the login endpoint at all.

#### How It Helps
- **Blocks:** Persistent attackers, botnets
- **Prevents:** Long-term credential stuffing campaigns
- **Protects:** System from repeated attack attempts

#### Attack Behavior Comparison

| Config State | Attack Behavior | Attack Success Rate |
|--------------|-----------------|---------------------|
| **OFF** | Attacker can retry from same IP indefinitely | Moderate - depends on other defenses |
| **ON** | After 50 total failures, IP is permanently blocked | Very Low - attacker must change IPs |

#### User Experience

**When OFF:**
- ✅ No IP restrictions
- ✅ Can login from anywhere
- ❌ Attackers can operate from same IP indefinitely

**When ON:**
- ✅ Persistent attackers are permanently blocked
- ❌ Shared IPs (corporate, public WiFi) may get blocked if multiple users fail logins
- ❌ Legitimate users behind blocked IPs cannot access system
- ⚠️ Requires manual intervention to unblock

**Example Attack:**
```bash
# Without IP blocking
# Day 1: 50 failed attempts from 1.2.3.4
# Day 2: 50 more failed attempts from 1.2.3.4 (still works)

# With IP blocking
# Day 1: 50 failed attempts from 1.2.3.4
# Day 2: IP 1.2.3.4 receives 403 Forbidden immediately
```

---

### 4. CAPTCHA (`CAPTCHA_ENABLED`)

**Default:** `False` (OFF)  
**Trigger:** After 3 failed login attempts for a username  
**⚠️ VULNERABILITY:** Math CAPTCHAs are trivially bypassable (see below)

#### What It Does
Requires users to solve a simple math CAPTCHA after multiple failed login attempts. The CAPTCHA must be solved correctly before the login attempt is processed.

**Current Implementation:** Presents arithmetic challenges like "What is 7 + 3?" in plain HTML.

#### How It Helps
- **Blocks:** Basic automated bots without CAPTCHA-solving capability
- **Slows down:** Simple brute force attacks (requires additional step)
- **Distinguishes:** Very basic automation from humans

#### ⚠️ Critical Vulnerability: Math CAPTCHAs Are Bypassable

**The Problem:**
- Math questions are rendered in **plain HTML** (`<div class="captcha-question">`)
- A script can parse the HTML, extract the question, compute the answer in <1ms, and submit
- No visual challenge, no proof-of-work, no behavioral analysis

**Bypass Demonstration:**
```bash
python attacks/attack_captcha_bypass.py -v
# Script automatically solves math CAPTCHAs and continues attacking
```

**Why It Fails:**
1. **Machine-readable format** - Question is in text, not image
2. **Simple arithmetic** - Addition, subtraction, multiplication are trivial to compute
3. **No rate limiting on solving** - Can solve thousands per second
4. **Predictable pattern** - Regex can extract numbers and operators

**Proper CAPTCHA Solutions:**
- **Cloudflare Turnstile** - Proof-of-work challenge, invisible to users
- **hCaptcha** - Image classification + computational challenge
- **reCAPTCHA v3** - Behavioral analysis, no user interaction
- **Image-based CAPTCHA** - Distorted text (still vulnerable to OCR/ML)

#### Attack Behavior Comparison

| Config State | Attack Behavior | Attack Success Rate |
|--------------|-----------------|---------------------|
| **OFF** | Automated scripts run at full speed | High - no human interaction required |
| **ON (Math CAPTCHA)** | Scripts parse HTML, solve math, continue attacking | High - bypass takes <1ms per attempt |
| **ON (Proper CAPTCHA)** | Scripts cannot solve proof-of-work challenges | Very Low - automation breaks |

#### User Experience

**When OFF:**
- ✅ No CAPTCHA challenges
- ✅ Fast login process
- ❌ Vulnerable to automated attacks

**When ON:**
- ⚠️ **Math CAPTCHAs provide minimal protection** - easily bypassed by scripts
- ⚠️ Legitimate users who mistype password 3+ times must solve CAPTCHA
- ⚠️ Adds friction to login process without real security benefit
- ⚠️ Accessibility concerns for users with disabilities

**Example Attack:**
```bash
# Without CAPTCHA
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt
# Result: Script runs automatically

# With Math CAPTCHA (Current Implementation)
python attacks/attack_captcha_bypass.py -u admin -w wordlists/passwords.txt -v
# Result: Script automatically solves CAPTCHAs and continues
# [CAPTCHA] Question: What is 7 + 3?
# [CAPTCHA] Computed answer: 10 (solved in <1ms)
# Attack continues uninterrupted

# With Proper CAPTCHA (Recommended)
python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt
# Result: Script cannot solve proof-of-work challenge, attack fails
```

**Educational Value:**
This implementation intentionally uses a weak CAPTCHA to demonstrate:
1. Why simple text-based challenges fail
2. The importance of proper CAPTCHA implementation
3. How attackers bypass weak defenses
4. The difference between "security theater" and real security

---

### 5. Anomaly Detection (`ANOMALY_DETECTION`)

**Default:** `False` (OFF)  
**Threshold:** 20 attempts in 60 seconds from single IP

#### What It Does
Monitors login attempt patterns and blocks IPs showing suspicious behavior (rapid-fire attempts). Triggers an alert and blocks the IP when threshold is exceeded.

#### How It Helps
- **Detects:** Unusual activity patterns
- **Blocks:** High-velocity attacks
- **Alerts:** Administrators to ongoing attacks

#### Attack Behavior Comparison

| Config State | Attack Behavior | Attack Success Rate |
|--------------|-----------------|---------------------|
| **OFF** | No pattern detection, attacks go unnoticed | Moderate - depends on other defenses |
| **ON** | Rapid attacks trigger immediate block | Low - high-speed attacks blocked quickly |

#### User Experience

**When OFF:**
- ✅ No behavioral monitoring
- ✅ No false positives
- ❌ Attacks not detected until damage is done

**When ON:**
- ✅ Rapid attacks blocked immediately
- ✅ Alerts generated for security team
- ⚠️ Legitimate users testing/debugging may trigger false positives
- ⚠️ Automated testing scripts may be blocked

**Example Attack:**
```bash
# Without anomaly detection
python attack_bruteforce.py -u admin -w passwords.txt --speed fast
# Result: 100 attempts/second, no detection

# With anomaly detection
python attack_bruteforce.py -u admin -w passwords.txt --speed fast
# Result: After 20 attempts in 60 seconds, IP blocked with 429 error
# Console: [ANOMALY ALERT] IP 1.2.3.4 made 20 attempts in 60 seconds
```

---

### 6. Multi-Factor Authentication (`MFA_ENABLED`)

**Default:** `False` (OFF)  
**Method:** Time-based One-Time Password (TOTP)

#### What It Does
Requires a second authentication factor (6-digit code) after successful password verification. Even if an attacker obtains the password, they cannot login without the OTP code.

#### How It Helps
- **Blocks:** Credential theft attacks
- **Protects:** Against stolen/leaked passwords
- **Requires:** Physical access to user's device

#### Attack Behavior Comparison

| Config State | Attack Behavior | Attack Success Rate |
|--------------|-----------------|---------------------|
| **OFF** | Password alone grants access | High - only password needed |
| **ON** | Password + OTP required; attackers cannot proceed without second factor | Very Low - requires compromising two factors |

#### User Experience

**When OFF:**
- ✅ Single-step login (password only)
- ✅ Fast, convenient
- ❌ Password compromise = account compromise

**When ON:**
- ✅ Strong protection against password theft
- ✅ Account secure even if password is leaked
- ❌ Requires additional step every login
- ❌ Requires smartphone/authenticator app
- ⚠️ Lost device = locked out of account

**Example Attack:**
```bash
# Without MFA
# Attacker obtains password: "admin123"
# Login succeeds immediately

# With MFA
# Attacker obtains password: "admin123"
# Login prompts for 6-digit OTP code
# Attacker cannot proceed without user's device
```

**New User Experience:**
- **Registration:** Same process, account created
- **First Login (MFA OFF):** Username + password → Dashboard
- **First Login (MFA ON):** Username + password → OTP prompt → Dashboard

---

### 7. Pwned Password Check (`PWNED_CHECK_ENABLED`)

**Default:** `False` (OFF)  
**Database:** HaveIBeenPwned API (800M+ compromised passwords)

#### What It Does
Checks if the password has been exposed in known data breaches using the HaveIBeenPwned API. Uses k-anonymity to protect user privacy (only first 5 characters of hash are sent).

#### How It Helps
- **Prevents:** Use of compromised passwords
- **Blocks:** Passwords from known breaches
- **Educates:** Users about password security

#### Attack Behavior Comparison

| Config State | Attack Behavior | Attack Success Rate |
|--------------|-----------------|---------------------|
| **OFF** | Common/breached passwords accepted | High - weak passwords work |
| **ON** | Breached passwords rejected immediately | Low - attacker must use unique passwords |

#### User Experience

**When OFF:**
- ✅ Any password accepted (if meets basic requirements)
- ✅ No external API calls
- ❌ Users can set compromised passwords

**When ON:**
- ✅ Prevents use of known-compromised passwords
- ✅ Improves overall security posture
- ❌ Common passwords like "password123" rejected
- ⚠️ Requires internet connection to HIBP API
- ⚠️ Slight delay (API call) during login/registration

**Example Attack:**
```bash
# Without pwned check
# Attacker tries: "password123" → Accepted

# With pwned check
# Attacker tries: "password123"
# Response: "This password was found in 2,384,093 known breaches"
# Login blocked
```

**New User Experience:**
- **Registration (OFF):** Any password accepted
- **Registration (ON):** Common passwords like "password", "123456" rejected with breach count
- **Login (OFF):** No password checking
- **Login (ON):** If user's password is later found in breach, login blocked

---

### 8. Password Strength Enforcement (`PASSWORD_STRENGTH`)

**Default:** `False` (OFF)  
**Requirements:** 
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

#### What It Does
Enforces password complexity requirements during registration and password changes. Weak passwords are rejected before account creation.

#### How It Helps
- **Prevents:** Weak password selection
- **Increases:** Brute force difficulty
- **Enforces:** Security best practices

#### Attack Behavior Comparison

| Config State | Attack Behavior | Attack Success Rate |
|--------------|-----------------|---------------------|
| **OFF** | Users can set weak passwords like "abc" | High - weak passwords easy to guess |
| **ON** | All passwords must meet complexity requirements | Low - stronger passwords harder to crack |

#### User Experience

**When OFF:**
- ✅ Any password accepted (even "123")
- ✅ No complexity requirements
- ❌ Users may choose weak passwords

**When ON:**
- ✅ All accounts have strong passwords
- ✅ Reduced risk of successful brute force
- ❌ Users must remember complex passwords
- ⚠️ May lead to password reuse across sites
- ⚠️ Registration may require multiple attempts

**Example Attack:**
```bash
# Without password strength
# User creates account with password: "abc"
# Attacker cracks it in seconds

# With password strength
# User tries password: "abc" → Rejected
# User must use: "Abc12345" → Accepted
# Attacker needs significantly more time to crack
```

**New User Experience:**
- **Registration (OFF):** Password "test" accepted
- **Registration (ON):** Password "test" rejected → "Password must contain uppercase, lowercase, and numbers"
- Must use password like "Test1234"

---

## Defense Combinations

### Recommended Configurations

#### 1. **Basic Protection** (Minimal Impact)
```
RATE_LIMIT_ENABLED = True
ANOMALY_DETECTION = True
```
- Blocks rapid automated attacks
- Minimal user friction
- Good for public-facing applications

#### 2. **Moderate Protection** (Balanced)
```
RATE_LIMIT_ENABLED = True
ACCOUNT_LOCKOUT = True
CAPTCHA_ENABLED = True
ANOMALY_DETECTION = True
PASSWORD_STRENGTH = True
```
- Strong protection against most attacks
- Some user friction (CAPTCHA, lockouts)
- Recommended for most applications

#### 3. **Maximum Protection** (High Security)
```
All defenses = True
```
- Strongest possible protection
- Significant user friction
- Recommended for high-value targets (banking, healthcare)

#### 4. **No Protection** (Testbed Default)
```
All defenses = False
```
- Demonstrates vulnerabilities
- Educational purposes only
- **Never use in production**

---

## Attack Scenarios

### Scenario 1: Brute Force Attack on Admin Account

**Attacker Goal:** Guess admin password using common password list

| Defense Configuration | Attack Result | Time to Block |
|----------------------|---------------|---------------|
| All OFF | ✗ 10,000 passwords tested in 2 minutes | Never |
| Rate Limit ON | ✗ 8 passwords tested, then blocked | 1 minute |
| Account Lockout ON | ✗ 5 passwords tested, account locked | Immediate |
| CAPTCHA ON | ✗ 3 passwords tested, CAPTCHA required | Immediate |
| All ON | ✗ 3 passwords tested, CAPTCHA + lockout | Immediate |

### Scenario 2: Credential Stuffing (Leaked Passwords)

**Attacker Goal:** Try 1,000 username:password pairs from data breach

| Defense Configuration | Attack Result | Accounts Compromised |
|----------------------|---------------|---------------------|
| All OFF | ✗ All 1,000 pairs tested | 50-100 (5-10%) |
| Rate Limit ON | ✗ 8 pairs per minute | 1-2 |
| IP Blocking ON | ✗ 50 pairs, then IP blocked | 2-5 |
| Pwned Check ON | ✗ Breached passwords rejected | 0 |
| MFA ON | ✗ Even correct passwords need OTP | 0 |

### Scenario 3: Distributed Attack (Botnet)

**Attacker Goal:** Use 100 different IPs to bypass rate limiting

| Defense Configuration | Attack Result | Success Rate |
|----------------------|---------------|--------------|
| Rate Limit Only | ⚠️ 800 attempts/minute (8 per IP) | Moderate |
| Rate Limit + Account Lockout | ✓ 5 attempts per account, then locked | Very Low |
| Rate Limit + Anomaly Detection | ✓ High velocity detected, IPs blocked | Very Low |
| All ON | ✓ Multiple defenses trigger | Near Zero |

---

## User Journey Comparison

### New User Registration

#### All Defenses OFF
1. Click "Sign up"
2. Enter username: "john"
3. Enter password: "123"
4. Click "Create Account"
5. ✅ Account created
6. Redirect to login

#### All Defenses ON
1. Click "Sign up"
2. Enter username: "john"
3. Enter password: "123"
4. ❌ Error: "Password must be at least 8 characters"
5. Enter password: "password"
6. ❌ Error: "Password must contain uppercase, lowercase, and numbers"
7. Enter password: "password123"
8. ❌ Error: "This password was found in 2,384,093 known breaches"
9. Enter password: "MySecure123"
10. ✅ Account created
11. Redirect to login

### Existing User Login

#### All Defenses OFF
1. Enter username: "admin"
2. Enter password: "admin123"
3. ✅ Logged in immediately

#### All Defenses ON
1. Enter username: "admin"
2. Enter password: "wrong1"
3. ❌ Error: "Invalid credentials" (attempt 1/5)
4. Enter password: "wrong2"
5. ❌ Error: "Invalid credentials" (attempt 2/5)
6. Enter password: "wrong3"
7. ❌ Error: "Invalid credentials" (attempt 3/5)
8. 🤖 CAPTCHA appears: "What is 7 + 3?"
9. Enter CAPTCHA answer: "10"
10. Enter password: "wrong4"
11. ❌ Error: "Invalid credentials" (attempt 4/5)
12. Enter password: "wrong5"
13. ❌ Error: "Invalid credentials" (attempt 5/5)
14. 🔒 Account locked for 15 minutes
15. ❌ Error: "Account temporarily locked"

---

## Configuration Best Practices

### For Development/Testing
```python
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
# ... all False
```
- No restrictions during development
- Easy to test multiple scenarios
- Fast iteration

### For Staging/QA
```python
RATE_LIMIT_ENABLED = True
ANOMALY_DETECTION = True
PASSWORD_STRENGTH = True
# Others False
```
- Test defense mechanisms
- Minimal impact on QA workflows
- Catch security issues early

### For Production
```python
# All True except:
CAPTCHA_ENABLED = False  # Only if accessibility is critical
MFA_ENABLED = True       # Strongly recommended
```
- Maximum protection
- Accept user friction for security
- Monitor and adjust based on metrics

---

## Monitoring & Metrics

### Key Metrics to Track

1. **Login Success Rate**
   - OFF: ~95% (legitimate users)
   - ON: ~85-90% (some lockouts/CAPTCHA failures)

2. **Attack Detection Rate**
   - OFF: 0% (no detection)
   - ON: 95%+ (most attacks blocked)

3. **False Positive Rate**
   - OFF: 0% (no blocking)
   - ON: 1-5% (legitimate users blocked)

4. **Average Login Time**
   - OFF: 0.5 seconds
   - ON: 1-3 seconds (CAPTCHA, MFA, API calls)

### Dashboard Metrics
View real-time metrics at http://localhost:8501:
- Total login attempts
- Blocked attempts by defense type
- Top attacking IPs
- Attack pattern classification
- Defense effectiveness rates

---

## Troubleshooting

### "Account temporarily locked"
- **Cause:** Account Lockout defense triggered (5 failed attempts)
- **Solution:** Wait 15 minutes or disable ACCOUNT_LOCKOUT
- **Prevention:** Use correct password or enable MFA

### "Your IP has been blocked"
- **Cause:** IP Blocking defense triggered (50 total failures)
- **Solution:** Disable IP_BLOCKING or manually remove IP from database
- **Prevention:** Don't run attack scripts from your main IP

### "This password was found in breaches"
- **Cause:** Pwned Check defense detected compromised password
- **Solution:** Choose a unique, strong password
- **Prevention:** Use password manager to generate unique passwords

### "Suspicious activity detected"
- **Cause:** Anomaly Detection triggered (20 attempts in 60 seconds)
- **Solution:** Wait 60 seconds or disable ANOMALY_DETECTION
- **Prevention:** Slow down login attempts

---

## API Control

Toggle defenses programmatically:

```bash
# Enable rate limiting
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{"defense_name": "RATE_LIMIT_ENABLED", "value": true}'

# Disable account lockout
curl -X POST http://localhost:5000/api/config \
  -H "Content-Type: application/json" \
  -d '{"defense_name": "ACCOUNT_LOCKOUT", "value": false}'

# Check current configuration
curl http://localhost:5000/api/config
```

---

## Summary

| Defense | Primary Protection | User Impact | Attack Impact |
|---------|-------------------|-------------|---------------|
| Rate Limiting | Brute force | Low | High |
| Account Lockout | Targeted attacks | Medium | Very High |
| IP Blocking | Persistent attackers | Low-Medium | Very High |
| CAPTCHA | Automation | Medium | Very High |
| Anomaly Detection | Rapid attacks | Low | High |
| MFA | Credential theft | Medium-High | Very High |
| Pwned Check | Weak passwords | Low | Medium |
| Password Strength | Weak passwords | Medium | Medium |

**Recommendation:** Enable all defenses in production, accept user friction for security. Disable selectively only when specific use cases require it (e.g., CAPTCHA for accessibility).
